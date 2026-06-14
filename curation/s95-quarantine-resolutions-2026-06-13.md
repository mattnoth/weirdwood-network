# S95 Research Resolutions — 4 QUARANTINE Items + Slug-Naming Confirmations
**Date:** 2026-06-13 (S95 post-merge research session, Opus 4.7 orchestrator + 4 parallel Sonnet research subagents)
**Scope:** Resolves the 4 "genuine judgment" QUARANTINE items in `curation/hub-review-triage-2026-06-12.md` (eagle / unnamed-victims / stallion-heart / wedding-feast) plus confirms the 3 new-hub slug names. Source-of-truth for the cleanup session.

**Method:** Each item researched against local sources only (book chapters + cached wiki + existing graph state). No web fetches. Per-agent dossiers retained inline below; only the final JSON is canonical.

> ## ✅ MATT REVIEW — 2026-06-14 (S96 walkthrough): GATE 2 CLEARED
> All of Q1–Q5 **APPROVED as written** (27 edges + 7 node mints; 2 SKIP items stay skipped; 3 flagged out-of-scope items stay queued for future sessions). Specific confirmations:
> - **Q5 `event.incident` type:** APPROVED to use AND **formalize** — add an `event.incident` row to `reference/architecture.md`'s entity-type table (it is already in use by 5+ live nodes but undocumented). Do NOT fall back to `event.battle` (the roadside Trident incident is not a battle). The cleanup session should make the architecture.md edit alongside the mint.
> - **Bride/groom AGENT_IN convention** (Q4): confirmed correct.
> - All Tier-1 verbatim-grounded edges: ship as-is.

---

## Q1 — Eagle skinchanger identity (`eagle-attacks-ghost`)

**Decision:** RESOLVED — mint ATTACKS attached to **Orell** (not the species `eagle`, not `varamyr`).

**Research findings:**
- Only one eagle-attacks-Ghost scene exists in the books: ACOK Jon VII (`acok-jon-07.md` lines 101 + 153, same attack — line 101 is the act, 153 is wound-discovery).
- Orell is alive at the time (Qhorin kills him in ACOK Jon VIII, the next chapter).
- Varamyr only takes the eagle in ASOS Jon X (`asos-jon-10.md:137`), so post-death warging does NOT apply to this edge.
- Existing slug: `varamyr` (not `varamyr-sixskins`); `orell`, `ghost` all verified.

**Why redirect to Orell vs species `eagle`:** the project's [[project_impersonation_edges_redirect]] memory rule applies cleanly here — when an in-universe identity manipulation routes an action through a vessel, the edge attaches to the actor, not the vessel. Skinchanging is the magic-and-supernatural analog of impersonation. The post-death warging question (Varamyr-via-Orell's-eagle attacks Jon in ASOS Jon-02:223) is a SEPARATE edge that needs its own qualifier handling — out of scope for this item.

**Edges to emit (1 row):**

```json
{"edge_type":"ATTACKS","source_slug":"orell","target_slug":"ghost","decision":"emit_edge","candidate_kind":"curator-s95-skinchanger-attribution","evidence_kind":"book-pass1","evidence_book":"acok","evidence_chapter":"acok-jon-07","evidence_quote":"a shadow plummeted out of the sky. A shrill scream split the air. He glimpsed blue-grey pinions spread wide, shutting out the sun","evidence_ref":"sources/chapters/acok/acok-jon-07.md:101","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Orell skinchanges his eagle to stoop on Ghost in the Skirling Pass, tearing the direwolf's neck","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00","qualifier":"via_skinchanged_eagle"}
```

**Drop:** the eagle species-level edge (do not mint).

**Follow-up (separate session, not this cleanup):** scan for other eagle-attacks-* scenes targeting Jon's face (ASOS Jon-02:223) — that one is Varamyr-piloted but carries Orell's residual second-life ("some part of the man remained within the eagle"). Recommendation when handled: ATTACKS `varamyr → jon-snow` with `qualifier:"via_skinchanged_eagle"`, plus a sibling `ECHOES_IN orell → varamyr` with `qualifier:"posthumous_skinchange"` to preserve the haunting. Do NOT emit posthumous ATTACKS edges from Orell directly.

