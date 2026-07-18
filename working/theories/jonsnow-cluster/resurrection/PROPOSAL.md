# Jon Snow resurrection cluster — proposal (S219)

Wave-2 flagship cluster. Source: ASX video `qSy2uaJ7ecU` ("The real Jon Snow"),
theory header "Jon's resurrection, second life, and Azor Ahai destiny" (line 3 of
`working/theories/extractions/qSy2uaJ7ecU.jsonl`). Substrate: 22 byte-verified beats
in `working/theories/jonsnow-cluster/substrate.jsonl` tagged with that theory name.
STAGING ONLY — nothing here has touched `graph/`.

## Summary

The theory bundles three linked claims about what happens after Jon Snow's death at
the Castle Black mutiny: (1) his spirit passes into Ghost via the skinchanger
"second life" mechanic; (2) his body is later revived, probably by Melisandre, at
some cost; (3) the revived Jon is physically/psychologically transformed. A fourth,
separable claim — that the transformed Jon is Azor Ahai reborn — overlaps with the
already-minted `azor-ahai-theories` node (S216) and is handled per the orchestrator's
split design: resurrection-mechanic beats mint a NEW node (`jon-snow-resurrection`);
AA-identity beats attach to the EXISTING node, and only where they add evidence
beyond the three edges (Z7/Z8/Z9) it already carries.

## Dedup notes — Z7/Z8/Z9 clearance

Grepped `graph/edges/edges.jsonl` for `azor-ahai-theories` before proposing anything;
found all 14 existing edges (Z1–Z14, run_id `azor-cluster-theories-s216`). Confirmed
none of my proposed quotes duplicate:

- **Z7** — melisandre, "I pray for a glimpse of Azor Ahai, and R'hllor shows me only
  Snow." (adwd-melisandre-01.md:37, t4) — not reused; my melisandre edges (JR7, JR8)
  cite adwd-jon-13.md:103 and adwd-jon-01.md:317, both distinct lines/chapters about
  a different subject (her personal stake in Jon, not her Snow-vision ambiguity).
- **Z8** — jon-snow, "A grey girl on a dying horse... A promised prince, born in
  smoke and salt..." (adwd-jon-13.md:101, t4) — not reused. Note this sits two lines
  above my JR7 quote (adwd-jon-13.md:103) in the SAME dialogue exchange — Z8 is
  Jon's outburst *at* Melisandre; JR7 is her reply. Adjacent but non-overlapping
  substrings of the same conversation; no byte overlap.
- **Z9** — jon-snow, "I am the sword in the darkness..." (agot-jon-06.md:147, t4) —
  not reused; none of my beats touch this chapter/line.

Two additional near-misses caught during verification, both resolved by exclusion
rather than reuse:

