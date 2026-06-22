# Lens D — Retro-grouping Standalone Arcs
**Date:** 2026-06-21 · **Lens:** D (retro-grouping standalones) · **Model:** Sonnet 4.6  
**Method:** Read-only. All claims grounded against live graph via `graph-query.py --full-chain`
and `event_alias_resolver.py --lookup`. Graph state: 22,384 edges; `containers:` field adopted
S121 (essos 16 nodes, wo5k 2 nodes).

---

## 0. Float policy confirmation

Architecture §containers (S121): omit the key **OR** set `containers: null` — **NEVER `[]`**.
Empty array is banned; it creates a false "uncategorized" class. This analysis uses that rule
throughout. `littlefinger-betrays-ned` already carries `containers: [wo5k]` — correct, not
`[]`.

---

## 1. The ~12 standalone arcs — inventory

The briefing names: RR · Bran's fall · Sack of KL · Purple Wedding · Tywin's death ·
B1 Red-Wedding-upstream · B2 Greyjoy→Theon-ward · B3 Ned's-downfall · the 4 AFFC arcs ·
littlefinger-betrays-ned. That is 12 named items (4 AFFC arcs = 4 separate arcs → 15 total
arc-threads across 12 shorthand entries). Table below treats each as a separate row.

---

## 2. Arc classification table

Each arc is verified by `--full-chain` on its root slug. Container set used for this analysis:
`wo5k`, `essos` (built), plus the proposed-but-not-yet-confirmed set `north`, `aegon`,
`kl-faith`, `riverlands`, `dorne`, `iron-islands`. Classification uses ONLY slugs that exist
in `graph/nodes/events/` or are confirmed by `event_alias_resolver.py`.

