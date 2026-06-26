# B4 Black-cells / Varys-visits-Ned — Proposal
Session S151 · 2026-06-26 · Lens: research+PROPOSE

---

## New nodes proposed

### `varys-visits-ned-in-the-black-cells`

| field | value |
|---|---|
| type | `event.incident` |
| slug | `varys-visits-ned-in-the-black-cells` |
| aliases | `Varys visits Ned in the black cells`, `Varys persuades Ned to confess`, `the gaoler visit to Eddard Stark` |
| confidence | tier-1 |
| book | agot |
| chapter | agot-eddard-15 |
| cite_ref | `sources/chapters/agot/agot-eddard-15.md:59-157` |
| gloss | Varys, disguised as the undergaoler Rugen, visits Eddard Stark in the Red Keep's black cells. He brings wine, delivers intelligence on Ned's daughters (Arya missing; Sansa betrothed to Joffrey and begging for Ned's life), and proposes the bargain: confess to treason publicly, command Robb to stand down, and the queen will let Ned take the black. He closes with an explicit threat — the next visitor could bring Sansa's head. This visit is the proximate cause of Ned's public confession. |

**Anchor quote (Varys's closing threat that clinches the MOTIVATES edge):**
> "The next visitor who calls on you could bring you bread and cheese and the milk of the poppy for your pain … or he could bring you Sansa's head. The choice, my dear lord Hand, is entirely yours."
— `sources/chapters/agot/agot-eddard-15.md:155-157`

**Anchor quote (Varys's disguise, establishing the event):**
> "The voice was strangely familiar, yet it took Ned Stark a moment to place it. 'Varys?' he said groggily when it came … Varys had transformed himself into a grizzled turnkey, reeking of sweat and sour wine."
— `sources/chapters/agot/agot-eddard-15.md:61`

**Anchor quote (the bargain — Wall + confession):**
> "I believe she will allow you to take the black and live out the rest of your days on the Wall, with your brother and that baseborn son of yours."
— `sources/chapters/agot/agot-eddard-15.md:135`

---

## Edges proposed

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter:line | verbatim_quote | note |
|---|---|---|---|---|---|---|---|---|
| E01 | varys | AGENT_IN | varys-visits-ned-in-the-black-cells | T1 | agot | agot-eddard-15.md:61 | "Varys had transformed himself into a grizzled turnkey, reeking of sweat and sour wine." | Varys is the active agent; disguise confirmed on-page |
| E02 | eddard-stark | VICTIM_IN | varys-visits-ned-in-the-black-cells | T1 | agot | agot-eddard-15.md:75 | "I trust you realize that you are a dead man, Lord Eddard?" | VICTIM_IN over PARTICIPATES_IN: Ned is the target of the persuasion, not a co-participant with agency. He does not seek the visit. |
| E03 | varys-visits-ned-in-the-black-cells | LOCATED_AT | black-cells | T1 | agot | agot-eddard-15.md:11 | "The dark was absolute." | `black-cells` node confirmed at `graph/nodes/locations/black-cells.node.md` |
| E04 | varys-visits-ned-in-the-black-cells | ENABLES | ned-confesses-to-treason | T1 | agot | agot-eddard-15.md:135–157 | "Tell the queen that you will confess your vile treason … I believe she will allow you to take the black … or he could bring you Sansa's head. The choice, my dear lord Hand, is entirely yours." | **MARQUEE fix.** ENABLES over CAUSES: Ned's choice remains formally free (Varys frames it as "entirely yours"), so ENABLES is the correct causal weight. This is the missing inbound causal edge for `ned-confesses-to-treason`. |
| E05 | varys | MANIPULATES | eddard-stark | T1 | agot | agot-eddard-15.md:135–157 | "Tell the queen that you will confess your vile treason … or he could bring you Sansa's head." | Qualifier: `via_threat`. Varys's closing ultimatum ("Sansa's head") is an explicit conditional threat. Distinct from the existing `varys DECEIVES eddard-stark` (T2) — that edge covers the Sansa-betrayal-of-Ned; this covers Varys's active coercion of Ned via threat. No dedup conflict. |
| E06 | varys | REVEALS_TO | eddard-stark | T2 | agot | agot-eddard-15.md:75 | "Your older girl is still betrothed to Joffrey. Cersei keeps her close. She came to court a few days ago to plead that you be spared." | Varys discloses Sansa's status and Arya's escape. Optional qualifier: `sansa-stark's-status-and-plea`. REVEALS_TO is distinct from DECEIVES (which is manipulation via falsehood) — this is factual intelligence on the daughters. T2 (wiki-anchored; the wiki explicitly notes Varys informs Ned of his daughters' fates). |
| E07 | varys-visits-ned-in-the-black-cells | MOTIVATES | eddard-stark | T1 | agot | agot-eddard-15.md:155–157 | "The next visitor who calls on you could bring you bread and cheese and the milk of the poppy for your pain … or he could bring you Sansa's head." | The visit's Sansa-threat is the lever MOTIVATES Ned to agree. This captures the mechanism (event→person) per the MOTIVATES edge direction spec. No conflict with existing `ned-discovers-the-truth-of-joffrey-s-parentage MOTIVATES eddard-stark` (that motivates the earlier warning to Cersei; this motivates the confession). |
| E08 | eddard-stark | IMPRISONED_AT | black-cells | T1 | agot | agot-eddard-15.md:11 | "The straw on the floor stank of urine. There was no window, no bed, not even a slop bucket … Once the door had slammed shut, he had seen no more. The dark was absolute." | No existing IMPRISONED_AT edge found for Ned in neighbor query. `black-cells` place node exists. IMPRISONED_AT is the canonical captivity-location edge per architecture.md. |

**Total: 8 edges, 1 new node.**

---

## Qualifier notes

**E05 — `varys MANIPULATES eddard-stark`:**
- Qualifier required (MANIPULATES is Tier-1 mandatory-qualifier).
- Proposed qualifier: **`via_threat`**.
- Rationale: The mechanism is an explicit conditional threat — "The next visitor … could bring you Sansa's head. The choice … is entirely yours." This is not flattery, bribery, seduction, or false information (the facts Varys states are substantially true). `via_threat` from the locked enum (`via_bribe` / `via_flattery` / `via_false_information` / `via_threat` / `via_seduction` / `unknown`) is the correct fit.
- Note on `via_false_information`: Varys does offer a false promise (that the queen will honor the Wall bargain — she does not), which would support `via_false_information` as an alternative or additional qualifier. However the closing sentence is an unambiguous threat that seals Ned's decision; `via_threat` is the primary mechanism. A synthesizer may choose to emit two MANIPULATES edges if the false-promise framing warrants separate treatment.

**E06 — `varys REVEALS_TO eddard-stark`:**
- Optional qualifier allowed (REVEALS_TO is Tier-2 optional).
- Proposed qualifier note (not a vocab enum): `daughters' status and Sansa's plea`.
- Architecture notes: "note what was revealed" — embed in the `notes` field rather than a fixed enum.

---

## Dedup skips

All checked against `baseline-intra.tsv`:

| skipped edge | reason |
|---|---|
| `varys DECEIVES eddard-stark` (T2) | EXISTS in baseline. E05 (MANIPULATES via_threat) is distinct — coercion via threat, not deception via falsehood. No conflict. |
| `varys BETRAYS eddard-stark` | EXISTS in baseline. E05 is not a duplicate — BETRAYS covers Varys's counsel to Cersei; MANIPULATES covers the active coercion of Ned. |
| `varys SWORN_TO eddard-stark` | EXISTS. Not proposed again. |
| `eddard-stark DISTRUSTS varys` | EXISTS. Not proposed again. |
| `ned-confesses-to-treason TRIGGERS execution-of-eddard-stark` | EXISTS. Not proposed again. |
| `ned-confesses-to-treason SUB_BEAT_OF execution-of-eddard-stark` | EXISTS. Not proposed again. |
| `eddard-stark AGENT_IN ned-confesses-to-treason` | EXISTS. Not proposed again. |
| `ned-discovers-the-truth-of-joffrey-s-parentage ENABLES arrest-of-eddard-stark` | EXISTS. The proposed E04 (`varys-visits-ned-in-the-black-cells ENABLES ned-confesses-to-treason`) is a DIFFERENT causal link (visit→confession, not parentage-discovery→arrest). No conflict. |

---

## NEW-TYPE-REQUEST

None. All edges use existing vocabulary types (`AGENT_IN`, `VICTIM_IN`, `LOCATED_AT`, `ENABLES`, `MANIPULATES`, `REVEALS_TO`, `MOTIVATES`, `IMPRISONED_AT`).

---

## Unresolved slugs

| slug | status |
|---|---|
| `black-cells` | RESOLVED — node exists at `graph/nodes/locations/black-cells.node.md` |
| `ned-confesses-to-treason` | RESOLVED — exists in baseline-intra.tsv |
| `varys` | RESOLVED — node exists in graph, 41 outgoing edges confirmed by neighbor query |
| `eddard-stark` | RESOLVED — node exists in graph |

No unresolved slugs.

---

## Evidence quality note

The chapter `agot-eddard-15.md` is the sole POV source for this event (Ned's POV). The visit, disguise, daughters' update, bargain terms, and Sansa-head threat are all T1 (explicit on-page). The `via_threat` qualifier is T1. The causal chain (visit → ENABLES confession) is T1 by direct narrative sequencing: this is the last scene before Ned's public confession, and Varys explicitly solicits the agreement.

The only T2 edge is E06 (REVEALS_TO), rated T2 because Varys's daughters-status disclosure is factual intelligence (wiki also records it), not a single verbatim performative speech act.
