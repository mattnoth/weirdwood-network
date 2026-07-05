# Op-semantics sign-off table (S191, D-G checkpoint #2)

**What this is:** the one-line-per-op semantics the new traversal suite pins as tests.
Every line is already the recorded contract (`graph/query/spec/operations.md`) — nothing
here is new behavior; the sign-off is "yes, freeze exactly these." Where the two profiles
deliberately diverge, the suite pins the divergence too (that's the drift alarm's job).

| op | semantics the suite pins |
|---|---|
| `resolve` | 5 statuses (`hit` / `hit-character` / `candidates` / `ambiguous` / `miss`); precedence = event-alias table → character exact → fuzzy; possessives resolve via alias table (no stemming magic); collision phrases return `ambiguous` with no top slug |
| `read` | node report from file; unknown slug → suggestions, no throw; path-dangerous slug (`../`) → None (the new S191 guard) |
| `neighbors` | ALL edge types, both directions, no filter; self-loop counts once outgoing + once incoming; orphan node → 0/0 without error; dangling targets surface fail-soft |
| `chain` | walks CAUSES/TRIGGERS/MOTIVATES only; ENABLES and PRECEDES excluded; full profile = unbounded BFS; cycle terminates, closing edge kept exactly once; self-loop appears once at depth 1 |
| `chain --full` | adds ENABLES preconditions (multi-hop); the ONLY way the wedding→crossing leg is reachable — plain `chain` must exclude it |
| `expand-beats` | beat map uses ROLE_EDGE_TYPES = {AGENT_IN, VICTIM_IN, COMMANDS_IN, WITNESS_IN, WIELDED_IN} — includes WITNESS_IN |
| `participants` | beat-attached roles only (hub-level role edges NOT unioned), PARTICIPANT_ROLE_TYPES = {AGENT_IN, COMMANDS_IN, VICTIM_IN, WIELDED_IN, ATTENDS, LOCATED_AT} — excludes WITNESS_IN; beats-but-no-roles ≠ no-beats (two distinct result shapes); unknown hub → error + suggestions |
| `container` | exact frontmatter-tag set — nothing more (the untagged boot stays out), disjoint bags don't bleed |
| `family` | PARENT_OF/SPOUSE_OF only; defaults up 2 / down 4; cap 96 with `truncated` flag; prominence = degree + 4·quoteCount; deep-spine threads past the horizon at default windows, explicit tight window opts OUT; remarriage keeps both spouse bonds; marry-in spouses are leaves (no ancestor walk); single-parent children fine |
| `path` | direct edges + 2-hop bridges (cap 50); cross-component → clean zero shape; path(a,a) legal, leg counts symmetric |
| `braid` / `fork-hubs` / `join-hubs` | reach-set overlap, NOT direct adjacency; empty results are `[]`, keys always present; self-loop counts toward both degrees. **Precision amendment (S191 suite build):** braiding a node with its own direct descendant is NOT all-empty — `shared_descendants`/`offset_shared_middle` are `[]`, but `shared_ancestors` is the pair's common upstream cone (plain intersection, no ancestor/descendant special-casing). The suite pins the exact split. |
| `health` | dangling endpoints counted (`crells-lost-chronicle` = 1 in the fixture) |
| `search` / `list` / `theme` | corpus-smoke level only (their substrates are built artifacts of the real graph; golden cases already pin scoring parity) |
| profile divergences | pinned as-recorded, not resolved: bounded chain caps (depth 2 / 12 links) vs full unbounded; bounded story-time sort vs full BFS-order print; bounded-only ops absent from full and vice versa per the inventory table |

**Known-gap notes carried, not fixed here:** no `truncated` flag on chain results
(recorded in spec); `mentions` may read a stale index (G13).