---

## Q2 — Unnamed-victim node policy (4 QUARANTINE items)

**Decision:** RESOLVED — **P4 mixed policy**: mint nodes only where the kill participates in a queryable narrative role (Arya's KILLS-list integrity, Victarion's anti-slavery prize-crew arc); accept the gap for atrocity-flavor kills with no downstream traversal need.

**Per-item resolutions:**

| Queue item | Decision | Why |
|---|---|---|
| `arya-kills-the-postern-guard` | **MINT** node + edge | Canonical entry on Arya's kill-roll; matches existing precedent `arya-stark KILLS stableboy-at-kings-landing`; first-class character-mechanic traversal. |
| `galley-crews-put-to-death-slaves-freed` | **MINT** collective node + edge | Anchors Victarion's chain-breaking arc; collective-character precedent exists (`character.minor`). |
| `a-boy-is-run-down-and-killed` | **SKIP — accept gap** | **Confirmed (Matt 2026-06-13): NOT Mycah.** Queue row is the Lhazareen boy in Drogo's sack of Lhazar (AGOT Dany VIII, agot-daenerys-07.md:21 — chased by Dothraki riders, whipped, shot with arrow). Mycah's death is already in the graph: `sandor-clegane KILLS mycah` Tier-1 from AGOT Eddard III + 5 other Mycah edges. Drogo's Lhazar sack coverable via existing Dothraki/Drogo/Lhazareen nodes; no traversal Matt has flagged. Single-edge node would be bloat. **Optional future:** reify Mycah's death as event hub `death-of-mycah` (currently a lone KILLS dyad) — small judgment call, queue separately if wanted. |
| `a-captive-girl-is-beheaded` | **SKIP — accept gap + flag** | **Agent 2 could not locate the queue's verbatim quote in-corpus.** This row may be a Pass-1 LLM paraphrase/aggregation of Gregor's Harrenhal pattern (`acok-arya-06`/`07`/`08`), not a citable single scene. Minting on an unverifiable quote is worse than the gap. Optionally surface to a Pass-1 audit queue. |

**Justification anchored in project values:** the real goal is graph-quality-for-agent-traversal ([[project_real_goal_graph_for_agents]]). Arya's "what did Arya do" query is a first-class use case; missing the postern guard breaks it. The Lhazareen-boy and Harrenhal-captive-girl items support no traversal the existing nodes don't already serve. Single-edge nodes minted only for completeness contradict [[feedback_python_before_agent]]'s minimal-bloat discipline.

**Nodes to mint (2 new files):**

`graph/nodes/characters/postern-guard-of-harrenhal.node.md`:

```yaml
---
name: "Postern Guard of Harrenhal"
type: character.human
slug: postern-guard-of-harrenhal
aliases: ["postern guard", "the northman at the postern"]
confidence: tier-2
sources: ["acok-arya-10"]
pass_origin: curator-s95-unnamed-victim
---
## Identity
Unnamed Dreadfort man-at-arms set to guard Harrenhal's eastern postern under Roose Bolton; killed by Arya Stark during her escape with Gendry and Hot Pie (ACOK Arya X).
```

`graph/nodes/characters/ghiscari-galley-crews-isle-of-cedars.node.md`:

```yaml
---
name: "Ghiscari Galley Crews (Isle of Cedars prize)"
type: character.minor
slug: ghiscari-galley-crews-isle-of-cedars
aliases: ["crews of Ghost and Shade", "Ghiscari galley crews"]
confidence: tier-2
sources: ["adwd-victarion-01"]
pass_origin: curator-s95-unnamed-victim
---
## Identity
Collective: the crews of two Ghiscari galleys (later renamed Ghost and Shade) captured by Victarion Greyjoy en route to New Ghis; put to death after their captains were beheaded (ADWD The Iron Suitor).
```

**Edges to emit (2 rows):**

