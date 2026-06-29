# Session 171 — Chat-UI alpha BUILD: the step-0 spike + the Foundation chunk

**Date:** 2026-06-29 · **Track:** meta · **Model:** Opus 4.8 orchestrator (persona smoke-test on `claude -p` Sonnet 4.6 + Opus 4.8, subscription quota).

## What this session was

The fresh BUILD session the S170 handoff called for. Per the design's §8 step-0 gate,
the job was: (a) run the runtime + persona spike to resolve the two gating §9 opens,
(b) confirm the architecture with Matt, (c) start building. Matt confirmed the four
queued decisions (Option A / MVP-then-live / smoke-test-then-pick / run-the-spike), then
made a good process call — the full MVP slice is A-to-Z and would blow one context window,
so we split the build into chunks. This session did the spike + the **Foundation chunk** only.

## The step-0 spike

### 0a — Runtime (the gate)
Could not deploy to Netlify (Matt's account), so resolved the runtime decision from the
authoritative Netlify docs rather than a live deploy. The decisive fact:

> Netlify **Edge Functions** (Deno): the **50 ms limit is CPU time only** and explicitly
> **excludes "time spent waiting for resources or responses,"** with a **40 s response-header
> timeout.**

An agentic tool-loop is almost entirely *waiting* (on the Claude API + tool I/O); its own
CPU work is graph map-lookups + string assembly (microseconds). So it fits an Edge Function
with enormous margin. A Node Function's 10 s (free) / 26 s (paid) is **total wall-clock**
including API waits — a 20–40 s multi-tool turn would time out. Background Functions can run
15 min but **cannot stream to the browser** (struck). **Decision: Edge Functions (Deno/TS).**

Caveat carried forward: the live `search_chapters` tool must NOT raw-scan ~4 MB of chapter
text per call (would blow the 50 ms CPU budget) — it needs a **build-time inverted index**.
The curated-MVP slice has no such concern (graph map lookups only).

### 0b — Model (persona smoke-test)
Ran the real Bloodraven persona prompt (base + grounding + question) through `claude -p`
on both models, 3 calibration questions, on Matt's subscription (no API $). Judged against
`bloodraven-persona-notes.md`:

- **Q1 "Who killed Tywin?"** — Opus kept Oberyn in the chain, one clean image ("the old lion"),
  and appended the `asos-tyrion-11:269` cite; Sonnet compressed the chain, dropped Oberyn, no cite.
- **Q2 "Did Jon learn Robb died?"** (gap-restraint) — Opus: *"A direwolf beside him, and
  otherwise no one. The grief is given. The giving of the news is not."* — almost verbatim the
  golden calibration line. (One slip: it blockquoted a grounding *note* as a book line — a prompt-
  hygiene issue, fixed by separating quotable-lines from context + the cite-verification gate.)
  Sonnet good too: *"grief, not its delivery."*
- **Q3 "Tell me about yourself"** (never-announce / tidbit-don't-volunteer) — Opus executed the
  rule textbook: never named himself, dropped ONE tidbit (*"I knew Aegon when he was a fourth son…"*)
  then stopped. Sonnet deflected correctly but cold — gave the visitor nothing to pull on.

**Decision: `claude-opus-4-8`** as the default, built **swappable via one config constant**
(Sonnet 4.6 is the cheaper fallback). Matt's note: the original demo (S160) ran richer still —
that's a **grounding** gap (the smoke-test fed a compressed paragraph; the demo walked the real
graph). The function chunk's prompt will hand the model full beat-level grounding to close it.

## The Foundation chunk (built)

`scripts/build-chat-export.py` — reads `graph/` + the prebuilt alias index, writes an
allowlisted static JSON bundle to `web/data/` (gitignored, regenerated). NO LLM, NO network.
Outputs measured:

| File | Size | Contents |
|---|---|---|
| `nodes.json` | 3.8 MB | 8,475 nodes (name/type/identity/quotes); 1,595 with quotes, 6,059 quotes total |
| `edges.json` | 4.1 MB | 23,330 edges (slim: type/source/target/quote/ref/tier/relation) |
| `alias-map.json` | 863 KB | 12,029 phrases → [{slug, category}] |
| `featured-tywin.json` | 11.5 KB | pre-rendered landing exchange |
| **TOTAL** | **8.8 MB** | — |

**Key finding:** 8.8 MB means the **whole curated graph fits in the Edge Function's cold-start
memory** — no lazy-loading, no pre-filtering to a reachable subset. The function can answer any
query, not just pre-baked ones. This simplifies the function chunk considerably.

**Featured Tywin chain verified** = the full 7-link arc, every link cited:
`Sansa receives the poisoned hair net —[CAUSES]→ Death of Joffrey —[TRIGGERS]→ Tyrion accused
—[CAUSES]→ Trial of Tyrion —[TRIGGERS]→ Gregor confesses and kills Oberyn —[CAUSES]→ Jaime frees
Tyrion —[CAUSES]→ Jaime reveals the truth of Tysha —[CAUSES]→ Assassination of Tywin`, 8 beats
with 2–5 quotes each, closing on *"Lord Tywin Lannister did not, in the end, shit gold."*
(`asos-tyrion-11:269`). Walked at build time via `graph-query.py --causal-chain … --json` so it
stays correct without a live call.

Scaffold: `web/public/theme/tokens.css` (the single-file theme layer — dark / soft / dusty-red
per Matt's S168 brief), `web/public/index.html` (palette-placeholder landing), `netlify.toml`
(Edge runtime + a build command that regenerates the bundle on deploy), contract READMEs in
`web/`, `web/src/lib/`, `web/netlify/edge-functions/`. `.gitignore` += `web/data/`, `node_modules/`,
`.netlify/`.

## The build plan (4 chunks, multi-session)

1. **Foundation** ✅ (this session) — export script + scaffold + theme + verified bundle.
2. **Retrieval-core** (next, Sonnet 4.6, no API) — port resolve/walkChain/neighbors/readNode to
   Deno TS, unit-test vs the bundle.
3. **Function** (Opus) — `chat.ts`: Claude tool-loop + Bloodraven prompt (full grounding) +
   streaming + global daily spend cap. Local `netlify dev` answers "who killed Tywin?".
4. **Front-end + ship** — chat thread, static Tywin exchange, typed-edge receipts panel →
   **local run Matt drives** → Netlify deploy.

"Local run" = `netlify dev` serves the function + page on Matt's machine (on subscription auth,
no API $) so he can chat with it + click the receipts against the real graph, before anything
goes public.

## Decisions (locked — design §0 + §9, do not reopen)
- Runtime = Netlify Edge Functions (Deno/TS) — the CPU-excludes-API-wait fact.
- Model = `claude-opus-4-8`, swappable via one config constant.
- Retrieval = Option A (tool-use agent). Scope = curated-MVP first, live search fast-follow.
- Bundle = 8.8 MB, loads in memory.

## Not done (deliberately, deferred to later chunks)
- The retrieval tools, the Edge function, the chat page, the receipts panel, live `search_chapters`/
  `read_passage` + the telemetry feed. All carried in `web/`'s contract READMEs + the continue prompt.
