---
session: 187
title: Chat-UI cite-verification false-positive — root-caused to build parser, fixed + deployed
date: 2026-07-03
track: meta
model: Opus 4.8
api_cost: ~$0.03 (3 fan-out subagents ≈ 200k subagent tokens; no live chat turns)
harvest_queue: 0
---

# Session 187 — The "citation could not be verified" banner

## The report
Matt: the amber "A citation could not be verified" banner pops on pretty much every chat.
Screenshot was a Lady Stoneheart / Lem-and-Merrett answer (ASOS Catelyn 7). The visible
quote rendered perfectly, yet the banner fired.

## The gate (how it works)
`web/netlify/edge-functions/lib/agent.ts`:
- `harvestResult()` builds a per-turn `validCites` allowlist from tool returns — but only
  from the STRUCTURED `cite`/`ref` fields.
- After the answer, `verifyCites(prose, validCites)` scans prose with `CITE_RE` for any
  `chapter.md:line` token not in the allowlist and flags it → `status: unverified-cites`
  → the banner (`app.js` STATUS map).

## First hypothesis (WRONG — and the logs killed it)
I guessed path-normalization: the model drops the `sources/chapters/` prefix or mangles the
token, so a byte-exact `validCites.has()` fails. Reproduced that the regex matches loose
shapes while the allowlist stores full paths — plausible, but a hypothesis, not evidence.

Pulled the real production logs to check (needed Netlify Blobs creds — see below). Of 12
logged turns, only 3 flagged, and every flagged token was a FULL, correct path that EXISTS
in the graph and points to the right line (`affc-brienne-08.md:307` = Stoneheart's hood
reveal; `asos-arya-11.md:51` = the Hound). Not mangled, not fabricated. My normalization
theory was wrong.

## Real root cause
The flagged tokens sit on their nodes as quotes whose structured `cite` field is `null`,
with the real `chapter:line` BURIED INSIDE the quote's `.text` (a book-cite-overlay
byproduct). `harvestResult` only reads the structured field → the buried token never enters
`validCites` → the model correctly lifts it from the text and gets false-flagged. 158 such
quotes graph-wide. Clusters on Red Wedding / Catelyn / Stoneheart — exactly Matt's test
topics — so it felt universal though it was 25% of turns.

Traced to the SOURCE: `web/data/nodes.json` is derived; the bug is in `parse_quotes()` in
`scripts/build-chat-export.py`, two defects:
1. When the attribution line sits inside the `>` block (`> — sources/…`, the common overlay
   shape), the block loop swallowed it into `.text`; the following-line attribution branch
   never fired.
2. `CITE_RE` required backticks, so bare cites (`— sources/…:25 · gloss`) wouldn't match
   even if the attribution were detected.
The node `.md` source data is correct — only the parser dropped the cite.

## Fan-out + synthesis (Matt asked for it)
3 parallel general-purpose subagents, different lenses:
- **Gate-logic**: confirmed the whole-payload `JSON.stringify(out)` harvest works, minimal,
  no regex/dedupe hazard; gave a regression test. (This was the fallback, not the primary.)
- **Data-hygiene**: found the true root cause in `parse_quotes`; recommended fixing the
  build parser (~15 lines) — then the structured field is correct and no gate change needed.
- **Adversarial**: independently reached the same "upstream is safest" conclusion; flagged
  that the whole-payload sweep loosens the anti-fabrication gate (pulls in 579 unrelated
  attribution tokens + a cross-quote-swap false-negative surface); preferred a narrow
  `.text`-scoped harvest if any gate change is made.

Convergent verdict: fix the parser (root cause), add a NARROW gate backstop only for
residue. Implemented both.

## What shipped
- `parse_quotes` rewritten: detect the `—` attribution line whether inside or after the
  `>` block; backtick-optional `CITE_RE`. Rebuilt bundle → structured cites 572→731; buried
  count 158→4.
- The 4 residuals are genuinely malformed source (cite embedded mid-quote-body, not a clean
  attribution line). Rather than hand-edit source, added the adversarial-blessed narrow
  backstop in `harvestResult`: also scan a quote's `.text` for `CITE_RE` and admit matches.
  Covers the 4 + any future overlay additions before a rebuild; scoped to quote text only,
  so it does not widen the gate to attributions/cross-node prose.
- Regression test added (`agent_test.ts`); full suite 41 passed / 0 failed; typecheck clean.
- Deployed to prod (`npx netlify deploy --prod --build`); live.

## Side note — Netlify Blobs creds
read-logs.ts needs `NETLIFY_SITE_ID` + `NETLIFY_AUTH_TOKEN`. Neither was in env/.env. Found
Site ID in `.netlify/state.json`; a usable PAT in the Netlify CLI login
(`~/Library/Preferences/netlify/config.json`). Appended both to `web/.env` (gitignored,
confirmed). NOTE: the first append jammed `NETLIFY_SITE_ID=` onto the un-newlined
`ANTHROPIC_API_KEY` line; fixed the split. `.env` is not committed.

## Follow-ups (backlog, not mid-flight)
- Optional: hand-fix the 4 malformed-source quotes (mance-rayder, nymeria-direwolf,
  victarion-admits-euron-s-role-in-his-wife-s-death ×2) so their cite is a clean attribution
  line — then the gate backstop becomes belt-and-suspenders.
- Optional: simplify `app.js` `cleanQuote()` now that most cites are structured (leave as a
  display safety net for now).