- **B63** (asx bleeding-star beat, affc-samwell-04.md:21) substantially overlaps the
  text already captured by the existing **Z6** edge (rhaegar-targaryen →
  azor-ahai-theories, same line 21: "Rhaegar, I thought . . . the smoke was from the
  fire that devoured Summerhall... He shared my belief when he was young, but later
  he became persuaded that it was his own son who fulfilled the prophecy"). B63's
  quote wraps around and duplicates that same clause. Excluded — would be a
  same-line, overlapping-substring duplicate of Z6, and doesn't add Jon-specific
  content (it's about the prince/princess gender question re: Dany, not Jon).
- **B81** (affc-samwell-04.md:21, "cycle repeats" CONTRADICTS beat) also draws from
  the SAME line 21 and its quoted text literally contains the "He shared my belief
  when he was young, but later he became persuaded that it was his own son who
  fulfilled the prophecy" clause already inside Z6. Beyond the overlap, the actual
  quoted sentence (Aemon second-guessing his Rhaegar/Aegon belief) does not, on a
  straight read, support the substrate's "cycle repeats / white walkers already came
  back once" framing that was attached to it as a paraphrase — that reading isn't
  in the quoted text. Excluded on both grounds (redundant + stance-label mismatch).

## Substrate-integrity notes

- Six beats carried `verbatim_quote: null` in the substrate (B38, B41, B43, B48,
  B56, B73) — meaning they were paraphrase-only, not yet byte-verified. I
  independently opened each cited `file:line` and extracted an exact quote myself
  (see candidates.json notes on JR3, JR4, JR6, JR7, JR11, JR13). All six checked
  out — the cited line contained material clearly matching the paraphrase in every
  case, no phantom citations.
- **B73**'s paraphrase said the Last Hero set out "with a sword, a dog, and
  companions"; the actual text at agot-bran-04.md:53 says "a sword, a horse, a dog,
  and a dozen companions" — the paraphrase silently dropped "a horse" and rounded
  "a dozen companions" to "companions." Not load-bearing for the theory, but I
  quoted the passage in full for accuracy rather than reproducing the paraphrase's
  omission.
- **B64**'s paraphrase claimed the quote supports the "Azor Ahai must be descended
  from Aerys" prophecy condition; the actual quote (adwd-jon-03.md:217) is about
  Nissa Nissa/Lightbringer's tempering, not lineage. I used the quote for what it
  actually says (the Lightbringer-forging sacrifice precedent, JR12) rather than
  the paraphrase's stated purpose. The "descended from Aerys" condition is already
  covered by the existing Z12 edge.
- **B48**'s paraphrase quoted both "I am your only hope" (adwd-jon-13.md:103, the
  cited location) and "have grave need of me" — but the latter phrase is NOT on
  that line; it's a different, earlier chapter (adwd-jon-01.md:317). The substrate
  row cited only one location for text that actually spans two. I kept B48's own
  citation as JR7 and added the second quote independently as JR8 (flagged as a
  non-substrate addition in both the candidates.json note and below).
- **B37**'s note says "Jon has warg-vision with Ghost" but the actual scene is Jon
  waking from a dream in which he experienced being attacked as Ghost — this is
  consistent with the paraphrase's substance (skinchanger persistence via Orell's
  eagle); no correction needed, just confirming the framing holds up.
- No other integrity problems found. All 16 quotes used in the final edge set are
  byte-exact matches to their cited `sources/chapters/*.md` line (verified via
  `sed -n '<line>p'` against each file before drafting any edge).

## Edge list and tier reasoning

### New node `jon-snow-resurrection` (13 edges, all SUPPORTS)

| id | source | quote gist | tier | why |
|---|---|---|---|---|
| JR1 | jon-is-stabbed-repeatedly | dying word "Ghost" | 3 | Subject-link anchor; minimal interpretation — it's literally his last word. |
| JR2 | orell | Jon's eagle-attack dream | 3 | Direct textual precedent of skinchanger-spirit persistence. |
| JR3 | varamyr | "second life worthy of a king" | 3 | Direct, explicit, uses the theory's own language. |
| JR4 | varamyr | "only the beast remains" | 3 | Direct statement of the mechanic (and its risk). |
| JR5 | melisandre | "man...wolf...man again" vision | 3 | Direct prophetic image, minimal interpretive layering. |
| JR6 | jon-snow | "I am a man, not a wolf" | 4 | Present-tense restraint; predicting post-death breakdown is an inference. |
| JR7 | melisandre | "I am your only hope" | 4 | Foreshadowing read, not an explicit resurrection statement. |
| JR8 | melisandre | "grave need of me" | 4 | Same category as JR7; also flagged as non-substrate addition. |
| JR9 | thoros | Beric's six revivals | 3 | Direct precedent for a real, already-demonstrated in-world cost mechanic. |
| JR10 | catelyn-stark | Stoneheart's transformation | 3 | Direct precedent for post-resurrection physical change. |
| JR11 | patchface | "crows white as snow" riddle | 4 | Riddle-reading; interpretive by nature. |
| JR12 | azor-ahai | Nissa Nissa/Lightbringer tempering | 3 | Direct legend text; minimal interpretation for the sacrifice-precedent claim itself. |
| JR13 | last-hero | Old Nan's Last Hero legend | 4 | Structural-parallel reading — legend maps to Jon's situation by analogy, not statement. |

