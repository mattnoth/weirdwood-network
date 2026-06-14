# Mode 3 Grounded-Agent Dip — Results (2026-06-14)

Fresh evaluator acting as a consumer agent answering ASOIAF questions using the graph
as its primary tool, then grading the graph's answers against wiki/chapter ground truth.

Graph state at test time (`--health`): 8,518 node files, 21,770 edges, 123 edge types.
Dense: SWORN_TO (4148), HOLDS_TITLE (3401), CULTURE_OF (3252), PARENT_OF (1686),
DIED_AT (915), BORN_AT (835). Sparse/dark: SUB_BEAT_OF (55), WIELDED_IN (~10),
ATTENDS (~2, not even in top distribution), causal/TRIGGERS edges (absent).

---

## 1. Per-query results

| # | Query | Tool calls (exact) | Graph's answer | Ground truth (file) | Grade | Failure mode |
|---|-------|--------------------|----------------|---------------------|-------|--------------|
| 1 | Who killed Robb Stark? | `event_alias_resolver.py --lookup "Robb Stark's death"` (MISS) → fs-search → `graph-query.py --neighbors robb-is-killed` | Roose Bolton (AGENT_IN, "thrusts his longsword through Robb's heart"); Walder Frey (COMMANDS_IN, orchestrates); Robb VICTIM_IN | Roose Bolton kills Robb; Walder Frey orchestrates (`sources/wiki/_raw/Red_Wedding.json`; `sources/chapters/asos/asos-catelyn-07.md`) | **correct** | slug-discoverability (resolver missed; data perfect) |
| 2 | Who ordered the Red Wedding? | `event_alias_resolver.py --lookup "the Red Wedding"` (HIT red-wedding) → `graph-query.py --event-participants red-wedding` | Walder Frey (COMMANDS_IN ×6, "orchestrates massacre"); Roose Bolton (COMMANDS_IN). Tywin ABSENT. | Walder Frey + Roose Bolton on-page; Tywin Lannister off-page architect (Red_Wedding.json) | **partial** | dark-historical / off-page (on-page orderers present; Tywin's off-page causation has no edge) |
| 3 | Who crowned Lyanna QoLB? | `--lookup` (MISS) → fs-search → `graph-query.py --neighbors lyanna-stark` | `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY <- rhaegar-targaryen` (1 edge) | Rhaegar crowned Lyanna at Tourney at Harrenhal (`sources/wiki/_raw/Tourney_at_Harrenhal.json`) | **correct** | slug-discoverability (resolver missed; the lone Pass-1 edge IS in the graph and a node query finds it) |
| 4 | What weapon killed Robb Stark? | `graph-query.py --neighbors robb-is-killed` (grep WIELDED) | No WIELDED_IN edge. Weapon "longsword" appears only inside the AGENT_IN quote text. | Roose stabs Robb with a longsword (asos-catelyn-07.md) | **failed** | dark-vocab + prose-only (WIELDED_IN not minted for this hub; fact survives only as quote prose) |
| 5 | Who fought at the Tourney at Harrenhal? | fs-search → `graph-query.py --neighbors tourney-at-harrenhal` | 0 outgoing, 0 incoming — isolated node | Rhaegar, Barristan, Brandon/Benjen Stark, the Knight of the Laughing Tree, etc. (Tourney_at_Harrenhal.json) | **failed** | dark-historical (pre-narrative event node with zero edges) |
| 6 | Connection: Tywin & Gregor? | `graph-query.py --path tywin-lannister gregor-clegane` | 4 direct (COMMANDS, SERVES, SWORN_TO, PROTECTS) + 9 2-hop bridges (via Tyrion, Cersei, Oberyn, Sandor, house-lannister, vargo-hoat, westermen, …) | Gregor is Tywin's bannerman/enforcer (Gregor_Clegane.json) | **correct** | — (best-in-class) |
| 7 | Who attended Ned's execution? | `--lookup "Ned Stark's execution"` (MISS) → fs-search → `graph-query.py --event-participants execution-of-eddard-stark` (0, hub has direct edges not beats) → `--neighbors execution-of-eddard-stark` | Ilyn Payne (AGENT_IN), Joffrey (COMMANDS_IN), Eddard (VICTIM_IN), **Ice (WIELDED_IN)**, LOCATED_AT great-sept-of-baelor. No ATTENDS for the watching crowd (Sansa, Arya, Cersei). | Ilyn Payne beheads Ned with Ice at the Great Sept; Sansa/Arya/Cersei/Joffrey present (`sources/wiki/_raw/Eddard_Stark.json`) | **partial** | slug-discoverability (resolver missed) + ATTENDS dark (perpetrators captured; audience not) |
| 8 | Jon Snow: relation to Ned / sworn to / born where? | `graph-query.py --neighbors jon-snow`; `--path jon-snow eddard-stark` | PARENT_OF <- eddard-stark (Ned as father); SWORN_TO nights-watch; SIBLING_OF Stark children; very dense relationship layer (RESPECTS 20, COMMANDS 16, etc.). BORN_AT absent. | Ned raised Jon as bastard son; Jon sworn to Night's Watch; birthplace canonically the Tower of Joy (left unasserted) (Jon_Snow.json) | **correct** | — (BORN_AT omission is arguably correct restraint, not a defect) |
| 9 | What set the Trident *incident* (roadside) in motion? | `--lookup "incident at the Trident"` (MISS); `--neighbors incident-at-the-trident` (0/0); fs-search shows mycah.node.md exists but no incident hub | Nothing. `incident-at-the-trident` node does not exist yet. | Joffrey attacks Mycah; Arya/Nymeria defend; Cersei demands Lady's death; Sandor kills Mycah (`sources/chapters/agot/agot-eddard-04.md` / `agot-sansa-01.md`) | **failed** | (EXPECTED baseline) hub pre-mint — scheduled for next session's narrative-arc work |
| 10 | Consequences of the Battle of the Trident? | `--lookup` (HIT battle-of-the-trident) → `graph-query.py --neighbors battle-of-the-trident` | Only PART_OF roberts-rebellion (in + out). No consequences. | Rhaegar dies, rebels win decisively, leads to Sack of KL & Robert's accession (`sources/wiki/_raw/Battle_of_the_Trident.json`) | **failed** | dark-vocab causal (no TRIGGERS/CAUSES/LEADS_TO edges radiate from historical hubs) |

**Tally: 4 correct, 2 partial, 4 failed.**

---

## 2. Failure-mode taxonomy

Counting every distinct failure contribution (a query can carry more than one):

| Failure mode | Count | Queries |
|--------------|-------|---------|
| slug-discoverability (data exists, alias resolver missed) | 4 | Q1, Q3, Q7, (and would-be Q9-mycah) |
| dark-historical (pre-narrative node has ~0 edges) | 3 | Q2 (Tywin), Q5, Q9 |
| dark-vocab (the answering edge type is graph-wide empty) | 3 | Q4 (WIELDED_IN), Q7 (ATTENDS), Q10 (causal) |
| prose-only (fact lives in quote text, never an edge) | 1 | Q4 |
| hub pre-mint (scheduled, not yet built) | 1 | Q9 |

**Dominant axis:** `slug-discoverability` is the single most frequent and the most
*correctable* failure — in 3 of 4 cases (Q1, Q3, Q7) the graph held the perfect answer
and the only thing that failed was the natural-phrase → slug step. The alias resolver
covers a curated set and misses obvious phrasings ("Robb Stark's death", "Ned Stark's
execution", "Lyanna crowned queen of love and beauty") even though `robb-is-killed`,
`execution-of-eddard-stark`, and `lyanna-stark` are all live, well-populated nodes.

Tied behind it: `dark-historical` and `dark-vocab`, both structural data gaps.

---

## 3. What works well

- **Dyadic relationship / `--path` queries are excellent.** Q6 (Tywin↔Gregor) returned
  4 typed direct edges + 9 disambiguated 2-hop bridges with refs and quotes. This is the
  graph's strongest shape and would satisfy a consumer agent immediately.
- **Post-infobox-merge kinship/allegiance/title/culture is dense and reliable.** Q8 (Jon
  Snow) answered relation-to-Ned (PARENT_OF), allegiance (SWORN_TO nights-watch), and the
  full sibling/relationship web without effort. The merged structural layer delivers.
- **Beat-reified chapter-resident events are fully answerable** once you hit the right
  hub. Q2 (`--event-participants red-wedding`) unioned 8 beats → 29 role edges → 13
  participants with chapter-cited quotes. Q1 (robb-is-killed) and Q7
  (execution-of-eddard-stark) returned perpetrator + victim + (for Ned) weapon + location.
  The reification model genuinely works for on-page narrative events.
- **Quote-carrying edges add real grading value** — every role edge cites a chapter file
  and quote, so an agent can show its work.

Note on tool nuance the agent had to learn: `--event-participants` only helps hubs that
have SUB_BEAT_OF children (red-wedding). Hubs that carry role edges *directly*
(execution-of-eddard-stark, robb-is-killed) return "0 participants" from
`--event-participants` and require `--neighbors` instead. A consumer agent must try both.

---

## 4. Routing decision

**Primary: (c) query-layer tooling — fix the alias resolver / slug-discoverability gap.**

Evidence: the largest and cheapest-to-fix failure class. In Q1, Q3, and Q7 the graph
*already contained the correct, quote-cited answer* and the ONLY thing standing between
the consumer agent and a correct answer was that the resolver returned MISS on an obvious
phrasing. I recovered every one of these by hand-searching the filesystem for the slug —
something a deployed agent can't reliably do. Concretely the resolver should: (a) fall
back to fuzzy/substring matching against the node slug index, (b) index the
victim/agent of `event.death`/`event.execution` hubs so "X's death" / "X's execution"
resolve, and (c) when a phrase names a character, return that character node as a
candidate so QoLB-style edges on the node are reachable. This converts 3 failures/partials
to correct and raises the realistic consumer-agent success rate from 4/10 to ~7/10 with
no new graph data.

**Secondary: (a) historical structural-backfill — connect existing dyadic edges to their
parent historical-event hubs.**

Evidence: Q5 (tourney-at-harrenhal, 0 edges) and Q10 (battle-of-the-trident, only
PART_OF) are isolated despite the underlying facts existing elsewhere in the graph as
dyadic edges and in the wiki cache. Backfilling participant/outcome edges onto these
existing historical hubs is well-scoped and addresses the `dark-historical` cluster.

I am explicitly **deprioritizing (d) narrative-arc reification** for *this* dip's
findings: only Q9/Q10 are arc-shaped, Q9 is already scheduled, and arc causal-chain work
is higher-cost/higher-risk than fixing the resolver. Arc work is the right *long-term*
track but not the highest-leverage *next* move given that the dominant failure is a
lookup-layer bug sitting on top of correct data. (b) Track-B beat-coverage is not
indicated — the beat-reified hubs I tested were already well-covered.

---

## 5. Bottom line for Matt

The graph is **genuinely useful to a consumer agent today for the two highest-frequency
question shapes**: "what's the relationship between A and B" (`--path` is excellent) and
"who did what in on-page event X" (beat reification + role edges, fully quote-cited). The
recently merged infobox layer makes kinship/allegiance/title questions reliably dense.
**The biggest thing holding it back is not data — it's the alias resolver:** in 3 of my
10 questions the perfect answer was already in the graph and only the natural-phrase→slug
step failed. Fix the resolver (fuzzy slug fallback + index death/execution hubs by their
victim) and the realistic success rate jumps from ~4/10 to ~7/10 for near-zero cost. The
remaining failures split into a known dark zone (historical events like the Tourney at
Harrenhal sit as isolated nodes; weapons/attendance/causal-chain edge types are empty
graph-wide) and the expected pre-mint Trident/Mycah arc hubs already on next session's
docket. **Highest-leverage next move: query-layer tooling first, historical
structural-backfill second; defer narrative-arc reification until those land.**

---

## 6. Post-dip corrections (Matt review, 2026-06-14)

Two of the auto-graded rows were re-examined against the source text. Both corrections
*strengthen* the routing conclusion (small deterministic fixes, not new extraction).

**Q4 — RE-GRADE: `failed` → not-applicable (no graph defect).** The dip framed the
missing weapon as a `dark-vocab` capability gap. That is wrong. The text *does* name the
weapon — Roose Bolton kills Robb with a longsword (`sources/chapters/asos/asos-catelyn-07.md:135`,
"He thrust his **longsword** through her son's heart, and twisted"; preceded by crossbow
bolts). But it is a *generic, unnamed* longsword, and `WIELDED_IN`'s target **must be an
`object.artifact`** (a *named* weapon node like Ice). There is no artifact to point the
edge at, and inventing a node for an unnamed longsword would be graph pollution. So the
graph correctly carries no `WIELDED_IN` here — this is **prose-only / not-applicable**, not
a dark-vocab failure. **Effect:** remove Q4 from the `dark-vocab` count; it should not
drive any backfill work. (Contrast Q7: Ned's execution *does* carry `WIELDED_IN → Ice`,
because Ice is a named artifact — the edge type works fine where a named weapon exists.)

**Q5 — REFRAME (grade stands as `failed`, but the fix is cheaper than stated).** The
"Rhaegar crowns Lyanna" fact is **already in the graph** as a dyad —
`rhaegar-targaryen → lyanna-stark` (`CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`), cited from
`sources/chapters/agot/agot-eddard-15.md:45`, and the evidence quote *literally describes
the Harrenhal tourney* ("...to lay the queen of beauty's laurel in Lyanna's lap"). The
only thing missing is that this dyad is **not attached** to the `tourney-at-harrenhal` hub
(confirmed 0 edges on the hub). Query from Rhaegar/Lyanna → found; query from the tourney →
nothing. So Q5 is the **poster child for the secondary track (historical structural-
attachment)**: the fix is to link an edge that already exists to its parent event hub —
no new fact extraction required. This is exactly the highest-leverage, $0-deterministic
shape of `POST-PLATE-5 followup #9`.

**Net effect on routing:** Q4 drops off the gap list entirely; Q5 confirms the secondary
track is cheap structural *attachment* of existing dyads to historical hubs. The corrected
failure-mode picture: dark-vocab is really only Q7-ATTENDS + Q10-causal (2, not 3);
slug-discoverability remains the dominant and cheapest-to-fix class. Stack unchanged in
order, sharper in justification: **(1) resolver fix, (2) attach-existing-dyads-to-
historical-hubs (followup #9), then new-extraction / arc-minting.**
