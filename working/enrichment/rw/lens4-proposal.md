# Red Wedding Enrichment — Lens 4: Causal-Wiring Proposal (S134)

> Existing-node↔existing-node cross-arc causal edges ONLY. Both endpoints verified to exist.
> Deduped against `baseline.md`. `--causal-chain` confirmed no edge exists before each proposal.

---

## PROPOSAL 1 (STRONGEST)

**`ser-wendel-manderly-is-killed` –MOTIVATES–> `wyman-manderly-stages-fake-execution-of-davos`**

- Source file confirmed: `graph/nodes/events/ser-wendel-manderly-is-killed.node.md`
- Target file confirmed: `graph/nodes/events/wyman-manderly-stages-fake-execution-of-davos.node.md`
- Tier: **1**
- Evidence — `sources/chapters/adwd/adwd-davos-04.md:125`
  > "My son Wendel came to the Twins a guest. He ate Lord Walder's bread and salt, and hung his sword upon the wall to feast with friends. And they murdered him. Murdered, I say, and may the Freys choke upon their fables. I drink with Jared, jape with Symond, promise Rhaegar the hand of my own beloved granddaughter … but never think that means I have forgotten. The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done."
- Causal mechanism: Wyman explicitly names Wendel's murder at the Twins as the reason he is faking cooperation with the Freys while secretly plotting against them. The fake execution of Davos (the elaborate deception that enables Manderly's covert pro-Stannis maneuver) is a direct consequence of Wendel's death — Wyman states this motivation in direct speech.
- Causal chain confirmed empty before: `--causal-chain wyman-manderly-stages-fake-execution-of-davos` → 0 upstream edges.
- Cross-arc seam: RW cluster (death beat) → Manderly revenge plot / White Harbor / north container.

---

## PROPOSAL 2

**`ser-wendel-manderly-is-killed` –MOTIVATES–> `wyman-publicly-arrests-davos-at-white-harbor`**

- Source file confirmed: `graph/nodes/events/ser-wendel-manderly-is-killed.node.md`
- Target file confirmed: `graph/nodes/events/wyman-publicly-arrests-davos-at-white-harbor.node.md`
- Tier: **1**
- Evidence — same passage: `sources/chapters/adwd/adwd-davos-04.md:125` (same Wyman monologue)
  > "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done."
  And from `adwd-davos-04.md:113`: "Afterward the Freys turned up with Wendel's bones … to make a peace and seal it with a marriage pact, they claimed, but I was not about to give them what they wanted until I had Wylis, safe and whole, and they were not about to give me Wylis until I proved my loyalty. Your arrival gave me the means to do that. That was the reason for the discourtesy I showed you in the Merman's Court."
