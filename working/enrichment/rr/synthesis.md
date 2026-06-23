# Robert's Rebellion — enrichment pass 1: SYNTHESIS & LOCKED MINT SET (S133)

> Board pick = Robert's Rebellion (unanimous A/B/C). 3-lens fan-out (`proposal-lens{1,2,3}.md`) synthesized
> here. Every quote below was LINE-CHECKED by the orchestrator against the chapter files (verbatim, at-cite).
> All target slugs confirmed to exist. This doc is the mint spec (→ `scripts/mint_rr_enrichment_s133.py`)
> AND the fresh-verify input.

## NEW NODES (3) — type event.incident, node_version 1, pass_origin s133-rr-enrich
1. **knight-of-the-laughing-tree-incident** — name "Knight of the Laughing Tree incident"; aliases
   ["Knight of the Laughing Tree incident","the mystery knight at Harrenhal","Laughing Tree incident"];
   era roberts-rebellion; occurred.ac_year 281, precision year, basis book-chapter, date_confidence tier-2.
   Desc: at the Tourney at Harrenhal a mystery knight in patchwork armor with a weirwood-faced shield
   unhorsed three knights whose squires had beaten the crannogman Howland Reed, demanding only "teach your
   squires honor" as ransom, then vanished when Aerys sent Rhaegar to unmask him. Identity GATED.
2. **exile-of-jon-connington** — name "Exile of Jon Connington"; aliases ["exile of Jon Connington",
   "Connington stripped and exiled","Aerys exiles Jon Connington"]; era roberts-rebellion; occurred.ac_year
   283, precision year, basis book-chapter, date_confidence tier-2. Desc: after losing the Battle of the
   Bells (failing to kill Robert), Jon Connington was stripped of titles and exiled by Aerys — the premise
   of the AEGON arc (Connington later raises Young Griff).
