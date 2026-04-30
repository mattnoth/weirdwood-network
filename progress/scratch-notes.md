# Scratch Notes

Observations worth keeping but not yet triaged. Tag with source/date.

---

### Wiki Pass 2 — paren-page slugs fail validator (Session 22, 2026-04-26)

`.claude/agents/wiki-ingester.md` line 62 slug rule: "lowercase, strip apostrophes/commas, hyphenate spaces". Doesn't strip parentheses. Wiki disambiguation pages like `Alys Arryn (wife of Rhaegel)` produce slug `alys-arryn-(wife-of-rhaegel)` which fails the validator's `[a-z0-9-]+` regex. `track_b_row.slug` is `None` for these pages, so the fallback rule kicks in.

**Manifests have the correct form already**: `expected_nodes` lists `alys-arryn-wife-of-rhaegel.node.md` (parens stripped). Mismatch is purely in the agent's slug derivation.

**Affected buckets in pending core (3 buckets, 8 paren-pages total):**
- `characters-house-arryn` (3) — already failed validation
- `characters-house-baratheon` (1)
- `characters-house-stark-h-q` (4)

**Fix (one-line agent prompt update):** "lowercase, strip apostrophes/commas/parentheses, hyphenate spaces" → safer: "lowercase, replace any non-`[a-z0-9-]` char with hyphen after lowercasing+hyphenating spaces, collapse multiple hyphens".

**Plan:** Let the 3 buckets fail naturally during Stage 1 run. After tabs go idle (rate-limit window or all 36 attempted), patch agent prompt + reset the 3 failed buckets + re-run them.

**Why this isn't a runbook §"Known risk areas" item:** the validator caught it (good), and the validator-report.json clearly identifies the failed nodes. Not a silent-rename gap. Just a prompt-incompleteness gap.

---

### Spoiler gating deferred for v1 wiki nodes (Session 19, 2026-04-26)

`first_available` was previously framed as "architectural, not optional" — it lives in CLAUDE.md and architecture.md as a required field on every node. For v1 wiki ingestion, that requirement is **suspended**: the wiki-infobox-parser only populated it for ~55% of pages, and forcing the agent to derive it for the rest would flood the question channel without near-term value.

The current state:
- `.claude/agents/wiki-ingester.md` lists `first_available` as **optional** v1 frontmatter
- `scripts/wiki-pass2-validator.py` does **not** check for it
- The agent copies it from `track_b_row.first_available` if present, else omits

This needs to be reconciled when spoiler gating becomes MVP-relevant. Options:
- **Backfill pass** — dedicated session(s) to populate `first_available` on all v1 wiki nodes once Pass 1 completes the remaining 4 books (more chapter cite data → better derivation accuracy)
- **Re-derive from corpus** — once the index/graph is stable, scan all chapter extractions for first-mention timing and write back to nodes
- **Reset wiki nodes to v2 at that time** — `weirwood wiki reset --version v1` archives v1, v2 has spoiler gating live

The decision is well-scoped (scope decision Matt made in session 19, captured in worklog), but the principle in CLAUDE.md isn't yet updated. When spoiler gating lands, edit CLAUDE.md + architecture.md to reflect the version split (v1 = open canon, v2+ = gated).

### Smoke-test launcher silent exit (Session 19, 2026-04-26)

`weirwood wiki run core --bucket direwolves` exits silently after "--- Orphan recovery (threshold=60min) ---" under `set -euo pipefail`. No "No pending buckets found" message appears, which would be the next legitimate output if the manifest collection produced nothing. Some command between `run_orphan_recovery` and the `pending_manifests` collection loop returns nonzero and kills the script.

Fix is in continue prompt `2026-04-26-wiki-pass2-smoke-debug.md`. Likely candidates: `ensure_stats_csv` (path-creation/permissions), `list_manifests` (find under set -e), or something inside the read-loop. Use `bash -x` to isolate.

---

### POV Reference Table Gaps (Session 2, chapter-splitter)

The original `reference/pov-characters.md` was missing 6 chapter headings. All have been added:
- AFFC: THE REAVER (Victarion Greyjoy)
- ADWD: THE BLIND GIRL (Arya), A GHOST IN WINTERFELL (Theon), THE IRON SUITOR (Victarion), THE KINGBREAKER (Barristan), THE QUEEN'S HAND (Barristan)

### Smart Quotes in Source Files (Session 2, chapter-splitter)

