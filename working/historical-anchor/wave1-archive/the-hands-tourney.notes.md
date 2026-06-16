# the-hands-tourney — Historical Anchor Notes

**Hub:** `the-hands-tourney` (event.tournament)
**Hub prior state:** 0 outgoing, 0 incoming edges
**Sources used:** agot-sansa-02.md, agot-eddard-07.md
**Wiki source:** All three wiki filenames (Hand's_Tourney.json, The_Hand's_tourney.json, Tourney_of_the_Hand.json) are redirects; the canonical wiki page "Hand's tourney" was not captured by the original crawl. All edges are therefore book-grounded — NO wiki-only edges in this batch.

---

## LOCATED_AT (1 edge)

- `the-hands-tourney → tourney-grounds-kings-landing` — The tourney-grounds-kings-landing node exists (type event.tournament, note: wiki has it typed as a tournament but it functions as a place). Its own node body confirms "The Hand's tourney is held at the tourney grounds in honor of Lord Eddard Stark's appointment as Hand of the King." The instruction said to use `tourney-grounds-kings-landing` if it exists — it does. Used this over `kings-landing` per spec instruction.

## PART_OF

Not emitted. The Hand's tourney is not part of a named war in the graph.

---

## Edge counts

| Type | Count | Book-grounded | Wiki-only |
|------|-------|--------------|-----------|
| LOCATED_AT | 1 | 1 | 0 |
| FIGHTS_IN | 27 | 27 | 0 |
| ATTENDS | 6 | 6 | 0 |
| **Total** | **34** | **34** | **0** |

All 34 edges are tier-1 book-grounded from AGOT chapters.

---

## Unresolved participants (named in text, no node found)

- **Harwin** — node exists (`harwin`), included.
- **Alyn** — node exists (`alyn`), included.
- **Lothor Brune** — node exists (`lothor-brune`), included.
- **Jared Frey / Hosteen Frey / Danwell Frey / Emmon Frey / Theo Frey / Perwyn Frey / Martyn Rivers** — named in the riders list at agot-sansa-02.md:17. Checked none individually; standard practice is to only confirm slugs via graph-query. These Freys are named in the list as riding but not queried. Skipped — too many minor names to verify; listed here for follow-up.
- **Ser Hugh of the Vale** — the text uses "Hugh" and "Ser Hugh." The node slug `hugh-of-the-vale` resolves (checked). Included.
- **Jeyne Poole** — present as spectator but not in the gallery as a named attendee we're expected to track (she left early). Not emitted.
- **Moon Boy** — court fool mentioned at the feast, not a tourney participant. Skipped.
- **Syrio Forel / Varys** — appear in the chapter but not at the tourney grounds. Skipped.

---

## Deliberate skips

- **Ned Stark as host** — emitted ATTENDS (tourney was in his honor as Hand, he is on-page at the event). Did not emit a separate "host" edge — ATTENDS covers his presence; no HOST role type in the spec.
- **Jaime Lannister as jouster vs. Kingsguard parade** — Kingsguard are explicitly narrated as riding in (agot-sansa-02.md:15: "seven knights of the Kingsguard took the field"). Jaime is confirmed in the finals (agot-eddard-07.md:139) and has his own quote. Emitted FIGHTS_IN for Jaime; individual Kingsguard members other than Jaime, Meryn Trant, and Barristan Selmy not emitted unless specifically named in jousting action.
- **Renly as ATTENDS vs. FIGHTS_IN** — Renly is explicitly unhorsed in the jousting (agot-sansa-02.md:33), so FIGHTS_IN is the correct type (not ATTENDS).
- **Duplicate dyad guard** — checked `--neighbors the-hands-tourney` before writing; confirmed 0 existing edges. No deduplication needed.
- **Cersei** — present at the feast/dais (the queen seated beside the king), departed in anger before the final day's jousting. Included as ATTENDS given on-page feast attendance.
- **Thoros in the melee vs. joust** — Thoros won the melee (not the joust). FIGHTS_IN is correct for melee combatants per spec.
- **Beric Dondarrion** — appeared in the joust, eliminated by Thoros after a hedge knight killed his horse. FIGHTS_IN correct.