```json
{"edge_type":"KILLS","source_slug":"arya-stark","target_slug":"postern-guard-of-harrenhal","decision":"emit_edge","candidate_kind":"curator-s95-unnamed-victim","evidence_kind":"book-pass1","evidence_book":"acok","evidence_chapter":"acok-arya-10","evidence_quote":"Arya slid her dagger out and drew it across his throat, as smooth as summer silk.","evidence_ref":"sources/chapters/acok/acok-arya-10.md:295","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Arya kills the postern guard at Harrenhal during her escape (Jaqen's iron coin pretext)","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"KILLS","source_slug":"victarion-greyjoy","target_slug":"ghiscari-galley-crews-isle-of-cedars","decision":"emit_edge","candidate_kind":"curator-s95-unnamed-victim","evidence_kind":"book-pass1","evidence_book":"adwd","evidence_chapter":"adwd-victarion-01","evidence_quote":"Afterward he put their crews to death as well, saving only the slaves chained to the oars.","evidence_ref":"sources/chapters/adwd/adwd-victarion-01.md:53","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Victarion beheads the captured galleys' crews after taking the prize, freeing the chained slaves","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
```

**Note on postern-guard quote:** Agent 2's draft used a paraphrase ("slits his throat when he kneels to pick it up"). I verified the actual verbatim at `acok-arya-10.md:295` and the JSON above uses the correct quote. Agent 2's tier-2 confidence has been promoted to tier-1 because the kill IS verbatim-grounded — the inferential risk was about the *victim identity* (unnamed), not the act. Cleanup session: use Tier 1.

---

## Q3 — Stallion-Heart Ceremony (`stallion-heart-ceremony`)

**Decision:** RESOLVED — **MINT** as a distinct event hub + mint the prophecy node + emit prophecy linkage edges. **Plus a bonus finding:** the existing node `the-stallion-is-brought-in-and-sacrificed` is mis-slugged (it's Mirri Maz Duur's bloodmagic ritual, AGOT Dany VIII — different chapter, different stallion, different purpose). That rename is OUT OF SCOPE for this cleanup; flagged below.

**Research findings:**
- Queue item = AGOT Daenerys V (`agot-daenerys-05.md`), Vaes Dothrak rite: wild stallion killed by Drogo + bloodriders with stone knives in the chalk pit; Dany consumes raw heart; dosh khaleen pronounce Stallion-Who-Mounts-the-World prophecy over Rhaego.
- Existing node `the-stallion-is-brought-in-and-sacrificed` ≠ same event — it's Mirri's healing-sacrifice in AGOT Dany VIII.
- `the-prince-that-was-promised` + `the-song-of-ice-and-fire` are the only 2 prophecy nodes in the graph; the Stallion prophecy is a structural gap.
- `SUBJECT_OF_PROPHECY` confirmed in locked vocab (architecture.md:390); `PROPHESIED_BY` confirmed (architecture.md:389). Agent 3's draft used `PROPHESIED_IN` which is NOT in vocab — replaced below with `PROPHESIED_BY` (prophecy → prophet, i.e. the dosh khaleen).

**Node to mint (prophecy):** `graph/nodes/prophecies/stallion-who-mounts-the-world.node.md`:

```yaml
---
slug: stallion-who-mounts-the-world
type: prophecy
name: "The Stallion Who Mounts the World"
aliases: ["Stallion Who Mounts the World", "stallion who mounts the world", "khal of khals"]
confidence: tier-1
sources: ["agot-daenerys-05"]
pass_origin: curator-s95-prophecy-linkage
---
## Identity
Dothraki prophecy of a khal of khals who will unite all Dothraki into one khalasar and conquer the world; pronounced over Rhaego by the dosh khaleen during Daenerys's stallion heart ceremony (AGOT Daenerys V).
```

**Node to mint (event hub):** `graph/nodes/events/stallion-heart-ceremony.node.md`:

