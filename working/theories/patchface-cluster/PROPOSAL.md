# Patchface cluster — build proposal (S216)

**Unit:** Theories wave-1 Patchface cluster. Pure enrich of the existing dark stub
`graph/nodes/theories/patchface-theories.node.md` (concept.theory). **No new node
minted.** Source: ASX video IZQOje3DdMk ("Patchface: the strangest Game of Thrones
character?"). **Graph mutation: NO** — all files confined to
`working/theories/patchface-cluster/`. Cluster is STAGED AT THE MINT GATE per the
standing Matt directive (2026-07-13): no mint without explicit review/go.

## Files produced

- `enrich/patchface-theories.node.md` — stub rewrite. `name`: "Patchface is a
  resurrected prophet of the Drowned God". `confidence: tier-4`, `status: open`.
  `node_version: 1 -> 2`. `wiki_source`, `bucket_id`, `prompt_version` preserved from
  the stub.
- `candidates.json` — 7 edges, `run_id: patchface-cluster-theories-s216`,
  `new_node_slugs: []`, `typed_by: curator-theories-wave1-s216`.
- This file.

## Edge summary (7, all SUPPORTS, no CONTRADICTS)

| id | source | target | tier | quote (short) |
|---|---|---|---|---|
| P1 | patchface | patchface-theories | tier-3 | "Fool's blood, king's blood..." (Red Wedding song) |
| P2 | patchface | patchface-theories | tier-4 | "merwives wear nennymoans..." (Purple Wedding song) |
| P3 | patchface | patchface-theories | tier-3 | "We will march into the sea and out again..." (Hardhome volunteering) |
| P4 | patchface | patchface-theories | tier-4 | "mermen feast on starfish soup..." (afterlife-lore echo) |
| P5 | melisandre | patchface-theories | tier-3 | "That creature is dangerous...skulls...blood" |
| P6 | moqorro | patchface-theories | tier-4 | "no more than a thrall of the Other..." |
| P7 | aeron-greyjoy | patchface-theories | tier-4 | "die and be reborn" (ironborn drowning ritual doctrine) |

Source slugs verified against live graph: `patchface`, `melisandre`, `moqorro`,
`aeron-greyjoy` — all resolve. Target `patchface-theories` resolves (the stub).
`quotecheck_enrichment.py` → **7/7 ALL FOUND** after two byte-fidelity fixes (see
Adjudications below). Tier audit: 3× tier-3, 4× tier-4, no tier-1/2 anywhere. Dry-run
mint on a scratch copy of `edges.jsonl` (never the live file) → **GREEN, 7 appended, 0
duplicates**; live `graph/edges/edges.jsonl` confirmed byte-identical
line-count before/after (26740).

## Adjudications made during the build (no separate ADJUDICATION file needed — folded
in here since this is a single-pass build, not a multi-agent review)

1. **B10 rejected as a Battle-of-the-Blackwater edge.** The ASX video reads
   Patchface's "smoke rises in bubbles, and flames burn green and blue and black" as
   predicting the Blackwater's wildfire. Byte-verification located the line at
   `sources/chapters/acok/acok-davos-01.md:43` — but read-through of the full chapter
   showed this is the burning-of-the-Seven / Lightbringer-forging scene (Stannis
   drawing the sword from the pyre, jade-green flames), not the Blackwater battle at
   all. The `patchface` character node already attributes this same recurring line to
   that same scene. No textual anchor ties it to the Blackwater; dropped to Ungrounded
   material rather than minted as a misleading edge.