| Arc shorthand | Root slug (verified) | Causal chain summary | Container classification | Recommended `containers:` |
|---|---|---|---|---|
| **Robert's Rebellion** | `roberts-rebellion` | 4-edge upstream (tourney→abduction→executions→aerys-demands→RR); 0 downstream built. Pre-war event, historical background. | The RR is the backstory for WO5K but **not itself a WO5K juncture** (WO5K = War of the Five Kings, 298 AC onward; RR = 282 AC). RR is also the prerequisite for the AEGON thread (Targaryen restoration). Cross-cuts both but belongs to neither as a built arc. **Genuine standalone** — the war is pre-series backdrop, its own historical theater. | `null` |
| **Bran's fall** | `jaime-pushes-bran-from-the-tower` | 1 upstream (bran-witnesses TRIGGERS push); 5 downstream through Tyrion-arrest → Gregor-raids. Bran-coma/direwolf/dagger trail CAUSES the Tyrion-arrest which feeds the WO5K trigger chain. | The arc's downstream tail is WO5K plumbing (Tyrion arrested → war triggers). The node itself is a prelude incident in AGOT, not a WO5K battle. Its upstream is Bran's own POV (greensight/beyond-the-wall territory). It sits at a boundary: **event-as-WO5K-trigger AND event-as-Bran-origin**. Dual: `[wo5k, bran]` — if `bran` is adopted (Lens B decision). If `bran` is not adopted: `[wo5k]`. | `[wo5k]` (or `[wo5k, bran]` if `bran` container adopted) |
| **Sack of King's Landing** | `sack-of-kings-landing` | 2 upstream (battle-of-the-trident + pycelle-opens-gates CAUSE sack); 1 downstream (CAUSES coronation-of-robert). All historical (pre-series, ~283 AC). | Same theater as RR — this is the final battle of Robert's Rebellion, not WO5K. The aftermath (Jaime's reputation, Lannister power base) is backstory for the narrative but the event itself precedes the series. **Genuine standalone** — historical, pre-series. Same reason as RR: forcing it into `wo5k` would misrepresent the container's scope (WO5K = 298–300 AC war). | `null` |
| **Purple Wedding** | `purple-wedding` | 0 upstream, 0 downstream on the wiki node; but `death-of-joffrey-baratheon` (the curated arc node for the same event) has 1 upstream + 13 downstream. Note: `purple-wedding` is a Pass-2 wiki node; `death-of-joffrey-baratheon` is the Plate-3 curated hub. The real arc spine runs through `death-of-joffrey-baratheon`. | Firmly WO5K (ASOS, war period; Joffrey's assassination is a WO5K consequence-hub). The curated node `death-of-joffrey-baratheon` has a 14-edge chain that walks up to Sansa's hairnet and down to cersei-stripped. If tagging the wiki node too, both get `[wo5k]`. | `[wo5k]` (both `purple-wedding` wiki-node and `death-of-joffrey-baratheon` curated node) |
| **Tywin's death** | `assassination-of-tywin-lannister` | 7 upstream (traces to Sansa's hairnet via Purple Wedding chain); 3 downstream (→ cersei-rearms → captured → stripped). | Firmly WO5K (ASOS/AFFC, war consequence; the chain from Purple Wedding is unbroken WO5K territory). The 3 downstream hops (cersei-rearms → captured → stripped) are what launch the AFFC arc — but the AFFC arc's first node (`cersei-rearms`) is also `[wo5k]`-downstream. This node is pure `[wo5k]`. | `[wo5k]` |
| **B1 Red-Wedding-upstream** | `red-wedding-conspiracy` (upstream) + `red-wedding` (event hub) | `robb-weds-jeyne-westerling TRIGGERS red-wedding-conspiracy CAUSES red-wedding CAUSES robb-is-killed`. Also `catelyn-is-killed` (SUB_BEAT_OF `red-wedding`). | The whole Red Wedding thread is firmly WO5K — Robb's war, the Frey-Bolton betrayal, Tywin's orchestration. Both the upstream conspiracy and the event hub. **No north boundary collision:** the Red Wedding is set at the Twins (Riverlands), it kills the King in the North, but causally it's the WO5K military story (not the northern-political/Watch story that `north` would cover). | `[wo5k]` for `red-wedding-conspiracy`, `red-wedding`, `robb-is-killed`; `catelyn-is-killed` gets `[wo5k]` now (→ `[wo5k, riverlands]` later if riverlands adopted, as catelyn-rises IS the Stoneheart/riverlands node) |
| **B2 Greyjoy→Theon-ward** | `greyjoy-rebellion` (upstream) + `theon-greyjoy-taken-as-ward` (arc node) | `greyjoy-rebellion CAUSES theon-greyjoy-taken-as-ward` (1 edge, 0 downstream built). | `greyjoy-rebellion` is historical (289 AC, pre-series). `theon-greyjoy-taken-as-ward` is the AGOT-era consequence that sets up Theon's ACOK arc. The ward node is functionally a WO5K **precondition** (Theon's wardship → his return to Pyke → ironborn invasion). It's also the origin beat of what the proposal calls `[wo5k, north]` Theon territory. **Dual:** `[wo5k]` for the ward event (WO5K precondition, ironborn thread). `greyjoy-rebellion` itself is historical like RR/Sack — `null`. | `greyjoy-rebellion: null` · `theon-greyjoy-taken-as-ward: [wo5k]` |
| **B3 Ned's-downfall** | `execution-of-eddard-stark` (terminus); chain = `death-of-robert-baratheon CAUSES arrest CAUSES execution` (3 edges up); `execution CAUSES robb-proclaimed-king-in-the-north` + `MOTIVATES robb-stark` (2 downstream). | Firmly WO5K — the three-node chain (death-of-robert → arrest → execution → robb-king) is the WO5K origin spine. No container ambiguity. | `[wo5k]` |
| **AFFC #1 — Cersei's downfall** | `cersei-rearms-the-faith-and-forgives-the-debt` (root); walks 8 upstream to Sansa's hairnet; 2 downstream to `cersei-is-stripped-and-imprisoned` | The `cersei-rearms` node is already JOINED to the WO5K chain via `assassination-of-tywin-lannister CAUSES cersei-rearms`. The Cersei arc is a WO5K consequence. HOWEVER, the `kl-faith` / KL political theater is its own distinct container (proposal names it). The arc's central theme (Faith Militant / High Sparrow / Cersei's personal downfall) is the KL-Faith story, not the military war story. This is a **genuine dual**: `[wo5k, kl-faith]` — it lives IN the WO5K causal chain AND is the founding arc of the kl-faith container. | `[wo5k, kl-faith]` (gated: apply after `kl-faith` container name is confirmed) |
| **AFFC #2 — Kingsmoot → Euron** | `kingsmoot-on-old-wyk` (spine midpoint); `death-of-balon-greyjoy` (root, 0 upstream — declared intentional standalone). Chain: `death-of-balon TRIGGERS euron-seizes-seastone-chair CAUSES kingsmoot CAUSES taking-of-the-shields CAUSES euron-commissions-victarion`. Downstream `euron-commissions-victarion` is the bridge to Essos (Euron→Victarion→dragon-quest). | The Kingsmoot arc is its own theater (Iron Islands succession). The `iron-islands` container proposal is confirmed — this arc IS that container. It's a **genuine standalone** from the WO5K military story (Balon's death is not a WO5K consequence in the built graph), though Balon's death is historically connected (he died during the WO5K period). The bridge `euron-commissions-victarion` eventually points at Essos but the Kingsmoot itself is not causal WO5K. | `[iron-islands]` (gated: apply after `iron-islands` container name confirmed) |
| **AFFC #3 — Brienne → Stoneheart** | `brienne-brought-before-lady-stoneheart` (terminus); upstream: `catelyn-is-killed CAUSES catelyn-rises-as-lady-stoneheart CAUSES brienne-brought-before-lady-stoneheart` (2 edges). `catelyn-is-killed` is SUB_BEAT_OF `red-wedding`. | The Brienne→Stoneheart arc's causal root is the Red Wedding (`catelyn-is-killed`). Red Wedding is WO5K. The arc plays out in the Riverlands (BWB, hollow hill). The proposal maps this to `riverlands`. It's a **dual**: the root is WO5K, the setting/thread is Riverlands. `[wo5k, riverlands]` is the honest tag — or `[riverlands]` only if the riverlands container is scoped to carry this and WO5K is its implicit upstream. Lean `[riverlands]` since the arc's identity (Stoneheart, BWB, Brienne) is the Riverlands story; the `catelyn-is-killed` seam node gets `[wo5k, riverlands]`. | `brienne-brought-before-lady-stoneheart: [riverlands]` · `catelyn-rises-as-lady-stoneheart: [riverlands]` · `catelyn-is-killed: [wo5k, riverlands]` (gated: after `riverlands` confirmed) |
| **AFFC #4 — Dorne / Queenmaker** | `the-queenmaker-plot` (root, 0 upstream — standalone); 4 downstream (`areo-hotah-springs-the-ambush CAUSES arianne-collapses-and-is-captured CAUSES doran-reveals-fire-and-blood-pact`; `ambush TRIGGERS myrcella-is-maimed-by-darkstar`). The `doran-reveals-fire-and-blood-pact` closes into the Essos AEGON thread (Dorne→Targaryen restoration). | The Queenmaker plot is the Dorne container's founding arc. Its terminus (`doran-reveals-fire-and-blood-pact`) cross-joins into the AEGON thread. Tag: `[dorne]` for the core nodes; `doran-reveals-fire-and-blood-pact` gets `[dorne, aegon]` when AEGON is built (it's the seam). The Queenmaker plot is already rooted in the WO5K chain via `gregor-confesses-and-kills-oberyn CAUSES arrest-of-the-sand-snakes` — which MOTIVATES Arianne. So the deepest upstream of the arc IS WO5K (the Purple Wedding chain). But the arc's identity is Dorne. Recommendation: tag nodes in the Dorne arc `[dorne]`; the `arrest-of-the-sand-snakes` seam node gets `[wo5k, dorne]`. | `the-queenmaker-plot: [dorne]` · `arrest-of-the-sand-snakes: [wo5k, dorne]` (gated: after `dorne` confirmed) |
| **littlefinger-betrays-ned** | `littlefinger-betrays-ned` | 0 upstream, 0 downstream in live graph (the causal chain is unbuilt — the edges connecting it to the arrest are not yet wired). Already tagged `containers: [wo5k]` in frontmatter. | **Already tagged.** Confirmed correct — Littlefinger's betrayal is the immediate spark for Ned's arrest, firmly WO5K. No change needed. | `[wo5k]` (ALREADY STAMPED) |

