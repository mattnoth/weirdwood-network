# `.claude/` — Custom Claude Tools for the Weirwood Network

Project-specific Claude Code customizations. Read this when you need to know what's available without exploring the directory.

**Index maintenance rule:** when adding a new agent or slash command, also add a one-line entry here. The list isn't auto-generated.

---

## Slash commands (`.claude/commands/`)

Invoke with `/<name> <args>` in any Claude Code session in this project.

| Command | Args | Purpose |
|---------|------|---------|
| `/endsession` | none | Full end-of-session checklist (worklog, session-details, continue prompts, archive). Never run without explicit user permission. |
| `/continue` | `<substring>` or none | Resume a work track from a continue prompt in `progress/continue-prompts/`. No-arg = list priority-ordered candidates. |
| `/check-fleet` | none | Read the fleet orchestrator's state files + audit reports; surface a one-page status summary. (Stub; fleet daemon not built yet.) |
| `/watcher` | `<mission-slug-substring>` | Emit the kickoff prompt for an interactive watcher session against a mission. Paste output as the first message in a fresh Opus 4.7 session. |
| `/worker` | `<mission-slug> <worker-slug>` | Emit the kickoff prompt for a single worker worker. Paste into a fresh Sonnet 4.6 session. One worker per session. |

---

## Agents (`.claude/agents/`)

Most of these are invoked via the Agent tool as subagents — the main session calls them, they run a bounded task, return output, and exit. **Exception: `watcher.md`** is a role spec that an interactive Claude Code session adopts (started via `/watcher`); it doesn't run as a typical subagent invocation.

Agents are listed by pipeline stage / function. See `reference/agents.md` for the canonical detailed roster + status.

### Extraction pipeline

| Agent | Stage | Status | Purpose |
|-------|-------|--------|---------|
| `mechanical-extractor` | Pass 1 | full | Pass 1 mechanical extraction on a chapter file. |
| `wiki-ingester` | Pass 2 Stage 1 | full | Wiki page → structured node file. (Stage 3+ uses Python; this prompt remains for Stage 1 re-runs.) |
| `voice-analyzer` | Pass 3 | stub | Per-POV voice profile + cross-POV perception. |
| `perception-mapper` | Pass 3 | stub | Cross-POV perception edges (PERCEIVED_AS, RESENTS, FEARS, etc.). |
| `foreshadowing-scanner` | Pass 4 | stub | Map foreshadowing prose to known events. |
| `chekhovs-gun-tracker` | Pass 4 | stub | Track planted-but-unresolved details. |
| `theory-extractor` | Pass 5 | stub | Per-theory evidence extraction. |
| `theory-evidence-scorer` | Pass 5 | stub | Confidence score + strongest evidence / counter-evidence per theory. |
| `discovery-agent` | Pass 6 | stub | Open-ended pattern discovery across the full corpus. |
| `chronology-extractor` | Tier 3 | stub | Year-page → temporal edges. Depends on temporal edge vocabulary. |
| `event-orderer` | Tier 3 | stub | Place events in chronological order using cite_refs + chronology + prose hints. |

### Audit & review

| Agent | Stage | Status | Purpose |
|-------|-------|--------|---------|
| `schema-drift-auditor` | post-promotion | full | Surface schema violations (types, edge labels, frontmatter, slugs). |
| `citation-validator` | post-promotion | full | Audit citation hygiene (missing cites, broken cite_refs, malformed formats). |
| `duplicate-detector` | post-promotion | full | Surface candidate duplicate nodes by slug / alias / wiki_source. |
| `orphan-edge-finder` | post-promotion | full | Find edges whose target resolves to no node. |
| `extraction-quality-auditor` | Pass 1 review | stub | Review a batch of Pass 1 chapter extractions for consistency. |
| `cross-book-entity-reconciler` | post Pass 1 multi-book | stub | Reconcile entity references across books. |
| `contradiction-surfacer` | Pass 1 vs graph | stub | Surface where wiki claims (graph) disagree with Pass 1 extractions. |
| `prose-edge-reviewer` | Stage 4 review | full | Review 5% sample of `prose-edge-classifier` output per bucket. |
| `cross-identity-reviewer` | Stage 4 review | full | Review 100% of `cross-identity-detector` SAME_AS proposals. |
| `fleet-stats-reviewer` | post-stage synthesis | stub | Synthesize stage CSVs + audit reports into one-page status. |

### Stage 4 (prose-derived edges)

| Agent | Status | Purpose |
|-------|--------|---------|
| `prose-edge-classifier` | full | Classify prose-derived edge candidates (locked 22-type vocabulary) or reject as just-a-mention. |
| `cross-identity-detector` | full | Decide SAME_AS pairs (Reek=Theon, Alayne=Sansa). |
| `disambiguation-resolver` | stub | Resolve ambiguous references ("King Aegon" → which Aegon). |
| `multi-type-entity-resolver` | stub | Decide policy for multi-type entities (Citadel = org + place). |

### Mission orchestration (NEW Session 45)

| Agent | Role | Purpose |
|-------|------|---------|
| `watcher` | reusable | Briefing-assistant for a mission. Reads worker state from disk; answers Matt's questions; proactively flags escalation conditions. **Started via `/watcher`** — not invoked via Agent tool. Opus-locked. |

### Utility

| Agent | Purpose |
|-------|---------|
| `script-builder` | Write/extend Python scripts for the project. |

---

## Related project artifacts (not in `.claude/`)

- **`CLAUDE.md`** (project root) — orchestrator guide for any Claude Code session. Read on session start.
- **`reference/agents.md`** — canonical detailed agent roster + status.
- **`reference/architecture.md`** — data model (entity types, edge vocabulary, confidence tiers).
- **`working/agent-fleet-specs/mission-protocol.md`** — DRAFT v0 of the mission orchestration pattern. Read before running a mission.
- **`working/agent-fleet-specs/missions/`** — concrete mission files (one per concrete batch of orchestrated work).
- **`working/agent-fleet-specs/agent-pipeline-plan.md`** — full agent roster + dependency plan.
- **`working/agent-fleet-specs/fleet-orchestration-plan.md`** — future-state daemon plan (deferred — see protocol doc).
- **`progress/continue-prompts/`** — resumable work-track contexts. Use `/continue`.

---

## Quick reference: starting a mission

For the first mission (case-collision top-10), see the mission file's "Notes for the operator" section. Generally:

1. **Window 1 (watcher, Opus 4.7):** type `/watcher <substring>` (e.g., `/watcher collision`), copy the kickoff output, paste into a fresh session.
2. **Windows 2-N (workers, Sonnet 4.6):** for each worker slug, type `/worker <substring> <worker-slug>` (e.g., `/worker collision free-folk`), copy the kickoff, paste into a fresh session.
3. **Check in with the watcher periodically** — ask status, surface concerns, get recommendations.
4. **Archive when success criteria met** — manually move mission file + write worklog entry + update todos.
