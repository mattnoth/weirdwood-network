# Pass-1-Derived Extra Tables: Recall Headroom Report

> Generated: 2026-05-25T04:22:54+00:00  
> run_id: pass1-extra-tables-20260525  
> schema_version: pass1-extra-tables-v1  

This report answers: **how much recall headroom do the extra Pass 1 tables add**
beyond the existing Relationships Observed spine?

Sections: Hospitality & Guest Right | Dialogue of Note | Food & Drink | Events & Actions | Information Revealed

---

## 1. Hospitality & Guest Right

| Metric | Count |
|--------|-------|
| Rows seen (non-None tables) | 627 |
| None/empty tables | 83 |
| guest_right_invoked skipped | 26 |
| Violation rows flagged | 93 |
| VIOLATES_GUEST_RIGHT emitted (resolvable violator+victim) | 69 |
| VIOLATES_GUEST_RIGHT counted-only (unresolved) | 63 |
| Drop (unresolved host/guest) | 266 |
| Drop (self-edge) | 1 |
| **GUEST_OF edges emitted (deterministic, $0)** | **460** |
| of which qualifier=refused | 29 |

**GUEST_OF qualifier distribution:**

| Qualifier | Count |
|-----------|-------|
| shelter | 211 |
| feast | 121 |
| unknown | 39 |
| gift_exchange | 33 |
| refused | 29 |
| safe_conduct | 17 |
| bread_and_salt | 10 |

**VIOLATES_GUEST_RIGHT — notable emitted violations:**