2. **B21 (Aeron's own drowning-ritual chapter) rejected as a CONTRADICTS edge.** The
   video argues Aeron, despite believing himself the Drowned God's resurrected
   prophet, never produces real magic or prophecy — a contrast meant to make Patchface
   look more genuine. But the specific grounded quote (`affc-the-prophet-01.md:29`)
   only shows Aeron performing the ritual on a convert; it doesn't itself demonstrate
   Aeron's lack of magic. Using it as CONTRADICTS would misrepresent the quote's
   actual content (the R+L=J cherry-pick precedent this cluster was warned against).
   The line-13 half of the same chapter (Aeron's ritual instructions) was kept as a
   SUPPORTS edge (P7) for the doctrinal-parallel point instead, which the quote does
   support directly.
3. **Byte-fidelity fixes.** Two quotes initially failed `quotecheck_enrichment.py`:
   P4 had a trailing period where the source has a comma (mid-sentence, followed by a
   dialogue-attribution tag) — trimmed the trailing punctuation. P6 originally
   stitched two sentences ("Your Drowned God is a demon. He is no more than a
   thrall...") that are split in the source by a narration tag ("the black priest
   Moqorro said afterward") — split into a lead-in reference to the first sentence
   plus a standalone quote of the second. Both re-verified 7/7 ALL FOUND after the fix.
4. **Layer rule applied.** The shipwreck/resurrection origin story (washing up,
   "broken in body and mind," "half his wits and all his memory," the fisherfolk
   mermaid-gossip) is already fully catalogued on the tier-1 `patchface` character
   node's Origins section — treated as premise prose in the theory node's Claim/
   Evidence-For lead-ins, not re-edged. The theory's actual added value is the
   interpretive claim (songs = literal predictions; the resurrection was the Drowned
   God's doing, for a prophetic purpose) — edges target only that interpretive layer.

## Held-out material (full list also fenced in the node's Ungrounded material section)

- **sub-claim 2 (Deep Ones / Lovecraft fish-hybrid breeding)** — held out in full. Rests
  on a not-groundable out-of-book GRRM/Lovecraft-influence claim plus folklore
  ("squishers," mermaid-seed gossip) that never connects to Patchface beyond thematic
  resonance.
- **sub-claim 3 (greyscale plague / Shrouded Lord / stone-dragon prophecy)** — held out
  in full. Each individual beat (Shireen's greyscale backstory, Val's "not clean,"
  the Shrouded Lord lore, Shireen's stone-dragon dreams) is a real grounded quote, but
  the chain connecting them to "Patchface spreads a plague" is the video's own
  synthesis, and the ASX verdict itself calls this thread "pretty vague."
- B10 (Blackwater misattribution) and B23 ("Only death can pay for life" cross-book
  analogy) and B20 (Melisandre's general R'hllor/Great-Other cosmology speech) — real
  quotes, book-interpretive pattern arguments, not independently about Patchface;
  fenced as prose only.
- GRRM/TWOW promotional line closing the video — outside the published corpus,
  not-groundable.

## Open questions for review

1. **Node confidence tier-4 vs tier-3.** The ASX verdict calls the core
   resurrection/prophet claim "likely," and two edges (P1, P5) are tier-3 — but 5 of 7
   edges are tier-4 (circumstantial/analogical), and the theory is structurally
   unfalsifiable within the published text (no character ever confirms a song was a
   real prediction). Set node confidence to tier-4 to reflect the edge mode; flag for
   Matt if tier-3 (matching R+L=J's node-tier convention of "one better than the
   weakest edge") is preferred instead.
2. **No CONTRADICTS edge.** Unlike R+L=J (Jon's vow) and GNC (Wyman's
   can't-trust-a-maester line), this cluster's only candidate counter-evidence (B21,
   B28) both failed independent grounding for a CONTRADICTS framing (see
   Adjudications 2 above, and the Hardhome-unconfirmed point being fully owned by the
   tier-1 `hardhome-catastrophe` node already). This matches the eldritch-apocalypse
   cluster's precedent of an honestly one-directional video, but is worth a second
   look in case a stronger counter-argument exists in the substrate that this pass
   missed.
3. **Subject-link convention.** Like KotLT before the S216 GNC session settled a
   pattern (retargeting a SUPPORTS edge onto the confirmed event node to double as a
   subject-link), this node has no dedicated edge to `hardhome-catastrophe`,
   `red-wedding`, or `purple-wedding` as EVENT nodes — P1/P2/P3 all source from
   `patchface` instead, since the songs are his utterances, not narration of the
   events themselves. Flagging for consistency review against the GNC-cluster
   precedent (G1's retarget), in case Matt prefers a parallel event-node edge here too.

## HARVEST (off-task pointers found while reading substrate chapters)

- `sources/chapters/acok/acok-davos-01.md:43` / thematic-echo / Patchface sings "smoke
  rises in bubbles...flames burn green and blue and black" during the burning of the
  Seven / Stannis drawing "Lightbringer" from the pyre (jade-green flames match the
  song's colors exactly) — a clean textual anchor for a future Lightbringer/Azor Ahai
  theory unit; not used here since it's not about Patchface's own prophetic claim.
- `sources/chapters/agot/agot-daenerys-10.md:95` / motif / "Only death can pay for
  life" (Dany to Mirri Maz Duur, before Drogo's death-ritual) — the series' recurring
  sacrifice-magic refrain; worth tracking across any future sacrifice/resurrection
  theory unit (Beric, Catelyn/Lady Stoneheart, Jon).
- `sources/chapters/adwd/adwd-jon-11.md:223` / character-note / Val tells Jon Shireen
  "is not clean" — dormant greyscale warning, untouched greyscale-plague thread; could
  seed a future Shireen-focused arc-enrichment dip independent of the Patchface theory.
