# Repo Reorganization Plan — 2026-06-12

> **PLAN ONLY. No file in this repo moves, changes, or disappears because this document exists.**
> This is the remaining piece of `progress/continue-prompts/2026-06-07-repo-audit-strategy-reconciliation.md`
> (scope item 6, "repo structure audit"). Everything else in that track was executed by the
> 2026-06-11 fable-audit session — see `working/audits/fable-audit-2026-06-11/SESSION-CHECKPOINT.md`.
>
> **Recommended model for execution sessions:** Sonnet 4.6 (mechanical `git mv` + grep work). Phase gates
> that need judgment (disposition-table execution) ride along with the design-doc consolidation sessions.
>
> **Hard boundaries respected throughout:**
> - `sources/` — immutable, never touched.
> - `graph/` — not touched (this is repo hygiene, not graph edits).
> - `history/` **contents** — never edited (records-of-thought rule). Moves *into* history/ are
>   additive and permitted (S36 precedent, restated in `history/README.md`). New subdirs get
>   2-line entries appended to `history/README.md`.
> - `scripts/` — no moves proposed here. Script archiving is its own later session per
>   `scripts/README.md` (9 ARCHIVE-CANDIDATE tags, 27 comention scripts deliberately KEPT per S73).
>   This plan only notes where working/ moves are *coupled* to that session (Phase 4).
> - `.claude/` — not touched. Where a move would invalidate a command/agent prompt, the move is
>   deferred to the session that owns that tooling (noted per row).
> - Top-level `scratch*` / `next.md` — Matt's private files, not read, not triaged (CLAUDE.md rule).

## Action legend

