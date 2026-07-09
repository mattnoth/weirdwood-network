---
session: 202
date: 2026-07-09
track: graph
model: Fable 5 (orchestrator) + Sonnet subagents (B4) + Haiku subagents (B5–B7, Matt-directed downgrade)
graph_mutation: YES — continuation of Matt's S201 apply-go; batches 4–7 of 7 applied + close-out residues
---

# Session 202 — F&B bulk reconcile-apply: the Dance batches 4–7 + small close-out residues

## Setup
Resumed from `2026-07-07-fab-bulk-reconcile-apply.md` at Batch 4. First verified S201's batches 1–3
end-to-end (commits, 847 book-fab edge count, semantic gate re-run PASS, 153 tests, surgery spot-checks
incl. both disambiguation renames) — all clean.

## The verification layer earned its keep — in both directions
The continue prompt's core warning (S200: 2 of 4 subagent clears were wrong) shaped the whole session:
every load-bearing subagent claim was re-verified against the chapter text. Both directions mattered:

- **Subagent right, orchestrator's pre-read wrong (B4):** I pre-read the Saera passages and expected
  the three LOVER_OF rows to be euphemism-class ("favorites"). The Sonnet adjudicator dug deeper and
  found her direct court confession ("I gave it to all three", 14-p03:217) — verified verbatim, all
  three flipped to flat tier-1. My baseline had been built from an incomplete read.
- **Subagent wrong, orchestrator caught it (B5 fresh-verify flag):** the agent flagged
  `viserys-i AGENT_IN tongue-removal-of-vaemonds-kinsmen` as chronologically implausible ("after
  Viserys's death"). The book says otherwise (heirs-15-p03:165 — King Viserys ordered the tongues
  removed, 126 AC, alive) — the agent had the SHOW's timeline. Flag rejected.
- **Subagent invented a convention (B6):** fresh-verify proposed folding Hugh Hammer's coronation and
  death into `second-battle-of-tumbleton`, claiming "the graph keeps sub-events within battle
  narratives." That contradicts the beat-reification pattern (death-of-ygritte, death-of-lucerys…),
  and the self-coronation predates the battle. Both folds rejected; both beat nodes minted.

## Verdict overrides (6 total, all primary-text anchored)
- B5: Addam/Alyn `SAME_AS` rows clear→**drop** — both Hull names already alias to the -velaryon slugs
  (matched.jsonl proof); the edges would self-loop. Textual claim itself was flat (legitimization).
- B6 R4: garth BETRAYS rhaenyra disputed→**clear** — the adjudicator over-extended a Mushroom zone;
  the attribution attaches only to Rhaenyra "ashen and inconsolable" (and Mushroom stayed in KL).
- B6 R23: benjicot ALLIES_WITH cregan disputed→**clear** — both chroniclers agree the Lads joined
  Stark's march; only the motive (willing vs cowed) is contested. Details-contested pattern; over-tagging
  flat facts dilutes the dispute signal the S199 audit fought for.
- B6 R9: larys KILLS aegon-ii disputed→**DROP** — the text explicitly says the poisoner's hand "will
  never be known"; only the BEHEST is Gyldayn's inference ("we can have no doubt"). KILLS misstates even
  the source. Correct encoding = `death-of-aegon-ii` event + larys SUSPECTED_OF — queued as event-residue
  (no death event node exists; not in the deferred sidecar either).

## The Haiku downgrade (Matt-directed) and its A/B
Matt: "use cheaper sub agents where possible." Adjudication went to Haiku immediately (safe because the
orchestrator re-verifies 100% of verdicts + excerpts). Fresh-verify was A/B'd on B5 with a litmus test
embedded: the `aegon-nephew-of-maegor` char CREATE (= Aegon the Uncrowned, resolver miss on the
parenthetical name-form). Haiku caught the fold with the right target AND resolved the Hull-brothers
identity question — so B6–B7 ran fully on Haiku. Verbatim excerpt checking needed apostrophe
normalization (curly ’ vs straight ') to avoid false fabrication alarms — 3 B7 "misses" were all this.

## Mechanics refined this session
- **Inject-before-surgery ordering** (B5 lesson): a dispute edge targeting a to-be-folded CREATE can't
  retarget if surgery runs first (surgery rewrites candidates.json only, not matched.jsonl). B5's
  leftover KILLS row ("unresolvable name") was wired manually as DISP-M1 with final slugs.
- `fab-apply-surgery.py` promoted from S201's ephemeral scratchpad to `scripts/` (spec-driven,
  parameterized — the S158 convention; scratchpads don't survive sessions).
- Cross-unit CREATE dedup proven live: `poisoning-of-gaemon-palehair` extracted by both lysene-24 parts;
  mint skip-if-exists deduped the node, both units' edges attached.

## Numbers
B4 +322 / B5 +191 / B6 +256 / B7 +275 = **+1,044 book-fab edges (847→1,891)**; event nodes 868→**963**;
edges.jsonl **24,988** (after the vaegon dup-drop). Disputed book-fab 98, all with in_universe_source.
62 dispute rows adjudicated (55 clear / 4 disputed / 3 drop after overrides). 6 FOLD + 4 RENAME + 2
rejected folds. Every batch: mint/merge 0-skipped/0-not-found, gate PASS, 153 tests, git checkpoint.

## Close-out residues fixed in-session
vaegon/vaegon-targaryen dupe folded (stub deleted, 2 dup edges dropped, aliases added);
great-council-of-101-ac retyped event.battle→event.council + real Identity line.

## What's next
`progress/continue-prompts/2026-07-09-fab-close-out.md` (S203): deferred-events triage (37 + the
death-of-aegon-ii residue), Lineages §3.4 parser build + diff, review-bucket triage plan (1,440 rows),
F&B harvest drain (337 rows), small residues (KNIGHTED_BY direction audit, capture-of-prince-viserys
date). Strip-boilerplate track un-park condition is NOW MET — Matt-gated.
