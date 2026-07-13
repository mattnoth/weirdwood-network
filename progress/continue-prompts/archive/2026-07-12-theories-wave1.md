# SESSION 214 — Theories wave 1: ASX transcript extraction → re-grounding → first mints

> **This is Session 214.** Stamp your worklog entry `### Session 214` at endsession.
> **Recommended model:** **Fable orchestrator** (Matt's explicit call — theories are the
> interpretive layer; adjudication depth matters) + Sonnet extraction/proposer subagents +
> Haiku fresh-verifiers.
> **PRE-REQ:** S213 committed+pushed (`779af9a4c2` or later). If git log disagrees with
> worklog.md S213, STOP and reconcile.

## Why (gate opened S213)

Matt opened the theories gate 2026-07-12 ("Yes — theories"), steer: **video-transcript-first
via Alt Shift X**. S213 did step 1: 183-video channel inventory → 72 theory candidates →
**curated 15-video wave-1 starter set, all transcripts pulled** to
`working/theories/videos/transcripts/*.en.vtt`. Read `working/theories/README.md` FIRST —
it holds the pipeline, the schema, and the starter table. Matt has NOT vetoed the starter
set; confirm it with him or proceed if he says go.

## The work (per theory; start with the R+L=J cluster — 3 mutually reinforcing transcripts)

1. **Extraction** (Sonnet, one agent per transcript): from the VTT → claim one-liner,
   sub-claims, every evidence beat the video cites (paraphrase + book-location hint),
   counter-evidence beats. Output JSONL per video in `working/theories/extractions/`.
2. **Re-grounding** (deterministic first: adapt `scripts/upgrade-wiki-quote-cites.py`'s
   normalized-containment corpus matcher; Haiku for residue): every beat → verbatim quote +
   `chapter:line` from `sources/chapters/`, or flagged unmatched. ASX is the map, the books
   are the truth — no beat mints on the video's authority alone.
3. **Node + edges** (the proven dip machine: propose → Haiku fresh-verify → adjudicate →
   standing audits → quotecheck → dry-run → Matt's go → mint): enrich existing stubs
   (jon-snow-theories, knight-of-the-laughing-tree-theories, azor-ahai-theories, …) or mint
   new (`grand-northern-conspiracy`, `eldritch-apocalypse` — the S110 seed in
   `working/theories-staging/eldritch-apocalypse-seed.md` is the worked template).
   Edges: SUPPORTS / CONTRADICTS (evidence → theory), CITED_BY (theory → theorist/video).
   **Theories are Tier 3–5 ALWAYS.**
4. **Chat surface: DO NOT touch** — SHARED_RULES' no-theories guardrail stays; exposing the
   theory layer in the chat is a separate Matt product decision.

## Vocabulary (paste into subagent prompts — they don't load CLAUDE.md)

Pass = big numbered corpus sweep; Track = named chunk of work; step (lowercase) = ordered
piece inside a Track; Tier = confidence rating 1–5 ONLY (never for work/process).
Harvest rule: while in chapter text for ANY reason, drop `chapter:line / kind / note`
pointers to notable off-task finds into the agent's own harvest file; POINT, don't extract.

## DO NOT

- Do NOT mint or deploy without Matt's explicit go (autonomous grant was S213-scoped).
- Do NOT let theory claims into tier-1/2 or into node prose stated as fact.
- Do NOT re-pull the ASX channel list or transcripts (all 15 are on disk).
- Do NOT run /endsession without permission.