---

## 3. Summary: classification by category

### Clean single-container arcs (tag now — no container-set dependency)

These map unambiguously to `wo5k` and can be tagged immediately regardless of whether the
broader container set (north/aegon/kl-faith/riverlands/dorne/iron-islands) is confirmed:

| Arc | Root slug | Tag |
|---|---|---|
| Bran's fall | `jaime-pushes-bran-from-the-tower` | `[wo5k]` |
| Purple Wedding (curated) | `death-of-joffrey-baratheon` | `[wo5k]` |
| Purple Wedding (wiki) | `purple-wedding` | `[wo5k]` |
| Tywin's death | `assassination-of-tywin-lannister` | `[wo5k]` |
| B1 Red-Wedding-upstream | `red-wedding-conspiracy`, `red-wedding`, `robb-is-killed` | `[wo5k]` |
| B3 Ned's-downfall chain | `execution-of-eddard-stark`, `arrest-of-eddard-stark`, `death-of-robert-baratheon`, `robb-proclaimed-king-in-the-north` | `[wo5k]` |
| B2 Theon-ward | `theon-greyjoy-taken-as-ward` | `[wo5k]` |
| littlefinger-betrays-ned | `littlefinger-betrays-ned` | `[wo5k]` (**already stamped**) |

Total wo5k-only tags needed (excluding already-stamped): approximately **13–15 node edits**.

