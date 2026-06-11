# Continue — Phase 2: Light Mode 3 grounded-agent dip

> **Recommended model:** Opus 4.7 — judgment-heavy. The work is interpreting agent failure modes against the graph and deciding what to fix next; not deterministic.
>
> **Prerequisites:** Phase 1 overnight work (S89) must be reviewed first:
> - `working/session-results/2026-06-10-overnight-event-participants.md` (NEW TODO #7 — `--event-participants` primitive)
> - `working/session-results/2026-06-10-overnight-alias-resolver.md` (NEW TODO #8 — event-alias-resolver)
> - `working/session-results/2026-06-10-overnight-rename-dryrun.md` (NEW TODO #10 — joffrey-orders-execution rename DRY-RUN ONLY)
>
> Matt: review those 3 files first. Apply #10 rename if dry-run looks clean (the file has the literal `--apply` command). Then fire this continue prompt.

## Context — where we are

S88 scoped a 4-mode validation track for the post-Plate-5 graph (edges.jsonl=4,757, events/=583). S89 executed Mode 1 (capability probes) — 8 probes complete, 5 NEW TODOs surfaced, 4 NEW hub-review items, capability boundaries mapped. Phase 1 (overnight S89) built the two missing query primitives (#7, #8) and prepped #10. This continue prompt is **Phase 2** — the light Mode 3 grounded-agent dip that S89's writeup recommended.

Read first:
- `working/session-results/2026-06-09-graph-validation.md` — the full S89 probe results + Mode 1 → Mode 3 readiness call. This is the design context for what Phase 2 is for.
- The 3 overnight result files (above) — what the new primitives can and can't do.

## What Phase 2 is

The minimum-viable test: hand a Claude agent the graph as a tool and ask it 5-10 grounded ASOIAF questions. Observe what it does. Use failures to prioritize what to fix next (Track B beat-coverage vs NEW TODO #9 historical structural-backfill vs query-layer gaps the probes didn't catch).

The point is NOT to prove the agent works. The point is to surface unknown unknowns about how the agent uses the graph, before sinking $25-75 into Track B or NEW TODO #9 work.

## Approach

### Setup

The agent gets access to `scripts/graph-query.py` as its primary tool. Available modes (after Phase 1):
- `--neighbors <slug>` — direct edges
- `--path <slug-a> <slug-b>` — 2-hop bridge search
- `--health` — graph-wide stats
- `--edges --type <T> --source <S> --target <T>` — filtered edge query
- `--event-participants <hub>` — NEW from #7: beat-union for reified events
- Event-alias-resolver (#8) — wherever the script landed; agent uses it to map natural-phrase questions to canonical slugs

The agent should ALSO know what the graph can't do (per S89 findings) so it can route around dark zones:
- Historical events are sparse (most have 0 edges; some have dyadic acts but unattached — NEW TODO #9 not yet built)
- WIELDED_IN ≈ 10 across whole graph (weapon participation dark)
- ATTENDS = 2 (presence dark)
- Action-named slugs may still exist if #10 rename hasn't been applied or audit found more (`orders/claims/demands/calls-for/grants/swears/denies`)

### Question set — 5-10 grounded queries

Pick a spread covering: chapter-resident events (should work), historical events (should fail OR work via the new alias resolver), strategic/architect chains (should fail per S89), dyadic relationships (should work), weapon/presence queries (should fail), cross-POV perception (untested in S89).

Suggested starter set (refine based on what feels most diagnostic):

1. **"Who killed Robb Stark?"** — capability test, chapter-resident, should work via `--event-participants robb-is-killed` after alias-resolution of "Robb Stark's death" or similar.
2. **"Who ordered the Red Wedding?"** — beat-union; should surface Walder Frey + Roose Bolton. Tywin will be absent — note whether agent flags the omission.
3. **"Who crowned Lyanna Stark queen of love and beauty?"** — historical, should work via the one Pass-1-direct edge (Rhaegar). Test whether agent finds it or fails to query a hub-attached version.
4. **"What weapon was used to kill Robb Stark?"** — designed-but-dark vocab test. Should return nothing. Watch how the agent handles dead-end.
5. **"Who fought at the Tourney at Harrenhal?"** — historical dark zone. Should fail entirely unless agent works around via individual-person dyad searches.
6. **"What's the connection between Tywin Lannister and Gregor Clegane?"** — should return direct edges + 2-hop bridges; agent's job is to summarize.
7. **"Was Bran Stark pushed or did he fall?"** — interpretive question; tests whether agent can extract from edge evidence quotes.
8. **"Who attended Ned Stark's execution?"** — ATTENDS dark + alias resolution test. Should fail; watch the routing.

### What to observe per query

For each query, log:
- Initial query strategy (which primitive did the agent reach for first?)
- Whether alias-resolver fired correctly (if applicable)
- Whether agent recognized when to give up vs hallucinated
- Which graph gaps surfaced
- Did the agent suggest a fix to its own failure (good signal)

### Output

Write `working/session-results/2026-06-11-mode3-dip-results.md` with:
1. Per-query results table (query | tool calls used | answer | correct? | failure mode)
2. Failure-mode taxonomy: which classes of failure dominated? Slug-discoverability, dark-vocab, dark-historical, prose-only, agent-protocol-error?
3. **Routing call:** based on failure modes, recommend the next track. Options to weigh: (a) NEW TODO #9 structural-backfill (if historical-dark dominated), (b) Track B beat-coverage (if hub-sparse dominated), (c) more query-layer tooling (if agent's tool-use was the gap), (d) the agent prompt itself needs sharpening before any more graph work.
4. Update worklog at end-of-session.

## Hard rules carried in

- **DO NOT touch `edges.jsonl`** unless explicitly approved (Mode 3 is a test, not a fix).
- **DO NOT run LLM enrichment passes** (gated on precision per S75 standing rule).
- **DO NOT auto-/endsession** (requires explicit Matt permission).
- **DO read S89 writeup before firing the agent** — context matters; if the agent doesn't know the historical dark zone exists, its failures will be uninterpretable.
- **DO NOT exceed 10 queries.** The point is signal, not coverage.

## End-of-session checklist

- Write `working/session-results/2026-06-11-mode3-dip-results.md` (sections per "Output" above)
- Update `working/todos.md` — close NEW TODOs that the dip resolved; add any new ones it surfaced; promote the recommended next-track recommendation to a `→ continue:` entry
- Update `worklog.md` S90 entry
- /endsession requires explicit permission per standing rule
