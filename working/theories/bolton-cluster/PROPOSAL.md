# Bolt-On cluster — S216 staging proposal (2026-07-13)

**Unit:** Theories wave-1 Bolt-On cluster ("is Roose Bolton a skin-stealing
immortal?"). **ENRICH-only** — no new node minted; this rewrites the existing empty
`roose-bolton-theories` stub. **Graph mutation: NONE.** All files live under
`working/theories/bolton-cluster/`. Staged at the mint gate per the theories-track
STAGING-ONLY decision (2026-07-13) — no mint without Matt's explicit go.

## What was built

- `enrich/roose-bolton-theories.node.md` — full rewrite of
  `graph/nodes/theories/roose-bolton-theories.node.md` (previously an empty stub:
  blank `## Identity` / `## Edges`, `confidence: tier-2`, no aliases). Slug
  preserved (`roose-bolton-theories`); `wiki_source`, `bucket_id`, `prompt_version`
  carried forward unchanged; `node_version` bumped 1→2; `pass_origin` updated to
  `theories-wave1-s216`.
  - `name`: "Roose Bolton is a skin-stealing immortal" (claim-style, per the
    ratified KotLT precedent).
  - `aliases`: "Bolt-On", "Roose Bolton theories", "Roose Bolton immortality
    theory", "Roose Bolton skin-stealer theory" — natural spaced phrases.
  - `confidence: tier-4` — the theory has some genuinely direct textual anchors
    (Roose's own leeching-for-long-life line, Ramsay's matching eyes) but the
    central skin-stealing/body-swap mechanism is pure inference, and the source
    video's own verdict is explicitly low-confidence ("vague hints," "red or pale
    herring"). Individual edges range tier-3 (the two strongest, most direct
    quotes) to tier-5 (the weakest imported analogies).
  - `status: open` — no show confirmation. The show's version of Roose dies a
    mundane, non-magical death (stabbed by Ramsay, S6), which if anything cuts
    *against* the theory; this is fenced as a **show** bullet in Ungrounded
    material, not folded into status logic.
- `candidates.json` — 8 edges (B1–B8), all `verify: true`, all byte-checked
  against `sources/chapters/*.md` at the cited line (Python exact-match script,
  8/8 pass after one fix — see below).
- This file.

## Edge summary

| id | type | source | tier | gist |
|---|---|---|---|---|
| B1 | SUPPORTS | old-nan | tier-4 | Night's King/Other union story (Old Nan to Bran) |
| B2 | CONTRADICTS | old-nan | tier-3 | Old Nan's own punchline: "He never was. He was a Stark" — rules out "a Bolton" |
| B3 | SUPPORTS | roose-bolton | tier-3 | Roose's own words: "Frequent leechings are the secret of a long life" |
| B4 | SUPPORTS | roose-bolton | tier-5 | "pale grey mask... chips of dirty ice" (weak — same passage warps every guest's face) |
| B5 | SUPPORTS | ramsay-snow | tier-4 | Ramsay's eyes already match Roose's "chips of dirty ice" |
| B6 | SUPPORTS | coldhands | tier-5 | Congealed-blood/blackened-extremities mechanism, imported from an unrelated wight-physiology passage |
| B7 | SUPPORTS | domeric-bolton | tier-4 | Roose's evasive-sounding kinslaying rhetoric about Domeric's death/Ramsay |
| B8 | SUPPORTS | house-bolton | tier-5 | Bolton flaying culture (literal, non-magical) as thematic scaffolding |

6 distinct source nodes across 8 edges (`old-nan` and `roose-bolton` each carry two
edges on independently distinct quotes/points — same reuse pattern the ratified
rlj-cluster set with `eddard-stark`, there across two different theory targets;
here within one target theory since Old Nan's single story both supplies and
undercuts the theory's founding claim, and Roose's own speech supplies both the
strongest support quote and the weakest physical-description one).

**Notable finding:** B2. The theory's own founding story (Old Nan's Night's King
tale) contains, two sentences later, Old Nan explicitly naming "a Bolton" as one of
several *wrong* folk guesses about the Night's King's identity, then resolving it as
"a Stark." Neither the source video nor (as far as this pass can tell) the wider
fan theory engages with this — it's a genuine, undealt-with textual complication,
not previously flagged in the ASX extraction's own beat list (`bolton-B09` in
`working/theories/extractions/8MO2Yb2OJ6Q.jsonl` mis-paraphrased this same passage
as "Old Nan says the man in the story may have been a Bolton," omitting the
explicit denial that follows in the very next clause — the regrounding-agent
correctly flagged that beat `byte-fail` rather than fabricate a supporting quote;
this pass instead grounded the omitted denial itself as a CONTRADICTS edge).

