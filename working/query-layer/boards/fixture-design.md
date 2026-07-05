# Board: the mini-graph fixture — synthesis (S191, D-G checkpoint #1)

**Status: PROPOSAL — awaiting Matt's read before any test is built on it.**
Three-lens Sonnet board (coverage engineer / storyteller / adversarial tester), Fable-synthesized.
Home when built: `graph/query/tests/fixtures/mini/` — test data, NOT graph data (no mutation gate).

## The synthesis in one line

Take the storyteller's saga (**"The Salt Debt" — House Quorwyn**, eel-tax hubris, four
generations, a nickname that ruins two people), lay it over the coverage engineer's
code-grounded skeleton, and quarantine the adversarial traps inside story-shaped corners
(a feud that literally goes in circles, a lost chronicle nobody can find).

## Two corrections the board surfaced (load-bearing)

1. **`MARRIED` is not in the vocabulary** — `family_tree()` reads `SPOUSE_OF` (traverse.py
   L609-618). The step card's "MARRIED spouse bonds" phrasing would have built dead edges.
2. **`event_participants` and `--expand-beats` use DIFFERENT role-edge sets** —
   `PARTICIPANT_ROLE_TYPES` = {AGENT_IN, COMMANDS_IN, VICTIM_IN, WIELDED_IN, ATTENDS,
   LOCATED_AT} vs `ROLE_EDGE_TYPES` = {AGENT_IN, VICTIM_IN, COMMANDS_IN, WITNESS_IN,
   WIELDED_IN}. WITNESS_IN counts in one, ATTENDS/LOCATED_AT in the other. The fixture
   deliberately straddles both sets so a test can pin the divergence instead of papering it.

## The saga (what Matt reads)

House Quorwyn holds an eel-poor spit of coast nobody wanted until eel prices tripled.
**Ormund Quorwyn** — called **"the Eel King"**, a nickname his great-aunt **Myrcella** wore
first as a joke about her stew — borrows against the salt tithe to hire the **Brined
Company** for a war he can't afford. His sister **Alys**'s marriage into House Harrow wins
the army safe passage over the Quiet Mile — the crossing doesn't *cause* what follows, it
merely makes it *possible* (the ENABLES break). The **Battle of Wrackmoor** forks into two
disasters — a beach rout and a burning granary — that converge on the **Salt Debt
Massacre**, where cousin **Dagon** ends up commanding the killing he never wanted and
Ormund's own war kills him. Attainder for the Quorwyns, a quiet truce for the Harrows
(the braid pair). Meanwhile, in a corner nobody else visits, the **eel-market feud** spins
in an actual causal circle (raid → burned nets → market ban → raid), and the ban renews
itself yearly (the self-loop). Maester Crell's chronicle of it all is lost — edges point
at it, but no node exists (the dangling target). Three quote-bearing orphans survive:
the **wedding broth**, **Lord Quorwyn's good boot** (the left one), and the **salted-eel
tithe ledger**.

## Node roster — 35 nodes

