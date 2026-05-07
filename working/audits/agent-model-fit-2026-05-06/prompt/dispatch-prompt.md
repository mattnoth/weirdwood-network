# Agent model-fit audit dispatch prompt

**Date:** 2026-05-06
**Sub-agent type:** `general-purpose`
**Trigger:** Resource-conservation pass per `working/todos.md` "Model-fit Policy (standing rule, 2026-05-04)" and the READY-TO-DO item ("Audit existing agent prompts for model-fit drift"). Goal: identify where Opus is being used by default rather than necessity, and recommend the cheapest viable model for each agent.

**Connection to fleet plan:** Per Q8 of the 2026-05-06 handoff, the model-fit audit is **input** to a separate fleet-plan review (`working/fleet-orchestration-plan.md` + `working/fleet-runtime-architecture.md`). The audit report should be written so the fleet-plan review session can ingest it directly.

**Dispatched prompt:**

```
Audit /Users/mnoth/source/asoiaf-chat/.claude/agents/*.md. For each agent
prompt, recommend the cheapest viable model (Opus 4.7 / Sonnet 4.6 /
Haiku 4.5) for what the prompt actually does. Apply the model-fit policy:
cheapest model that can do the job; Opus only when reasoning depth
genuinely requires it; smoke-test before upgrading.

Output a markdown table to:
  /Users/mnoth/source/asoiaf-chat/working/audits/agent-model-fit-2026-05-06/execution/agent-model-fit-report.md

Columns:
| agent name | current model assumption | recommended model | one-sentence rationale | suggested smoke test |

Plus a short closing section "Connection to fleet plan" that calls out which
agents in fleet-orchestration-plan.md / fleet-runtime-architecture.md are
affected by these recommendations, so the fleet-plan review session can
ingest this report directly.

Do NOT modify any agent prompts. This is a recommendation-only pass; Matt
reviews before any frontmatter changes.
```

**Why this folder layout:** Q10 of the 2026-05-06 handoff established the per-audit folder convention. `prompt/` keeps the dispatch record alongside `execution/` (the report itself), `validation/` (independent re-checks), and `prompt-planning/` (any pre-audit notes).
