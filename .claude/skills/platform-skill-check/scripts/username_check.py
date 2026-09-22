#!/usr/bin/env python3
"""Check whether a handle is registered on a curated set of platforms.

Passive, read-only HTTP/API checks only: one profile or API response per site,
no login, no scraping beyond that single response. Site definitions live in
sites.json, each tagged with the check method that was verified against a real
account and a fabricated one before being added (see ../reference/site-coverage.md)
- do not trust an unverified entry added later without the same calibration.

Uses curl rather than urllib, because macOS python.org builds often lack a CA bundle.

Usage:
  username_check.py HANDLE [--sites sites.json] [--delay 0.5] [--json]

Verdicts per site:
  EXISTS       the check matched the site's "account is real" signature
  NOT_FOUND    the check matched the site's "no such account" signature
  INCONCLUSIVE network error, unexpected status/body, or rate-limited

EXISTS is membership evidence only, never identity proof: handle squatting and
coincidental reuse are common. Corroborate (bio, avatar, linked accounts, join
date) before attributing a hit to a specific person.
"""
import argparse
import json
import os
import subprocess
import sys
import time

DEFAULT_SITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sites.json")


def curl(url, method="GET", headers=None, timeout=10):
    cmd = ["curl", "-s", "-m", str(timeout), "-X", method, "-w", "\n%{http_code}",
           "-A", "Mozilla/5.0 (platform-skill-check; passive OSINT check)"]
    for h in headers or []:
        cmd += ["-H", h]
    cmd.append(url)
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    text, _, code = out.rpartition("\n")
    try:
        return int(code), text
    except ValueError:
        return 0, text


def check_site(site, handle):
    url = site["url"].format(handle=handle)
    code, body = curl(url, method=site.get("method", "GET"), headers=site.get("headers"))
    mode = site["check"]

    if mode == "status":
        if code == site.get("exists_code"):
            verdict = "EXISTS"
        elif code == site.get("missing_code"):
            verdict = "NOT_FOUND"
        else:
            verdict = "INCONCLUSIVE"
    elif mode == "json_null":
        stripped = body.strip()
        if code != 200:
            verdict = "INCONCLUSIVE"  # e.g. Firebase 400 on an invalid path (a "@" in the handle) is an error body, not a hit
        else:
            verdict = "NOT_FOUND" if stripped == "null" else ("EXISTS" if stripped else "INCONCLUSIVE")
    elif mode == "json_status_code":
        try:
            verdict = "EXISTS" if json.loads(body).get("status", {}).get("code") == 0 else "NOT_FOUND"
        except (ValueError, AttributeError):
            verdict = "INCONCLUSIVE"
    elif mode == "string_present":
        verdict = "EXISTS" if site["marker"] in body else "NOT_FOUND"
    elif mode == "string_absent":
        verdict = "NOT_FOUND" if site["marker"] in body else "EXISTS"
    else:
        verdict = "INCONCLUSIVE"

    if code == 0:
        verdict = "INCONCLUSIVE"
    return {"site": site["name"], "url": url, "http": code, "verdict": verdict}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("handle")
    p.add_argument("--sites", default=DEFAULT_SITES)
    p.add_argument("--delay", type=float, default=0.5, help="seconds between requests, be polite")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    with open(args.sites, encoding="utf-8") as f:
        sites = json.load(f)

    results = []
    for i, site in enumerate(sites):
        if i:
            time.sleep(args.delay)
        results.append(check_site(site, args.handle))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    print(f"{'SITE':<12}{'VERDICT':<13}{'HTTP':<6}URL")
    for r in results:
        print(f"{r['site']:<12}{r['verdict']:<13}{r['http']:<6}{r['url']}")
    print()
    print("EXISTS = membership evidence only. Corroborate before attributing to a person.")


if __name__ == "__main__":
    main()