### Dual-container arcs (gated on container-set confirmation)

| Arc | Nodes | Tag |
|---|---|---|
| AFFC #1 Cersei's downfall | `cersei-rearms-the-faith-and-forgives-the-debt`, `osney-kettleblack-confesses-to-high-sparrow`, `cersei-is-captured-in-the-sept`, `cersei-is-stripped-and-imprisoned` | `[wo5k, kl-faith]` |
| AFFC #3 Brienne→Stoneheart seam | `catelyn-is-killed` | `[wo5k, riverlands]` |
| AFFC #3 (Riverlands nodes) | `catelyn-rises-as-lady-stoneheart`, `brienne-brought-before-lady-stoneheart` | `[riverlands]` |
| AFFC #4 seam | `arrest-of-the-sand-snakes` | `[wo5k, dorne]` |
| AFFC #4 (Dorne nodes) | `the-queenmaker-plot`, `areo-hotah-springs-the-ambush`, `arianne-collapses-and-is-captured`, `myrcella-is-maimed-by-darkstar` | `[dorne]` |
| AFFC #4 terminus | `doran-reveals-fire-and-blood-pact` | `[dorne, aegon]` (when AEGON built) |
| AFFC #2 Kingsmoot | `death-of-balon-greyjoy`, `euron-seizes-the-seastone-chair`, `kingsmoot-on-old-wyk`, etc. | `[iron-islands]` |

### Genuine standalones — stay `null`

| Arc | Root slug | Why null |
|---|---|---|
| Robert's Rebellion | `roberts-rebellion` | Historical (282 AC); pre-dates WO5K; cross-cuts both WO5K-backstory and AEGON-backstory. No container owns it cleanly. |
| Sack of King's Landing | `sack-of-kings-landing` | Historical (283 AC); final battle of RR. Same reason. |
| Greyjoy Rebellion | `greyjoy-rebellion` | Historical (289 AC); backdrop, not a live-narrative arc. |

---

## 4. Cost/benefit: retro-tagging now vs deferring

### The half-tagged graph problem

The briefing asks directly: is a half-tagged graph **worse than none**?

