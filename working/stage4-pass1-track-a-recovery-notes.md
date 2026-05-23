# Stage 4 Pass-1-derived — Track A/C session notes (2026-05-23, Matt away)

Worked the `stage4-pass1-tail-and-recovery` continue prompt while Matt was stepping away
("do what you can"). Did the no-permission deterministic tracks (A, C); held the LLM tail
(B) for Matt's OK; left worklog/continue-prompt rotation for `/endsession` (needs permission).
**Model note:** ran on Opus 4.7 (session was already Opus); the prompt recommends Sonnet for
this work. Spot-audits done manually rather than trusting green tests.

## State at start (verified)
- Spine committed at `047e49b3b`; HEAD is `8cf10e70e` ("wip") — **Matt's own checkpoint**
  committing the ~31 throwaway `classify_*`/comention scripts S65 flagged + `next prompt temp.txt`.
  Working tree clean at start. (Throwaway-script cleanup remains on HOLD = Matt's call.)
- Baseline: 2,818 edges, 3,029 tail rows, 633 ambiguous rows, 453 distinct unresolved names.
- Two continue-prompt inaccuracies found & flagged (point-in-time snapshot lag, CLAUDE.md #9):
  1. **Track A mechanism as written is a no-op.** `pass1-derived-firstname-aliases.json` is
     WRITE-ONLY (dumped at candidates.py:~1106); the resolver only reads `alias-resolver.json`.
     Adding entries to firstname-aliases.json changes nothing. Real lever = supplementary
     alias input (built this session) or a resolver rung.
  2. **Track C count.** Prompt says "130 wiki-comention files"; actual = **133**
     `*.comention-edges.jsonl` files. (Total `prose-edges/*.jsonl` = 1,691, mostly legit
     `wiki-entity` source_target edges — must NOT blanket-stamp.)

## Track C — DONE (deprecate-stamp comention) ✅
- New script `scripts/stage4-deprecate-comention-stamp.py` (`--dry-run` default / `--apply`),
  test `tests/test_stage4_deprecate_comention_stamp.py`. 286 tests green.
- Stamped **133 files / 11,269 rows** with `status: superseded`, `superseded_by: pass1-derived`,
  `do_not_promote: true`. Idempotent (2nd run = 0 changes). In-data, not dir-archiving (per the
  provenance-in-data principle). **Files are git-TRACKED; NOT committed** (left for review).

## Track A — conservative alias recovery DONE + spot-audited ✅
- New data file `working/wiki/data/pass1-derived-supplementary-aliases.json` (13 hand-vetted
  single-referent / title-disambiguated aliases). Wired into `scripts/stage4-pass1-edge-candidates.py`
  via additive **fill-only** merge (new `IN_SUPP_ALIAS`; never overrides or mutates
  `alias-resolver.json`; logs `+N merged (M conflicts skipped)` → ran as `+13 merged (0 conflicts)`).
- Aliases (key → target): hotah→areo-hotah, noye→donal-noye, lady-dustin→barbrey-dustin,
  lord-manderly→wyman-manderly, tris-botley→tristifer-botley, lame-lothar-frey→lothar-frey,
  lord-peasebury→robin-peasebury, strickland→harry-strickland, slynt→janos-slynt,
  thorne→alliser-thorne, selmy→barristan-selmy, greatjon→jon-umber, lord-bolton→roose-bolton.
- Regenerated (`--apply` x2). **Result: 2,818 → 2,834 edges (+16); tail 3,029 → 3,052 (+23)**
  (recovery grows both, as predicted — recovered names whose hint didn't deterministically type
  fall to the tail). Ambiguous unchanged (rung-b bypasses it). Distinct unresolved 453 → 442.
- **Spot-audit (manual, the gate the prompt demanded):**
  - All 13 names GONE from needs-node.
  - areo-hotah / barbrey-dustin / janos-slynt / wyman-manderly edges eyeballed → all correct
    person + sensible relations + verbatim quotes from the right chapters. No S66-style
    misresolution (no concept-node / title-token bleed).
  - Validator: **3 type-contract violations / 2,834 (0.1%)** — `baelor-blacktyde→seven-kingdoms`
    (WORSHIPS; "the Seven" mis-slugged), `marillion→lady-catelyns-sept` (TRAVELS_WITH),
    `gorys-edoryen→landing-of-the-golden-company` (GUARDS). **None involve the 13 alias targets**
    → pre-existing noise, same disease as the index-pollution issue below. Conform: 0 drift.
- **Excluded (queued for Matt, intentionally conservative):** bare ambiguous surnames
  (bolton, manderly, drumm, serry), multi-name cells ("Robb, Bran, Rickon, her mother"),
  generic/collective cells. "Wrong edges are worse than queued ones."

## Track B — LLM tail RUN ✅ (Matt authorized "run LLM tail" mid-session)
- New `scripts/stage4-tail-classifier.py` (+ tests; 350 green) — invokes **`claude -p --model claude-sonnet-4-6`**
  subprocesses (NOT the Agent tool, NOT raw API — no key/SDK in this shell; this is the "normal pipeline"
  mechanism, same as `stage4-haiku-run.py`). Cost control: subprocesses run with **cwd=/tmp** so they don't
  cold-load the 28k-token project CLAUDE.md (~49% cheaper). Batches 40 rows/call; idx-echo alignment.
- **Drift caught at smoke (the gate worked):** first 50-row smoke emitted deprecated **`KNOWS`** ×2 →
  root cause: classifier scraped ALL backtick ALL-CAPS tokens from architecture.md (172, incl. junk:
  `ADWD`, `POV`, `FIELD_EDGE_MAP`, deprecated `KNOWS`/`LOCATED_IN`/`ACCOMPANIES`). Fixed to use the
  canonical table-row extraction (`build-edge-type-counts.py::extract_canonical_types` → **163 active types**).
  Re-run smoke clean. Lesson reaffirmed: green tests didn't catch this; the smoke eyeball did.
- **Full run: 3 parallel background chains by book** (script has no concurrency/retry/incremental-write →
  book-partitioned for per-book resumability + modest 3-way concurrency). ~2h wall.
- **RESULTS — 3,052 tail rows → 2,385 typed (78%) / 667 rejected / 0 needs-qual / 0 classify-failed / $20.88:**
  agot 482, acok 475, asos 588, affc 353, adwd 487. 112 distinct edge types, 0 deprecated/pollutant types.
  Output: `_tail-typed/{book}/*.edges.jsonl` with `typed_by: "sonnet"` (separate from the 2,834 deterministic
  `python-map` edges — provenance preserved). **gitignored/regenerable.**
- **Validator: 21/2,385 (0.88%)** — categorized for cleanup decision (NOT auto-dropped; some are correct edges
  blocked by wrong TARGET-NODE types, not classifier errors):
  - 6× `HOLDS_TITLE → place` (model maps "Lord of <seat>" to a place target; contract wants a title). Systematic.
  - 4× `GUARDS → place/artifact` (Jon→Wall, Brynden→Riverrun; + `princess-myrcella` is mis-typed `object.artifact` in the graph → node-type bug, edge correct).
  - 4× `ENCOUNTERS` verb-gate-failure (no staging verb; my tail prompt omitted the S61/S63 Rule-6 ENCOUNTERS gate — prompt gap).
  - 2× `MEMBER_OF → character` (resolved to a character named "stark"/"tormund" instead of the house — resolution looseness).
  - 2× `ATTENDS → non-event`, 1× `WORSHIPS → godswood(place)`, 1× `CLERGY_OF → house-of-black-and-white` (typed `organization.house` not `.religion` → node-type bug, edge correct).
  - 1× `SPOUSE_OF` qualifier `'claimed'` not in enum (Ramsay→fake-Arya; should be current/unknown).
- **Combined book-pass1 edge total: 2,834 deterministic + 2,385 tail = 5,219.**
- **Follow-ups for Matt:** (a) decide on the 21 violations — deterministic re-type for the 6 HOLDS_TITLE→place + drop/repair the 4 ENCOUNTERS + 1 bad qualifier; the ~6 node-type-bug ones are graph-node-typing fixes, not edge fixes; (b) add the ENCOUNTERS Rule-6 verb-gate to the tail prompt if re-running; (c) dedup (the tail has some duplicate rows from the spine, e.g. arya SIBLING_OF sansa ×2 same chapter); (d) eventual merge of `_tail-typed/` into the main edge set.

## Track D — NOT done (optional). Validator works on book-pass1 via the existing
   (emit_edge, pass1_relationship) contract path; a first-class `evidence_kind: book-pass1`
   schema branch is a nicety, deferred.

## TWO HIGH-VALUE RESOLVER LEVERS — for Matt's decision (resolver-semantics = his "how aggressive" call)
Measured over 651 ambiguous endpoints (633 rows; a row can have 2 ambiguous endpoints):

1. **Full-surname-match rung (HIGH value, HIGH confidence): ~72 endpoints (~11%).**
   Raw cell names the person fully but resolver uses only the first non-title token and discards
   the surname. e.g. "Ser Rodrik **Cassel**" lands ambiguous across 5 `rodrik-*` even though
   `rodrik-cassel` is literally in the candidate set. Fix: add a rung — if
   `to_slug(title-stripped raw)` exactly equals one candidate slug, take it. Recovers Ser Rodrik
   Cassel (many rows), Brynden Tully, Jason Mallister, Donnel Waynwood, … Strictly more-correct;
   low risk. ~5-min change in `stage4_name_resolver.py` + tests + spot-audit once approved.

2. **Index-pollution filter (clears NOISE): ~417 endpoints (~64%) are not real ambiguity.**
   Collective/generic cells collide with non-person nodes sharing a leading common word:
   "The council"/"The Kingsguard"/"The Sealord of Braavos" → songs/texts (`the-book-of-holy-prayer`,
   `the-seasons-of-my-love`); "Golden face" → `golden-skulls`/`golden-wedding`; "House Stark /
   Eddard Stark" → `house-hornwood`/`house-falwell`. These should be UNRESOLVED, not queued — and
   the same disease produces the 3 validator violations above. Fix options: (a) exclude non-person
   node types (text/song/place/house/event) from firstname candidates; (b) extend the leading-common-word
   stoplist ("the", "northern", "golden", "house", …) like the existing TITLE_PREFIXES/GENERIC_TERMS gates.
   This makes `ambiguous-review.md` actually reviewable (≈234 genuine endpoints, not 651).

## Open questions for Matt (unchanged from continue prompt + new)
- Track B: explicit go + cost ceiling.
- Approve resolver levers #1 (full-surname) and #2 (pollution filter)? Both are his "how aggressive" call.
- The 3 pre-existing type-contract violations: drop them in conform, or leave for the pollution fix to clear?

## Uncommitted changes left for review (NOT committed)
- M scripts/stage4-pass1-edge-candidates.py (supplementary-alias merge)
- A scripts/stage4-deprecate-comention-stamp.py + tests/test_stage4_deprecate_comention_stamp.py
- A working/wiki/data/pass1-derived-supplementary-aliases.json
- M 133 *.comention-edges.jsonl (stamped)
- M tracked audit reports under working/wiki/data/pass1-derived-* (regenerated)
- A this notes file
(gitignored & regenerated: working/wiki/pass2-buckets/pass1-derived/** edges+tail)
