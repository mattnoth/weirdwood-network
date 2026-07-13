# A+J=T (Tyrion Targaryen) cluster — proposal (S216)

**Status: STAGING ONLY. No graph mutation.** All files under
`working/theories/ajt-cluster/`. Mint gate per Matt's standing S214 decision — no
mint of any theory node without explicit go.

## Source

ASX video `eqVhKOxmJCw` ("Tyrion Targaryen: is Tyrion the Mad King's son?"),
substrate: `working/theories/extractions/eqVhKOxmJCw.jsonl` (29 rows: 1 theory
header + 28 beats) → `working/theories/regrounding/eqVhKOxmJCw.jsonl` (deterministic
pass) → `working/theories/regrounding-agent/eqVhKOxmJCw.jsonl` (agent pass, 9
`grounded` rows out of 28 beats).

This is a markedly thinner substrate than R+L=J: only 9/28 beats grounded to a
verbatim book quote (vs. R+L=J's much richer hit rate), and the video's own verdict
is skeptical ("possible but quite unlikely ... no strong evidence"). The node's
`confidence: tier-4` and the edge set reflect that.

## Build

**Node:** `nodes/a-plus-j-equals-t.node.md` — slug `a-plus-j-equals-t`, type
`concept.theory`, tier-4, `status: open` (the show never engaged this theory —
Tyrion stayed Tywin's biological son on screen — so there is no show-confirmed/
jossed basis; the books haven't resolved it either).

**Edges (5, candidates.json):**

| id | type | source | target | tier | basis |
|---|---|---|---|---|---|
| A1 | SUPPORTS | barristan-selmy | a-plus-j-equals-t | tier-4 | Barristan's wedding-night "liberties" account (adwd-daenerys-07:339) |
| A2 | SUPPORTS | tywin-lannister | a-plus-j-equals-t | tier-4 | Cisterns punishment predates Tyrion's vices (adwd-tyrion-03:165) |
| A3 | SUPPORTS | tywin-lannister | a-plus-j-equals-t | tier-4 | Tywin's dying words "no son of mine" (asos-tyrion-11:263) |
| A4 | CONTRADICTS | genna-lannister | a-plus-j-equals-t | tier-3 | Genna's plain "Tyrion is Tywin's son" (affc-jaime-05:325) |
| A5 | CONTRADICTS | tywin-lannister | a-plus-j-equals-t | tier-4 | Tytos-mistress/Shae mirror, alternate explanation (affc-cersei-01:105) |

Tier mix: 1× tier-3, 4× tier-4 — matches the task's explicit steer that this theory
is weaker-evidenced than R+L=J. Source slugs verified live: `barristan-selmy`,
`tywin-lannister`, `genna-lannister` all resolve to `graph/nodes/characters/`.

**The Tywin/Genna pair, typed honestly (per task instruction, not forced to agree):**
A3 (Tywin's dying "no son of mine") is typed SUPPORTS but held to tier-4 because the
scene reads at least as plausibly as a dying insult as a literal paternity denial —
Tyrion's own reply ("I believe I'm you writ small") cuts against a literal reading.
A4 (Genna's "Tyrion is Tywin's son, not you") is typed CONTRADICTS at tier-3 because
it is a flat, unhedged statement with no similar ambiguity in its immediate context,
even though the video itself reframes it as recognition-of-temperament rather than
literal-paternity commentary — the line's plain meaning is what's edged.

## Held-out / not edged

- **B01/B04 (Barristan's "wanted"/"kitchen gossip" framing, adwd-daenerys-07:335)** —
  explicitly self-hedged by Barristan in-text ("it was only kitchen gossip, the
  whispers of washerwomen and stableboys"). Per the no-edges-from-self-hedged-rumors
  rule (eldritch-cluster E10 precedent), this is premise prose in the node body, not
  an edge. Only the unhedged continuation of the same conversation (the "liberties"
  clause) is edged as A1.
- **B20 ("seed is strong" / Tyrion's hair)** — the grounded quote
  (agot-eddard-12.md:133) is real but belongs to an unrelated plotline (Ned's
  investigation of Cersei's children via Robert's black-haired bastards); no passage
  applies the principle to Tyrion or describes his hair as Targaryen-silver. Held out
  as `book-speculative` in Ungrounded material, not edged — an analogy borrowed
  across plots rather than a beat about Tyrion himself.
- **B18/B19 (Targaryen dragon-dream pattern vs. Tyrion's plain fondness for
  dragons)**, **B21 (mismatched eyes / Shiera Seastar, Dunk & Egg)**, **B22
  (dwarfism as Targaryen weirdness/abortion, community)**, **B23/B24 (three heads of
  the dragon prophecy fit + prophecy-reliability meta-argument)** — all ungrounded
  (no verbatim quote in the substrate), fenced in Ungrounded material with domain
  labels (`book-speculative` ×4, `community` ×1). B23/B24 are the prophecy
  extension, deliberately scoped separately from the parentage core per the task
  instruction (mirrors R+L=J's throne-claim fencing).
- **B03, B05–B09, B11, B13–B17, B26 (timeline objections, comparative-treatment
  arguments, vice-mirroring framing)** — all ungrounded interpretive arguments from
  the video with no matching book quote. These are on-topic (not out-of-corpus), so
  per the R+L=J precedent (its own "further complications ... could not be grounded"
  paragraph) they're folded into Evidence For / Evidence Against as prose, not moved
  to Ungrounded material and not edged.
- **`aegon-targaryen-son-of-rhaegar-theories` (Young Griff)** — confirmed as a
  separate, untouched stub; not read or used as a source for this cluster.

## Open questions for the eventual validation review

1. Is A3's tier-4/SUPPORTS-with-heavy-caveat the right call, or should Tywin's dying
   words be dropped to prose entirely given how strongly the immediate context reads
   as insult rather than genealogical claim? (Chose to keep as an edge, honestly
   caveated, rather than drop — parallel to R+L=J's T6 "kept weaker, not dropped"
   precedent — but this is a closer call than T6's.)
2. Only 5 edges landed (low end of the 5–10 range) — a genuine reflection of how thin
   this theory's grounded substrate is, not a shortfall in search effort. Confirm
   that's an acceptable outcome rather than a signal to loosen the self-hedged-rumor
   rule for B01/B02.
3. No GRRM-interview material surfaced in this video's beats (unlike R+L=J) — nothing
   fenced under that label. Confirmed absence, not an oversight.

## HARVEST

- `sources/chapters/adwd/adwd-daenerys-07.md:331` / character quote / Barristan's own
  confession of unspoken love for Queen Rhaella ("he became most pious, and was heard
  to say that only the Maiden could replace Queen Rhaella in his heart") — found
  while reading the A1 context, off-task for this theory; candidate for
  `barristan-selmy` node's Quotes section.
- `sources/chapters/affc/affc-cersei-01.md:101` / descriptive parallel / Shae's
  strangled corpse explicitly compared to Joffrey's poisoned death-face ("her face,
  which had turned as black as Joff's had at his wedding feast") — found while
  reading the A5 context, off-task for this theory; candidate cross-event imagery
  link between the Purple Wedding and Shae's murder.

## Gates run this session

- All 6 body blockquotes + all 5 candidates.json edge quotes byte-verified against
  `sources/chapters/*.md` at cited lines (python substring check, exact Unicode
  including curly quotes/ellipses).
- `candidates.json` validated as well-formed JSON, 5 edges.
- All 3 edge-source slugs (`barristan-selmy`, `tywin-lannister`, `genna-lannister`)
  confirmed to resolve to live `graph/nodes/characters/*.node.md` files.
- No tier-1/2 anywhere in staged artifacts (node tier-4; edges 1× tier-3 + 4× tier-4).
- Claim opens "The theory holds that ..."; no sentence in the node states the theory
  as settled fact.

**Mint gate (not run):** on Matt's explicit go —
`scripts/mint_enrichment.py --candidates working/theories/ajt-cluster/candidates.json
--nodes-dir working/theories/ajt-cluster/nodes` + `weirwood refresh` +
architecture.md sync (shared `concept.theory` frontmatter fields already documented
via the R+L=J batch).
