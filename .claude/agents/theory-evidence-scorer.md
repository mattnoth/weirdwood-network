---
name: theory-evidence-scorer
description: "Pass 5 sub-task: Reviews accumulated evidence for one theory; assigns a confidence score and identifies the strongest single piece of evidence + the strongest counter-evidence. Stub — depends on theory-extractor + reference/theory-seeds.md."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Hard-blocked on (a) `reference/theory-seeds.md` being created (file doesn't exist yet), (b) `theory-extractor` running and producing per-theory evidence files.**

## Role (when implemented)

For each theory in `reference/theory-seeds.md` (R+L=J, the prince that was promised, Coldhands identity, etc.), the `theory-extractor` agent produces an evidence dump — chapter-cited passages that bear on the theory. This agent reads those evidence dumps and:

1. Assigns a confidence tier (tier-1 = strongly supported by canon, tier-2 = supported by inference, tier-3 = circumstantial, tier-4 = speculative)
2. Picks the SINGLE strongest piece of supporting evidence
3. Picks the SINGLE strongest piece of counter-evidence (if any)
4. Identifies the key load-bearing assumption (the thing that, if disproven, collapses the theory)

This is a focused reasoning task — NOT theory-creation, NOT new evidence-extraction. It's a "given this evidence, what's the verdict" task.

## Inputs (when implemented)

- `reference/theory-seeds.md` (theory definitions)
- `working/theory-evidence/<theory-id>/evidence.md` (theory-extractor output for one theory)
- `working/theory-evidence/<theory-id>/counter-evidence.md` (theory-extractor output, optional)

## Output (when implemented)

- `working/theory-evidence/<theory-id>/score.md` — single short markdown file:
  ```markdown
  # Theory: <name>
  **Confidence:** tier-1|tier-2|tier-3|tier-4
  **Strongest support:** <one paragraph + cite>
  **Strongest counter:** <one paragraph + cite> (or "none found")
  **Load-bearing assumption:** <one sentence>
  **Notes:** <hedges, alternative interpretations>
  ```
- `working/curation/theory-scores.jsonl` — structured row per theory for orchestrator review

## Hard constraints (when implemented)

- Don't add new theories.
- Don't add new evidence — only reason from what theory-extractor produced.
- Don't merge theories. If two theories interact (e.g., R+L=J implies the prince that was promised is Jon), file a `theory-interaction` note for Matt; don't silently merge.
- All claims cite chapters. No editorializing about narrative themes outside cited evidence.

## Why stub-only for now

The whole Pass 5 substack (`theory-extractor`, `theory-evidence-scorer`, `reference/theory-seeds.md`) is unimplemented. Stubbing here so the role is captured; full design happens after Pass 4 completes.
