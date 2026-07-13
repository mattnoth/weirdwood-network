---
session: 213
date: 2026-07-12
model: Fable 5 (orchestrator) + Sonnet 4.6 proposers/pressure-test + Haiku 4.5 verifiers
---

# Session 213 — Roles round 2, the citation overhaul, the Dance dip, and two gates opened

The largest single session to date: two graph mints (+122 edges), a 1,836-quote
citation upgrade, seven UI fixes, two SHARED_RULES revisions (both live-probe-verified),
the roles slice DECLARED DONE, the path tool wired into the chat, and the **theories
track gate opened** by Matt. Five production deploys (final: `6a5464f6`).

## 1. Opening — the vile-meal thread and "what is SHARED_RULES?"

Matt re-prioritized the S212 handoff: re-test the vile-meal question before the
routing fix. Re-test at the new 10-step bound: `end_turn` at exactly 10/10 calls —
the walk succeeded but with zero headroom and still never called `theme`. That proved
the routing gap was real (win by budget, not routing), so the superlative/comparative
routing row landed (test repin 13212→13747). Post-deploy third ask: first call
`theme("meals & feasts")`, 7/10 calls, grounding 67→84. The bound raise fixed the
symptom; the routing row fixed the disease.

## 2. Matt's phone screenshots — the citation bug class

Two screenshots showed quote attributions rendering raw MediaWiki anchors
(`wiki:Aegon_I_Targaryen.cite_ref-Rasos71.7B.7B…`). Root-cause chain: Pass 2 left
`(wiki:…cite_ref…)` tokens inline in node quote text → `parse_quotes` only extracts
attribution-line book cites, so the token rode the quote text → the model dutifully
copied it into the quote marker's source field → `prettyCite` passed non-chapter refs
through raw. Scale: 4,761 quote lines across 1,304 files (later count minus
`_conflicts`: 4,687/1,298).

Matt's instinct — "you can easily GREP for that line" — proved out completely:
all three screenshot quotes matched unique corpus lines. The fix became the
session's biggest data win (§5).

## 3. Roles slice round 2 → DECLARED DONE

The S212 machine reran on frozen ranks 51–100. Two honest narrowings: (1) caught that
still-zero-role events at frozen ranks ≤50 were round-1 events that adjudicated to
zero mintable roles — re-running them would re-propose settled outcomes, so round 2
starts strictly at rank 51; (2) the early-stop rule tripped (median fresh degree 3.0
< 4) — cut at the score-50 knee, 50→24 events, dropping quote-zero thin rows and
three junk nodes (`marriage` typed event.battle, `great-council`,
`tourney-at-ashford-meadow` — node-hygiene residue).

4 Sonnet proposers → 103 candidates; 4 Haiku verifiers → 94C/5A/4P; adjudication
kept 101 (2 dropped: Rodrik textually absent from the Hornwood fighting; Rickard
Karstark's bounty ≠ command and he's dead at event time; 2 reclassified: Cersei→
ATTENDS since Lady Alerie made the arrangements, Maegor→FIGHTS_IN). **The
deterministic byte-check overrode the Haiku verifier twice** — both "quote-not-found"
PROBLEMs were verifier false positives (fab OCR mixes straight and curly apostrophes
within single lines; the verifier assumed uniform encoding). Lesson recorded: the
deterministic line-check is the authoritative quote gate; verifier quote verdicts are
advisory, support/role verdicts are their real value.

Minted on Matt's go: +101 (26,618→26,719), all gates green. With rounds 1+2 = 337
role edges on the 74 highest-value zero-role events, the slice is DONE — the
remaining ~185-event tail is quote-zero wiki-stub territory, documented as not worth
agent passes.

## 4. "Burn usage — pick a higher-value target": the HotD audit and the Dance dip

Matt: do as many tasks as possible before the weekly reset; what would enrich
questions for House of the Dragon viewers? A deterministic coverage audit over ~80
HotD entities answered: every principal had ZERO causal edges, the
dance-of-the-dragons umbrella had 3 weak roles and no wiring, marquee characters had
no quotes. Best discovery: **Blood and Cheese existed all along** as
`murder-of-prince-jaehaerys`, fully wired — only the alias was missing. Second
discovery: the naive gap map undercounted — many "missing" links exist via
intermediate nodes (the chain-as-arc design working as intended); the W2 proposer
independently flagged the same and re-derived from edges.jsonl.

The Dance dip ran the full machine (4 Sonnet proposers on disjoint workstreams, 3
Haiku verify passes, a Sonnet pressure-tester with BLOCK authority per the autonomous
mint protocol — Matt's "do as many tasks as you can" treated as a session-scoped
grant): **+21 edges** (COMMANDS_IN per side on the umbrella matching the WO5K
pattern with blacks/greens qualifiers backfilled deterministically; roles on
aemonds-march + the four-faction Daughters' War; 6 causal gap-fills) and **57 curated
F&B quotes** onto 20 thin HotD nodes. Verdict: CLEAR TO MINT, two nits recorded
(archon-of-tyrosh is a title-node used as a role source — standing schema question;
qualifier backfill applied pre-mint). Aliases: "Blood and Cheese", "Battle of Rook's
Rest", "Frey pie" singular (+ the S212 alias-gap todo closed).

W3a's sharpest catch: `the-dragons-wroth` is Conquest-era (the 10–12 AC Dornish
war), not Dance — swept in by name-vibes; its quotes enrich the correct node anyway.

