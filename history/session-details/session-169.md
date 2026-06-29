# Session 169 — Chat-UI alpha design review (no build)

**Date:** 2026-06-29 · **Track:** meta · **Model:** Opus 4.8 orchestrator + a 6-lens adversarial-review Workflow (~55 Sonnet/Opus agents) + 1 Sonnet 4.6 doc-editing sub-agent.

## What happened

S168 scoped a deployable Bloodraven chat-UI alpha for Matt's job portfolio and its handoff said *build it*. Matt redirected this session: **review the plan first** — rate it, critique it, propose a build order — then fold the findings into the design doc. No app code was written; no graph writes.

## Method

Ran a multi-lens adversarial review (Workflow tool) over `working/chat-ui/alpha-design.md`, grounded in verified repo facts (node/edge/chapter sizes, `graph-query.py --json`, the false-gitignore check) and the `claude-api` skill (model IDs/pricing, adaptive thinking, tool runner, prompt caching, Netlify runtime limits). Six lenses — runtime, cost, security, UX/persona, build-order, doc-quality — each produced findings; **every finding was then verified by an independent skeptic** that tried to refute it and rated materiality. Then a single Sonnet 4.6 sub-agent applied the surviving findings to the doc; the two highest-stakes edits were spot-checked by the orchestrator.

## Per-lens ratings

| Lens | Rating | One-line |
|---|---|---|
| Runtime & architecture | 6 | "grep not RAG" is right; runtime feasibility is the gate and is sequenced last |
| Cost & model economics | 5 | right instincts (key custody, Sonnet default, adaptive); token model + caching + real spend ceiling missing |
| Security / abuse / copyright | 5 | key-server-side correct; stateless rate-cap broken; **the gitignore premise is factually false** |
| Product / UX / persona | 7 | typed-edge receipts are a strong differentiator; silent agentic turn + unhappy paths unspecified |
| Build order & scope | 6 | good scope cuts; inverts the risk gradient (validates the unknowns last); no named MVP slice |
| Doc quality (meta) | 6 | strong think, not build-ready; missing §0 table, persona eval, failure modes |

Consensus: **a strong discussion artifact (~7.5/10), not yet a buildable spec (~5.5/10).** The big architectural call — live quote-finding is a grep tool, not a RAG pipeline — is correct, and the scope discipline (defer embeddings/vector store/auth) is right.

## Findings that held (folded into the doc)

- **The one factual error:** §2/§7 claimed the book text is gitignored. It is NOT — `.gitignore` has only `sources/raw/`; all 347 chapter files are git-tracked; the repo is currently private. The "bundled into the private deploy" story rested on a false premise. → §7 now an explicit deploy-boundary OPEN DECISION (private repo vs. text-out-of-public-artifact), gated before any public fold-in.
- **Runtime is the gate, sequenced last** → new §8 step-0 spike: prove streaming holds a loop-length turn within the timeout (Edge/Deno vs sync), and persona-over-API on both models, before building. Corrected two errors: Background Functions can't stream; no `python3` on Netlify (do the Python at build time via `--json` export, port the small live-query subset — don't shell out).
- **Typed-edge receipts won't fall out of the trace for free** → tools must return structured typed-edge JSON on a separate channel; spec the no-chain (neighbor-query) fallback.
- **Cost/abuse:** add prompt caching; the per-IP in-function cap can't hold (stateless) → global daily spend ceiling in durable state + per-request bounds; pre-render the Tywin landing static; `effort: medium`.
- **Security:** move loop-bounding + input-validation from "Open" to spec (tool layer = trust boundary; clamp `read_passage` spans; output quotation norm).
- **UX:** stream the tool-gathering trace as the "watch it dig" wow; spec the not-mapped / error / cost-cap / mobile states; one out-of-character framing line above the fold so the never-announces persona doesn't read as broken.
- **Doc artifacts:** added §0 status table; flagged the missing persona+faithfulness eval, failure-modes, conversation/session state, and the §8b-vs-§9 telemetry contradiction in §9.

## Checked and dismissed (don't re-raise)

The adversarial pass refuted several plausible findings: cold-start latency (data parse is sub-second vs. the model round-trips), the persona-vs-demo-voice "mismatch" (the doc already routes the explaining job to page chrome + About), the `graph/edges/` directory bundling "trap" and §8b "scope creep" (invented failure modes — the doc names `edges.jsonl` and defers §8b), and shell-injection (argv arrays are safe). One overreach: a reviewer pushed "drop live search from v1" — rejected, since live search is Matt's stated #1 priority; it stays the v1 goal, just sequenced after the spike.

## Next

Build is still pending — a fresh session picks it up from the now-sharpened design doc, starting with the §8 step-0 spike and resolving §9 with Matt. Continue prompt: `progress/continue-prompts/2026-06-29-chat-ui-alpha.md`.
