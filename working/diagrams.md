# Diagrams — Weirwood Network Architecture at a Glance

**Purpose:** Small, focused, scan-in-30-seconds diagrams for each major architectural concept. Companion to the full design docs which carry the dense reference DAGs. When a human is trying to understand "how does X work?", they read this first; the deep docs are second.

**Convention:** each diagram fits on a screen (≤20 lines), captures one idea, and links to the deep doc that has the full version.

---

## 1. The whole project at a glance

```
SOURCE                 CONSTRUCTION                RETRIEVAL                 USE
                                                                              
Books +    ──►    Python pipelines + ──►    Embeddings +     ──►   Chat UI
wiki cache        agent fleet                graph traversal         (D&D group)
                                                                              
   ↓                    ↓                          ↓                    ↓
sources/           graph/nodes/                 vector store         hosted web UI
                   working/wiki-pass2/                                behind auth
```

**See:** `CLAUDE.md`, `working/agent-pipeline-plan.md`, `working/chat-ui-architecture.md`

---

## 2. Three corpora, one join key

```
                ┌──────────────┐
                │   Question   │
                └──────┬───────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    ┌───────┐      ┌────────┐    ┌──────────┐
    │ GRAPH │      │  WIKI  │    │   BOOK   │
    │ NODES │      │ PROSE  │    │ CHAPTERS │
    │+edges │      │ chunks │    │  chunks  │
    └───┬───┘      └────┬───┘    └─────┬────┘
        │               │              │
        └──────────────►◄──────────────┘
                  JOIN ON SLUG
                       │
                       ▼
                  Answer + cites
```

The slug is the universal join key. Every chunk and every node carries the slugs it relates to.

**See:** `working/chat-ui-architecture.md` § "Three corpora, one join"

---

## 3. Single-writer-per-file (the core invariant)

```
   Python emits         Python emits         Promoter emits
       ↓                    ↓                     ↓
  skeleton/foo.md  +   prose/foo.md   ──►   graph/nodes/foo.node.md
  (frontmatter +       (Origins,             (skeleton + "\n" + prose)
   ## Edges)           ## Narrative Arc,
                       ## Quotes, ...)

   ONE writer            ONE writer           ONE writer
```

No agent ever paraphrases the skeleton bytes. No two processes write the same file. Composition happens at the promoter, not at the source.

**See:** `working/design-philosophy.md`

---

## 4. Construction fleet vs UI build fleet

```
   CONSTRUCTION FLEET              UI BUILD FLEET
   (build the data)                (build the product)
                                   
   ┌──────────────────┐           ┌──────────────────┐
   │ Bounded scope    │           │ Continuous scope │
   │ Days-long batches│           │ Minutes/hours    │
   │ tmux: fleet-cnstr│           │ tmux: fleet-ui   │
   └────────┬─────────┘           └────────┬─────────┘
            ▼                              ▼
       graph/nodes/                hosted chat UI
       working/wiki-pass2/         (Vercel + Render)
       extractions/
```

Two fleets, two orchestrators, one monitoring skill (`/check-fleet` is multi-orchestrator-aware).

**See:** `working/agent-pipeline-plan.md`, `working/chat-ui-architecture.md`

---

## 5. Daemon process layers (no Claude Code session limits!)

```
   LAYER 1 (Python daemon, runs for days)
   fleet-orchestrator.py
        │
        │  subprocess.run(["claude", "--print",
        │                  "--agent", "prose-edge-classifier", ...])
        ▼
   LAYER 2 (ephemeral headless Claude CLI per agent invocation)
   each invocation = bounded fresh session, dies on completion
        │
        ▼ (output written to disk)
   LAYER 3 (Matt's interactive Claude Code, fresh each time)
   /check-fleet → reads state files → renders status
```

Layer 1 isn't a Claude session — it's Python. Layer 2 sessions are short. Layer 3 is on-demand. **No session limits.**

**See:** `working/fleet-runtime-architecture.md` § "Process model"

---

## 6. The Unix philosophy in one diagram