**Answer: yes, partial is worse than none for `--container` queries, but the damage is bounded
and asymmetric by container.**

- `--container wo5k` currently returns 2 nodes (only `robert-orders-daenerys-assassination` and
  `littlefinger-betrays-ned`). A user running `--container wo5k` today gets a misleadingly thin
  result that looks like the container is mostly unbuilt — but 13+ WO5K-tagged nodes are sitting
  untagged. That is actively misleading.
- `--container essos` returns 16 nodes and is accurate (Essos is fully tagged). The contrast
  makes `wo5k` look like an incomplete container next to a complete one.
- The half-tagged state gets **worse with every new node minted** into the WO5K thread that
  also goes untagged. Each future WO5K-adjacent build inherits the problem.

### What "defer entirely" (option c) costs

Option (c) = treat tagging as a separate project, stamp going-forward only. This means the
accumulated 13–15 wo5k-backlog nodes remain untagged while every NEW node does get tagged.
The result is a graph where new builds are retrievable but the founding arcs (Ned's execution,
Red Wedding, Purple Wedding) are invisible to `--container wo5k`. That defeats the query's
purpose for the most important events in the corpus.

### What "tag all now" (option a) costs

Option (a) = tag the wo5k-clean subset + all the gated arcs (AFFC containers). The AFFC arcs
are gated on container-set confirmation (kl-faith/riverlands/dorne/iron-islands). If Matt
hasn't confirmed those names, tagging with them bakes in names that may change. This is the
real risk — not the effort (15 node edits is cheap).

### What "tag the clean subset now" (option b) costs/benefits

Option (b) = tag all the wo5k-only arcs now (no container-set dependency), leave the AFFC
gated arcs null until Matt confirms kl-faith/riverlands/dorne/iron-islands. This:
- Fixes the `--container wo5k` misleadingness immediately (2 nodes → 15+ nodes).
- Does NOT bake in unconfirmed container names.
- Leaves the AFFC arcs null (honest — they genuinely have no confirmed container yet).
- The AFFC null state is defensible: those arcs have no `containers:` field at all, so
  `--container kl-faith` simply returns 0 nodes (a clear signal nothing is built yet).
  That's different from `--container wo5k` returning 2 when 15 exist.

---

## 5. Weighing against architecture's retro-tagging caveat

Architecture note: "retro-tagging is a separate decision, not automatic."

This clause exists to prevent auto-stamping at mint-time for containers that weren't confirmed
when the arc was built. It does NOT mean "never retro-tag." The clause is a process gate
(require explicit decision), not a permanent deferral.

The wo5k-only tags are:
- The simplest possible container assignment (all ~15 nodes unambiguously `[wo5k]`).
- Idempotent: a `stamp_containers.py` script can be run safely and re-run.
- Low risk of name instability: `wo5k` is the most established container name in the project
  (appears in both decomp docs, two node files, multiple session entries).

The AFFC-gated tags depend on `kl-faith`/`riverlands`/`dorne`/`iron-islands` — names that
are currently PROPOSALS, not confirmed decisions. Stamping them before Matt confirms the
container-set names would violate the "retro-tagging is a separate decision" principle.

---

## 6. Single recommendation

**Option (b): tag the wo5k-clean subset now; leave AFFC arcs null pending container-set
confirmation.**

Concretely:
1. Run `scripts/stamp_containers.py` (or equivalent) on the ~15 wo5k-only nodes listed in
   §3's "clean single-container" table. This is the only set that needs no additional
   decision from Matt.
2. Bran's-fall node gets `[wo5k]` (or `[wo5k, bran]` if Matt confirms the `bran` container,
   which is a Lens B decision).
