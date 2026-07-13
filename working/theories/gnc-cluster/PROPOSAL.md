# Grand Northern Conspiracy cluster — proposal (S216, staging-only)

**Status: STAGED, NOT MINTED.** Nothing here is written to `graph/`. All output
lives under `working/theories/gnc-cluster/`. Mint gate awaits Matt's explicit go
per the standing theories-track rule.

## What was built

`nodes/grand-northern-conspiracy-theory.node.md` — a new `concept.theory` node
(slug `grand-northern-conspiracy-theory`, deliberately distinct from the existing
tier-1 `graph/nodes/events/grand-northern-conspiracy.node.md` event node). Claim:
tier-4, status `open`. The node body opens `## Claim` with "The theory holds
that…" per the hard rule, and states its relationship to the existing event node
explicitly in a dedicated paragraph (the event node = confirmed Manderly-plot
facts only; this theory node = the unproven claim that the Manderly plot, the
Robb's-will/Jon-Snow thread, and the Stannis's-army mountain-clan thread are one
coordinated whole).

`candidates.json` — 12 edges (G1–G12), 11 distinct source nodes (`wyman-manderly`
and `barbrey-dustin` each appear twice — once SUPPORTS, once for a second distinct
quote/thread). All edge-source slugs verified to resolve against live
`graph/nodes/**/*.node.md` files (script run, all OK). All 12 quotes verified
byte-exact against `sources/chapters/*.md` at the cited chapter (grep + Python
substring check, all OK — see below).

## Edge summary

| id | type | source | tier | thread |
|---|---|---|---|---|
| G1 | SUPPORTS | wyman-manderly | 3 | Manderly plot — "mummer's farce" declaration |
| G2 | SUPPORTS | rickon-stark | 3 | Manderly plot — Rickon-for-Stannis terms |
| G3 | SUPPORTS | robett-glover | 3 | Manderly plot — Wex's Winterfell testimony |
| G4 | SUPPORTS | roose-bolton | 3 | Manderly plot — antagonist's own suspicion list |
| G5 | SUPPORTS | barbrey-dustin | 3 | Manderly plot — Dustin's private disloyalty roster |
| G6 | SUPPORTS | barbrey-dustin | 4 | Manderly plot — watchword reuse (coded-signal reading) |
| G7 | SUPPORTS | house-norrey | 4 | Stannis's-army thread — mountain clans join Stannis |
| G8 | SUPPORTS | torghen-flint | 4 | Stannis's-army thread — clan chiefs visit Jon |
| G9 | SUPPORTS | jon-snow | 4 | Stannis's-army thread — Jon names his lineage |
| G10 | SUPPORTS | alys-karstark | 3 | Robb's-will thread — northern perception of Jon |
| G11 | SUPPORTS | desmond-grell | 4 | Robb's-will thread — Riverrun men choose the Wall |
| G12 | CONTRADICTS | wyman-manderly | 3 | Communications-security objection to the "Grand"/unified claim |

Tier split: 6× tier-3, 6× tier-4, 0× tier-1/2 anywhere in staged artifacts (node
`confidence: tier-4`). One genuine CONTRADICTS (G12), scoped to the theory's
"Grand"/unified extension specifically (per the same T7-style scoping precedent
Matt ratified for R+L=J) — it does not contradict the existence of the individual
sub-plots, only their claimed unification.

## Source slugs used

`wyman-manderly` (×2), `rickon-stark`, `robett-glover`, `roose-bolton`,
`barbrey-dustin` (×2), `house-norrey`, `torghen-flint`, `jon-snow`,
`alys-karstark`, `desmond-grell`. The existing event node
`graph/nodes/events/grand-northern-conspiracy.node.md` was read as context (per
the task brief) but is **not** used as an edge source — every fact it records was
folded into the node body's Manderly-plot subsection as prose, cited to the
existing event node's own chapters, rather than double-minted as a redundant
edge.

## Held-out material

Fenced in the node's `## Ungrounded material (outside the corpus)` section,
domain-labelled:

- **book-interpretive** — the snowmen-of-four-lords scene, the
  Harwood-Stout/Whoresbane-Umber quiet conversation, and Barbrey's crypt visit
  sequence (gnc-B24–B29 in the source extraction) could not be re-grounded to a
  clean verbatim line this session (agent search came back `ungrounded` on all
  three); the claim is plausible book content but not independently cited here.
- **book-interpretive** — Howland Reed as Tower-of-Joy witness / Jon's Targaryen
  parentage as the secret motive for a hypothetical crown-Jon plot (depends
  entirely on `r-plus-l-equals-j`, cross-referenced rather than re-argued).
- **book-interpretive** — Catelyn's real-life dislike of Jon as a possible
  obstacle to Stoneheart crowning him.
- **community** — the Tom o' Sevenstreams "Red Wedding 2.0" fan extrapolation;
  the clansmen-already-know-the-will / Alysane-Mormont / Sybelle-Glover-godswood
  fan-link readings.
- **TWOW** — the published sample chapter in which Stannis exposes Arnolf
  Karstark's betrayal (outside the five-book corpus; not treated as evidence
  either way).