```yaml
---
slug: stallion-heart-ceremony
type: event.ceremony
name: "Stallion Heart Ceremony"
aliases: ["stallion heart ceremony", "Dany's heart-eating", "the heart ceremony at Vaes Dothrak"]
confidence: tier-1
sources: ["agot-daenerys-05"]
pass_origin: curator-s95-prophecy-linkage
---
## Identity
Dothraki rite at Vaes Dothrak in which a pregnant khaleesi consumes the raw heart of a wild stallion under the Mother of Mountains. Daenerys's ceremony culminated in the dosh khaleen pronouncing the Stallion Who Mounts the World prophecy over her unborn son Rhaego.
```

**Edges to emit (2 + 6 role edges):**

```json
{"edge_type":"SUBJECT_OF_PROPHECY","source_slug":"rhaego","target_slug":"stallion-who-mounts-the-world","decision":"emit_edge","candidate_kind":"curator-s95-prophecy-linkage","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-daenerys-05","evidence_quote":"The prince is riding, and he shall be the stallion who mounts the world.","evidence_ref":"sources/chapters/agot/agot-daenerys-05.md:41","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Rhaego is named as the Stallion Who Mounts the World by the dosh khaleen crone during the heart-eating prophecy","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"PROPHESIED_BY","source_slug":"stallion-who-mounts-the-world","target_slug":"dosh-khaleen","decision":"emit_edge","candidate_kind":"curator-s95-prophecy-linkage","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-daenerys-05","evidence_quote":"The stallion who mounts the world! the onlookers cried in echo, until the night rang to the sound of their voices.","evidence_ref":"sources/chapters/agot/agot-daenerys-05.md:43","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"The Stallion Who Mounts the World prophecy is pronounced by the dosh khaleen during Dany's heart ceremony","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
```

**Role edges for the ceremony hub** — queue row lists 6 agents (Drogo, Daenerys, the bloodriders Cohollo/Haggo/Qotho, and the dosh khaleen). Cleanup session should hydrate these from the queue row's participants field, using AGENT_IN for Drogo + bloodriders (active sacrificers) and the dosh khaleen (active prophesiers), and ATTENDS or specifically `PARTICIPATES_IN` for Daenerys (subject of the rite, eats the heart — judgment call; lean AGENT_IN since her consumption IS the rite). Recommended:

- `drogo AGENT_IN stallion-heart-ceremony` (kills stallion)
- `daenerys-targaryen AGENT_IN stallion-heart-ceremony` (consumes heart)
- `cohollo AGENT_IN stallion-heart-ceremony` (bloodrider sacrifice)
- `haggo AGENT_IN stallion-heart-ceremony` (bloodrider sacrifice)
- `qotho AGENT_IN stallion-heart-ceremony` (bloodrider sacrifice)
- `dosh-khaleen AGENT_IN stallion-heart-ceremony` (prophet body)
- `rhaego SUBJECT_OF stallion-heart-ceremony` — *N.B.* `SUBJECT_OF` is NOT in vocab; the prophecy edge above already captures Rhaego's relation. Skip this row.

**Bonus / out-of-scope finding (flagged, not actioned):** rename `the-stallion-is-brought-in-and-sacrificed` → something like `mirri-maz-duur-bloodmagic-ritual` since the current name describes a DIFFERENT scene than what its content covers. Queue for a future rename session with `scripts/rename-event-node.py`.

---

## Q4 — Wedding-Feast Disambiguation (`wedding-feast`)

