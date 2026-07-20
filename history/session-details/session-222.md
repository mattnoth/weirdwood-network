---
session: 222
date: 2026-07-19
model: "Fable 5 (orchestrator); Sonnet subagents (script-builder ×3 iterations, curated-map builder, pressure-test, exhaustive re-pass, 3 harvest attachers); Haiku (entity-fit fresh-verify)"
type: EXECUTION (Matt-directed orchestration) + one adjudication
track: graph (absorbs the D&E close-out; occupies the DE-4 slot too)
---

# Session 222 — Dunk & Egg: close-out → graph integration → harvest drain → deployed

Matt's directive: *"orchestrate not just the wrap up, but harvest, and anything else to get dunk n egg
deployed. if not in one session, in consecutive. no parallel, it gets too confusing."* The whole arc fit
in one session: four commits + one prod deploy, every subagent sequential.

## 1. DE-4 close-out (`c7d00e7296`)

The 4 TMK epithet-SAME_AS rows (`tmk-dunk-01-p05:287/290`, `p06:269/271` — Dunk↔the Gallows Knight,
Glendon Ball↔the Knight of the Pussywillows) were the last open D&E Pass-1 item. Adjudicated **(a) KEEP
as alias capture**: the ingest rule maps any SAME_AS row whose target is an epithet phrase to an **alias
on the bearer's node, never a cross-identity edge** — which is both what the resolver needs ("who was
the Gallows Knight?" is a real chat query, proven at deploy verification) and a complete answer to the
auditor's epithet≠identity objection. Lossless and reversible; rows stay in the extraction files; Matt
can veto at review. `worklog-dunk-egg.md` frozen to `history/`; CLAUDE.md's track-aware branches
rewritten to point at the frozen file.

## 2. Graph integration (`233a8ea058`) — the interesting part

**Design call:** the extractions' Relationships tables are already locked-vocab typed (v4's lockdown),
so unlike the five-book Stage 4 run there is NO classifier step — the whole ingest is deterministic
Python (`scripts/dunk-egg-graph-ingest.py`), reusing `stage4_name_resolver.py` and the evidence-locator
patterns, emitting rows in the existing `pass1_relationship`/`book-pass1` edges.jsonl schema
(run_id `dunk-egg-pass1-derived-s222`). Vocab census up front: **all 61 D&E relationship types already
existed in the live vocabulary — zero drift.**

**The gate chain earned its keep.** Sequence: dry run (666 rows parsed → 226 emitted) → Sonnet
curated-map builder (132 name→slug rows; caught 13 namesake mis-hits incl. Quentyn Blackwood→
`quentyn-martell`) → fresh pressure-test with BLOCK authority → **PASS-WITH-EDITS**: cite integrity
was 60/60 clean, but the weak resolver rungs (`resolved-context-present`/`-prior`/`-firstname-unique`)
showed a systematic ~20–30% wrong-node rate across four distinct failure modes:

