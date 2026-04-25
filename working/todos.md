# Actionable TODOs

> **Purpose:** Tasks that need doing but aren't part of the current session's work. Organized by topic. Check items off as they're completed. Move completed items to a "Done" section at the bottom periodically.

---

## Agent Improvements

- [x] **mechanical-extractor: test variations** — Done 2026-04-22. Smoke test on 3 AGOT chapters (prologue, bran-01, catelyn-01) surfaced three issues: cross-chapter dramatic-irony leak, no confidence tier convention, missing `first_available` field in metadata. All addressed via prompt patches (see below).
- [x] **mechanical-extractor: chapter isolation enforcement** — Done 2026-04-22. Added dedicated "Chapter Isolation — Critical" section to agent prompt; flipped Rule #5 from "Note dramatic irony" (which encouraged leakage) to "Dramatic irony is NOT your concern"; tightened the `Known To (Reader Only?)` column definition to within-chapter scope only.
- [x] **mechanical-extractor: confidence tier convention** — Done 2026-04-22. All Pass 1 output now treated as Tier 1 by default, with only two explicit exception markers: `(inferred)` and `(uncertain — verify)`. Eliminates per-row tier-tag noise.
- [x] **mechanical-extractor: first_available field** — Done 2026-04-22. Added `first_available` field to Chapter Metadata section of output schema so downstream passes can grep spoiler-gating anchor directly.
- [x] **mechanical-extractor: no meta-commentary in tables** — Done 2026-04-22. Added Rule #9 forbidding the extractor from using table cells to explain its own extraction choices (observed in agot-bran-01 smoke output — "symbolic weight is implicit…" in the Information Revealed table).
- [x] **mechanical-extractor: tighten Raw Entity List categories** — Done 2026-04-24. Prompt now v3: 12 categories (10 named + Other catch-all), strict formatting rules (all headers required, no merging/renaming, "None" for empty). Prior extractions archived (agot-v1, agot-v2, acok-v2). v3 run in progress (30/73 AGOT).
- [ ] **mechanical-extractor: add worked example** — Still open. The original spec had an AFFC Prologue example extraction showing ideal output. Consider adding as a reference file the agent loads. Deferred until we've seen the patched prompt run a full book — if output quality is high without the example, may not be needed.
- [ ] **mechanical-extractor: verbose extraction rules** — Still open. The original spec had richer fact-vs-interpretation explanations (e.g., "Ned thinks about a promise" = fact vs. "Ned is thinking about Lyanna's deathbed promise about Jon" = interpretation). Deferred pending full-book output review.
- [x] **script-builder: verify POV table completeness** — Done. Found 6 missing headings (THE REAVER, THE BLIND GIRL, A GHOST IN WINTERFELL, THE IRON SUITOR, THE KINGBREAKER, THE QUEEN'S HAND). All added to reference file and splitter.

## Timeline & Chronology

- [ ] **Timeline reconstruction pass or script** — Once all books have Pass 1 extractions with `time_markers` fields, build a dedicated pass (or Python script) that attempts fan-community-style relative timeline reconstruction from the captured markers across all chapters. Cross-reference with known travel times, moon-turn references, and seasonal indicators.

## Direwolves & Dragons

- [x] **Direwolves and dragons are characters, not creatures** — Ghost, Grey Wind, Lady, Nymeria, Summer, Shaggydog, Drogon, Rhaegal, and Viserion must be treated as characters in all extractions and graph nodes. They have agency, POV-adjacent perspectives, and narrative arcs. Added to mechanical-extractor prompt (2026-04-22). Verify AGOT re-run captures them in Characters Present tables, not as fauna. Ensure node schema and future agent prompts also enforce this.

## Agent Prompts to Write

- [ ] **Pass 2: wiki-ingester** — Full prompt. Needs: node file schema, wiki infobox parser output, entity target list from Pass 1, **wiki-category → confidence-tier mapping** (wiki mixes canon, fan inference, and theory on the same pages — the category/tag system helps route to correct tiers, but needs explicit rules).
- [ ] **Pass 3: voice-analyzer** — Full prompt. Needs: voice profile schema, perception mapping format, identity-split handling.
- [ ] **Pass 4: foreshadowing-scanner** — Full prompt. Needs: mapping output schema, confidence criteria, scanning strategy (per-chapter vs per-event).
- [ ] **Pass 5: theory-extractor** — Full prompt. Needs: theory seeds file first (`reference/theory-seeds.md`), evidence mapping schema.
- [ ] **Pass 6: discovery-agent** — Full prompt. Needs: scoping strategy, candidate finding format, chunking approach.

## Reference Files to Create

- [ ] **theory-seeds.md** — Top 20-30 ASOIAF theories with descriptions and confidence tiers. Input for Pass 5.
- [ ] **taxonomy.md** — Standalone reference for entity types, edge types, confidence tiers (currently embedded in architecture.md).
- [ ] **node-schema.md** — What does a single entity node file look like? Frontmatter fields, required sections.
- [ ] **Expand `reference/foreshadowing-events.md` before Pass 4** — currently 26 events + 15 Chekhov's guns. Audit/expand both: more event anchors (deaths, identity reveals, plot reveals, magic returnings, prophecy fulfillments) AND a richer Chekhov's gun *pattern library* so the scanner can flag candidate unknown foreshadowing, not just match known events. See `progress/scratch-notes.md` "Foreshadowing Pass Prep" entry for detail. Long-lead — Pass 4 is many sessions away, but file this now so it's not forgotten.

## Collaboration

- [ ] **Schema lock-in before collaborator handoff** — A collaborator may join to share extraction load. They have less ASOIAF depth than Matt, so the Pass 1 schema must produce correct output without needing lore knowledge to second-guess. Sequence: finish Track B → schema review across AGOT v3 → lock schema → onboard collaborator. See `progress/scratch-notes.md` "Collaborator Onboarding" entry.
- [ ] **Revisit `/install-github-app`** — Useful once a collaborator is producing extractions: tagging Claude in PRs/issues becomes the natural review surface. Skip until handoff is near.
- [ ] **Collaborator quick-reference doc** — README onboarding works for first-run, but a collaborator extracting on another machine needs a focused "running extractions" reference that doesn't require reading CLAUDE.md end-to-end. Write before handoff.

## Wiki / Pass 2 Prep

- [ ] **Track B orchestration planning (PLAN-ONLY session)** — Design the multi-agent orchestration for wiki Pass 2 before writing code. Decompose deterministic vs. agentic work, define wave-equivalent for wiki, mirror extraction-stats observability, decide batch granularity, lock in no-DB-for-now. Output: `working/runbooks/wiki-pass2-orchestration.md`.
  → continue: `2026-04-25-track-b-orchestration-planning.md`
- [ ] **Wiki infobox parser for `first_available`** — Wiki "Books" infobox field has structured HTML with appearance types: `(POV)`, `(appears)`, `(mentioned)`. First non-"mentioned" book → `first_available`. 5,279 of 17,657 pages have infoboxes. Write a script to extract this systematically. Chapter-level links also exist in body text (`A_Game_of_Thrones-Chapter_2` pattern) for finer granularity. **Implementation gated on orchestration runbook above.**
  → continue: `2026-04-24-track-b-wiki-infobox-parser.md`
- [ ] **Wiki infobox field → edge type extraction** — Infobox fields (Father, Mother, Spouse, Allegiance, Overlord, etc.) map directly to edge types. See mapping table in `reference/architecture.md`. Script should parse these for Pass 2 input.
- [ ] **AGOT supplementary entity index** — Lightweight script to scan existing AGOT extractions and build a supplementary index for the 7 candidate entity types (religion, culture, species, magic, title, text, war). Not a re-extraction — just categorize what's already captured in narrative sections.
- [ ] **Wiki uncategorized page triage** — 17,305 of 17,945 wiki pages are in `_uncategorized/`. Before designing Pass 2, scan `_category-reports/` and sample uncategorized pages to determine what entity types are actually needed. Will validate or reject the 7 candidate types.

## Infrastructure

- [x] **Chapter splitter script** — Done. `scripts/chapter-splitter.py`, all 5 books split (344 chapters total).
- [x] **Wiki scraper script** — Done. `scripts/wiki-scraper.py` (1213 lines, stdlib-only). Full crawl complete (17,945 pages, 377 MB).
- [x] **Batch extraction runner** — Done. `scripts/extract.sh` + `scripts/weirwood.zsh`. Wave-based parallel extraction via iTerm tabs, stats tracking, rate-limit detection, auto-worklog updates.
- [ ] **AGOT v3 schema review** — Review extraction output quality across AGOT v3 (73 chapters). Check for: section completeness, entity coverage gaps, Raw Entity List consistency, Food & Drink / Hospitality coverage. One known gap: agot-eddard-01 missing `### Other` header. **Sequenced after Track B** — see worklog "DECIDED: Track B Before v3 Schema Review" (2026-04-25). Track B's parser surfaces schema signals (entity boundaries, edge vocabulary, redundancy) that an isolated v3 review cannot.


