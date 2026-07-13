# Jojen Paste cluster — build proposal (S216)

**Status:** STAGING ONLY. No graph mutation. All files confined to
`working/theories/jojen-cluster/`. Mint gate: pending Matt (standing rule since S214 —
a dry-run/design pass earns confidence, not a mint).

## Summary

One new `concept.theory` node: `jojen-paste` ("Bran's weirwood paste contains
Jojen"), tier-4, `status: open`. Source: single ASX video EhtbVpc8E70 ("Jojen Paste:
does Bran eat Jojen?"). 9 edges (8 SUPPORTS, 1 CONTRADICTS; 5× tier-3, 4× tier-4)
drawn from 6 distinct existing graph nodes.

This is the grimmest/most speculative of the three S216 wave-1 clusters — a
symbolic/thematic reading with, per the source video's own words, "no direct textual
confirmation either way." Tier-4 (not tier-3) reflects that honestly: unlike R+L=J
(multiple independent corroborating POVs, a named textual motif tracked across
books) or the Grand Northern Conspiracy (anchored to a tier-1 event node), this
theory's evidence is entirely circumstantial and internal to one chapter plus
series-wide thematic pattern-matching.

## Edge list

| id | type | source | tier | anchor |
|---|---|---|---|---|
| J1 | SUPPORTS | weirwood-paste | tier-3 | paste's blood-like red veins |
| J2 | SUPPORTS | jojen-reed | tier-3 | "My task was to get you here. My part in this is done." |
| J3 | SUPPORTS | meera-reed | tier-3 | "He will not even try and fight his fate." |
| J4 | SUPPORTS | jojen-reed | tier-4 | Jojen "ever more sullen and solitary" |
| J5 | SUPPORTS | bran-stark | tier-4 | "Only he was, in a way" (ASOS foreshadowing, ambiguous pronoun) |
| J6 | CONTRADICTS | brynden-rivers | tier-3 | "Your blood makes you a greenseer" — stated purpose attributes blood to Bran, not an ingredient |
| J7 | SUPPORTS | bran-stark | tier-3 | same-chapter human sacrifice vision, Bran tastes blood |
| J8 | SUPPORTS | jojen-reed | tier-3 | Jojen/Meera's alcove "cold and empty" right after the paste scene |
| J9 | SUPPORTS | rat-cook | tier-4 | Rat Cook legend — unknowing-cannibalism precedent in Bran's own arc |

Source-slug diversity: `weirwood-paste` (existing `object.food` node — useful find,
already carries two of the same block quotes independently), `jojen-reed` ×3,
`meera-reed`, `bran-stark` ×2, `brynden-rivers`, `rat-cook` (an existing `texts`
node — the in-world Rat Cook legend, a nice structural parallel to how R+L=J used
`combat-at-the-tower-of-joy` and `crowning-of-lyanna-at-harrenhal` event nodes as
edge sources).

All 9 quotes independently grep-verified against `sources/chapters/*.md` at the
cited lines by this session (Python exact-substring check, see below) — not just
inherited from the regrounding/regrounding-agent substrate, though every quote used
does trace back to a "matched"/"exact" row in `regrounding/EhtbVpc8E70.jsonl` or a
"grounded" row in `regrounding-agent/EhtbVpc8E70.jsonl`.

```
J1: FOUND in sources/chapters/adwd/adwd-bran-03.md
J2: FOUND in sources/chapters/adwd/adwd-bran-03.md
J3: FOUND in sources/chapters/adwd/adwd-bran-03.md
J4: FOUND in sources/chapters/adwd/adwd-bran-03.md
J5: FOUND in sources/chapters/asos/asos-bran-01.md
J6: FOUND in sources/chapters/adwd/adwd-bran-03.md
J7: FOUND in sources/chapters/adwd/adwd-bran-03.md
J8: FOUND in sources/chapters/adwd/adwd-bran-03.md
J9: FOUND in sources/chapters/asos/asos-bran-04.md
ALL FOUND (9/9)
```

## Held-out / dropped material

- **False-positive grounding caught and excluded.** `jojen-B33` in the raw
  extraction ("Sansa realizes Cersei is a 'vile, scheming, evil bitch'") was
  deterministically matched to `affc-cersei-10.md:173` by keyword search — but that
  line is **Kevan Lannister** speaking to Cersei, not a Sansa POV thought. The
  paraphrase and the matched quote describe two different things. No edge minted;
  documented in the node's `## Ungrounded material` as a caught misattribution
  rather than silently dropped.
- **`jojen-B23` (Coldhands feeds Bran human flesh as "pork")** — a load-bearing beat
  in the video's cannibalism-precedent argument, but `regrounding-agent` marked it
  `ungrounded` ("could not locate explicit textual confirmation in ASOS Bran
  chapters"). Not used anywhere, not even as prose citation — fenced in
  `## Ungrounded material` as unconfirmed.
- **`jojen-B14/B15/B18/B19/B25` (ungrounded)** — Euron's ship-blood-sacrifices,
  Skagosi human sacrifice, Stannis's soldiers eating their dead, Wyman Manderly's
  Frey pies, and Bran-eats-a-friend-elk are all plausible ASOIAF beats the video
  cites but none could be grounded to a specific passage in this session's
  substrate. Named in `## Ungrounded material` as book-plausible-but-unsourced,
  not used as edges or block quotes.
- **`jojen-B34` ("Coldhands is a monster")** — `no-match` status in both regrounding
  passes; not used.
- **`jojen-B35` (Bran warging Hodor without consent)** — grounded
  (`adwd-bran-03.md:113`), but it's about Bran's general moral trajectory, not
  about the paste theory specifically. Held out — mentioned only in passing inside
  the literary-parallel `## Ungrounded material` bullet, no independent citation.
- **`jojen-B36` (show divergence)** — fenced **show**, no edge, per hard rules.
- **`jojen-B37` (video's own "no strong direct evidence" hedge)** — this is the
  video's own meta-commentary about its argument, not a book passage; used only in
  `## Status Notes` as the ASX verdict, exactly like R+L=J's convention, never as an
  edge.
- **B01/B02 atmosphere** — chapter-opening dark imagery and the "moon was a
  crescent" refrain (claimed by the video to recur 4×; only 2 occurrences were
  located: lines 11 and 47) are named in `## Ungrounded material` as mood-setting,
  explicitly not asserted as edges (single motif recurrence, pure atmosphere).
- **B26–B32b (Bloodraven characterization, Leaf's claimed benevolence)** — cited in
  node body prose with citations but deliberately NOT minted as edges: they
  characterize Bloodraven/the children of the forest generally (creepy mentor,
  ambiguous motives) without naming Jojen or the paste. Per the hard-rule ban on
  atmosphere-only edges.

## Open questions for Matt (mint-gate review)

1. **Tier-4 node confidence.** Is tier-4 the right call for the overall node, given
   the video's own "no direct textual confirmation either way" hedge? (R+L=J shipped
   tier-3; GNC shipped tier-4; this one leans GNC's direction, arguably weaker still
   since GNC is anchored to a tier-1 event node and this one anchors to nothing
   tier-1/2.)
2. **J6 (CONTRADICTS) framing.** Is scoping the Brynden "your blood" line as
   CONTRADICTS-but-not-dispositive the right register, or should it instead be
   demoted to premise prose (like R+L=J's Bran-07:79 treatment) since Brynden's
   unreliability as a narrator-of-his-own-motives is itself asserted rather than
   textually proven?
3. **`weirwood-paste` node reuse.** This is the first wave-1 theory to attach an
   edge to a pre-existing Pass-2 wiki node (`object.food` type) rather than only to
   character/event nodes. Worth flagging as a precedent if a future cluster needs
   the same pattern.
4. **Rat Cook as edge source.** Is treating `rat-cook` (a `texts` node — an in-world
   legend, not a character/event) as a valid SUPPORTS source consistent with how the
   graph wants theory-adjacent edges typed, or should legend/text nodes stay
   edge-target-only?

## HARVEST

(Notable off-task finds while reading the substrate — pointers only, not extracted.)

- `sources/chapters/adwd/adwd-bran-03.md:113` / description / Bran wargs into Hodor
  and makes him explore the caves without Hodor's consent ("I felt the real Hodor
  stir down in his pit") — a clean textual beat for any future Bran-agency/consent
  or Hodor-arc enrichment dip; not used here (held out of this theory).
- `sources/chapters/adwd/adwd-bran-03.md:91` / worldbuilding / Leaf's line "we have
  lived here for a thousand thousand of your man-years" — a striking, very large
  children-of-the-forest longevity/timescale claim, possibly useful for a
  children-of-the-forest chronology or origins enrichment dip.
- `sources/chapters/asos/asos-bran-04.md:129` / food / Rat Cook's pie recipe detail
  ("onions, carrots, mushrooms, lots of pepper and salt, a rasher of bacon, and a
  dark red Dornish wine") — a rich, specific in-world recipe; flagged per the
  food/hospitality-is-first-class-extraction-target design value, not previously
  captured on the `rat-cook` node's own file (worth a look for a future food-pass).
- `sources/chapters/affc/affc-cersei-10.md:173` / dialogue / Kevan Lannister calling
  Cersei "you vile, scheming, evil bitch" — a sharp, quotable Kevan/Cersei
  confrontation line, misidentified by the source video's paraphrase as a Sansa
  thought (see Held-out above); worth a look for a Kevan-Cersei relationship
  enrichment dip on its own merits, independent of this theory.
