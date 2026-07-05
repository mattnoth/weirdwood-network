# The Salt Debt — a mini-graph test fixture

**This is synthetic test data. No relation to the real graph.** House Quorwyn,
the Brined Company, Wrackmoor, and everyone's eel-based nicknames are
invented for the Weirwood query engine's test suite (query-layer Track,
S191, D-G checkpoint #1). Nothing here should ever be cited as ASOIAF canon,
and nothing here is loaded by `graph/nodes/` or `graph/edges/` — this
directory is quarantined under `graph/query/tests/fixtures/mini/`.

## The pitch

House Quorwyn holds an eel-poor spit of coast nobody wanted until eel prices
tripled. Ormund Quorwyn — called "the Eel King," a nickname his great-aunt
Myrcella wore first as a joke about her own stew — borrows against the salt
tithe to hire the Brined Company for a war he can't afford. His sister
Alys's marriage into House Harrow wins the army safe passage over the Quiet
Mile — the crossing doesn't *cause* what follows, it merely makes it
*possible*. The Battle of Wrackmoor forks into two disasters — a beach rout
and a burning granary — that converge on the Salt Debt Massacre, where
cousin Dagon ends up commanding the killing he never wanted and Ormund's
own war kills him. Attainder for the Quorwyns, a quiet truce for the
Harrows. Meanwhile, in a corner nobody else visits, the eel-market feud
spins in an actual causal circle (raid, burned nets, market ban, raid
again), and the ban renews itself yearly. Maester Crell's chronicle of it
all is lost — edges point at it, but no node exists. Three quote-bearing
orphans survive: the wedding broth, Lord Quorwyn's good boot (the left
one), and the salted-eel tithe ledger.

## Node map (35 nodes)

| slug | type | role in the saga |
|---|---|---|
| `quor-quorwyn-the-elder` | character.human | gen 0 founder |
| `baelic-quorwyn` | character.human | gen 1 patriarch, twice-wed |
| `sella-harrow` | character.human | gen 1, first wife |
| `morra-saltpans` | character.human | gen 1, second wife (remarriage) |
| `rodrik-quorwyn` | character.human | gen 2 |
| `myrcella-quorwyn` | character.human | gen 2, "the Eel King" #1, RESENTS Ormund |
| `harwin-quorwyn` | character.human | gen 3 |
| `dagon-quorwyn` | character.human | gen 3, "the Reluctant Sword," single recorded parent |
| `jonna-harrow` | character.human | gen 3 marry-in, no parentage recorded |
| `ormund-quorwyn` | character.human | gen 4, "the Eel King" #2, quotes |
| `alys-quorwyn` | character.human | gen 4 |
| `perrin-harrow` | character.human | gen 4 marry-in |
| `tomm-quorwyn` | character.human | gen 5, posthumous, 2 quotes, deep-spine anchor |
| `maester-crell` | character.human | witness, lost-chronicle author |
| `tam-salter` | character.human | witness + PARTICIPATES_IN (neither role set) |
| `the-brined-company` | organization.faction | hired sellswords |
| `ormund-borrows-against-the-salt-tithe` | event.incident | chain root |
| `battle-of-wrackmoor` | event.battle | diamond fork point |
| `beach-rout-at-graycliff` | event.battle | diamond leg A |
| `burning-of-the-long-granary` | event.incident | diamond leg B |
| `salt-debt-massacre` | event.assassination | diamond join hub, 2 beats |
| `the-granary-floor` | event.beat | sub-beat of massacre |
| `the-eel-kings-fall` | event.beat | sub-beat of massacre, alias "Ormund's death" |
| `quorwyn-attainder` | event.incident | braid strand A terminus |
| `harrow-quiet-truce` | event.negotiation | braid strand B terminus |
| `alys-weds-perrin` | event.wedding | ENABLES source, beat but zero roles |
| `the-quiet-mile-crossing` | event.incident | ENABLES middle link |
| `the-seating-of-the-harrows` | event.beat | sub-beat of wedding, no roles |
| `the-drowning-of-the-ledgers` | event.beat | sub-beat of the dangling chronicle |
| `raid-on-saltpans-skiffs` | event.incident | feud spiral, own component |
| `burning-of-quorwyn-nets` | event.incident | feud spiral |
| `the-forbidding-of-the-eel-market` | event.incident | feud spiral + CAUSES self-loop |
| `bowl-of-eel-and-barley` | object.food | orphan, 2 quotes, container-tagged |
| `lord-quorwyns-good-boot` | object.artifact | orphan, 2 quotes, deliberately UN-tagged |
| `salted-eel-tithe-ledger` | object.text | orphan, 1 quote |

35 node files, 39 edge rows (`edges.jsonl`).

## How the traps are wired

- **Remarriage dedup** — `baelic-quorwyn` carries two `SPOUSE_OF` bonds
  (Sella, then Morra); `family_tree()` must keep both.
- **Single-parent child** — `dagon-quorwyn` has one `PARENT_OF` edge in
  (from Rodrik), no mother recorded.
- **Marry-in leaf** — `jonna-harrow` has zero outgoing/incoming `PARENT_OF`
  edges; she's a spouse-only leaf in the family tree, no ancestor walk.
