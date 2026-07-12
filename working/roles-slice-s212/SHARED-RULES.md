# Roles slice S212 — proposer SHARED RULES

You are proposing ROLE EDGES for event nodes in the Weirwood Network ASOIAF knowledge
graph. These events carry rich prose naming actors, victims, and commanders, but ZERO
role edges — so the chat cannot answer "who was involved?". Repo root:
`/Users/mnoth/source/asoiaf-chat`. This is a PROPOSAL step — you write candidate files
only. You NEVER edit anything under `graph/`.

Vocabulary canon for anything you name: **Pass** = big numbered corpus sweep; **Track**
= named chunk of work; **step** (lowercase) = ordered piece inside a Track; **Tier** =
confidence rating 1–5 ONLY (never for work/process).

## Role vocabulary (directions are exact — source is ALWAYS the person/house, target is ALWAYS the event)

- `AGENT_IN` — the agent/executor: the participant who actually PERFORMED the act.
  (Person/House → Event)
- `VICTIM_IN` — receives the action as victim/patient — the one the act was done TO.
  **HARM-GATE:** the target event's subtype must be a harm subtype (death, execution,
  murder, assassination, poisoning, maiming, torture, capture, imprisonment, battle,
  sack, destruction, suicide, stillbirth, betrayal, raid, attack, duel, deception,
  mutiny, massacre, abduction, wounding). `event.war` and `event.incident` are NOT
  harm subtypes — a VICTIM_IN onto them FAILS the mint gate. Route those people to
  PARTICIPATES_IN/FIGHTS_IN instead, or flag the node as possibly mistyped.
- `COMMANDS_IN` — command-tier role in a battle/war (note which side in `note`), OR
  the orderer/instigator of an event the commander did NOT personally execute (Tywin
  orders the Riverlands attack → Tywin COMMANDS_IN, the Mountain AGENT_IN).
- `FIGHTS_IN` — combatant in a battle, war, or tournament.
- `PARTICIPATES_IN` — active NON-combat involvement: logistical, administrative,
  organizational, supportive. Not a combatant, not a guest, not command-tier.
- `ATTENDS` — guest/audience at a *staged social/ceremonial gathering* (feast, wedding,
  tourney-as-a-whole, court, coronation). Voluntary audience only.
- `WITNESS_IN` — the observer/perceiver of a CHARGED incident (violence, death, a
  secret, an atrocity) where the perception itself is load-bearing. **Text-anchor
  gate:** the prose must show the character actually SEES it — present-but-shielded
  does NOT qualify (Yoren forcing Arya's eyes shut ⇒ NOT a witness; Sansa who "could
  not turn her head" ⇒ IS). Staged-gathering audience = ATTENDS, not WITNESS_IN.
- `OFFICIATES` — performs the ritual/religious/ceremonial role at the event (septon at
  a wedding, Damphair at the kingsmoot).
- `HONORED_AT` — the ceremonial HONOREE (the crowned queen of love and beauty, the
  dubbed knight). The conferrer is AGENT_IN.

One person can hold multiple roles on one event only when the text supports each
distinctly (rare). Pick the MOST SPECIFIC role that fits; do not double-emit
FIGHTS_IN + PARTICIPATES_IN for the same person.

## Quote grounding (hard requirement — mint line-checks every quote and ABORTS on miss)

Every candidate needs a VERBATIM quote you located in a chapter file under
`sources/chapters/{book}/{chapter}.md`, where book ∈ agot acok asos affc adwd tmk tss
thk fab. Use Grep to find it; copy the quote EXACTLY as it appears in the file —
punctuation, curly quotes, OCR artifacts like `|` for `I` included; do NOT "fix"
anything. The quote must be a SINGLE-LINE substring of the chapter file (quotes
spanning line-wraps fail the line-check) — keep it short, one sentence or a tight span.
The quote must itself support the claimed ROLE (who did/suffered/commanded/witnessed),
not merely mention the people.

If the role is clear in node/wiki prose but you cannot locate supporting book text,
put the row in `wiki_only` (same shape, `quote` = the node-prose line, `chapter` = the
node file path) — do NOT force it into `candidates`. wiki_only rows are tier-2.

## Slug validity

`source` must be an existing node slug — verify with Glob
(`graph/nodes/**/<slug>.node.md`). If unsure, check
`working/wiki/data/all-node-alias-lookup.json` or Glob name fragments. If the person
has NO node, record the row in `no_node` instead. NEVER invent a slug, NEVER propose
creating a node. `target` is the packet's event slug — never anything else.

## Dedup + honesty

- Check the packet's `existing_edges` — if an equivalent typed edge already exists
  (e.g. the person already has KILLS/EXECUTES/CAPTURES onto a party of this event),
  a role edge may still be valid (roles reify the hub), but note the overlap in `note`.
  Never re-emit a role type the person already carries onto this event.
- If the text proves nothing about a person's role, emit NOTHING for them. Un-attributed
  acts stay empty (the honest-whodunit discipline). SUSPECTED_OF is OUT OF SCOPE this
  slice — if you spot an unproven-suspicion case, put it in `flags`.
- Aim for the LOAD-BEARING participants (agent, victim, commander, officiant, key
  witnesses), not exhaustive attendance rosters. 2–8 role edges per event is typical;
  a thin stub event may honestly yield 0 (say so in flags).

## Output schema

Write ONE json file (your prompt names the exact path). Shape:

```json
{
  "_meta": {"slice": "roles", "agent": "<your-chunk>", "packets_processed": N},
  "candidates": [
    {"id": "R1-01", "type": "AGENT_IN", "source": "<person-slug>",
     "target": "<event-slug>", "book": "asos", "chapter": "asos-jaime-01",
     "quote": "<verbatim single-line substring>", "tier": "tier-1",
     "note": "<one-line why + which side if COMMANDS_IN>", "qualifier": ""}
  ],
  "wiki_only": [...], "no_node": [...],
  "flags": ["<anything off-pattern: harm-gate conflicts (VICTIM_IN wanted on a
             war/incident node), possible node mistypes, proven-vs-suspected cases,
             direction ambiguity, possible dups, events yielding 0 honest roles>"]
}
```

- ids: `R<chunk>-NN` (e.g. chunk 2 → R2-01, R2-02 …). tier: `tier-1` for on-page book
  facts, `tier-2` for secondhand/chronicler-hedged claims and all wiki_only rows.
- `qualifier`: leave `""` unless a mechanism genuinely matters.

## Harvest rule (FIRM project rule — do this as you read)

While you are in chapter text for ANY reason and spot a notable-but-off-task find
(a load-bearing homeless quote, food/meal detail, physical description, hospitality
beat, foreshadowing), drop a one-line pointer `chapter:line / kind / note` into YOUR
OWN file `working/roles-slice-s212/proposals/harvest-chunk<N>.md` (NOT the global
queue — the orchestrator merges serially). POINT, don't extract.

## Final message

Your final message = a 5-line summary: counts (candidates / wiki_only / no_node /
flags), and anything the orchestrator must look at first. The JSON file is the
deliverable, not the message.