- **show** — explicit note that GOT depicted none of this (no Manderly plot, no
  Robb's-will succession scheme, Brynden Blackfish killed at Riverrun instead of
  escaping), so the theory in every form here is book-only material — flagged per
  the task brief's specific instruction to note the show's divergent Winterfell
  plot.

Also explicitly **not minted as an edge**, deliberately: the Arnolf Karstark
conspiracy itself (gnc-B66/B69 in the source extraction) — the one grounded
attempt at a verbatim quote for it failed byte-verification (`adwd-jon-09.md:156`
does not contain the claimed sentence; confirmed empty via `sed -n '156p'`), so
per the hard rule ("Quotes ONLY from grounded substrate rows") it stays out of
the edge set entirely. It is discussed in `## Evidence Against` prose without a
quote, cross-referencing the existing `house-karstark` / `arnolf-karstark` nodes
by name only.

## Open questions for the orchestrator

1. **Relationship convention to the existing event node** — I did not mint a
   dedicated edge from `grand-northern-conspiracy` (the event node) to
   `grand-northern-conspiracy-theory` (this node). The R+L=J review (S216)
   flagged the same "subject-link" gap for the Knight of the Laughing Tree
   cluster and explicitly declined to adopt a convention for it ("offered S216,
   not adopted"). I've followed that precedent here rather than inventing a new
   pattern unilaterally — but this is now the *second* theory cluster with the
   same gap (theory node discusses an existing graph node in prose but has no
   traversable edge to it), which may be worth deciding as a real convention
   rather than re-deferring a third time.
2. **`manderly-bakes-the-frey-pies` as a candidate edge source** — the task
   brief suggested this event node as a natural SUPPORTS source. I chose not to
   use it: the Frey-pies event postdates and is downstream of the plot rather
   than evidencing it, and every quote I could ground for that specific event
   (Wyman's dinner-party dialogue) was already used via `wyman-manderly`
   directly (G1, G12) or would have required inventing an edge without a
   distinct grounded quote of its own. Flag if the orchestrator wants a
   dedicated event→theory edge regardless (would need a fresh quote pull from
   the Frey-pies chapter specifically, e.g. `adwd-the-prince-of-winterfell` or
   wherever that scene lands — not yet checked this session).
3. **Tier-4 overall node confidence** — chosen because the sourcing video's own
   verdict argues against the "Grand"/unified framing while affirming the
   individual sub-plots (which are largely tier-3, with the Manderly leg already
   tier-1 on the event-node layer). If the orchestrator's convention is to grade
   theory-node confidence off the *strongest* supporting thread rather than the
   *overall claim being argued*, tier-3 would also be defensible — I judged the
   claim-as-written (the unification, not any one leg) as the thing being rated.
4. **House Umber / House Glover as umbrella-node edge sources** — the task brief
   listed `house-umber` and `house-glover` as candidates. I used the more
   specific character nodes instead (`roose-bolton`'s line naming "Whoresbane"
   the Umbers; `robett-glover` directly) since I could ground quotes to named
   individuals rather than the house umbrella nodes. No edge targets
   `house-umber` or `house-glover` directly in this build; flag if the
   orchestrator wants house-level edges added as well for query-traversal
   reasons (bag-retrieval via `--container`-style modes, per the S121
   containers convention) rather than only character-level ones.

## Harvest

- `sources/chapters/adwd/adwd-davos-04.md:97` / quote / Wyman's standing cover
  story for secret meetings: "I have eaten too much, as ever, and all White
  Harbor knows my bowels are bad. My friends of Frey will not question a
  lengthy visit to the privy, we hope." — good standalone hospitality/deception
  beat (guest-right-adjacent misdirection), not used as an edge this session.
- `sources/chapters/adwd/adwd-davos-04.md:109` / quote / "the debt" beat:
  "she reminded me of the debt White Harbor owes to the Starks of Winterfell, a
  debt that can never be repaid" — Manderly-Stark loyalty motif, not used as an
  edge (redundant with G1/G2 for this build but worth a pointer for a future
  Manderly-focused enrichment dip).
- `sources/chapters/adwd/adwd-the-turncloak-01.md:161` / quote / general
  northern-loyalty backdrop: "the Freys may not care, but the northmen … they
  fear the Dreadfort, but they love the Starks" (Barbrey Dustin) — same
  conversation as G5, one line earlier; not independently edged.
- `sources/chapters/acok/acok-theon-06.md:251` / quote / Ramsay/Donella
  Hornwood: "Snow, my wife called me before she ate her fingers, but I say
  Bolton." (Roose Bolton, taunting Reek) — corroborates the Hornwood-atrocity
  backdrop for G5's "Hornwood men have forgotten" line; not independently
  edged.
- `sources/chapters/asos/asos-catelyn-06.md:247` / quote / Cerwyn/Tallhart
  deaths at Winterfell reported to Robb: motive-building for the general
  Bolton-betrayal backdrop; not edged (redundant with G4's Roose-Bolton line
  naming the same two houses).
- `sources/chapters/adwd/adwd-davos-04.md:199` / dialogue exchange around "Two
  of them Ned Stark's murdered sons" — speaker attribution ambiguous on a close
  read of the surrounding dialogue block (alternating Wyman/Glover/Davos lines
  without a clean tag on that specific line); flagged rather than risk a
  misattributed source node.
