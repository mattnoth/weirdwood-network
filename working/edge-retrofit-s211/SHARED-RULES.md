# Edge-vocab retrofit S211 — proposer SHARED RULES

You are proposing retrofit edge candidates for the Weirwood Network ASOIAF knowledge
graph. Older extraction passes predate newer edge types; where published text supports
them, we add typed edges so the whole graph speaks current vocabulary. Repo root:
`/Users/mnoth/source/asoiaf-chat`. This is a PROPOSAL step — you write candidate files
only. You NEVER edit anything under `graph/`.

## Vocabulary for this dip (directions are exact — do not invert)

- `KNIGHTED_BY` — **Knight → Dubber** ("X was knighted by Y" ⇒ source=X, target=Y).
  Emit ONLY this form for knighting facts (not BESTOWS_KNIGHTHOOD_ON — one edge per
  fact, canonical direction). Use only when prose explicitly describes the
  dubbing/knighting (not squire-service, not TUTORS-style training, not APPOINTS).
- `SUSPECTED_OF` — **Suspect (character) → Event**. A character is suspected — in-world
  and/or clearly by the published text — of being agent/cause of an event the text does
  NOT prove. Capped `tier-2`. NEVER asserts the act as fact.

## SUSPECTED_OF honesty rules (the whodunit discipline — violations get rejected)

1. The suspicion must be IN THE TEXT: a character voices it, rumor reports it, or the
   narration plants it pointedly. Fan-theory inference is FORBIDDEN (theory work is
   gated project-wide).
2. If the published text PROVES the actor did it, SUSPECTED_OF is wrong — note it in
   `flags` instead (it would be AGENT_IN/KILLS territory, out of scope this dip).
3. If the text leaves an act un-attributed with NO named suspect, emit NOTHING
   (precedent: the Dorne "someone always tells" informer — honest whodunits stay empty).
4. Check the packet's `existing_suspected_of` + the global `existing_suspected_pairs`
   in `_meta` — never re-propose a covered pair.

## Quote grounding (hard requirement — mint line-checks every quote and ABORTS on miss)

Every candidate needs a VERBATIM quote you located in a chapter file under
`sources/chapters/{book}/{chapter}.md`, where book ∈ agot acok asos affc adwd tmk tss
thk fab. Use Grep to find it; copy the quote EXACTLY as it appears in the file
(punctuation, curly quotes, OCR artifacts included — do not "fix" anything). Keep
quotes short (one sentence or a tight span). The quote must itself support the claim
(the knighting / the suspicion), not merely mention the people.

If the fact appears only in node/wiki prose and you cannot locate supporting book text,
put the row in `wiki_only` (same shape, `quote` = the node-prose line, `chapter` = the
node file path) — do NOT force it into `candidates`.

## Slug validity

`source` and `target` must be existing node slugs — verify each with Glob
(`graph/nodes/**/<slug>.node.md`). If unsure of a slug, check
`working/wiki/data/all-node-alias-lookup.json` or Glob for name fragments. If the
person has NO node, record the row in `no_node` instead. NEVER invent a slug, NEVER
propose creating a node.

## Output schema

Write ONE json file (your prompt names the exact path). Shape:

```json
{
  "_meta": {"slice": "...", "agent": "...", "packets_processed": N},
  "candidates": [
    {"id": "K1", "type": "KNIGHTED_BY", "source": "<knight-slug>",
     "target": "<dubber-slug>", "book": "asos", "chapter": "asos-jaime-01",
     "quote": "<verbatim>", "tier": "tier-1", "note": "<one-line why>",
     "qualifier": ""}
  ],
  "wiki_only": [...], "no_node": [...],
  "flags": ["<anything off-pattern worth orchestrator eyes: proven-agent cases,
             direction ambiguity, possible dup, node mistype you noticed>"]
}
```

- ids: K1..Kn (knighting) / S1..Sn (suspicion). tier: `tier-1` for on-page facts,
  `tier-2` for SUSPECTED_OF (always) and anything reported-secondhand.
- `qualifier`: leave `""` unless a mechanism matters (e.g. suspicion `via_rumor`).
- Dedup against the packet's `existing_edges` list — if an equivalent typed edge
  already exists, skip it.

## Harvest rule (FIRM project rule — do this as you read)

While you are in chapter text for ANY reason and spot a notable-but-off-task find
(a load-bearing homeless quote, food/meal detail, physical description, hospitality
beat, foreshadowing), drop a one-line pointer `chapter:line / kind / note` into YOUR
OWN file `working/edge-retrofit-s211/proposals/harvest-<your-slice>.md` (NOT the
global queue — the orchestrator merges serially). POINT, don't extract.

## Final message

Your final message = a 5-line summary: counts (candidates / wiki_only / no_node /
flags), and anything the orchestrator must look at first. The JSON file is the
deliverable, not the message.
