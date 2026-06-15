# Narrative Arc Wave 1 — Joffrey Poisoning Conspiracy Draft
**Date:** 2026-06-14 (research subagent, working from S96 context)
**Status:** DRAFT — awaiting Matt review. Do NOT touch edges.jsonl, graph/nodes/, or sources/.
**Prototype followed:** Q5 `incident-at-the-trident` in `curation/s95-quarantine-resolutions-2026-06-13.md`
**Reference:** `working/narrative-arcs-design-memo-2026-06-13.md`

---

## 1. Proposed Arc Tree

```
[NEW: joffrey-poisoning-conspiracy]  (event.conspiracy — parent arc hub)
│
├── [NEW: dontos-delivers-hairnet-to-sansa]          SUB_BEAT_OF parent  — ASOS Sansa II
│         (the poison-vector delivery; Littlefinger's catspaw plants the weapon)
│
├── [NEW: olenna-takes-stone-from-hairnet]            SUB_BEAT_OF parent  — ASOS Tyrion VIII
│         (the Strangler crystal removed from hairnet at the pre-ceremony yard)
│
├── [EXISTS: purple-wedding]                          SUB_BEAT_OF parent  — already in graph
│         (wraps ceremony + feast; itself parent of 3 sub-beats)
│   ├── [EXISTS: wedding-ceremony-at-the-great-sept-of-baelor]  (sub-beat of purple-wedding)
│   ├── [EXISTS: death-of-joffrey-baratheon]                    (sub-beat of purple-wedding)
│   └── [EXISTS: tyrell-plot-revealed]                          (sub-beat of purple-wedding)
│
├── [EXISTS: killing-of-dontos-hollard]               SUB_BEAT_OF parent  — ASOS Sansa V
│         (Littlefinger silences his catspaw; already fully reified with role edges)
│
└── [NEW: sansa-s-escape-from-kings-landing]          SUB_BEAT_OF parent  — ASOS Sansa V
          (Dontos leads Sansa to Littlefinger's ship; arc closes when the trail goes cold)
```

**TRIGGERS chain (load-bearing junctures only):**
```
dontos-delivers-hairnet-to-sansa
    TRIGGERS olenna-takes-stone-from-hairnet
    (the hairnet must be on Sansa for Olenna to access it)

olenna-takes-stone-from-hairnet
    TRIGGERS death-of-joffrey-baratheon
    (the extracted crystal is the poison instrument)

death-of-joffrey-baratheon
    TRIGGERS killing-of-dontos-hollard
    (Dontos now a loose end; Littlefinger eliminates him)

death-of-joffrey-baratheon
    TRIGGERS sansa-s-escape-from-kings-landing
    (Joffrey's death is the trigger-event Dontos waited for; escorts Sansa out)
```

**Count:** 3 NEW sub-beat hubs + 4 EXISTS reused = 7 total sub-beats under the parent.
**Parent is new:** 1 new parent hub.
**Total new mints:** 4 nodes (parent + 3 sub-beat hubs).

---

## 2. JSON-Ready Edges

All edges below use the exact schema from Q5 (`curation/s95-quarantine-resolutions-2026-06-13.md`).

### 2a. Parent hub SUB_BEAT_OF chains (existing → new parent)

