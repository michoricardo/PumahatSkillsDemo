#!/usr/bin/env python3
"""Generate search variants for a selector the user owns. No network access.

Every variant is tagged:
  equivalent - provably the same mailbox / number, safe to search once ownership is confirmed
  derived    - plausible relative (other domain, other handle). Same person only by
               inference, so it needs the user's explicit confirmation before it is searched

Usage:
  variants.py email    micho_gr94@hotmail.com
  variants.py phone    8441206120 [--country MX|US]
  variants.py username micho_gr94
  add --json for machine-readable output
"""
import argparse
import json
import re
import sys

MS_DOMAINS = ["hotmail.com", "outlook.com", "live.com", "msn.com"]
MS_REGIONAL = ["hotmail.es", "hotmail.com.mx", "outlook.es", "live.com.mx"]


def v(value, kind, priority, why, next_step):
    return {"variant": value, "kind": kind, "priority": priority, "why": why, "next": next_step}


def email_variants(addr):
    addr = addr.strip()
    local, _, domain = addr.rpartition("@")
    if not local or not domain:
        sys.exit("not an email address")
    low_local, low_domain = local.lower(), domain.lower()
    out = [v(addr, "equivalent", 1, "as given", "breach lookup")]

    base = low_local.split("+", 1)[0]
    if base != low_local:
        out.append(v(f"{base}@{low_domain}", "equivalent", 1, "plus-tag stripped: same mailbox", "breach lookup"))

    if low_domain in ("gmail.com", "googlemail.com"):
        nodots = base.replace(".", "")
        for d in ("gmail.com", "googlemail.com"):
            out.append(v(f"{nodots}@{d}", "equivalent", 1, "Gmail ignores dots and treats googlemail.com as an alias", "breach lookup"))
    if low_local != local or low_domain != domain:
        out.append(v(f"{low_local}@{low_domain}", "equivalent", 1, "lowercased", "breach lookup"))

    if low_domain in MS_DOMAINS + MS_REGIONAL:
        for d in MS_DOMAINS:
            if d != low_domain:
                out.append(v(f"{base}@{d}", "derived", 2, "same handle on another Microsoft domain: a different mailbox, often owned by the same person", "breach lookup"))
        out.append(v(f"{base}@" + "hotmail.es", "derived", 3, "regional Microsoft domain", "breach lookup"))

    out.append(v(base, "derived", 2, "local part as a username selector", "platform-skill-check"))
    out.extend(username_variants(base, include_origin=False))
    return out


def username_variants(name, include_origin=True):
    name = name.strip()
    out = [v(name, "equivalent", 1, "as given", "platform-skill-check")] if include_origin else []
    lowered = name.lower()
    if lowered != name:
        out.append(v(lowered, "equivalent", 2, "lowercased", "platform-skill-check"))
    for a, b in (("_", "."), ("_", "-"), ("_", ""), (".", "_"), ("-", "_"), (".", ""), ("-", "")):
        if a in lowered:
            out.append(v(lowered.replace(a, b), "derived", 3, f"separator '{a}' -> '{b or 'none'}'", "platform-skill-check"))
    stem = re.sub(r"[\d_.\-]+$", "", lowered)
    if stem and stem != lowered:
        out.append(v(stem, "derived", 3, "trailing digits and separators removed. Very common handles link nothing", "platform-skill-check"))
    seen, uniq = set(), []
    for item in out:
        if item["variant"] not in seen:
            seen.add(item["variant"])
            uniq.append(item)
    return uniq


def phone_variants(raw, country):
    digits = re.sub(r"\D", "", raw)
    notes = []
    if len(digits) == 10:
        national = digits
    elif len(digits) == 12 and digits.startswith("52"):
        national, country = digits[2:], "MX"
    elif len(digits) == 11 and digits.startswith("1"):
        national, country = digits[1:], "US"
    else:
        sys.exit("expected a 10-digit national number or one with a +52 / +1 prefix")
    a, b, c = national[:3], national[3:6], national[6:]

    if a in ("800", "833", "844", "855", "866", "877", "888"):
        notes.append(f"{a} is a North American toll-free prefix, usually a business line. If the number is personal, MX (lada {a}) is the likelier reading")

    out = [v(national, "equivalent", 1, "national digits", "breach lookup"),
           v(f"{a} {b} {c}", "equivalent", 2, "spaced", "breach lookup"),
           v(f"{a}-{b}-{c}", "equivalent", 2, "dashed", "breach lookup"),
           v(f"({a}) {b}-{c}", "equivalent", 3, "US style", "breach lookup")]
    if country in ("MX", "AUTO"):
        out += [v(f"+52{national}", "equivalent", 1, "E.164 Mexico", "breach lookup"),
                v(f"52{national}", "equivalent", 1, "country code without plus", "breach lookup"),
                v(f"+52 {a} {b} {c}", "equivalent", 2, "spaced E.164", "breach lookup"),
                v(f"+521{national}", "equivalent", 3, "legacy Mexican mobile format (dropped in 2019), still present in old dumps", "breach lookup"),
                v(f"521{national}", "equivalent", 3, "legacy mobile without plus", "breach lookup"),
                v(f"044{national}", "equivalent", 3, "legacy mobile dial prefix", "breach lookup"),
                v(f"01{national}", "equivalent", 3, "legacy long-distance dial prefix", "breach lookup")]
    if country in ("US", "AUTO"):
        out += [v(f"+1{national}", "equivalent", 1, "E.164 NANP", "breach lookup"),
                v(f"1{national}", "equivalent", 2, "country code without plus", "breach lookup")]
    for item in out:
        item["next"] = "whose-number-is-this" if item["priority"] == 1 else item["next"]
    return out, notes


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("kind", choices=["email", "phone", "username"])
    p.add_argument("value")
    p.add_argument("--country", choices=["MX", "US", "AUTO"], default="AUTO")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    notes = []
    if args.kind == "email":
        items = email_variants(args.value)
    elif args.kind == "username":
        items = username_variants(args.value)
    else:
        items, notes = phone_variants(args.value, args.country)

    seen, uniq = set(), []
    for it in items:
        if it["variant"] not in seen:
            seen.add(it["variant"])
            uniq.append(it)
    uniq.sort(key=lambda x: (x["priority"], x["kind"] != "equivalent"))

    if args.json:
        print(json.dumps({"notes": notes, "variants": uniq}, ensure_ascii=False, indent=2))
        return
    for n in notes:
        print("NOTE:", n)
    print(f"{'P':<2} {'KIND':<11} {'VARIANT':<34} WHY")
    for it in uniq:
        print(f"{it['priority']:<2} {it['kind']:<11} {it['variant']:<34} {it['why']}")


if __name__ == "__main__":
    main()
