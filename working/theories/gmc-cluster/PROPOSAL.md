# Grand Maester Conspiracy cluster — proposal (S216, staging-only)

**Status: STAGED, NOT MINTED.** Nothing here is written to `graph/`. All output
lives under `working/theories/gmc-cluster/`. Mint gate awaits Matt's explicit go
per the standing theories-track rule (staging-only, S214/S216).

## What was built

`nodes/grand-maester-conspiracy.node.md` — a new `concept.theory` node, slug
`grand-maester-conspiracy`, verified free against `graph/nodes/**` before minting.
Claim: tier-4, status `open`. `## Claim` opens "The theory holds that…" per the
hard rule. Body sections: Claim / Evidence For / Evidence Against / Ungrounded
material / Status Notes, matching the R+L=J / GNC / eldritch-apocalypse exemplars.

`candidates.json` — 11 edges (M1–M11), 8 distinct source nodes (`pycelle` and
`cressen` each appear twice — once SUPPORTS, once CONTRADICTS, mirroring the same
maester's own confessed motive against the theory's reading of his action; this
directly follows the R+L=J T7 / GNC G12 scoped-CONTRADICTS precedent). All 8
source slugs verified to resolve against live `graph/nodes/**/*.node.md` files.
All 11 quotes verified byte-exact against `sources/chapters/*.md` at the cited
line via a Python substring check (see Gates below) — three initial drafts
(M2, M5, M11) failed on first pass (an elided non-adjacent sentence spliced with
"…" in M2, a straight vs. curly apostrophe in M5, a trailing period where the
source has a comma in M11) and were corrected to exact substrings before the
final 11/11 pass.

## Edge summary

| id | type | source | tier | sub-claim |
|---|---|---|---|---|
| M1 | SUPPORTS | barbrey-dustin | 3 | mechanism thesis ("grey rats" general distrust) |
| M2 | SUPPORTS | walys-flowers | 3 | sub-claim 0 — Robert's Rebellion angle |
| M3 | SUPPORTS | marwyn | 3 | sub-claim 1 — maesters killed the dragons |
| M4 | SUPPORTS | marwyn | 3 | sub-claim 2 — anti-magic world-building |
| M5 | SUPPORTS | pycelle | 3 | maester hand in the Sack of King's Landing |
| M6 | SUPPORTS | cressen | 4 | sub-claim 2 case study — poison for Melisandre |
| M7 | SUPPORTS | quaithe | 4 | magic returning despite the Citadel's project |
| M8 | CONTRADICTS | pycelle | 3 | M5's motive was Lannister loyalty, not ideology |
| M9 | CONTRADICTS | cressen | 3 | M6's motive was fatherly love, not doctrine |
| M10 | CONTRADICTS | luwin | 3 | official Citadel position is skepticism, not fear |
| M11 | CONTRADICTS | daenerys-targaryen | 4 | magic's decline predates any maester agency |

Tier split: 8× tier-3, 3× tier-4, 0× tier-1/2 anywhere in staged artifacts (node
`confidence: tier-4`, matching the ASX video's own hedged verdict). Two genuine
CONTRADICTS pairs (M5/M8 on Pycelle, M6/M9 on Cressen) directly reproduce the
source video's own move — it tests Pycelle and Cressen as case studies and finds
personal motive sufficient in both — so the node's evidentiary shape mirrors the
theory's own honest self-testing rather than only compiling one-directional
support.

## Source slugs used

`barbrey-dustin`, `walys-flowers`, `marwyn` (×2), `pycelle` (×2), `cressen` (×2),
`quaithe`, `luwin`, `daenerys-targaryen`. All existing character nodes (tier-1
confidence at the node-entity level); none of the specific claims cited as
edge evidence are already asserted as established fact in those nodes' own prose
(layer-rule check performed individually — see below).

## Layer-rule check (S216 convention)

Before minting, I read each candidate source node's existing prose to check
whether the fact I wanted to cite was already owned as confirmed content:

- **walys-flowers** (M2): the node's `## Origins` states only the neutral
  biographical facts (Hightower/archmaester parentage, posting to Winterfell under
  Rickard Stark). The claim that he engineered the Tully marriage lives *only*
  inside a `## Quotes` block attributed to Barbrey Dustin — i.e. it is already
  flagged on the node as a character's allegation, not narrator-confirmed fact.
  Clear to use as theory evidence.
- **marwyn** (M3/M4): the node's own `## Quotes` section already carries the
  "no place in it for sorcery or prophecy or glass candles" line with the
  annotation *"theory-adjacent, attached as evidence-only"* — a prior pass had
  already flagged this exact quote as theory-relevant without minting a formal
  edge. This cluster completes that flag rather than duplicating owned fact: the
  node records the quote: this build supplies the edge.
- **pycelle, cressen, luwin, daenerys-targaryen, quaithe, barbrey-dustin**: all
  standard wiki-sourced character nodes with no pre-existing prose asserting any
  of these specific claims as confirmed fact. Clear to use.

No existing tier-1/2 event node in the graph already owns "maester conspiracy
against Targaryens/dragons/magic" as a confirmed fact (unlike the GNC cluster,
where a tier-1 `grand-northern-conspiracy` event node already existed) — there is
no analogous event-layer node here to fold quotes into as premise, so all grounded
beats stayed available as edges.

