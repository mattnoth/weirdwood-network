# Advisory board — MCP adapter (design.md §8 fork)

> Board deliberation only. Session-C fan-out per `working/query-layer/design.md` §5/§8.
> Fork: build `graph/query/mcp_server.py` (thin over `weirwood_query`) in step 9, or park it?
> **Tier** = confidence 1–5 only; this is a **Track** fork, step-numbered per `design.md`.

## The fork, restated

The query-layer Track has now shipped a fully consolidated Python engine
(`graph/query/weirwood_query/`: `model`, `load`, `normalize`, `resolve`, `traverse`, `search`,
`themes`(planned), `braid`, `report`, `cli`) with a documented contract (`spec/operations.md`)
and a `weirwood query <subcommand>` CLI front door. The question is whether to also wrap that
package in an MCP server — a fourth-ish access path, alongside direct Python import, the CLI,
and the TS/chat bounded profile.

## Board

### Advisor 1 — the in-repo agent
Every session in this repo already has the cheapest possible path to the graph: `PYTHONPATH`
import of `weirwood_query`, or `weirwood query <subcommand>` via the CLI shim. Both are
zero-network, zero-serialization-boundary, same-process-or-one-subprocess-hop. MCP would add a
server process, a tool-schema layer, and a JSON-RPC round-trip for something Claude Code
sessions already do faster and more flexibly (a subagent can read `traverse.py` source directly
when the contract doc under-specifies something — a raw MCP tool call can't). Fresh Claude Code
sessions in this repo don't currently reach for MCP servers for local Python packages; they Read/
Bash/import. **Verdict: no benefit to the in-repo agent. Neutral-to-negative** (one more thing
that could be stale/misconfigured when a session starts).

### Advisor 2 — the drift-cost accountant
The whole Track exists because 4 accidental surfaces (`graph-query.py`, `event_alias_resolver.py`,
`graph/index/`, `web/src/lib/`) grew independently with no shared contract, and G11/G12 were
named as the root-cause gaps. An MCP server is a **5th adapter**. The spec's golden-case
machinery (`spec/cases/*.json` + `run_cases.py` + `spec_cases_test.ts`) only covers it if a third
runner is added — today the cases run under pytest (full profile) and deno (bounded profile);
an MCP runner would need its own harness wiring (stand up the server, speak MCP over stdio/SSE,
assert against the same JSON fixtures) for parity to mean anything. Every operation added to
`weirwood_query` in future steps (`theme`, `mentions`, the gated `passage`) would need a parity
decision for a 3rd time. This is real, non-trivial maintenance load for a package that's really
just argparse-shaped already. **Verdict: meaningfully raises the Track's steady-state
maintenance surface for a solo maintainer.**

### Advisor 3 — the outside-user advocate
The stated motive is exposing the graph to *other* local Claude/MCP clients (Claude Desktop) or
future agents without repo context. This is real in principle — an MCP server is exactly the
right shape for "let some other tool query this graph without cloning the repo or knowing
Python." But there's no evidence of current demand: this is a solo, private, unpublished-to-
others project (per `project_team_is_solo` / `project_publish_settled` memory — repo is private,
Matt-only). Nothing in the worklog names an actual second consumer waiting on this (no Claude
Desktop workflow described, no external collaborator, no second agent fleet pointed at this
graph from outside the repo). Building it now would be speculative infrastructure for a user
who doesn't exist yet. If Matt starts actually using Claude Desktop against this graph, or a
future non-repo agent needs it, the ask becomes concrete and the server is cheap to build
*then* — the engine underneath (which is the hard part) is already done and stable.
**Verdict: no live demand signal; speculative.**

### Advisor 4 — the maintenance minimalist
Matt is solo. Every adapter is something he alone keeps in parity forever. The Track's own
hard-won lesson (G11/G12, the reason this whole master-design session happened) is: don't mint
a surface without a reason pulling it into existence. Step 9 already has real, load-bearing
work queued (doc-truth sweep G17, `graph/query/README.md` final pass, optional `--explain`,
feeding the "how it works" page) — an MCP server competes with that for the same session's
attention and is the least load-bearing item on the list. Parking it costs nothing: the engine
is already MCP-ready-in-spirit (one Python package, one contract doc, clean function surface) —
building the actual `mcp_server.py` file later, if triggered, is a small, bounded task precisely
*because* this Track did the consolidation work already. **Verdict: park; the consolidation is
the valuable part and it's done regardless.**

## Synthesis

**Decision: PARK-with-condition.**

Rationale (5 lines):
1. No advisor found a real current consumer — not the in-repo agent (already has faster paths),
   not an identified outside user (solo, private project, no named external client today).
2. It would be the Track's 5th (arguably 6th, counting the CLI vs import as one) drift surface,
   and the golden-case parity machinery doesn't cover it without new harness work — real
   ongoing cost, not a one-time build.
3. The hard part (one consolidated engine + documented contract) is already done; that is what
   makes `mcp_server.py` cheap *whenever* it's actually needed — parking loses nothing durable.
4. Step 9 has higher-value, already-load-bearing work (doc-truth sweep, README, "how it works"
   page) competing for the same session budget.
5. Building speculative infrastructure ahead of demand is exactly the failure mode the Track's
   own diagnosis (G11) was created to stop repeating.

**Trigger condition to un-park:** build it the first time one of these becomes true —
(a) Matt actually wants to query this graph from Claude Desktop or another MCP client in a
real session (not hypothetically), or (b) a second agent/fleet outside this repo needs graph
access without importing the Python package or shelling out to the CLI, or (c) the project
stops being solo/private in a way that makes a documented external access path a real ask.
Any one of these is a concrete, cheap trigger — the engine is already in the right shape to
serve it same-session.

**Dissents:** none registered — all four advisors converge on PARK; Advisor 3 flags this as the
one to revisit first if Matt's own tool usage changes (e.g., if he starts running Claude Desktop
sessions against repo-adjacent data day to day), since that's the most plausible real trigger
among the three.

---

## Appendix — session log
- **2026-07-04 (S189, session C fan-out):** board convened per design.md §8; PARK-with-condition
  decided; no dissent. Trigger condition recorded above for whoever revisits this fork.
