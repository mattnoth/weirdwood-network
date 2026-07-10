# S204 orchestrator adjudications (running log)

Applied at final assembly, after Haiku fresh-verify. Batch-1 review (F1516/G17/H181920):

| id | decision | reason |
|----|----------|--------|
| H-E36 | DROP | battle MOTIVATES birth-of-royce-baratheon — quote grounds Lady Elenda's NAMING decision, not the birth; trivia, not spine. |
| G17-E12 | RETYPE MOTIVATES→ENABLES | city-watch is the ACTOR, not the motivation; their loyalty is the door-opener for the fall (rubric: MOTIVATES source = motivation, target = actor/decision-event). |
| F1516-E02 | PENDING fresh-verify, skeptical | MOTIVATES → faction node target is off-rubric; quote = the oath scene, weak for "blacks form". |
| F1516-E03 | PENDING fresh-verify, skeptical | quote grounds the greens/blacks NAMING custom (111 AC tourney), not birth→faction causation. |
| F1516-E04 | ACCEPT | F&B stages the Driftmark brawl after Ser LAENOR's funeral (unlike the show's Laena funeral) — quote grounds it. |
| G17-E17, H-E17, H-E18 | already-live dedup drops (assembler) | fine. |

Batch-2 additions:
- E14 flag: `lord-rogars-war` vs `third-dornish-war` suspected DUPLICATE nodes for the same war (E14 targeted third-dornish-war only) → dup-merge follow-up, feed to duplicate-detector class work.
- E14: tier-2/disputed `myrish-bloodbath CAUSES great-council-of-101-ac` grounded in Gyldayn's foreshadowing line — cross-check at final assembly against section-15 wiring (F1516 minted nothing for the Baelon-heir mechanical chain).
- E14: Prince Gaemon birth/death nodes missing, left unwired + flagged (out of scope).

- I2122 flag: `maidens-day-ball` / `regency-of-aegon-iii` carry a mistyped `event.battle` type → retype residue (schema-drift class), not blocking this mint.

Fresh-verify wave 1 reconciliation (F1516 23C/4A/1R, G17 23C/1A):
| id | decision | reason |
|----|----------|--------|
| F1516-E03 | DROP (verifier REJECT + my pre-flag) | quote grounds naming custom, not birth→faction causation. |
| F1516-E02 | DROP | same class as E03 — faction-target MOTIVATES with oath-scene quote; the blood-oath node already carries green formation. |
| F1516-E09 | RETYPE CAUSES→ENABLES | Aegon resisted ("My sister is the heir, not me"); Cole's threat mediated — concealment was door-opener. |
| F1516-E12 | KEEP, RE-QUOTE to 16-p01:191 | orchestrator re-verified with text open: "They stole my crown and murdered my daughter, and they shall answer for it." grounds BOTH E11 and E12 (usurpation + stillbirth jointly motivate the counter-coronation); replaces the weak "And so the Dance began" hinge. |
| F1516-E25/E26 | DROP | PART_OF dance for the two coronations: weak quotes + non-battle containment; both coronations already wired causally into the spine. E24/E27 (CONFIRMed) stay. |
| G17-E12 | RETYPE MOTIVATES→ENABLES | verifier agrees with pre-flag. |
| aemond-loses-his-eye-at-driftmark node | FIX era → targaryen-rule | 120 AC is pre-Dance; verifier caught. |

Fresh-verify H181920 reconciliation (37C/2A/1R):
| id | decision | reason |
|----|----------|--------|
| H-E36 | DROP confirmed | battle grounds the NAMING (child born 7 days earlier); verifier REJECT agrees with pre-flag. |
| H-E37 | RETYPE AGENT_IN→SUSPECTED_OF (keep tier-2+disputed) | "the hand that poisoned the Arbor red will never be known… at the behest of Larys Strong" — orchestrator-not-poisoner; ACCEPT. Note: SUSPECTED_OF matches the larys SUSPECTED_OF death-of-aegon-ii edge S203 already minted — CHECK for dup at assembly before emitting. |
| H-E35 | RETYPE MOTIVATES→TRIGGERS | "put their plans in motion" — pre-existing conspiracy sparked, not a new decision; ACCEPT. |

Fresh-verify B0506 (30C/0A/0R — clean, disputed rows audited) + E14 (26C/4A/0R) reconciliation:
| id | decision | reason |
|----|----------|--------|
| E14-E16 | RETYPE CAUSES→ENABLES (keep tier-2+disputed+gyldayn-synthesis) | Gyldayn's hellhorns line foreshadows consequences but never narrates the mechanical chain; ENABLES = honest precondition, traversable via full-chain. |
| E14-E10, E14-E26 | RE-QUOTE per verifier (extend truncated quotes) | mechanical pass but quotes cut mid-phrase; exact fixes in verifications/E14.json. |

Fresh-verify I2122 reconciliation (21C/1A/0R, 5 nodes OK):
| id | decision | reason |
|----|----------|--------|
| I-E01 | DROP | source `regis-groves` is a character — wrong shape for TRIGGERS; refusal-to-kneel is too fine-grained to reify for one edge. VERIFY at assembly that the `death-of-regis-groves` mint identity narrates the refusal + contested means (it should — tier-2/gyldayn-synthesis grounding was confirmed). |

Fresh-verify C070809 reconciliation (26C/1A/0R, 4 nodes OK):
| id | decision | reason |
|----|----------|--------|
| C-E04 | KEEP, DOWNGRADE tier-1→tier-2, note inferential step | causation implicit (failed gates confrontation → Alyssa's undermine-via-household plan); tier-2 is the schema treatment for "inferable with high confidence, not stated directly". |

Flag follow-ups (not this session's mint):
- assault-on-harrenhal `DEFEATS: blacks` wiki edge looks direction-backwards → schema-drift/orphan-edge pass fodder.
- Prince Daeron's death at Second Tumbleton has no event node (3 conflicting accounts) → possible future mint, harvest-logged by H.
- "Moon of the Three Kings" NOT minted (Gyldayn calls the label a misnomer) — endorse; note in report.
- Batch-1 harvest pointers (12) to be appended to working/harvest-queue.md at close-out.