Tier floor respected throughout (3–5 only). No tier-5 edges made the final cut (see
"cut for scope" below) — the tier distribution ended up 3/3/3/3/3/4/4/4/3/3/4/3/4,
i.e. 8×tier-3, 5×tier-4 within this node's edge set, which is a legitimate reflection
of how much of this particular mechanic (second-life persistence, resurrection-costs-
something, physical change) is directly textually stated versus interpretively
extended.

### Existing node `azor-ahai-theories` (3 edges: 2 SUPPORTS, 1 CONTRADICTS)

| id | type | source | quote gist | tier | why new (not Z7/8/9) |
|---|---|---|---|---|---|
| JR14 | SUPPORTS | daenerys-targaryen | House of Undying "prince that was promised"/"song of ice and fire"/"three heads" vision | 4 | Distinct scene from Z10 (primary vision vs. Dany's later recollection); adds the "three heads" line Z10 lacks. |
| JR15 | SUPPORTS | stannis-baratheon | Stannis's glowing blade, Jon-witnessed | 4 | New witness angle (Jon's own POV) not covered by Z2/Z3/Z4. |
| JR16 | CONTRADICTS | jon-snow | Mercy for Ygritte, echoing Ned | 4 | The video's own preferred "moral choice over prophecy" resolution — a thematic counterweight to the whole Jon-as-chosen-one framing, functionally parallel to how Z3/Z4 push back on Stannis. |

## Beats considered and excluded (accounting for all 22 substrate rows)

