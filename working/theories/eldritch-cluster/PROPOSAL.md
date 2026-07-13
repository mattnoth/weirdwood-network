# Eldritch Apocalypse cluster — S216 build proposal (staging only, no mint)

**Scope:** one new `concept.theory` node (`eldritch-apocalypse` / "Euron's Apocalypse") built
from the single ASX video `sbX_ak0N1EI` ("Euron Greyjoy's apocalypse in the Game of Thrones
books"). All files live under `working/theories/eldritch-cluster/`; no graph mutation.

## What was built

- `nodes/eldritch-apocalypse.node.md` — new theory node. `confidence: tier-4`, `status: open`
  (no show confirmation exists for this theory at all — GoT's final seasons never touched
  Euron's magic, the Bloodraven connection, or the Horn of Winter plot).
- `candidates.json` — 11 SUPPORTS edges, all byte-verified against `sources/chapters/*.md`
  with an automated script (every `quote` field confirmed as an exact substring of its cited
  chapter file — see Verification below), no CONTRADICTS edges (see below for why).

## Edge list summary

| id | source node | tier | what it grounds |
|---|---|---|---|
| E1 | euron-greyjoy | tier-3 | Euron's self-declared godhood ("godliest man ever to raise sail") |
| E2 | dragonbinder | tier-3 | The horn's claimed Valyrian origin + dragon-binding power |
| E3 | silence | tier-4 | The ship's uncanny, mouthless, mute design |
| E4 | moqorro | tier-3 | Moqorro's vision of Euron as a tentacled monster — strongest single published-book "eldritch" beat |
| E5 | melisandre | tier-4 | Melisandre's "towers by the sea" vision, read as Oldtown |
| E6 | victarion-greyjoy | tier-4 | Tentacle/puppet imagery around Victarion's manipulation |
| E7 | rodrik-harlaw | tier-4 | "History is a wheel" — cyclical-repeat framing (names Urron Greyiron, not Bloodstone Emperor) |
| E8 | horn-of-winter | tier-3 | Mance's horn confirmed fake; true horn still unfound |
| E9 | oldtown | tier-3 | Euron's raids already turning toward Oldtown |
| E10 | leyton-hightower | tier-4 | "Raise an army from the deeps" — hedged in-text rumor |
| E11 | daenerys-targaryen | tier-5 | "Eyes are amethysts" — weakest edge, single-word symbolism onto TWOIAF-only Bloodstone Emperor material |

Tier spread: 4×tier-3, 5×tier-4, 1×tier-5. All 11 source nodes are distinct existing graph
files (verified present at `graph/nodes/**/<slug>.node.md` before use): `euron-greyjoy`,
`dragonbinder`, `silence`, `moqorro`, `melisandre`, `victarion-greyjoy`, `rodrik-harlaw`,
`horn-of-winter`, `oldtown`, `leyton-hightower`, `daenerys-targaryen`.

## No CONTRADICTS edge — and why

The video's own extraction notes flag it as structurally different from a contested theory
like R+L=J: "explicit counter-evidence/objections are rare (only 2 beats)." Both of those beats
were checked and neither grounds to an independent CONTRADICTS edge:

- **euron-B78** (Euron's own claim he threw a dragon egg into the sea) is grounded
  (`affc-the-reaver-01.md:251`), but it's Euron's own unverifiable account, doubted by the
  video itself rather than by an independent character — and it bears on the separate
  Balon-murder/Faceless-Men sub-claim, not the eldritch-apocalypse core. Kept as prose in
  Evidence Against, not an edge.
- **euron-B79** (the video's own hedge that "it's not clear what exactly will happen" from the
  Forsaken-chapter ritual) is sourced entirely from the unpublished TWOW sample chapter
  (`source_domain: unknown`) and could not be grounded to any passage in the 5-book corpus —
  not usable as an edge under the corpus-only quote rule.

I did not manufacture a weak CONTRADICTS edge to satisfy a quota; the Evidence Against section
documents this honestly instead, matching the R+L=J precedent's own thin Evidence Against
section but going one step further (zero edges rather than one).

## Held-out material (and why)

- **The unpublished "Forsaken" chapter** (TWOW sample, read publicly by GRRM at a convention)
  is the theory's single densest evidentiary source — Euron's "I am your god" proclamation, the
  mass blood-sacrifice-to-the-ships imagery, Falia's mutilation, the "mass of writhing
  tentacles" transformation. None of it exists in `sources/chapters/`, so none of it could be
  quote-verified. It's flagged **TWOW** in the node's Ungrounded material section, entirely
  prose, zero edges. This is the single biggest gap between "what the video argues" and "what
  this corpus can support" — worth flagging to Matt explicitly since it's most of the theory's
  visceral case.
- **The Bloodraven-dream-visitation and skinchanging sub-claims** (sub_claims 1 and 2 in the
  extraction) are almost entirely community inference layered onto a real structural parallel
  (Euron's claimed boyhood flying dream vs. Bran's tower-fall/three-eyed-crow dream, both
  independently grounded beats) — but nothing states Bloodraven visited Euron or that Euron can
  skinchange. Held out as **community** material, not edges.
- **The entire Bloodstone Emperor parallel** is TWOIAF (*The World of Ice and Fire*) material —
  a real published in-universe historical text, but outside the 5-book POV corpus this cluster
  is grounded against (and outside what `sources/chapters/` covers). Only the amethyst-eyes
  wordplay (E11) ties back to a groundable POV-book line, and that edge is flagged tier-5 as
  the weakest in the set.
- **The "silence vs. title" and "Feast for Crows = literal crows feasting" thematic/title
  arguments** are literary readings of structure, not falsifiable in-world claims — held out as
  **book-interpretive**, no edges.
- **The seed's "Lovecraftian authorial influence" material** (`working/theories-staging/eldritch-apocalypse-seed.md`)
  is a craft/authorial fact about GRRM, not an in-world claim about Euron — deliberately not
  folded into this node to avoid conflating the two things the seed itself flagged as distinct.

## Open questions for the orchestrator

1. **Node existence mismatch with the seed.** The seed document (S110) states "`concept.theory`
   `eldritch-apocalypse` exists as a dark stub in `graph/nodes/theories/`" — this is **not
   true**: I searched `graph/nodes/theories/` and the wider graph and found no existing
   `eldritch-apocalypse` node of any kind (dark stub or otherwise). This node is a clean new
   mint candidate, not an enrichment of an existing stub, unlike the KotLT half of the R+L=J
   cluster. Flagging per the "trust worklog over stale claims" convention, though this is a
   seed-doc claim rather than a worklog claim — still stale and worth correcting at mint time.
2. **Tier-4 node confidence vs. the strength of E4 (Moqorro's vision).** The single strongest
   published-book beat (Moqorro's literal tentacled-monster vision) is genuinely tier-3-strong
   on its own, but the theory as a *whole* chains it to five other sub-claims of wildly varying
   groundedness (three of which lean on unpublished material). I kept the node at tier-4 per
   the seed's own framing and the orchestration guidance ("stacked-symbolism-heavy theories are
   tier-4"), but a reviewer could reasonably argue for tier-5 given how much rides on the
   Forsaken chapter. Flagging the judgment call rather than silently picking one.
3. **No CITED_BY / theorist-origin node**, consistent with the R+L=J cluster's S216 ratified
   decision to keep provenance in frontmatter (`origin`, `video_sources`) rather than a
   dedicated source-node type. Followed here without re-litigating.

## Verification

Ran an automated byte-exact check (Python, substring match) of all 11 `candidates.json` quote
fields against their cited `sources/chapters/*.md` files at the exact cited lines — 11/11
exact matches after two apostrophe-style fixes (curly `’` vs. straight `'` in E7/E9). Also
verified all 11 source-node slugs resolve to existing `graph/nodes/**/<slug>.node.md` files.
Node-body blockquotes were spot-checked the same way; several are deliberately partial-sentence
excerpts from longer character speeches (normal quotation practice — a complete grammatical
sentence pulled from within a longer quoted passage), not truncations that alter meaning.

## HARVEST

- `sources/chapters/affc/affc-the-prophet-01.md:91` / physical-description+foreshadowing /
  Harlon Greyjoy's greyscale death: "sitting grey-faced and still in a windowless tower room ...
  as the greyscale turned his tongue and lips to stone" — vivid disease imagery, thematically
  resonant with Shireen Baratheon's ongoing greyscale arc elsewhere in the corpus.
- `sources/chapters/affc/affc-the-reaver-01.md:57` / material-culture (gift-economy) / Euron's
  catalogue of exotic plunder used to buy ironborn loyalty — nutmeg, cloves, saffron, ivory
  tusks, unicorn horns, jade manticores, "bolts of fine silk and shimmering samite" — a rich
  trade-goods/luxury inventory line.
- `sources/chapters/affc/affc-the-reaver-01.md:71` / hospitality+body-horror / Victarion's
  rotting hand tended by the "dusky woman" with vinegar and linen, brushed off with a curt
  "Bring me wine" — a slow physical-decay thread (his hand festers across several later
  chapters) plus a blunt camp-hospitality beat (wine demanded, not offered).
