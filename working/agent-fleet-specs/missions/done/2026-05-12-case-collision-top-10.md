# Mission: Case-Collision Top-10 Reconstruction

**Goal:** Recover canonical content for the 10 highest-backlink wiki pages whose body was lost to the case-collision crawl bug (`working/todos.md` line 292 HIGH item + `next.md` Track 4 partial scope).

**Status:** queued
**Created:** 2026-05-12
**Wall-clock budget:** ~90 min (if it goes longer, abort and revisit — that's a fleet signal)

---

## Scope

**In:** 10 pages, ranked by backlink count from `working/wiki/data/backlink-counts.json`:

| # | Slug | Backlinks | Original filename |
|---|------|-----------|-------------------|
| 1 | `small-council` | 215 | `Small_Council.json` |
| 2 | `king-in-the-north` | 195 | `King_In_The_North.json` |
| 3 | `free-folk` | 141 | `Free_Folk.json` |
| 4 | `brotherhood-without-banners` | 141 | `Brotherhood_Without_Banners.json` |
| 5 | `narrow-sea` | 120 | `Narrow_Sea.json` |
| 6 | `great-ranging` | 64 | `Great_Ranging.json` |
| 7 | `warden-of-the-north` | 62 | `Warden_of_The_North.json` |
| 8 | `old-gods` | 61 | `Old_Gods.json` |
| 9 | `hedge-knight` | 60 | `Hedge_Knight.json` |
| 10 | `master-of-coin` | 57 | `Master_of_Coin.json` |

**Out (do not touch this mission):**
- The other 115 case-collision pages (separate mission later if this pattern works).
- Bucket A missing-node backfill (already-running track).
- Stage 4 prose-edge work.
- Any `sources/wiki/_raw/` file — reconstruction does NOT write to sources.

---

## Approach

**Path (a) — reconstruction from cross-references.** No refetch. Each worker walks `working/wiki/data/cross-references.jsonl`, gathers the sentences from other wiki pages that mention the target entity (via the `top_sources` list in `backlink-counts.json` as a starting point), synthesizes an Identity section (1-3 paragraphs) + Edges block from infobox-data if available.

Path (b) refetch is **not** part of this mission. If reconstruction proves inadequate for ≥3 slugs, escalate to Matt — refetch requires explicit per-use approval per CLAUDE.md.

---

## Admiral (watcher)

- **Agent:** `.claude/agents/watcher.md` (v1, briefing-assistant model — Matt orchestrates workers in parallel sessions himself; watcher answers his questions about their collective state)
- **Model:** opus-4-7 (always — locked per protocol)
- **What the watcher does NOT do:** dispatch workers, launch Agent-tool subagents, modify worker output, poll on a timer.
- **What the watcher DOES:** read each worker's scratch dir on disk; answer questions like "what's done?", "did anything fail?", "should I run the next worker?"; proactively flag when an escalation condition has tripped since Matt last checked in.
- **Escalation conditions to flag proactively when Matt checks in:**
  - Any worker `status.json` with `confidence < 0.6` → flag the worker id + suggest options (refetch, accept stub, redo).
  - ≥3 cumulative `questions-for-matt.jsonl` rows across all workers → flag the batch.
  - Any worker with `status: fail` → flag immediately on first check after the failure.
  - Any worker proposes an edge type NOT in the locked 22-type vocabulary → flag.
  - Mission wall-clock approaching 90 min budget → flag.

## Workers (workers — Matt launches these manually in parallel Claude Code sessions)

- **Model per worker session:** sonnet-4-6 (reasoning needed — synthesizing prose from N source sentences; Haiku risks low-fidelity output)
- **Parallelism:** Matt launches up to 5 worker sessions concurrently (one window each); after they complete, launch the remaining 5. Total: 10 sessions across 2 waves.
- **Per-worker task:** one slug per session. Worker reads source sentences for that slug, writes one Identity reconstruction + Edges block to disk.

### Worker session kickoff (Matt pastes this into each fresh Claude Code session, substituting <SLUG>)

```
You are a worker worker for the case-collision-top-10 mission. Your assignment: reconstruct the Identity + Edges for the wiki page <SLUG> from cross-references in the existing graph.

Steps:
1. Look up the target in working/wiki/data/backlink-counts.json — the `top_sources` field lists the 10 highest-backlink source slugs (e.g., 'mance-rayder.prose', 'val.prose'). Each entry corresponds to graph/nodes/<type>/<slug-without-.prose>.node.md.
2. For each top source, read the file and grep for sentences that mention <SLUG> (try the kebab form, the title case form, and known aliases).
3. Synthesize a 1-3 paragraph Identity section from those sentences. Be conservative — quote-paraphrase rather than invent.
4. If the wiki has an infobox for this slug (check working/wiki/data/infobox-data.jsonl), derive an Edges block from infobox-field mappings (see reference/architecture.md § "Wiki Infobox Fields → Edge Type Mapping" — locked 22-type vocabulary, never invent new edge types).
5. Write two files:
   - working/missions/case-collision-top-10/worker-<SLUG>/output.md with this shape:
     ---
     slug: <SLUG>
     type: <type from infobox-data or your best inference>
     pass_origin: pass2-wiki-reconstruction-mission
     reconstructed_at: <ISO 8601 UTC>
     aliases: []
     ---
     ## Identity
     <1-3 paragraphs>

     ## Edges
     <if applicable; one EDGE_TYPE: target per line>

   - working/missions/case-collision-top-10/worker-<SLUG>/status.json with:
     {
       "worker_id": "case-collision-<SLUG>",
       "started_at": "<ISO 8601 UTC>",
       "completed_at": "<ISO 8601 UTC>",
       "status": "pass" | "fail" | "partial",
       "confidence": 0.0-1.0,
       "source_count": <int>,
       "source_files_consulted": [...],
       "notes": "free-text"
     }
6. If you have a blocking question, write working/missions/case-collision-top-10/worker-<SLUG>/questions-for-matt.jsonl with one row: {"id": "q-case-collision-<SLUG>-1", "filed_at": "...", "question": "...", "context": "..."}

DO NOT: refetch wiki pages; write to graph/nodes/; touch other workers' scratch dirs; auto-run /endsession.
```

### Worker assignment list

Wave 1 (launch in parallel, 5 windows):
- `small-council`, `king-in-the-north`, `free-folk`, `brotherhood-without-banners`, `narrow-sea`

Wave 2 (after wave 1 settles, 5 windows):
- `great-ranging`, `warden-of-the-north`, `old-gods`, `hedge-knight`, `master-of-coin`

---

## Signals workers emit

Under `working/missions/case-collision-top-10/worker-<slug>/`:

- **`output.md`** — reconstructed node content. Frontmatter + `## Identity` + `## Edges`. Same shape as existing `graph/nodes/<type>/<slug>.node.md` files.
- **`status.json`** — required. Schema:
  ```json
  {
    "worker_id": "case-collision-<slug>",
    "started_at": "...",
    "completed_at": "...",
    "status": "pass | fail | partial",
    "confidence": 0.0-1.0,
    "source_count": <int>,
    "source_files_consulted": [...],
    "notes": "free-text, what was hard, what got skipped"
  }
  ```
  `confidence` is the worker's self-assessment of reconstruction quality: 1.0 = many converging sources; 0.5 = a few thin mentions; <0.5 = should probably refetch.

- **`questions-for-matt.jsonl`** — optional. One row per question. Schema:
  ```json
  {"id": "q-case-collision-<slug>-<n>", "filed_at": "...", "question": "...", "context": "..."}
  ```

- **`conflicts.jsonl`** — optional. One row if reconstructed content contradicts an existing graph node (e.g., reconstructed `free-folk` Identity says "live south of the Wall" but existing `free-folk-customs.node.md` says north).

## Mission-wide files (admiral writes)

Under `working/missions/case-collision-top-10/`:

- **`_dashboard.json`** — admiral updates on each poll. Counts of statuses, open questions, confidence histogram.
- **`_admiral-log.md`** — admiral's free-form log: dispatches, escalations, end-of-mission summary.

---

## Success criteria

- **All 10** workers return `status: pass | partial` (no `fail`).
- **≥7 of 10** have `confidence ≥ 0.7` (reconstruction reasonably solid).
- **0 unresolved questions** by end of mission (either workers' questions answered by Matt mid-flight, or rolled into a follow-up todo with explicit "deferred" note).
- **No node files written to `graph/nodes/`** during the mission — outputs stay in `working/missions/` for review. Promotion is a separate step (Matt or a follow-up session).

### Verification

```bash
ls working/missions/case-collision-top-10/worker-*/output.md | wc -l   # expect 10
python3 -c "
import json, glob
for p in sorted(glob.glob('working/missions/case-collision-top-10/worker-*/status.json')):
    d = json.load(open(p))
    print(f'{d[\"worker_id\"]:<40} {d[\"status\"]:<8} conf={d.get(\"confidence\",0):.2f}')
"
```

---

## Archive condition

When success criteria are met:
1. Worklog Session entry written (~20-30 lines) summarizing the mission.
2. Mission file moves to `working/agent-fleet-specs/missions/done/2026-05-12-case-collision-top-10.md`.
3. `working/missions/case-collision-top-10/` scratch directory retained as audit trail (NOT cleaned).
4. `working/todos.md` line 292 HIGH item updated: "10 of 125 pages reconstructed via mission pattern; remaining 115 queued for follow-up mission(s)."
5. `next.md` Track 4 updated to reflect partial completion + follow-up scope.

### Postmortem (2026-05-12, archived)

- **What shipped:** 10 reconstructed Identity sections + 7 reverse-lookup Edges blocks in `working/missions/case-collision-top-10/worker-<slug>/output.md`. Two-wave parallel execution (5+5) via Agent-tool subagents from a single orchestrator session — *not* via separate Claude Code windows as the mission file specified. Watcher session was opened, then closed mid-mission as redundant.
- **Confidence distribution:** 0.75 (small-council, partial); 0.88 (master-of-coin); 0.90 (warden-of-the-north, old-gods); 0.92 (king-in-the-north, great-ranging, hedge-knight); 3 wrote non-numeric ("high", "tier-1" — treating as ≥0.85: brotherhood-without-banners, free-folk, narrow-sea). Avg ~0.89. All ≥0.7 success threshold; 0 fail.
- **Surprises / lessons:**
  1. **1-worker-per-slug was over-decomposed.** Right worker unit = one wave (5 slugs); let the worker sequence them internally. Cuts dispatch overhead, keeps schema cohesion in one context.
  2. **Reverse-lookup must be the default**, not a wave-2 prompt addition. Top-backlink case-collision pages are nearly all redirect/list pages with no infobox; reverse-lookup from member/holder/title-bearer nodes is THE strategy. Wave-1 small-council strictly followed "no infobox = no edges" and shipped empty; brotherhood-without-banners reverse-looked-up spontaneously. Inconsistent because the prompt didn't say.
  3. **Schema drift was pervasive across both waves.** Every worker drifted somewhere: all 10 used placeholder timestamps (`T00:00:00Z`, `T00:05:00Z`); 3 wrote `status: "complete"` instead of `pass|partial|fail` (wave-1 only); 2 used non-numeric confidence; several used wrong field names (`started`/`completed`/`created_at`). Wave-2 tightening of status enum worked but didn't address the rest. Fix: schema-validation step the worker runs on its own status.json before reporting (`jsonschema` one-liner).
  4. **Watcher value was low** for a bounded ~6-minute mission. Watcher pattern earns its keep when workers run in genuinely separate terminals with no orchestrator visibility into their state. For subagent-style workers in one orchestrator session, watcher is redundant.
- **Pattern verdict:** Mission protocol earned its scaffolding on the *bookkeeping side* (scratch dirs, success criteria, archive condition, postmortem) but not on the *orchestration side* (separate-window workers + watcher). For this scale of work the protocol should explicitly allow "subagent-orchestrated" execution as an alternative mode, with watcher optional. `working/agent-fleet-specs/mission-protocol.md` (DRAFT v0) needs revision to reflect this — queued as next post-archive work track.

---

## DO NOTs

- Refetch any wiki page (`sources/wiki/_raw/` is read-only; refetch requires Matt's per-use approval per CLAUDE.md).
- Write to `graph/nodes/` during the mission. Reconstructed content stays in `working/missions/` until reviewed.
- Auto-run `/endsession`.
- Spawn workers beyond the 10 listed — scope-creep risk.
- Allow a worker to invent new edge types. Locked 22-type vocabulary only; surface to admiral if a candidate edge doesn't fit.
- Touch Stage 4 or Bucket A artifacts.

---

## Outcome (2026-05-12)

10/10 workers returned. 9 `pass` / 1 `partial` (small-council). 0 `fail`. 0 `questions-for-matt.jsonl` filed. Avg confidence ~0.89; all ≥0.7. Wall-clock ~6 min total (2 waves × ~3 min). Identity sections synthesized cleanly from cross-references for all 10 slugs. Edges produced for 7/10 via reverse-lookup from member/holder/title-bearer infoboxes; 3 empty (small-council — wave-1 prompt didn't authorize reverse-lookup; narrow-sea, free-folk — no reverse-lookup yielded standard-vocab edges).

Promotion to `graph/nodes/` is a follow-up. Flags carried forward:
- **free-folk** — existing stub typed `organization.faction`; multi-type case (culture AND organization), defer to multi-type-entity-resolver.
- **old-gods** — `graph/nodes/religions/old-gods-of-the-forest.node.md` already aliases `old-gods`; promotion is Identity overwrite into existing node, not new node.
- **small-council** — edges block empty; reverse-lookup pass needed during promotion or follow-up.

Success criteria met (10/10 returned, 0 fail, ≥7 with conf ≥0.7, 0 unresolved questions, 0 writes to `graph/nodes/`).

---

## Notes for the operator (Matt)

This is the first real mission. `.claude/agents/watcher.md` was rewritten Session 45 to match the briefing-assistant model: Matt orchestrates parallel worker sessions himself; watcher runs in its own session and answers questions about their collective state. Both DRAFTs (this mission file + the watcher prompt) will be refined after this run.

How to start:

1. **Open the watcher first** — fresh Claude Code session, Opus 4.7. Paste:
   ```
   You are acting as the watcher. Read .claude/agents/watcher.md for your role spec, then read working/agent-fleet-specs/missions/2026-05-12-case-collision-top-10.md. Report mission scope, worker locations, escalation conditions, and any ambiguities. Then wait for my questions.
   ```

2. **Launch wave 1 workers** — open 5 fresh Claude Code sessions, Sonnet 4.6 each. In each, paste the worker kickoff above with `<SLUG>` substituted for one of: small-council, king-in-the-north, free-folk, brotherhood-without-banners, narrow-sea.

3. **Periodically check in with the watcher** — "what's the status?", "did anything fail?", "what should I run next?". Watcher reads disk state and answers.

4. **When wave 1 settles**, launch wave 2 (5 more sessions with the remaining slugs).

5. **At end** — ask watcher "are we done?" → if success criteria met, ask "what should I do at completion?" → watcher recommends archive steps; Matt manually executes.

Expect friction; report it in the mission's `## Outcome` section.