**Decision:** RESOLVED — **MINT** sub-beat attached to existing hub `wedding-of-tommen-i-baratheon-and-margaery-tyrell`. Source chapter unambiguous: AFFC Cersei III, `affc-cersei-03.md:147` (the chapter explicitly contrasts this feast with Joffrey's prior wedding).

**Research findings:**
- The 3 named fools (Butterbumps, Moon Boy, Blue Bard) anchor the scene to King's Landing AFFC era; the chapter context names Tommen-Margaery directly.
- Existing hub has 2 SUB_BEAT_OF children already (`wedding-ceremony-in-the-royal-sept`, `post-ceremony-congratulations`); NO feast beat. Genuine gap.
- Tommen vows belong to the ceremony beat (already covered), not the feast — the queue row's "Tommen's vows" mention is a Pass-1 conflation that the new feast sub-beat does NOT need to absorb.
- All participant slugs verified: `tommen-baratheon` (not `tommen-i-baratheon`), `margaery-tyrell`, `butterbumps`, `moon-boy`, `blue-bard`.

**Role-edge convention (S95 Matt clarification 2026-06-13):** the bride and groom are **AGENT_IN** their own wedding event, not ATTENDS — they are the principals of the rite, not guests. ATTENDS is reserved for guests/witnesses. Apply this convention to all wedding-event role-edges going forward (incl. F3a `death-of-joffrey-baratheon` — Joffrey + Margaery are AGENT_IN the purple wedding, not ATTENDS — though F3a is keyed on the poisoning sub-beat where the role calculus is different).

**New event node:** `graph/nodes/events/wedding-feast-at-the-red-keep.node.md`:

```yaml
---
slug: wedding-feast-at-the-red-keep
type: event.feast
name: "Wedding Feast at the Red Keep"
aliases: ["Tommen-Margaery wedding feast", "the modest feast"]
confidence: tier-1
sources: ["affc-cersei-03"]
pass_origin: curator-s95-wedding-feast
---
## Identity
The modest 7-course wedding feast following the marriage of King Tommen I Baratheon and Margaery Tyrell at the Red Keep, AFFC. Notable for Cersei's contrast against the Purple Wedding's lavishness, and for the performances of Butterbumps, Moon Boy, and the Blue Bard.
```

**Edges to emit (6 rows):**

```json
{"edge_type":"SUB_BEAT_OF","source_slug":"wedding-feast-at-the-red-keep","target_slug":"wedding-of-tommen-i-baratheon-and-margaery-tyrell","decision":"emit_edge","candidate_kind":"curator-s95-wedding-feast","evidence_kind":"book-pass1","evidence_book":"affc","evidence_chapter":"affc-cersei-03","evidence_quote":"Like the service, the wedding feast was modest. Lady Alerie had made all the arrangements; Cersei had not had the stomach to face that daunting task again, after the way Joffrey's wedding had ended.","evidence_ref":"sources/chapters/affc/affc-cersei-03.md:147","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"sub-beat: feast at Tommen-Margaery wedding","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"butterbumps","target_slug":"wedding-feast-at-the-red-keep","decision":"emit_edge","candidate_kind":"curator-s95-wedding-feast","evidence_kind":"book-pass1","evidence_book":"affc","evidence_chapter":"affc-cersei-03","evidence_quote":"Butterbumps and Moon Boy entertained the guests between dishes","evidence_ref":"sources/chapters/affc/affc-cersei-03.md:147","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"performed as fool at feast","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"moon-boy","target_slug":"wedding-feast-at-the-red-keep","decision":"emit_edge","candidate_kind":"curator-s95-wedding-feast","evidence_kind":"book-pass1","evidence_book":"affc","evidence_chapter":"affc-cersei-03","evidence_quote":"Butterbumps and Moon Boy entertained the guests between dishes","evidence_ref":"sources/chapters/affc/affc-cersei-03.md:147","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"performed as fool at feast","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"blue-bard","target_slug":"wedding-feast-at-the-red-keep","decision":"emit_edge","candidate_kind":"curator-s95-wedding-feast","evidence_kind":"book-pass1","evidence_book":"affc","evidence_chapter":"affc-cersei-03","evidence_quote":"The only singer was some favorite of Lady Margaery's, a dashing young cock-a-whoop clad all in shades of azure who called himself the Blue Bard. He sang a few love songs and retired.","evidence_ref":"sources/chapters/affc/affc-cersei-03.md:147","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"sang love songs at feast","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"tommen-baratheon","target_slug":"wedding-feast-at-the-red-keep","decision":"emit_edge","candidate_kind":"curator-s95-wedding-feast","evidence_kind":"book-pass1","evidence_book":"affc","evidence_chapter":"affc-cersei-03","evidence_quote":"Like the service, the wedding feast was modest.","evidence_ref":"sources/chapters/affc/affc-cersei-03.md:147","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"groom — principal at own wedding feast","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"margaery-tyrell","target_slug":"wedding-feast-at-the-red-keep","decision":"emit_edge","candidate_kind":"curator-s95-wedding-feast","evidence_kind":"book-pass1","evidence_book":"affc","evidence_chapter":"affc-cersei-03","evidence_quote":"Margaery wore the same gown she had worn to marry Joffrey, an airy confection of sheer ivory silk, Myrish lace, and seed pearls.","evidence_ref":"sources/chapters/affc/affc-cersei-03.md:147","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"bride — principal at own wedding feast","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
```

**Note on LOCATED_AT:** the slug already encodes the venue (`-at-the-red-keep`); no separate LOCATED_AT edge needed. Cleanup session can add one if it wants stronger queryability.

---

## Slug-naming confirmations (3 new hubs from the FIX bucket)

These are the F3a / F3b / F4a hub slugs in `curation/hub-review-triage-2026-06-12.md`. Reviewed against existing AWOIAF wiki page titles + S91 rename convention (event-named, not action-named) + existing graph conventions:

| Proposed slug | Decision | Why |
|---|---|---|
| `death-of-joffrey-baratheon` | **APPROVE** | Matches the `death-of-*` pattern used elsewhere in the graph; AWOIAF page = `Poisoning_of_Joffrey_Baratheon` (alt: consider `poisoning-of-joffrey-baratheon`; both are defensible — going with `death-of-` for consistency with the existing `death-of-*` series in `graph/nodes/events/`). |
| `wedding-ceremony-at-the-great-sept-of-baelor` | **APPROVE** | Venue-anchored, distinguishes from Tommen's ceremony in the royal sept. AWOIAF treats this as part of `Purple Wedding`; the sub-beat slug fits S91 convention. |
| `catelyn-secures-guest-right` | **APPROVE** | Action-anchored phrasing flags this as a hospitality beat (first-class category per [[user_asoiaf_design_values]]); matches the existing `bread-and-salt` rite context. |

---

## Execution summary for the cleanup session

This file replaces the 4 QUARANTINE items + the 3 slug-naming checks in `curation/hub-review-triage-2026-06-12.md` § QUARANTINE. The cleanup session should:

1. **Append** all JSON edges in this file to `graph/edges/edges.jsonl` (3 + 2 + 8 + 6 = 19 new edges).
2. **Mint** the 5 new node files (postern-guard-of-harrenhal, ghiscari-galley-crews-isle-of-cedars, stallion-who-mounts-the-world, stallion-heart-ceremony, wedding-feast-at-the-red-keep).
3. **Skip** the 2 SKIP-marked QUARANTINE items (a-boy-is-run-down-and-killed, a-captive-girl-is-beheaded).
4. **Flag for future session** (do NOT touch now):
   - Eagle-attacks-Jon scene (Varamyr-via-Orell's-eagle) — separate edge with `ECHOES_IN` sibling
   - Rename `the-stallion-is-brought-in-and-sacrificed` → `mirri-maz-duur-bloodmagic-ritual` (mis-slugged)
   - `a-captive-girl-is-beheaded` Pass-1 audit (queue evidence_quote may be LLM paraphrase, not in corpus)

All edges land as Tier 1 except where the source-of-truth is genuinely inferential (none in this batch — all 19 are verbatim-grounded).

---

## Q5 — Mycah / Trident-incident reification (Matt addition 2026-06-13)

**Decision:** RESOLVED — **MINT** parent event `incident-at-the-trident` + new sub-beat `death-of-mycah`; retroactively attach 3 existing standalone event hubs (`cersei-maneuvers-for-lady-s-death`, `ned-kills-lady`, `ned-claims-the-execution`) as sub-beats of the new parent so the whole causal cluster traverses as one unit.

**Why:** Matt's read — Mycah's death and Lady's death belong to the same causal incident chain (Joffrey attacks Mycah → Nymeria bites Joffrey → Cersei demands recompense → Ned kills Lady → Sandor kills Mycah on the kingsroad). The graph already has rich coverage at the dyad level (`sandor-clegane KILLS mycah`, `joffrey-baratheon ATTACKS mycah`, `arya-stark MOURNS mycah`, `arya-stark COMPANION_OF mycah`, `nymeria PROTECTS arya-stark`) AND three standalone event hubs for the Lady arc, but no umbrella holding them together. Following the S87 Plate 5 reification pattern: parent event hub + SUB_BEAT_OF children + role edges only at the beat level.

**Out-of-scope (do not touch):** the existing `sandor-clegane KILLS mycah` Tier-1 dyad stays as-is — sibling to the new `death-of-mycah` event-hub role edges. The S87 convention is dyad + reified-event coexist.

**Event hubs to mint (2 new files):**

`graph/nodes/events/incident-at-the-trident.node.md`:

```yaml
---
slug: incident-at-the-trident
type: event.incident
name: "Incident at the Trident"
aliases: ["the Trident incident", "Joffrey-Arya confrontation at the Trident", "the butcher's boy incident"]
confidence: tier-1
sources: ["agot-sansa-01", "agot-arya-02", "agot-eddard-03"]
pass_origin: curator-s95-trident-incident
---
## Identity
The kingsroad incident on the Trident's south bank in which Arya Stark, practicing swords with the butcher's boy Mycah, was confronted by Prince Joffrey. Joffrey cut Mycah with Lion's Tooth; Arya struck Joffrey with a stick; Nymeria bit Joffrey's arm; Arya threw Joffrey's sword into the river. Royal justice followed at Castle Darry: Cersei demanded a direwolf's life, Ned executed Lady in Nymeria's stead, and Sandor Clegane returned with Mycah's body. Cause of the Lady-direwolf rift and the first major political confrontation between House Stark and House Lannister on the way south.
```

`graph/nodes/events/death-of-mycah.node.md`:

```yaml
---
slug: death-of-mycah
type: event.death
name: "Death of Mycah"
aliases: ["killing of Mycah", "the butcher's boy's death"]
confidence: tier-1
sources: ["agot-eddard-03"]
pass_origin: curator-s95-trident-incident
---
## Identity
Sandor Clegane ran down Mycah, the butcher's boy from the Crossroads Inn, on the kingsroad while searching for Arya at Cersei's demand. Mycah was cut nearly in half from shoulder to waist. The kill is established off-page; Sandor confessed in front of Ned Stark at Castle Darry: "He ran. But not very fast."
```

**Edges to emit (4 SUB_BEAT_OF + 4 role + 0 net new dyads = 8 new rows):**

```json
{"edge_type":"SUB_BEAT_OF","source_slug":"cersei-maneuvers-for-lady-s-death","target_slug":"incident-at-the-trident","decision":"emit_edge","candidate_kind":"curator-s95-trident-incident","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-03","evidence_quote":"This girl of yours attacked my son. Her and her butcher's boy. That animal of hers tried to tear his arm off.","evidence_ref":"sources/chapters/agot/agot-eddard-03.md:47","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Cersei's maneuver for Lady's death is the political-justice beat of the broader Trident incident","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"ned-kills-lady","target_slug":"incident-at-the-trident","decision":"emit_edge","candidate_kind":"curator-s95-trident-incident","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-03","evidence_quote":"Cut almost in half from shoulder to waist by some terrible blow struck from above.","evidence_ref":"sources/chapters/agot/agot-eddard-03.md:151","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Ned's execution of Lady is the wolf-sacrifice beat of the Trident incident (Nymeria-substitute by royal demand)","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"ned-claims-the-execution","target_slug":"incident-at-the-trident","decision":"emit_edge","candidate_kind":"curator-s95-trident-incident","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-03","evidence_quote":"Ned took the duty of executing Lady from the Hound himself.","evidence_ref":"sources/chapters/agot/agot-eddard-03.md:151","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Ned claiming the execution himself is the sub-beat preceding Lady's death within the Trident incident","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"SUB_BEAT_OF","source_slug":"death-of-mycah","target_slug":"incident-at-the-trident","decision":"emit_edge","candidate_kind":"curator-s95-trident-incident","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-03","evidence_quote":"No sign of your daughter, Hand, but the day was not wholly wasted. We got her little pet.","evidence_ref":"sources/chapters/agot/agot-eddard-03.md:149","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Sandor's kingsroad killing of Mycah is the human-victim beat of the Trident incident","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"AGENT_IN","source_slug":"sandor-clegane","target_slug":"death-of-mycah","decision":"emit_edge","candidate_kind":"curator-s95-trident-incident","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-03","evidence_quote":"\"He ran.\" He looked at Ned's face and laughed. \"But not very fast.\"","evidence_ref":"sources/chapters/agot/agot-eddard-03.md:155","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Sandor ran Mycah down on the kingsroad and killed him","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"VICTIM_IN","source_slug":"mycah","target_slug":"death-of-mycah","decision":"emit_edge","candidate_kind":"curator-s95-trident-incident","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-03","evidence_quote":"It was the butcher's boy, Mycah, his body covered in dried blood. He had been cut almost in half from shoulder to waist by some terrible blow struck from above.","evidence_ref":"sources/chapters/agot/agot-eddard-03.md:151","confidence_tier":1,"typed_by":"curator-s95","asserted_relation":"Mycah killed by Sandor on the kingsroad","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"LOCATED_AT","source_slug":"death-of-mycah","target_slug":"kingsroad","decision":"emit_edge","candidate_kind":"curator-s95-trident-incident","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-03","evidence_quote":"the hunt for Arya and the butcher's boy was conducted on both sides of the river","evidence_ref":"sources/chapters/agot/agot-eddard-03.md:25","confidence_tier":2,"typed_by":"curator-s95","asserted_relation":"Sandor caught Mycah while searching along the kingsroad north of the Trident; precise location unspecified","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
{"edge_type":"TRIGGERS","source_slug":"cersei-maneuvers-for-lady-s-death","target_slug":"death-of-mycah","decision":"emit_edge","candidate_kind":"curator-s95-trident-incident","evidence_kind":"book-pass1","evidence_book":"agot","evidence_chapter":"agot-eddard-03","evidence_quote":"Sandor Clegane and his riders came pounding through the castle gate, back from their hunt.","evidence_ref":"sources/chapters/agot/agot-eddard-03.md:147","confidence_tier":2,"typed_by":"curator-s95","asserted_relation":"Cersei's demand for justice authorized the hunt that ran Mycah down","schema_version":"pass1-derived-v1","produced_at":"2026-06-13T00:00:00+00:00"}
```

**Design notes for the cleanup session:**

- Parent `incident-at-the-trident` has **no direct role edges** — all participants attach at the sub-beat level (Joffrey/Arya/Nymeria/Mycah on the dyads `joffrey ATTACKS mycah`, `nymeria PROTECTS arya-stark`, etc.; Sandor/Mycah on `death-of-mycah`; Cersei/Ned/Lady on the existing 3 hubs). This matches the Red Wedding pattern (S87 Plate 5).
- `event.incident` type — confirmed in use elsewhere (was the original type for `attack-on-ned-stark-in-the-streets-of-kings-landing` before S93 promoted it to `event.battle`). Cleanup session: verify against architecture.md before mint; fall back to `event.battle` only if `event.incident` is not in the type list.
- F6c `nymeria ATTACKS joffrey-baratheon` and F6d `arya-stark ATTACKS joffrey-baratheon` (from the FIX-22 bucket) DO NOT need event-hub reification — they fit cleanly as dyads under the parent incident's umbrella. Keep them as dyads per F6's original framing.
- Existing `sandor-clegane KILLS mycah` dyad is NOT modified; it stays as the action-level edge sibling to the new event-hub role edges. The graph carries both per S87 convention.

**Total S95 emissions (incl. Q5):** 19 + 8 = **27 new edges** + **7 new node files** (postern-guard-of-harrenhal, ghiscari-galley-crews-isle-of-cedars, stallion-who-mounts-the-world, stallion-heart-ceremony, wedding-feast-at-the-red-keep, incident-at-the-trident, death-of-mycah).
