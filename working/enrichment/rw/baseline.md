# Red Wedding enrichment dip — shared dedup BASELINE (S134)

> Every lens subagent reads this FIRST. It is the authoritative list of what ALREADY
> exists in the Red Wedding cluster. **Do NOT propose anything already here.** Propose
> only NET-NEW nodes/edges/attachments. Dedup-check every proposal against this file.

## The hub + spine (BUILT — do not re-propose)

- **`red-wedding`** (event.wedding) — the hub. 12 beats, 44 role edges, 17 participants.
  - OUT: `CAUSES roose-named-warden-of-the-north`; `PART_OF war-of-the-five-kings`; `PRECEDES purple-wedding`.
  - IN: `red-wedding-conspiracy CAUSES red-wedding`; `battle-near-yunkai PRECEDES`.
- **12 SUB_BEAT_OF `red-wedding` beats (BUILT):** `catelyn-secures-guest-right`, `the-wedding-feast-proceeds`,
  `lord-walder-calls-for-the-bedding`, `the-bedding-ceremony-begins`, `ser-wendel-manderly-is-killed`,
  `crossbows-kill-more-northmen`, `robin-flint-is-killed`, `ser-ryman-kills-dacey-mormont`, `robb-is-killed`,
  `catelyn-is-killed`, `the-camp-becomes-a-battlefield`, `red-wedding-revealed`.
- **`red-wedding-conspiracy`** (event.conspiracy) — BUILT. IN: `walder-frey COMMANDS_IN`, `tywin-lannister COMMANDS_IN`,
  `roose-bolton AGENT_IN`, `karstark-host-deserts-robb ENABLES`, `robb-weds-jeyne-westerling TRIGGERS`.
  OUT: `CAUSES red-wedding`, `CAUSES robb-is-killed`.
- **`red-wedding-revealed`** (event.ceremony) — BUILT, the KL reveal (ASOS Tyrion VI). Tywin/Walder/Roose COMMANDS_IN,
  house-frey/house-bolton AGENT_IN, robb/catelyn/edmure VICTIM_IN, LOCATED_AT kings-landing.

### Participant role edges already on the beats (BUILT — do not re-propose these dyads)
- `walder-frey` COMMANDS_IN (many beats) + `lord-walder-calls-for-the-bedding` AGENT_IN.
- `tywin-lannister` COMMANDS_IN red-wedding-revealed + red-wedding-conspiracy.
- `roose-bolton` COMMANDS_IN (crossbows + revealed) + AGENT_IN conspiracy + AGENT_IN robb-is-killed.
- `house-frey` / `house-bolton` AGENT_IN (multiple beats).
- `ryman-frey` AGENT_IN (feast + kills-dacey).
- VICTIM_IN: robb-stark, catelyn-stark, edmure-tully, roslin-frey, wendel-manderly, donnel-locke, owen-norrey,
  dacey-mormont, robin-flint, robb-stark, house-stark.
- `catelyn-stark` ATTENDS the-wedding-feast-proceeds + AGENT_IN catelyn-secures-guest-right.
- `jon-umber` (Greatjon) AGENT_IN the-bedding-ceremony-begins.

### Existing causal chain (BUILT)
```
capture-of-winterfell --CAUSES--> robb-receives-false-news-of-brans-death
  --TRIGGERS--> robb-weds-jeyne-westerling --TRIGGERS--> red-wedding-conspiracy
  --CAUSES--> red-wedding --CAUSES--> roose-named-warden-of-the-north
```
Also BUILT: `catelyn-is-killed CAUSES catelyn-rises-as-lady-stoneheart CAUSES brienne-brought-before-lady-stoneheart`.

---

## WHERE THE GAPS ARE (the enrichment seam)

**The hub is dense INSIDE but THIN on downstream consequence — only ONE downstream causal edge.**
The Red Wedding's vast aftermath is almost entirely un-wired. That is the prize.

### Existing nodes that are CAUSAL ISLANDS (lens-4 wiring targets — both endpoints already exist, no edge yet)
- **`wyman-manderly-stages-fake-execution-of-davos`** (event.deception) — 0 causal edges. The Manderly revenge for the
  Red Wedding (Wendel Manderly died there; "The North remembers"). Also `wyman-publicly-arrests-davos-at-white-harbor`,
  `wyman-publicly-orders-davos-execution`, `learning-about-manderly-s-hostage`, `wyman-manderly` (char), `house-manderly`.
  → Candidate: `red-wedding` (or `ser-wendel-manderly-is-killed`) MOTIVATES the Manderly revenge plot.