```json
{"edge_type":"SUB_BEAT_OF","source_slug":"dontos-delivers-hairnet-to-sansa","target_slug":"joffrey-poisoning-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-02","evidence_quote":"The night of Joffrey's wedding, that's not so long, wear the silver hair net and do as I told you, and afterward we make our escape.","evidence_ref":"sources/chapters/asos/asos-sansa-02.md:71","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Dontos delivers Littlefinger's hairnet (containing the Strangler) to Sansa — the poison-vector delivery beat of the conspiracy","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"olenna-takes-stone-from-hairnet","target_slug":"joffrey-poisoning-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-tyrion-08","evidence_quote":"The little old woman reached up and fussed at the loose strands, tucking them back into place and straightening Sansa's hair net.","evidence_ref":"sources/chapters/asos/asos-tyrion-08.md:101","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Olenna removes the Strangler crystal from Sansa's hairnet under the pretext of straightening it — the weapon-acquisition beat of the conspiracy","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"purple-wedding","target_slug":"joffrey-poisoning-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-06","evidence_quote":"Lady Olenna was not about to let Joff harm her precious darling granddaughter, so the night of Joffrey's wedding she'd had a certain maester slip a certain something into the king's wine.","evidence_ref":"sources/chapters/asos/asos-sansa-06.md:193","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"The Purple Wedding (ceremony + feast) is the execution beat of the conspiracy — the event within which the Strangler was deployed","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"killing-of-dontos-hollard","target_slug":"joffrey-poisoning-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"A bag of dragons buys a man's silence for a while, but a well-placed quarrel buys it forever.","evidence_ref":"sources/chapters/asos/asos-sansa-05.md:135","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Littlefinger's elimination of Dontos is the loose-end-silencing beat: closes the operational trail back to the conspirators","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"sansa-s-escape-from-kings-landing","target_slug":"joffrey-poisoning-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"Your disappearance will make them suspect you in Joffrey's death. The gold cloaks will hunt, and the eunuch will jingle his purse.","evidence_ref":"sources/chapters/asos/asos-sansa-05.md:135","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Littlefinger extracts Sansa (the frame and the tool) from King's Landing — the conspiracy's exit beat, engineering Tyrion's framing by her absence","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

### 2b. TRIGGERS (causal junctures)

```json
{"edge_type":"TRIGGERS","source_slug":"dontos-delivers-hairnet-to-sansa","target_slug":"olenna-takes-stone-from-hairnet","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-06","evidence_quote":"I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you.","evidence_ref":"sources/chapters/asos/asos-sansa-06.md:183","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"The hairnet can only be accessed on Sansa's head at the wedding; the delivery is the necessary precondition for the stone-removal beat","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"TRIGGERS","source_slug":"olenna-takes-stone-from-hairnet","target_slug":"death-of-joffrey-baratheon","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-06","evidence_quote":"Lady Olenna was not about to let Joff harm her precious darling granddaughter, so the night of Joffrey's wedding she'd had a certain maester slip a certain something into the king's wine.","evidence_ref":"sources/chapters/asos/asos-sansa-06.md:193","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"The extracted Strangler crystal is the poison instrument — removing it from the hairnet directly triggers its deployment in Joffrey's cup","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"TRIGGERS","source_slug":"death-of-joffrey-baratheon","target_slug":"killing-of-dontos-hollard","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"Ser Dontos the Red was a skin of wine with legs. He could never have been trusted with a task of such enormity. He would have bungled it or betrayed me.","evidence_ref":"sources/chapters/asos/asos-sansa-06.md:145","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Joffrey's death activates Littlefinger's pre-arranged disposal of Dontos — the catspaw becomes a liability only once the deed is done","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"TRIGGERS","source_slug":"death-of-joffrey-baratheon","target_slug":"sansa-s-escape-from-kings-landing","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"One bolt took Dontos in the chest as he looked up, punching through the left crown on his surcoat.","evidence_ref":"sources/chapters/asos/asos-sansa-05.md:127","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Joffrey's death is the trigger-event Dontos was waiting for to begin the escape; both sequences (Dontos killed + Sansa escapes) fire in the same night","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

### 2c. Role edges for NEW sub-beat hubs only

*(Role edges for existing hubs — `purple-wedding`, `death-of-joffrey-baratheon`, `killing-of-dontos-hollard` — are already in the graph or in pending S96 emissions. Do NOT duplicate.)*

**`dontos-delivers-hairnet-to-sansa` role edges:**
```json
{"edge_type":"COMMANDS_IN","source_slug":"petyr-baelish","target_slug":"dontos-delivers-hairnet-to-sansa","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"All he had to do was lead you from the castle . . . and make certain you wore your silver hair net.","evidence_ref":"sources/chapters/asos/asos-sansa-06.md:145","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Littlefinger directed Dontos to ensure Sansa wore the poisoned hairnet to the wedding — Dontos was the catspaw, Littlefinger the architect","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"dontos-hollard","target_slug":"dontos-delivers-hairnet-to-sansa","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-02","evidence_quote":"wear the silver hair net and do as I told you, and afterward we make our escape.","evidence_ref":"sources/chapters/asos/asos-sansa-02.md:71","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Dontos is the immediate delivery agent — he gave Sansa the hairnet and instructed her to wear it at the wedding","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"RECIPIENT_IN","source_slug":"sansa-stark","target_slug":"dontos-delivers-hairnet-to-sansa","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"The web of spun silver hung from her fingers, the fine metal glimmering softly, the stones black in the moonlight. Black amethysts from Asshai.","evidence_ref":"sources/chapters/asos/asos-sansa-05.md:23","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Sansa received and wore the hairnet (the poison vector) unknowingly — an innocent instrument of the conspiracy","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

**`olenna-takes-stone-from-hairnet` role edges:**
```json
{"edge_type":"AGENT_IN","source_slug":"olenna-tyrell","target_slug":"olenna-takes-stone-from-hairnet","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-tyrion-08","evidence_quote":"The little old woman reached up and fussed at the loose strands, tucking them back into place and straightening Sansa's hair net. 'I was very sorry to hear about your losses,' she said as she tugged and fiddled.","evidence_ref":"sources/chapters/asos/asos-tyrion-08.md:101","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Olenna removes the Strangler crystal from Sansa's hairnet under the cover of social fussing — the on-page weapon-acquisition act","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"UNWITTING_INSTRUMENT_IN","source_slug":"sansa-stark","target_slug":"olenna-takes-stone-from-hairnet","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"One of them was missing. Sansa lifted the net for a closer look. There was a dark smudge in the silver socket where the stone had fallen out.","evidence_ref":"sources/chapters/asos/asos-sansa-05.md:23","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Sansa's unwitting presence (wearing the hairnet) enables Olenna's stone-removal — Sansa discovers the missing stone only after Joffrey's death","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

> **Vocab note:** `RECIPIENT_IN` and `UNWITTING_INSTRUMENT_IN` are PROPOSED NEW role-edge qualifiers.
> Confirm these are in locked vocab before emitting — if not, fall back to `ATTENDS` (for Sansa on the delivery beat) and `VICTIM_IN` (for Sansa on the stone-removal beat, framing her as the instrument-victim).
> See §5 Open Design Questions #5 below.

**`sansa-s-escape-from-kings-landing` role edges:**
```json
{"edge_type":"AGENT_IN","source_slug":"dontos-hollard","target_slug":"sansa-s-escape-from-kings-landing","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"'Not far.' Ser Dontos took her hand in his own and rubbed it gently. 'Your friend is near, waiting for you.'","evidence_ref":"sources/chapters/asos/asos-sansa-05.md:105","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Dontos physically escorts Sansa from the Red Keep, over the cliff, and to Littlefinger's boat","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"COMMANDS_IN","source_slug":"petyr-baelish","target_slug":"sansa-s-escape-from-kings-landing","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"He smiled sadly. 'All he did he did at my behest. I dared not befriend you openly.'","evidence_ref":"sources/chapters/asos/asos-sansa-05.md:135","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Littlefinger orchestrated the escape route (ship, boat, man Oswell) — Dontos was executing his plan","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"VICTIM_IN","source_slug":"sansa-stark","target_slug":"sansa-s-escape-from-kings-landing","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"Your disappearance will make them suspect you in Joffrey's death.","evidence_ref":"sources/chapters/asos/asos-sansa-05.md:135","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Sansa is the principal extracted — framed by her disappearance, unknowing instrument of Littlefinger's design","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"lothor-brune","target_slug":"sansa-s-escape-from-kings-landing","decision":"emit_edge","candidate_kind":"curator-arc-wave1-joffrey","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-sansa-05","evidence_quote":"The two old men waded out up to their thighs to lift Sansa from the boat so she would not get her skirts wet. Oswell and Lothor splashed their way ashore.","evidence_ref":"sources/chapters/asos/asos-sansa-06.md:55","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Lothor Brune is the operational agent of the escape — rowed Sansa to the galley, later appeared at the Fingers landing","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

**Edge count:**
- 5 SUB_BEAT_OF (parent links)
- 4 TRIGGERS (causal chain)
- 9 role edges on new sub-beat hubs
- **Total proposed: 18 new edges**

---

## 3. Node Frontmatter — New Hubs

### Parent arc hub

`graph/nodes/events/joffrey-poisoning-conspiracy.node.md`:

```yaml
---
slug: joffrey-poisoning-conspiracy
type: event.conspiracy
name: "Joffrey Poisoning Conspiracy"
aliases:
  - "the Purple Wedding conspiracy"
  - "Littlefinger's plot to kill Joffrey"
  - "Olenna's plot"
  - "the Strangler plot"
confidence: tier-2
sources:
  - "asos-sansa-02"
  - "asos-tyrion-08"
  - "asos-sansa-05"
  - "asos-sansa-06"
pass_origin: curator-arc-wave1
---
## Identity
The coordinated conspiracy between Petyr Baelish (Littlefinger) and Olenna Tyrell (the Queen of Thorns) to assassinate King Joffrey Baratheon at his own wedding feast using the Strangler poison. Littlefinger supplied the poison concealed as black amethysts in a silver hairnet, which he caused to be delivered to Sansa Stark via his catspaw Ser Dontos Hollard. Olenna removed the Strangler crystal from Sansa's hairnet at the pre-feast gathering and introduced it into Joffrey's wine. The conspiracy was designed to frame Tyrion Lannister (whose absence as the accused would be engineered by Sansa's disappearance). Revealed to Sansa by Littlefinger at his Fingers tower in ASOS Sansa VI.

## Quotes
> "Ser Dontos the Red was a skin of wine with legs. He could never have been trusted with a task of such enormity. He would have bungled it or betrayed me. No, all Dontos had to do was lead you from the castle . . . and make certain you wore your silver hair net."
> — sources/chapters/asos/asos-sansa-06.md:145

> "I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you."
> — sources/chapters/asos/asos-sansa-06.md:183

> "Lady Olenna was not about to let Joff harm her precious darling granddaughter, so the night of Joffrey's wedding she'd had a certain maester slip a certain something into the king's wine."
> — sources/chapters/asos/asos-sansa-06.md:193
```

---

### Sub-beat hub 1: Hairnet delivery

`graph/nodes/events/dontos-delivers-hairnet-to-sansa.node.md`:

```yaml
---
slug: dontos-delivers-hairnet-to-sansa
type: event.deception
name: "Dontos Delivers Hairnet to Sansa"
aliases:
  - "the hairnet delivery"
  - "Sansa receives the silver hairnet"
  - "Dontos's hairnet instruction"
confidence: tier-2
sources:
  - "asos-sansa-02"
pass_origin: curator-arc-wave1
---
## Identity
Ser Dontos Hollard, acting as Littlefinger's catspaw, delivered a silver hairnet set with purported "black amethysts from Asshai" (actually Strangler crystals) to Sansa Stark and instructed her to wear it to Joffrey's wedding feast. The delivery likely occurred in the Red Keep godswood during one of Dontos's clandestine meetings with Sansa, prior to ASOS Sansa II (where the hairnet is already referenced as a standing instruction). Sansa wore it unknowingly as a poison-delivery mechanism.

## Quotes
> "The night of Joffrey's wedding, that's not so long, wear the silver hair net and do as I told you, and afterward we make our escape."
> — sources/chapters/asos/asos-sansa-02.md:71

> "The web of spun silver hung from her fingers, the fine metal glimmering softly, the stones black in the moonlight. Black amethysts from Asshai. One of them was missing."
> — sources/chapters/asos/asos-sansa-05.md:23
```

> **Uncertainty flag (see §6):** The exact chapter in which Dontos first gave Sansa the hairnet is off-page — it occurs before ASOS Sansa II, and the chapter of the actual gift-giving is not depicted directly. The ASOS Sansa II reference already treats it as an existing fact. This sub-beat's `evidence_chapter` is therefore `asos-sansa-02` (earliest citation) but with tier-2 confidence on the delivery's specifics.

---

### Sub-beat hub 2: Olenna takes the stone

`graph/nodes/events/olenna-takes-stone-from-hairnet.node.md`:

```yaml
---
slug: olenna-takes-stone-from-hairnet
type: event.deception
name: "Olenna Takes Stone from Hairnet"
aliases:
  - "Olenna removes the Strangler"
  - "the hairnet fussing"
  - "the Queen of Thorns steals the crystal"
confidence: tier-2
sources:
  - "asos-tyrion-08"
  - "asos-sansa-06"
pass_origin: curator-arc-wave1
---
## Identity
At the pre-feast gathering in the yard (ASOS Tyrion VIII), Lady Olenna Tyrell approached Sansa Stark and, under the social pretext of tidying a wind-blown hairnet, removed the Strangler crystal from one of its settings. The act was observed by Tyrion (the chapter POV) but its significance was not understood until Littlefinger's reveal in ASOS Sansa VI. The missing stone's dark smudge was discovered by Sansa later that same night after Joffrey's death.

## Quotes
> "The little old woman reached up and fussed at the loose strands, tucking them back into place and straightening Sansa's hair net."
> — sources/chapters/asos/asos-tyrion-08.md:101

> "One of them was missing. Sansa lifted the net for a closer look. There was a dark smudge in the silver socket where the stone had fallen out."
> — sources/chapters/asos/asos-sansa-05.md:23

> "I will wager you that at some point during the evening someone told you that your hair net was crooked and straightened it for you."
> — sources/chapters/asos/asos-sansa-06.md:183
```

---

### Sub-beat hub 3: Sansa's escape

`graph/nodes/events/sansa-s-escape-from-kings-landing.node.md`:

```yaml
---
slug: sansa-s-escape-from-kings-landing
type: event.escape
name: "Sansa's Escape from King's Landing"
aliases:
  - "Sansa flees the Red Keep"
  - "Dontos leads Sansa to Littlefinger's ship"
  - "Sansa's flight after the Purple Wedding"
confidence: tier-1
sources:
  - "asos-sansa-05"
  - "asos-sansa-06"
pass_origin: curator-arc-wave1
---
## Identity
Immediately following Joffrey's death, Ser Dontos Hollard led Sansa Stark out of the Red Keep — down a godswood path, over a cliff face, and into a waiting skiff — to a galley where Petyr Baelish awaited. Dontos was then killed by Lothor Brune on Littlefinger's order to silence the trail. Sansa's disappearance was engineered by Littlefinger to cast suspicion on her (and by extension Tyrion) for Joffrey's murder. She sailed to the Fingers, where Littlefinger revealed the conspiracy.

## Quotes
> "All he did he did at my behest. I dared not befriend you openly. When I heard how you saved his life at Joff's tourney, I knew he would be the perfect catspaw."
> — sources/chapters/asos/asos-sansa-05.md:135

> "Your disappearance will make them suspect you in Joffrey's death. The gold cloaks will hunt, and the eunuch will jingle his purse."
> — sources/chapters/asos/asos-sansa-05.md:135
```

> **Vocab note:** `event.escape` is PROPOSED. If not in locked vocab, fall back to `event.incident`. Check `reference/architecture.md` before minting.

---

## 4. Reused-Unchanged List

The following existing hubs and dyads are relied on by this arc but must NOT be modified:

| Slug | Type | Role in arc | Status |
|---|---|---|---|
| `purple-wedding` | event.wedding | Arc sub-beat (execution venue) | EXISTS, untouched |
| `death-of-joffrey-baratheon` | event.assassination | Arc sub-beat (the kill) | EXISTS, untouched (S96 role edges already live) |
| `wedding-ceremony-at-the-great-sept-of-baelor` | event.ceremony | Sub-beat of purple-wedding | EXISTS, untouched |
| `tyrell-plot-revealed` | event.conspiracy | Sub-beat of purple-wedding; Littlefinger reveals Tyrell plot to spirit Sansa to Highgarden | EXISTS, untouched |
| `killing-of-dontos-hollard` | event.death | Arc sub-beat (loose-end elimination) | EXISTS, untouched (S96 role edges already live) |
| `strangler` | concept.medical | The poison instrument | EXISTS, untouched |
| `petyr-baelish CONSPIRES_WITH olenna-tyrell` | dyad | Existing spine edge; arc does not duplicate | EXISTS, untouched |
| `tyrion-lannister POISONS joffrey-baratheon` | dyad | Tier-4 false-confession edge (F5, S96) | EXISTS, retier in progress |

---

## 5. Open Design Questions for Matt

### Q1 — Parent shape and name

**Proposed name:** `joffrey-poisoning-conspiracy`

**Rationale:** The arc is a *conspiracy* (deliberate plot with multiple phases), not a single incident. The name anchors to the most canonical "what happened" (Joffrey's poisoning) rather than the mastermind's name (avoids `littlefinger-s-plot-*` which front-loads a character over the event). Matches the S91 rename convention (event-named).

**Alternative:** `littlefinger-olenna-conspiracy` — emphasizes the co-conspirators explicitly; better for "who conspired" traversal but worse for "what happened to Joffrey" traversal.

**Matt's call:** Accept `joffrey-poisoning-conspiracy` OR rename. No functional difference for the graph; name only affects which queries hit the node naturally.

---

### Q2 — Arc boundary

**Proposed boundary:** Arc ends with `sansa-s-escape-from-kings-landing` (i.e., the arc includes both the kill AND the cover-up / frame-up beats).

**Rationale:** Littlefinger designed the escape as part of the conspiracy — Sansa's disappearance is intentional framing of Tyrion. The arc is not just "kill Joffrey" but "kill Joffrey and get away with it." Ending at `death-of-joffrey-baratheon` would leave the cover-up causal chain floating with no parent.

**Excluded from this arc (left for separate treatment):**
- Tyrion's trial (no trial/arrest event hub exists yet — would be a new mint in a future session)
- Sansa's ongoing arc at the Eyrie (different causal chain; beyond this conspiracy's scope)
- Tyrion killing Tywin (consequence cascade, not part of the original conspiracy)

**Alternative (narrower):** End at `killing-of-dontos-hollard` — "conspiracy completes when loose ends are tied." Sansa's escape then becomes a separate operational-consequence hub attached to the arc's aftermath, not a beat within the conspiracy itself.

**Recommended:** The wider boundary (include escape) because Littlefinger's instructions to Dontos explicitly bound both missions ("lead you from the castle AND make certain you wore your silver hair net" — same sentence, one agent, one commissioning). The escape IS part of the operation.

---

### Q3 — `tyrell-plot-revealed` relationship to this arc

**Context:** `tyrell-plot-revealed` (event.conspiracy, existing, SUB_BEAT_OF purple-wedding) models Littlefinger's EARLIER revelation to the Lannisters of the Tyrell plot to wed Sansa to Willas. This is a DIFFERENT event from the poisoning conspiracy — it's Littlefinger's political maneuvering to neutralize the Tyrell-Sansa plan and force the Tyrion-Sansa marriage. It shares actors (Littlefinger, house-tyrell) but is a distinct conspiratorial act.

**Current graph state:** `tyrell-plot-revealed` is already SUB_BEAT_OF `purple-wedding`. That link is defensible (it's a political beat that enabled the Purple Wedding to proceed as planned). This arc does NOT need to re-link it.

**Proposed answer:** Leave `tyrell-plot-revealed` as-is (SUB_BEAT_OF `purple-wedding` only). It is a sibling conspiracy — Littlefinger's information-warfare to foreclose Sansa's Highgarden escape route — not a beat in the poisoning conspiracy itself. The two conspiracies share Littlefinger as orchestrator but have different objects (Tyrell-Sansa marriage vs. Joffrey's life). A future "Littlefinger's King's Landing maneuvers" parent arc could group BOTH under one umbrella, but that is a larger, separate mint.

**Alternative:** Make `tyrell-plot-revealed` a second SUB_BEAT_OF `joffrey-poisoning-conspiracy` (arguing that derailing the Highgarden plan was necessary to keep Sansa in King's Landing as the weapon-carrier). Plausible but creates an arc with a boundary problem: when did the conspiracy "start"? The Highgarden deflection predates the hairnet delivery by multiple chapters.

**Recommended:** Keep them separate. The `tyrell-plot-revealed` → `purple-wedding` link is the right abstraction level.

---

### Q4 — TRIGGERS density

**Proposed:** 4 TRIGGERS edges only (the 4 load-bearing junctures above). No TRIGGERS between every adjacent pair of sub-beats.

**What was intentionally omitted:**
- `sansa-s-escape-from-kings-landing TRIGGERS killing-of-dontos-hollard` — actually, the temporal order is reversed: Dontos is killed *during* the escape sequence (he's in the boat when Brune fires). The TRIGGERS from `death-of-joffrey` to both events simultaneously is the right structure.
- `purple-wedding TRIGGERS killing-of-dontos-hollard` — overconstrained (Joffrey's death is the trigger, not the Purple Wedding broadly).
- SUB_BEAT_OF already implies temporal ordering within the arc; TRIGGERS is reserved for causal necessity.

**Recommended:** Ship the 4 TRIGGERS as proposed.

---

### Q5 — Vocab gaps: `RECIPIENT_IN` and `UNWITTING_INSTRUMENT_IN`

The `dontos-delivers-hairnet-to-sansa` and `olenna-takes-stone-from-hairnet` beats need a role for Sansa that expresses "passive participant / unknowing instrument" — not AGENT_IN, not VICTIM_IN (she's not harmed), not ATTENDS (she's the *object* of the act).

**Proposed vocab additions (if Matt approves):**
- `RECIPIENT_IN` — entity receives/bears the object of an event (weapon delivery, gift, verdict); neutral polarity
- `UNWITTING_INSTRUMENT_IN` — entity whose presence or action enables the event without their knowledge or consent

**Fallback if vocab not expanded:**
- `dontos-delivers-hairnet-to-sansa`: Sansa as `ATTENDS` (weakest but harmless)
- `olenna-takes-stone-from-hairnet`: Sansa as `VICTIM_IN` (slightly off — she's the instrument, not the victim)

**Recommended:** At minimum add `RECIPIENT_IN` (it has clear use cases beyond this arc: trial verdicts, prophecy recipients, etc.). `UNWITTING_INSTRUMENT_IN` is more specialized; could defer and use `VICTIM_IN` for now.

---

## 6. Uncertainty and Risk Flags

**Flag 1 — Hairnet delivery chapter is off-page.**
The specific chapter in which Dontos first physically handed Sansa the hairnet is not directly shown in ASOS. The earliest on-page reference to Sansa already *having* the hairnet with instructions is ASOS Sansa II (`asos-sansa-02.md:71`). The gift likely occurred at a prior godswood meeting. This means `dontos-delivers-hairnet-to-sansa`'s evidence is indirect (instruction-reference, not act-depiction). Tier-2 confidence is appropriate; the event is unambiguous, just not dramatized directly.

**Flag 2 — Littlefinger's account is his own testimony (reliability-2).**
All three of the key "Littlefinger reveal" quotes (`asos-sansa-06.md:145, 183, 193`) are Littlefinger speaking to Sansa. He is a canonical unreliable narrator. The poisoning conspiracy is corroborated circumstantially (missing stone, Olenna's behavior in `asos-tyrion-08`, the book's internal logic), but the exact mechanism ("a certain maester slip a certain something") remains secondhand. Tier-2 on all Littlefinger-sourced role-and-causal edges is correct and must not be promoted to tier-1.

**Flag 3 — `purple-wedding` as arc sub-beat creates a nesting asymmetry.**
`purple-wedding` is itself a parent hub with 3 sub-beats. Making it a sub-beat of `joffrey-poisoning-conspiracy` creates a two-level nesting (arc → purple-wedding → purple-wedding sub-beats). This is structurally legal (Trident prototype has no such nesting, but the vocab doesn't prohibit it) but may produce unexpected 2-hop traversal results. An agent querying "what are the sub-beats of `joffrey-poisoning-conspiracy`?" will get `purple-wedding` (1 hop), not `death-of-joffrey-baratheon` directly (2 hops through `purple-wedding`). This is the correct semantics — the conspiracy's "execution beat" IS the purple wedding as a whole, and drilling into the poisoning beat is a second-level query. But flag for Matt: if this is confusing, the alternative is to link `death-of-joffrey-baratheon` directly as SUB_BEAT_OF the arc, and demote `purple-wedding` to a non-sub-beat contextual link (e.g., `OCCURS_DURING`).

**Flag 4 — `event.escape` type may not be in locked vocab.**
Verify `reference/architecture.md` before minting `sansa-s-escape-from-kings-landing`. Fallback: `event.incident`.

**Flag 5 — Tyrion's framing/trial gap.**
This arc deliberately excludes Tyrion's arrest, trial, and escape (beyond scope; no hub exists yet for those). The consequence cascade (Tyrion kills Shae + Tywin, flees to Essos) is a separate narrative arc with its own causal structure. Flag for future wave-2 arc: `tyrion-lannister-trial-and-escape` as a sibling arc that begins where this one ends (Sansa's escape creates the vacuum that frames Tyrion).

---

## 7. Execution Checklist (for cleanup session)

Before emitting:
1. Verify `event.escape` in `reference/architecture.md` — if absent, use `event.incident` for `sansa-s-escape-from-kings-landing`
2. Verify `RECIPIENT_IN` and `UNWITTING_INSTRUMENT_IN` in locked vocab — if absent, apply fallbacks per §5 Q5
3. Mint 4 new node files (parent + 3 sub-beats) with the frontmatter above
4. Emit 18 edges to `graph/edges/edges.jsonl`
5. Do NOT modify: `purple-wedding`, `death-of-joffrey-baratheon`, `killing-of-dontos-hollard`, `tyrell-plot-revealed`, or any existing dyads
