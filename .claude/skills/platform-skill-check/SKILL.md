---
name: platform-skill-check
description: >-
  Check whether a username/handle is registered on other platforms, using a small,
  individually-calibrated set of server-verifiable sites (GitHub, GitLab, Hacker News,
  Lichess, Dev.to, Keybase, Telegram, Steam, Strava) plus a documented email-keyed companion
  (Epieos) for Google-account liveness. Use when a username recovered from a breach
  record, or a handle already in hand, needs mapping to live accounts elsewhere — the
  standard pivot from `what-leaked-about-you`. Distinguishes EXISTS / NOT_FOUND /
  INCONCLUSIVE per site and documents which popular platforms are deliberately excluded
  because a plain HTTP request cannot read them reliably. Passive, read-only checks
  only; a hit is membership evidence, never identity proof, and must be corroborated
  before it is attributed to a person.
---

# Hunt a handle

A username found in a breach record, or handed to you directly, is only useful once you
know where else it's live. This skill answers "does an account with this exact handle
exist here" across a small set of platforms — cheaply, without a key, and without
guessing at derived spellings you haven't been given.

## Scope gate

Same rule as `what-leaked-about-you`, and it matters more here, not less: this skill
makes live requests to third-party services, not a lookup against a historical dump.
Before checking any handle, establish that it is the user's own, or that its owner has
authorized the work. If neither is clear, ask once and stop until it is. A mock or
invented handle needs no gate, but say plainly that nothing was queried.

Scope applies to every variant you check, not just the handle as given. If
`what-leaked-about-you`'s `scripts/variants.py` produced `derived` variants (a
different separator, a trimmed suffix, the local part of an email as a
username), those still need the user's confirmation before you spend a request on
them — they may belong to someone else entirely.

## What a hit means, and what it doesn't

`EXISTS` means: an account with this exact string exists on that platform, right now.
It does **not** mean it's the same person you're auditing. Handle squatting, coincidental
reuse of a common word, and unrelated people picking the same short handle are all
common — more common the shorter and more generic the handle is. A hit is a lead, not a
conclusion.

Corroborate before attributing a hit to a specific person:

- **Bio, display name, avatar** that match something else you already know about the
  subject (not just the handle matching itself — that's circular).
- **Cross-platform consistency** — the same distinctive bio text, the same avatar image,
  or a link between the accounts (one profile linking to another) is real evidence.
  Several platforms returning `EXISTS` for a generic handle on their own is not.
- **Timing** — an account created around the same time as a breach record with the same
  handle is more likely the same registration event than one created years apart.

Never use a hit to log in, message, follow, or otherwise interact with the account. That
crosses from passive observation into contact, which needs its own authorization and is
out of scope here regardless of what you find.

## Running it

```
python3 scripts/username_check.py <handle> [--delay 0.5] [--json]
```

Reads `scripts/sites.json` — nine sites, each calibrated against a real account and a
fabricated one before being added. Full method-by-site table, caveats, and the reasoning
for what's deliberately left out (Reddit, Chess.com — blocked identically for real and
fake handles; Instagram, TikTok, X, LinkedIn, Facebook, YouTube — JS-rendered, invisible
to a plain request): [reference/site-coverage.md](reference/site-coverage.md).

Verdicts:

- `EXISTS` — the site's calibrated "account is real" signature matched.
- `NOT_FOUND` — the site's calibrated "no such account" signature matched.
- `INCONCLUSIVE` — network error, unexpected response, or the request otherwise didn't
  land cleanly. Report it as such, not as a negative — same discipline
  `what-leaked-about-you` applies to IntelX's `status: 2`.

**Be polite.** The default delay between requests exists so this doesn't read as
scraping to any of the nine sites. Don't loop this over a wordlist of guessed handles —
that turns a targeted check into enumeration against a third party, which is exactly what
the scope gate exists to prevent.

## Worked example

Checking the handle `torvalds` (a real, public account used here only to calibrate the
tool) returns: `EXISTS` on GitHub, GitLab, Lichess, Keybase, Telegram, and Steam;
`NOT_FOUND` on Hacker News and Dev.to.

Read naively, that's six platforms for one identity. Read correctly: GitHub and GitLab
are attributable with high confidence — the bio, activity, and public reputation attached
to that specific account are consistent with the well-known person. The Steam and
Telegram hits for the same three-syllable, real-world surname are exactly the kind of
coincidence this section warns about — nothing in either profile was checked for
corroborating content, so neither is reported as the same person's account. This is the
whole point of the distinction: the script tells you where the handle exists, not who's
behind it.

## Pivots

| Lead | Where it goes |
|---|---|
| Handle confirmed live on a platform, need identity attributes from that profile | `find-anyone` |
| Handle came from a breach record, want the service list that produced it | `what-leaked-about-you` |
| Email selector, no more username leads — check Google-account liveness | Epieos, manual (see reference doc) — no API key configured here |
| Several confirmed accounts for one person | `graph-the-network` |
| A platform outside the nine covered here | verify manually; do not script around anti-bot protection |

## Legal and handling notes

Same posture as `what-leaked-about-you` — see [../../../ETHICS.md](../../../ETHICS.md).
Specific to this skill:

- Every request here goes to a real, live third-party service, not a static dataset.
  Rate limits and terms of service apply directly, in real time, not as an abstraction.
  Respect them; do not add sites whose only working access path is scraping around a
  captcha or a login wall.
- Record only what the objective needs: the verdict and, where you corroborated it, the
  specific matching detail. Do not archive full profile pages or avatars beyond what's
  needed to support the finding.
- A confirmed live account is current, in-use identity — more sensitive than a breach
  record from years ago. Handle findings with that in mind before they go in a report.
