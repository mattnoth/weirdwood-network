# S213 Dance arc dip — adjudication record

Input: 21 edges (W1 15 roles + W2 6 causal) + 58 curated quotes (W3a 28 events +
W3b 30 people/dragons), all Sonnet-proposed, Haiku fresh-verified:
W1 14C/1A/0P · W2 6C/0A/0P · W3 58C/0A/0P.

## Decisions

- **W1-14 (racallio-ryndoon COMMANDS_IN daughters-war) [AMBIGUOUS quote-fragment]:**
  KEEP, quote strengthened to the line the verifier itself identified
  ("Racallio overran the islands in a trice and put the reigning King of the
  Narrow Sea to death...") — byte-copied from fab-the-hooded-hand-21.md:123.
- All other rows kept as proposed. No drops.

## Standing audits (assemble-final.py, all pass)

- No VICTIM_IN anywhere in the batch (war-node harm-gate moot by construction).
- 0 duplicates vs edges.jsonl; 0 in-batch duplicates; all 21 quotes exact
  single-line substrings; all 58 curated quotes verified AT their stated line.
- W2 proposer independently caught + dropped a would-be duplicate
  (battle-of-the-kingsroad TRIGGERS death-of-aegon-ii already exists, run_id
  fab-causal-spine-s204).

## Design-compliance notes

- Umbrella wiring: dance-of-the-dragons gets COMMANDS_IN per side (WO5K
  pattern), NO causal edges to/from the umbrella (chain-as-arc, S105/S106).
  Existing weak rows (AGENT_IN aegon-ii, PARTICIPATES_IN rhaenyra) left in
  place — different types, not dups; noted as residue below.
- W2 skipped 8 investigated gaps honestly (2-hop paths already present,
  sequence-not-causation, umbrella out of scope) — recorded in the proposals
  file's `skipped` array.

## Residue (recorded, not this dip's work)

- `caltrops` FIGHTS_IN dance-of-the-dragons — junk row (an artifact "fighting"
  in a war); candidate for a hygiene drop pass.
- Existing dup edges spotted: blood-butcher AGENT_IN murder-of-prince-jaehaerys
  ×2; viserys-i VICTIM_IN death-of-viserys-i ×2 — pre-existing, S200-guard-era
  informational class.
- `the-dragons-wroth` is Conquest-era (10–12 AC Dornish war), NOT Dance — my
  audit list swept it in by name-vibes; its new quotes are correct for the node.
  W3a flagged tier-2 stamps on death-of-queen-rhaenyra / death-of-lucerys
  despite primary-chronicle sourcing — confidence-tier review candidate.
- gap-map-output.txt's edge dump was incomplete (only edges touching the listed
  event set); W2 re-derived from edges.jsonl directly. Fix the script if reused.
- No node for Willem Blackwood, Jaehaera's death (133 AC), or a "Fishfeed"-era
  first-Tumbleton Treasons sub-event; arrax node has an empty Identity section.
- HotD principals' remaining thin cards (Rhaena Targaryen deg 0, Daeron the
  Daring deg 1, Morghul/Shrykos/Dreamfyre 0 roles) — below this dip's cut.
