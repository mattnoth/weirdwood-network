# Hub-Review Queue Triage — 2026-06-12

**What this is:** Proposal-only triage of the 109-item Plate 3 hub-review queue, plus the 4 wrong-direction role-edge items S89 added. **Nothing here has been applied to the graph.** Every FIX is a proposed action awaiting Matt's approval.

> ## ✅ MATT REVIEW — 2026-06-14 (S96 walkthrough): GATE 2 CLEARED
> All FIX-22 items **APPROVED as proposed**, with these specific decisions/amendments:
> - **F3a (death-of-joffrey-baratheon):** `olenna-tyrell AGENT_IN` at **tier 2** (book-canon by inference + Littlefinger's ASOS Sansa VI reveal, NOT on-page — show-only confession does not apply). **ADD `petyr-baelish COMMANDS_IN death-of-joffrey-baratheon`** (tier 2, architect/orderer role) carrying Littlefinger's reveal quote as `evidence_quote`: *"someone told you that your hair net was crooked and straightened it for you… Lady Olenna was not about to let Joff harm her precious darling granddaughter"* — `evidence_ref: sources/chapters/asos/asos-sansa-06.md:183` (also see :145, :193). **ALSO add a `## Quotes` block** to the death-of-joffrey-baratheon node with the hairnet/missing-stone passage (asos-sansa-05:23) + Littlefinger's reveal (asos-sansa-06:145/183/193). *(Per new firm rule [[feedback_capture_quotes_during_research]] — capture the marquee dialogue so "who really poisoned Joffrey?" pulls Littlefinger's words straight from the graph.)*
> - **F5 (Tyrion false confession):** CONFIRMED — demote `tyrion-lannister POISONS joffrey-baratheon` tier-1 → **tier-4** + `false-confession` qualifier. Execute together with F3a (no gap).
> - **F6h (Quentyn's death):** RESOLVED — **not** ambiguous. Emit `rhaegal KILLS quentyn-martell` (qualifier: dragonfire), **tier 2**, evidence_quote: *"Rhaegal, he reminded himself, the green one is Rhaegal. When he raised his whip, he saw that the lash was burning. His hand as well. All of him, all of him was burning."* — `evidence_ref: sources/chapters/adwd/adwd-the-dragontamer-01.md:265`. (Verified S96: Quentyn reaches for Viserion; Rhaegal torches him from behind. Tier 2 because flame-source is by-sequence, not a clean SVO sentence.)
> - **F1/F2/F4/F6 (rest):** ship all as proposed, all verbatim-cited.
> - **QUARANTINE:** governed by `s95-quarantine-resolutions-2026-06-13.md` (5 resolved, 2 SKIP, 3 Track-B). No change here.

**Where the queue lives:**
- `working/edge-modeling/plate3-full/hub-review-queue.jsonl` — 109 rows (75 borderline-single-agent, 32 non-harming-multi-agent, 2 fuzzy-match duplicate rows for one event)
- Human-readable companion: `working/edge-modeling/plate3-full/HUB-REVIEW-TRIAGE-LIST.md`
- S89 additions: `working/session-results/2026-06-09-graph-validation.md` (routing summary, follow-up #3) — 4 wrong-direction role edges, all confirmed live in `graph/edges/edges.jsonl`

**What the queue items are:** Plate 3 events where the LLM said `is_nary=true` but the emitted role structure was effectively a clean dyad (borderline-single-agent), or multi-agent with no harm structure (non-harming), or where the resolver fuzzy-matched an existing event node instead of classifying (fuzzy-match). Per D8 ("reify on n-ary STRUCTURE, not event TYPE"), clean dyads should not get hubs. **Q1=a at Plate 5 (S87)** applied the defaults: 0 of 109 minted, and the staged role edges for the 2 fuzzy-match rows were dropped (5 of 6 — see FIX-1).

**Triage method:** Every verdict below was checked against the live graph where it changes the answer — `graph/edges/edges.jsonl` dyad lookups and `graph/nodes/` slug existence. The D8 default (KEEP-DYAD, don't mint) is only *correct* when the direct dyad actually exists in the spine. For 14 canon-significant acts it does not — those are the core of the FIX bucket.

**Staleness check:** S87–S91 work (rename execution, alias resolver, event-participants) did NOT touch any queue item. The queue is fully un-actioned. One Plate 5 leak found (FIX-1c): a role edge sourced from the never-minted `siege-of-storm-s-end-recalled` is live and dangling.

## Bucket counts

| Bucket | Queue rows | S89 items | Total |
|---|---|---|---|
| FIX | 18 (17 actions; fuzzy pair = 1) | 4 | 22 |
| QUARANTINE | 10 | 0 | 10 |
| KEEP-AS-IS | 81 | 0 | 81 |
| **Total** | **109** | **4** | **113** |

---

## FIX (22 items — exact proposed actions)

### F1. Fuzzy-match pair + Plate 5 leak — `siege-of-storm-s-end-recalled` (2 queue rows) — **[scriptable]** [EXECUTED 2026-06-14]

The 2 fuzzy rows are duplicates of one event, matched to existing node `siege-of-storms-end-299` (score 0.833 — the match is correct; same siege, recalled in ACOK Catelyn IV / prologue). Three sub-actions:

- **F1a.** Repoint the 5 dropped staged role edges (in `working/edge-modeling/plate3-full/role-edges-staging.jsonl`) to `siege-of-storms-end-299` and merge: `mace-tyrell AGENT_IN`, `stannis-baratheon COMMANDS_IN`, `gawen-wylde VICTIM_IN`, `cressen AGENT_IN`, `davos-seaworth AGENT_IN`. The live node currently has **only 1 edge** (shadow-assassination-of-renly SUB_BEAT_OF) — zero participants. This single fix gives a canonical historical siege its full cast.
- **F1b.** Note: `stannis COMMANDS_IN` should arguably be the defender-AGENT and `mace-tyrell` the besieging COMMANDS_IN — review roles at merge.
- **F1c. BUG (found this triage):** the 6th staged edge **leaked into the live graph**: `{"edge_type":"LOCATED_AT","source_slug":"siege-of-storm-s-end-recalled","target_slug":"storms-end"}` is live in `edges.jsonl` (plate5_merged_at 2026-06-09) with a **dangling source** — that node was never minted. Repoint source to `siege-of-storms-end-299` (it already has no LOCATED_AT) or drop. Worklog said "5 role edges dropped"; the LOCATED_AT row escaped the drop filter.

### F2. S89 wrong-direction role edges (4 items, all live in edges.jsonl) — **[manual — retype/drop judgment per edge]** [EXECUTED 2026-06-14]

| # | Live edge | Proposed action |
|---|---|---|
| F2a | `robb-stark COMMANDS_IN lord-walder-calls-for-the-bedding` | **Drop.** Walder called for the bedding; Robb merely granted permission (evidence quote says exactly this). |
| F2b | `greatjon-umber AGENT_IN the-bedding-ceremony-begins` | **Retype → ATTENDS.** He carries Roslin per custom — participant, not executor; AGENT_IN on a Red Wedding beat reads as perpetrator. |
| F2c | `catelyn-stark AGENT_IN the-wedding-feast-proceeds` | **Retype → ATTENDS.** POV attendee (and eventual victim); mining picked up her direct-object Pass-1 mention. |
| F2d | `house-tyrell VICTIM_IN tyrell-plot-revealed` | **Retype → AGENT_IN.** It was *their* plot being revealed; framed-conspirator is not a victim role. (Probe 2.) |

### F3. Mint two Purple Wedding beats (fills Probe 2's confirmed gap) — **[manual-light: mint from queue JSON]** [EXECUTED 2026-06-14]

Probe 2 (S89): purple-wedding hub has exactly 1 SUB_BEAT_OF (`tyrell-plot-revealed` — not even about the poisoning). The queue contains the missing beats; Q1=a declined them.

- **F3a. `joffrey-dies`** — MINT hub + `SUB_BEAT_OF purple-wedding`. Queue participants are the *correct* attribution: `lady-olenna-tyrell AGENT_IN` (resolve slug → live `olenna-tyrell`), `joffrey-baratheon VICTIM_IN`, `golden-wedding-chalice WIELDED_IN` (no artifact node — mint or drop role), `red-keep LOCATED_AT`. **This matters doubly:** the only death edge live today is `tyrion-lannister POISONS joffrey-baratheon` at tier 1 — Tyrion's sarcastic ADWD false confession ("Oh, and my nephew Joffrey, I poisoned him") — see F5. Suggest slug `death-of-joffrey-baratheon` per the S90/S91 rename convention (event-named, not action-named).
- **F3b. `wedding-ceremony-at-the-great-sept-of-baelor`** — MINT + `SUB_BEAT_OF purple-wedding` (Joffrey+Margaery vows; participants joffrey/margaery/mace + great-sept-of-baelor LOCATED_AT). Gives the hub its ceremony beat.

### F4. Mint Red Wedding guest-right beat — **[manual-light]** [EXECUTED 2026-06-14]

- **F4a. `catelyn-secures-guest-right`** — MINT + `SUB_BEAT_OF red-wedding`. The bread-and-salt beat (catelyn + walder-frey, the-twins) is the thematic cornerstone of the Red Wedding's guest-right violation; hospitality is a first-class extraction target in this project. Red Wedding's 8 existing beats don't include it.

### F5. Retier the false-confession edge — **[scriptable]** *(adjacent to queue item `tyrion-falsely-confesses-to-joffrey-s-murder`)* [EXECUTED 2026-06-14]

- Live edge `tyrion-lannister POISONS joffrey-baratheon` carries `confidence_tier: 1` while its own `asserted_relation` says "Claims to have poisoned (unverified)". Retier (Tier 4/5) and/or add a `false-confession` qualifier. Once F3a lands, the graph stops asserting the wrong poisoner as its strongest Joffrey-death signal.

### F6. Add missing canon-death/attack dyads — **[scriptable from queue JSON + slug-resolution map]** [EXECUTED 2026-06-14]

D8's KEEP-DYAD default assumed the direct edge already existed in the Pass-1 spine. Verified against live `edges.jsonl`: **none of these have one.** Proposed: emit direct edges using each queue item's participants + evidence quote (chapter-scope provenance, like Plate 3 role edges).

| # | Queue slug | Proposed edge | Note |
|---|---|---|---|
| F6a | dany-mercy-kills-drogo-at-dawn | `daenerys-targaryen KILLS drogo` (qualifier: mercy) | Only LOVES/MOURNS/SPOUSE_OF live |
| F6b | the-watching-others-kill-royce | `others KILLS waymar-royce` | Species node `others` + `waymar-royce` both exist; series-opening death absent |
| F6c | nymeria-attacks-joffrey | `nymeria ATTACKS joffrey-baratheon` | Triggers Lady's death; node `nymeria` exists, zero such edge |
| F6d | arya-attacks-joffrey | `arya-stark ATTACKS joffrey-baratheon` | Companion beat to F6c; WIELDED Needle in queue data |
| F6e | sam-kills-the-other-with-dragonglass | `samwell-tarly KILLS others` (qualifier: individual, dragonglass) | First Other killed in millennia; queue slug `sam-tarly` needs resolution; no individual Other node — point at species or mint |
| F6f | sam-stabs-paul-with-dragonglass | `samwell-tarly KILLS small-paul` (qualifier: wight) | `small-paul` node exists; no edge |
| F6g | wun-wun-kills-ser-patrek | `wun-weg-wun-dar-wun KILLS patrek-of-kings-mountain` | Both nodes exist under different slugs than queue (`wun-wun`/`ser-patrek`) — resolver map needed |
| F6h | quentyn-martell-dies | `viserion KILLS quentyn-martell` (qualifier: dragonfire; tier 2) | Quentyn has 40+ live edges, zero death edge; which dragon is text-soft — keep tier 2 |
| F6i | beric-killed | `sandor-clegane KILLS beric-dondarrion` (qualifier: trial-by-combat, resurrected) | Only OPPOSES live; this is the Hollow Hill kill |
| F6j | brienne-fights-and-kills-the-man-in-the-hound-s-helm | `brienne-of-tarth KILLS rorge` | Helm-wearer is Rorge (named in text); `rorge` node exists, no edge |
| F6k | pate-s-death | `alchemist KILLS pate-novice` (qualifier: poison) | Both nodes exist; per impersonation-edge rule, edge attaches to `alchemist` (the worn face), not to a Jaqen theory |
| F6l | holly-killed | `house-bolton KILLS holly` (qualifier: crossbow, escape-from-winterfell) | `holly` node exists; agents are anonymous Bolton crossbowmen — faction-level attribution per queue |

---

## QUARANTINE (10 items — needs Matt or a policy decision)

> **S95 (2026-06-13) — 5 of 10 items RESOLVED via parallel research subagents.** See `curation/s95-quarantine-resolutions-2026-06-13.md` for full dossiers, JSON-ready edges, and minted-node frontmatter. Cleanup session: read that file as the source of truth for these rows.

| Queue slug | What's unresolvable | S95 status |
|---|---|---|
| multiple-deaths-at-the-wedding | `dothraki-warriors` is both AGENT_IN and VICTIM_IN of itself (Drogo's wedding brawls); no coherent dyad or hub shape — needs a "collective self-harm event" convention or a drop. | open |
| a-boy-is-run-down-and-killed | Victim unnamed, no node. Needs the unnamed-minor-victim node policy before any edge is mintable. | **SKIP — accept gap** (Lhazar sack; **Matt 2026-06-13: NOT Mycah** — Mycah's death already exists as Tier-1 dyad + S95 Q5 reifies it as `death-of-mycah` event hub under `incident-at-the-trident` parent) |
| a-captive-girl-is-beheaded | Same unnamed-victim class. | **SKIP — accept gap + Pass-1 audit flag** (queue verbatim not located in-corpus; likely LLM paraphrase) |
| arya-kills-the-postern-guard | Victim unnamed (`postern-guard`, no node) — but this is a canonical entry in Arya's kill list (her live KILLS list lacks it). Mint a minor node or accept the list stays incomplete: Matt's call. | **MINT** `postern-guard-of-harrenhal` (character.human) + KILLS edge (Tier 1, acok-arya-10:295) |
| galley-crews-put-to-death-slaves-freed | Victim is an unnamed collective (`ghiscari-galley-crews`, no node); same node-policy question at faction scale. | **MINT** `ghiscari-galley-crews-isle-of-cedars` (character.minor collective) + KILLS edge (Tier 1, adwd-victarion-01:53) |
| eagle-attacks-ghost | Attacker is Orell's skinchanged eagle (later Varamyr's). Attaching ATTACKS to species node `eagle` loses the skinchanger identity the project cares about — needs an identity-attachment decision (analog of the impersonation rule). | **MINT** ATTACKS `orell → ghost` (only scene: ACOK Jon-07:101 — Orell still alive at time of attack; Varamyr-takeover is later); skinchanger-identity convention parallels impersonation rule |
| forest-battle-begins | This micro-beat (northern-forces vs asha at Deepwood Motte) is the graph's only trace of the Battle of Deepwood Motte. A dyad undersells it; a hub is Track B mining territory. Route to Track B, don't resolve here. | open (route Track B) |
| three-squires-attack-the-crannogman | Knight of the Laughing Tree backstory — crannogman↔howland-reed identity inference + unnamed squires + Probe 3's "Tourney at Harrenhal: 0 beats" gap. Belongs to a deliberate Harrenhal/KotLT mining decision (Track B), not a one-off edge. | open (route Track B) |
| stallion-heart-ceremony | Design said spot-check non-harming for legit ceremonies — this is one: named Dothraki rite carrying the "stallion who mounts the world" prophecy payload (6 agents + Vaes Dothrak). Mint-worthiness is a prophecy-linkage judgment for Matt. | **MINT** event hub `stallion-heart-ceremony` (event.ceremony) + prophecy node `stallion-who-mounts-the-world` + SUBJECT_OF_PROPHECY (`rhaego→prophecy`) + PROPHESIED_BY (`prophecy→dosh-khaleen`) + 6 role edges. **Bonus finding:** existing `the-stallion-is-brought-in-and-sacrificed` is mis-slugged (it's Mirri's bloodmagic, not the Vaes Dothrak rite) — rename queued for future session |
| wedding-feast | Queue evidence conflates Tommen's vows with feast beats (participants: tommen, margaery, butterbumps, moon-boy, blue-bard). Which wedding-event this belongs to is ambiguous; Tommen-Margaery has no hub to attach to. | **MINT** sub-beat `wedding-feast-at-the-red-keep` SUB_BEAT_OF `wedding-of-tommen-i-baratheon-and-margaery-tyrell` (existing hub) + 3 AGENT_IN performers + 2 ATTENDS bride/groom (AFFC Cersei III, affc-cersei-03:147) |

---

## KEEP-AS-IS (81 items — default was right, no action ever)

Reason codes: **DL** = direct dyad verified live in edges.jsonl (cited); **OBS** = observation/witness/internal beat, no n-ary structure; **SPC** = speech/dialogue/intent/decree beat; **MIC** = micro-beat not worth any graph object; **JRN** = journey/movement/logistics beat; **CER** = routine ceremony/scene beat, no unique payload; **NOA** = death/event with no external agent.

### borderline-single-agent (53)

| Queue slug | Reason |
|---|---|
| arya-kills-the-stableboy-with-needle | DL — `arya-stark KILLS stableboy-at-kings-landing` live |
| street-rumors-about-robert-s-death | OBS — "victim" is the rumor's subject, not a harmed party |
| arya-sees-the-tower-of-the-hand-under-attack | OBS — witness beat; house-stark "VICTIM" never minted |
| dawn-breaks-and-the-battle-ends | OBS — scene transition |
| ser-jorah-fights-and-kills-qotho | DL — `jorah-mormont KILLS qotho` live |
| gregor-kills-his-horse-and-attacks-loras | MIC — tourney beat; dyad class, horse unnamed |
| littlefinger-s-final-betrayal | DL-class — betrayal carried by Pass-1 spine; no n-ary structure |
| gared-attributes-the-deaths-to-cold | SPC — attribution dialogue |
| will-discovers-the-bodies-have-vanished | OBS — discovery beat |
| fool-s-jest-about-kinslayer-kingslayer | SPC — jest |
| the-undying-attack-dany | MIC — HOTU sequence beat; dyad class |
| sorrowful-man-assassination-attempt | MIC — attempt; dyad class |
| ghost-kills-craster-s-rabbits | MIC |
| davos-boards-and-captures-white-hart | MIC — naval capture, dyad class |
| cressen-offers-the-poisoned-cup-to-melisandre | DL — `cressen POISONS melisandre` live |
| cressen-drinks-the-poisoned-wine-and-dies | DL — same scene, covered by the POISONS dyad |
| theon-threatens-systematic-executions | SPC — threat |
| tyrion-confronts-slynt-about-ned-stark-s-execution | SPC — confrontation dialogue |
| aron-santagar-killed | MIC — riot death, anonymous mob agent |
| tyrion-assesses-the-battle-situation | OBS — internal |
| tyrion-reasons-the-battle-was-won | OBS — internal |
| battlefield-delirium-dream | OBS — dream |
| thoros-at-the-siege-of-pyke | OBS — recollection beat (siege itself is a separate node question) |
| arya-questions-the-prisoners | SPC |
| robb-sentences-karstark-to-death | DL — `robb-stark EXECUTES rickard-karstark` live |
| dawn-execution-in-the-godswood | DL — same event, covered by EXECUTES dyad |
| catelyn-takes-jinglebell-hostage | DL — `catelyn-stark KILLS aegon-frey-son-of-stevron` live |
| davos-declares-intent-to-kill-melisandre | SPC — intent, never executed |
| chett-goes-to-kill-sam-anyway | SPC — intent, interrupted by the Others |
| bannen-dies | NOA — dies of wounds |
| craster-attacks | MIC — mutiny beat; dyad class |
| sam-kills-the-other-with-dragonglass | *(moved to FIX F6e)* |
| ravens-attack-the-wights | MIC — collective animals |
| joffrey-dies | *(moved to FIX F3a)* |
| tyrion-declares-his-innocence-and-demands-trial-by-battle | SPC — trial demand |
| tywin-dies | DL — `tyrion-lannister KILLS tywin-lannister` live |
| tyrion-falsely-confesses-to-joffrey-s-murder | *(moved to FIX F5 — its live edge is mis-tiered)* |
| the-kindly-man-explains-the-nature-of-death-and-the-candles | SPC |
| brienne-invokes-guest-right | SPC — hospitality beat; jeyne-heddle "VICTIM" is mis-roled but was never minted |
| jaime-ends-the-council-and-announces-attack-at-first-light | SPC — council close |
| battle-concluded | OBS — transition |
| sea-battle-at-the-mouth-of-the-mander | MIC — recalled skirmish; dyad class |
| cersei-denies-murder-charges | SPC |
| hostage-decree | SPC — decree |
| dany-dresses-in-her-tokar-with-baby-pearls-for-the-wedding | MIC — toilette |
| dany-surveys-the-siege-from-the-terrace | OBS |
| drogon-kills-the-boar-with-black-fire | MIC — unnamed animal victim |
| mock-battle | CER — performance beat |
| davos-captured-in-sisterton | MIC — capture, dyad class |
| varamyr-fails-and-dies | NOA — second-life failure; his KILLS dyads (bump, haggon) live |
| ramsay-promises-food-and-care-for-prisoners | SPC |
| the-kindly-man-s-teaching-about-killing | SPC |
| hizdahr-taken-prisoner | MIC — arrest, anonymous agents |
| post-ceremony-music | MIC — ambient |
| theon-climbs-the-inner-wall-battlements | JRN |
| tyrion-finds-poisonous-mushrooms | OBS — solo discovery (Chekhov tracking belongs to Pass 4) |
| quentyn-martell-dies | *(moved to FIX F6h)* |

*(Rows marked "moved to FIX" are shown for cross-reference; they are counted in FIX, not here.)*

### non-harming-multi-agent (28)

| Queue slug | Reason |
|---|---|
| the-direwolves-howl-from-a-kill | MIC |
| robb-presents-his-battle-plan | SPC — council |
| the-battle-rages-through-the-night | OBS — ambient battle beat |
| pre-wedding-dinner-at-the-manse | CER — dinner scene (food detail lives in Pass-1 extraction, not the graph) |
| dany-rides-through-the-battlefield-aftermath | JRN |
| stallion-sacrifice | MIC — follow-on to stallion-heart-ceremony (which is quarantined) |
| they-approach-the-battleground-at-the-ford | JRN |
| tyrion-arms-for-battle | JRN — preparation |
| shaggydog-kills-the-dying-horse | MIC |
| theon-arms-for-battle | JRN — preparation |
| joffrey-s-role-in-battle-debated | SPC — council debate |
| wedge-advances-along-the-walls | JRN — troop movement |
| waiting-during-the-battle | OBS |
| ser-axell-and-queen-selyse-attribute-the-deaths-to-r-hllor | SPC — attribution |
| nightfire-prayer-ceremony | CER — routine rite |
| night-attack-begins | OBS — battle transition |
| they-depart-for-the-wedding | JRN |
| wedding-feast-and-bedding | CER — Lysa+Petyr wedding; the marriage itself rides the Pass-1 MARRIES/SPOUSE_OF spine |
| joffrey-s-wedding-feast-planned | SPC — planning beat |
| shagwell-attacks | MIC — Whispers fight; dyad class |
| arianne-and-doran-argue-about-the-plot-s-consequences | SPC |
| wedding-ceremony-at-the-temple-of-the-graces | CER — Dany+Hizdahr wedding; SPOUSE_OF spine covers it; hub is Track B if ever |
| jon-attends-the-wedding-feast | CER — Alys+Sigorn feast attendance |
| wedding-ceremony-begins | CER — Alys+Sigorn rite; marriage rides the spine |
| conspiracy-meeting-in-armory | SPC — meeting beat |
| theon-leads-jeyne-holly-and-frenya-toward-battlements-gate | JRN — escape movement |
| arrive-at-battlements-gate | JRN |
| the-cart-travels-through-the-siege-camp | JRN |

*(catelyn-secures-guest-right → FIX F4a; wedding-ceremony-at-the-great-sept-of-baelor → FIX F3b; wedding-feast and stallion-heart-ceremony → QUARANTINE.)*

---

## Suggested execution

**Scriptable batch (one script, dry-run gated):**
- F1a/F1c — repoint 5 staged role edges + repair the dangling LOCATED_AT leak (inputs already in `role-edges-staging.jsonl`)
- F5 — retier the false-confession POISONS edge
- F6a–F6l — 12 dyad emissions from queue-item participants + evidence quotes, with a small slug-resolution map (`lady-olenna-tyrell→olenna-tyrell`, `sam-tarly→samwell-tarly`, `wun-wun→wun-weg-wun-dar-wun`, `ser-patrek→patrek-of-kings-mountain`, `pate→pate-novice`, `the-alchemist→alchemist`)

**Manual (Matt review per item):**
- F2a–F2d — 4 retype/drop judgments on live Red Wedding / Tyrell role edges
- F3a/F3b/F4a — 3 hub mints (slug naming per S91 convention; SUB_BEAT_OF targets purple-wedding ×2, red-wedding ×1)
- The 10 QUARANTINE items — 5 are one policy decision (unnamed-victim node policy), 2 route to Track B, 3 are individual judgment calls (eagle identity, stallion ceremony, wedding-feast conflation)

**Sequencing note:** F3a before/with F5 — don't leave the false-confession edge as the only Joffrey-death signal after retiering removes its tier-1 status.
