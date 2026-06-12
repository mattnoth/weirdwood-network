⏺ You're right and I was framing this wrong. Let me show what I found, then propose the artifact.

  Where I was wrong

  My "S74 still applies, don't enrich" recommendation conflated two different things:
  - Enrichment (S74's no-go) = "extract new edges from prose, into uncertain territory" — that's where 74.5%/62.5% precision gets you graph pollution.
  - Backfill (what you're describing) = "we already have an edge with verified evidence; retype it to a more specific vocab type that didn't exist when it was emitted" — that's a constrained retype, not a new emission. The evidence is
  already there. The risk profile is fundamentally different.
  
  S74's ban doesn't apply to backfill. I was wrong to invoke it.

  Empirical evidence that the dictionary approach works

  I just scanned existing edges for hint phrases against newer-vocab types:

  ┌───────────────┬───────────────────────────────────────────────────────────────────────────────────┐
  │  Newer type   │            Existing edges with matching phrase, currently mistyped as             │
  ├───────────────┼───────────────────────────────────────────────────────────────────────────────────┤
  │ GUARDS        │ 12+ edges currently PROTECTS (3) / COMMANDS (3) / SWORN_TO (3) / COMPANION_OF (3) │
  ├───────────────┼───────────────────────────────────────────────────────────────────────────────────┤
  │ RESCUES       │ 6+ edges currently LOVES (2) / PROTECTS (2) / TRUSTS (1) / SIBLING_OF (1)         │
  ├───────────────┼───────────────────────────────────────────────────────────────────────────────────┤
  │ SPIES_ON      │ 2 edges currently ALLIES_WITH (1) / DISTRUSTS (1)                                 │
  ├───────────────┼───────────────────────────────────────────────────────────────────────────────────┤
  │ IMPRISONED_AT │ 3 edges currently APPOINTS / COMPANION_OF / RESENTS (all clearly wrong)           │
  ├───────────────┼───────────────────────────────────────────────────────────────────────────────────┤
  │ ENCOUNTERS    │ 2 edges currently FEARS / LOVER_OF (gate violations)                              │
  └───────────────┴───────────────────────────────────────────────────────────────────────────────────┘

  That's a small sample (only 6 patterns from a ~10-type vocab-drift list), and even at this floor I'm finding ~25+ deterministic retype candidates. Full sweep across all 7 post-S55 additions will likely surface 100-200+. Doable cheaply.

  Reframing SUB_BEAT_OF — you were pushing on the right thing

  SUB_BEAT_OF specifically: 0 literal backfill, because there are no event→event edges in the existing graph. But that's because the existing graph has structurally empty event hubs. Your instinct that "where characters are at a certain
  time might require examination" points at the bigger question: should existing character-relationship edges be reified into event hubs?

  Cleanroom (S82) said yes, explicitly, for this set:
  - Killings-at-named-occasion → currently KILLS person→person; could be AGENT_IN/VICTIM_IN on event hub.
  - Sieges → currently scattered FIGHTS_IN / COMMANDS; could be hub'd.
  - Wedding/tourney ceremonies → currently scattered ATTENDS / FIGHTS_IN.
  - CONSPIRES_WITH plots → currently scattered ALLIES_WITH / NEGOTIATES_WITH.
  - VIOLATES_GUEST_RIGHT → currently scattered. (404 GUEST_OF edges in the graph; some fraction anchor to named events.)

  That's real backfill, much bigger than SUB_BEAT_OF. The reification design intended it for the future; it just hadn't been queued.

  What I'd propose to capture this

  Write working/edge-modeling/post-plate5-backfill-design.md — a design memo (not for execution this session) covering three tracks:

  Track A — Vocab-drift retype (Phase 1 deterministic dictionary + Phase 2 Haiku for ambiguous rows).
  - Phase 1: for each post-S55 type, build a phrase-dictionary mapping old-vocab-emit + hint-phrase → new-vocab-type. Run as deterministic pass over edges.jsonl. $0.
  - Phase 2: for rows where the hint matches but the deterministic dictionary isn't confident enough (multiple candidate new-types, or hint is ambiguous), Haiku reads the row + evidence quote and picks. Constrained to retype-only (no new
  emissions). ~$5-15 budget.
  - Output: staged diff for your review before merge.
  - CONSPIRES_WITH plots → currently scattered ALLIES_WITH / NEGOTIATES_WITH.
  - VIOLATES_GUEST_RIGHT → currently scattered. (404 GUEST_OF edges in the graph; some fraction anchor to named events.)

  That's real backfill, much bigger than SUB_BEAT_OF. The reification design intended it for the future; it just hadn't been queued.

  What I'd propose to capture this

  Write working/edge-modeling/post-plate5-backfill-design.md — a design memo (not for execution this session) covering three tracks:

  Track A — Vocab-drift retype (Phase 1 deterministic dictionary + Phase 2 Haiku for ambiguous rows).
  - Phase 1: for each post-S55 type, build a phrase-dictionary mapping old-vocab-emit + hint-phrase → new-vocab-type. Run as deterministic pass over edges.jsonl. $0.
  - Phase 2: for rows where the hint matches but the deterministic dictionary isn't confident enough (multiple candidate new-types, or hint is ambiguous), Haiku reads the row + evidence quote and picks. Constrained to retype-only (no new
  emissions). ~$5-15 budget.
  - Output: staged diff for your review before merge.

  Track B — Reification of existing edges into event hubs (the cleanroom recommendation).
  - For each of the named reification-eligible families (killings-at-named-occasion, sieges, ceremonies, conspiracies, VIOLATES_GUEST_RIGHT), match existing person→person edges against existing event-nodes (and Plate-3 mints once Plate 5
  lands).
  - Where the match is strong: emit role edges (AGENT_IN/VICTIM_IN/etc.) on the event hub, mark original person→person edge as superseded_by: <hub-slug> (don't delete).
  - Mixed deterministic + Haiku.

  Track C — Head-rule retroactive cleanup beyond Plate 0's 10 flips.
  - Plate 0's normalizer caught explicit inversions (specific reverse-signal lexicon). The Plate 1 head rule (semantic-agent-not-grammatical-subject) is more subtle and broader. There are likely more direction errors than 10.
  - Deterministic phrase-pattern extension to Plate 0's normalizer, then sample-and-review.

  Plus: future passes (Dialogue v2.1) fold in the edge-modeling lessons — head rule mandatory, reification-aware extraction, current vocab not pre-S86 vocab. TODO item.

  What I want to confirm before writing

  1. Should this memo land at working/edge-modeling/post-plate5-backfill-design.md, or somewhere else?
  2. Plate 5 still proceeds as planned (Sonnet session, the ~50 retroactive cleanups already queued, no scope creep)? Then backfill becomes "Plate 6" / post-Plate-5 work, sequenced after the merge lands.
  3. Should I also add to working/todos.md a HIGH-priority "Post-Plate-5 backfill — 3 tracks" entry that links to the memo?

  Sound right?