# Session 071 — Stage 4 accuracy push → unpromoted-node pivot (2026-05-25)

**Model:** Opus 4.7 (orchestrator) + Sonnet 4.6 script-builders + Opus reviewers. Long autonomous stretch (Matt AFK in parts, checking in).

## Arc

Started on the Stage-4 enrichment A/B/C decision (continue prompt `stage4-enrichment-decision`).
v1 (3,842 cited deterministic edges) was already landed/committed. The question: enrich with
Events+Dialogue edges typed by Haiku, or not.

**Phase 1 — determinism first (Matt's directive).** Built a deterministic accuracy suite, all $0,
all tested: quote-relevance filter (name/alias-aware), type-contract validator (grew to 9 contracts
with keep/drop/flip/flag dispositions), an improved evidence locator (v2 — prefer windows naming
both entities, + `locate_quality`), a fresh-sample relocate harness, the v1.1 refine script, and
`prompt_version`/`prompt_sha` stamping on every classified row (reject-provenance, Matt's idea).

**Phase 2 — prompt overhaul.** Two independent fresh-eyes Opus reviews of the classifier prompt
converged hard: evidence-grounding (#1), default-to-REJECT asymmetry (#2), consolidate the
co-presence rule, gate 8 more types. Implemented as prompt v4 (GOVERNING PRINCIPLE + GATE 1/2/3,
fixed Rule 4's hint-leaning bug, gated types 5→13).

**Phase 3 — the honesty check.** Smoke5 (fresh seed-4242) hit 72.5% raw; the type-contract filter
*appeared* to lift it to ~80-91%. A **fresh general Opus reviewer flagged that lift as circular**
(the contracts were tuned on smoke5's own errors). The out-of-sample test (smoke6, seed-7777)
confirmed: **~62% raw**, and the filter fired ~0 — overfit confirmed. I had over-claimed; the
fresh-review discipline (Matt's standing mandate) caught it. Root cause of the ceiling = locator
`hint_raw`↔`evidence_quote` decoupling (drives both wrong-emits and false-rejects). Enrichment =
NOT-YET; locator quote-grounding is the lever (spec'd in a continue prompt).

**Phase 4 — the pivot.** Reviewing the v1.1 refinement with Matt, two things converged: (a) several
"type-contract drops" were actually true relationships mis-targeted (RULES→person should retype to
COMMANDS; HEIR_TO→place / COUSIN_OF→`bronze` should retarget to existing title/character nodes),
and (b) the validator was **false-dropping `COMMANDS→faction` edges** (stone-crows, second-sons,
iron-fleet, brotherhood-without-banners) because those factions aren't in `graph/nodes/characters/`.
That exposed the real problem: **a large slice of the wiki Pass-2 entity schema was never promoted.**
Count: `graph/nodes/` = 8,299, but **~7,251 staged `.node.md` are sitting unpromoted** in
`working/wiki/pass2-buckets/*/skeleton/`. The nodes aren't lost — a promotion run (~sessions 40s)
never finished.

## Postmortem — why the node gap wasn't caught before edge work

- The node layer looked "done" in prior worklog summaries; the unpromoted skeletons were in a
  staging tree that no recent session opened. The gap likely fell off the worklog as entries
  archived across ~30 sessions.
- A trivial health check would have surfaced it: `count(graph/nodes/**/*.node.md)` vs
  `count(working/wiki/pass2-buckets/**/skeleton/*.node.md)`. Added to the node-recovery plan.
- Consequence: edge type-contracts + resolution were run against an incomplete node set, producing
  false drops. Good that only v1 (a conservative deterministic core) was committed and the
  enrichment was held — minimal cleanup.

## Key decisions

- **Edges PAUSED.** Fix nodes first; then re-resolve + re-type-check edges (deterministic, $0) —
  NOT a re-extract. v1 frozen; v1.1 candidate built but NOT applied (its faction-drops are wrong
  until nodes land).
- **Validator corrections (architecture-drift fixes, CLAUDE.md #6):** removed the wrong
  ECHOES-char↔char contract (architecture's PARALLELS/ECHOES explicitly allow character mirroring);
  RULES→person retypes to COMMANDS (RULES is location-authority, COMMANDS is person-authority).
- **Aliases are a shared lever** — node-resolution and the quote tokenizer both ride the alias
  index; the `bronze`→Bronze-Yohn / `queen-cersei`→cersei-lannister class is fixable there.
- Folder reorg (wiki/scripts are dumps) queued as its own session.

## Artifacts (all gitignored scratch unless noted)
- Tracked reports: `readiness-review-fresh.md`, `prompt-review-opus-{1,2}.md`,
  `pass1-derived-staging-manifest.md`, `pass1-derived-v1.1-applied.md`, `pass1-derived-v1-refine-proposal.md`.
- Smokes: `_smoke4/5/6-haiku/`, `_fresh-relocate-4242/7777/`. v1.1: `_v1-refine/`.
- Top-level continue prompt: `CONTINUE-node-recovery-and-edges.md`.
- All Stage-4 scripts UNCOMMITTED.
