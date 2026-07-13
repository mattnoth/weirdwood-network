# Azor Ahai / Prince That Was Promised cluster — build proposal (S216)

**STAGING ONLY. No graph mutation.** All files under `working/theories/azor-cluster/`.
Mint gate unchanged from S214 standing (Matt's explicit go required; validation review
before any mint).

## What was built

One enrich: `graph/nodes/theories/azor-ahai-theories.node.md` (existing tier-2 wiki
stub, `## Identity` / `## Edges` empty) becomes the canonical `concept.theory` node
for the Azor Ahai reborn / "the prince that was promised" identity theory. Display
name set claim-style: **"Daenerys and Jon Snow are Azor Ahai reborn"** (the video's
own converging verdict). `node_version` bumped 1 → 2; `wiki_source`, `bucket_id`,
`prompt_version` preserved from the stub.

**Structural decision (as instructed, not deviated from):** ONE enrich only.
`the-prince-that-was-promised-theories` and `lightbringer-theories` stay dark — their
material folds into `azor-ahai-theories` via aliases ("the prince that was promised",
"TPTWP", "PTWP") rather than separate nodes, matching the source video's own framing
that the two prophecy-names describe one figure (explicit sub-claim 0, grounded at
`azor-B10`/`sub_claim: 0`). This mirrors the KotLT precedent of enriching a stub in
place rather than minting a sibling node.

Per-candidate subsections used inside `## Evidence For` / `## Evidence Against`
(Stannis Baratheon / Daenerys Targaryen / Jon Snow / Rhaegar Targaryen), plus a
candidate-neutral "the prophecy's own mechanism" subsection — following the KotLT
enrich's structural pattern rather than R+L=J's flatter shape, since this theory
(unlike R+L=J) is explicitly multi-candidate.

## Sources

