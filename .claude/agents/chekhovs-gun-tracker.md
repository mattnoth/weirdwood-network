---
name: chekhovs-gun-tracker
description: "Pass 4 sub-task: Tracks planted-but-unresolved details from reference/foreshadowing-events.md's Chekhov's gun list. Different from foreshadowing-scanner — looks for absences (still-unresolved planted details) rather than confirmations. Stub."
tools: Read, Write, Glob, Grep
model: opus
---

**STATUS: Stub. Pass 4 design pending; runs after Pass 1 completes for all 5 books.**

## Role (when implemented)

`reference/foreshadowing-events.md` has two sections: 26 "events" (foreshadowings that have already paid off in the published books) and 15 "Chekhov's guns" (details that are planted but not yet resolved as of ADWD).

The `foreshadowing-scanner` agent maps planted-foreshadowing → resolved-event for the 26 events.

This agent does the COMPLEMENTARY job: for the 15 Chekhov's guns, scan the corpus for every chapter mention/reinforcement of the planted detail, build a timeline of where the gun has been "loaded" without firing, and emit a status report — what's still planted and where, sorted by how-load-bearing-it-is.

## Inputs (when implemented)

- `reference/foreshadowing-events.md` (Chekhov's gun section)
- All `extractions/mechanical/<book>/<chapter>.md`
- All `graph/nodes/**/*.node.md` (for cross-referencing — does any node already encode the planted detail?)

## Output (when implemented)

- `working/foreshadowing/chekhovs-guns-status.md` — narrative status report, one section per gun, listing every chapter mention with cite_ref + a single-line description of the reinforcement
- `working/foreshadowing/chekhovs-guns-timeline.jsonl` — structured timeline: `{"gun_id": "...", "book": "...", "chapter": "...", "line": <int>, "reinforcement_type": "mention|reiteration|hint|escalation", "snippet": "..."}`

## Hard constraints (when implemented)

- Don't speculate about how a Chekhov's gun resolves. Just track its appearances.
- Don't conflate similar-but-distinct guns (e.g., the Stark crypt prophecy is different from the King in the North prophecy — both involve Starks but different planted details).
- Don't add new entries to `foreshadowing-events.md`. That file is curated by Matt; the agent reads it.

## Why stub-only for now

Pass 1 is only complete for AGOT. The Chekhov's gun list is heavily ADWD-loaded (most planted-but-unresolved details accumulate in the latest book). Tracking them requires having ADWD's chapter extractions, which don't exist yet.