- Causal mechanism: Wyman explains directly that the public arrest of Davos (and the whole theater of the Merman's Court) was performed to demonstrate loyalty to the Freys and secure Wylis's return — all driven by Wendel's death and Wyman's covert plan of revenge.
- Note: This is a SUB_BEAT_OF `wyman-manderly-stages-fake-execution-of-davos` — Proposal 1 already captures the main parent. Consider whether this beat-level wire adds value or is redundant. Flag for orchestrator judgment. Lower priority than Proposal 1.

---

## PROPOSAL 3 (STRONG)

**`roose-named-warden-of-the-north` –ENABLES–> `wedding-of-ramsay-bolton-and-arya-stark`**

- Source file confirmed: `graph/nodes/events/roose-named-warden-of-the-north.node.md`
- Target file confirmed: `graph/nodes/events/wedding-of-ramsay-bolton-and-arya-stark.node.md`
- Tier: **1**
- Evidence — `sources/chapters/adwd/adwd-the-prince-of-winterfell-01.md:127`
  > "In her children our two ancient houses will become as one," he [Roose] said, "and the long enmity between Stark and Bolton will be ended."
  And `:101`: "By this marriage Ramsay would be Lord of Winterfell."
- Causal mechanism: Roose being confirmed as Warden of the North — the political appointment that legitimizes Bolton rule — is what makes the fArya wedding possible and meaningful. The wedding is the instrument by which Bolton *consolidates* rule of Winterfell and the North after being elevated. Without the Warden status (which the RW directly caused), the marriage would lack the political substance that compels northern lords to attend and that makes Winterfell the prize.
- `--causal-chain wedding-of-ramsay-bolton-and-arya-stark` → 0 upstream causal edges confirmed.
- `--causal-chain roose-named-warden-of-the-north` → 0 downstream confirmed.
- Cross-arc seam: RW consequence → Bolton rule/north arc (ADWD).
- **Interpretive note**: the mechanism is strong on-page (Roose's Warden title is the political scaffold for the wedding plan) but the direct-text "because Roose is Warden, therefore this wedding" is an inference the reader makes from the political context, not a single verbatim sentence. Flag for fresh verify.

---

## PROPOSAL 4 (STRONG, cross-arc)

**`roose-named-warden-of-the-north` –MOTIVATES–> `stannis-march-on-winterfell`**

- Source file confirmed: `graph/nodes/events/roose-named-warden-of-the-north.node.md`
- Target file confirmed: `graph/nodes/events/stannis-march-on-winterfell.node.md`
- Tier: **1**
- Evidence — `sources/chapters/adwd/adwd-the-kings-prize-01.md:69`
  > "Roose Bolton is feared, but little loved. And his friends the Freys … the north has not forgotten the Red Wedding. Every lord at Winterfell lost kinsmen there. Stannis need only bloody Bolton, and the northmen will abandon him."
  And `:65`: "We will march, and we will free Winterfell … or die in the attempt."
- Causal mechanism: Stannis marches specifically to dislodge the Bolton regime — the illegitimate (in northern eyes) rule that flows directly from Roose's Warden appointment post-RW. The march is motivated by contesting Bolton's claim. The text makes explicit that Bolton is the target of the march.
- `--causal-chain stannis-march-on-winterfell` → 0 upstream causal edges confirmed.
- `--causal-chain roose-named-warden-of-the-north` → 0 downstream confirmed.
- Cross-arc seam: RW consequence (Bolton elevation) → Stannis/north military arc.
- Note: MOTIVATES fits better than ENABLES here — the Bolton rule provides Stannis with both motivation and a political opening (northern lords' resentment), not merely a technical precondition.

---

## PROPOSAL 5

**`the-rains-of-castamere` –ENABLES–> `red-wedding`**

- Source file confirmed: `graph/nodes/texts/the-rains-of-castamere.node.md`
- Target file confirmed: `graph/nodes/events/red-wedding.node.md` (hub)
- Tier: **1**
- Evidence — `sources/chapters/asos/asos-catelyn-07.md:99`
  > "No one sang the words, but Catelyn knew 'The Rains of Castamere' when she heard it. Edwyn was hurrying toward a door. She hurried faster, driven by the music."
  And `:103`: "The music drowned all other sound, echoing off the walls as if the stones themselves were playing. Robb gave Edwyn an angry look and moved to block his way . . . and staggered suddenly as a quarrel sprouted from his side."
- Causal mechanism: The playing of "The Rains of Castamere" is the pre-arranged massacre signal — the moment the song begins, crossbowmen reveal themselves. The song operationally enables the coordinated slaughter by serving as the trigger for armed action. This is mechanically functional, not merely atmospheric.
- `--neighbors the-rains-of-castamere` → 0 outgoing, 0 incoming edges confirmed (complete island).
- **Edge type clarification**: ENABLES (the song makes the coordinated signal/timing possible) rather than TRIGGERS (the song is not itself an agent that produces the massacre; it coordinates it). Orchestrator may prefer TRIGGERS — flag for judgment.

---

## PROPOSAL 6 (cross-arc, Arya)

**`robb-is-killed` –MOTIVATES–> `kill-list-recitation-before-sleep`**

- Source file confirmed: `graph/nodes/events/robb-is-killed.node.md`
- Target file confirmed: `graph/nodes/events/kill-list-recitation-before-sleep.node.md`
- Tier: **1**
- Evidence — `sources/chapters/asos/asos-arya-01.md:33` (pre-RW version of kill list does NOT include Walder Frey or Roose Bolton), versus post-RW Arya chapters where the list expands.
  
  **CAUTION — VERIFY BEFORE MINTING.** The kill-list node is cited from `asos-arya-01.md`, which is BEFORE the Red Wedding. The kill-list as a *practice* predates the RW; the RW adds Walder Frey, Roose Bolton, and others to it. The node `kill-list-recitation-before-sleep` appears to represent the general practice (it has 6 VICTIM_IN edges — Gregor, Dunsen, Polliver, Tickler, Sandor — none of which are RW killers). The mechanism would be: `robb-is-killed MOTIVATES` adding Frey/Bolton to the list — but this is the same recurring node, not a separate RW-expanded instance.
  
  **VERDICT: Flag as weak / interpretive.** The existing node predates the RW and the RW expands it, but the graph has no separate post-RW kill-list node to wire to. This proposal is not clean without a new node for "post-RW kill-list additions." Do NOT mint this edge as stated — the endpoint is the wrong instance. Flagged for orchestrator: if a lens-1/2 agent mints a "Arya-adds-Frey-and-Bolton-to-kill-list" node, THEN `robb-is-killed MOTIVATES` that new node.

---

## PROPOSAL 7 (cross-arc, Stoneheart downstream)

**`catelyn-rises-as-lady-stoneheart` –MOTIVATES–> `brienne-brought-before-lady-stoneheart`**

- **ALREADY EXISTS** — confirmed by `--causal-chain` as: `catelyn-rises-as-lady-stoneheart --[CAUSES]--> brienne-brought-before-lady-stoneheart`.
- Do NOT re-propose. Listed here to document the check.

---

## PROPOSAL 8 (cross-arc, Riverrun siege)

**`red-wedding` –ENABLES–> `siege-of-riverrun`**

- Source file confirmed: `graph/nodes/events/red-wedding.node.md`
- Target file confirmed: `graph/nodes/events/siege-of-riverrun.node.md`
- Tier: **1**
- Evidence — `sources/chapters/affc/affc-jaime-06.md:89`
  > "I've seen him. He looks lonely. Harrenhal has fallen. Seagard and Maidenpool. The Brackens have bent the knee … Piper, Vance, Mooton, all your bannermen have yielded. Only Riverrun remains."
  And the fundamental political context: the Red Wedding annihilated Robb's army and command structure, leaving Riverrun isolated and surrounded. The siege is only viable because the RW eliminated Riverrun's relieving force.
- Causal mechanism: The Red Wedding destroyed the Stark host that Riverrun depended on, leaving it strategically isolated and making the siege viable. Without the RW, Riverrun was the seat of an active military alliance with a field army; after it, Riverrun was an isolated holdout.
- `--causal-chain siege-of-riverrun` → 0 upstream causal edges confirmed.
- `--neighbors siege-of-riverrun` → `PART_OF war-of-the-five-kings` only on the causal side.
- **Interpretive note**: the mechanism is strong militarily but the prose does not state "the RW caused the siege" in a single sentence — it is the clear historical inference. Flag for fresh verify.

---

## HARVEST QUEUE ADDITIONS

| open | food/hospitality | asos | asos-catelyn-07.md:95 | Ser Wendel Manderly "lustily attacking a leg of lamb" moments before his death — last meal as a doomed guest; "food as dramatic irony" | S134 RW-lens4 |
| open | quote | adwd | adwd-davos-04.md:125 | "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done." — canonical statement of northern vengeance motive; should anchor wyman-manderly node ## Quotes | S134 RW-lens4 |
| open | foreshadowing | asos | asos-catelyn-07.md:99 | Catelyn "driven by the music" of the Rains of Castamere — her recognition is the on-page signal cue | S134 RW-lens4 |

---

## SUMMARY TABLE

| # | Edge | Type | Tier | Status |
|---|------|------|------|--------|
| 1 | `ser-wendel-manderly-is-killed` → `wyman-manderly-stages-fake-execution-of-davos` | MOTIVATES | 1 | **SHIP** — verbatim on-page |
| 2 | `ser-wendel-manderly-is-killed` → `wyman-publicly-arrests-davos-at-white-harbor` | MOTIVATES | 1 | Lower priority (beat-level redundancy with P1) |
| 3 | `roose-named-warden-of-the-north` → `wedding-of-ramsay-bolton-and-arya-stark` | ENABLES | 1 | **SHIP** — flag for fresh verify (inference) |
| 4 | `roose-named-warden-of-the-north` → `stannis-march-on-winterfell` | MOTIVATES | 1 | **SHIP** — strong cross-arc |
| 5 | `the-rains-of-castamere` → `red-wedding` | ENABLES | 1 | **SHIP** — flag edge-type (ENABLES vs TRIGGERS) |
| 6 | `robb-is-killed` → `kill-list-recitation-before-sleep` | MOTIVATES | — | **REJECT** — wrong node instance; needs post-RW node |
| 7 | Stoneheart → Brienne | CAUSES | — | Already exists — skip |
| 8 | `red-wedding` → `siege-of-riverrun` | ENABLES | 1 | **SHIP** — flag for fresh verify (historical inference) |
