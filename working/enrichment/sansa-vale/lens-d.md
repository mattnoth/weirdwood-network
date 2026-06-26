# Lens D — Cross-Arc Causal Wiring
## Sansa / Vale enrichment dip

Date: 2026-06-25
Source chapters read: asos-sansa-06, asos-sansa-07, affc-sansa-01, affc-alayne-01, affc-alayne-02

---

## CROSS-ARC SEAMS (ranked by structural value)

---

### SEAM D-1 (HIGHEST VALUE): murder-of-jon-arryn ENABLES lysa-accuses-tyrion-of-poisoning-jon-arryn

**Structural problem:** `murder-of-jon-arryn` has zero outgoing edges. It is the root event of the entire war — nothing flows out of it. The most direct downstream is Lysa's false accusation against Tyrion (which set Catelyn chasing Tyrion into the Vale), but this edge is missing.

**Quote:** "You told me to put the tears in Jon's wine, and I did. For Robert, and for us! And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."
— `sources/chapters/asos/asos-sansa-07.md:287`

**Proposed edge:**
```
source_slug: murder-of-jon-arryn
edge_type:   ENABLES
target_slug: lysa-accuses-tyrion-of-poisoning-jon-arryn
ref:         sources/chapters/asos/asos-sansa-07.md:287
quote:       "You told me to put the tears in Jon's wine, and I did. For Robert, and for us! And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."
tier:        1
rationale:   Lysa's confession makes the causal sequence explicit: the murder ENABLES the false accusation (she committed both acts per LF's instruction). This is the same passage that established LF's agency — it now needs the downstream arrow.
```

**Endpoint check:** Both slugs verified present (query confirmed). `murder-of-jon-arryn` has 0 outgoing; `lysa-accuses-tyrion-of-poisoning-jon-arryn` has 0 outgoing. Both are dead-ends; this edge fixes the more structurally important one.

---

### SEAM D-2: lysa-accuses-tyrion-of-poisoning-jon-arryn ENABLES littlefinger-smuggles-sansa-out-of-kings-landing

**Structural problem:** `lysa-accuses-tyrion` has zero outgoing edges. That false accusation is what drove Catelyn to kidnap Tyrion and bring him to the Vale (AGOT), which made the Eyrie a known quantity for LF as a refuge. More directly: LF's entire plan to get Sansa into the Vale depends on Lysa being there and being loyal to him — Lysa is loyal because of the original murder/accusation conspiracy. The accusation ENABLES LF's use of the Vale as refuge.

**Quote (same passage confirms the causal chain):** "And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."
— `sources/chapters/asos/asos-sansa-07.md:287`

**Rationale for routing:** The proximate cause of the smuggle is `death-of-joffrey-baratheon` (already wired: `death-of-joffrey TRIGGERS littlefinger-smuggles-sansa`). But the *possibility* of using the Vale as refuge rests on Lysa's presence there and her bond to LF — which rests on the murder/accusation conspiracy. This is ENABLES (precondition), not TRIGGERS.

**Proposed edge:**
```
source_slug: lysa-accuses-tyrion-of-poisoning-jon-arryn
edge_type:   ENABLES
target_slug: littlefinger-smuggles-sansa-out-of-kings-landing
ref:         sources/chapters/asos/asos-sansa-07.md:287
quote:       "You told me to put the tears in Jon's wine, and I did. For Robert, and for us! And I wrote Catelyn and told her the Lannisters had killed my lord husband, just as you said."
tier:        2
rationale:   The Vale was available to LF as refuge specifically because Lysa's loyalty to him (founded on the murder + accusation conspiracy) made her compliant. Cross-book deduction, hence Tier 2. Agency-collapse check: LF's plan required Lysa's cooperation; routing through the accusation event (which cemented that cooperation) is more precise than routing through Lysa directly.
```

**Endpoint check:** Both slugs verified present.

---

### SEAM D-3 (DEAD-END FIX): littlefinger-smuggles-sansa-out-of-kings-landing ENABLES wedding-of-petyr-baelish-and-lysa-arryn

**Structural problem (see also § DEAD-END FIX below):** The smuggle has 2 outgoing edges: `LOCATED_AT red-keep` and `SUB_BEAT_OF purple-wedding`. Neither edge leads forward into the Vale. The *immediate downstream* of the smuggle is arrival at the Fingers and Lysa's wedding. That edge is completely absent.

