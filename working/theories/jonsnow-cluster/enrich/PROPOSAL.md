# Jon Snow cluster — wave-2 ENRICH proposal (S219)

**Targets:** `r-plus-l-equals-j` (minted S214, run_id `rlj-cluster-theories-s214`), `bloodravens-grand-plan`
(minted S216, run_id `bloodraven-cluster-theories-s216`). Source: ASX "The real Jon Snow" (qSy2uaJ7ecU),
via `working/theories/jonsnow-cluster/substrate.jsonl`. **STAGING ONLY** — nothing here has been written
to `graph/`. No new nodes proposed.

## Method

1. Pulled all substrate rows tagged `theory: "R+L=J"` (13), `"Bloodraven's hidden hand"` (4), and
   `"Grand Northern Conspiracy"` (1 — dedup-check only, not a wave-2 target theory).
2. Dedup pass 1: `grep` the three target slugs against `graph/edges/edges.jsonl` (existing minted edges:
   8 on `r-plus-l-equals-j`, 6 on `bloodravens-grand-plan`, 10 on `grand-northern-conspiracy-theory`).
3. Dedup pass 2 (went further than the grep-only instruction): read both theory nodes' full bodies
   (`graph/nodes/theories/r-plus-l-equals-j.node.md`, `graph/nodes/theories/bloodravens-grand-plan.node.md`).
   Both nodes quote several passages **in prose without a dedicated edge** (e.g. the crypt-statue "Promise
   me, Ned" line, the raven's "Snow, snow, snow" line) — a beat can collide with node prose even when no
   edge object matches it. This caught one dup (B02) the edge-only grep would have missed.
4. Byte-verified every surviving quote against `sources/chapters/*.md` at the cited line (see Verification
   table below) before drafting `candidates.json`.
5. Applied a quality filter on top of dedup: a few beats are genuinely *new* (no collision) but too thin/
   generic to be honest theory evidence (e.g. "Jon has a Valyrian steel sword" ⇒ Targaryen blood, when many
   non-Targaryen houses carry Valyrian steel). These are marked `DROPPED-weak`, not `DROPPED-dup`.

## Dedup log — R+L=J (13 substrate beats → 8 kept, 5 dropped)

| beat | chapter:line | verdict | reason |
|---|---|---|---|
| jonsnow-B02 | agot-eddard-09:39 | **DROPPED-dup** | "Ned's promise to dying Lyanna" ("I will," Ned had promised her...). Same chapter+line already partially quoted in `r-plus-l-equals-j.node.md`'s own prose companion to edge T1 ("Ned Stark kept his vows" ... "Robert would swear undying love and forget them before evenfall," cited to `agot-eddard-09.md:39`) — the exact same sentence. Also the "promise-me" theme the task flagged as an already-used marquee beat (crypt-statue "Promise me, Ned" quote is likewise already in the node's Evidence For prose). |
| jonsnow-B03 | agot-bran-01:189 | **KEPT → JE1** | Ghost's albino coloring/red eyes as a Rhaegar echo. Not in any existing edge or node prose. Tier-5 (weak/crackpot, honestly tagged). |
| jonsnow-B05 | agot-jon-06:147 | **DROPPED-dup** | Night's Watch vow ("I shall take no wife... wear no crowns and win no glory") — exact same quote text AND same `agot-jon-06.md:147` line already minted as edge **T7** (`jon-snow` CONTRADICTS `r-plus-l-equals-j`). Word-for-word collision. |
| jonsnow-B07 | agot-tyrion-03:45 | **KEPT → JE2** | Alliser Thorne's Rebellion backstory (fought for the Targaryens, forced to take the black). Not covered by any existing edge. Tier-4. |
| jonsnow-B08 | agot-tyrion-02:105 | **DROPPED-weak** | "Jon's temper (Ghost attacking Tyrion) = Targaryen wolf-blood" is not tied to any established Targaryen trait in the text (no textual "Targaryens have tempers" premise); thinner and more generic than JE1's coloring echo. Not a dup, cut on quality grounds to keep the set honest. |
| jonsnow-B09 | agot-jon-08:143 | **DROPPED-weak** | "Longclaw is Valyrian steel ⇒ subtly connects Jon to Targaryen ancestry." Valyrian steel is not Targaryen-exclusive (Ice/Stark, Oathkeeper, Widow's Wail, Heartsbane, etc. — non-Targaryen houses hold Valyrian blades routinely); the inference doesn't hold up even at crackpot grade. Cut on quality. |
| jonsnow-B10 | acok-jon-06:191 | **KEPT → JE3** | Bael the Bard legend (blue winter rose left on a Stark maiden's pillow after a secret union) as a precursor parallel to Rhaegar/Lyanna. Not covered by any existing edge — a genuinely new, fandom-major beat. Tier-4. |
| jonsnow-B11 | agot-jon-07:23 | **KEPT → JE4** | Jon's own recurring Winterfell-crypt dream (searching for his father). Distinct from Ned's Tower of Joy dream (T2/T3, different chapter/character). Not covered. Tier-4. |
| jonsnow-B12 | adwd-jon-02:243 | **KEPT → JE5** | Jon swapping Gilly's baby for Mance/Dalla's son to hide it from Melisandre — an explicit textual echo of Ned protecting Lyanna's baby. Not covered by any existing edge; strongest new R+L=J add. Tier-3. |
| jonsnow-B13 | agot-eddard-10:93 | **KEPT → JE6** | Howland Reed's confirmed presence/survival at the Tower of Joy ("seven against three... Eddard Stark himself and the little crannogman, Howland Reed"). Same chapter as T3 but a different line (93 vs. 45) and a different point (survivor fact vs. rose-petal dream imagery) — not a duplicate. Tier-3. |
| jonsnow-B14 | acok-bran-03:127 | **KEPT → JE7** (judgment call) | Ned's emotional shutdown recounting Arthur Dayne/Howland Reed at the ToJ ("Father had gotten sad... would say no more"). Thematically adjacent to JE6 (both ToJ/Howland Reed, different books) — flagged explicitly as a judgment call, not dropped, because the evidentiary point is different: JE6 is "Howland Reed is a living witness," JE7 is "Ned's own visible evasiveness is itself a tell." Tier-4. |
| jonsnow-B17 | acok-jon-01:197 | **KEPT → JE8** | Maester Aemon's own backstory: a Targaryen prince (9th/10th in succession) diverted from the throne to the Citadel/Wall as a boy. This is the Aemon/Wall structural parallel the task explicitly named as an expected gap. Not covered by any existing edge. Tier-4. |
| jonsnow-B19 | affc-samwell-04:21 | **DROPPED** (off-target) | Quote is Aemon reflecting on Rhaegar's belief in the Prince Who Was Promised prophecy / Summerhall. Substrate tags this row `theory: "R+L=J"`, but the content is Azor Ahai/prophecy material — the R+L=J node's own body explicitly HOLDS OUT this exact territory ("UrhqmMRv1gQ's larger 'Rhaegar is Azor Ahai'... reading is deliberately excluded from this node... belongs to a separate Azor Ahai theory unit"). Flagged as a substrate mistagging, not evidence for the parentage claim; correctly belongs to the (out-of-scope) "Jon's resurrection... Azor Ahai destiny" theory bucket. |

**R+L=J: 8 kept (JE1–JE8), 5 dropped (2 dup, 2 weak, 1 mistagged).**

## Dedup log — Bloodraven's hidden hand (4 substrate beats → 3 kept, 1 dropped)

| beat | chapter:line | verdict | reason |
|---|---|---|---|
| jonsnow-B23 | agot-jon-08:157 | **KEPT → JE9** | Jon recalls finding Ghost only because he "heard a noise" — notable since Ghost is established elsewhere as always-silent. Not discussed anywhere in `bloodravens-grand-plan.node.md` or any G-edge. Tier-4. |
| jonsnow-B25 | agot-jon-01:39 | **KEPT → JE10** | Ghost's red-eyes/white-fur coloring as a weirwood/Bloodraven echo. This is the "Ghost/raven steering" beat the task flagged as an expected gap; not in the node body or any G-edge (G1/G3/G4/G6/G7/G9 cover Leaf's speech, the raven's "queer" line, the Whitewalls quote, Septon Sefton's rant, Melisandre's vision, and Bran's "thousand dreamers" — none touch Ghost's coloring). Tier-4. |
| jonsnow-B28 | asos-jon-11:55 | **KEPT → JE11** | Ghost leads Jon to the dragonglass cache buried at the Fist of the First Men. Same "is Ghost being steered" pattern as JE9/JE10, different beat (a concrete plot-critical discovery, not just an odd noise). Not covered by any existing edge. Tier-4. |
| jonsnow-B30 | asos-jon-08:11 | **DROPPED** (substrate mismatch) | Quote is Jon's Winterfell stone-kings dream ("You are no Stark... Go away"). Substrate's own paraphrase for this beat claims it's about "Bran warging his direwolf to save Jon from Styr" — but that scene is not in the quoted text at all; the quote is purely the crypt-dream. Confirmed as a substrate tagging error: the *identical* quote at the *identical* chapter:line (`asos-jon-08.md:11`) also appears as **jonsnow-B170** in `working/theories/jonsnow-cluster/enrichment-beats-worklist.md`, correctly classified there as a `"Jon Snow character enrichment"` context beat (about Jon's alienation + the Mance-army attack), not Bloodraven's-hidden-hand evidence. Same passage, two different theory tags under two different beat IDs — the Bloodraven tagging is the error. Dropped, not minted under either theory. |

**Bloodraven's hidden hand: 3 kept (JE9–JE11), 1 dropped (substrate mismatch).**

## Dedup log — Grand Northern Conspiracy (1 substrate beat → 0 kept, as expected)

| beat | chapter:line | verdict | reason |
|---|---|---|---|
| jonsnow-B102 | adwd-davos-04:125 | **DROPPED-dup** | "The north remembers, Lord Davos. The north remembers, and the mummer's farce is almost done. My son is home." — word-for-word identical quote, identical `adwd-davos-04.md:125` line, already minted as edge **G1** (`grand-northern-conspiracy` SUPPORTS `grand-northern-conspiracy-theory`, run_id `gnc-cluster-theories-s216`). Exact dup, as expected going in. |

## Verification table (byte-check against `sources/chapters/*.md`)

All 11 kept quotes were re-verified against the live chapter files at the exact cited line during this
session (not just trusted from the substrate's `grounded_by` field):

| id | file:line | match |
|---|---|---|
| JE1 | agot/agot-bran-01.md:189 | exact |
| JE2 | agot/agot-tyrion-03.md:45 | exact |
| JE3 | acok/acok-jon-06.md:191 | exact |
| JE4 | agot/agot-jon-07.md:23 | exact |
| JE5 | adwd/adwd-jon-02.md:243 | exact |
| JE6 | agot/agot-eddard-10.md:93 | exact |
| JE7 | acok/acok-bran-03.md:127 | exact |
| JE8 | acok/acok-jon-01.md:197 | exact |
| JE9 | agot/agot-jon-08.md:157 | exact |
| JE10 | agot/agot-jon-01.md:39 | exact |
| JE11 | asos/asos-jon-11.md:55 | exact |

## Source-node sanity check

All 8 `source` slugs used in `candidates.json` (`ghost`, `alliser-thorne`, `bael-the-bard`, `jon-snow`,
`howland-reed`, `eddard-stark`, `aemon-targaryen-son-of-maekar-i`) resolved to existing tier-1 nodes under
`graph/nodes/`. Note: `aemon-targaryen` (bare slug) is a 3-way disambiguation hub; the correct node for
"Maester Aemon" is `aemon-targaryen-son-of-maekar-i` (aliases include "Maester Aemon", "Uncle Maester") —
used that, not the hub.

## Judgment calls flagged for review

1. **JE1 (tier-5) and the Ghost/Rhaegar-coloring reading** — kept as genuinely new material, but this is a
   stacked, weak inference (Rhaegar's own described coloring is silvery-gold, not albino-white; "red eyes"
   only maps to Targaryen heraldry, not a stated physical trait of Rhaegar himself). Included at honest
   tier-5 rather than dropped, consistent with the tier-floor convention (crackpot-grade material stays in
   at tier-5 rather than being cut).
2. **JE6 / JE7 adjacency** — both source from the Tower of Joy/Howland Reed material and could arguably be
   read as one beat split into two edges. Kept both because the evidentiary point differs (witness-exists
   vs. Ned's-silence-is-a-tell) but flagging explicitly in case a reviewer wants to fold them into one or
   drop JE7.
3. **B19 mistagging** — dropped as off-target for R+L=J (belongs to the held-out Azor Ahai bucket per the
   node's own Ungrounded material section), not as a dup or weak beat. Worth noting the substrate has at
   least one cross-theory tagging error of this kind.
4. **B30 substrate integrity** — the clearest finding of this pass: `jonsnow-B30` (tagged Bloodraven's
   hidden hand) and `jonsnow-B170` (tagged Jon Snow character enrichment, in the separate worklist file)
   are the *same quote at the same chapter:line* under two different beat IDs and two different theory
   classifications. The Bloodraven tag appears to be the spurious one (the quote itself contains no
   Bran-warging/rescue content the paraphrase claims). Surfacing this in case it indicates a broader
   beat-extraction duplication pattern worth a spot-check elsewhere in the substrate.

## Harvest

No off-task finds worth pointing to `working/theories/harvest-s219-je.md` this pass — all chapter reads
were narrow single-line byte-checks (`sed -n '<line>p'`) against already-targeted quotes, not broader
passage reads that would surface incidental material (food/hospitality/description/foreshadowing). File
not created.

## Counts summary

| target | proposed | dropped-dup | dropped-weak | dropped-mistag | tier distribution (proposed) |
|---|---|---|---|---|---|
| r-plus-l-equals-j | 8 (JE1–JE8) | 2 (B02, B05) | 2 (B08, B09) | 1 (B19) | tier-3: 2 (JE5, JE6) · tier-4: 5 (JE2, JE3, JE4, JE7, JE8) · tier-5: 1 (JE1) |
| bloodravens-grand-plan | 3 (JE9–JE11) | 0 | 0 | 1 (B30, substrate mismatch) | tier-4: 3 (JE9, JE10, JE11) |
| grand-northern-conspiracy-theory | 0 | 1 (B102) | 0 | 0 | — |
| **Total** | **11** | **3** | **2** | **2** | **2×t3, 8×t4, 1×t5** |

18 substrate beats in → 11 proposed edges out (7 dropped: 3 exact/near-exact dup, 2 weak, 2 mistagged/
mismatched). All within the task's expected ranges (4–8 R+L=J, 2–4 Bloodraven).