| Action | Meaning |
|---|---|
| KEEP | Live workspace or live record; stays where it is |
| MOVE-P1 / MOVE-P2 | Move in Phase 1 / Phase 2 (this plan's own execution) |
| DEFER-CONSOLIDATION | Already has a row in `working/audits/fable-audit-2026-06-11/design-doc-proposal.md` §3 (the Option-A disposition table, pending Matt's pick). That table governs; this plan does not restate targets. Executed as consolidation Session 4. |
| DEFER-SCRIPTS | Coupled to the future scripts/ archiving session; move together |
| MATT | Blocked on a decision only Matt can make; options stated, no recommendation executed |
| NOTE | No action; recorded so it isn't re-discovered |

**Universal safety rule for every move:** `git mv` only (preserves history), preceded by
`grep -rn "<filename-or-path>" --exclude-dir=history --exclude-dir=sources --exclude-dir=.git .`
A hit in a *living* file (CLAUDE.md, todos.md, READMEs, runbooks, scripts, .claude/, continue-prompt
manifest) blocks the move until that reference is updated in the same commit. Hits in records
(worklog session entries, session-details, audit reports, session-results) do NOT block — records keep
stale paths by established convention (precedent documented in `working/wiki/README.md` "History note").
Provenance lives in the data files themselves, never in their directory location — so moves never
rewrite file contents, except additive stale-tag preambles where the disposition table calls for them.

---

## 1. `working/` triage

Sorting rule (from CLAUDE.md): `working/` = ACTIVE scratchpad only. Three bins: **live workspace**,
**completed work → history/**, **feeder material for the design-doc consolidation** (must NOT move
before consolidation — these are its source texts).

### 1a. Live — KEEP (no action)

| Current path | Action | Reason |
|---|---|---|
| `working/todos.md` | KEEP | The queue; just cleaned (420→232) |
| `working/infobox-merge/` | KEEP | THE live track (spec v2; merge script + dry-run is checkpoint item 4) |
| `working/audits/fable-audit-2026-06-11/` | KEEP | Live audit; checkpoint waves still relaunching from it |
| `working/nomenclature-reform-proposal.md` | KEEP | Pending Matt review (v1, fixes queued in checkpoint item 3) |
| `working/runbooks/` (live ones: edge-modeling-audit-loop, mechanical-extraction-howto, wiki-pass2-pipeline, wiki-pass2-orchestration) | KEEP | Live procedures / design-doctrine feeders. Stale runbooks (stage4-events-haiku-bulk, general-watcher, pass1-auto-advance, the two `-DONE` files) already have a disposition-table row: stamp → `runbooks/archive/` — DEFER-CONSOLIDATION |
| `working/wiki/data/` | KEEP | Permanent reference products, downstream code reads them (infobox merge reads `infobox-data.jsonl` next session) |
| `working/wiki/pass2-staging/` | KEEP | Compact canonical run record; documented in `working/wiki/README.md`; bucket-targeting still uses triage-manifest |
| `working/logs/` | KEEP / NOTE | Gitignored runtime artifacts (`.gitignore:50`); nothing to do |
| `working/session-results/` (the directory + README + June files) | KEEP dir | Live convention — watcher handoff channel; referenced by `working/runbooks/general-watcher.md`, worklog, todos. Old *files* rotate out (§1b) |
| `working/edge-modeling/post-plate5-backfill-design.md` | KEEP | Live design until Tracks A/B/C ship (its disposition row says the same) |

### 1b. Completed work → history/ (this plan executes)

| Current path | Proposed action | Reason | Reference-breakage check |
|---|---|---|---|
| `working/session-results/2026-05-*.md` (27 files, watcher-era + stage4/events) | MOVE-P2 → `history/session-results/` (new dir; flat, filenames already dated) | Channel is for *current* handoff; May files are spent records of deprecated/finished tracks. Keep the 5 June files + README. **Add a rotation rule to the README:** files older than the last 2 sessions' tracks move on each /endsession | grep each filename; expect hits only in worklog records + each other (records, non-blocking). `general-watcher.md` references the *directory*, which stays |
| `working/audits/` completed audit folders — all 13 dated ≤2026-05-29 *except* `events-haiku-bulk-2026-05-29` (agent-model-fit, citation-corpus-rerun, citation-issues, cleanup-scrubs, duplicate-detector, missing-nodes, orphan-edges-04-30/05-01/05-02, schema-drift ×2, wiki-prose-coverage) | MOVE-P2 → `history/audits/` (new dir, folder-per-audit preserved) | Audits are done; their findings are encoded in graph/docs. working/audits keeps only live + latest-baseline | grep folder names; `.claude/agents/` hits found in the broad scan — verify orphan-edge-finder / schema-drift-auditor agents don't *write* into a dated folder being moved (they create new dated folders; confirm per agent before moving) |
| `working/audits/orphan-edges-2026-05-12*` loose files (4: 2 .md + 2 .tsv) | MOVE-P2 → `history/audits/` | Superseded by the 2026-06-09 baseline | Same grep; non-blocking expected |
| `working/audits/orphan-edges-2026-06-09*` (md + tsv) | KEEP | Latest orphan baseline; the 115-orphan-slug fix in the infobox-merge spec cites it | — |
| `working/audits/events-haiku-bulk-2026-05-29/` | KEEP until Track B | The NO-GO'd Haiku emits are Track B's input (`2026-06-05-edge-modeling-plate-4-haiku-disposition.md` re-buckets them). Moves with Track B's completion | grep confirms the Track-B continue prompt's paths before any move |
| `working/stage4-hint-inventory.md` (763 KB) + `working/stage4-hint-residue.md` (225 KB) | MOVE-P2 → `history/archive/stage4-comention/` (new subdir) | Giant output records of the superseded comention track; ~1 MB of scratchpad weight | Written by `scripts/stage4-pass1-hint-inventory.py` (SUPERSEDED-tagged) — update its output path comment or note in scripts/README at move time; no readers found |
| `working/stage4-pass1-track-a-recovery-notes.md` | MOVE-P2 → `history/archive/stage4-comention/` | May-23 recovery record, pre-reification; episode closed | grep `track-a-recovery` — zero living refs found |
| `working/extraction-stats.csv` (root of working/, May 2) | MOVE-P2 → `history/archive/` | Superseded by `working/extraction-stats/` per-book files | grep — expect zero |
| `working/extraction-stats/` (whole dir, 10 csv) | MOVE-P2 → `history/extraction-stats/` — **second choice: KEEP** | Pass 1 + Pass 2 are DONE; these are frozen run stats, nothing writes them anymore. But CLAUDE.md's directory tree + conventions section name this path | BLOCKED-BY-LIVING-REF: requires CLAUDE.md tree edit in same commit; check `/endsession` command + status-reporter agent for path mentions. If the greps get noisy, downgrade to KEEP — value is low either way |
| `working/edge-vocabulary-gaps.md`, `working/tier3-promotion-plan.md` | DEFER-CONSOLIDATION | Disposition rows exist (stale-tag → history/) | per disposition |

### 1c. Feeder material — must NOT move before the design-doc consolidation

These are the source texts for `reference/design/` (Option A, Matt's pick pending). Moving them first
would make the consolidation sessions dig through history/. All have disposition-table rows; the
consolidation's own Session 4 ("disposition sweep") executes them.

| Current path | Action | Note |
|---|---|---|
| `working/edge-modeling/` (everything except post-plate5-backfill-design.md — 14 MB, 293 tracked: reification design, SESSION-LOG, plate reports, merge diffs, lineage/, plate3/4 result dirs) | DEFER-CONSOLIDATION | Richest source for `edge-strategy.md`. After absorption: stamps on the two design docs, then the folder archives wholesale → `history/edge-modeling/`. Living refs to fix at that time: `working/runbooks/edge-modeling-audit-loop.md`, todos.md links |
| `working/agent-fleet-specs/` (4 design docs + missions/ prompts + worker-snippets/ + vocab-lock records, 12 tracked) | DEFER-CONSOLIDATION | Retired-unexecuted fleet → `history/archive/` with stale-tag preambles per disposition. Living refs to fix: **CLAUDE.md directory tree + Working Directory section**, todos.md, `.claude/commands/check-fleet.md` + `watcher.md` + `worker.md` (stamp or retire those commands in the same change — they exist solely for this apparatus) |
| `working/qualifier-vocab/` (3 files) | DEFER-CONSOLIDATION | Records; `reference/edge-qualifier-vocab.md` is the living spec (disposition row: archive wholesale) |
| `working/stage4-pass1-derived-edges-design.md` | DEFER-CONSOLIDATION | Pivot rationale absorbed into `pipeline.md`, then retired to history/ (disposition row) |

### 1d. Coupled to the scripts/ session — DEFER-SCRIPTS

| Current path | Action | Reason | Reference-breakage check |
|---|---|---|---|
| `working/missions/` (42 MB, 386 tracked — batch results, locks, state.jsonl for the two superseded stage4 missions + case-collision runs) | DEFER-SCRIPTS → `history/missions/` | Completed mission state, but ~20 `scripts/stage4-*`/`mission-stage4-init.py` scripts and `.claude` worker/watcher commands hard-code `working/missions/` paths. Those scripts are the same SUPERSEDED set the scripts session will archive — move state and tooling **together**, one coherent sweep, instead of breaking retired-but-present tooling now | the scripts-session grep list IS this list; nothing else reads it |
| `working/batch0007_classify.py`, `classify_edges.py`, `classify_haiku.py`, `classify_proper.py`, `stage4-classify-temp.py` (strays at working/ root) | DEFER-SCRIPTS → same archive destination as their stage4 siblings | One-off classifiers from the comention era that never lived in scripts/; archiving them belongs to the same sweep so the comention tooling story stays in one place | grep found zero living refs; re-grep at move time |
| `working/wiki/classify-mormont-edges.py` (stray, single one-off) | DEFER-SCRIPTS (or fold into MOVE-P2 if Phase 2 lands first — zero refs, zero risk) | Misplaced one-off; `working/wiki/` README defines only data/, pass2-buckets/, pass2-staging/ | grep `classify-mormont` — zero hits |

---

## 2. Stale staging trees

### 2a. `working/wiki/pass2-buckets/` — the skeleton-untrack decision (MATT — options restated, NOT decided)

State (verified this session): **23,081 tracked files**; **7,180 stale `skeleton/*.node.md`** (~28 MB,
S72-verified redundant with `graph/nodes/`; a raw grep counts 7,192 because `_archive/` holds copies).
788 MB on disk total (most of the bulk is the gitignored `pass1-derived/` + enriched-candidates outputs).
The *disk* contents stay regardless — bucket workspaces are Pass-2 provenance and future stages target
them (`working/wiki/README.md`). The open decision is **git tracking only**, deferred at S73
(todos.md:170). Options, restated without a verdict:

1. **Status quo** — keep skeletons tracked. Cost: ~28 MB repo bloat, 7,180 stale files in every clone.
   Risk: zero.
2. **`git rm --cached` + gitignore the `*/skeleton/` dirs** — repo de-bloats; disk untouched, so the
   ~24 `wiki-pass2-*` promotion scripts that read `skeleton/` keep working. Risks: skeletons lose git
   backup (regenerable via Stage 3a, and redundant with graph/nodes/, but that's a recovery *procedure*,
   not a copy); tracked-vs-disk divergence is a standing confusion source; and the entanglement means
   any future re-promotion run quietly depends on untracked state.
3. **Untrack + cold copy first** — tar the 7,180 skeletons to `history/` (or external storage) before
   `git rm --cached`. Costs one ~28 MB tarball; removes the only real risk of option 2.

Not scheduled in any phase below. 28 MB isn't urgent (S73's own assessment). When Matt picks, it's a
single focused session: the pick + the gitignore line + a one-paragraph note in `working/wiki/README.md`.

### 2b. Gitignored output dirs — NOTE only

`working/wiki/pass2-buckets/*/prose-edge-candidates-enriched/` (.gitignore:22), `pass2-buckets/pass1-derived/`
(.gitignore:28), `working/logs/` (.gitignore:50). All intentional, documented in .gitignore comments.
No action; listed so the next audit doesn't re-discover them.

---

## 3. `progress/` hygiene

`progress/continue-prompts/README.md` (built 2026-06-11) is the manifest; `archive/` already exists with
17 DONE files. This plan extends the existing pattern — archive what the manifest already marks
DONE/STALE, keep LIVE/HALTED in the top level so `/continue` shows only actionable tracks.

| Current path | Proposed action | Reason | Reference-breakage check |
|---|---|---|---|
| `2026-05-02-stage4-v1-prose-edge-classifier.md` | MOVE-P2 → `archive/` | Manifest: STALE-superseded-by-pass1-derived-pivot | grep todos.md `→ continue:` links + `.claude/commands/continue.md` mechanics (it lists the dir dynamically — confirm) |
| `2026-05-05-dialogue-meals-mention-index-design.md` | MOVE-P2 → `archive/` | Manifest: STALE (predates pivot + reification); Dialogue v2.1 must be re-designed anyway per todos | same grep; if the Dialogue todo links it as design input, update the link to the archive path (living ref) |
| `2026-05-16-stage4-bulk-resume.md`, `2026-05-17-stage4-bulk-watcher.md` | MOVE-P2 → `archive/` | Manifest: STALE (comention deprecated S65) | same grep |
| `2026-05-23-stage4-pass1-finishing.md` | MOVE-P2 → `archive/` | Manifest: STALE-superseded-by-edges-v1.3 | same grep |
| `2026-05-26-stage4-events-enrichment.md` | MOVE-P2 → `archive/` | Manifest: STALE-superseded-by-plate4-haiku-disposition | same grep |
| `2026-06-01-events-bulk-escalation-pick.md` | MOVE-P2 → `archive/` | Manifest: STALE-superseded-by-backfill-Track-B (5 path descriptions are reference-only — archive preserves them) | same grep; Track-B prompt may cite it (update that one living link) |
| `2026-05-31-events-v2-promotion-chain/` (folder) | KEEP until Track B closes | Manifest: HALTED-gated; absorbed into Track B — archive it in the same commit that closes Track B | — |
| LIVE prompts (2026-06-05, 2026-06-07, 2026-06-11, 2026-06-12) | KEEP | Manifest: LIVE. The 2026-06-07 prompt flips to DONE when *this plan* is accepted — archive it then | manifest row update |
| `progress/continue-prompts/README.md` | UPDATE (same commit as each batch of moves) | It's the living manifest — every move above edits its table; archive section gains the new rows | — |
| **Misfiled: `2026-06-08-alias-and-display-design.md`** | MATT-confirm, then MOVE-P2 → `history/archive/2026-06-08-alias-and-display-chat-excerpt.md` with a 3-line preamble: *raw chat excerpt, trimmed by Matt 2026-06-xx; design formalized in `working/edge-modeling/post-plate5-backfill-design.md` + `reference/alias-resolver-design.md`* | Manifest already flags it: "not a continue prompt — raw agent chat export… should be deleted or renamed." It's a record, so history/archive/ (never delete). **Matt has uncommitted edits trimming it 293→87 lines** — commit his trim first, and confirm he's done curating before moving | living refs: manifest README row (update); worklog + PLATE5-READINESS + SESSION-2026-06-07-AUTONOMOUS-REPORT mentions are records (non-blocking) |

No other `progress/` substructure is needed — `archive/` + the manifest already are the structure; the
gap was just that six STALE prompts hadn't been moved into it.

---

## 4. Root strays + the replies/ledger convention

| Current path | Proposed action | Reason | Reference-breakage check |
|---|---|---|---|
| `scr` (untracked, 1.5 KB, Jun 9) | MATT | Looks scratch-family but isn't named `scratch*`, so neither the gitignore pattern nor the don't-read rule formally covers it. Not read per the spirit of the scratch policy. Ask Matt: (a) it's scratch → he renames to `scratch-*` (gitignored, invisible), or (b) it's project material → he says where it goes | none (untracked) |
| `next.md`, deleted `scratch-*` files, deleted `Untitled 6.rtf` | NOTE — no action | `next.md` is gitignored and explicitly agent-off-limits (its own header). The deletions are Matt's, staged, awaiting his commit | — |
| `next prompt temp.txt` (TRACKED, May 20) | MOVE-P1 → `history/archive/2026-05-20-next-prompt-temp.md` | A pasted session-handoff note from the stage4-haiku era (points at a continue prompt that no longer exists at top level). Tracked, so it's project material, and it's spent | grep — zero refs found; re-verify |
| `STAGE4-SMOKE-REVIEW.md` (root, May 24) | MOVE-P1 → `history/archive/stage4-comention/` | "For Matt" plain-language review of S69; its three waiting decisions were made long ago (S70+ pivot). Pure record | grep — zero refs found |
| `BEFORE-LEAVE-RESUME-2026-05-28.md` (root) | MOVE-P1 → `history/archive/` | Spent resume note; the paused Events run completed (S79-S81) and was then NO-GO'd | grep — zero refs found |
| `EDGE_MODELING_VALIDATOR_LOG.md` (root, 21 KB) | KEEP until consolidation, then archive with the edge-modeling records | Self-described "standing, append-only" validator surface Matt reads. Backfill Tracks A/B/C are still pending, so it may still receive appends; and it's feeder material for `edge-strategy.md`'s validation-stack section. Don't move a file Matt deliberately keeps at eye level — flag it in the consolidation sweep instead | at archive time: grep + note in `edge-strategy.md` where the validator role now lives |

### The replies/ledger convention (proposal)

File-based replies are now Matt's standing mechanism (`working/reply-to-audit-session-2026-06-11.md`
was written *to be executed by an agent* — "this IS Matt's reply. Execute it."). One-offs at working/
root will accrete exactly like the stage4 strays did. Proposed convention:

1. **`working/replies/`** (new dir) — Matt drops `YYYY-MM-DD-<topic>.md` reply/instruction files;
   sessions execute them. Companion ledgers (`YYYY-MM-DD-<topic>-ledger.md`) live alongside.
2. **Lifecycle:** while any item in the reply is unexecuted, it stays. When fully executed, the
   executing session appends one line at top — `> EXECUTED <date>, session NN` — and `git mv`s it to
   **`history/replies/`** (new dir). Records rule applies after the move: never edited again.
3. **CLAUDE.md** Working Directory section gains two lines describing this (edit rides with Phase 2's
   CLAUDE.md commit; until then the convention is recorded here and in todos.md).
4. **Retroactive application:** `working/reply-to-audit-session-2026-06-11.md` +
   `working/deliverables-ledger-2026-06-11.md` move to `history/replies/` **only after** the
   SESSION-CHECKPOINT remaining waves complete (the checkpoint instructs relaunched agents to read the
   reply file at its current path — moving it now breaks a live pointer). MOVE-P3-gated.

---

## 5. Sequencing, safety, effort

Ordering principle: lowest-risk, zero-living-reference moves first; anything entangled with live
tooling or pending consolidation waits for its gate. Lesson honored: **archiving-by-directory has been
contention-prone** (S73: a directory-level archive proposal swept up 27 comention scripts that were
deliberately kept as a recall lever). So: file-level moves wherever a directory has mixed liveness;
directory-level moves only where every file inside has the same disposition; provenance lives in the
data, so no file content is rewritten beyond additive preambles.

### Phase 0 — preconditions (no moves)
- **Commit the current tree first.** The entire fable-audit session is uncommitted (per
  SESSION-CHECKPOINT); `git mv` on top of a dirty 30-path tree makes the diff unreviewable. Needs
  Matt's commit authorization. Also commit Matt's trim of the alias-and-display file.
- Matt's picks collected (any time, none block Phase 1): design-doc Option A/B/C; skeleton-untrack
  option 1/2/3; `scr` disposition; replies-convention sign-off; alias-and-display move confirmation.

### Phase 1 — zero-reference strays (~9 moves) — effort: 0.25–0.5 session, Sonnet
Root: `next prompt temp.txt`, `STAGE4-SMOKE-REVIEW.md`, `BEFORE-LEAVE-RESUME-2026-05-28.md`.
Working root: `stage4-hint-inventory.md`, `stage4-hint-residue.md`, `stage4-pass1-track-a-recovery-notes.md`,
`extraction-stats.csv` (+ optionally `working/wiki/classify-mormont-edges.py`).
Creates `history/archive/stage4-comention/`. Per-move grep; append new-dir lines to `history/README.md`.

### Phase 2 — manifest-driven + rotation moves (~55 moves) — effort: 0.5–1 session, Sonnet
- 7 STALE continue prompts → `progress/continue-prompts/archive/` + manifest README update + todos
  `→ continue:` link fixes.
- 27 May session-results → `history/session-results/` + rotation rule added to the channel README.
- ~14 completed audit folders + 4 loose orphan-edge files → `history/audits/` (after per-agent
  write-path verification; `events-haiku-bulk-2026-05-29` and `orphan-edges-2026-06-09*` stay).
- Misfiled alias-and-display file → `history/archive/` (gated on Matt's confirmation).
- `working/replies/` convention created + CLAUDE.md Working Directory note (+ optional
  `working/extraction-stats/` move with its CLAUDE.md tree edit — drop if greps get noisy).

### Phase 3 — gated on design-doc consolidation (Matt's Option pick → ~3-4 sessions, already estimated in design-doc-proposal.md §4)
Disposition-table execution (its Session 4): `working/edge-modeling/` wholesale post-absorption,
`working/agent-fleet-specs/` + the fleet `.claude` command stamps, `working/qualifier-vocab/`,
`stage4-pass1-derived-edges-design.md`, `tier3-promotion-plan.md`, `edge-vocabulary-gaps.md`,
stale runbooks → `runbooks/archive/`, `reference/model-strategy.md`, CLAUDE.md directory-tree refresh,
`EDGE_MODELING_VALIDATOR_LOG.md`. Plus the gated reply/ledger retro-move (§4.4) once checkpoint waves
finish. **No net-new effort beyond what that proposal already budgets.**

### Phase 4 — gated on the scripts/ archiving session (its own later session per scripts/README.md)
`working/missions/` → `history/missions/` together with the superseded stage4/mission scripts and the
5 stray classify scripts at working/ root; `.claude` worker/watcher/check-fleet commands stamped or
retired in the same sweep. Effort: folds into that session (+~0.25 session for the working/ side).

### Deferred to Matt (decision register)
1. **Skeleton-untrack** — options 1/2/3 in §2a (its own focused session when picked).
2. **`scr`** — scratch-rename vs project-filing (§4).
3. **Design-doc Option A/B/C** — gates Phase 3 (recommendation already on file: Option A).
4. **Commit authorization** for the uncommitted audit session (gates everything).
5. **Alias-and-display trim** — confirm curation is done before the Phase-2 move.
6. **Replies convention** — sign-off on §4's lifecycle before creating `working/replies/`.

### End state
`working/` contains only: todos.md, infobox-merge/, runbooks/ (live), wiki/ (data + staging + buckets),
session-results/ (rotating), audits/ (live + latest baselines), replies/ (rotating), the two live
design docs awaiting consolidation, and nomenclature proposal pending review. Root contains only
CLAUDE.md, README.md, worklog.md, next.md (Matt's), config files. Everything else is in history/ with
its README index extended, or in graph//sources//reference/ untouched.

**Total net-new effort: ~1–1.5 Sonnet sessions (Phases 1+2). Phases 3–4 ride existing planned sessions.**