## One quote-verbatim fix during drafting

Initial B7 quote spliced two non-adjacent sentences from the same speech with an
inserted "…" that was not in the source text (only the mid-sentence "…" already
present in "Tell me, my lord … if the kinslayer…" is genuine). Caught by the
byte-verify script before finalizing; B7 was narrowed to the single verbatim
closing sentence, and the node body's quote block was corrected to match, with the
dropped context (Roose's "I say poison" line) restated as unquoted prose instead of
folded into the quote.

## Held-out material (Ungrounded, never edges)

- **show** ×2 — Roose's mundane on-screen death (cuts against); the fireball
  children-of-the-forest genre-normalization aside.
- **community** ×5 — the core body-swap/skin-stealing mechanism and its timing to
  Ramsay's legitimization; Ramsay's eyes as his own Other-ness rather than Roose's;
  Roose as Domeric's actual killer / killer of his other trueborn children for
  lacking pale eyes; Roose as literally part-Other or the Night's King himself; the
  video's own thematic-objection-and-rebuttal exchange (monsters-cheapen-the-theme
  vs. Others-already-exist).
- Two grounded-but-not-edge prose quotes used for scene-setting/context only (per
  the abduction-of-lyanna precedent): Osha's wights speech (`agot-bran-06.md:145`,
  general genre-plausibility, says nothing about Roose) and the "agelessness"
  portion of the Reek-POV Roose description (`adwd-reek-02.md:221`, to avoid a
  third `roose-bolton` edge when two (B3, B4) already anchor the node).
- `bolton-B09` itself (the mis-paraphrased "may have been a Bolton" beat) — not used
  as a quote source; superseded by the B2 CONTRADICTS edge grounded independently
  against the actual line.

## Open questions for Matt / later passes

1. Same structural question the S216 RLJ review raised and left unadopted: should
   `roose-bolton-theories` carry a "subject-link" edge to `roose-bolton` (or to an
   event node, if one existed for "identity of the Night's King") distinct from the
   evidence SUPPORTS/CONTRADICTS edges? Not created here, consistent with the S216
   ratified-as-is convention set.
2. Whether `tier-4` (vs. `tier-5`) is the right overall node confidence — reasonable
   people could call this `tier-5` given how thin the actual mechanism evidence is;
   flagging for review rather than defaulting to the harsher grade myself, since two
   of the eight edges are tier-3 and genuinely direct (B2, B3).
3. No RLJ-style "GRRM-interview" or "TWOW" material surfaced in this substrate —
   the video is entirely book-and-show sourced; nothing held out on that account.

## HARVEST (off-task pointers found while in the text)

- `sources/chapters/adwd/adwd-reek-03.md:227` / character-backstory / Roose's own
  account of fathering Ramsay on a miller's wife, including "I gave her the mill and
  had the brother's tongue cut out" — rich, ungrounded-here material for a future
  Ramsay-Snow-origin or Roose-Bolton character-node enrichment dip; not used in this
  cluster (the "peaceful land, a quiet people" phrase repeats here too, at line 227,
  a second occurrence of the line already grounded once at line 129).
- `sources/chapters/affc/affc-arya-02.md:245-249` / faction-color / the House of
  Black and White's recurring-visitor descriptions ("the fat fellow," "the handsome
  man," "the kindly man," "the squinter," "the lordling," "the starved man") sit
  right next to the grounded B8 cupbearer line — good future material for a
  Faceless Men / House of Black and White node enrichment, not used here.
- `sources/chapters/asos/asos-bran-04.md:105` / atmosphere-quote / "Night's King was
  only a man by light of day... but the night was his to rule" — a strong closing
  line for the Night's King tale, not cited in this cluster (not needed for any
  Bolt-On edge) but notable for a future Night's King theory/lore node.
- `sources/chapters/adwd/adwd-reek-01.md:91` (same line as edge B5) / description /
  the full paragraph continues past the quoted eyes sentence into an extended
  physical description of Ramsay's "ugly," "fleshy" build — potential
  character-node physical-description backfill for `ramsay-snow`, not extracted
  here.
