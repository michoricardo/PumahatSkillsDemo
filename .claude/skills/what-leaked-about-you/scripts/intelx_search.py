#!/usr/bin/env python3
"""Budget-capped IntelX search that returns metadata only.

Reads INTELX_API_KEY and INTELX_API_URL from the environment or from a .env file in the
current directory. The key is never printed. It never opens a file's contents.

Uses curl rather than urllib, because macOS python.org builds often lack a CA bundle.

Usage:
  intelx_search.py TERM [TERM ...] [--max-searches 3] [--max-results 50] [--dry-run]

Result status, per IntelX's documentation (verify against your plan):
  0 results   1 no more results   2 search id not found   3 not ready yet   4 error
Status 2 with zero records is INCONCLUSIVE, not "nothing found".
"""
import argparse
import collections
import json
import os
import subprocess
import sys
import time

INCONCLUSIVE = "INCONCLUSIVE"


def load_env(path=".env"):
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, val = line.partition("=")
        os.environ.setdefault(k.strip(), val.strip().strip("\"'"))


def call(method, path, body=None):
    cmd = ["curl", "-s", "-m", "30", "-X", method, "-w", "\n%{http_code}",
           "-H", f"x-key: {os.environ['INTELX_API_KEY']}", "-H", "Content-Type: application/json",
           "-H", "User-Agent: what-leaked-about-you", os.environ["INTELX_API_URL"] + path]
    if body is not None:
        cmd += ["-d", json.dumps(body)]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    txt, _, code = out.rpartition("\n")
    try:
        return int(code), json.loads(txt or "{}")
    except (ValueError, json.JSONDecodeError):
        return int(code or 0), {}


def search(term, max_results):
    st, s = call("POST", "/intelligent/search", {
        "term": term, "buckets": [], "lookuplevel": 0, "maxresults": max_results,
        "timeout": 0, "datefrom": "", "dateto": "", "sort": 4, "media": 0, "terminate": []})
    info = {"term": term, "http": st, "soft_selector_warning": s.get("softselectorwarning"),
            "altterm": s.get("altterm") or ""}
    sid = s.get("id")
    if not sid:
        return {**info, "verdict": INCONCLUSIVE, "reason": "no search id returned"}, []
    r = {}
    for _ in range(5):
        time.sleep(4)
        _, r = call("GET", f"/intelligent/search/result?id={sid}&limit={max_results}&statistics=1&previewlines=0")
        if r.get("status") != 3:
            break
    call("GET", f"/intelligent/search/terminate?id={sid}")
    recs = r.get("records") or []
    info.update(status=r.get("status"), count=len(recs))
    if recs:
        info["verdict"] = "HITS"
    elif r.get("status") in (0, 1):
        info["verdict"] = "NONE"
    else:
        info["verdict"] = INCONCLUSIVE
    return info, recs


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("terms", nargs="+")
    p.add_argument("--max-searches", type=int, default=3, help="hard cap on credits spent in one run")
    p.add_argument("--max-results", type=int, default=50)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    load_env()
    if not args.dry_run and not (os.environ.get("INTELX_API_KEY") and os.environ.get("INTELX_API_URL")):
        sys.exit("INTELX_API_KEY / INTELX_API_URL not set")

    terms = args.terms[: args.max_searches]
    if len(args.terms) > len(terms):
        print(f"budget: only the first {len(terms)} of {len(args.terms)} terms will run "
              f"(raise --max-searches after asking the user)")
    if args.dry_run:
        print(f"dry run: would spend {len(terms)} search credit(s) on: {terms}")
        return

    for term in terms:
        info, recs = search(term, args.max_results)
        print("=" * 60)
        print(json.dumps(info, ensure_ascii=False))
        if info["altterm"]:
            print(f"warning: IntelX also matched on '{info['altterm']}', so hits may be domain-level noise")
        if info["verdict"] == INCONCLUSIVE:
            print("warning: inconclusive, do not report this as 'not found'")
        print("by bucket:", dict(collections.Counter(x.get("bucket") for x in recs)))
        for x in recs:
            if not str(x.get("bucket", "")).startswith("web.public"):
                print({k: x.get(k) for k in ("name", "date", "bucket", "mediah", "size")})


if __name__ == "__main__":
    main()