Source .txt files use Unicode curly/smart quotes (U+2019 right single quote mark instead of U+0027 straight apostrophe). The chapter splitter normalizes these before heading matching. The wiki scraper may also need to be aware of this if cross-referencing chapter text.

### Relational DB Decision — Defer (Session 13, 2026-04-25)

Not needed yet, and probably not for a long time. Reasoning:
- Pass 2 output is ~5,279 wiki entities + ~17K cite_ref records. That fits easily in JSONL/markdown and grep.
- Access patterns so far are: "find entity X," "find all entities with edge Y," "filter by `first_available`." All trivially served by JSONL + Python or markdown + grep.
- A graph DB (Neo4j) becomes useful when you need real traversal queries — "find all characters within 3 hops of Jon Snow who appear before AGOT Bran III." That's still 1–2 passes away.
- The Active Decision in worklog (`OPEN: Storage Format`) already leans markdown-first. Confirming that lean.
- Migration cost from JSONL → SQLite → Neo4j is low because the parser output is already structured. The choice can be deferred without painting into a corner.

**Recommendation:** stay with JSONL + markdown for Track B. Revisit when there's a query that's painful without traversal.

### Collaborator Onboarding — Schema Lock-In Before Handoff (Session 13, 2026-04-25)

A collaborator may join to share the extraction load — effectively running concurrent extraction agents from another machine. Implication: the Pass 1 schema (and surrounding pipeline) needs to be **ironclad before handoff**, because the collaborator is not as deep a fan, doesn't remember the books in detail, and hasn't done the theory-video research. They need a process that produces correct output without needing the lore knowledge to second-guess the schema.

What this changes:
- **Track B sequencing reaffirmed:** schema review after Track B (informed by wiki coverage) is even more important if a non-expert is going to run the schema across more books.
- **`/install-github-app` value rises:** tagging Claude in PRs/issues from GitHub becomes the natural review surface for collaborator-produced extractions. Revisit installing once schema is locked and collaborator is ready.
- **Documentation needs:** README's onboarding flow should hold up for a collaborator who has the source files but isn't going to read the worklog. The skip-ahead note (Session 13) helps. May need a "running extractions" quick-reference doc that doesn't require reading CLAUDE.md end-to-end.
- **Schema lock-in checkpoint:** before handoff, do a full v3 schema review across AGOT (post-Track B) and resolve any open issues. Treat schema lock as a hand-off gate.

### Foreshadowing Pass Prep — Expand Event List & Chekhov's Guns (Session 13, 2026-04-25)

**Long-lead reminder for Pass 4 (foreshadowing-scanner):**

`reference/foreshadowing-events.md` currently has 26 events + 15 Chekhov's guns. Before running Pass 4, audit and expand both:

1. **Foreshadowing events** — review whether 26 known-future-event anchors are enough for the scanner to be useful. Likely too few. Add events from:
   - Major character deaths and identity reveals (Red Wedding, Joffrey, Tywin, Jon's stabbing, Hardhome, Quentyn's burning, Stannis's march on Winterfell, Bran's warging, etc.)
   - Major plot reveals (Lannister twincest, Jon's parentage hints, Arya's Faceless Men arc, Bran's Greenseer arc, Sam's Citadel arc, Davos's resurrection role, Theon's redemption arc)
   - Magic returnings (dragons hatching, White Walkers reawakening, glass candles burning, warging confirmed)
   - Prophecy fulfillments and inversions
2. **Chekhov's guns** — current list is 15. Expand to build a *pattern* the scanner can use to find *unknown* Chekhov's guns. Each gun entry should describe:
   - The setup (where the object/fact/character is introduced)
   - The shape of the payoff (or "unfired" if still open)
   - The textual pattern that signals "this matters later" (named in dialogue, dwelt on by POV, contrasted with normal description, etc.)

The pattern library is the actual scanner input. Without it, the scanner can only check for events the user already named. With it, the scanner can flag *candidate* foreshadowing for unknown payoffs — which is the whole point of Pass 4.

**Action when Pass 4 nears:** dedicated session to expand the events list and Chekhov's gun pattern library. Before then, surface this scratch-note in Pass 4 prompt design.

### Wiki cache shape: 70% stubs (Session 18, 2026-04-26)