| # | slug | type | notes / trap served |
|---|------|------|---------------------|
| 1 | `quor-quorwyn-the-elder` | character | gen 0 — makes Tomm depth-5 so the deep-spine anchor FIRES at default caps |
| 2 | `baelic-quorwyn` | character | gen 1 patriarch; **two SPOUSE_OF bonds** (remarriage dedup trap) |
| 3 | `sella-harrow` | character | gen 1, first wife |
| 4 | `morra-saltpans` | character | gen 1, second wife (the remarriage) |
| 5 | `rodrik-quorwyn` | character | gen 2 |
| 6 | `myrcella-quorwyn` | character | gen 2; alias **"the Eel King"** #1; RESENTS Ormund (nickname theft) |
| 7 | `harwin-quorwyn` | character | gen 3 |
| 8 | `dagon-quorwyn` | character | gen 3; **single recorded parent** (no mother edge); "the Reluctant Sword" |
| 9 | `jonna-harrow` | character | gen 3 marry-in, **zero PARENT_OF anywhere** (spouse-is-a-leaf trap) |
| 10 | `ormund-quorwyn` | character | gen 4; alias **"the Eel King"** #2 (the collision); quotes |
| 11 | `alys-quorwyn` | character | gen 4 |
| 12 | `perrin-harrow` | character | gen 4 marry-in |
| 13 | `tomm-quorwyn` | character | gen 5 posthumous babe, 2 quotes (prominence formula = degree + 4×quoteCount → wins the deep-spine anchor slot) |
| 14 | `maester-crell` | character | WITNESS_IN a beat; author of the lost chronicle |
| 15 | `tam-salter` | character | "the boy who counted the boats"; WITNESS_IN a beat + **PARTICIPATES_IN battle** (a role type in NEITHER walker set — both ops must ignore it) |
| 16 | `the-brined-company` | faction | CONTRACTED_WITH + FIGHTS_IN flavor bridges for `path` |
| 17 | `ormund-borrows-against-the-salt-tithe` | event.incident | chain root |
| 18 | `battle-of-wrackmoor` | event.battle | diamond X |
| 19 | `beach-rout-at-graycliff` | event.battle | diamond A |
| 20 | `burning-of-the-long-granary` | event.incident | diamond B |
| 21 | `salt-debt-massacre` | event.assassination | diamond Y; **join hub** (in-degree 2); marquee hub with 2 beats + hub-level AGENT_IN |
| 22 | `the-granary-floor` | event.beat | SUB_BEAT_OF massacre; Dagon COMMANDS_IN, Tam WITNESS_IN |
| 23 | `the-eel-kings-fall` | event.beat | SUB_BEAT_OF massacre; Ormund VICTIM_IN, Crell WITNESS_IN; alias **"Ormund's death"** (possessive resolve) |
| 24 | `quorwyn-attainder` | event.incident | braid strand A terminus |
| 25 | `harrow-quiet-truce` | event.negotiation | braid strand B terminus |
| 26 | `alys-weds-perrin` | event.wedding | ENABLES source; **hub with a beat but ZERO role edges** (the two empty shapes must stay distinct) |
| 27 | `the-quiet-mile-crossing` | event.incident | 2-hop ENABLES middle link |
| 28 | `the-seating-of-the-harrows` | event.beat | SUB_BEAT_OF the wedding, no roles |
| 29 | `the-drowning-of-the-ledgers` | event.beat | SUB_BEAT_OF **`crells-lost-chronicle`** — a slug with NO node file (dangling target; health() must count it, participants() must fail soft with suggestions) |
| 30 | `raid-on-saltpans-skiffs` | event.incident | feud-spiral node (own component → doubles as the no-path island) |
| 31 | `burning-of-quorwyn-nets` | event.incident | feud spiral |
| 32 | `the-forbidding-of-the-eel-market` | event.incident | feud spiral + **CAUSES self-loop** ("the ban renewed itself yearly") — cycle termination, neighbors double-count, path(a,a), fork/join self-degree |
| 33 | `bowl-of-eel-and-barley` | object.food | orphan, 2 quotes, container-tagged (orphan-inside-a-bag) |
| 34 | `lord-quorwyns-good-boot` | object.artifact | orphan, 2 quotes, deliberately UN-tagged (proves container returns the exact set) |
| 35 | `salted-eel-tithe-ledger` | object.text | orphan, 1 quote, dry bureaucratic comedy |

**Containers:** `wrackmoor` on the war cluster + family (~26 nodes incl. the bowl);
`eel-feud` on the spiral trio (second bag → container op tested on two disjoint tags).

## Edge groups — ~39 edges

- **Family (12):** SPOUSE_OF ×4 (Baelic×2 remarriage, Harwin–Jonna, Alys–Perrin);
  PARENT_OF ×8 (Quor→Baelic→{Rodrik, Myrcella}; Rodrik→{Harwin, Dagon}; Harwin→{Ormund,
  Alys}; Ormund→Tomm). Root choices give every family assertion: root=Baelic default →
  deep-spine threads Tomm (depth 5); root=Tomm, generations_up=2 → up-cap truncation
  (Rodrik excluded); explicit generations_down=2 → no deep-spine bleed (off-by-one
  isolation).
- **Causal diamond + aftermath (7 CAUSES):** borrow→battle; battle→{rout, granary};
  {rout, granary}→massacre; massacre→{attainder, truce}.