```
    BAD (mega-agent)                 GOOD (focused agents + pipes)
                                     
   ┌───────────────┐                ┌─────┐    ┌─────┐    ┌─────┐
   │ wiki-ingester │                │  A  │ ──►│  B  │ ──►│  C  │
   │ does 5 things │                └─────┘    └─────┘    └─────┘
   └───────────────┘                  ↓          ↓          ↓
   ↓                                 file      file       file
   "what failed?"                    (any tool can read these)
   "the wiki-ingester somewhere"
                                     "what failed?"
                                     "B — see file output"
```

One agent per task. JSONL/markdown between them. The pipe IS the API.

**See:** `working/design-philosophy.md`

---

## 7. Self-review pattern (orchestrator-driven, not recursive)

```
   ❌ DISALLOWED                   ✅ ALLOWED
                                  
   Orch ──► Agent A                Orch ──► Agent A ──► writes JSONL
                │                  Orch ──► Reviewer ──► reads JSONL
                ▼                          (separately invoked)
              Agent B
              (recursive)
              
   "convergence bias buried        "composition through pipes;
    in nested context"              same Unix pattern as everything else"
```

Agents never invoke other agents. The orchestrator dispatches both classifier and reviewer; they communicate via files.

**See:** `working/fleet-orchestration-plan.md` § "Self-review pattern"

---

## 8. Per-stage independence (the escape hatch)

```
   Daemon mode:           OR        Manual mode:
                                    
   weirwood fleet start              weirwood stage stage-1
        │                                  │
        ▼                                  ▼
   chains stage-0 → 1 → 2 → ...       runs ONE stage to completion
   auto-pauses at boundaries          you stop. you choose what's next.
        │                                  │
        ▼                                  ▼
   same artifacts on disk             same artifacts on disk
```

Every stage is independently runnable. Daemon is a convenience, not a requirement.

**See:** `working/fleet-runtime-architecture.md` § "Stages are independently liftable"

---

## 9. Spoiler gate (v1 OPEN, v2 ADDITIVE)

```
   v1 (today)                          v2 (post-release backfill)
                                       
   Question ──► retrieve ──► answer    Question ──► retrieve ──► gate ──► answer
                                                                  │
                  no gate                                      first_available
                                                               <= user.read_progress
   "every chunk fair game"             "additive filter; doesn't change corpus"
```

Don't accidentally re-introduce gating in v1. It's an explicit simplification.

**See:** `working/chat-ui-architecture.md` § "Spoiler gating"

---

## 10. Multi-day orchestration with monitoring (the daily Matt cycle)

```
   DAY 1                               DAY 2-5                            DAY 6
                                       
   ┌──────────────┐                   ┌──────────────┐                   ┌─────────┐
   │ matt starts  │                   │ daemon runs  │                   │ matt    │
   │ daemon       │                   │ unattended   │                   │ wraps   │
   │              │                   │              │                   │ up      │
   │ smoke tests  │                   │ matt opens   │                   │         │
   │ pass         │                   │ Claude any-  │                   │ daemon  │
   │              │                   │ time, runs   │                   │ has     │
   │ tmux session │                   │ /check-fleet │                   │ written │
   │ detached     │                   │ and goes     │                   │ all     │
   │              │                   │              │                   │ output  │
   │ matt walks   │                   │ answers any  │                   │ to disk │
   │ away         │                   │ questions    │                   │         │
   └──────────────┘                   └──────────────┘                   └─────────┘
```

Matt isn't tied to a session. Daemon survives. Skill is on-demand. State persists.

**See:** `working/fleet-runtime-architecture.md`

---

## 11. Stage shape (every stage looks like this)

```
   INPUTS                    PROCESS                    OUTPUTS
                                                         
   working/<dir>/   ──►    Python prep    ──►    working/<bucket>/skeleton/
   sources/<...>           ↓
                          Agent invocations  ──►   working/<bucket>/<artifact-dir>/
                          (bucket-parallel)
                          ↓
                          Python promote    ──►   graph/nodes/<type>/<slug>.node.md
                                                  
                                                  +stats CSV row
                                                  +audit report (if reviewer)
```