After running `wiki-pass2-triage.py` end-to-end against the 17,657 cached AWOIAF pages:
- **5,279 (29.9%)** have infoboxes → real triage buckets (`characters-house-stark`, `houses-north`, `battles`, `titles`, etc.)
- **12,378 (70.1%)** have no infobox → 12,328 land in `singletons-unknown`, 50 land in `disambiguation` / `tv-only-skip` / etc.

Of the 12,328 singletons-unknown: 12,266 have ZERO populated signals — these are stubs, redirects, calendar pages (e.g., "1 AC", "10 BC"), short list pages. The 62 with *some* signal are mostly partial pages whose signals (region, culture) didn't match a known bucket rule.

Implication for tripwire: the default 0.8 threshold is wrong. Real data shape is ~30% of the corpus is bucketable. Options for v2:
- Lower threshold to ~0.25
- Measure against `pages-with-infoboxes` (5,279) instead of total
- Add a `pre-tripwire-filter` stage that excludes pages with `byte_size < 1KB` and `cite_ref_total == 0`

The runbook's whole point of triage is to filter stubs out. Tripwire was originally calibrated for a hypothetical "every page should classify cleanly" world. Reality: triage's job IS to identify stubs, not classify them.

### Scheduled Launches — Direction Bank (Session 16, 2026-04-25)

Surfaced during the wiki Pass 2 orchestration review when the rate-limit-prevention discussion expanded. Option C in the auto-relaunch todo (`weirwood schedule`) is the immediate need; these are downstream directions that share the same primitive (cron / launchd / `CronCreate` triggering `weirwood` and friends).

**Directions worth considering once `weirwood schedule` exists:**

1. **Multi-day unattended runs.** Pass 2 spans weeks of API time at any reasonable rate. Cron-triggered launches with auto-relaunch on rate-limit reset = walk away for a week, return to a finished tier. The combined feature (Option A auto-resume + Option C scheduling) is more powerful than either alone.

2. **Off-peak cost.** Anthropic doesn't have differential pricing today, but if it ever lands or if your daily quota refills overnight, scheduling shifts work onto cheaper time without active management. Cheap to add now (just a time-of-day arg); pays out if pricing changes.

3. **Cross-pass orchestration / event-driven pipeline.** "Run Pass 1 ASOS overnight; if it succeeds, schedule a Pass 2 incremental triage at 6am that picks up new entities; if Pass 2 finishes, kick off the v3 schema review at 10am." A pipeline triggered by completion events, not by Matt sitting at the keyboard. Implementation: each launcher writes a completion sentinel; a scheduler (`weirwood pipeline`) reads sentinels and dispatches the next stage.

4. **Periodic re-crawl + diff.** Wiki gets updated periodically (real authors, real edits). Schedule a weekly partial re-crawl of pages whose `last-modified` headers changed, diff against cached version, only re-trigger Pass 2 buckets that touch changed pages. Keeps the graph fresh without re-running the universe.

5. **Proactive monitoring.** A scheduled `weirwood status` post that runs every Monday and notifies if anything stalled — Slack webhook, email, or just a markdown report committed to the repo. Catches broken runs before Matt notices via "wait, when did I last extract anything?"

6. **State snapshotting.** Daily commit of `extractions/` (already gitted), `graph/`, and stats CSVs gives a free time-series of project state. Useful for retroactive debugging ("when did the schema change break ACOK extractions?") and for showing progress over time. Gitignored content (raw text, wiki cache) stays out — only derived artifacts get versioned. Probably wants its own branch (`snapshots/`) so daily commits don't pollute main history.

7. **Notification sinks.** Once scheduled work is running, you want output channels: completion notifications, rate-limit halt alerts, validator failure summaries. Slack webhook is cheapest; email second; a self-hosted dashboard is overkill until volume justifies. Probably wire one channel and grow as needed.

**Common primitives across all six:**
- A scheduling layer (cron / launchd / `CronCreate`).
- Sentinel files for inter-stage signaling (`working/sentinels/<stage>-complete.json`).
- A status-emitter that produces machine-readable snapshots (likely the same JSONL or CSV the launchers already produce).
- An optional notification adapter (Slack/email/markdown).

**Sequencing recommendation:**
- v1 (immediate): Option A + Option C as filed in todos — single-pass auto-resume + manual `weirwood schedule`.
- v2 (after v1 proves out): completion sentinels + 1-step pipeline (e.g., Pass 1 done → triage runs).
- v3 (later): full event-driven orchestration + monitoring sink + snapshotting branch.

Don't build past v1 until the primitives are exercised; the directions above are *what becomes possible*, not what to build now.
