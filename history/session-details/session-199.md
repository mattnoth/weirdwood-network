---
session: 199
date: 2026-07-07
model: Fable 5 (orchestrator) + Opus claude -p extraction workers (Matt-fired) + general-purpose subagent verifiers
track: graph (fire-and-blood)
api_cost: 4 Opus extraction units (Matt-fired from iTerm, ~8 min each) + 5 verifier subagents
graph_mutation: NONE — everything --smoke dry-run; apply stays gated
---

# Session 199 — F&B reconciler fix → Stage-2 quality → §5.1 tuning → ALL pre-bulk gates green

Session 199 ran across multiple windows (server-error interruptions; one worklog entry covers all).
An earlier window applied the 5 Stage-1 reconciler fixes + a 6th (event-type-aware routing) and
parked the strip-boilerplate track behind F&B (see `EVAL-stage1-reconciler-fix.md` and the
strip-vs-fab RECOMMENDATION). This window took the track from "Stage-2 smoke extracted" to
**every §7 pre-bulk gate green**, with two Matt decisions landed on the way.

## 1. Stage-2 smoke (fab-heirs-of-the-dragon-15-p01) + quote repair

First reconcile located only 63.7% of quotes. Diagnosis: the extractor clips quotes mid-sentence
and appends a synthetic terminal '.' (31/33 quarantines), plus 1 OCR doubled-apostrophe
(`Mushroom’'s`) and 1 genuine comma-in-close-quote deviation. Fix philosophy: **repair the quote,
never loosen the matcher** — `locate_or_repair()` retries with trailing punct stripped and stores
the stripped strictly-verbatim form as canonical, so mint's fail-fast locator is untouched;
`norm()` gained an `''`→`'` collapse (mirrored byte-identically in mint — lockstep tests).
Result: 98.9% located. New sidecar `quotes-repaired.jsonl`.

## 2. Fresh Stage-2 eval → PASS-WITH-CONCERNS → all fixes landed

`EVAL-stage2.md` (fresh subagent): extraction strong, zero hallucinations, quote repairs verified
sound 31/31 — plus two NEW blockers, both fixed same window:
- **Type-blind clean-hit routing (R1 class):** `Lorath` (place) UPDATE-routed onto `jaqen-hghar`
  via a junk alias. Fix: type-agreement gate (roster Type guess ↔ node category). The re-run
  caught a second live wrong-match the eval itself had passed: `Sea Snake` (ship) → `corlys-velaryon`.
- **run_id dropped `-pMM`:** p01/p02/p03 same-day runs shared a run_id → merge idempotency would
  silently drop parts 2–3 (R3 class). run_id is now `<unit>-<date>`; merge-plan cites now carry
  the part suffix. Spec amended.
Also landed from the eval's ranked list: review-candidate probes (pack + name-token — the Septon
Eustace row now presents `eustace-dance-of-the-dragons`), CREATE type normalization
(TYPE_SYNONYMS/BARE_TYPE_DEFAULTS), year-aware `era:` for dated CREATE events (92 AC in a
Dance-section unit = targaryen-rule), merge-plan hygiene (orphan bullets, dead-cite refusal,
blank-start cite fix mirrored in mint), `matched.jsonl` audit sidecar, and a mechanical edge-type
vocab guard (canonical 170 via `edge-type-counts.json`; measured drift across all 4 units: ZERO).

## 3. §5.1 auto-accept tuning (23-row in-sample) → out-of-sample validation PASS

