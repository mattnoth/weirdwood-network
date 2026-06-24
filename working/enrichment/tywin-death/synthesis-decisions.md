# SYNTHESIS — Tywin's Death enrichment (S139, pass 1)

Opus orchestrator synthesis of 4 Sonnet lenses. **Every quote line-checked against the files.**

## The big line-check catch
Lenses 1 & 3 cited Shae's trial testimony / "my giant of Lannister" to **ch09:39** — WRONG.
Shae's testimony is in **ch10** (she's the "one final witness" brought "on the morrow", ch09:329).
- "my giant of Lannister" = **ch10:39** (testimony) and **ch11:205** (her dying echo) — NOT ch09.
- Tyrion's confession "I am guilty of being a dwarf" = **ch10:57**; trial-by-combat demand = **ch10:65**.
All other cites verified by grep against the source files before minting.

## MINT — 5 nodes
- `tywins-crossbow` (object.artifact) — the wall-hung crossbow Tyrion kills Tywin with (ch11:211/259/225)
- `hands-chain-of-office` (object.artifact) — the Hand's gold chain Tyrion strangles Shae with (ch11:197/209)
- `oberyn-spear` (object.artifact) — Oberyn's 8-ft ash spear, the venom vector (ch10:119/123/233)
- `shae-testifies-against-tyrion-at-trial` (event.incident) — Cersei's final witness; the betrayal (ch10:27-51)
- `varys-smuggles-tyrion-out-of-kings-landing` (event.incident) — the escape → exile (ch11:57/153)

## MINT — 37 edges (see mint script for full cites)
- **Objects (11):** crossbow WIELDED_IN/WIELDS/KILLED_WITH/OWNS · chain WIELDED_IN/WIELDS/KILLED_WITH · spear WIELDED_IN/WIELDS · oberyn POISONS gregor · manticore-venom WIELDED_IN
- **Causal seams (3):** `murder-of-elia... MOTIVATES oberyn-martell` (MARQUEE cross-arc) · `tywin DECEIVES tyrion` (by_lie, the Tysha lie) · `tyrion-kills-shae ENABLES assassination` (the crossbow detour)
- **Testimony node (5):** shae AGENT_IN · SUB_BEAT_OF trial · cersei COMMANDS_IN · CAUSES the killing · MOTIVATES tyrion
- **Escape node (4):** jaime-frees ENABLES smuggle · varys AGENT_IN · tyrion AGENT_IN · LOCATED_AT red-keep
- **Trial roles (3):** mace + oberyn PARTICIPATES_IN (judges) · cersei COMMANDS_IN
- **Combat roles (3):** oberyn + gregor FIGHTS_IN · ellaria WITNESS_IN (wails at the skull-crush, ch10:247)
- **Witness parade (8):** pycelle·varys·balon-swann·meryn-trant·boros-blount·osmund/osney/osfryd-kettleblack PARTICIPATES_IN trial

## REJECTED at synthesis (with reason)
- `tywin AGENT_IN/COMMANDS_IN jaime-reveals-the-truth-of-tysha` (L1 A6, L2 #13) — conflates the *lie's author* with the *reveal's agent*; Jaime reveals it AGAINST Tywin. Captured instead by `tywin DECEIVES tyrion`.
- `tywin MANIPULATES jaime` (L4 SEAM 10) — Jaime KNEW he was lying at Tywin's command; MANIPULATES = "unknowingly used." Command ≠ manipulation. Drop.
- `cersei MANIPULATES shae` (L1 A15) — Shae knew she lied ("the queen made me"); redundant with `cersei COMMANDS_IN shae-testifies`. Drop.
- `pycelle BETRAYS tyrion` / `varys BETRAYS tyrion` (L1 A18/A14) — Pycelle/Tyrion were never allies (enmity, not broken faith); Varys's "betrayal" is surface — he orchestrates the escape. `shae BETRAYS tyrion` already in graph ×2.
- `tysha VICTIM_IN jaime-reveals` (L2 #14) — she's the subject the truth is *about*, not the reveal's patient; stretch.
- `jaime-reveals MOTIVATES jaime` (L1 A5) — circular (event motivates its own agent).
- `cersei CAUSES tyrion-accused` (L1 A12) — she's AGENT_IN it; CAUSES is wrong slot.
- `shae DECEIVES trial` (L1 A17) — event target non-standard; covered by `shae BETRAYS` (exists).
- `oberyn AGENT_IN gregor-confesses` (L1 B1) — double-role muddle; FIGHTS_IN + VICTIM_IN suffice.
- Minor witness MINTS (ser-balon-swann etc.) — NOT needed; canonical slugs already exist.

## DEFERRED → pass-2 / harvest
- Tommen's accession node (between assassination and cersei-rearms) → Cersei-arc enrichment
- Jaime burns Cersei's letter (no node) → Jaime-arc enrichment
- `tyrion SEEKS tysha` already exists (adwd) — soft-complete via MOTIVATES route; no new edge
- the strangler poison node + Pycelle's full pharmacopoeia → medical/harvest
- `widows-wail` book-cite overlay (cuts the pie, ch08) → harvest