- **`roose-named-warden-of-the-north`** — 0 downstream. Should connect to the Bolton rule of the North (fArya wedding,
  Stannis's march — north container). Check those nodes exist before wiring.
- **`grey-wind-attacks`** (event.incident) — 0 causal edges, an island. Grey Wind (`grey-wind`, char) was killed and
  desecrated at the Red Wedding (head sewn onto Robb's body). Wire to the RW cluster.
- `catelyn-rises-as-lady-stoneheart` — already wired upstream to `catelyn-is-killed` (do NOT re-propose that edge).

### Likely-MISSING downstream/aftermath nodes (lens-1/lens-3 NEW-node candidates — VERIFY non-existence first)
- the Rains of Castamere played as the **massacre signal** (text `the-rains-of-castamere` EXISTS; no "plays" beat).
- Grey Wind killed / desecrated (head sewn on Robb) — likely no beat node.
- the Blackfish (Brynden Tully) escapes the Twins; Edmure taken hostage.
- the later **fall/siege of Riverrun** consequence; **Emmon Frey granted Riverrun**; Walder's rewards.
- the Freys become realm-wide pariahs ("guest right" broken) — the cultural/political fallout.
- Arya outside the walls (ASOS Arya XI — `the-camp-becomes-a-battlefield` exists; her trauma/kill-list response may not).

---

## SECONDARY CHARACTERS under-developed (lens-2)
- **Roslin Frey** (the weeping unwilling bride — Edmure's wife; she knew), **Lame Lothar Frey** & **Black Walder Frey**
  (the actual negotiators/planners — Lothar & Black Walder brokered it; `black-walder-frey` char EXISTS, Lothar?),
  **Dacey Mormont** (killed), **the Greatjon** (Jon Umber — captured, not killed; bites off Frey fingers),
  **Roose Bolton** (the leech-lord; "Jaime Lannister sends his regards"; the concealed-mail betrayal),
  **Walder Rivers / the bastard**, **Merrett Frey** (the ASOS Epilogue POV — `merrett-attempts-to-defend-his-innocence`
  exists). SUSPECTED_OF/WITNESS substrate: who SAW Robb die, who WITNESSED Catelyn's grief, etc.

## CHAPTER FILES (read these — line-check every quote you cite)
- `sources/chapters/asos/asos-catelyn-07.md` — **THE Red Wedding** (the slaughter, guest-right, the Rains signal, grey-wind).
- `sources/chapters/asos/asos-tyrion-06.md` — the KL reveal (Tywin's architecture, the coded Frey message).
- `sources/chapters/asos/asos-arya-11.md` — Arya outside the Twins (the camp battlefield, grey-wind's death seen).
- `sources/chapters/asos/asos-catelyn-03.md`, `asos-catelyn-02.md` — upstream (Karstark desertion, Jeyne, the broken Frey pact).
- `sources/chapters/asos/asos-epilogue.md` (Merrett Frey) — Lady Stoneheart's first appearance + the BWB hangings.
- ADWD Davos chapters (White Harbor) — the Manderly revenge / Frey-pies setup.
- `sources/chapters/affc/` Jaime chapters — Riverrun siege aftermath, the Blackfish.

## RULES FOR ALL LENSES
- **PROPOSE ONLY — mint nothing.** Output a structured proposal list; the orchestrator synthesizes + line-checks + mints.
- **Dedup against this file.** If it's listed above as BUILT, don't propose it.
- **Cite every claim with `chapter:line`** (book + file + line), and quote the verbatim line. The orchestrator re-checks
  every quote against the file before minting — bad cites get dropped.
- **NO CAUSES between sibling/sequence beats** (post-hoc ≠ causal; that's an "agency-collapse" reject). A beat in a
  sequence does not CAUSE the next beat just because it precedes it.
- **Tier discipline:** Tier-1 = proven canon w/ verbatim cite. `SUSPECTED_OF` (Tier-2, never Tier-1) for unproven agency.
  Theory READINGS are GATED (Frey-pies-as-Manderly-revenge is fair Tier-2 *substrate* if on-page; do not assert the theory).
