# SESSION 189 — Graph-query docs coagulation + traversal-script organization plan
> **This is Session 189.** Stamp your worklog entry `### Session 189` at endsession.

**Track:** meta/graph (documentation + organization only). **Recommended model:** Sonnet 4.6
(reading, editing docs, planning — no heavy reasoning, no code build).

**HARD SCOPE (Matt, S188 endsession):** deliverables this session are **ONLY** documentation,
organization, or refinement of the two markdown files. **No graph mutation. No feature build.
No code changes to `web/` or `scripts/`.** If you find yourself about to write/run code that
changes the graph or the app, STOP — that's a future session.

---

## Context (what S188 produced)

S188 was a design/analysis session on the chat-UI's **retrieval/query surface**. It produced
two new top-level living docs:
- **`GRAPH-QUERY-ROADMAP.md`** — forward-looking traversal/query design (gaps G1–G10,
  directions D1–D8, the "two apertures / essential-vs-incidental shrink" framing, live-evidence
  exhibit, script-org/interview framing §4, prior-art §8).
- **`GRAPH-STATE.md`** — current-state snapshot (census §1, enrichment story §2, the
  descriptive-layer census §2a [food 96% islanded], the harvest-mechanism root cause §2b,
  parked tracks §4, backlog salvage §4b).

Read `history/session-details/session-188.md` for the full narrative and all 7 findings.

## Step 1 — Evaluate, coagulate, organize the two docs (PRIMARY)

Read both docs end to end with fresh eyes and tighten them into a clean, non-redundant pair:
- **Check for drift/duplication** between the two (some overlap is intentional per Matt, but
  kill accidental repetition; make the split crisp — roadmap = forward, state = snapshot).
- **Verify every grounded claim** still holds (counts, the census numbers, the query-mode
  divergence table). Spot-check a couple against the repo; flag anything stale.
- **Improve structure/legibility** — these are portfolio-adjacent; they should read cleanly to
  a hiring engineer. Consider whether G1–G10 / D1–D8 want a short priority ranking or a
  one-glance summary table at the top.
- **`working/todos.md` cleanup:** fold the query-layer findings into **Track 7 — Query-Layer
  Tooling** (it already exists, S96). Add the un-done items surfaced in GRAPH-STATE §4b as
  proper todo entries where they belong (content-search D1, braid/convergence D7, trigger table
  D8, the descriptive-wiring step, TWOIAF ingestion, prophecy layer). Remove/merge anything
  now-superseded. Make sure nothing "coagulated" in the docs is lost from the actionable list.

## Step 2 — Plan the traversal-script organization (PLAN ONLY, do not build)

Matt's interview framing: the graph should ship *with* its query interface as a first-class,
co-located, documented layer — not scratch scripts in `working/`, and unified with the chat-UI's
TS re-implementation. Currently: `scripts/graph-query.py` (~11 modes) + `scripts/
event_alias_resolver.py` live next to one-off cleanup scripts; `web/src/lib/*` is a separate
partial port (~5 modes). See roadmap §4 + the query-mode divergence table in §1d.

Produce a **plan** (write it into the roadmap §4 or a short sibling planning note, your call):
- Where the traversal layer should live (candidates: `graph/query/`, top-level `query/`, a
  packaged Python module) and why.
- How to unify the two implementations conceptually (one documented query API; Python CLI +
  chat-UI tools as thin adapters) and what the concrete first move is.
- Which of the un-ported modes (`--container`/`--path`/`--expand-beats`/`--event-participants`)
  are cheap wins to expose in the chat, and what integrating them into the chat-UI would take.
- Keep it a PLAN with a recommended sequence — do not implement.

## At endsession
- Update `GRAPH-QUERY-ROADMAP.md` + `GRAPH-STATE.md` appendix logs with what changed.
- Worklog entry `### Session 189` (worklog.md, meta/graph track).
- Update `working/todos.md` per Step 1.
- Commit docs + todos only.

## DO NOT
- Mutate the graph (`graph/`), rebuild the bundle, or change `web/`/`scripts/` code.
- Build the content-search tool or any feature — that's a later session (this is docs/plan only).
- Run `/endsession` without Matt's explicit permission.
- Touch the top-level `scratch`/`scr` file.
