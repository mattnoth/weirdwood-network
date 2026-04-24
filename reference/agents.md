# Agent Inventory

All agent definitions live in `.claude/agents/`. The orchestrator (main Claude Code session) delegates to these — they execute, they don't coordinate.

## Pipeline Agents

| Agent | File | Status | Pass | Purpose |
|-------|------|--------|------|---------|
| **mechanical-extractor** | `mechanical-extractor.md` | Full prompt (v2) | Pass 1 | Reads a chapter file, produces a structured extraction with characters, locations, artifacts, events, relationships, food, hospitality, physical descriptions, spatial layout. One extraction per chapter. |
| **wiki-ingester** | `wiki-ingester.md` | Stub | Pass 2 | Will ingest AWOIAF wiki pages into structured entity node files. Wiki data already scraped (17,945 pages in `sources/wiki/`). |
| **voice-analyzer** | `voice-analyzer.md` | Stub | Pass 3 | Will build POV character voice profiles and cross-POV perception mappings (how different characters see the same person/event). |
| **foreshadowing-scanner** | `foreshadowing-scanner.md` | Stub | Pass 4 | Will scan extractions for foreshadowing of known events listed in `reference/foreshadowing-events.md`. |
| **theory-extractor** | `theory-extractor.md` | Stub | Pass 5 | Will extract textual evidence for/against known theories. Needs `reference/theory-seeds.md` (not yet created). |
| **discovery-agent** | `discovery-agent.md` | Stub | Pass 6 | Open-ended pattern discovery across the full extraction corpus. Runs after all other passes. |

## Utility Agents

| Agent | File | Status | Purpose |
|-------|------|--------|---------|
| **script-builder** | `script-builder.md` | Full prompt | Writes and tests Python scripts — chapter splitters, wiki ingesters, indexing tools, any automation. |
| **status-reporter** | `status-reporter.md` | Full prompt | Surveys the repo filesystem, counts artifacts, checks pipeline progress, and produces a detailed status report. Read-only — doesn't modify anything. |

## Agent Status Key

- **Full prompt** — Complete, tested, ready to run
- **Stub** — File exists with a description and placeholder structure, but the prompt hasn't been written yet. Needs design work before it can run.

## How Agents Run

Pipeline agents (Pass 1-6) are invoked by shell scripts in `scripts/` or directly by the orchestrator. Each invocation is a fresh Claude session with no shared context — the agent reads the project files it needs from disk.

The mechanical extractor runs in waves of 5 chapters, with multiple waves running in parallel across terminal tabs. See `working/runbooks/mechanical-extraction-howto.md` for the operational procedure.
