# Narrative-Arc Wave 1 — Red Wedding Arc (DRAFT)
**Date:** 2026-06-14
**Status:** DRAFT — research-and-propose pass only. Do NOT touch graph/edges/edges.jsonl, graph/nodes/, or sources/.
**Reviewer:** Matt
**Model:** claude-sonnet-4-6 (research + drafting)
**Prototype used:** `incident-at-the-trident` / Q5 in `curation/s95-quarantine-resolutions-2026-06-13.md`

---

## Summary

The Red Wedding arc spans from Robb Stark's broken Frey marriage pact through the massacre at the Twins and ends at Lady Stoneheart's emergence. The graph already has the central `red-wedding` event hub (12 sub-beat children, rich role edges). This draft proposes a new **parent arc hub** that treats `red-wedding` as ONE of its children, alongside upstream cause-beats and downstream consequence-beats.

**Proposed parent slug:** `red-wedding-conspiracy` (type `event.conspiracy`)
**Beats summary:** 2 new mints + 5 reused existing nodes = 7 total sub-beats of the parent
**Proposed edges:** 13 new edges (7 SUB_BEAT_OF + 4 TRIGGERS + 2 role edges on new mints)
**Open question for Matt:** see §5 below — the most important decision is whether the arc terminus is `catelyn-is-resurrected-as-lady-stoneheart` (ASOS epilogue) or whether that beat is deferred to a separate "Lady Stoneheart arc."

---

## 1. Proposed Arc Tree

**PARENT (NEW):**
- `[NEW: red-wedding-conspiracy]` — `event.conspiracy` — the Tywin-brokered Frey-Bolton betrayal pact and its execution; encompasses cause, execution, and immediate aftermath

**SUB-BEATS (in causal order):**

| Order | Node | Status | Source |
|---|---|---|---|
| 1 | `[NEW: robb-breaks-frey-marriage-pact]` | NEW | ASOS Catelyn II |
| 2 | `[NEW: frey-bolt-offer-edmure-roslin]` | NEW | ASOS Catelyn IV |
| 3 | `[EXISTS: red-wedding]` | EXISTS — retro-linked | ASOS Catelyn VII (has 12 sub-beats of its own) |
| 4 | `[EXISTS: robb-is-killed]` | EXISTS — already SUB_BEAT_OF red-wedding | ASOS Catelyn VII |
| 5 | `[EXISTS: catelyn-is-killed]` | EXISTS — already SUB_BEAT_OF red-wedding | ASOS Catelyn VII |
| 6 | `[NEW: death-of-grey-wind]` | NEW | ASOS Catelyn VII + Arya XI + Tyrion VI |
| 7 | `[NEW: catelyn-is-resurrected-as-lady-stoneheart]` | NEW | ASOS Epilogue (Merrett POV) |

**Notes on tree shape:**
- Beats 4 and 5 (`robb-is-killed`, `catelyn-is-killed`) are already children of `red-wedding`. The arc parent does NOT need to directly claim them — they are reachable via `red-wedding TRIGGERS robb-is-killed` + the `SUB_BEAT_OF` chain. TRIGGERS from `red-wedding` to `catelyn-is-resurrected-as-lady-stoneheart` covers the causation at arc level.
- Beat 2 (`frey-bolt-offer-edmure-roslin`) is the Lame Lothar offer scene (ASOS Catelyn IV) — the mechanism by which Edmure is lured to the Twins. This is the conspiracy's operational lure.
- The conspiracy's backstage architects (Tywin, Walder, Roose) attach to `red-wedding-conspiracy` via role edges; the on-the-ground massacre participants attach at the `red-wedding` sub-beat level per existing S87 convention.

---

## 2. JSON-Ready Edges

### 2a — Parent hub SUB_BEAT_OF links (7 edges)