- **Deep-spine anchor** — `tomm-quorwyn` sits at generation 5 from
  `quor-quorwyn-the-elder`; his 2 quotes + degree push his prominence score
  (`degree + 4*quoteCount`) high enough to win the deep-spine anchor slot at
  default caps when rooted at `baelic-quorwyn`.
- **Up/down cap boundaries** — rooting at `tomm-quorwyn` with
  `generations_up=2` truncates at Harwin/Jonna and excludes Rodrik
  (one generation further up).
- **Causal diamond** — `battle-of-wrackmoor` forks to `beach-rout-at-graycliff`
  and `burning-of-the-long-granary`, both of which `CAUSES` into
  `salt-debt-massacre` — a single join, not a doubled edge.
- **ENABLES break** — `alys-weds-perrin` → `the-quiet-mile-crossing` →
  `salt-debt-massacre` is `ENABLES`, not `CAUSES`. This leg attaches to
  `salt-debt-massacre`, not `battle-of-wrackmoor` — the causal-vs-full-chain
  divergence must be asserted from the massacre, not the battle.
- **Self-loop** — `the-forbidding-of-the-eel-market` `CAUSES` itself
  ("the ban renews itself yearly"). `neighbors()` counts it once outgoing,
  once incoming; `path(a, a)` must not crash.
- **Feud spiral / cross-component island** — `raid-on-saltpans-skiffs` →
  `burning-of-quorwyn-nets` → `the-forbidding-of-the-eel-market` →
  (back to) `raid-on-saltpans-skiffs` is its own connected component,
  disjoint from the war cluster. `path()` between any feud-spiral node and
  any war-cluster node must return a clean zero shape (no direct edges, no
  bridges).
- **Dangling target** — `the-drowning-of-the-ledgers` has a `SUB_BEAT_OF`
  edge pointing at `crells-lost-chronicle`, which has **no node file**.
  `health()` must count exactly this one orphan endpoint; `event_participants()`
  on the dangling slug must fail soft with suggestions, not crash.
- **Two empty shapes stay distinct** — `alys-weds-perrin` has a beat
  (`the-seating-of-the-harrows`) but zero role edges anywhere under it;
  a hub with beats-but-no-participants must not collapse into the
  "no beats at all" message shape that a true beat-less hub would return.
- **Role-set divergence** — `event_participants()` reads
  `PARTICIPANT_ROLE_TYPES` (includes `ATTENDS`/`LOCATED_AT`, excludes
  `WITNESS_IN`); `causal_chain(..., expand_beats=True)` reads
  `ROLE_EDGE_TYPES` (includes `WITNESS_IN`, excludes `ATTENDS`/`LOCATED_AT`).
  Maester Crell and Tam Salter's `WITNESS_IN` edges on the massacre's two
  beats show up in `expand_beats` output but are invisible to
  `event_participants()`'s participant count — the same hub, two different
  answers, by design. `tam-salter`'s `PARTICIPATES_IN` edge on
  `battle-of-wrackmoor` sits in **neither** role-type set; both walkers must
  silently ignore it rather than error.
- **Hub-level vs beat-level role** — `dagon-quorwyn` carries `AGENT_IN`
  directly on `salt-debt-massacre` (the hub), separate from his
  `COMMANDS_IN` on the `the-granary-floor` beat. `event_participants()` only
  unions **beat-attached** roles, so the hub-level `AGENT_IN` must not
  appear in its participant list.
- **Ambiguous alias collision** — "the Eel King" normalizes to `eel king`
  and sits in `alias-lookup.json`'s `ambiguous_collisions` block, mapping to
  both `myrcella-quorwyn` (coined it first) and `ormund-quorwyn` (wore it in
  earnest). `resolve()` must return status `ambiguous`, not silently pick one.
- **Possessive resolve** — "Ormund's death" is a direct hit in
  `alias_to_canonical` → `the-eel-kings-fall`.
- **Container as exact set, not vibes** — `wrackmoor` tags the war cluster +
  the full family + the wedding broth; `eel-feud` tags the spiral trio;
  `lord-quorwyns-good-boot` is deliberately untagged and must never appear
  in either bag. The two tags are disjoint bags on the same node pool.
- **Flavor/negative-space edge** — `myrcella-quorwyn` `RESENTS`
  `ormund-quorwyn` is in-vocabulary but must appear only in `neighbors()`;
  it is not a `PARENT_OF`/`SPOUSE_OF`/`CAUSES`/`ENABLES` type, so `family`,
  `chain`, and `braid` must never surface it.

## Files

- `nodes/<category>/<slug>.node.md` — 35 node files, categories mirroring
  the real graph's `graph/nodes/` type-dir layout (`characters/`, `events/`,
  `factions/`, `foods/`, `artifacts/`, `texts/`).
- `edges.jsonl` — 39 edge rows, one JSON object per line.
- `alias-lookup.json` — the event-alias-lookup shape (`alias_to_canonical`
  + `ambiguous_collisions`) that `weirwood_query.load.load_alias_lookup` /
  `load_alias_collisions` read.
- `all-node-index.json` — the all-node-alias-lookup shape (`phrase_to_nodes`)
  that `weirwood_query.load.load_all_node_index` reads, feeding `resolve()`'s
  character-name fallback.
