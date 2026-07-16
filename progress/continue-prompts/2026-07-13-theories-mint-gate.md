# SESSION 218 — Theories MINT-GATE review: Matt's mint decision over the 13 staged wave-1 clusters

> **This is Session 218.** Stamp your worklog entry `### Session 218` at endsession.
> (Renumbered 217→218 at the S217 endsession: S217 was a docs/deploy meta session that
> changed NO graph state. Everything in the State section below still holds verbatim.)
> **Recommended model:** **Fable orchestrator** (this is an adjudication + potential first-mint session with Matt; any new builds spawn Sonnet proposers + Haiku fresh-verifiers).
> **PRE-REQ:** S216 committed+pushed. If git log disagrees with worklog.md S216, STOP and reconcile.

## State (end of S216)

**ALL 13 wave-1 clusters are STAGED at the mint gate, fully validated** — 105
SUPPORTS/CONTRADICTS edges, 8 new `concept.theory` nodes, 6 stub enriches. Every
cluster ran: Sonnet proposer → deterministic quotecheck → 2 Haiku adversarial
fresh-verifiers → Fable adjudication → scratch dry-run (edges + nodes both
off-graph). Per-cluster records: `working/theories/<cluster>/ADJUDICATION-s216.md`
(+ `rlj-cluster/REVIEW-s216.md` for the S216 pressure-test cycle). Live graph
untouched: edges.jsonl 26,740.

Clusters (dirs under `working/theories/`): rlj (13e) · eldritch (8e) · gnc (10e) ·
bolton (5e) · gmc (10e) · ajt (4e) · jojen (9e) · hooded (12e) · coldhands (7e) ·
patchface (7e) · azor (14e) · pinkletter (11e) · bloodraven (8e).

**"The real Jon Snow" (qSy2uaJ7ecU) is INGESTED** (wave-2 opener): 205 beats / 8
headers / ~57 byte-verified cites on disk; its cluster BUILDS are wave-2 work, not
yet proposed.

## The work

1. **Mint decision with Matt** — walk the staging tally; he picks mint-all /
   mint-subset / hold. **On any mint go:** per cluster run
   `scripts/mint_enrichment.py --candidates working/theories/<cluster>/candidates.json`
   (+ `--nodes-dir` where the cluster has nodes/), apply each `enrich/*.node.md`
   over its live stub, then `weirwood refresh` (new nodes + aliases) + rebuild
   affected indexes. **architecture.md sync is REQUIRED in the same batch**
   (orchestration rule 6): `concept.theory` frontmatter fields (`claim`, `status`
   [open | show-confirmed | jossed], `origin`, `video_sources`, `pass_origin`),
   SUPPORTS/CONTRADICTS semantics (evidence-node → theory-node), theory tier floor
   3–5, the layer rule + subject-link pattern.
2. **Open questions for Matt (adjudicate at the gate):**
   (a) question-form display names for unresolved whodunits ("Who is the Hooded Man
   of Winterfell?" / "Who is Coldhands?" / "Who Wrote the Pink Letter?") — ratify as
   the whodunit-class convention or force declarative;
   (b) may wave-2 theory edges cite `fab-*` chapters? (wave-1 rule was 5-book
   grounding; the corpus has carried F&B since S198);
   (c) novel edge-source node classes — foods (`weirwood-paste`), legend/texts
   (`rat-cook`), concept (`wights`) — ratify;
   (d) the S216-practice conventions listed in the worklog S216 Active Decision
   (layer rule, tier floor, subject-link pattern) — formal ratification;
   (e) chat exposure remains explicitly DEFERRED (do not re-open unless Matt does).
3. **If minted: post-mint verification** — `verify_node_quotes.py` (staged bodies
   carry quotes), gate suite (pytest + deno), a query-layer probe (resolve/neighbors
   on r-plus-l-equals-j), and NO deploy without a separate go (the chat guardrail
   makes theories invisible to the chat regardless — bundle impact is dossier-only).
4. **Wave-2 (only if Matt wants it this session):** Jon Snow cluster builds from the
   ingested qSy2uaJ7ecU substrate (Night's King parallel · resurrection/AA overlap
   with the staged azor cluster — dedup carefully · character-enrichment beats are
   NOT theory material, route them to a future enrichment dip). "The real X" epics
   queue continues per `working/theories/README.md`.

## Residue (non-blocking)

- Byte-fail redo pool grew: ~36 wave-1 rows + 41 jonsnow rows (p1's false
  "byte-verified" claim — 32 fails; p2-redo 1) — a consolidated Haiku redo could
  rescue some; only needed before the affected beats' clusters build.
- Haiku regrounding failure modes now = invent (S214) AND blanket-giveup (S216 p2;
  caught by orchestrator, not byte-check) — fold the anti-giveup contract (mandatory
  logged grep attempts + famous-line calibration) into regrounding-agent-spec.md.
- Dangling `ramsay-bolton` slug link on live `bastard-letter`/`pink-letter-delivered`
  nodes (should be `ramsay-snow`) — small fix, rides any mint session.
- Coldhands B30/B35 still missing (S214 spend wall).

## Vocabulary (paste into subagent prompts — they don't load CLAUDE.md)

Pass = big numbered corpus sweep; Track = named chunk of work; step (lowercase) =
ordered piece inside a Track; Tier = confidence rating 1–5 ONLY.
Harvest rule: while in chapter text for ANY reason, drop `chapter:line / kind / note`
pointers to notable off-task finds into the agent's own harvest file; POINT, don't extract.

## DO NOT

- Do NOT mint/deploy ANY theory node or edge without Matt's explicit go IN THIS
  SESSION (S214 standing; the S216 validation satisfies the review requirement but
  the go itself is still his).
- Do NOT let theory claims into tier-1/2 or into node prose stated as fact.
- Do NOT touch the chat's no-theories guardrail (exposure explicitly DEFERRED).
- Do NOT re-pull ASX transcripts (16 clean on disk incl. qSy2uaJ7ecU).
- Do NOT run /endsession without permission.
