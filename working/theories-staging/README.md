# Theories staging — deferred track

> **STATUS: DEFERRED / GATED. Do NOT start this unprompted.**
> **TRIGGER: Matt says "let's start theories" (or equivalent) in a session.** Until then, this folder is
> a parking lot — orchestrators read this README, note it exists, and move on. It is NOT the active track.

## What this is

The staging ground for the **theory layer** of the Weirwood Network — the HIGH backlog item
"Create theory seeds file (top 20-30 theories with confidence tiers)" (`worklog.md` Ideas & Backlog).
The graph already has a `theories/` node dir (~45 `concept.theory` nodes) but it is **almost edge-less** —
the infobox merge contributed nothing there, and no pass has connected theories to their evidence.
This track fills that gap: seed the canonical theories, then wire each to its supporting/contradicting
evidence via `SUPPORTS` / `CONTRADICTS` / `CITED_BY` edges (architecture.md "Evidentiary" section).

## Why it's deferred (the gating rationale — Matt, S110 2026-06-20)

Theories are **edge-heavy, not node-heavy**: a theory's value is the web of evidence it connects across
many *existing* nodes (characters, events, quotes, prophecies). That evidence layer must be dense first.
So this waits until **after a lot more dip work + the narrative-arc/causal layer** has populated the beats,
quotes, and connections a theory would cite. Starting it early would mean wiring theories to a sparse graph.

## When triggered — the work, roughly (re-scope at start; this is a sketch, not a spec)

1. **Build the theory-seeds file** — top 20-30 community/textual theories, each with: a one-line claim,
   a confidence framing (Tier 5 crackpot → Tier 1 near-canon; most theories are Tier 3-5), the strongest
   single piece of evidence_for, the strongest evidence_against, and the originating theorist/community
   (`CITED_BY`). This is the prerequisite for **Pass 5 (theory-informed extraction)** and the
   `theory-extractor` / `theory-evidence-scorer` agents (stubs exist).
2. **Reconcile with the 45 existing `theories/` nodes** — many are dark stubs; dedup + enrich, don't double-mint.
3. **Wire evidence edges** — `SUPPORTS` / `CONTRADICTS` (evidence → theory), `CITED_BY` (theory → theorist).
   Dip-gated + fresh-subagent-verified like the causal-arc machine; theories are interpretive → Tier 3-5,
   never Tier 1-2 (a wrong cited edge is graph pollution — the project value holds doubly here).
4. **First concrete seed already drafted:** `eldritch-apocalypse-seed.md` (this folder) — research captured
   S110 so it isn't re-derived. Use it as the worked example / template for the seed-file schema.

## Pointers

- Backlog item: `worklog.md` Ideas & Backlog → HIGH "Create theory seeds file".
- Schema: `reference/architecture.md` → `concept.theory` type + "Evidentiary (Theory Support)" edges + Tiers.
- Agents (stubs, prompts unwritten): `theory-extractor` (Pass 5), `theory-evidence-scorer`.
- Existing nodes: `graph/nodes/theories/` (~45, mostly edge-less).
- Connects to: the deferred TWOIAF / Fire & Blood ingestion (pre-series events anchor R+L=J / KotLT / deep-lore theories).

## Index of staged seeds

- `eldritch-apocalypse-seed.md` — the cosmic-horror / Lovecraftian-influence theory (Euron / Drowned God).
  Drafted S110 from Matt's question + a quick web pass. Ready to template the seed-file schema.