- `working/theories/extractions/O3o2LqFZcGU.jsonl` (85 beats, ASX "Who is Azor
  Ahai?") — the main candidate-testing video: seven prophetic signs tested against
  Stannis, Daenerys, Jon, and briefly a third-candidate/no-one reading.
- `working/theories/regrounding/O3o2LqFZcGU.jsonl` +
  `working/theories/regrounding-agent/O3o2LqFZcGU-p1.jsonl` + `-p2.jsonl` — grounded
  rows only used as leads; every quote actually placed in the staged files was
  independently re-verified against `sources/chapters/*.md` in this session (several
  regrounding-agent "grounded" rows were rejected as too loosely matched — see Notes
  below).
- `working/theories/extractions/UrhqmMRv1gQ.jsonl`, filtered to
  `theory: "Rhaegar is Azor Ahai (Lightbringer three-swords theory)"` beats only
  (rhaegar-B11 through rhaegar-B51). The R+L=J-header beats from this same video
  (rhaegar-B01–B10, B20-ish parentage material) were **not** touched — S214 already
  built those into `r-plus-l-equals-j`.
- `working/theories/regrounding/UrhqmMRv1gQ.jsonl` +
  `working/theories/regrounding-agent/UrhqmMRv1gQ.jsonl` for the same filtered beat
  range.

## Edges (candidates.json, run_id `azor-cluster-theories-s216`)

14 edges, all sourced from existing graph nodes, all targeting `azor-ahai-theories`.
8× tier-3, 6× tier-4. 12 SUPPORTS, 2 CONTRADICTS (both against Stannis).

| id | source | type | tier | subject |
|---|---|---|---|---|
| Z1 | azor-ahai (character/legend, tier-1) | SUPPORTS | 3 | subject-link: the prophecy's own seven-sign definition |
| Z2 | melisandre | SUPPORTS | 3 | Stannis proclamation |
| Z3 | salladhor-saan | CONTRADICTS | 3 | doubts Stannis's sword |
| Z4 | aemon-targaryen | CONTRADICTS | 3 | "the sword is wrong" |
| Z5 | aemon-targaryen | SUPPORTS | 3 | names Daenerys |
| Z6 | rhaegar-targaryen | SUPPORTS | 3 | Aemon's testimony re: Rhaegar's/Aegon's belief |
| Z7 | melisandre | SUPPORTS | 4 | "R'hllor shows me only Snow" (self-hedged) |
| Z8 | jon-snow | SUPPORTS | 4 | invokes "promised prince, born in smoke and salt" |
| Z9 | jon-snow | SUPPORTS | 4 | NW vow as fiery-weapon reading |
| Z10 | rhaegar-targaryen | SUPPORTS | 4 | "song of ice and fire" |
| Z11 | rhaegar-targaryen | SUPPORTS | 4 | boyhood "must be a warrior" transformation |
| Z12 | barristan-selmy | SUPPORTS | 3 | woods-witch origin of the prophecy |
| Z13 | aemon-targaryen | SUPPORTS | 4 | "the dragon must have three heads" |
| Z14 | dragon-hatching-on-drogo-pyre (event, tier-1) | SUPPORTS | 3 | Dany's pyre sacrifice/rebirth |

**Distinct sources:** 8 (azor-ahai, melisandre×2, salladhor-saan, aemon-targaryen×3,
rhaegar-targaryen×3, jon-snow×2, barristan-selmy, dragon-hatching-on-drogo-pyre).

## Layer rule applied (GNC precedent)

Two edges are deliberately sourced from **existing tier-1 nodes** rather than
character nodes, functioning as subject-links (paralleling GNC's G1 retarget):

- **Z1** → `azor-ahai` (the tier-1 legend/character node, which already documents
  the full prophecy text, the Melisandre/Aemon/Benerro candidate claims, and even
  carries the "R'hllor shows me only Snow" quote in its own `## Quotes`). Z1 quotes a
  *different* sentence (the Asshai'i prophecy definition) than anything already
  quoted on that node, and functions as the theory's anchor back to the legendary
  figure — the same structural move GNC used for its G1 subject-link.
- **Z14** → `dragon-hatching-on-drogo-pyre` (the tier-1 event node for Dany's pyre).
  Quotes "Only death can pay for life" — text the event node does not already quote
  (its own `## Quotes` carries the "Daenerys Stormborn..." and unburnt-emergence
  lines instead) — so this is new evidentiary content, not a restated fact.

One candidate edge was **dropped from the plan** under the same rule: Salladhor
Saan's full Lightbringer-forging legend (Nissa Nissa's sacrifice, `acok-davos-01.md:
137`) is candidate-neutral premise **already fully owned** by three existing tier-1/2
nodes (`azor-ahai`, `lightbringer`, `nissa-nissa`, all of which paraphrase or quote
this exact legend). It does not bear on any specific identity claim, so per the
layer rule it stays prose-only (mentioned in the `## Claim` framing, no edge) rather
than becoming a 15th edge.

## Held-out material

- `the-prince-that-was-promised-theories` and `lightbringer-theories` stubs — left
  dark, folded into `azor-ahai-theories` via aliases (structural decision above).
- The full "Rhaegar is Azor Ahai / Lightbringer three-swords" pattern-match
  (Rhaegar/Trident=first sword, Aegon/Lannister-lion=second sword,
  Lyanna/childbirth=third sword, Jon=the forged weapon) — fenced in
  `## Ungrounded material` as **community**, per the source video's own framing
  ("that's one theory anyway"), not built as edges. No single citable textual beat
  supports the three-way parallel; it's cross-death pattern-matching.
- Show-only Lyanna-names-him-Aegon material (`rhaegar-B36`) — fenced as **show**.

## Open questions

- Whether `azor-ahai-theories`'s new tier-3 confidence (vs. the wiki stub's original
  auto-assigned tier-2) is the right call given the theory has genuinely *more*
  independent in-world testimony converging on it than most fan theories (three
  separate named characters — Melisandre, Aemon, Benerro — independently name a
  Targaryen-blooded candidate). Matt may want to weigh this against R+L=J's tier-3
  during review; I judged tier-3 the honest ceiling given Tier 3-5 is the hard floor
  for the theory layer and no single candidate is textually confirmed.
- Whether the Z1/Z14 subject-link pattern (edges sourced from tier-1 legend/event
  nodes rather than character-testimony nodes) should become a standing convention
  for future theory-cluster builds, the way GNC's G1 retarget was offered but not
  formally adopted as a rule.

## HARVEST (one-line pointers, off-task finds — POINT only)

- `sources/chapters/agot/agot-daenerys-10.md:69` / physical-description /
  Dany's grief-sensory memory of Drogo before the pyre: "He smelled like grass and
  warm earth, like smoke and semen and horses." — vivid, unused sensory-detail beat.
- `sources/chapters/affc/affc-samwell-04.md:37` / homeless-quote / Aemon's dying
  aside "He said the sphinx was the riddle, not the riddler, whatever that meant." —
  cryptic, unresolved in the corpus; possible Chekhov's-gun candidate (House of the
  Undying sphinx imagery).
- `sources/chapters/adwd/adwd-the-griffin-reborn-01.md:121` / homeless-quote /
  Jon Connington's memory of Elia Martell: "Elia was never worthy of him. She was
  frail and sickly from the first, and childbirth only left her weaker." — POV-biased
  physical/character description, useful for characterization or cross-POV-perception
  work on Elia.

## Gates run this session

- All 14 edge quotes byte-verified against `sources/chapters/*.md` (Python
  containment check at cited lines) — see inline verification above.
- All 5 body-prose blockquotes independently re-verified byte-exact.
- All 8 edge-source slugs resolve to live node files (`find graph/nodes -iname`).
- Target slug `azor-ahai-theories` confirmed to exist as the stub being enriched.
- Tier audit: no tier-1/2 stamped on any edge or the node itself (node tier-3; edges
  8×tier-3 + 6×tier-4).

## Mint gate (unchanged, pending Matt)

On explicit go: `scripts/mint_enrichment.py --candidates
working/theories/azor-cluster/candidates.json --nodes-dir
working/theories/azor-cluster/nodes` (note: node lives under `enrich/`, not `nodes/`,
matching the KotLT enrich-only precedent — mint script invocation should apply
`enrich/azor-ahai-theories.node.md` over the stub the same way S214's KotLT enrich
was applied) + `weirwood refresh` + architecture.md sync if new frontmatter fields
are introduced (none are — this node reuses the same `concept.theory` fields R+L=J/
GNC/eldritch already established: `claim`, `status`, `origin`, `video_sources`,
`pass_origin`).
