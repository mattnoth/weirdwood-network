# Session 67 — Stage 4 Pass-1-derived: recovery + comention deprecation + LLM tail (2026-05-23)

**Model:** Opus 4.7 (session was already Opus; the continue prompt recommended Sonnet for the
deterministic/typing work — flagged but unchanged, since a session can't downgrade itself. Mechanical
build work was delegated to script-builder; per-item typing ran on Sonnet via `claude -p`.)

**Mode:** Matt handed off (`/continue stage4-pass1-tail-and-recovery`) then stepped away ("do what you
can"), returned mid-session to authorize the LLM tail ("run LLM tail"), then authorized `/endsession`.

## Starting state
Deterministic spine (S66) = 2,834 typed `book-pass1` edges, committed `047e49b3b`. HEAD was `8cf10e70e`
("wip") — **Matt's own checkpoint** committing the ~31 throwaway `classify_*`/comention scripts S65 flagged
(cleanup remains ON HOLD, his call) + a `next prompt temp.txt`. Working tree clean.

## What was done (Tracks A, C, B; D deferred)

### Two continue-prompt inaccuracies caught (CLAUDE.md #9 / point-in-time-snapshot lag)
1. **Track A's documented mechanism was a no-op.** `pass1-derived-firstname-aliases.json` is WRITE-ONLY
   (audit dump at candidates.py:~1106); the resolver only reads `alias-resolver.json`. Adding entries to
   firstname-aliases.json changes nothing. Built a real supplementary-input path instead.
2. **Track C count.** Prompt said "130 comention files"; actual = **133** `*.comention-edges.jsonl`. The
   broader `prose-edges/*.jsonl` set (1,691 files) is mostly legit `wiki-entity` source_target edges — must
   NOT blanket-stamp. Discriminator = filename, not the (mixed) `evidence_kind` field.

### Track C — deprecate-stamp comention (done)
`scripts/stage4-deprecate-comention-stamp.py` (--dry-run default/--apply, idempotent) + test. Stamped
**133 files / 11,269 rows** in-data with `status: superseded`, `superseded_by: pass1-derived`,
`do_not_promote: true`. Provenance lives in data, not folder names (the project's archiving-contention fix).

### Track A — conservative alias recovery (done + spot-audited)
New `working/wiki/data/pass1-derived-supplementary-aliases.json` (13 hand-vetted single-referent / title-
disambiguated aliases: hotah→areo-hotah, lady-dustin→barbrey-dustin, lord-manderly→wyman-manderly, slynt→
janos-slynt, selmy→barristan-selmy, etc.). Wired into `stage4-pass1-edge-candidates.py` as an **additive
fill-only** merge (new `IN_SUPP_ALIAS`; never overrides/mutates `alias-resolver.json`; logs `+13 merged, 0
conflicts`). Regenerated: **2,818 → 2,834 edges (+16); tail 3,029 → 3,052 (+23)** — recovery grows both, as
predicted. **Spot-audit (manual — green tests missed S66's bugs):** all 13 names left needs-node;
areo-hotah/barbrey-dustin/janos-slynt/wyman-manderly edges all correct person + sensible relations + right
quotes. Validator 3/2,834 (0.1%), none mine (pre-existing). Conform 0 drift. Excluded (queued for Matt):
ambiguous bare surnames (bolton/manderly/drumm/serry), multi-name cells, generics.

### Track B — LLM tail (done; Matt authorized mid-session)
**Execution-substrate discovery:** the Sonnet API is NOT reachable from this Claude Code shell (no
`ANTHROPIC_API_KEY`, no `anthropic` SDK). `stage4-haiku-run.py` revealed the "normal pipeline" mechanism =
**`claude -p` subprocesses** (CLI / Matt's subscription), not raw API and not Agent-tool subagents. Built
`scripts/stage4-tail-classifier.py` (+tests) on that pattern. **Cost control:** subprocesses run with
**cwd=/tmp** so they don't cold-load the 28k-token project CLAUDE.md (~49% cheaper — measured: 13,019 vs
5,588 cache-creation tokens). Batches 40 rows/call with idx-echo alignment.

**INCIDENT — vocab drift caught at the smoke gate (the gate worked):** first 50-row Sonnet smoke emitted
deprecated **`KNOWS`** ×2. Root cause: `load_locked_vocab` naively scraped ALL backtick ALL-CAPS tokens from
architecture.md → **172 tokens**, polluted with `KNOWS` (in the deprecation NOTE prose, not a table row),
plus `ADWD` (a book code!), `POV`, `FIELD_EDGE_MAP`, `LOCATED_IN`, `ACCOMPANIES`, etc. — any of which the
model could emit as a fake edge type. Fix: use the canonical table-row extraction
(`build-edge-type-counts.py::extract_canonical_types` → **163 active types**). Re-smoked clean (0 deprecated,
0 conform violations). **Lesson reaffirmed (drift-detection memory):** green tests didn't catch it — the
50-row eyeball did. Smoke-first is non-negotiable for LLM bulk.

**Full run:** 3 parallel background chains by book (script has no concurrency/retry/incremental-write →
book-partitioned for per-book resumability + modest 3-way concurrency). ~2h wall, 0 rate-limit events.
**Result: 3,052 tail rows → 2,385 typed (78%) / 667 rejected / 0 needs-qual / 0 classify-failed / $20.88**
(agot 482, acok 475, asos 588, affc 353, adwd 487; 112 distinct edge types; 0 deprecated/pollutant).
Output → `_tail-typed/{book}/*.edges.jsonl`, `typed_by: "sonnet"` (separate from the deterministic
`python-map` edges — provenance preserved). Cross-book eyeball strong (illyrio SPOUSE_OF/widowed serra;
cersei DECEIVES margaery; robert PARENT_OF/claimed joffrey — apt qualifiers).

**Final validator: 21/2,385 (0.88%)** — 6× `HOLDS_TITLE→place` (systematic; "Lord of <seat>"), 4×
`ENCOUNTERS` verb-gate (tail prompt omitted the S61/S63 Rule-6 gate), 4× `GUARDS→place`, 2× `MEMBER_OF→
character`, 2× `ATTENDS`, 1× `WORSHIPS`, 1× `CLERGY_OF`, 1× `SPOUSE_OF` qualifier `'claimed'` not in enum.
Several are correct edges blocked by wrong TARGET-NODE types (e.g. `princess-myrcella` typed object.artifact;
HoB&W typed house not religion) — node-typing bugs, not classifier errors. NOT auto-dropped — left for Matt's
cleanup decision.

## Edge tally
**Book-pass1 edges: 2,834 deterministic + 2,385 tail = 5,219.** Test suite 350 green (286 baseline + 8
comention-stamp + ~56 tail-classifier incl. 4 vocab-canonical regression).

## Two resolver levers found (measured; NOT implemented — Matt's "how aggressive" call)
Over 651 ambiguous endpoints: **~72 (~11%) cleanly resolvable by a full-surname rung** ("Ser Rodrik Cassel"
lands ambiguous though `rodrik-cassel` is in the candidates — resolver ignores surname); **~417 (~64%) are
common-leading-word index pollution** ("The council"/"The Kingsguard" → song/text nodes like
`the-book-of-holy-prayer`; "Golden face" → `golden-skulls`). Pollution is the same disease as the spine's 3
type-contract violations. Both fixes are strictly-more-correct but change core resolution semantics → held.

## State at close
Everything **uncommitted** (Matt checkpoints via his own `wip` commits; base rule = commit only when asked).
Tail-typed output gitignored/regenerable. Tracked changes: 2 new scripts + tests, modified candidates script,
supplementary-aliases.json, 133 stamped comention files, regenerated `pass1-derived-*` audit reports, this
detail, worklog, continue prompt, todos. Full notes: `working/stage4-pass1-track-a-recovery-notes.md`.