| Chapter | Event | Violator (slug) | Victim (slug) |
|---------|-------|----------------|--------------|
| acok-arya-04 | Ser Amory demands entry | yoren | amory-lorch |
| acok-arya-09 | Prisoners promised honorable treatment | vargo-hoat | robett-glover |
| acok-arya-10 | Ser Hosteen's reference to Lannister captivity | tywin-lannister | hosteen-frey |
| acok-bran-05 | Bastard of Bolton's forced marriage | ramsay-snow | hornwood |
| acok-prologue | Cressen not summoned to feast | stannis-baratheon | cressen |
| acok-theon-04 | Theon's claim of gentle usage | theon-greyjoy | winterfell |
| acok-theon-06 | Beth Cassel used as hostage | theon-greyjoy | beth-cassel |
| acok-theon-06 | Ramsay admitted as ally | theon-greyjoy | ramsay-snow |
| acok-theon-06 | Ramsay admitted as ally | theon-greyjoy | dreadfort |
| acok-tyrion-15 | Cersei's "care" for Tyrion | cersei-lannister | tyrion-lannister |
| adwd-a-ghost-in-winterfell-01 | Red Wedding reference | house-frey | northmen |
| adwd-daenerys-02 | Hostage children from pyramids | daenerys-targaryen | children-of-the-forest |
| adwd-daenerys-07 | Wedding foot-washing | hizdahr-zo-loraq | daenerys-targaryen |
| adwd-davos-03 | Execution ordered | wyman-manderly | davos-seaworth |
| adwd-davos-04 | Red Wedding violation | walder-frey | wendel-manderly |
| adwd-davos-04 | Red Wedding violation | walder-frey | robb-stark |
| adwd-davos-04 | Red Wedding violation | walder-frey | others |
| adwd-jaime-01 | Red Wedding reference | walder-frey | lucas-blackwood |
| adwd-jaime-01 | Red Wedding reference | walder-frey | others |
| adwd-jon-04 | Mountain clan customs (discussed) | mountain-clans | stannis-baratheon |
| adwd-reek-01 | Ramsay's sarcastic reference to hospitality | ramsay-snow | reek |
| adwd-reek-01 | Ramsay's sarcastic reference to hospitality | ramsay-snow | kyra |
| adwd-reek-02 | Ramsay's safe conduct letter | ramsay-snow | ironborn |
| adwd-the-discarded-knight-01 | Yunkish kill Admiral Groleo | yunkai | groleo |
| adwd-the-spurned-suitor-01 | Tattered Prince offers food and drink | tattered-prince | quentyn-martell |
| adwd-the-spurned-suitor-01 | Tattered Prince offers food and drink | tattered-prince | gerris-drinkwater |
| adwd-the-spurned-suitor-01 | Tattered Prince offers food and drink | tattered-prince | archibald-yronwood |
| adwd-theon-01 | Freys/Manderlys as Bolton "guests" | roose-bolton | house-frey |
| adwd-tyrion-09 | Crew threatens to eat the pig | ship-playhouse | tyrion-lannister |
| adwd-tyrion-09 | Crew threatens to eat the pig | ship-playhouse | penny |
| affc-alayne-01 | Corbray draws sword at parley | petyr-baelish | lyn-corbray |
| affc-alayne-01 | Freys at the Twins | house-frey | catelyn-stark |
| affc-alayne-01 | Freys at the Twins | house-frey | robb-stark |
| affc-brienne-08 | Brotherhood rejects hospitality claim | brotherhood-without-banners | brienne-tarth |
| affc-brienne-08 | Brotherhood rejects hospitality claim | brotherhood-without-banners | podrick-payne |
| affc-brienne-08 | Brotherhood rejects hospitality claim | brotherhood-without-banners | hyle-hunt |
| affc-cersei-04 | Red Wedding referenced | walder-frey | robb-stark |
| affc-jaime-05 | Freys and the Red Wedding | house-frey | robb-stark |
| affc-jaime-06 | Red Wedding invocation | house-frey | robb-stark |
| affc-jaime-06 | Red Wedding invocation | house-frey | catelyn-stark |
| affc-jaime-06 | Marq Piper as "honored guest" | house-frey | marq-piper |
| affc-the-princess-in-the-tower-01 | Myrcella as Doran's ward | doran-martell | myrcella-baratheon |
| agot-arya-02 | Winterfell dining custom | eddard-stark | his-high-holiness |
| agot-catelyn-05 | Catelyn's arrest of Tyrion | catelyn-stark | tyrion-lannister |
| agot-catelyn-06 | Lysa demands immediate ascent | lysa-arryn | catelyn-stark |
| agot-catelyn-09 | Lord Walder boasts of hosting kings | walder-frey | three-sisters |
| agot-daenerys-05 | Drogo assigns Viserys to lowest place | drogo | viserys-targaryen |
| agot-daenerys-05 | Sacred city prohibition on blades | vaes-dothrak | all-for-joffrey |
| agot-daenerys-06 | Wine merchant offers a cask | wineseller | daenerys-targaryen |
| agot-tyrion-04 | Crossroads inn capture (flashback) | fat-walda-frey | tyrion-lannister |
| agot-tyrion-04 | Crossroads inn capture (flashback) | fat-walda-frey | catelyn-stark |
| agot-tyrion-06 | Tyrion invites clansmen to share fire and food | tyrion-lannister | stone-crows |
| asos-arya-09 | Hound cheats ferryman | bent-backed-man | sandor-clegane |
| asos-arya-11 | The Red Wedding massacre | walder-frey | robb-stark |
| asos-catelyn-03 | Murder of captive squires | robb-stark | tion-frey |
| asos-catelyn-03 | Murder of captive squires | robb-stark | willem-lannister |
| asos-catelyn-07 | Swordbelts hung on walls | walder-frey | all-for-joffrey |
| asos-catelyn-07 | The Red Wedding massacre | walder-frey | robb-stark |
| asos-catelyn-07 | The Red Wedding massacre | walder-frey | catelyn-stark |
| asos-davos-05 | Red Wedding (referenced) | walder-frey | robb-stark |
| asos-davos-05 | Red Wedding (referenced) | walder-frey | catelyn-stark |
| asos-epilogue | Ransom exchange (false pretense) | brotherhood-without-banners | merrett-frey |
| asos-jaime-05 | Bolton separates Jaime and Brienne | roose-bolton | brienne-tarth |
| asos-jon-01 | Bread and meat shared | mance-rayder | jon-snow |
| asos-samwell-02 | Murder of Craster | craster | nights-watch |
| asos-samwell-02 | Murder of Mormont | craster | nights-watch |
| asos-sansa-07 | Lysa threatens Sansa at the Moon Door | lysa-arryn | sansa-stark |
| asos-tyrion-06 | Red Wedding discussed | walder-frey | robb-stark |
| asos-tyrion-06 | Red Wedding discussed | walder-frey | catelyn-stark |

---

## 2. Dialogue of Note

| Metric | Count |
|--------|-------|
| Rows seen | 6,317 |
| Drop (group listener) | 278 |
| Drop (unresolved endpoint) | 1,617 |
| Drop (self-edge) | 0 |
| **Tail rows emitted (untyped, Speaker→Listener)** | **4,422** |
| Locator verbatim match | 4,416 (99.9%) |
| LLM cost if typed (S67 rate ≈ $0.0068/row) | $30.07 |

Edge type is NOT deterministic from the Dialogue table — the quote/context
is the hint for a future LLM tail step. All rows carry evidence_ref.

---

## 3. Food & Drink (Task 1 — entity-matched pairs)

