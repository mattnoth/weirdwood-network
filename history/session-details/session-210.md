# Session 210 — Prod deploy → strip wiki boilerplate → redeploy

**Date:** 2026-07-11 · **Model:** Opus 4.8 · **Track:** graph (chat-UI data hygiene + deploy)
**Scope:** Matt's ask — deploy the S205–S209 backlog, strip the "from the AWOIAF wiki"
boilerplate everywhere, redeploy. Graph mutation: YES. Two prod deploys.

## Deploy #1 — ship the backlog

Nothing had been live since the S204 deploy. `netlify deploy --prod --build` (deploy
`6a51e7cd`) regenerated the five `web/data/` bundle files from the current graph, shipping
S205 (harvest quotes), S206 (cross-era seams), S207 (schema hygiene), S208 (review-bucket
recovery, +995 edges/+201 nodes), S209 (dispute-drain, +44 edges/+24 bullets). Verified the
S209 dispute bullets on the deployed `corlys-velaryon` node; chat pipeline healthy.

## The strip — a design pivot on the front-end finding

The built script (`strip-wiki-boilerplate.py`, board design 2026-07-06) split nodes rich vs
thin: rich → keep a stripped stub `"X is a <type>."`, thin → drop the line. Before applying I
found the decisive fact: **`web/public/app.js` `isWikiBoilerplate` already blanks any identity
ending in "from the AWOIAF wiki" — it's never shown.** So the boilerplate lives in the *data*
but is invisible in the UI today. That inverts the board's logic: keeping a stripped
`"X is a artifact."` stub would make `isWikiBoilerplate` return false and **newly surface**
~5,300 contentless stubs (some with raw types like `organization.house`) into dossiers — a
regression. Matt picked **drop-everywhere**: remove the boilerplate Identity line from all
6,481 nodes → `identity` becomes empty → UI shows nothing (the type is already in the card
subtitle) → clean data, zero UI change.

Also fixed the classifier while there: the old `RICH_SECTIONS_RE` allowlist was incomplete
(missed Culture/Aftermath/Heraldry & Sigil/Fire & Blood/…); inverted it to the docstring's real
intent — rich = any `## ` section beyond Identity/Edges. Result: 5,312 rich + 1,169 thin, all
dropped, 0 phrase remaining. `## Identity` sections left cleanly empty (`## Identity\n\n## …`).

## The family-golden scare — traced, not the strip

Post-strip, `family.json:family-aegon-i-targaryen-default-window` failed on `generationCounts`.
The strip only touches Identity text, not edges — so this shouldn't move. Ruled out
non-determinism (stable 3×), confirmed edges.jsonl unchanged, then **stashed the strip and the
test still failed** — proving the strip was innocent. Root cause: the golden reads the *built
bundle* (`web/data/{nodes,edges}.json`, gitignored), which was stale since the S204 deploy;
deploy #1's `--build` rebuilt it with the S205–S209 F&B genealogy edges (recovery +995,
dispute-drain +44), which legitimately reshuffled Aegon-I's 96-member cap. `mustInclude` and
memberCount=96 both held — exactly the "repin the counts" case the golden's own note describes.
Repinned (gen 5: 8→11, 7: 5→4, 12: 11→10, 13: 4→3) with the reason logged in the note.

## Emitters — guard, not patch

The "patch the generators so it can't come back" half turned out to be **20 files / 33 emitter
lines**, not the ~8 estimated — all retired Pass-2 ingestion scripts (new nodes come from
enrichment/F&B, which never emit the phrase). Rather than churn 20 untested generators, added a
**data-layer regression guard** (`tests/test_no_wiki_boilerplate.py`): asserts 0 node files
carry the phrase, failing loudly if anything ever reintroduces it — catches the whole class
regardless of source. Matt agreed (guard-test-not-patch). The 20-file list is logged in todos.

## The "more detailed" wiki references

Matt recalled seeing wiki references beyond the flat boilerplate. Scanned all non-empty Identity
lines: 7 mentioned "wiki"/"AWOIAF" outside functional `(wiki:Link)`/`cite_ref` markers. **5 were
user-facing meta-attributions** in composed prose (`hound-helm` "the wiki notes,"; `house-sweet`
"the wiki lists both regions"; `lothar` "see the wiki disambiguation page"; `gender-and-sexuality`
"a wiki meta-topic"; `porridge-gaoler` "the wiki page is Porridge") — stripped surgically, every
fact kept. **2 are provenance/build notes** (`red-wedding-conspiracy` "evidence_kind wiki /
book-pass1"; `mutiny-at-castle-black` "tier-1 wiki Origins prose ported") where "wiki" means
source-*tier* — the same provenance class as the `wiki_source` field Matt is keeping — left intact
and flagged.

## Deploy #2 + verify

`netlify deploy --prod --build` (deploy `6a51ee9b`) shipped the stripped bundle. Verified
`arakh` now ships `identity: ""`, "from the AWOIAF wiki" absent from the deployed data, chat
pipeline healthy (`end_turn`, 2 tools, 15 grounding, 0 unverified cites, ~$0.024/turn). A final
redeploy carried the 5 prose cleanups live.

## Commits

- `36387b3286` — the 6,481-node strip + classifier fix + family-golden repin.
- (endsession) — 5 wiki-attribution prose cleanups + the guard test + worklog/todos/archive.

## Gates

pytest 1458 (incl. the new guard) / deno 100 green throughout. No `weirwood refresh` — body-prose
edits only, no slug/alias changes; the deploy's `--build` rebuilds the shipped search index.
