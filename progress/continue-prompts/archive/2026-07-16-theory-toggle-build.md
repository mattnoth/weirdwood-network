# SESSION 220 — Theory-toggle build: the S218 chat-exposure plan of record (web/ only, parallel-safe)

> **Session number:** graph/meta sessions number by write-order at endsession — S220 is the guess assuming the wave-2 mega window (S219) writes first. **CHECK at endsession:** grep `^### Session` in `worklog.md` and take the next free number.
> **Recommended model: Opus 4.8** (focused code task: edge-function + front-end + tests; no Fable-grade orchestration needed). Haiku for any verify subagents.
> **PARALLEL-SAFE:** this session touches `web/` only — NO graph mutation, no `graph/` writes, no `weirwood refresh`. The wave-2 mega window owns the graph. Stage-by-path at commit; don't endsession while another window is mid-endsession.

## What this is

Matt's S218 exposure design (worklog Active Decision "FIRST THEORY MINT + …", architecture.md § Evidentiary closing bullet): a **theory on/off toggle** in the chat UI. The theory layer is minted (118 SUPPORTS/CONTRADICTS edges + 15 `concept.theory` nodes live in the graph); today the chat is protected only by the prompt-level SHARED_RULES no-theories guardrail (`web/netlify/edge-functions/lib/agent.ts` ~line 127). This build makes OFF a hard guarantee and ON a labeled-speculation mode.

## The build (three pieces, all with codebase precedent)

1. **Runtime tool-layer filter (OFF mode — the hard guarantee):** when the toggle is off, every chat tool result (neighbors / search / list / theme / path / walkChain / node dossier-fetch) strips `concept.theory` nodes and `SUPPORTS`/`CONTRADICTS` edges before the model sees them. Filter at the tool-dispatch layer in the edge function (single choke point), not per-tool. CAUTION: the 4 legacy interpersonal SUPPORTS edges (luwin↔osha, renly→jon-arryn, haldon→ysilla) may be retyped by the parallel wave-2 window — filter by edge type regardless; if they're still SUPPORTS they're tier-1 factual, acceptable collateral to hide in OFF mode (note it).
2. **ON-mode prompt contract:** conditional SHARED_RULES block (same mechanism as the existing persona switch): replace the no-theories block with — theories visible as `concept.theory` nodes + SUPPORTS/CONTRADICTS evidence; discuss ONLY as theories; always name + attribute ("the R+L=J theory holds that…"); never state a claim as narration/fact; distinguish what the text establishes (quoted evidence) from what the theory infers; mention `status` when relevant (open / show-confirmed-but-not-books / jossed); cite the per-edge quotes. The node `claim:` field is the ready-made summary; tiers grade confidence in-answer.
3. **UI switch:** same pattern as the parked Bloodraven voice toggle (`web/public/index.html` + `app.js` — the hidden-toggle precedent from S213). Label carries the spoiler note: "Include fan theories — may reference show outcomes". Toggle state rides the request → edge function (like the persona param). Default OFF, persisted in localStorage with the thread.

## Verification (no API spend needed until the end)

- deno tests for the filter (fixture with a theory node + SUPPORTS edge → OFF strips, ON passes) alongside the existing suites (`cd web && deno task test`, currently 102 green; `deno task check` clean).
- Stubbed-loop agent tests for the prompt swap (the S173 pattern in `agent_test.ts`).
- Local live check ONLY if Matt okays the spend (`netlify dev`); otherwise dry-validate.
- **NO deploy** — deploys are manual + Matt-gated (`DEPLOY.md`; no git-CD). Note for his deploy decision: once this ships, the next deploy also ships theory dossiers with the OFF-mode hard filter in place — strictly safer than deploying without it.

## Read first

- `reference/architecture.md` § Evidentiary (Theory Support) — the ratified conventions + the toggle plan bullet.
- `web/netlify/edge-functions/lib/agent.ts` (SHARED_RULES + persona-switch mechanism + tool dispatch) and `web/netlify/edge-functions/chat.ts` (request params).
- `web/public/app.js` + `index.html` (the hidden voice-toggle precedent).
- worklog.md S218 entry + the S218 Active Decision.

## DO NOT

- Do NOT write anything under `graph/` or run `weirwood refresh` (the parallel wave-2 window owns graph state).
- Do NOT deploy, and do NOT spend API without asking (local `netlify dev` proof costs real calls).
- Do NOT remove or weaken the OFF-default; do NOT expose theories in any mode without the attribution contract.
- Do NOT touch the Bloodraven persona park state.
- Do NOT run /endsession without permission.