## Held-out material

Fenced in the node's `## Ungrounded material (outside the corpus)` section,
domain-labelled:

- **twoiaf** — the historians'-grudge motive argument (maesters uniquely aware of
  Targaryen-caused damage; several Grand Maesters killed by Targaryen kings); the
  counter-argument that Aemon went to the Wall to protect his brother King Aegon V
  politically, not from Citadel distrust; the claim a Targaryen has served as
  archmaester before.
- **fab** — the detailed 21-dragon death count from the Dance of the Dragons;
  Grand Maesters Orwyle and Runciter trying to *prevent* the Dance; the
  Mushroom/Septon-Eustace/Runciter multi-source corroboration argument against a
  maester history-cover-up (real *Fire & Blood* text, byte-verified at
  `sources/chapters/fab/fab-heirs-of-the-dragon-15-p02.md:15`, but judged too
  indirect — evidence about historian reliability in general, not the conspiracy
  itself — to mint as an edge; cross-referenced by node name only, per the
  gnc-cluster Arnolf-Karstark precedent); House Hightower's role in starting the
  Dance and its otherwise-documented Targaryen loyalty.
- **community** — dragon-hatchling poisoning speculation; Pycelle's doddering act
  as possible deception; Marwyn's claims as possibly self-serving/exaggerated.
- **book-interpretive** — the Hightower/Dance-of-Dragons "manipulated the same way
  as the Starks" analogy (the video's own extrapolation, not a stated parallel);
  the Citadel-convergence beat (Sam, Jaqen, Sarella-as-Alleras, Euron's raids
  toward Oldtown) — real, verifiable plot setup, but structural "more will be
  revealed" foreshadowing rather than evidence of the conspiracy's content, so
  kept out of the edge set as atmosphere.

Also explicitly **not minted as an edge**: beat maester-B47 (the Citadel
convergence) and the Mushroom/Runciter corroboration beat (B23) — both discussed
above, both judged too indirect for an edge despite being individually
groundable quotes.

## Open questions for the orchestrator

1. **Two double-edged sources (Pycelle, Cressen)** — this build leans into the
   scoped-CONTRADICTS convention twice on purpose, since the source video
   structures its own skepticism around exactly these two case studies. Flag if
   the orchestrator would rather cap a cluster at one double-edged source for
   edge-count discipline.
2. **Quaithe (M7) is one inferential step removed** from the conspiracy itself
   (it evidences "magic is returning," not "the maesters are conspiring against
   it") — kept at tier-4 with an explicit note on the inferential gap rather than
   dropped, since it is a clean, distinct, well-corroborated source (independent
   of Marwyn, same year, same conclusion). Flag if this reads as too indirect and
   should be prose-only instead.
3. **No subject-link edge** to any existing graph node about the Citadel or the
   Dance of the Dragons — same open gap the R+L=J and GNC reviews already flagged
   twice and declined to resolve with a new convention; not re-litigated here.

## Harvest

- `sources/chapters/affc/affc-samwell-05.md:189` / description / Marwyn's full
  physical introduction (chain of many metals, "dockside thug" look, sourleaf-
  stained teeth) — vivid character-description beat, only partially used (chain
  detail only) in this node's prose; good standalone material for a future
  Marwyn/Citadel character-enrichment dip.
- `sources/chapters/affc/affc-samwell-05.md:197` / quote / the glass-candle
  demonstration itself: "Call it dragonglass. … It burns but is not consumed." —
  not used as an edge here (folded into node context only); good anchor quote for
  a future dedicated `glass-candle` artifact/mechanism node if one is ever built.
  Distinct from the M7 edge, which uses Quaithe's separate "glass candles are
  burning" line instead.
- `sources/chapters/acok/acok-prologue.md:253` / quote / Cressen's horror at
  fratricide: "Fratricide . . . my lord, this is evil, unthinkable . . . please,
  listen to me." — used only as a supporting citation in Evidence Against prose,
  not independently edged; strong standalone Stannis/Renly-relationship beat for
  a future Stannis or Renly enrichment dip.
- `sources/chapters/affc/affc-samwell-05.md:175` / quote / "Samwell. A new
  novice, come to see the Mage." — the first line of Sam's arrival at the
  Citadel; pointer only, not extracted; part of the held-out Citadel-convergence
  beat (B47).