## 5. The quote-cite upgrade — 1,836 wiki quotes become navigable book cites

`scripts/upgrade-wiki-quote-cites.py`: for every wiki-cited node quote, a
normalized-containment search over the whole 410-file chapter corpus (one big
normalized blob per file + offset map → line); a UNIQUE hit rewrites the quote block
(wiki artifacts stripped, attribution line gains `BOOK (\`path:line\`)`). The norm()
family matches verify_node_quotes, so upgrades pass the verifier BY CONSTRUCTION —
and did: 3,038/3,038 (was 1,202). 15-file smoke first (caught `_conflicts/`
processing + a spacing nit), then full apply: **1,836 upgraded across 782 nodes**;
2,640 no-unique-match (mostly TWOIAF material not in the corpus) + 211 too-short left
untouched. Render half: `parse_quotes` now strips wiki tokens at the engine layer (no
consumer ever sees them) and `prettyCite` renders residuals as "AWOIAF <Page>".
Live spot-check: the exact Dany quote from Matt's screenshot now cites ASOS
Daenerys 6:309, zero raw tokens on the node.

## 6. UI: seven fixes, two phone passes

Batch 1 (e/h/i/j/k + finds): stream-follow scroll (upward wheel/touch disengages;
new question re-engages), Bloodraven persona PARKED (Matt: "loremaster is good" —
toggle hidden, code intact), localStorage thread persistence + New button (mobile
Safari tab-discard), receipts dup-passage dedupe (chips merge onto one passage),
dossier reorder v1 (description first), prettyCite fab `-pNN` multi-part chapter fix
(spotted live: raw `fab/fab-the-blacks…md:245` in the rail), `###` sub-headers as
labels. Batch 2 after Matt's second phone pass: **dossier v2 reverts v1's order** —
quotes FIRST under a small "Directly from the text" label, description under one
small "From the ASOIAF wiki" credit, arc last; plus the "F&B FAB …" double-label fix
in bookQuote. New records: (n) HTML remnants + bare short-form cite tokens in section
prose; (l)+(m) below.

## 7. Live probes drove two more SHARED_RULES fixes + the path tool

The "Why did the Dance happen?" probe produced a good answer with two flaws: the
model narrated "The causal chain panel is empty for this node… Let me pull the
relationships" INTO the prose (→ the no-process-narration rule), and the umbrella-war
empty-walk design tension (→ the why-did-a-WAR-happen routing row: walk the
constituent spark event, never remark on the empty chain). Matt chose the prompt-fix
option and asked for the path tool now — show airing, show-watcher questions
incoming. `path(a,b)` existed fully built in the TS lib (direct edges + ranked
shared-neighbor bridges) but was never registered as a chat tool. Wired: TOOL_DEFS +
dispatch (bridges capped at 10 on the wire) + **harvestResult** (critical: direct-edge
refs must enter the cite allowlist or quoted evidence would false-flag as unverified)
+ receipts "connection" card + routing row (the old row apologized for the missing
op). Repin 13747→15020. Live probes: WO5K-why walked Robert's death + Ned's
execution with zero narration leaks (grounding 92); Manderly↔Rat-Cook found the
Frey-pies bridge in one path() call ($0.06).

## 8. Theories gate OPENED

Matt: "Yes — theories," video-transcript-first, Alt Shift X. His other repo's
planned yt-dlp tooling wasn't built, but the `yt_dlp` module was installed — enough.
Pulled the full channel (183 videos), deterministic triage (72 theory candidates /
83 show recaps / 28 non-ASOIAF), curated a 15-video wave-1 starter set favoring
canonical named theories with existing dark-stub nodes, pulled all 15 transcripts
(~10–30KB VTT each). Pipeline + schema written to `working/theories/README.md`; core
principle: **ASX is the map, the books are the truth** — every evidence beat
re-grounds against our corpus to a verbatim chapter:line before any edge mints;
theories are Tier 3–5 always; the chat's no-theories guardrail is untouched.
Staging README superseded; memory updated. Discrepancy noted: the staging README's
claimed `eldritch-apocalypse` stub does not exist — fresh mint needed.

## 9. Numbers

- Edges: 26,618 → **26,740** (+101 roles r2, +21 Dance)
- Book-cited verified quotes: 1,202 → **3,095** (+1,836 upgrades, +57 Dance)
- Deploys: `6a540e73` (roles+routing) → `6a541571` (Dance+UI+aliases) →
  `6a541767` (quote upgrade) → `6a545dd8` (path+prompts+dossier v2) →
  **`6a5464f6` (final)**
- Suites at close: pytest 1342 green, deno 102 green, semantic gate PASS,
  verify_node_quotes 3,038/3,038 pre-Dance-quotes (3,095 at close)
- Harvest queue: 0 → 42 open rows merged at endsession → drain staged as a
  parallel-safe continue prompt (rule: never let it balloon silently)
