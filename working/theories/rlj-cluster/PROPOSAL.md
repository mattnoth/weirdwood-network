# R+L=J cluster — proposal (S214, theories wave-1)

> Proposer output. NOT minted. Awaits fresh-verify + adjudication + Matt's go per the
> build plan (`working/theories/rlj-cluster/build-plan.md`).

## Node decisions

1. **New node `r-plus-l-equals-j`** (`concept.theory`) —
   `working/theories/rlj-cluster/nodes/r-plus-l-equals-j.node.md`. `confidence:
   tier-3`, `status: show-confirmed`, sourced from kHqzFwodZqQ (R+L=J core) +
   UrhqmMRv1gQ (R+L=J-cluster beats only — Azor Ahai beats held out per build plan).
2. **Enriched existing stub `knight-of-the-laughing-tree-theories`** —
   `working/theories/rlj-cluster/enrich/knight-of-the-laughing-tree-theories.node.md`.
   Slug + wiki_source kept; confidence bumped tier-2 → tier-3; `status: open` (never
   show-confirmed, unlike R+L=J itself); sourced from eUVr_lUxYf8.
3. `jon-snow-theories` umbrella stub left untouched, per guardrail.

## Edge table

| id | type | source | target | note |
|----|------|--------|--------|------|
| T1 | SUPPORTS | eddard-stark | r-plus-l-equals-j | Ned's "lived his lies for fourteen years" — Jon is fourteen at AGOT's start |
| T2 | SUPPORTS | lyanna-stark | r-plus-l-equals-j | Tower of Joy dream: Lyanna "in her bed of blood" |
| T3 | SUPPORTS | combat-at-the-tower-of-joy | r-plus-l-equals-j | ToJ dream fuses blue-rose imagery with the fight |
| T4 | SUPPORTS | rhaegar-targaryen | r-plus-l-equals-j | Rhaegar crowns Lyanna over his wife Elia at Harrenhal |
| T5 | SUPPORTS | tourney-at-harrenhal | r-plus-l-equals-j | Barristan (ADWD) independently corroborates the Harrenhal choice |
| T6 | SUPPORTS | daenerys-targaryen | r-plus-l-equals-j | House of the Undying: blue flower at "a wall of ice" |
| T7 | CONTRADICTS | jon-snow | r-plus-l-equals-j | NW vow forecloses the throne-claim extension (not the parentage claim) |
| T8 | SUPPORTS | abduction-of-lyanna | r-plus-l-equals-j | Robert's "official" account establishes the premise the theory reinterprets |
| T9 | SUPPORTS | crowning-of-lyanna-at-harrenhal | r-plus-l-equals-j | Lyanna's crypt statue carries the same blue-rose garland from her crowning |
| T10 | SUPPORTS | lyanna-stark | knight-of-the-laughing-tree-theories | Lyanna ("the she-wolf") rescues Howland — establishes motive |
| T11 | SUPPORTS | howland-reed | knight-of-the-laughing-tree-theories | The core incident: mystery knight avenges Howland, demands squires be taught honor |
| T12 | SUPPORTS | rhaegar-targaryen | knight-of-the-laughing-tree-theories | Aerys sends Rhaegar himself to unmask the knight |
| T13 | SUPPORTS | tourney-at-harrenhal | knight-of-the-laughing-tree-theories | Meera confirms the "wolf maid" (Lyanna) was later crowned queen of love and beauty |
| T14 | SUPPORTS | eddard-stark | knight-of-the-laughing-tree-theories | Jojen's surprise Ned never told Bran the tale — suggestive, not conclusive |

9 edges → r-plus-l-equals-j (target 8–15, met). 5 edges → knight-of-the-laughing-tree-theories
(target 3–6, met). All 14 edges + all in-body blockquote runner-up quotes byte-verified
against `sources/chapters/*.md` at the cited lines via a standalone Python check (exact
substring match, including curly-quote characters) before this proposal was written.

## Beats deliberately dropped (and why)