**Quote:** "I expect your aunt is already riding to meet us. . . The Lady Lysa and I are to be wed."
— `sources/chapters/asos/asos-sansa-06.md:41`

The wedding happens directly as a result of the arrival at the Fingers after the escape: "They said their vows within the hour, standing beneath a sky-blue canopy as the sun sank in the west."
— `sources/chapters/asos/asos-sansa-06.md:245`

**Proposed edge:**
```
source_slug: littlefinger-smuggles-sansa-out-of-kings-landing
edge_type:   ENABLES
target_slug: wedding-of-petyr-baelish-and-lysa-arryn
ref:         sources/chapters/asos/asos-sansa-06.md:41
quote:       "I expect your aunt is already riding to meet us. The Lady Lysa and I are to be wed."
tier:        1
rationale:   LF's plan made Sansa's arrival at the Fingers the occasion for the long-deferred wedding. The smuggle directly enables the wedding by bringing LF to the Fingers at the appointed time. Without the escape from KL, LF could not have made his journey north to wed Lysa at that juncture.
```

**Endpoint check:** Both slugs verified present. `wedding-of-petyr-baelish-and-lysa-arryn` has 0 outgoing — still a dead-end after this fix (see SEAM D-4).

---

### SEAM D-4: wedding-of-petyr-baelish-and-lysa-arryn ENABLES lord-nestor-and-the-knights-call-for-marillion-s-death

**Structural problem:** The wedding has 0 outgoing edges. After the wedding, LF became Lord Protector of the Vale — which is exactly what gives him the authority to orchestrate Marillion's false confession and control the post-Lysa political situation.