Used (16 of 22, several combined/deduped):
B37→JR2, B38→JR3, B39→JR5, B41→JR4, B42→(cut, see below), B43→JR6, B48→JR7(+JR8
bonus), B52→JR9, B53→JR10, B56→JR11, B61→JR15, B64→JR12, B66→JR14, B73→JR13,
B75→(merged into JR12's note as redundant), B82→JR16.

Excluded entirely:
- **B42** (Ned's "wolf blood" line, agot-arya-02.md:119) — grounded and real, but
  applying it to Jon requires *also* assuming the separately-unconfirmed R+L=J
  parentage claim is true (Ned's blood-line framing only reaches Jon if he's
  actually Lyanna's son). A legitimate tier-5 crackpot-depth edge, but I cut it
  to keep the edge count disciplined per the "fewer good edges beat many weak
  ones" guidance — flagging here in case the orchestrator wants it added back
  (it would slot in cleanly as a 14th new-node SUPPORTS edge, tier-5).
- **B44** (Dany's "fire and blood" internal monologue, adwd-daenerys-06.md:137) —
  the quote itself is about Dany, not Jon; the "parallel arc" argument is a
  cross-character structural comparison made BY the video, not textual evidence
  bearing on Jon. Doesn't fit the layer rule (no tier-1 node's confirmed content
  anchors a claim about Jon here). Not promoted to an edge or even ungrounded body
  prose — too tangential to include at all.
- **B63** — redundant with Z6 (see dedup notes above).
- **B68** (Melisandre's ranger-death prophecy accuracy, adwd-melisandre-01.md:103) —
  considered for the new node (credibility-building toward her later resurrecting
  Jon) but cut as the weakest/most-diffuse interpretive link in the set; general
  "she's been right before" doesn't specifically speak to resurrection.
- **B71** (Great Other/no-Night's-King lore, asos-davos-03.md:69) — real and
  well-grounded (Melisandre's full R'hllor-vs-Great-Other cosmology speech), but
  tangential to Jon specifically; flagged as "weak" in the substrate itself.
  Excluded from edges; pointed to the harvest queue instead (it's a strong quote
  for a future R'hllor/Great Other node, not for this theory).
- **B75** — same line as B64/JR12 (adwd-jon-03.md:217); kept only the Nissa-Nissa
  tempering half (JR12), dropped the monster-slaying half as redundant restatement
  of the same sacrifice-precedent point from the same passage.
- **B81** — redundant with Z6 + stance-label mismatch (see dedup notes above).
- **B86** (wildling-exile "third path," asos-jon-05.md:49) — explicitly "weak"
  strength in the substrate, no clear stance (sub_claim: null), and doesn't fit a
  SUPPORTS/CONTRADICTS relationship with either target — it's an alternative-ending
  possibility that bypasses the whole resurrection/prophecy question rather than
  supporting or contradicting it. Excluded; mentioned in the node's Evidence
  Against section as considered-and-set-aside, not as an edge.

## Judgment calls flagged for the orchestrator

1. **JR1 and JR8 are not substrate rows.** JR1 (Jon's dying word "Ghost",
   adwd-jon-13.md:325) is the single most load-bearing quote in the whole cluster
   and was specifically anticipated by the orchestrator's own design note about the
   assassination scene as the natural subject-link anchor — I found and used the
   more precise "Ghost" line rather than the event node's own pre-existing Quotes
   citation (line 323, the stabbing itself) because it's a tighter match to THIS
   theory's specific claim. JR8 (adwd-jon-01.md:317, "grave need of me") was found
   incidentally while verifying B48 and directly strengthens the same beat. Both are
   byte-verified and on-theory, not off-task finds, so I included them as edges
   rather than harvest-queue pointers — flagging here in case the orchestrator wants
   them held to a stricter substrate-only standard instead.
2. **B42 (wolf blood) cut for scope, not weakness-of-grounding.** See exclusions
   above — restorable as a tier-5 edge if the orchestrator wants deeper crackpot
   coverage.
3. **Edge count is 16, not "roughly 10-16."** Landed exactly at the top of the
   guided range across both targets (13 new-node + 3 azor-ahai-theories). I trimmed
   B42 and B68 specifically to stay inside it rather than run to 18.
4. **JR13's source is the `last-hero` character node**, not an event. The Last
   Hero has no confirmed on-page event distinct from the legend itself (it's
   recounted, not witnessed) — sourcing the legend's own node felt more correct
   than inventing an event, but flagging the choice since it's a slightly different
   shape than this session's other "confirmed event anchors" evidence chain.
5. **No CONTRADICTS edges landed on the new node itself.** All 13 `jon-snow-
   resurrection` edges are SUPPORTS. The design note suggested CONTRADICTS "where
   the substrate carries counter-evidence (e.g. Bloodstone Emperor / dark-AA
   counter-legends if grounded)" — the Bloodstone Emperor material in this video's
   transcript wasn't grounded to a specific book quote in the substrate I was
   given, so I didn't force one. The closest counter-evidence (B81, B86) got
   excluded for the reasons above rather than forced into a weak CONTRADICTS slot.

## Harvest queue

Two off-task-but-notable finds while verifying chapter text, pointed (not extracted)
to `working/theories/harvest-s219-jr.md`:
- Melisandre's full R'hllor-vs-Great-Other cosmology speech (asos-davos-03.md:69,
  the B71 beat) — strong candidate for a future R'hllor or Great Other node's Quotes
  section, not used here since it's tangential to Jon specifically.
- Old Nan's Others-lore description (agot-bran-04.md:47, adjacent to the Last Hero
  passage used in JR13) — vivid physical description of the Others themselves,
  useful for an Others/White Walkers node.

## Files produced

- `working/theories/jonsnow-cluster/resurrection/PROPOSAL.md` (this file)
- `working/theories/jonsnow-cluster/resurrection/candidates.json` (16 edges, JR1–JR16)
- `working/theories/jonsnow-cluster/resurrection/nodes/jon-snow-resurrection.node.md`
- `working/theories/harvest-s219-jr.md` (2 pointers)
