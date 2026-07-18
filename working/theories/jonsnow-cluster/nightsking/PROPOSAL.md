# PROPOSAL — Night's King parallel (jonsnow-cluster, S219)

Staging-only proposal. Nothing here is minted. Written under
`working/theories/jonsnow-cluster/nightsking/`; enrich target is the live
`graph/nodes/theories/nights-king-theories.node.md` stub (not touched by this
session).

## What this is

The ASX video "The real Jon Snow" (qSy2uaJ7ecU) carries a "Night's King parallel"
header theory: the historical Night's King legend (a Lord Commander who married a
corpse-queen figure and sacrificed to the Others, possibly ending the first Long
Night via pact rather than battle) may repeat with Jon Snow, who could be
tempted/pressured into a similar marriage-and-sacrifice bargain, with the wildling
Val floated as a possible corpse-queen analog. The video's own verdict is that
this would be a temptation Jon should refuse, not a prediction.

## Substrate integrity

`working/theories/jonsnow-cluster/substrate.jsonl` carries exactly **one** row
tagged `"theory": "Night's King parallel"`: `jonsnow-B92` (Craster's sacrifice of
his sons — "He gives his sons to the wood.", `acok-jon-03.md:371`, byte-verified,
`grounded_by: redo-s219-worker-2.jsonl`).

I traced this back to the full raw extraction
(`working/theories/extractions/qSy2uaJ7ecU.jsonl`) to confirm nothing was silently
dropped between the raw video-derived beats and the substrate. The theory's header
is line 4 of that file (claim + 2 sub_claims + asx_verdict + notes — reproduced in
full in the node's `## Claim` and `## Status Notes`). Nine beats carry this theory
tag (`jonsnow-B89` through `jonsnow-B97`):

| beat | domain | stance | grounding outcome |
|---|---|---|---|
| B89 | grrm | supports | never sent to grounding (not book-domain) |
| B90 | grrm | supports | never sent to grounding (not book-domain) |
| B91 | book (ADWD, Patrek "hospitality" line) | supports | **attempted, failed** — `working/theories/regrounding-agent/redo-s219-worker-2.jsonl`: "tried 'Patrek' + 'King's Mountain' + 'hospitality', tried 'white walkers' + 'hospitality' + 'joking'; no canonical Patrek of King's Mountain with hospitality line in corpus" |
| B92 | book (legend of the Night's King) | supports | **grounded** — the sole survivor, becomes NK3 |
| B93 | community | supports | never sent to grounding (not book-domain) |
| B94 | community | supports | never sent to grounding (not book-domain) |
| B95 | community | supports | never sent to grounding (not book-domain) |
| B96 | community | contradicts | never sent to grounding (not book-domain) |
| B97 | grrm | contradicts | never sent to grounding (not book-domain) |

This confirms the "1 byte-verified beat" the task brief flagged is not a gap in
this session's work — it's the accurate result of the substrate's own domain
gating (only book-domain beats get grounding attempts) plus one honest grounding
failure (B91). Nothing was skipped or under-searched. I did not attempt to
independently re-ground B91 myself beyond what the redo worker already tried
(searched the same terms in `sources/chapters/adwd/` mentally against what I know
of the text; the worker's search terms were reasonable and I have no reason to
believe a different search would succeed) — flagging this as a judgment call
rather than re-running the search myself, since the design brief scoped
independent grounding to the *legend text*, not to re-attempting failed
substrate beats.

## What I built beyond the substrate: the legend text itself

The task brief correctly identified that the Night's King legend is independently
groundable from `sources/chapters/asos/asos-bran-*.md` regardless of the video
substrate, since it's Old Nan's tale told to Bran at the Nightfort (ASOS, Bran
POV). I grepped `asos-bran-04.md` for "Night's King," "thirteenth," "corpse
queen," "blue stars," "forbidden," "forgotten" and found the full legend at lines
99–105 — the same passage the existing `nights-king` character/legend node
already *summarizes* in its Origins prose but had not directly quoted at these
specific lines (its own `## Quotes` section quotes lines 44 and 105, not 101 or
103).

I used this to build two edges (NK1, NK2) sourced from the `nights-king` node
into `nights-king-theories`, following the exact subject-link pattern the azor
cluster used (Z1: `azor-ahai` → `azor-ahai-theories`, Melisandre's prophecy
recitation as the candidate-neutral premise-setting edge):

- **NK1** (line 101): the core marriage/corpse-queen/sacrifice-to-Others/erasure
  passage — the theory's entire premise in one paragraph. Tier-3, matching Z1's
  precedent exactly.
- **NK2** (line 103): Old Nan's own preferred ending to her tale — "He was a
  Stark, the brother of the man who brought him down." Tier-4 (see judgment call
  below).

I stopped there rather than mining further into the chapter for more legend
material — the design capped this at "possibly 1 more legend-text edge," and I
judged NK2 satisfies that without stretching into padding. (Other legend-adjacent
material in the same chapter — the Rat Cook, Danny Flint, Mad Axe, Symeon
Star-Eyes catalogue at line 19, and the "wildlings who would lay with the Others"
hearth-tale at `acok-jon-03.md:367` — is pointed to in
`working/theories/harvest-s219-nk.md`, not extracted here; it's a different
legend/theme, not this one.)

## Judgment calls flagged

1. **NK2's claim mismatch.** Sub_claim 0 of the header reads: "...with the Starks
   possibly descended from that union..." — i.e., House Stark descended FROM the
   Night's King/corpse-queen marriage. The book line I found and used ("He was a
   Stark, the brother of the man who brought him down") says something narrower
   and different: that the Night's King himself was Stark-born, in one telling of
   the tale, BEFORE the marriage — not that his union with the corpse queen
   produced Stark descendants. I used it anyway, as the closest groundable
   legend-text tying House Stark to the figure at all, but flagged the mismatch
   explicitly in both the edge's `note` field and the node body's prose, rather
   than silently treating it as confirming the "Starks descended from the union"
   sub-claim. Matt/a reviewer may prefer to cut NK2 entirely rather than accept
   this narrower substitution — I judged keeping-with-a-loud-caveat better than
   dropping a real, on-page, on-topic quote, but this is exactly the kind of call
   the brief asked me to surface rather than decide silently.

2. **NK3's tier (Craster, tier-4 not tier-3).** The underlying fact (Craster
   trades sons to the Others, Mormont confirms it) is rock-solid, on-page, tier-1
   material *as a fact about Craster*. But as evidence FOR the theory that *Jon*
   specifically may face/repeat this pattern, it's one inferential step removed —
   a precedent establishing plausibility, not direct evidence about Jon. I set it
   to tier-4 rather than tier-3 to keep that distinction honest, consistent with
   the design's explicit instruction that this cluster leans t4/t5. A reviewer
   could reasonably argue tier-3 instead (the azor cluster's Z14 kept tier-3 for
   a comparably-structured "confirmed on-page fact used as theory evidence" edge)
   — I lean t4 because Z14's fact (Dany's own sacrifice framing at the pyre) is
   about the actual candidate the theory names, while Craster's fact is about a
   different character used as an analogy.