3. All AFFC arc nodes stay **null** until Matt confirms the container-set names (the open
   question from the proposal's §"Open questions for Matt" #1).
4. Historical arcs (RR, Sack of KL, Greyjoy Rebellion) stay `null` permanently — they are
   genuine standalones.
5. `littlefinger-betrays-ned` is already correctly stamped `[wo5k]` — no action needed.

**Trigger for the gated batch:** once Matt confirms the AFFC container names
(`kl-faith`, `riverlands`, `dorne`, `iron-islands` — or their replacements), the
remaining AFFC arc nodes can be tagged in one additional `stamp_containers.py` run.
That is a second, separate decision — no need to conflate it with the wo5k backfill.

---

## 7. Slug existence verification

Verified against live `graph/nodes/events/` or `event_alias_resolver.py`:

| Slug | Status |
|---|---|
| `roberts-rebellion` | EXISTS |
| `jaime-pushes-bran-from-the-tower` | EXISTS |
| `sack-of-kings-landing` | EXISTS |
| `purple-wedding` | EXISTS |
| `death-of-joffrey-baratheon` | EXISTS |
| `assassination-of-tywin-lannister` | EXISTS |
| `red-wedding-conspiracy` | EXISTS |
| `red-wedding` | EXISTS |
| `robb-is-killed` | EXISTS |
| `execution-of-eddard-stark` | EXISTS |
| `arrest-of-eddard-stark` | EXISTS |
| `death-of-robert-baratheon` | EXISTS |
| `robb-proclaimed-king-in-the-north` | EXISTS |
| `greyjoy-rebellion` | EXISTS |
| `theon-greyjoy-taken-as-ward` | EXISTS |
| `littlefinger-betrays-ned` | EXISTS (already tagged `[wo5k]`) |
| `cersei-rearms-the-faith-and-forgives-the-debt` | EXISTS |
| `osney-kettleblack-confesses-to-high-sparrow` | EXISTS |
| `cersei-is-captured-in-the-sept` | EXISTS (via chain) |
| `cersei-is-stripped-and-imprisoned` | EXISTS |
| `kingsmoot-on-old-wyk` | EXISTS |
| `brienne-brought-before-lady-stoneheart` | EXISTS |
| `catelyn-rises-as-lady-stoneheart` | EXISTS |
| `catelyn-is-killed` | EXISTS |
| `the-queenmaker-plot` | EXISTS |
| `battle-of-the-blackwater` | EXISTS (HIT via resolver) |
| `cersei-is-captured-in-the-sept` | EXISTS (in Cersei chain) |

---

## 8. Divergence from orchestrator proposal (Lens D §)

The orchestrator proposal's Lens D table (`working/session-results/2026-06-21-container-split-PROPOSAL.md`)
includes `battle-of-the-blackwater [wo5k]` and `robb-proclaimed-king-in-the-north [wo5k]`
as separate rows. Both are **confirmed here** (Blackwater has 3 downstream WO5K edges; Robb-King
is the B3 terminus). The orchestrator also included "Robert's death" as `[wo5k]` — here
classified `[wo5k]` (the death-of-robert-baratheon node is the WO5K root trigger, not a
pre-series historical event unlike RR/Sack).

One divergence: the orchestrator marks "Greyjoy→Theon-ward (B2)" as `[wo5k]` (single tag
for the whole arc). This analysis splits it: `greyjoy-rebellion` itself stays `null`
(historical, 289 AC), while `theon-greyjoy-taken-as-ward` gets `[wo5k]` (the narrative
consequence that feeds into WO5K). The greyjoy-rebellion node has no downstream WO5K edges
other than the ward event — it's background.

The orchestrator deferred the entire retro-tag batch "until Matt picks the container SET."
This analysis disagrees on one point: the **wo5k-only nodes are safe to tag NOW without
waiting for the full set decision**, because `wo5k` is already an adopted, stable container
name. Waiting for kl-faith/riverlands confirmation to tag Ned's execution as `[wo5k]` is
unnecessary caution.

---

## 9. Float policy — final confirmation

- Omit key: valid (same as null for query purposes).
- `containers: null`: valid (preferred when you want to make the intentional no-container
  decision explicit).
- **`containers: []`: NEVER.** Banned per architecture §S121. Zero nodes in this audit use
  it; the `littlefinger-betrays-ned` node correctly uses `containers: [wo5k]` (single-element
  array with a real name).
