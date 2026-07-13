# Coldhands cluster — proposal (S216, staging-only)

**Status: STAGED, NOT MINTED.** Nothing here is written to `graph/`. All output
lives under `working/theories/coldhands-cluster/`. Mint gate awaits Matt's
explicit go per the standing theories-track rule.

## What was built

`enrich/coldhands-theories.node.md` — a rewrite of the existing stub
`graph/nodes/theories/coldhands-theories.node.md` (`concept.theory`, slug
`coldhands-theories` unchanged, `wiki_source`/`bucket_id`/`prompt_version`
preserved, `node_version` 1→2). Display name `"Who is Coldhands?"` — **neutral
framing chosen deliberately**, not a claim-style "Coldhands is X" name (see
Naming judgment below). `confidence: tier-4`, `status: open`.

`candidates.json` — 7 edges (C1–C7), 4 distinct source slugs (`coldhands` ×5,
`wights` ×1, `waymar-royce` ×1). All source slugs verified to resolve against
live `graph/nodes/**/*.node.md` files. All 7 quotes verified byte-exact against
`sources/chapters/*.md` at the cited line (direct line read + Python substring
check, both green — see Gates below).

## Naming judgment (why neutral, not claim-style)

The task brief offered two options: a claim-style name ("Coldhands is Benjen
Stark") if the substrate centers a leading candidate, or a neutral framing if the
video treats it as genuinely open. The substrate is unambiguous on this: the ASX
video's own verdict (row 1 of the extraction, `asx_verdict`) is that it "doesn't
know who Coldhands is" and treats **every** named candidate — Benjen Stark,
Will/Waymar Royce, Ser Duncan the Tall, the Night's King, and the Night's
King/Other hybrid — as unconvincing. No candidate is presented as a leading
theory the way Lyanna-as-mystery-knight was for `knight-of-the-laughing-tree-theories`
or Rhaegar/Lyanna-as-Jon's-parents was for `r-plus-l-equals-j`. The only
identity-related material with any real weight is negative (the GRRM manuscript
note reportedly ruling out Benjen). Claim-style naming would misrepresent the
substrate's own shape. Name: `"Who is Coldhands?"` (echoes the video's own title
and the existing stub's wiki-derived framing).

## Edge summary

| id | type | source | tier | thread |
|---|---|---|---|---|
| C1 | SUPPORTS | coldhands | 3 | What-is-Coldhands — never gives his own name |
| C2 | SUPPORTS | coldhands | 4 | What-is-Coldhands — raven command / greenseer parallel |
| C3 | SUPPORTS | coldhands | 4 | What-is-Coldhands — elk-death ritual, "strange tongue" |
| C4 | SUPPORTS | wights | 4 | What-is-Coldhands — ordinary wights' blue eyes vs. his black |
| C5 | SUPPORTS | coldhands | 4 | What-is-Coldhands — fear of fire (wight-vulnerability parallel) |
| C6 | SUPPORTS | coldhands | 3 | What-is-Coldhands — self-aware clinical explanation of his own undeath |
| C7 | CONTRADICTS | waymar-royce | 4 | Who-was-Coldhands — against the Will/Waymar Royce candidate |

Tier split: 2× tier-3, 5× tier-4, 0× tier-1/2 anywhere in staged artifacts (node
`confidence: tier-4`). One CONTRADICTS (C7), scoped to a specific identity
candidate rather than the theory's *what*-is-Coldhands claim as a whole.

## The layer finding (why only 7 edges, not more)

Most of the "what is Coldhands" physical/behavioral material in the source
extraction (B01, B05–B07, B12, B14, B19–B21) turned out, on inspection, to be
**already owned by the tier-1 `coldhands` character node** — either quoted
verbatim in its own Quotes section (the Meera suspicion speech, the "dead meat,
dry blood" Summer-smell line, the "Who are you? Why are your hands black?"
dialogue, the "Beneath the trees, a man muffled head to heels..." first
appearance) or already backing existing tier-1/tier-2 edges in
`graph/edges/edges.jsonl` (the "closed his eyes, but Bran did not think he slept"
line is the evidence_quote on an existing `coldhands KILLS nights-watch` edge;
the "Dreamer, wizard... the last greenseer" line is the evidence_quote on the
existing `coldhands AGENT_IN bran-meets-coldhands` edge). Re-editing these as
"new" theory edges would double-quote content the graph already carries and
violate the layer rule (facts owned by existing tier-1/2 nodes are premise, not
theory evidence) — the same finding the gnc-cluster and eldritch-cluster S216
adjudications made for their own overlapping material. These beats are discussed
in the node body as premise prose (with pointers to the existing node/edges)
rather than re-edged.

What survived as genuinely new, theory-specific, byte-groundable content: the
name-origin line (C1, not previously quoted anywhere), the raven/greenseer
comparison (C2), the elk-ritual "strange tongue" detail (C3), the wights'
blue-eye contrast pulled from a different passage than the character node cites
(C4), the fire-fear beat (C5), Coldhands's own clinical self-explanation (C6),
and the Waymar Royce counter-evidence (C7) — none of which appear anywhere else
in the graph.

## Source slugs used

`coldhands` (×5), `wights` (×1), `waymar-royce` (×1). The existing character node
`graph/nodes/characters/coldhands.node.md` and its existing edges were read as
context (per the task brief) but the facts they already carry are **not**
re-edged — see layer finding above. Existing `SERVES`/`SWORN_TO` edges to
`brynden-rivers` are treated as settled premise for the "most likely reanimated
by Bloodraven" clause of the claim, not re-argued as theory evidence.

## Held-out material (fenced in `## Ungrounded material`, domain-labelled)

- **grrm** — The Reddit-reported GRRM manuscript note rejecting Benjen Stark as
  Coldhands's identity. The marquee GRRM-interview-class item for this cluster,
  fenced prominently per the hard rule. Out-of-book, secondhand-reported,
  unverifiable against the local corpus; never an edge.
- **community** — The Benjen Stark candidate itself; the Night's King candidate
  and its own book-side counter-arguments (none groundable this pass, see gap
  below); the Night's King/Other-hybrid candidate.
- **dunk-egg** — The Ser Duncan the Tall candidate, both the supporting reasoning
  (his known relationship with Bloodraven at the end of *The Mystery Knight*) and
  the video's own counter-arguments (height mismatch, death at Summerhall,
  Watch-membership-would-have-been-noted). No verbatim passage groundable in
  either the D&E novellas or the main series this pass.