3. **No 4th edge for the Jon-specific reading.** The design allowed a t4/t5 edge
   for "the Jon-parallel reading... ONLY if a grounded quote genuinely carries
   it." Nothing in the substrate or my own legend-text search grounds anything
   about Jon himself facing this choice — B91 (the one book-domain,
   Jon-adjacent beat) failed to ground. I did not manufacture a stretch edge to
   hit a target edge count; the Jon-specific reading (Val as corpse-queen analog,
   visions, magical pressure) stays entirely as domain-labelled body prose in
   `## Ungrounded material`, honestly reflecting that this is the theory's
   weakest-evidenced layer.

4. **Node display name.** The stub's original `name` field was the bare wiki
   page title, "Night's King/Theories." Following the ratified naming convention
   (claim-style display names) and the azor/KotLT/RLJ precedent, I renamed it to
   "Jon Snow may become a new Night's King" — a claim-style name capturing the
   theory's actual subject (Jon, not the historical legend, which already has its
   own `nights-king` node). Old title kept as an alias. Flagging this rename
   explicitly since it's a frontmatter change beyond pure edge-adding.

5. **No CONTRADICTS edges.** Both contradicts-stance beats (B96, B97) are
   community/grrm domain and were never sent to grounding by the substrate's own
   design (only book-domain beats get grounding attempts). I did not invent a
   book-domain CONTRADICTS edge to balance the node — the "Evidence Against"
   section states plainly that no on-page passage exists either way, since Jon's
   story ends (as of ADWD) before any such choice could be dramatized.

## Counts

- Edges proposed: **3** (NK1 SUPPORTS tier-3, NK2 SUPPORTS tier-4, NK3 SUPPORTS
  tier-4). 0 CONTRADICTS. 0 new nodes.
- Tier distribution: 1× tier-3, 2× tier-4, 0× tier-5.
- Sources touched: `nights-king` (×2, subject-link legend edges), `craster` (×1,
  the sole grounded substrate beat).
- Body-prose-only material: 6 of 9 header beats (B89, B90, B91, B93, B94, B95 are
  supports-stance-but-ungrounded; B96, B97 are the two contradicts-stance beats,
  also ungrounded) — all domain-labelled in `## Ungrounded material`.
- Harvest pointers logged: 4, in `working/theories/harvest-s219-nk.md` (Nightfort
  horror-legend catalogue at asos-bran-04.md:19, Old Nan's full rival-identity
  list at asos-bran-04.md:103, the separate "wildlings lay with the Others"
  hearth-tale at acok-jon-03.md:367, and a standalone Mormont line at
  acok-jon-03.md:381 for the `craster` node's own Quotes section).

## Files in this proposal

- `PROPOSAL.md` — this file
- `candidates.json` — 3 mint-ready edges (NK1–NK3), run_id
  `jonsnow-nightsking-theories-s219`, typed_by `curator-theories-wave2-s219`
- `enrich/nights-king-theories.node.md` — full rewritten stub (frontmatter
  slug/type preserved; name/claim/aliases/status/confidence/video_sources/body
  added)