**Quote:** "She'd never let them . . . no more than I'll let you steal my Petyr Littlefinger." [Lysa's speech]
Then (AFFC): "Petyr Baelish, Lord of Harrenhal, Lord Paramount of the Trident, and Lord Protector of the Eyrie and the Vale of Arryn"
— `sources/chapters/affc/affc-sansa-01.md:25`

The wedding is the precondition for LF's Lord Protector status and thus his ability to stage Marillion's confession before Nestor Royce.

**Quote for the specific ENABLES relationship:**
"I gave the man my word, sweetling. . . It will not be much longer. Lord Nestor is making his ascent on the morrow."
— `sources/chapters/affc/affc-sansa-01.md:29-30`

**Proposed edge:**
```
source_slug: wedding-of-petyr-baelish-and-lysa-arryn
edge_type:   ENABLES
target_slug: lord-nestor-and-the-knights-call-for-marillion-s-death
ref:         sources/chapters/affc/affc-sansa-01.md:25
quote:       "Petyr Baelish, Lord of Harrenhal, Lord Paramount of the Trident, and Lord Protector of the Eyrie and the Vale of Arryn, looked up from the letter he was writing."
tier:        2
rationale:   LF's marriage to Lysa made him Lord Protector, which is what gave him the authority to manage Lysa's death, coerce Marillion, and receive Nestor's "justice" hearing. Cross-book, hence Tier 2.
```

**Endpoint check:** Both slugs verified present.

---

### SEAM D-5: murder-of-jon-arryn MOTIVATES lysa-arryn [to keep the Vale out of the war]

**Structural problem:** There is no edge connecting LF's founding crime to Lysa's isolation of the Vale from the War of the Five Kings. Lysa herself states the connection — her guilt and her dependence on LF explain her political paralysis.

**Quote:** "I have kept the Vale out of this war. Our harvest has been plentiful, the mountains protect us, and the Eyrie is impregnable. Even so, it would not do to draw Lord Tywin's wrath down upon us."
— `sources/chapters/asos/asos-sansa-06.md:307`

**Quote establishing LF's control over Lysa:** "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!"
— `sources/chapters/asos/asos-sansa-07.md:287`

**Proposed edge:**
```
source_slug: murder-of-jon-arryn
edge_type:   MOTIVATES
target_slug: lysa-arryn
ref:         sources/chapters/asos/asos-sansa-07.md:287
quote:       "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!"
tier:        2
rationale:   Lysa's complicity in the murder (at LF's behest) is what made her politically dependent on him, explaining her keeping the Vale neutral — she could not act against LF's interests. The MOTIVATES target is a PERSON (lysa-arryn), routing her agency correctly. Agency collapse check: Lysa's neutrality was her own decision, but the founding crime is the coercive lever that MOTIVATED it. Tier 2 (interpretive causal link across scenes).
```

**Endpoint check:** `murder-of-jon-arryn` present. `lysa-arryn` present.

NOTE: The "Vale stays out of WO5K" is not currently a standalone event node. This MOTIVATES edge is the best available wiring given existing nodes; a future enrichment could mint a `vale-stays-neutral-in-the-war-of-five-kings` node and route CAUSES through it.

---

### SEAM D-6: death-of-lysa-arryn (NEW) — foundational node needed for downstream

**Structural problem:** `death-of-lysa-arryn` does not exist as a node. It is referenced by `lord-nestor-and-the-knights-call-for-marillion-s-death` (which treats Marillion as the killer) and is the precondition for the Lords Declarant pact and LF's formal Lord Protector status consolidation. Lens A is expected to mint this node. Until it exists, SEAMS D-4, D-7, and D-8 cannot be fully wired.

**Quote (the death):** "Littlefinger let Lysa sob against his chest for a moment, then put his hands on her arms and kissed her lightly. 'My sweet silly jealous wife,' he said, chuckling. 'I've only loved one woman, I promise you.' . . . 'Only Cat.' He gave her a short, sharp shove."
— `sources/chapters/asos/asos-sansa-07.md:297-303`

Once `death-of-lysa-arryn` is minted by Lens A, propose:

```
PENDING — requires death-of-lysa-arryn node from Lens A

source_slug: death-of-lysa-arryn
edge_type:   ENABLES
target_slug: lord-nestor-and-the-knights-call-for-marillion-s-death
ref:         sources/chapters/affc/affc-sansa-01.md:29
quote:       "Lord Nestor is making his ascent on the morrow."
tier:        1
rationale:   Lysa's death is the direct ENABLES for the framing hearing (it is what Lord Nestor is coming up to adjudicate). The hearing only occurs because someone pushed Lady Lysa through the Moon Door.
```

---

### SEAM D-7 (LF web): littlefinger-brokers-tyrell-lannister-alliance MOTIVATES petyr-baelish [to escape to the Vale]

**Structural problem:** The alliance brokerage is the last major act before LF departs KL. He secures his position by engineering Joffrey's betrothal to Margaery, then needs Joffrey dead to complete the play. The Vale becomes his refuge after the murder. There is no edge connecting the KL maneuvering arc to the Vale arc through LF's person.

**Quote:** "When I came to Highgarden to dicker for Margaery's hand, she let her lord son bluster while she asked pointed questions about Joffrey's nature. I praised him to the skies, to be sure . . . whilst my men spread disturbing tales amongst Lord Tyrell's servants. That is how the game is played."
— `sources/chapters/asos/asos-sansa-06.md:187`

**Proposed edge:**
```
source_slug: littlefinger-brokers-tyrell-lannister-alliance
edge_type:   MOTIVATES
target_slug: petyr-baelish
ref:         sources/chapters/asos/asos-sansa-06.md:187
quote:       "When I came to Highgarden to dicker for Margaery's hand, she let her lord son bluster while she asked pointed questions about Joffrey's nature. I praised him to the skies, to be sure . . . whilst my men spread disturbing tales amongst Lord Tyrell's servants."
tier:        2
rationale:   The Highgarden trip gave LF the cover to set up the Tyrell-Joffrey assassination scheme and position himself with clean hands. His safe departure to the Vale was enabled by this prior move. Cross-book deduction, Tier 2.
```

**Endpoint check:** Both slugs verified present.

---

### SEAM D-8 (LF web): sansa-receives-the-poisoned-hairnet ENABLES littlefinger-smuggles-sansa-out-of-kings-landing

**Structural problem:** This is the critical chain link. `sansa-receives-the-poisoned-hairnet CAUSES death-of-joffrey` is already wired. `death-of-joffrey TRIGGERS littlefinger-smuggles-sansa` is already wired. But the hairnet giving LF an excuse to extract Sansa is a separate ENABLES: Sansa's possession of the hairnet, her presence at the wedding, and LF's advance arrangement of the escape ship are all preconditions that ENABLE the smuggle independent of the trigger.

However — this is **already almost fully wired**. Check: `sansa-receives-the-poisoned-hairnet` → `CAUSES` → `death-of-joffrey` → `TRIGGERS` → `littlefinger-smuggles-sansa`. The `--full-chain` traversal via `CAUSES + TRIGGERS` already walks this path. An additional `ENABLES` edge from `sansa-receives-the-poisoned-hairnet` directly to `littlefinger-smuggles-sansa` would be over-proximal (it collapses the intermediate `death-of-joffrey` node, which is a genuine intermediate event). 

**VERDICT: No new edge needed here.** The `--full-chain` path already works from hairnet → death → smuggle. Do not short-circuit the intermediate event node.

---

## DEAD-END FIX (smuggle downstream)

**Current state:** `littlefinger-smuggles-sansa-out-of-kings-landing` has 2 outgoing edges:
- `LOCATED_AT red-keep`
- `SUB_BEAT_OF purple-wedding`

Neither leads forward. The node is a structural dead-end in the graph even though the smuggle is the pivot event of the entire arc.

**Fix:** SEAM D-3 above (`littlefinger-smuggles-sansa ENABLES wedding-of-petyr-baelish-and-lysa-arryn`) provides the immediate forward edge. Once the wedding node is wired forward via D-4 (`wedding ENABLES lord-nestor-and-the-knights-call`), the chain reads:

```
sansa-receives-the-poisoned-hairnet
  → CAUSES →
death-of-joffrey-baratheon
  → TRIGGERS →
littlefinger-smuggles-sansa-out-of-kings-landing     [D-3 below]
  → ENABLES →
wedding-of-petyr-baelish-and-lysa-arryn               [D-4 below]
  → ENABLES →
lord-nestor-and-the-knights-call-for-marillion-s-death
```

The full-chain traversal from the hairnet will now walk all the way into the Vale arc.

**Remaining gaps after D-3/D-4:**
- `lord-nestor-and-the-knights-call-for-marillion-s-death` has 0 outgoing. The downstream is LF securing Nestor's permanent loyalty via the Gates of the Moon deed — but this event is not yet a node (`littlefinger-bribes-nestor-royce-with-gates-of-moon` or similar). This is a **Lens A new-node candidate**, not a Lens D cross-arc wire.
- `wedding-of-petyr-baelish-and-lysa-arryn` has 0 incoming except `battle-on-the-green-fork PRECEDES`. SEAM D-3 adds the needed incoming from the smuggle.

---

## ENDPOINT-EXISTENCE FLAGS

| Slug | Exists? | Notes |
|------|---------|-------|
| `littlefinger-smuggles-sansa-out-of-kings-landing` | YES | 2 outgoing, 4 incoming |
| `wedding-of-petyr-baelish-and-lysa-arryn` | YES | 0 outgoing, 1 incoming — structural dead-end |
| `lord-nestor-and-the-knights-call-for-marillion-s-death` | YES | 0 outgoing, 3 incoming — structural dead-end |
| `sansa-receives-the-poisoned-hairnet` | YES | 3 outgoing, 3 incoming — well-wired |
| `death-of-joffrey-baratheon` | YES | confirmed in prior query |
| `murder-of-jon-arryn` | YES | 0 outgoing — the most critical dead-end in the whole graph |
| `lysa-accuses-tyrion-of-poisoning-jon-arryn` | YES | 0 outgoing — also a dead-end |
| `littlefinger-betrays-ned` | YES | 1 outgoing |
| `littlefinger-brokers-tyrell-lannister-alliance` | YES | 2 outgoing |
| `littlefinger-names-the-dagger-as-tyrion-s` | YES | 2 outgoing |
| `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` | YES | 0 outgoing |
| `petyr-baelish` | YES | character node |
| `sansa-stark` | YES | character node |
| `lysa-arryn` | YES | character node |
| `death-of-lysa-arryn` | **NO** | Expected from Lens A. Quote captured at asos-sansa-07.md:297-303. Required before SEAM D-6 can be minted. |

**Critical finding:** `murder-of-jon-arryn` (0 outgoing) is the single most structurally important dead-end in the Weirwood Network. It is the root event of the entire narrative — Robert Baratheon rides to Winterfell because Jon Arryn died — and nothing flows out of it. SEAM D-1 fixes its most direct downstream.

---

## HARVEST

`sources/chapters/asos/asos-sansa-06.md`
- line 91 / food+hospitality / Arbor vintage wine described in unusual depth — "tasted of oak and fruit and hot summer nights, the flavors blossoming in her mouth like flowers opening to the sun" — first proper drink Sansa keeps down after the voyage; rare positive sensory note for her
- line 75 / food / Oswell brings "oranges and pomegranates" from the King (the Merling King galley); LF offers pomegranate seeds one by one with his dagger throughout the confession scene — hospitality-as-manipulation register
- line 133 / food / Grisel brings "apples and pears and pomegranates, some sad-looking grapes, a huge blood orange" — the blood orange squeezed into LF's mouth immediately after he reveals the Tyrell role in Joffrey's death; charged imagery, likely intentional
- line 245 / food+hospitality / Wedding feast: "quail, venison, and roast boar, washing it down with a fine light mead" — Lysa brings her own mead; outdoor feast with torchlight
- line 258-259 / witness / Marillion's sexual assault attempt on Sansa, stopped by Lothor Brune with a knife — not in the graph at all; a foreseeable pattern in Sansa's vulnerability to male predation in her disguised state
- line 171 / foreshadowing / LF's "Three hidden daggers" speech about the Kettleblacks — plants that Osmund's loyalty to the Kingsguard white cloak overrode LF's control; anticipates TWOW Kettleblack testimony against Cersei

`sources/chapters/asos/asos-sansa-07.md`
- line 11 / setting / Snow falling on the Eyrie; Sansa builds snow-Winterfell — "I can feel the snow on my lashes, taste it on her lips. It was the taste of Winterfell." — first fully peaceful moment in her arc, immediately before the Lysa confrontation destroys it
- line 287 / foreshadowing / Lysa's full confession to Petyr (and Sansa) in the High Hall — Sansa is the only witness besides Marillion to the full scope of LF's crimes; this is what makes her dangerous and why LF keeps her close; not fully reflected in the graph
- line 301-303 / death / Lysa's death — the push is described economically: "Only Cat. He gave her a short, sharp shove. Lysa stumbled backward, her feet slipping on the wet marble. And then she was gone." — future Lens A should capture this verbatim

`sources/chapters/affc/affc-sansa-01.md`
- line 195 / food+hospitality / "We will serve him lies and Arbor gold, and he'll drink them down and ask for more" — the Arbor gold used to win Nestor Royce; hospitality-as-political-bribery; the wine appears physically (line 197) and is the vehicle of the lie
- line 278 / foreshadowing / "Trust no one, I once told Eddard Stark, but he would not listen. You are Alayne, and you must be Alayne all the time." — LF's only direct comparison of Ned and Sansa as strategic objects; she is being told to be better at playing the game than her father was

`sources/chapters/affc/affc-alayne-01.md`
- line 338 / foreshadowing / LF's prediction of the Lords Declarant: Redfort/Waynwood will die, Hunter will be murdered by Harlan, Belmore is corrupt, Lyn Corbray is his paid enemy — this is a full long-range prediction by LF of his own Vale strategy; if these facts are in the wiki they should be book-cite overlaid
- line 343 / character / "Ser Lyn will remain my implacable enemy . . . All he likes is gold and boys and killing" — LF paying Corbray to appear to oppose him is a master-class manipulation; Corbray's sexuality revealed here in passing; not currently graphed

`sources/chapters/affc/affc-alayne-02.md`
- line 467 / foreshadowing / The "Alayne Stone" end-game plan revealed: Harry the Heir → Robert dies → Harry becomes Lord of the Eyrie → Sansa revealed at his wedding in Stark maiden's cloak → Vale knights rally to Sansa's claim to Winterfell — this is the clearest statement of LF's entire strategic objective; major theory-evidence substrate
- line 182 / witness / Mya Stone's eyes "as big and blue" as Robert Baratheon's, "thick black hair he shared with Renly" — Sansa's internal recognition of Mya as Robert Baratheon's bastard; not in the graph; book-cite that should overlay the Mya Stone node
- line 367 / character / Mya Stone's speech about her father (unnamed): "He stands as tall as the sky, and he throws me up so high it feels as though I'm flying. . . Then one day he wasn't." — rare emotional glimpse; the man is Robert Baratheon (never named); the abandonment motif connects to the broader theme of Baratheon bastards left unacknowledged
