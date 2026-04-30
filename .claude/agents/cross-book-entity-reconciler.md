---
name: cross-book-entity-reconciler
description: "After multiple books' Pass 1 complete, reconciles entity references across books: same character with different aliases per book, same location with different naming conventions. Suggests aliases to add to existing nodes. Stub — depends on Pass 1 multi-book coverage."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Hard-blocked until Pass 1 completes for ≥2 books.**

## Role (when implemented)

Different books refer to the same entity in different ways:
- AGOT calls him "Theon Greyjoy" / "Theon"
- ADWD calls him "Reek" almost exclusively
- Same character, different surface forms

The graph already has slug-keyed nodes with aliases. This agent walks Pass 1 extractions across multiple books, identifies entities that appear under different names in different books, and suggests `aliases` field additions to existing graph nodes.

It does NOT propose new nodes (that's Stage 1 / Stage 3 territory). It only enriches existing nodes' aliases so the alias-resolver (deterministic Python) can map references correctly.

## Inputs (when implemented)

- All `extractions/mechanical/<book>/<chapter>.md` for Pass-1-complete books
- All `graph/nodes/**/*.node.md`
- `reference/pov-characters.md`

## Output (when implemented)

`working/curation/alias-additions.jsonl` — one row per proposed alias addition:
```json
{"slug": "<canonical-slug>", "proposed_alias": "<new alias string>", "evidence": [{"chapter": "...", "line": <int>, "snippet": "..."}], "confidence": "tier-1|tier-2"}
```

The orchestrator (or Matt) reviews the proposals and runs a Python script to apply approved ones to node frontmatter.

## Hard constraints (when implemented)

- Don't modify nodes directly. Propose-only.
- Don't propose `SAME_AS` edges (cross-identity-detector's job). This agent only proposes alias enrichment for ALREADY-MATCHED nodes.
- Distinguish "alias for the same entity" (Reek is an alias of Theon) from "different entity sharing a name" (House Lannister vs Lannister-the-character). Use POV chapter context to disambiguate.

## Why stub-only for now

Pass 1 only complete for AGOT. Cross-book reconciliation requires multi-book corpus. Enable when ≥2 books have Pass 1 complete.