Same shape every stage. Different agents, different inputs, same orchestration template.

**See:** `working/fleet-orchestration-plan.md` § "Stages in detail"

---

## 12. Friend-group deployment (chat UI v1)

```
   ┌──────────────┐
   │   Frontend   │  (Vercel — Next.js / Streamlit / similar)
   │  + auth gate │  shared password OR magic-link
   └──────┬───────┘
          │ HTTPS
          ▼
   ┌──────────────┐
   │   Backend    │  (Render / Fly.io / Railway — Python FastAPI)
   │              │  Anthropic API key (server-side)
   │              │  Vector store (sqlite-vec file, bundled)
   │              │  Graph nodes (read from disk, bundled)
   └──────┬───────┘
          │ Anthropic API
          ▼
       Claude Sonnet/Opus → cited answer
       (synthesis-not-quotation
        prompt rule)
```

Cost ~$10-50/month for D&D-group scale.

**See:** `working/chat-ui-architecture.md` § "Deployment"

---

## 13. Citation chain (every fact traces back)

```
   Answer in chat UI
        │
        │  "Eddard's wife was Catelyn¹"
        │
        ▼  ¹ click expands to:
   ┌─────────────────────────────────┐
   │  cite: agot-eddard-01           │
   │  source: chapter file           │
   │  excerpt: "...his lady wife..." │
   └─────────────────────────────────┘
   
   OR
   
   cite: wiki:Eddard_Stark.cite_ref-Ragot1
   cite: track_b: Spouse
   cite: node:eddard-stark
```

Every claim → cite → resolvable file. Citation-validator agent enforces this property.

**See:** `reference/architecture.md` § "Citation Format"

---

## 14. The session-limit problem (and how we sidestep it)

```
   ❌ DOESN'T WORK                    ✅ WORKS
   
   Long-running orchestration         Long-running orchestration
   inside ONE Claude Code session     as a Python daemon (no Claude session)
                                      
   ↓ 100 stages, 50 agents each       ↓ 100 stages, 50 agents each
                                      
   context exhausted by agent #500    each agent invocation is bounded:
   session limit hit                    claude --print --agent foo
   matt locked out                    daemon process never IN a session
```

The orchestrator daemon isn't a Claude session. Each agent invocation is a separate bounded session that dies on completion. Multi-day runs are possible.

**See:** `working/fleet-runtime-architecture.md` § "Process model"

---

## 15. Where to find more detail

| Concept | Quick diagram (this file) | Deep doc |
|---------|--------------------------|----------|
| Project flow | #1 | `CLAUDE.md` |
| Three corpora + slug join | #2 | `working/chat-ui-architecture.md` |
| Single-writer invariant | #3 | `working/design-philosophy.md` |
| Construction vs UI fleets | #4 | `working/agent-pipeline-plan.md` |
| Daemon process layers | #5 | `working/fleet-runtime-architecture.md` |
| Unix philosophy | #6 | `working/design-philosophy.md` |
| Self-review pattern | #7 | `working/fleet-orchestration-plan.md` |
| Per-stage independence | #8 | `working/fleet-runtime-architecture.md` |
| Spoiler gate v1/v2 | #9 | `working/chat-ui-architecture.md` |
| Multi-day Matt cycle | #10 | `working/fleet-runtime-architecture.md` |
| Stage shape (generic) | #11 | `working/fleet-orchestration-plan.md` |
| Friend-group deployment | #12 | `working/chat-ui-architecture.md` |
| Citation chain | #13 | `reference/architecture.md` |
| Session-limit sidestep | #14 | `working/fleet-runtime-architecture.md` |

---

## When to update this file

- A new architectural concept emerges (rare; most additions are refinements)
- An existing concept gets misunderstood often (means the diagram is wrong; revise)
- A deep doc has been rewritten and the diagram-pointer here needs updating

**Don't add diagrams for every implementation detail.** This file is for concepts that need quick mental modeling, not for every script's flowchart.
