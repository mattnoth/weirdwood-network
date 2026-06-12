# Fable Audit — 2026-06-11

First Fable 5 session on this project. Matt asked for a full project audit + graph deep-dive
("what's your take, can the wiki edges be salvaged, enrich or dialog next").
Produced by the orchestrator + two read-only Fable subagents; accepted by Matt same day
(reply: `working/reply-to-audit-session-2026-06-11.md`).

| File | What |
|---|---|
| `synthesis.md` | Orchestrator synthesis: verdicts, recommendation, theories/prophecies gap answer |
| `history-audit.md` | Full 91-session history audit (phases, failures, successes, patterns, spend ledger) |
| `graph-deep-dive.md` | Quantitative graph analysis (edge composition, connectivity, three wiki layers, overlap, verdict) |
| `doc-rot-punch-list.md` | Actionable doc-contradiction punch list (feeds the Step-1 doc fixes + repo-audit track) |
| `design-doc-proposal.md` | (Step 1d) Canonical design-doc structure proposal — Matt picks |

Headline numbers: 8,261 nodes / 4,760 cited edges / 14.7% node connectivity;
infobox layer = 20,614 parsed wiki relationship rows, 98.4% additive, merge moves connectivity to ~72%.
Decision: infobox merge greenlit (Tier 2, `evidence_kind: wiki-infobox`); prose-comention stays deprecated;
Mode 3 dip runs AFTER the merge lands.
