# Site coverage: what's checked, how, and why the list is short

`scripts/sites.json` only carries sites that were calibrated against a real,
public account and a fabricated one before being added — the same discipline
`what-leaked-about-you` applies to reading IntelX responses. A site is on the
list because its "exists" and "does not exist" signatures were observed to
actually differ. Do not add a site without doing the same calibration; a wrong
signature produces confident, wrong verdicts, which is worse than no coverage.

## Verified, in `sites.json`

| Site | Method | Exists signal | Missing signal |
|---|---|---|---|
| GitHub | REST API (`api.github.com/users/{handle}`) | HTTP 200 | HTTP 404 |
| GitLab | Profile page | HTTP 200 | HTTP 302 (redirected to sign-in) |
| Hacker News | Firebase REST endpoint | JSON object | literal `null` |
| Lichess | Public API | HTTP 200 | HTTP 404 |
| Dev.to | Public API | HTTP 200 | HTTP 404 |
| Keybase | Lookup API | `status.code == 0` | any other status code |
| Telegram | `t.me/{handle}` page | `tgme_page_title` marker present | marker absent |
| Steam (vanity URL) | `steamcommunity.com/id/{handle}` | error string absent | `"The specified profile could not be found"` present |
| Strava (vanity URL) | `strava.com/athletes/{handle}` | HTTP 200 | HTTP 404 |

Caveats worth carrying into a report:

- **Hacker News**'s check now requires HTTP 200 before trusting the null/object
  body — found empirically: feeding it a handle containing `@` (e.g. running an
  email through this script by mistake) hits Firebase's path parser, which
  returns HTTP 400 with `{"error":"Invalid path: Invalid token in path"}`. That
  body is non-null and non-empty, so before this fix it read as `EXISTS` — a
  false positive from a malformed request, not a real account. This script only
  checks usernames; an email will produce noise like this across several sites,
  not a meaningful result.
- **GitHub** unauthenticated requests are rate-limited (~60/hour per IP). Space
  out repeated runs; do not loop this script over a wordlist.
- **GitLab**'s 302 signature is inferred from one observation, not documented
  API behaviour — treat a 302 as a strong "not found" hint, not certainty.
- **Strava**'s status code is reliable — tested against a real vanity slug and
  four differently-shaped fabricated ones (alphabetic, short, hyphenated,
  digit-suffixed), all four gave 404 while the real one gave 200. But the
  page's own content is not useful for corroboration: Strava hides the
  athlete's real name behind a login wall for anonymous viewers, so the
  `og:title` reads as a generic "Sign up to see more" teaser regardless of
  whose profile it is. Use the hit for existence only; corroborate identity
  some other way.
- **Keybase**'s error path returns `INPUT_ERROR` for malformed handles
  (too long, invalid characters) as well as for genuinely unregistered ones.
  A verdict here that turns on handle *length* rather than registration is a
  false read — sanity-check unusual handles by hand.
- **Telegram** only confirms a public `t.me/<handle>` page exists (channel,
  bot, or a user who enabled a public username). A private account with no
  public username will read as `NOT_FOUND` even if the person uses Telegram.

## Known-unreliable via a plain HTTP request — deliberately excluded

- **Reddit**, **Chess.com** — both returned HTTP 403 on *every* request in
  testing, real handle and fabricated handle alike. Cloudflare/bot-protection
  blocks the check before it can discriminate anything. Do not add either
  without a different access path (their own OAuth-backed API, in Reddit's
  case) — a same-response-for-both signature is worse than no data, because it
  looks like a working check.
- **Instagram, TikTok, X/Twitter, LinkedIn, Facebook, YouTube** — client-side
  rendered. The server returns effectively the same shell HTML whether the
  handle exists or not; the real content loads via JavaScript after the page
  arrives. A `curl`-based check cannot see it. Checking these requires a
  headless browser hitting the live site, which is a heavier, ToS-sensitive
  operation this skill does not perform — verify these manually.

## Email-keyed liveness: Epieos

Epieos (epieos.com) answers a different question than this script: given an
**email address**, is it tied to a live Google account, and — through that —
what else does Google expose (a Gaia ID, a Google Maps reviewer profile, an
associated name or avatar, a YouTube channel where public)? It also checks a
handful of other services by email. This is the email-selector equivalent of
what this script does for a username, and it is a natural companion pivot when
`what-leaked-about-you` hands you an email with no further leads.

There is no API key configured in this environment, and none is assumed:

- The free web tool at epieos.com covers a single email at a time and is
  meant for manual, human use — run it yourself in a browser, the same way
  this project already treats the HIBP web lookup.
- Epieos also sells a keyed API for programmatic/bulk use. If you get a key,
  treat query volume and retention the same way `what-leaked-about-you`
  treats any keyed commercial source: budget-conscious, logged by the vendor,
  and not something to loop over a wordlist without thinking about it.
- Do not attempt to script around the web tool's own anti-automation
  measures (captcha, rate limiting) — that is exactly the kind of ToS
  workaround `ETHICS.md` rule 6 rules out.

## Extending this list

Adding a site means: pick one real, public account and one fabricated handle,
run the request by hand, and record the actual status code or body signature
— not the documented API behaviour, the observed one. Put both in the pull
request or commit message so the next person can re-verify instead of trusting
a claim.