- **ENABLES break (2):** wedding→crossing→massacre. `chain battle-of-wrackmoor` excludes
  the wedding leg; `full-chain` includes it — the divergence assertion.
- **Beats (4 SUB_BEAT_OF):** granary-floor→massacre; eel-kings-fall→massacre;
  seating→wedding; drowning-of-the-ledgers→`crells-lost-chronicle` (dangling).
- **Roles (6):** Dagon COMMANDS_IN granary-floor; Ormund VICTIM_IN eel-kings-fall; Tam +
  Crell WITNESS_IN (one beat each); Dagon AGENT_IN massacre (hub-level — participants()
  only unions BEAT-attached roles); Tam PARTICIPATES_IN battle (in neither set).
- **Feud spiral (4 CAUSES):** raid→nets→forbidding→raid + forbidding→forbidding (self-loop).
- **Flavor/negative-space (4):** Myrcella RESENTS Ormund (in-vocab, must appear in
  neighbors but never in chain/family/braid); Ormund CONTRACTED_WITH Brined Company;
  Brined Company FIGHTS_IN battle; Tomm NAMED_AFTER Quor (degree bump for prominence).

## What each op asserts (summary)

resolve: all 5 statuses — hit ("Ormund's death"), hit-character ("Alys Quorwyn"),
candidates (fuzzy "Wrackmoor rout"), ambiguous ("the Eel King"), miss. chain/full-chain:
diamond depths, ENABLES divergence, cycle terminates with the closing edge kept once,
self-loop appears exactly once. participants vs expand-beats: the two role-set outputs
differ on the same hub; beats-but-no-roles ≠ no-beats (distinct shapes, no "message" key
leak). family: remarriage keeps 2 bonds; single-parent child; marry-in spouses are
leaves (no ancestor walk); deep-spine fires; up/down caps at exact boundaries. braid:
{attainder, truce} share exactly the massacre upstream; braid(massacre, attainder) is
all-empty-but-keys-present (reach-overlap, not adjacency); empty results are `[]` never
missing keys. path: cross-component = clean zero shape; path(a,a) invariants. container:
exact sets for both tags, the untagged boot excluded. health: dangling
`crells-lost-chronicle` counted. neighbors: orphans return 0/0 without error; self-loop
counts once outgoing + once incoming; RESENTS visible here and nowhere else.

## Not in the fixture (unit tests instead — no node budget)

- `normalize()` hyphen-variant + straight-vs-curly apostrophe divergence
  (`title_to_slug("Oldtown's…")` ≠ `title_to_slug("Oldtown's…")` — real, silent)
- `resolve()` precedence (event-alias table beats character-index on a colliding key) via
  hand-built lookup dicts
- `find_node_file()` **path-escape freeze**: `../`-laden slugs must not resolve outside
  nodes_dir. The adversarial lens found only `family_tree` guards slug validity;
  `neighbors`/`path`/`chain`/`participants` pass raw strings to `find_node_file`, and
  pathlib WILL walk `..` on `.exists()`. See knob 3.

## Knobs for Matt (recommendations first)

1. **Budget: 35 nodes / ~39 edges vs the card's ~25/~40.** Recommend ACCEPT the overage —
   every node above the storyteller's 22 buys a named trap; the trim list (drop Quor +
   Morra + seating-beat + ledger → 31) costs deep-spine-at-default, remarriage, and the
   two-empty-shapes distinction. The suite is the Track's last artifact; lean the wrong way
   here and the coverage is theater.
2. **Second container tag (`eel-feud`)** — recommend YES (tests exact-set on two disjoint
   bags for free).
3. **`find_node_file` path-escape**: freeze current behavior in a test only, or also land
   the 2-line `_is_valid_slug` guard in `load.py` (code-side, ungated, golden cases
   unaffected)? Recommend GUARD + test. Pairs with the reconciliation file's already-queued
   "fail loudly on duplicate slugs" hardening.
4. **Role-set completion**: leave WIELDED_IN/ATTENDS/LOCATED_AT out (recommended — 5 role
   types straddle the two sets already; full enum coverage adds nodes for no new shape) or
   add a location + weapon for all-6 coverage.