- **UrhqmMRv1gQ's "Rhaegar is Azor Ahai" theory (beats rhaegar-B11 through rhaegar-B51,
  ~40 beats)** — held out per build plan; belongs to a separate Azor Ahai theory unit.
  Not represented anywhere in this dip's outputs, including the node's Ungrounded
  section (flagged there only as a pointer, not summarized in content).
- **kHqzFwodZqQ sub-claim 1 (Song of Ice and Fire personification, warging+dragon
  fire, PTWP/Azor Ahai candidacy for Jon)** — entirely ungrounded per both grounding
  passes (rlj-B20 through rlj-B22), and thematically overlaps the held-out Azor Ahai
  territory. Noted in the node's Ungrounded section, not made into edges.
- **kHqzFwodZqQ sub-claim 0 (Iron Throne claim mechanics: secret-marriage precedent,
  legitimization, proof-of-parentage difficulty, whether Jon would even want the
  throne)** — all either ungrounded (no locatable verbatim quote) or pure legal/
  narrative speculation. The Night's Watch vow beat (rlj-B26) was the one piece with a
  clean verbatim grounding, so it became edge T7 (CONTRADICTS); the rest are
  summarized as prose in Evidence Against/Ungrounded, not edges.
- **kotlt-B04's specific "mud-man"/"frog-eater" slur wording** — the deterministic and
  agent grounding passes disagreed on the precise phrase ("cursing him for a
  frogeater" is the actual text; "mud-men" plural wasn't located). Used the
  confirmed "she-wolf" rescue line instead (edge T10) rather than risk a near-miss
  quote.
- **kotlt sub-claims 0/1/2/3 case-by-case candidate elimination (Howland/Brandon/Ned/
  Benjen height, temperament, training arguments)** — each rests on characterization
  scattered across multiple chapters/books with no single clean citable quote per
  claim; several came back `byte-fail`/`ungrounded` in the regrounding-agent pass.
  Summarized as one prose paragraph in the node's Ungrounded section rather than
  forced into edges or an inflated Evidence Against list.
- **roberts-rebellion** (build-plan candidate node) — not used. Its likely content
  (the war's broad political causes) would have been redundant with the
  abduction-of-lyanna edge (T8) and the Harrenhal edges; adding it felt like padding
  toward the 15-edge ceiling rather than a genuinely distinct evidentiary link.
- **Show-only/TWOW/community beats** (GoT S7 parentage reveal mechanics, "died with
  Lyanna's name on his lips," secret Isle-of-Faces wedding, Bran-warging alternative,
  Elia Sand "Lady Lance" TWOW precedent) — all routed to the Ungrounded material
  sections of the relevant node, explicitly domain-labelled, never edges.

## Flags for Matt / adjudication

1. **T8 (abduction-of-lyanna → r-plus-l-equals-j, SUPPORTS)** is the one edge on a
   knife's edge for direction/type. The quoted passage is Robert's "official" account
   (abduction + rape) — the version R+L=J *disputes* in spirit, even though the
   underlying fact pattern (Rhaegar + Lyanna together, her resulting death) is what
   the theory builds on. I judged this SUPPORTS-the-premise rather than
   CONTRADICTS-the-theory; a fresh-verify pass should double check that call.
2. **T13's quote is a two-line dialogue exchange split across two speaker turns**
   ("She was," said Meera, "but that's a sadder story.") that only makes sense with
   Bran's preceding line for context (quoted in the node body but not in the edge
   quote itself, to keep the edge quote itself short/contiguous per the mint
   fail-fast re-grep). Worth confirming this reads clearly enough standalone in a
   future UI surface.
3. **eddard-stark and rhaegar-targaryen each carry edges to BOTH theory nodes** (T1/T14
   for eddard-stark; T4/T12 for rhaegar-targaryen) with genuinely distinct quotes and
   distinct theories as targets — this is allowed under the "one edge per
   (evidence-node, theory) PAIR" rule (not one edge per evidence-node overall), but
   flagging in case the adjudication pass reads it as a near-duplicate.