- **book-interpretive** — The Thoros/Beric fire-magic parallel underlying the
  video's core reanimation-mechanism model; the video's own "maybe he's just an
  unnamed Watchman" fallback reading and its own argument against that fallback
  (doesn't explain the face-hiding or the narrative emphasis on mystery).
- **show** — Game of Thrones never depicts a character named Coldhands. It gives
  Coldhands's narrative *function* (undead-but-still-a-person guide/protector
  beyond the Wall) to a reworked Benjen Stark, reintroduced in Season 6 as a man
  saved mid-wight-transformation by the Children of the Forest. This is the
  show's own de facto answer to "who is Coldhands," documented in the node's
  Status Notes as a genuine complication (it sits in direct tension with the
  fenced **grrm** manuscript note above) but explicitly **not** treated as book
  confirmation — status stays `open`, not `show-confirmed`.

## KNOWN GAP — missing beats B30 and B35

Per the task brief: the S214 regrounding-agent pass (`working/theories/
regrounding-agent/Ge6VduBUJFo.jsonl`) died at a spend wall before appending rows
for the final two beats it was assigned, `coldhands-B30` (Night's King legend
counter-argument: cast down and name struck from memory, vs. Coldhands killed by
the Others — "very name from memory") and `coldhands-B35` (hybrid-theory
counter-argument: Coldhands shows none of the Others' own distinguishing
features — "a different sort of life"). Both beats had `status: no-match` in the
earlier deterministic `regrounding/` pass (automated exact-match failed) and were
never picked up by the agent pass. **No quote exists on disk for either beat.**
Per the hard rule against inventing quotes for missing beats, neither is asserted
as fact, quoted, or represented as an edge; both are noted as a `KNOWN GAP` bullet
in the node's Ungrounded material section and here. If a future session re-runs
regrounding-agent to close this residue, both beats are Night's King/hybrid
counter-arguments only — low priority, since the Night's King and hybrid
candidates are already edge-less and fully fenced as community material with or
without these two beats.