1. **Targaryen generational collisions** — bare Aegon/Aemon/Aerys resolving three generations off
   (Aegon IV's bastards attributed to Aegon V; Aemon Blackfyre → Maester Aemon; Aerys I → the Mad King).
2. **Cross-house first-name collisions** — Alyn Cockshaw (the TMK antagonist) → `alyn-velaryon`
   (a Dance-era admiral) in 6 of 7 rows: an entire subplot on the wrong person.
3. **A bad curated-map anchor** — "the Grey Lion"/Damon Lannister hand-mapped to a disambiguation-hub
   stub whose one member is born 244 AC. Even the "safe" bucket needed spot-checks.
4. **Wrong-TYPE fuzzy matches** — person names resolving to song/event/faction nodes
   ("Wild Wyl Waynwood" → the `wild-hares` faction).

The reviewer explicitly refused to clear the ~61 unchecked risky rows, so a second fresh agent ran an
**exhaustive 101-row re-pass**: 76 CONFIRM / **21 FIX** (right node existed — slugs swapped, better than
dropping) / 4 REJECT, and found one NEW failure mode (disambiguation-hub/generic stubs outranking
correctly-surnamed specific nodes — filed as a resolver-priority fix candidate in todos). Assemble step
applied verdicts by triple-match (101/101 matched), re-deduped post-fix (2 merges, 6 moved to overlay),
and ran a graph-wide alias collision guard (caught `uthor-underleaf|"Snail"` colliding with an existing
node; I additionally dropped bare "the Pretender"/"Pretender" — ambiguous between Daemon I and II).

**Landed:** +241 edges (edges.jsonl 26,860 → 27,101), +56 aliases on 23 nodes, backup at
`graph/edges/edges.jsonl.bak-s222-dunk-egg`, re-run sentinel on the run_id. refresh 5/5 · pytest 1452 ·
deno 115. Timestamp-only `graph/index/` churn (8,639 files, `generated_at` only) reverted per the S205
precedent — verified with `git diff -I'generated_at'`, which left exactly 2 files with real changes
(the two alias lookups).

**Parked residue** (all in `working/dunk-egg-graph-ingest/`): 35 overlay candidates (triples already
live from the wiki layer — book-evidence overlay opportunities), 46-row quarantine (deliberate SKIPs +
ungroundable paraphrase), Treb/Will node-level SAME_AS (both nodes exist; cross-identity-detector
worklist), the Brown Dragon ALIAS_OF row dropped as a Pass-1 labeling slip.

## 3. Harvest sidecar drain (`b8cc918cab`)

372 slash-delimited rows (the misnamed `.jsonl`). Deterministic locator first
(`scripts/dunk-egg-harvest-locate.py`): 75 **causal-spine rows routed to a staged seeds file**
(`harvest/causal-spine-seeds.jsonl` — the future event-wiring slice, deliberately NOT drained), 297
drainable. First locator pass grounded only 63% — the misses were dominated by **ellipsis-spliced
quotes** (harvest rows splice non-adjacent text with "…"). One iteration added ellipsis-segmentation
(each sub-part must hit within a 6-line span) + dialogue-tag-strip: 109 → 46 not-located (the rest
genuine paraphrase). Three sequential Sonnet attachers (THK 75 / TSS 82 / TMK 104 candidates) re-read
the SOURCE line for every row — attachers emit the real sentence, never the harvest paraphrase — and
self-verified verbatim before handoff. `apply-node-quotes.py --apply` landed **259 quotes on 80 nodes**
(2 smoke-era dups auto-skipped by its substring idempotence — the feared 55-row overlap was a non-issue).
`verify_node_quotes.py` 339/339 on touched slugs; Haiku entity-fit fresh-verify 18/18 (0 misfits).
Parked: 3 food-mint candidates (blackberries-in-cream, carrot/onion/barley stew, boiled eggs), 2
no-node, the rest duplicates/paraphrase — all in `harvest/*-parked.jsonl`.

## 4. Deploy + live verification (`6a5d4ba1`)

`npx netlify deploy --prod --build` per DEPLOY.md. Live-verify turn on prod:
*"Who was the Gallows Knight at the Whitewalls tourney, and what happened to him there?"* →
`resolve("Gallows Knight")` **matchType exact → duncan-the-tall** (this session's alias working live);
the answer streamed three of this session's TMK quote attaches with verified cites and the full
Blackfyre-conspiracy frame. $0.17, grounding 67, 0 unverified cites, stopState end_turn. The one
visible gap is the known deferred slice: `neighbors(wedding-tourney-at-whitewalls)` → 0 roles (event
reification not in this slice; substrate staged). Log-blob retrieval note: keys are `log/DATE/<uuid>`
— uuid sort is NOT chronological; find turns by question text.

## Decisions of record

- **Epithet-SAME_AS → alias, never cross-identity edge** (DE-4 adjudication, veto-able).
- **Fix-don't-drop** at re-pass: wrong-slug rows with good quotes get slug swaps (21 rescued).
- **Event wiring is its own next slice** — 75 staged causal-spine seeds + the extractions' Events
  reification tables; nothing event-shaped minted this session.
- Session numbering: this session takes **S222**; the theories wave-2 mint-gate prompt (pre-stamped
  "fires as S222") was corrected at endsession to fire as the next free S-number.
