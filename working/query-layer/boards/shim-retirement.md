# Advisory board — shim retirement timing (design.md §8, fork 4)

> Board deliberation only. Session-C fan-out per `working/query-layer/design.md` §5/§8.
> Fork: WHEN do the compat shims (`scripts/graph-query.py`, `scripts/event_alias_resolver.py`,
> `scripts/build-chat-export.py`) retire — files deleted, tests repointed at
> `graph/query/weirwood_query/` directly?
> **Track**/lowercase **step**/**Tier** (confidence 1–5 only) per the project vocabulary.

## The fork, restated

Step 1 (session A, S190) landed the shims: all three old entry points are now thin wrappers
that import from `graph/query/weirwood_query/` and `graph/query/build/`, print a deprecation
pointer to stderr, and preserve byte-identical old behavior. `weirwood.zsh` already treats
`weirwood query` as the front door and demotes `weirwood graph` / `weirwood resolve` to
"LEGACY alias" in its own help text. `scripts/README.md`'s QUERY section already documents the
shims as shims. The open question the design doc parked to this board: how long do the old
files stay on disk, and what has to happen before they're deleted.

## Ground truth gathered this board (read-only survey)

- **Shim content**: `graph-query.py` is 439 lines, `event_alias_resolver.py` 240 lines,
  `build-chat-export.py` 27 lines. The first two are not pass-throughs in the trivial sense —
  they carry real wrapper logic: path-global monkeypatch threading (`NODES_DIR`,
  `CROSS_REFS_FILE`, `ALIAS_RESOLVER_FILE`, `DEFAULT_EDGES_FILE` are shim-level globals that
  tests mutate directly, so every wrapper function re-reads them at call time and threads them
  into the package call), old-signature preservation for functions whose call shape changed
  underneath (`_leg_direction`, `_edges_to_neighbor_records` drop/ignore now-unused params),
  and the full old argparse surface reimplemented rather than delegated.
- **Tests exercising the shims directly**: 3 files, 89 test functions total, all currently
  green (`python3 -m pytest tests/test_event_alias_resolver.py tests/test_graph_query_edges.py
  tests/test_graph_query_hardening.py` → `89 passed in 0.22s`):
  - `tests/test_event_alias_resolver.py` (41 tests) — `load_script("event_alias_resolver.py")`,
    exercises resolve/build/stats behavior and the monkeypatched-path contract.
  - `tests/test_graph_query_edges.py` (39 tests) — `load_script("graph-query.py")`, exercises
    `--neighbors`/`--path`/`--health`/`--event-participants`/`--causal-chain`/`--container`.
  - `tests/test_graph_query_hardening.py` (9 tests) — same load path, edge-case/robustness
    coverage.
  - All three use `tests/_helpers.py`'s `load_script()`, which loads a file from `scripts/` by
    **path**, not by package import — so retiring the shim means these tests must be rewritten
    to import `weirwood_query`/`build.build_alias_table` as a real package (a `sys.path`/
    `PYTHONPATH` change in the test, not just a filename swap), not just repointed at a new
    filename in the same directory.
- **Static importers**: exactly one, confirmed by grep across the whole repo —
  `scripts/backfill-epithet-aliases.py` does
  `from event_alias_resolver import normalize, name_to_normalized`. (The design doc's claim of
  "exactly one" checks out; the only other hits are in-package comments in
  `graph/query/weirwood_query/{resolve,load}.py` and `graph/query/build/build_alias_table.py`
  citing the old name for provenance, not imports.)
- **Doc/runbook references to the old paths**: `reference/architecture.md` (5 hits — the
  `--causal-chain`/ENABLES explanation, the `aliases` field description, the `--container`
  bag-retrieval note, the slug-convention note, the "Investigation tooling" paragraph),
  `reference/alias-resolver-design.md` (2 hits, historical design record),
  `reference/narrative-arc-glossary.md` (2 hits, worked examples), `reference/roadmap.md`
  (4 hits, status/roadmap prose), `reference/schema-legend.md` (2 hits),
  `working/runbooks/edge-modeling-audit-loop.md` (1 hit, an open-check item). `scripts/README.md`
  already documents both as **COMPAT SHIM** with the new front door named alongside — this file
  is *already updated*, not drifted. `weirwood.zsh` already routes new usage to `weirwood
  query`; the old paths remain only as documented "LEGACY alias" fallthroughs (`weirwood graph`
  → `scripts/graph-query.py`, `weirwood resolve` → `scripts/event_alias_resolver.py`, both by
  deliberate design as user-facing back-compat spellings, not accidental drift).
  `worklog.md` carries 7 hits, all in past-tense session-history entries (S39/S75/S89/S103/S121
  plus the S189/S190 entries describing this very consolidation) — these are correctly frozen
  narrative, not live instructions, and are exempt from any sweep. `working/query-layer/
  design.md` (11 hits) and `graph/query/spec/operations.md` (5 hits) also name the old paths —
  but every one of these is the Track's own planning/spec prose describing the shim
  relationship or citing the old scripts as historical parity ground-truth (e.g. "the live
  Python scripts (`scripts/graph-query.py`, `scripts/event_alias_resolver.py`)" as the baseline
  the golden cases were checked against) — accurate present-tense description of the Track
  itself, not drift to fix.
- **Continue prompts**: one **live** file references the old names in passing
  (`progress/continue-prompts/2026-07-04-query-layer-orchestrated-build.md`, describing the
  absorption work itself — this is accurate present-tense description of the Track, not stale
  drift) plus `progress/continue-prompts/README.md`'s archive-index one-liners (historical, by
  the one-live-continue-prompt convention these don't get rewritten). ~30+ archived
  continue-prompts under `progress/continue-prompts/archive/` mention the old script names in
  passing (worked examples from before the consolidation) — these are frozen history by
  standing convention and are not retirement blockers.
- **`history/`**: dozens of files mention the old names (expected — frozen historical record,
  never edited per CLAUDE.md's history/ convention).
- **Current test suite health**: the shims' own tests are green; nothing today is red or
  blocked on this decision.

## Board

### Advisor 1 — the safety-net keeper
The shims cost approximately nothing to keep running: they're already written, already tested,
already green, and every old invocation (`python3 scripts/graph-query.py --health`, `weirwood
graph <slug>`, the 8 `reference/*.md` worked examples, the ~30 archived continue-prompts, any
muscle-memory command Matt types from habit) keeps working with a visible stderr nudge toward
the new front door. Deleting them now buys nothing except forcing an immediate rewrite of 89
tests and a documentation sweep that has no urgency — the shims are not blocking any other
step in the Track (steps 3–9 all import `weirwood_query` directly or call `weirwood query`,
per the design doc's own step cards). The one real risk of *keeping* them too long is
`backfill-epithet-aliases.py`'s static import silently ossifying into permanent load-bearing
status instead of being repointed — that's a 5-minute fix whenever it's touched next, not a
reason to rush deletion of the other two files. **Verdict: no deletion pressure exists yet;
the cost of keeping is near-zero and asymmetric with the cost of premature removal (broken
`weirwood graph`/`weirwood resolve` muscle memory, 89 tests needing simultaneous rewrite).**

### Advisor 2 — the clean-cut advocate
Two live surfaces answering to the same questions is exactly the failure mode this whole Track
exists to kill (G11/G12: the root cause was never "missing features," it was "nothing pins the
implementations together"). The shims are not inert forwarding stubs — `graph-query.py` at 439
lines and `event_alias_resolver.py` at 240 lines carry real logic: monkeypatch-threading
wrappers, old-signature adapters, a fully reimplemented argparse surface. That is surface area
that can itself drift from the engine underneath if someone edits `weirwood_query` and forgets
the shim's wrapper needs a matching update — the exact bug class the Track was created to stop.
Every week the shims live past their no-regression purpose is a week two things can rot instead
of one. The counter-risk (Advisor 1's point) is real but time-bounded, not permanent: once the
things that justify the shims' *existence* (test coverage, the one static importer, doc
examples) are migrated, the shim becomes pure liability with no offsetting benefit.
**Verdict: retire deliberately, but retirement is gated on migration completing — not on a
calendar date divorced from that work, and not held open indefinitely either.**

### Advisor 3 — the test engineer
What migration actually requires, concretely: rewrite `tests/test_event_alias_resolver.py`
(41 tests), `tests/test_graph_query_edges.py` (39 tests), `tests/test_graph_query_hardening.py`
(9 tests) to import `weirwood_query`/`build.build_alias_table` as real packages
(`sys.path.insert` on `graph/query/` or a `PYTHONPATH` fixture) instead of
`_helpers.load_script()`-ing a file in `scripts/`. This is not a rename — the monkeypatch
contract changes shape: today tests mutate shim-level globals like `gq.NODES_DIR = tmp_path`
and rely on the shim's wrapper functions re-reading that global at call time; a direct-import
test would instead need to call `weirwood_query.traverse.neighbors(slug, edges,
nodes_dir=tmp_path)` with the path passed explicitly, since the package functions already take
`nodes_dir`/`edges_path` as real parameters (per `graph-query.py`'s own docstring: "each
wrapper reads the shim's global at CALL time and threads it into the package function as an
explicit parameter"). That's a genuine, if mechanical, rewrite — not a find-and-replace. The
design doc's own D-G already named the natural pairing: **the deferred FINAL session** builds
`graph/query/tests/` from scratch as an idiomatic pytest suite (fixtures, parametrize, a
synthetic mini-graph) with Matt co-designing the fixture content. Migrating these 89 tests in
that same final session means writing the monkeypatch→explicit-parameter translation exactly
once, in the same sitting where the mini-graph fixtures and golden-case runners are being
built anyway, instead of doing throwaway shim-compatible test work now and real test work
later. Doing it now, before the final session, would mean touching these three files twice.
**Verdict: fold the test migration into the deferred final pytest session — that is the
natural, lowest-total-effort pairing, not a delay tactic.**

### Advisor 4 — the archaeologist
Roughly a dozen live (non-archived, non-`history/`) files reference the old paths by name:
`reference/architecture.md` (5x), `reference/alias-resolver-design.md` (2x),
`reference/narrative-arc-glossary.md` (2x), `reference/roadmap.md` (4x),
`reference/schema-legend.md` (2x), `working/runbooks/edge-modeling-audit-loop.md` (1x) — plus
`scripts/README.md` and `weirwood.zsh`, which are **already correctly updated** to describe the
shim relationship (not drift), and `working/query-layer/design.md` (11x) + `graph/query/spec/
operations.md` (5x), which are the Track's own planning/spec docs citing the old scripts as
historical parity ground-truth — also not drift, just provenance. `worklog.md` (7x) is entirely
past-tense session history, correctly frozen. The `reference/` hits are mixed in character:
some are worked CLI examples ("run `python3 scripts/event_alias_resolver.py --lookup ...`")
that would need a literal command swap; others are conceptual explanations ("the walk tool
`graph-query.py --causal-chain` follows only {CAUSES, TRIGGERS, MOTIVATES}") where the *tool
name* is almost incidental to the point being made. None of these are urgent to fix — the shim
guarantees the commands still work verbatim as written, so today's `reference/*.md` is not
lying, just not using the newest preferred spelling. But if the shim files are deleted while
these examples still say `scripts/graph-query.py`, every one of those becomes a broken command
a future session or Matt could copy-paste and hit a `FileNotFoundError`. History (`history/`,
`progress/continue-prompts/archive/`, 32 files by count) is correctly exempt by standing
convention (frozen record, never edited) and should never be swept regardless of shim status.
**Verdict: the ~6 live reference/runbook files are the one class of doc genuinely at risk from
deletion — they need a mechanical find-and-replace pass (not urgent, but a real pre-condition),
separate from and much cheaper than the test migration.**

## Synthesis

**Decision: retire in two tiers, both gated on concrete conditions — not a calendar date.**

**Tier A — cheap, do it opportunistically, doesn't block deletion by itself:**
Sweep the ~6 live `reference/*.md` + `working/runbooks/*.md` files (`architecture.md`,
`alias-resolver-design.md`, `narrative-arc-glossary.md`, `roadmap.md`, `schema-legend.md`,
`edge-modeling-audit-loop.md`) to prefer `weirwood query <args>` / `graph/query/weirwood_query`
in new prose, keeping old-command mentions only where historically accurate (e.g. "the S120
board found..."). `working/query-layer/design.md` and `graph/query/spec/operations.md` do NOT
need this sweep — their old-path mentions are the Track's own accurate provenance/parity
citations, not stale drift. This is a documentation-consistency task any Sonnet subagent can do
in under an hour; it can happen any time (docs-only, no graph-mutation gate applies) and does
not need to happen before the files are deleted — it just should happen before or in the same
session as deletion, so no live doc dead-ends into a `FileNotFoundError`.

**Tier B — the actual deletion, gated on three conditions all being true:**
1. **The deferred final pytest session (D-G) has run and landed** `graph/query/tests/` with
   equivalent (or better) coverage of what `test_event_alias_resolver.py` /
   `test_graph_query_edges.py` / `test_graph_query_hardening.py` exercise today — per Advisor 3,
   this is the natural single sitting to do the monkeypatch→explicit-parameter rewrite, since
   it's happening in that session anyway for the new fixture suite.
2. **`scripts/backfill-epithet-aliases.py`'s import is repointed** from
   `from event_alias_resolver import normalize, name_to_normalized` to
   `from weirwood_query.normalize import normalize, name_to_normalized` (a one-line, zero-risk
   change — but it must happen, since it's the one real static dependency left standing).
3. **Tier A's doc sweep has run** (or runs in the same pass as deletion) so no `reference/*.md`
   worked example dead-ends.

When all three are true, delete `scripts/graph-query.py`, `scripts/event_alias_resolver.py`,
`scripts/build-chat-export.py`; remove the `weirwood graph`/`weirwood resolve` legacy aliases
from `weirwood.zsh` (or leave them pointed at `weirwood query` under the hood as permanent
short aliases — a naming call for whoever runs that session, not a retirement blocker either
way); update `scripts/README.md`'s QUERY section to drop the "COMPAT SHIM" language.

**Do NOT set a wall-clock/telemetry-based trigger** (e.g. "N weeks of clean runs") — this
project has no shim-invocation telemetry to measure against (the per-turn Netlify Blobs logs
track the *chat* surface, not local script invocations), so a time-based gate would be
theater, not a real signal. The three conditions above are the real signal: they're the actual
work that makes deletion safe, and none of them are currently scheduled to happen "later for no
reason" — they're already on the Track's own roadmap (final pytest session is D-G/step 2;
the import fix and doc sweep are both sub-hour tasks that can ride along with it).

### Rationale (5 lines)
1. The shims cost ~0 to keep and are not blocking any other step — no deletion pressure exists
   independent of the migration work itself (Advisor 1).
2. But they carry real wrapper logic (not pure forwarding) and are a second surface that can
   itself drift from the engine — retirement should happen, just gated on real work, not held
   open forever (Advisor 2).
3. Test migration is a genuine rewrite (monkeypatch globals → explicit params), and the
   deferred final pytest session is the one sitting that's already doing equivalent fixture/
   semantics work — pairing them avoids touching the same three test files twice (Advisor 3).
4. A small, cheap doc sweep (~6 `reference/*.md` + `working/runbooks/*.md` files) and one static-import repoint
   (`backfill-epithet-aliases.py`) are the only other real pre-conditions; both are sub-hour
   and can ride along with the final session or happen opportunistically beforehand (Advisor 4).
5. Gate on conditions (tests migrated + import repointed + docs swept), not on a calendar date
   or invocation-telemetry threshold that doesn't exist for local scripts — the conditions are
   already scheduled work, not new busywork invented for this fork.

### Dissents
None on the core two-tier structure — all four advisors converge on "gate deletion on the
final pytest session, not a date." Advisor 1 would go further and explicitly argue against
*ever* deleting `weirwood graph`/`weirwood resolve` as zsh aliases even after the underlying
`.py` files are gone (keep them as one-line pass-throughs to `weirwood query`/`weirwood
resolve` — muscle memory is cheap to honor forever), where Advisors 2 and 4 are indifferent
(fine to drop the aliases once the files are gone, since `weirwood query`/`weirwood resolve`
already exist as the preferred spelling and the deprecation stderr has had a full session cycle
to be seen). This is a low-stakes naming call, explicitly left to whoever runs the deletion
session.

---

## Appendix — session log
- **2026-07-04 (S190, session-C board fan-out):** board convened per design.md §8; surveyed
  shim content (439/240/27 lines), 89 shim-dependent tests across 3 files (all green), the one
  confirmed static importer (`backfill-epithet-aliases.py`), and ~12 live doc references
  (`reference/*.md` ×5 files, `scripts/README.md` + `weirwood.zsh` already correct). Decided:
  two-tier retirement — cheap doc sweep opportunistic/anytime; actual file deletion gated on
  (1) the deferred final pytest session migrating the 89 tests, (2) the one static import
  repointed, (3) the doc sweep done. No wall-clock or telemetry gate (no signal exists for
  local script invocations). No dissent on structure; one low-stakes naming dissent on whether
  `weirwood graph`/`weirwood resolve` zsh aliases should outlive the underlying files.