Tuning population: the 23 `smoke-auto-accept-disabled` rows across both smoke units, each
hand-ground-truthed. Original rule (top ≥2, runner-up 0 hits): 6/23 accepted, 100% precision,
~30% recall. Three changes: (a) parent/spouse base-name matching (cluster registry stores slugs,
disambiguators say "son of Jaehaerys I" — no surname); (b) punctuation-tolerant tokenization
(";"-adjacent tokens never matched); (c) margin rule = top ≥2 AND strictly outscores runner-up
AND runner-up's hits ⊆ top's (shared evidence can't block; runner-only evidence forces review).
In-sample: 15/23, 0 wrong. A subtle bug was caught by writing the tests: the original
break-after-first-(a)-hit dropped shared title hits, which would have made runner-up subset
checks fail — all (a)-hits are now recorded, score caps category (a) at 1.
A second rule drains the exact-name review flood (57/85 rows): exact-normalized 1.0 top +
margin ≥0.2 + **positive** type agreement (no guess → never accepts). 130 would-accepts across
the smoke units, all verified correct.

**Out-of-sample (Matt fired `heirs-15-p02` + `sons-05-p01`):** adversarial fresh-subagent
ground-truth of all 66 would-accept rows → **0 wrong** (`EVAL-oos-accept-validation.md`). The
era-sensitive splits resolved correctly (two different Rhaenys Targaryens across units; Samwell
Tarly → `samwell-tarly-lord`/"Savage Sam", not POV Sam); the review-held rows were exactly the
dangerous ones (sons' Vulture King candidate is the Dance-era third one; the tie forced review).
p02 also surfaced a new extractor drift class — evidence cells wrapped in literal `"…"` marks
(35.6% located, 0 edges) — fixed by an enclosing-quote-pair repair variant (dialogue matches
strict-first, untouched). After: 94.1% located, 69 edges, disputed_rate 0.101.

## 4. CREATE fresh-verify: 3-for-3 units caught a semantic dupe → step is permanent

Stage-2: `baelon-avenges-aemon-on-tarth` = existing `myrish-bloodbath`. Out-of-sample:
`accession-melee-at-maidenpool` = `tourney-for-king-viserys-is-accession`;
`death-of-alyn-stokeworth` = `harren-the-reds-rebellion`; `daemon-slays-craghas-crabfeeder` =
DUPE-RISK of `war-for-the-stepstones`; renames `birth-of-aegon` → `birth-of-aegon-ii-targaryen`,
`birth-of-maegor-targaryen` → `birth-of-maegor-i-targaryen` (bare slug is a declared
disambiguation hub). Reports: `fresh-verify-creates.md`, `EVAL-oos-create-verify.md`.

## 5. Matt decisions

1. **Novel event subtypes ADOPTED** — `event.appointment`/`event.exile`/`event.birth`/
   `event.investiture` added to architecture.md's type table (rule 6 sync same stroke), including
   the `birth-of-<canonical-char-slug>` convention. Incidental: `event.death`/`capture`/
   `ceremony`/`council` are live but undocumented (pre-existing; todo).
2. **`identity_line` WIRED** — the reconciler now derives a book-grounded Identity line from the
   first surviving Node-Prose bullet (pronoun/length guards; un-doubled when name-prefixed).
   58/58 merge-plan entries carry it; 18/48 distinct targets still have the literal "…from the
   AWOIAF wiki." placeholder and get upgraded at apply. The strip-track's parking premise holds.

## 6. §7.2 dispute-axis gate: FAIL → quarantine → PASS (the session's big catch)

First formal stratified audit: **FAIL** — over-tag 0.0% but missed-hedge **26.9%**. The extractor
tags sentence-local hedges perfectly and is blind to passage-scope framing ("Here is where our
sources diverge" … "Of the aftermath, these things are certain"): one un-hedged sentence in the
p02 exile zone minted 6 tier-1 artifacts including an event node whose slug hard-codes Mushroom's
version of the cause. Insinuation subtype: "favorite" euphemism + Mushroom detail upgraded to
tier-1 `LOVER_OF`.

Fix (deterministic, prompt untouched): **dispute-proximity quarantine.** Untagged artifacts
located within ±1 line (fab files are paragraph-per-line — the first ±10 attempt held 51 rows on
an audit-certified-clean unit before the paragraph-granularity realization) of a STRONG hedge
term (chronicler names + divergence framing; certainty markers clear the neighborhood) are HELD
to `dispute-review.jsonl`, never emitted; untagged `LOVER_OF`/`PARAMOUR_OF` always held. Weak
generic hedges ("rumor", "it was said") were measured and deliberately EXCLUDED — 100% of false
holds on clean units, 0 real catches (the extractor already tags sentence-local hedges). Held ≠
demoted: adjudication at apply via the per-unit fresh-verify, so no deflation possible.
Empirical tuning record: `scratchpad tune_window.py` table in `EVAL-stage2-reconciler-tuning.md`.

**Re-audit v2: PASS — 0.0% both directions, 100% quarantine recall** on the prior failure set;
certainty-rescue verified both ways. Non-gating residuals documented: 52.6% false-hold rate
(mostly "mushroom" in non-attributive roles — nickname parentheticals; cheap fixes listed) and
weak narrator hedges outside the lexicon (zero escapes observed; `disputed_rate`+`dispute_held`
in run-summary are the bulk drift alarms).

## 7. Where this leaves the track

All §7 gates green. Tests 63/63 (`scripts/test-fab-reconcile.py`). Next = Matt's apply-go on the
4 smoke units per §8 (checkpoint → mint → merge → finalize → refresh; dispositions + staged mint
patch + architecture batch land with it), then the 35-unit bulk extraction (Matt-fired, ~5h).
Incidental graph flags parked to todos: `vaegon`/`vaegon-targaryen` dupe, `great-council-of-101-ac`
mistyped+empty, `manfred-hightower-aegons-conquest` typed `event.war`, no node for the historical
Ronnel Arryn, `jaqen-hghar` junk "Lorath" alias.
