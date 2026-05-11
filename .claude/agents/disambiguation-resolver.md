---
name: disambiguation-resolver
description: "Stage 4 sub-task: When prose says 'King Aegon' (or any ambiguous reference), decides which entity is meant from a list of candidates. Reads surrounding context + chronology hints. Stub — full prompt to be written when Stage 4 candidate volume justifies it."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Not yet runnable.** Write the full prompt when `prose-edge-classifier` accumulates a meaningful number of `escalate_disambiguation` decisions in `prose-edges/` JSONL files.

## Role (when implemented)

When the `prose-edge-classifier` flags a reference as ambiguous (e.g., "Aegon" could be I, II, III, IV, or V; "Brandon Stark" could be the Builder, Eddard's brother, or Bran), this agent reads the surrounding prose + chronological context (cite_refs to which book, mentioned characters' eras) + each candidate's frontmatter aliases and decides which one is meant.

## Inputs (when implemented)

- `working/wiki/pass2-buckets/<bucket>/prose-edges/<slug>.edges.jsonl` rows with `decision: escalate_disambiguation`
- The source node's full prose
- Each candidate's frontmatter (just type + aliases + first_appearance hints from cite_refs)

## Output (when implemented)

`working/wiki/pass2-buckets/disambiguation-decisions.jsonl` — one row per resolved ambiguity. Schema:
```json
{"source": "<slug>", "ambiguous_anchor": "...", "candidates": ["...", "..."], "chosen": "<slug>", "rationale": "<one paragraph>", "confidence": "tier-1|tier-2|tier-3"}
```

## Hard constraints (will apply when full prompt written)

- Read-only on graph nodes.
- Don't propose `SAME_AS` (cross-identity-detector's job).
- Don't expand the candidate list — your input already enumerates the choices; pick from them or escalate to questions.
- If genuinely undecidable, file a question of type `disambiguation-undecidable`.

## Why stub-only for now

Disambiguation reasoning needs Pass-1-derived chronology context that isn't fully built yet. Wait for Pass 1 to complete (or at least ACOK + ASOS) before designing this agent's prompt — the cite_ref book/chapter signals are richer with more Pass 1 coverage.
