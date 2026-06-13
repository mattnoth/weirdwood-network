---
slug: wyman-manderly-stages-fake-execution-of-davos
type: event.deception
name: "Wyman Manderly stages the fake execution of Davos Seaworth"
aliases: ["the mummer's farce", "Manderly's fake execution of Davos", "the staged beheading at White Harbor", "Davos's official death", "Wyman's mummer's farce"]
status: minted-s93
minted_at: 2026-06-12T00:00:00+00:00
evidence_chapters:
  - ADWD Davos III
  - ADWD Davos IV
  - AFFC Cersei IV
---

# Wyman Manderly stages the fake execution of Davos Seaworth

Parent event for Wyman Manderly's covert operation to ransom his captive son Wylis from the Iron Throne by making Cersei's small council believe Davos Seaworth has been executed in White Harbor. Wyman calls it "the mummer's farce" (ADWD Davos IV) — a discrete, multi-beat deception staged inside the broader Grand Northern Conspiracy.

The deception has four canonical beats reified as sub-beat nodes:

1. **Public arrest** in the Merman's Court (ADWD Davos III) — `wyman-publicly-arrests-davos-at-white-harbor`. Theatrical, performed for Frey envoys.
2. **Public execution order** (ADWD Davos III) — `wyman-publicly-orders-davos-execution` (renamed S93 from `lord-wyman-orders-execution`). Wyman commands his cousin Ser Marlon Manderly to take Davos to the Wolf's Den, behead him, and return head and hands by supper with an onion in Davos's teeth.
3. **Substitute beheading** (ADWD Davos IV, reported) — `execution-of-davos-lookalike-at-white-harbor`. An unnamed criminal "who resembles Davos" is killed in Davos's place; head and hands are dipped in tar, fingers shortened by Ser Bartimus so the publicly-displayed remains pass for Davos. Davos himself goes to comfortable Wolf's Den captivity, then to Stannis as Wyman's envoy.
4. **Frey witnesses attest to small council** (AFFC Cersei IV) — `frey-witnesses-attest-davos-dead-at-small-council`. Members of House Frey testify that they have seen Davos's head; Cersei is deceived. In return, the Iron Throne returns Wylis Manderly from captivity at Maidenpool — the political payoff.

The deception is the structural pivot of Wyman's Grand Northern Conspiracy arc: it both protects Davos (so he can carry Wyman's terms to Stannis: Manderly fealty in exchange for Rickon Stark's return) and extracts Wylis from Lannister hands. Wyman's line — "the mummer's farce is almost done. My son is home." (ADWD Davos IV) — names the whole operation.

## Edges

Role edges, SUB_BEAT_OF beats, and the CONSPIRES_WITH alliance edge are emitted into `graph/edges/edges.jsonl` as part of the S93 restructure batch.

## Notes

Type `event.deception` is the new entity subtype added Session 93 (2026-06-12) — see `reference/architecture.md:118`. This node is the seed instance; canonical examples in that schema row include this arc plus Cersei's false-attack claim, Theon's burned-boys charade, and the "Arya Stark" (Jeyne Poole) substitution — each of which is a candidate for future event.deception promotion.
