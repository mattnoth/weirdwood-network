# SESSION 181 — Graph parentage cleanup, phase 2: node merges + conflation-bucket splits
> **This is Session 181.** Stamp your worklog entry `### Session 181` at endsession.
> (Renumbered from 180→181: S180 fired on unrelated chat-UI + infobox-disambiguation
> work instead, per Matt's redirect — this track never got picked up, just delayed one slot.)

> **STALE-INPUT WARNING (added at S180 endsession, read before trusting the JSONL below):**
> S180 shipped an UNRELATED fix (wiki-infobox-parser.py + infobox-merge.py: a piped-wikilink
> disambiguation-title bug — see worklog S180 entry) that corrected 375 relationship
> resolutions and retracted 137 stale wrong edges graph-wide. Side effect: the >2-parent
> count this file's "50" figures were built from has dropped **50 → 13** (verified by
> direct query at S180 endsession). Confirmed ZERO slug overlap between S180's 375 fixed
> rows and this file's `parent-edge-proposal.jsonl` — the classes below are not directly
> invalidated. But the underlying edges.jsonl changed materially since the classifier ran.
> **Re-run `scripts/audit-parent-conflation.py` FRESH before trusting any count/slug in
> this file** — treat the JSONL/verdict docs below as directional (the taxonomy and rules
> still apply) rather than an exact current inventory.

> **Track:** graph-data correctness (graph track, global S-numbering → `worklog.md`).
> Phase 1 (S179) shipped the 138 provably-safe PARENT_OF deletes + epithet aliases +
> resolver ranking. This phase handles the two classes the S179 cold-reviews said MUST
> NOT auto-apply, plus the conflation buckets.
>
> **Recommended model:** Sonnet 4.6 (deterministic apply scripts + fresh subagent review;
> the same shape as S179).

## Start here — read the S179 outputs first (do NOT re-derive from scratch)

The classifier + two cold-reviews already ran. Read, in order:
- `working/graph-cleanup/parent-edge-proposal.jsonl` — every PARENT_OF edge into a
  >2-parent node, with `edge_class` (produced by `scripts/audit-parent-conflation.py`;
  re-run it to refresh — it's read-only). After S179's 138 deletes, 50 nodes still have
  >2 parents; those are exactly the classes below.
- `working/graph-cleanup/cold-review-verdict.md` — the taxonomy review (caught the
  two-Aerions false-merge; explains the guards).
- `working/graph-cleanup/deletion-safety-and-alias-review.md` — the deletion-safety +
  **merge⇒alias** analysis. Its §(b) is the rule this phase must implement.

## The work (three classes, gated by a fresh review — Matt can't hand-review these)

**1. `DUPLICATE_PARENT_NODE` (~32 edges).** One real parent under two slugs (maiden/married
`elenda-caron`=`elenda-baratheon`; `damon-lannister`→`-son-of-jason`; Petyr's mother
`alayne`→`alayne-baelish`). Fix = a cross-identity node MERGE (retire the dup slug into the
canonical), which collapses the duplicate parent edge. **HARD RULE from the S179 review:**
- Canonical = the DISAMBIGUATED variant slug, or the wiki-redirect TARGET — NEVER
  highest-quote-count (that rule inverts on namesakes). Confirm each pair is ONE person
  against the LOCAL wiki (`sources/wiki/_raw/<Page>.json`; a literal "Redirect to: X"
  settles it) before merging.
- **merge ⇒ preserve retired name as alias:** when you retire a slug, add its natural
  SPACED-phrase name (and its aliases) onto the surviving node's `aliases:` so the maiden/
  old name still resolves. Bake this into the merge tooling so it can't be forgotten
  (`project_node_alias_spaced_phrases`).

**2. `WRONG_NAMESAKE` (~36 edges).** A bare high-qc slug collides with a disambiguated
variant that are DIFFERENT people (the two Aerions: bare `aerion-targaryen` qc8 = Aerion
the Monstrous vs `aerion-targaryen-son-of-daemion` qc0 = Aegon I's real father). Fix =
DELETE the wrong-namesake edge, KEEP the correct variant. Verify each against the wiki
disambiguation header before deleting. Do NOT merge these.

**3. `NODE_SPLIT` (8 conflation buckets).** Bare slugs holding parents of ≥2 distinct
people: `brandon-stark`, `rickon-stark`, `rhaella-targaryen`, `elaena-targaryen`,
`rhaenys-targaryen`, `rickard-stark`, `sansa-stark`, `joffrey-baratheon`. These need
node-splitting/disambiguation, not edge-pruning. **`joffrey-baratheon` = KEEP all 3**
(cersei + robert[presumed] + jaime[biological] is a legit special case, per the review).
For the others, decide per-node whether the bare slug is a real character that should keep
its 2 true parents (e.g. brandon-stark qc7 = Ned's brother → rickard + lyarra) with the
other-era parents pruned/rehomed. This is the judgement-heaviest class — fresh subagent,
policy-gated, present summaries not edge-lists.

## Method (same machine as S179)
1. Extend/adapt `scripts/apply-parent-conflation.py` (or a new `apply` mode) for merges +
   namesake-deletes — deterministic, dry-run first, assert exact counts.
2. Fresh general-purpose subagent(s) verify each merge/delete/split against LOCAL wiki +
   chapters before apply (`feedback_subagent_verify_not_matt`, `feedback_fresh_review_and_out_of_sample`).
   Batch sequentially near quota (`feedback_sequential_near_spend_caps`).
3. Apply only after review clears; rebuild bundle (`scripts/build-chat-export.py`) + indexes
   + alias resolver (regenerate `all-node-alias-lookup.json` via `event_alias_resolver.py`,
   then rebuild — the merge aliases must land). Re-run the Aegon family tree to confirm.

## DO-NOT
- No node/edge mint, merge, or delete until the fresh review clears (Agents propose, Matt
  gates by policy on summaries).
- Never `git add -A` — a parallel sigils session may still be editing ~380 house nodes; stage
  only your own files by explicit path.
- Never write to `sources/`. Never re-fetch the wiki (read the local cache).
- Do not run `/endsession` without Matt's explicit permission.

## Also queued (separate task chip, not this track)
Delete the mistyped non-canon node `list-of-characters-created-for-the-cyanide-game`
(video-game list-article typed `character.human`; "the butcher"/"the collector" alias it) +
drop those aliases from the generator, per `project_video_game_entities_excluded`.