One additional near-miss: `coldhands-B32` (the "cold preserves" Aemon quote,
`affc-samwell-03.md:105`, `status: matched` in the deterministic regrounding
pass) was **deliberately excluded from the edge set**, not because it fails
byte-verification (it passes) but because the quoted line is Aemon reflecting on
the Wall's protective magic ("Fire consumes, but cold preserves. The Wall...."),
not on corpse or mind preservation over millennia — the sense the video borrows
it for. Using it as an edge would risk the same "quote pulled out of its own
context to support an unrelated claim" problem the R+L=J and eldritch-cluster
S216 reviews flagged and repaired/dropped elsewhere (the eldritch cluster's E11
single-word-tie rejection is the closest precedent). It is not discussed in the
node body at all; flagging here for the record in case a future reviewer wants
it added back with a more careful scoping note.

Also excluded: `coldhands-B19` and `coldhands-B24`, both marked `status:
byte-fail` in the regrounding-agent file — B19's quoted span does not appear
verbatim on the cited line, and B24's quote is stitched from three separate
non-contiguous paragraphs (`agot-prologue.md` lines 223/225/227) concatenated
without the intervening text, which does not exist as a single verbatim span in
the source. Both correctly excluded per the hard rule; B24's underlying scene
(Waymar Royce's wight-transformation, "The pupil burned blue") is real and
consistent with C7's premise but was not independently re-quoted since C7 already
covers the Waymar-Royce candidate with a clean, contiguous, byte-verified line.

## Open questions for the orchestrator

1. **Node confidence tier-4 vs. tier-3.** Chosen because the theory's own title
   question ("who was Coldhands") — as opposed to the *what*-is-Coldhands
   reanimation-mechanism reading, which has decent textual support — has
   essentially no surviving textual evidence for any candidate after grounding.
   If node confidence should instead be graded off the *what*-question's
   stronger showing (which is closer to tier-3 territory, matching
   `r-plus-l-equals-j` and `knight-of-the-laughing-tree-theories`), tier-3 would
   also be defensible — I judged the *identity* question as the theory's
   defining claim (it is literally the node's own name) and rated accordingly,
   matching the gnc-cluster precedent of rating off the claim-as-written rather
   than its best-supported sub-thread.
2. **Subject-link to the existing character node.** Following the KotLT/GNC
   precedent (offered and declined twice already), I did not mint a dedicated
   edge from `coldhands` (the character node) to `coldhands-theories` beyond the
   6 SUPPORTS edges already sourced from it. If the orchestrator wants a
   convention here, this is now the third cluster to surface the same gap.
3. **`wights` as a concept-node edge source (C4).** I used the `wights` concept
   node as the SUPPORTS source for the blue-eyes-vs-black-eyes contrast rather
   than `coldhands` itself, since the quoted passage is about wights, not about
   Coldhands directly. Flag if the orchestrator prefers `coldhands` as source for
   all comparison-type edges regardless of which entity the quoted passage is
   literally about.

## Harvest

- `sources/chapters/adwd/adwd-bran-01.md:211` / quote / the full exchange
  continuing past the "Dreamer, wizard... last greenseer" line ("The longhall's
  wooden door banged open. Outside, the night wind howled, bleak and black. The
  trees were full of ravens, screaming. Coldhands did not move.") — good
  standalone atmosphere/foreshadowing beat (the ravens' reaction, Coldhands's
  stillness); not used as an edge this session (the line is already the
  evidence_quote on the existing `coldhands AGENT_IN bran-meets-coldhands` edge).
- `sources/chapters/adwd/adwd-bran-01.md:199` / dialogue / Bran's direct
  interrogation of Coldhands ("Who are you? Why are your hands black?") — already
  quoted near-verbatim on the tier-1 `coldhands` node; flagging only because it's
  a strong standalone Bran-voice beat if a future Bran-POV voice-analysis pass
  wants it.
- `sources/chapters/asos/asos-bran-04.md:209` / quote / "'There's a gate,' said
  fat Sam. 'A hidden gate, as old as the Wall itself. The Black Gate, he called
  it.'" — Sam retelling the Black Gate/Coldhands story directly to Bran's party;
  plot-logistics content, not identity-theory-specific; not used as an edge but
  worth a pointer for a future Black-Gate-event enrichment dip.
