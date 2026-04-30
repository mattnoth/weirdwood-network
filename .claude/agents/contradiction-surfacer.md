---
name: contradiction-surfacer
description: "Stage 4 sub-task: Compares wiki claims (in graph nodes) to Pass 1 chapter extractions; surfaces cases where they disagree. Doesn't decide who's right — surfaces for human review. Stub — runs after Pass 1 is complete for ≥2 books."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Hard-blocked until Pass 1 has multi-book coverage.** Write the full prompt after Pass 1 completes for ACOK + ASOS (currently only AGOT is done).

## Role (when implemented)

For each promoted node, compare its frontmatter + body claims against the matching Pass 1 chapter extractions for that entity. Surface contradictions:
- Wiki says X was Hand of the King in 295 AC; Pass 1 ASOS chapter shows X was already in Casterly Rock that year.
- Wiki says X is Y's father; Pass 1 dialogue shows Y referring to X as uncle.
- Wiki and Pass 1 disagree on a death scene's circumstances.

The agent does NOT decide who's correct. It surfaces the contradiction for human curation.

## Inputs (when implemented)

- All `graph/nodes/**/*.node.md`
- All `extractions/mechanical/<book>/<chapter>.md` for Pass-1-complete books
- `reference/architecture.md` for confidence tiering

## Output (when implemented)

Append-only `working/wiki-pass2/pass1-contradictions.jsonl`:
```json
{"node": "<slug>", "claim": "<one sentence>", "wiki_evidence": "<source>", "pass1_evidence": "<chapter>:<line>", "severity": "high|medium|low", "detected_at": "<UTC ISO8601>", "resolved_at": null, "resolution": null}
```

## Hard constraints (when implemented)

- Read-only.
- Surface; don't resolve.
- Don't modify nodes or extractions.
- Skip non-Pass-1-complete books (mark as `pending-pass-1` and defer).
- Use the same confidence tier rubric as architecture.md — wiki claims are tier-1 by default, chapter claims are tier-1 by default; tier-2 only when one side is hedged.

## Why stub-only for now

Pass 1 is only complete for AGOT. Running this agent now would only surface AGOT contradictions — leaving 4 books' worth of contradictions undetected. Wait for fuller Pass 1 coverage (at least ACOK + ASOS) before running. The orchestrator can re-run incrementally as each book completes.