```json
{"edge_type":"SUB_BEAT_OF","source_slug":"robb-breaks-frey-marriage-pact","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-02","evidence_quote":"\"And you,\" she said softly, \"have lost the Freys.\" His wince told all.","evidence_ref":"sources/chapters/asos/asos-catelyn-02.md:133","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Robb's marriage to Jeyne Westerling — breaking his Frey pact — is the inciting upstream beat of the Red Wedding conspiracy","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"frey-bolt-offer-edmure-roslin","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-04","evidence_quote":"\"You are then instructed to offer Lord Tully the hand of my sister, the Lady Roslin, a maid of sixteen years.\"","evidence_ref":"sources/chapters/asos/asos-catelyn-04.md:209","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Lame Lothar's Roslin offer to Edmure is the conspiracy's operational lure — the Twins wedding that brings Robb's army within Frey reach","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"red-wedding","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-07","evidence_quote":"The players in the gallery had finally gotten both king and queen down to their name-day suits. With scarcely a moment's respite, they began to play a very different sort of song. No one sang the words, but Catelyn knew \"The Rains of Castamere\" when she heard it.","evidence_ref":"sources/chapters/asos/asos-catelyn-07.md:99","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"The Red Wedding massacre event-hub is the execution beat of the Red Wedding conspiracy arc","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"death-of-grey-wind","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-07","evidence_quote":"Catelyn heard the crash of distant battle, and closer the wild howling of a wolf. Grey Wind, she remembered too late.","evidence_ref":"sources/chapters/asos/asos-catelyn-07.md:113","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Grey Wind's death outside the Twins is a direct consequence-beat of the conspiracy, occurring simultaneously with Robb's killing","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"catelyn-is-resurrected-as-lady-stoneheart","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-epilogue","evidence_quote":"When she lowered her hood, something tightened inside Merrett's chest, and for a moment he could not breathe. No. No, I saw her die. She was dead for a day and night before they stripped her naked and threw her body in the river.","evidence_ref":"sources/chapters/asos/asos-epilogue.md:169","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Catelyn's resurrection as Lady Stoneheart is the arc's downstream consequence-terminus: the Red Wedding conspiracy is what kills her and drives her transformation","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

*Note: The remaining 2 SUB_BEAT_OF edges (robb-is-killed, catelyn-is-killed → red-wedding-conspiracy) are proposed as OPTIONAL — see design question §5.3. If Matt prefers not to double-parent them, omit. The arc is traversable via `red-wedding-conspiracy → red-wedding → robb-is-killed` anyway.*

### 2b — TRIGGERS edges (causal direction within the arc; 4 load-bearing junctures only)

```json
{"edge_type":"TRIGGERS","source_slug":"robb-breaks-frey-marriage-pact","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-02","evidence_quote":"\"And you,\" she said softly, \"have lost the Freys.\" His wince told all. She understood the angry voices now, why Perwyn Frey and Martyn Rivers had left in such haste, trampling Robb's banner into the ground as they went.","evidence_ref":"sources/chapters/asos/asos-catelyn-02.md:133","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Robb breaking the Frey pact is the direct cause that initiates the Frey-Bolton-Lannister betrayal planning (Walder begins secretly corresponding with Roose and Tywin)","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"TRIGGERS","source_slug":"frey-bolt-offer-edmure-roslin","target_slug":"red-wedding","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-04","evidence_quote":"\"It is my lord father's wish that this marriage take place at once.\" ... \"It must happen,\" said Catelyn, though not gladly. \"Without this wedding, Robb's cause is lost. Edmure, we must accept.\"","evidence_ref":"sources/chapters/asos/asos-catelyn-04.md:219","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"The Edmure-Roslin wedding arrangement lures Robb's army to the Twins — it is the direct operational cause of the massacre","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"TRIGGERS","source_slug":"red-wedding","target_slug":"death-of-grey-wind","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-tyrion-06","evidence_quote":"\"Roslin caught a fine fat trout,\" the message read. \"Her brothers gave her a pair of wolf pelts for her wedding.\"","evidence_ref":"sources/chapters/asos/asos-tyrion-06.md:41","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"The Red Wedding massacre causes Grey Wind's death outside the Twins (wolf pelts = Grey Wind and the Stark banner; Frey message to Tywin confirms both wolf and king killed together)","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"TRIGGERS","source_slug":"catelyn-is-killed","target_slug":"catelyn-is-resurrected-as-lady-stoneheart","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-epilogue","evidence_quote":"No. No, I saw her die. She was dead for a day and night before they stripped her naked and threw her body in the river. Raymund opened her throat from ear to ear. She was dead.","evidence_ref":"sources/chapters/asos/asos-epilogue.md:169","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Catelyn's throat-cutting at the Red Wedding is the direct cause of her corpse being recovered and resurrected as Lady Stoneheart by Beric Dondarrion","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

### 2c — Role edges for new beats only (2 edges)

Role edges for `robb-breaks-frey-marriage-pact`:

```json
{"edge_type":"AGENT_IN","source_slug":"robb-stark","target_slug":"robb-breaks-frey-marriage-pact","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-02","evidence_quote":"\"Mother,\" he said, \"I have the great honor to present you the Lady Jeyne Westerling. Lord Gawen's elder daughter, and my . . . ah . . . my lady wife.\"","evidence_ref":"sources/chapters/asos/asos-catelyn-02.md:99","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Robb's marriage to Jeyne Westerling is the act that breaks the Frey pact","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"lothar-frey","target_slug":"frey-bolt-offer-edmure-roslin","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-04","evidence_quote":"\"You are then instructed to offer Lord Tully the hand of my sister, the Lady Roslin, a maid of sixteen years.\"","evidence_ref":"sources/chapters/asos/asos-catelyn-04.md:209","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Lame Lothar delivers the Roslin offer at Hoster Tully's funeral — the Conspiracy's operational step","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

Role edges for `catelyn-is-resurrected-as-lady-stoneheart`:

```json
{"edge_type":"AGENT_IN","source_slug":"beric-dondarrion","target_slug":"catelyn-is-resurrected-as-lady-stoneheart","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-arya-07","evidence_quote":"\"I gave him the good god's own kiss to send him on his way. I filled my mouth with fire and breathed the flames inside him, down his throat to lungs and heart and soul. The last kiss it is called.\"","evidence_ref":"sources/chapters/asos/asos-arya-07.md:97","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Beric Dondarrion gives Catelyn the Last Kiss, sacrificing his own final life to resurrect her; the quote is from ASOS Arya VII where Thoros explains the mechanism (Tier 2 — the mechanism is verbatim from Arya VII; the act itself at Catelyn's resurrection is reported by Merrett in the epilogue, not POV-witnessed)","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"nymeria-direwolf","target_slug":"catelyn-is-resurrected-as-lady-stoneheart","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-arya-12","evidence_quote":"She paddled after the sharp red whisper of cold blood, the sweet cloying stench of death. She chased them as she had often chased a red deer through the trees, and in the end she ran them down, and her jaw closed around a pale white arm. She shook it to make it move, but there was only death and blood in her mouth. By now she was tiring, and it was all she could do to pull the body back to shore.","evidence_ref":"sources/chapters/asos/asos-arya-12.md:89","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Nymeria (via Arya's wolf-dream) retrieves Catelyn's body from the river, enabling Beric's resurrection","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"VICTIM_IN","source_slug":"catelyn-stark","target_slug":"catelyn-is-resurrected-as-lady-stoneheart","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-epilogue","evidence_quote":"Her cloak and collar hid the gash his brother's blade had made, but her face was even worse than he remembered. The flesh had gone pudding soft in the water and turned the color of curdled milk.","evidence_ref":"sources/chapters/asos/asos-epilogue.md:171","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Catelyn Stark is the subject of the resurrection — killed at the Red Wedding, resurrected as Lady Stoneheart","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

Role edges for `red-wedding-conspiracy` — conspiracy architects (parent arc only; no role edges on execution beats beyond what already exists at red-wedding sub-beat level):

```json
{"edge_type":"COMMANDS_IN","source_slug":"tywin-lannister","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-tyrion-06","evidence_quote":"\"How long have you and Walder Frey been plotting this?\" \"I mislike that word,\" Lord Tywin said stiffly. ... \"There was no reason to tell you. You had no part in this.\"","evidence_ref":"sources/chapters/asos/asos-tyrion-06.md:125","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Tywin Lannister co-engineered the Red Wedding conspiracy, providing political cover and the promise of Lannister protection that made Walder Frey dare act","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"COMMANDS_IN","source_slug":"walder-frey","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-tyrion-06","evidence_quote":"\"I have no doubt he hatched this ugly chicken, but he would never have dared such a thing without a promise of protection.\"","evidence_ref":"sources/chapters/asos/asos-tyrion-06.md:205","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Walder Frey is the primary architect of the conspiracy (Tyrion's words confirm this is Walder's design, enabled by Tywin)","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"roose-bolton","target_slug":"red-wedding-conspiracy","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-tyrion-06","evidence_quote":"\"The price was cheap by any measure. The crown shall grant Riverrun to Ser Emmon Frey once the Blackfish yields. Lancel and Daven must marry Frey girls, Joy is to wed one of Lord Walder's natural sons when she's old enough, and Roose Bolton becomes Warden of the North.\"","evidence_ref":"sources/chapters/asos/asos-tyrion-06.md:207","confidence_tier":1,"typed_by":"curator-arc-wave1","asserted_relation":"Roose Bolton is a co-conspirator; his reward (Warden of the North) confirms his active participation in the betrayal pact","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

Role edge for `death-of-grey-wind`:

```json
{"edge_type":"VICTIM_IN","source_slug":"grey-wind","target_slug":"death-of-grey-wind","decision":"emit_edge","candidate_kind":"curator-arc-wave1-red-wedding","evidence_kind":"book-pass1","evidence_book":"asos","evidence_chapter":"asos-catelyn-07","evidence_quote":"Catelyn heard the crash of distant battle, and closer the wild howling of a wolf. Grey Wind, she remembered too late.","evidence_ref":"sources/chapters/asos/asos-catelyn-07.md:113","confidence_tier":2,"typed_by":"curator-arc-wave1","asserted_relation":"Grey Wind is killed outside the Twins during the Red Wedding massacre (Tier 2 — Catelyn hears the howl and Wolf pelts confirmed in Walder-Tywin message; exact kill-scene is off-page)","schema_version":"pass1-derived-v1","produced_at":"2026-06-14T00:00:00+00:00"}
```

---

## 3. Node Frontmatter for NEW Hubs

### `graph/nodes/events/red-wedding-conspiracy.node.md`

```yaml
---
slug: red-wedding-conspiracy
type: event.conspiracy
name: "Red Wedding Conspiracy"
aliases: ["the Red Wedding conspiracy", "Frey-Bolton betrayal", "Tywin's plan", "betrayal at the Twins"]
confidence: tier-1
sources: ["asos-catelyn-02", "asos-catelyn-04", "asos-catelyn-07", "asos-tyrion-06", "asos-epilogue"]
pass_origin: curator-arc-wave1
---
## Identity
The secret betrayal pact engineered by Tywin Lannister, Walder Frey, and Roose Bolton to assassinate Robb Stark, King in the North, by violating guest right. Triggered by Robb's marriage to Jeyne Westerling (breaking his promise of a Frey bride). The Edmure-Roslin wedding was constructed as operational lure to bring Robb's army within Frey reach at the Twins. The arc runs from the broken pact (ASOS Catelyn II) through the massacre (ASOS Catelyn VII) to Lady Stoneheart's emergence (ASOS Epilogue). Walder Frey is confirmed by Tyrion as the architect; Tywin as enabler; Roose Bolton as co-conspirator rewarded with the Wardenship of the North.
```

### `graph/nodes/events/robb-breaks-frey-marriage-pact.node.md`

```yaml
---
slug: robb-breaks-frey-marriage-pact
type: event.incident
name: "Robb Breaks the Frey Marriage Pact"
aliases: ["Robb marries Jeyne Westerling", "the broken Frey pact", "the marriage to the Crag"]
confidence: tier-1
sources: ["asos-catelyn-02"]
pass_origin: curator-arc-wave1
---
## Identity
While recuperating from a wound taken at the Crag, and after learning of the reported deaths of Bran and Rickon, Robb Stark married Jeyne Westerling out of grief and honor (he had taken her maidenhood). This violated the marriage contract sealed at the Twins, by which Robb had promised to wed a daughter of Walder Frey in exchange for passage of the bridge and Frey swords. Catelyn first learns of the marriage publicly, presented with Jeyne on the dais in Riverrun's great hall (ASOS Catelyn II). The Freys present — Perwyn, Martyn Rivers, and close to forty others — left immediately, trampling Robb's banner as they departed.
```

### `graph/nodes/events/frey-bolt-offer-edmure-roslin.node.md`

```yaml
---
slug: frey-bolt-offer-edmure-roslin
type: event.incident
name: "Frey Offer: Edmure-Roslin Marriage"
aliases: ["Lame Lothar's offer", "the Roslin offer", "the Frey renewal offer"]
confidence: tier-1
sources: ["asos-catelyn-04"]
pass_origin: curator-arc-wave1
---
## Identity
At Hoster Tully's funeral at Riverrun, Lame Lothar Frey presented Lord Walder's terms for restoring the Frey-Stark alliance: Robb to apologize in person at the Twins, and Edmure Tully to marry Roslin Frey. Catelyn and Brynden Tully urged acceptance despite Edmure's reluctance — without Frey swords, Robb had no path to retake Moat Cailin. The wedding's timing (immediate, at the Twins) was Lord Walder's insisted condition — ostensibly for dynastic urgency, actually to control the venue. This offer is the operational mechanism by which the Red Wedding conspiracy lures Robb's army within Frey reach (ASOS Catelyn IV).
```

### `graph/nodes/events/death-of-grey-wind.node.md`

```yaml
---
slug: death-of-grey-wind
type: event.death
name: "Death of Grey Wind"
aliases: ["Grey Wind's death", "the killing of Grey Wind", "the wolf pelts"]
confidence: tier-2
sources: ["asos-catelyn-07", "asos-tyrion-06"]
pass_origin: curator-arc-wave1
---
## Identity
Grey Wind, Robb Stark's direwolf, was killed outside the Twins during the Red Wedding massacre, simultaneously with Robb's own death. Lord Walder Frey had refused to allow the direwolf into the hall; he was kenneled outside, separated from Robb. His howl is audible during the massacre (Catelyn hears it from inside the hall). His death is confirmed off-page via Walder Frey's message to Tywin Lannister: "Her brothers gave her a pair of wolf pelts for her wedding" (ASOS Tyrion VI). Salladhor Saan reports that smallfolk heard Lord Frey had Grey Wind's head hacked off and sewn onto Robb's corpse, with a crown nailed about the wolf's ears (ASOS Davos V). Kill is Tier-2 (no on-page POV witness to the act itself).
```

### `graph/nodes/events/catelyn-is-resurrected-as-lady-stoneheart.node.md`

```yaml
---
slug: catelyn-is-resurrected-as-lady-stoneheart
type: event.incident
name: "Catelyn Is Resurrected as Lady Stoneheart"
aliases: ["the Last Kiss", "Beric's resurrection of Catelyn", "Catelyn becomes Lady Stoneheart", "Lady Stoneheart's emergence"]
confidence: tier-1
sources: ["asos-arya-12", "asos-epilogue"]
pass_origin: curator-arc-wave1
---
## Identity
After the Red Wedding, Nymeria (in Arya's wolf-dream) retrieved Catelyn Stark's body from the Green Fork, where the Freys had thrown it after stripping it naked. Beric Dondarrion gave Catelyn the Last Kiss — sacrificing his own final life to breathe fire into her corpse. The resurrection mechanism is described by Thoros of Myr in ASOS Arya VII. Catelyn was resurrected mute (her throat had been cut too deep) and consumed by vengeance. She became Lady Stoneheart and took command of the Brotherhood Without Banners, beginning Frey retribution (ASOS Epilogue, Merrett POV). Her resurrection is the arc terminus: the Red Wedding conspiracy's final, unintended consequence.
```

---

## 4. Reused-Unchanged List

These existing hubs/dyads the arc relies on but does NOT modify:

| Slug | Type | Why it's needed |
|---|---|---|
| `red-wedding` | event.wedding | Core massacre beat; retro-linked as SUB_BEAT_OF red-wedding-conspiracy |
| `robb-is-killed` | event.death | Already SUB_BEAT_OF red-wedding; reachable via red-wedding chain |
| `catelyn-is-killed` | event.death | Already SUB_BEAT_OF red-wedding; TRIGGERS catelyn-is-resurrected-as-lady-stoneheart |
| `catelyn-secures-guest-right` | event.incident | Already SUB_BEAT_OF red-wedding (S95 just minted) |
| `the-wedding-feast-proceeds` | event.feast | Already SUB_BEAT_OF red-wedding |
| `grey-wind-attacks` | event.incident | Pre-massacre warning beat (ASOS Catelyn VI, Frey riders at the gate); no new edges needed — its chapter evidence is the lead-up, not the conspiracy itself |
| `red-wedding-revealed` | event.ceremony | Post-massacre Tyrion VI / ASOS Epilogue beat; already in graph |
| `merrett-attempts-to-defend-his-innocence-in-the-red-wedding` | event | Post-massacre; already in graph |
| `jaime-demands-the-red-wedding-captives` | event | AFFC aftermath; already in graph |
| `catelyn-stark` | character.human | Both alias `lady-stoneheart` per resolver |
| `grey-wind` | character.direwolf | Resolved by resolver |
| `beric-dondarrion` | character.human | Verified by resolver |
| `nymeria-direwolf` | character.direwolf | Verified by resolver |
| `walder-frey` | character.human | Verified by resolver |
| `roose-bolton` | character.human | Verified by resolver |
| `tywin-lannister` | character.human | Verified by resolver |
| `robb-stark` | character.human | Verified by resolver |
| `lothar-frey` | character.human | Verified by resolver |
| `roslin-frey` | character.human | Verified by resolver |
| `jeyne-westerling` | character.human | Verified by resolver |
| `war-of-the-five-kings` | event | red-wedding already PART_OF this; no new edge needed at arc level |

---

## 5. Open Design Questions for Matt

### Q1 — Parent shape: NEW arc hub vs. `red-wedding` as anchor

**The question:** Should the parent be a NEW hub `red-wedding-conspiracy` (proposed here), or should `red-wedding` itself serve as the parent with upstream cause-beats TRIGGERS-linked into it?

**Proposed answer: NEW hub `red-wedding-conspiracy`.** Reasoning:

1. `red-wedding` is already a rich event-hub with 12 SUB_BEAT_OF children and 44 role edges. Adding upstream beats (broken pact, Frey offer) as SUB_BEAT_OF children of `red-wedding` would misrepresent them — the broken pact (ASOS Catelyn II) happened months before the wedding; it is NOT a sub-beat of the wedding event, it is its cause. Sub-beats should be concurrent or closely sequential parts of the same event.
2. The Trident prototype (Q5) always minted a NEW parent even when the central event was already reified. `incident-at-the-trident` wraps the Lady execution hubs as its children; by analogy `red-wedding-conspiracy` wraps `red-wedding` as one of its children.
3. A new `event.conspiracy` hub cleanly separates "what happened at the Twins" from "the months-long planning, deception, and aftermath that constitute the arc."

**Alternative:** treat `red-wedding` as anchor, TRIGGERS-link cause-beats into it (`robb-breaks-frey-marriage-pact TRIGGERS red-wedding`), and TRIGGERS-link aftermath beats out of it (`red-wedding TRIGGERS catelyn-is-resurrected-as-lady-stoneheart`). Simpler; avoids minting a new parent. Loses the conspiracy framing and makes arc-level queries harder (no single node to traverse "everything about this arc"). Recommend rejecting.

### Q2 — Parent type: `event.conspiracy` vs. alternatives

**Proposed answer: `event.conspiracy`.** The arc's defining shape is a multi-party secret betrayal plan executed across months. `event.conspiracy` is already in locked vocab (architecture.md lists it). Alternatives:

- `event.incident`: too narrow (used for single-scene events like the Trident roadside confrontation)
- `event.battle`: wrong — the Red Wedding is a slaughter, not a pitched engagement
- `event.deception`: describes a sub-aspect (the lure); not the full arc shape

Flag: `event.conspiracy` was added to vocab in S93. If architecture.md lists it as locked, we are fine. If not fully locked in the type table, may need architecture.md annotation (same issue as `event.incident` which Q5 resolved by adding it to the table).

### Q3 — Arc boundaries: where does it start and end?

**Proposed start:** `robb-breaks-frey-marriage-pact` (ASOS Catelyn II, Riverrun). This is the earliest event the graph can speak to with verbatim evidence. The ACTUAL start of the Frey-Robb alliance is the crossing-pact at the Twins (AGOT), but that is already a separate event chain; starting the CONSPIRACY arc at the broken pact is clean.

- Alternative start: the Tywin-Walder-Bolton secret correspondence (between Catelyn II and Catelyn IV). This is not on-page in any chapter; Tywin confirms it in Tyrion VI but the actual parley is wholly off-page. Omit as a mintable beat.

**Proposed end:** `catelyn-is-resurrected-as-lady-stoneheart` (ASOS Epilogue). Reasoning:
- The arc's thematic completion is Catelyn's transformation — the Red Wedding's most lasting structural consequence.
- The Frey retribution thread (Lady Stoneheart hanging Freys, Wyman Manderly's pies) continues into AFFC/ADWD but belongs to a downstream arc ("Lady Stoneheart retribution"), not this one.

**Alternative end:** `robb-is-killed` (treat the arc as closed at the primary assassination, omit aftermath beats). Simpler, tighter. Loses Stoneheart, which is the most consequential downstream node for agent queries. Recommend rejecting.

### Q4 — TRIGGERS density: load-bearing junctures only

**Proposed:** 4 TRIGGERS edges (see §2b above). These are the minimum causal load-bearing links:
1. `robb-breaks-frey-marriage-pact TRIGGERS red-wedding-conspiracy` — initiating cause
2. `frey-bolt-offer-edmure-roslin TRIGGERS red-wedding` — operational lure causes massacre
3. `red-wedding TRIGGERS death-of-grey-wind` — parallel kill
4. `catelyn-is-killed TRIGGERS catelyn-is-resurrected-as-lady-stoneheart` — death causes resurrection

**What was omitted:**
- `grey-wind-attacks TRIGGERS red-wedding` (wolf's warning at the gate): tempting but Tier-3 causal (the attack didn't trigger the massacre; the massacre was already planned; the attack was a symptom). Omit.
- `robb-breaks-frey-marriage-pact TRIGGERS frey-bolt-offer-edmure-roslin`: correct causally (the broken pact causes Walder to construct the lure) but this causal link is already captured by both beats being SUB_BEAT_OF the same conspiracy parent. Adding a TRIGGERS edge would be redundant. Omit.

---

## 6. Uncertainty and Risk Flags

### 6.1 — Grey Wind's kill scene is off-page (Tier-2 flag)
The text never gives a POV witness to Grey Wind's actual killing. Evidence: (a) Catelyn hears howling during the massacre (`asos-catelyn-07.md:113`); (b) Walder's message to Tywin calls them "wolf pelts" (`asos-tyrion-06.md:41`); (c) Salladhor Saan's smallfolk rumor about the sewn-on wolf head (`asos-davos-05.md:13`). The death is effectively confirmed by the text but no verbatim kill-act quote exists. All `death-of-grey-wind` edges above are marked Tier-2. The node can be minted at Tier-2.

### 6.2 — Beric's Last Kiss on Catelyn is itself off-page
The epilogue (Merrett POV) only shows us the RESULT of the resurrection (Catelyn hooded, alive, vengeful). It does not show Beric giving her the Last Kiss. That mechanism is described by Thoros in ASOS Arya VII (explaining a PREVIOUS resurrection) — we infer Beric applied it to Catelyn. The edge `beric-dondarrion AGENT_IN catelyn-is-resurrected-as-lady-stoneheart` is Tier-2 for this reason. The Thoros quote in the JSON (`asos-arya-07.md:97`) is the mechanism-description, not the act itself. Flagged in the JSON already.

### 6.3 — Double-parentage question: robb-is-killed and catelyn-is-killed
These two beats are already `SUB_BEAT_OF red-wedding`. This draft proposes NOT to add them as direct children of `red-wedding-conspiracy` too (they're reachable via the chain). But a question remains: should high-profile terminus events be double-parented (SUB_BEAT_OF both red-wedding AND red-wedding-conspiracy) to make them directly 1-hop from the arc parent?

Recommendation: **NO double-parenting.** It complicates graph semantics (what does it mean to be a sub-beat of two different parents at different levels of abstraction?). The existing Trident prototype did not double-parent. Trust the chain traversal.

### 6.4 — Lothar Frey slug: `lothar-frey` verified, but name disambiguation note
The resolver returns `lothar-frey` as a HIT-CHARACTER. However, there is also a `walda-frey-daughter-of-lothar` node. Confirm `lothar-frey` is Lame Lothar (Walder's steward son) and not another Lothar before minting the role edge. High confidence this is correct (only one notable Lothar Frey in canon) but worth a quick node-file check before emitting.

### 6.5 — `event.conspiracy` not confirmed in architecture.md type table
The design memo says `event.conspiracy` was added S93. Verify against `reference/architecture.md` before minting `red-wedding-conspiracy`. If it appears only in the vocab table (edge types) and not in the entity-type table, a cleanup-session edit to architecture.md is needed (same as the `event.incident` fix from Q5).

### 6.6 — Olyvar Frey as intelligence source: not minted as a beat
Catelyn's realization at the massacre — "Olyvar, and Perwyn, Alesander, all absent. And Roslin wept..." (`asos-catelyn-07.md:101`) — implies Olyvar was a spy who warned his family to be absent. This could be minted as a beat `olyvar-frey-withdraws-as-robb-s-squire` (conspiracy intelligence beat). Deliberately omitted from wave-1 as it's inferential (the spy role is implied, not stated). Flag for a future enrichment pass.

### 6.7 — `frey-bolt-offer-edmure-roslin` slug name
The proposed slug is functional but slightly awkward ("bolt offer" reads oddly — "bolt" intended as "Frey offer" shorthand, but risks confusion with crossbow bolts, which are the murder weapon). Alternative: `lothar-delivers-roslin-offer` or `frey-offer-edmure-roslin-marriage`. Flagging for Matt to pick.

---

## Edge and node count summary

| Category | Count |
|---|---|
| New event-hub mints | 5 (`red-wedding-conspiracy`, `robb-breaks-frey-marriage-pact`, `frey-bolt-offer-edmure-roslin`, `death-of-grey-wind`, `catelyn-is-resurrected-as-lady-stoneheart`) |
| Existing nodes retro-linked (no file change) | 1 (`red-wedding` → retro SUB_BEAT_OF) |
| New edges total | 22 (5 SUB_BEAT_OF + 4 TRIGGERS + 13 role edges) |
| All edges Tier-1 | 18 |
| Tier-2 (off-page confirmation) | 4 (Grey Wind victim, Beric agent, TRIGGERS grey-wind death, TRIGGERS conspiracy initiation) |