| Metric | Count |
|--------|-------|
| Rows seen | 1,263 |
| Rows with >=2 named referents (heuristic) | 314 |
| Rows with >=2 resolved slugs | 447 |
| Rows dropped (<2 resolved) | 816 |
| **Candidate pairs emitted** | **620** |
| Locator verbatim match | 620 (100.0%) |

The Food & Drink table is medium-noise for edges. The 'Who Is Eating/Drinking'
column is the primary entity source; group cells (e.g. 'All guests') are
filtered by the resolver's GENERIC_TERMS stoplist.

**5 example rows (Who Is Eating/Drinking cell):**

- `[agot-arya-01]` Arya sat with "the little fat one" (Tommen); Sansa sat with Joffrey
- `[agot-arya-02]` Ned's household: Arya, Sansa, Septa Mordane, Jeyne Poole, Jory, Hullen, Desmond, Jacks, Harwin, Port
- `[agot-arya-02]` Arya, Septa Mordane, Ned (implied)
- `[agot-arya-03]` Robert Baratheon, Lord Tywin Lannister (the cat stole quail from Tywin's fingers)
- `[agot-arya-04]` No one eating — Arya is running through

---

## 4. Events & Actions (Task 1 — entity-matched pairs)

| Metric | Count |
|--------|-------|
| Numbered items corpus-wide | 8,384 |
| Items with >=2 resolved slugs | 7,128 |
| Items dropped (<2 resolved) | 1,256 |
| **Candidate pairs emitted** | **16,572** |
| Locator verbatim match | 16,401 (99.0%) |

Events & Actions is a numbered prose list with actor/action embedded in
free text. The >=2-entity filter is the primary noise cut. Direction heuristic:
first-resolved entity = actor/source; subsequent distinct entities = targets.

**5 representative examples:**

- `[agot-arya-01]` 1. **Arya struggles with needlework** — Arya's stitches are crooked; she compares her work unfavorably to Sansa's exquis
- `[agot-arya-01]` 2. **Girls discuss Prince Joffrey** — Sansa, Jeyne Poole, and Beth Cassel whisper about Joffrey, who told Sansa she was 
- `[agot-arya-01]` 3. **Arya quotes Jon about Joffrey** — Arya says Jon thinks Joffrey "looks like a girl." Sansa calls Jon a jealous basta
- `[agot-arya-01]` 4. **Septa Mordane inspects Arya's work** — The septa notices the disturbance, crosses the room, and publicly criticizes
- `[agot-arya-01]` 5. **Arya flees the sewing room** — Humiliated, with tears running down her cheeks, Arya makes a sarcastic excuse ("I ha

---

## 5. Information Revealed (Task 1 — entity-matched pairs)

| Metric | Count |
|--------|-------|
| Rows seen | 5,654 |
| Rows with >=2 resolved slugs | 3,701 |
| Rows dropped (<2 resolved) | 1,953 |
| **Candidate pairs emitted** | **5,162** |
| Locator verbatim match | 5,162 (100.0%) |

The 'Known To (Characters)' column is the primary entity source, combined
with the Information column. The edge direction is: first entity in reading
order → subsequent entities (actor = information holder or revealer).

**5 representative examples (How Revealed column):**

- `[agot-arya-01]` how=*Jeyne Poole whispers to Arya*
- `[agot-arya-01]` how=*Sansa's correction and Arya's internal thoughts*
- `[agot-arya-01]` how=*Arya's internal comparison*
- `[agot-arya-01]` how=*Jon explains to Arya*
- `[agot-arya-01]` how=*Jon points it out to Arya*

---

## Summary

| Table | Rows Seen | Deterministic Edges | Tail Rows (untyped) | Verbatim% |
|-------|-----------|--------------------:|--------------------:|----------:|
| Hospitality & Guest Right | 627 | 529 (GUEST_OF + VIOLATES) | — | 99.4% |
| Dialogue of Note | 6,317 | — | 4,422 | 99.9% |
| Food & Drink | 1,263 | — | 620 | 100.0% |
| Events & Actions | 8,384 | — | 16,572 | 99.0% |
| Information Revealed | 5,654 | — | 5,162 | 100.0% |

**Total new deterministic edges: 529** (GUEST_OF + VIOLATES_GUEST_RIGHT)
**Total new untyped tail rows: 26,776** (Dialogue 4,422 + Events 16,572 + Info 5,162 + Food 620)
**Tail LLM cost estimate (S67 rate $0.0068/row): $182.08**

All candidates carry `evidence_ref` (sources/chapters/{book}/{chapter}.md:LINE) + `locate_status`.

Output path: `working/wiki/pass2-buckets/pass1-derived/_extra-tables/{book}/`

---

> Generated by `scripts/stage4-pass1-extra-tables.py` on 2026-05-25T04:22:54+00:00