3. **murder-of-jon-arryn** — name "Murder of Jon Arryn"; aliases ["murder of Jon Arryn","death of Jon
   Arryn","poisoning of Jon Arryn"]; era war-of-the-five-kings; occurred.ac_year 298, precision year, basis
   book-chapter, date_confidence tier-2. Desc: the inciting mystery of the saga — Jon Arryn poisoned with
   the tears of Lys; the realm (via Lysa's letter) blamed the Lannisters; the ASOS reveal exposes Lysa as
   the administrator at Littlefinger's instigation. (NOT PART_OF roberts-rebellion — 298 AC, standalone.)

> No `containers:` tags on the new nodes this pass (RR is not one of the 5 approved containers; these are
> RR-cluster roots — a future RR-container decision can tag them). Flagged, not assigned.

## EDGES TO MINT (24) — run_id rr-enrichment-s133, typed_by curator-causal-arc, candidate_kind causal-curator-arc, evidence_kind book-pass1
Causal edges carry `verified_by: pending` until the fresh-verify subagent CONFIRMs.

### Causal / structural (5)
| # | type | source → target | tier | evidence_ref | quote (verbatim, contiguous) |
|---|------|-----------------|------|--------------|------|
| E1 | CAUSES | battle-of-the-bells → exile-of-jon-connington | 1 | adwd-the-griffin-reborn-01.md:57 | "After the Battle of the Bells, when Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion" |
| E2 | ENABLES | exile-of-jon-connington → aegon-revealed-to-the-golden-company | 1 | adwd-the-griffin-reborn-01.md:71 | "I failed the father," he said, "but I will not fail the son." |
| E3 | ENABLES | coronation-of-robert-i-baratheon → wedding-of-robert-i-baratheon-and-cersei-lannister | 1 | agot-eddard-07.md:101 | "I had no wish to marry after Lyanna was taken from me, but Jon said the realm needed an heir. Cersei Lannister would be a good match, he told me, she would bind Lord Tywin to me should Viserys Targaryen ever try to win back his father's throne" |
| E4 | ENABLES | wedding-of-robert-i-baratheon-and-cersei-lannister → death-of-robert-baratheon | 2 | agot-eddard-07.md:101 | "Cersei Lannister would be a good match, he told me, she would bind Lord Tywin to me should Viserys Targaryen ever try to win back his father's throne" |
| E5 | SUB_BEAT_OF | knight-of-the-laughing-tree-incident → tourney-at-harrenhal | 1 | asos-bran-02.md:179 | "The little crannogman was walking across the field, enjoying the warm spring day and harming none, when he was set upon by three squires." |

> E4 is the stretchiest (the Cersei-marriage as distal enabler of Robert's death). Flag for fresh-verify
> CONFIRM/ADJUST/REJECT. E2 is cross-container (RR→AEGON) — the high-value bridge.

### Role edges — KotLT incident (4)
| # | type | source → target | tier | evidence_ref | quote |
|---|------|-----------------|------|--------------|------|
| E6 | FIGHTS_IN | knight-of-the-laughing-tree → knight-of-the-laughing-tree-incident | 1 | asos-bran-02.md:225 | "The porcupine knight fell first, then the pitchfork knight, and lastly the knight of the two towers." |
| E7 | VICTIM_IN | howland-reed → knight-of-the-laughing-tree-incident | 1 | asos-bran-02.md:179 | "he was set upon by three squires. They were none older than fifteen, yet even so they were bigger than him, all three." |
| E8 | WITNESS_IN | aerys-ii-targaryen → knight-of-the-laughing-tree-incident | 1 | asos-bran-02.md:229 | "The king was wroth, and even sent his son the dragon prince to seek the man, but all they ever found was his painted shield, hanging abandoned in a tree." |
| E9 | AGENT_IN | rhaegar-targaryen → knight-of-the-laughing-tree-incident | 1 | asos-bran-02.md:229 | "the king himself urged men to challenge him" — USE the "sent his son the dragon prince to seek the man" span (contiguous from :229) |

### Role edges — Connington exile (2)
| # | type | source → target | tier | evidence_ref | quote |
|---|------|-----------------|------|--------------|------|
| E10 | VICTIM_IN | jon-connington → exile-of-jon-connington | 1 | adwd-the-griffin-reborn-01.md:57 | "Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion" |
| E11 | COMMANDS_IN | aerys-ii-targaryen → exile-of-jon-connington | 1 | adwd-the-griffin-reborn-01.md:57 | "Aerys Targaryen had stripped him of his titles and sent him into exile in a mad fit of ingratitude and suspicion" |

### Role edges — Battle of the Bells (fill bare node) (2)
| # | type | source → target | tier | evidence_ref | quote |
|---|------|-----------------|------|--------------|------|
| E12 | COMMANDS_IN | jon-connington → battle-of-the-bells | 1 | asos-jaime-05.md:53 | "After dancing griffins lost the Battle of the Bells, Aerys exiled him." |
| E13 | AGENT_IN | robert-baratheon → battle-of-the-bells | 1 | asos-jaime-05.md:53 | "He had finally realized that Robert was no mere outlaw lord to be crushed at whim, but the greatest threat House Targaryen had faced since Daemon Blackfyre." |

### Role edges — Wildfire-plot overlays (wire the Chekhov's-gun cache) (2)
| # | type | source → target | tier | evidence_ref | quote |
|---|------|-----------------|------|--------------|------|
| E14 | AGENT_IN | rossart → wildfire-plot | 1 | asos-jaime-05.md:55 | "Aerys burnt him alive for that, and hung his chain about the neck of Rossart, his favorite pyromancer." |
| E15 | COMMANDS_IN | aerys-ii-targaryen → wildfire-plot | 1 | asos-jaime-05.md:53 | "So His Grace commanded his alchemists to place caches of wildfire all over King's Landing. Beneath Baelor's Sept and the hovels of Flea Bottom, under stables and storehouses, at all seven gates, even in the cellars of the Red Keep itself." |

### Jon Arryn murder reification (4)
| # | type | source → target | tier | evidence_ref | quote |
|---|------|-----------------|------|--------------|------|
| E16 | VICTIM_IN | jon-arryn → murder-of-jon-arryn | 1 | agot-eddard-07.md:311 | "The tears of Lys, they call it. A rare and costly thing, clear and sweet as water, and it leaves no trace." |
| E17 | AGENT_IN | lysa-arryn → murder-of-jon-arryn | 1 | asos-sansa-07.md:287 | "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!" |
| E18 | SUSPECTED_OF | petyr-baelish → murder-of-jon-arryn | 2 | asos-sansa-07.md:287 | "You told me to put the tears in Jon's wine, and I did. For Robert, and for us!" |
| E19 | SUSPECTED_OF | cersei-lannister → murder-of-jon-arryn | 2 | agot-catelyn-07.md:87 | "but whether it was Tyrion, or Ser Jaime, or the queen, or all of them together, I could not begin to say." |

> E16 VICTIM_IN tier-1 (Varys confirms the poisoning + victim). E17 lysa AGENT_IN tier-1 (her confession;
> coexists with the existing lysa KILLS/POISONS jon-arryn dyads — this is the reification role). E18
> Littlefinger SUSPECTED_OF (Tier-2 — the confession names him as instigator, but the full degree is the
> contested/inference part; SUSPECTED_OF, not COMMANDS_IN, holds the gating). E19 Cersei SUSPECTED_OF
> captures the FALSE in-world misdirection (Lysa's letter blamed the queen) — the suspicion is real even
> though she's innocent; this is the model use of SUSPECTED_OF.

### SUSPECTED_OF / WITNESS_IN substrate (5)
| # | type | source → target | tier | evidence_ref | quote |
|---|------|-----------------|------|--------------|------|
| E20 | SUSPECTED_OF | rhaegar-targaryen → abduction-of-lyanna | 2 | agot-bran-07.md:79 | "Robert was betrothed to marry her, but Prince Rhaegar carried her off and raped her," Bran explained. |
| E21 | SUSPECTED_OF | lyanna-stark → knight-of-the-laughing-tree-incident | 2 | asos-bran-02.md:233 | "Are you certain you never heard this tale before, Bran?" asked Jojen. "Your lord father never told it to you?" |
| E22 | WITNESS_IN | howland-reed → combat-at-the-tower-of-joy | 1 | agot-eddard-10.md:93 | "They had been seven against three, yet only two had lived to ride away; Eddard Stark himself and the little crannogman, Howland Reed." |
| E23 | WITNESS_IN | eddard-stark → combat-at-the-tower-of-joy | 1 | agot-eddard-10.md:45 | "he could hear Lyanna screaming. 'Eddard!' she called. A storm of rose petals blew across a blood-streaked sky, as blue as the eyes of death." |
(E1–E23 = the full set; 23 edges.)

> E20: the in-world "abduction/rape" framing (Robert's war-narrative). Holds the contested-agency substrate
> WITHOUT asserting either reading; the elopement counter-evidence (Dany "died for the woman he loved",
> agot-daenerys-08.md:187) attaches as node ## Evidence prose, NOT a competing edge. The node name stays.
> E21: Lyanna as the in-world-suspected KotLT (Meera's coded "she-wolf" tale; Jojen's pointed question
> implies Ned/Howland knew). Identity GATED — SUSPECTED_OF only.

**EDGE COUNT: 23 mint (E1–E23) + 1 DROP.** (E24 row is a numbering artifact — ignore; total is 23.)

## DROP (1)
- `roberts-rebellion GUEST_OF winterfell` (ref agot-catelyn-03.md:13, "Take the books away…healthy
  appetites") — misparsed junk; GUEST_OF not in vocab; the RR hub's sole (bogus) outgoing edge.

## NODE PROSE OVERLAYS (book-cite, attach to existing node ## Quotes / ## Evidence)
- `wildfire-plot` ## Book Citations: asos-jaime-05.md:53 (caches), :55 (Rossart's chain), :57 ("naught but ashes").
- `battle-of-the-bells` ## Book Citations: asos-jaime-05.md:53 (Connington's defeat/exile), adwd-the-griffin-reborn-01.md:55 ("I rose too high… overreached, and fell").
- `coronation-of-robert-i-baratheon` ## Quotes: agot-eddard-07.md:93 ("Damn you, Ned Stark… You were the one should have been king, you or Jon.").
- `abduction-of-lyanna` ## Evidence (contested-agency, opposing testimony): agot-daenerys-08.md:187 ("Her brother Rhaegar had died for the woman he loved.") + alias kebab→spaced fix (frontmatter `aliases:` to natural phrases).

## DEFERRED (noted, NOT minted this pass)
- `exile-of-viserys-and-daenerys` (RR→Essos seam) — forward-dangling into the theory-trap Essos container;
  defer to Essos enrichment. (Lens 1 3b.)
- `brandon-rides-to-kings-landing` granularity beat — low value; existing abduction CAUSES execution edge suffices.
- `battles-at-summerhall robert AGENT_IN` — wiki-only, no book quote; defer to a wiki-anchor pass.
- **`CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` recast** (off-vocab edge rhaegar→lyanna) — needs a vocab Active Decision
  ("no new capitalized terms" this session). HOLD for Matt; do NOT churn. → Matt-review item.
