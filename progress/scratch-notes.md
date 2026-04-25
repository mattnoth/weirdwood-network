# Scratch Notes

Observations worth keeping but not yet triaged. Tag with source/date.

---

### POV Reference Table Gaps (Session 2, chapter-splitter)

The original `reference/pov-characters.md` was missing 6 chapter headings. All have been added:
- AFFC: THE REAVER (Victarion Greyjoy)
- ADWD: THE BLIND GIRL (Arya), A GHOST IN WINTERFELL (Theon), THE IRON SUITOR (Victarion), THE KINGBREAKER (Barristan), THE QUEEN'S HAND (Barristan)

### Smart Quotes in Source Files (Session 2, chapter-splitter)

Source .txt files use Unicode curly/smart quotes (U+2019 right single quote mark instead of U+0027 straight apostrophe). The chapter splitter normalizes these before heading matching. The wiki scraper may also need to be aware of this if cross-referencing chapter text.

### Relational DB Decision — Defer (Session 13, 2026-04-25)

Not needed yet, and probably not for a long time. Reasoning:
- Pass 2 output is ~5,279 wiki entities + ~17K cite_ref records. That fits easily in JSONL/markdown and grep.
- Access patterns so far are: "find entity X," "find all entities with edge Y," "filter by `first_available`." All trivially served by JSONL + Python or markdown + grep.
- A graph DB (Neo4j) becomes useful when you need real traversal queries — "find all characters within 3 hops of Jon Snow who appear before AGOT Bran III." That's still 1–2 passes away.
- The Active Decision in worklog (`OPEN: Storage Format`) already leans markdown-first. Confirming that lean.
- Migration cost from JSONL → SQLite → Neo4j is low because the parser output is already structured. The choice can be deferred without painting into a corner.

**Recommendation:** stay with JSONL + markdown for Track B. Revisit when there's a query that's painful without traversal.

### Collaborator Onboarding — Schema Lock-In Before Handoff (Session 13, 2026-04-25)

A collaborator may join to share the extraction load — effectively running concurrent extraction agents from another machine. Implication: the Pass 1 schema (and surrounding pipeline) needs to be **ironclad before handoff**, because the collaborator is not as deep a fan, doesn't remember the books in detail, and hasn't done the theory-video research. They need a process that produces correct output without needing the lore knowledge to second-guess the schema.

What this changes:
- **Track B sequencing reaffirmed:** schema review after Track B (informed by wiki coverage) is even more important if a non-expert is going to run the schema across more books.
- **`/install-github-app` value rises:** tagging Claude in PRs/issues from GitHub becomes the natural review surface for collaborator-produced extractions. Revisit installing once schema is locked and collaborator is ready.
- **Documentation needs:** README's onboarding flow should hold up for a collaborator who has the source files but isn't going to read the worklog. The skip-ahead note (Session 13) helps. May need a "running extractions" quick-reference doc that doesn't require reading CLAUDE.md end-to-end.
- **Schema lock-in checkpoint:** before handoff, do a full v3 schema review across AGOT (post-Track B) and resolve any open issues. Treat schema lock as a hand-off gate.

### Foreshadowing Pass Prep — Expand Event List & Chekhov's Guns (Session 13, 2026-04-25)

**Long-lead reminder for Pass 4 (foreshadowing-scanner):**

`reference/foreshadowing-events.md` currently has 26 events + 15 Chekhov's guns. Before running Pass 4, audit and expand both:

1. **Foreshadowing events** — review whether 26 known-future-event anchors are enough for the scanner to be useful. Likely too few. Add events from:
   - Major character deaths and identity reveals (Red Wedding, Joffrey, Tywin, Jon's stabbing, Hardhome, Quentyn's burning, Stannis's march on Winterfell, Bran's warging, etc.)
   - Major plot reveals (Lannister twincest, Jon's parentage hints, Arya's Faceless Men arc, Bran's Greenseer arc, Sam's Citadel arc, Davos's resurrection role, Theon's redemption arc)
   - Magic returnings (dragons hatching, White Walkers reawakening, glass candles burning, warging confirmed)
   - Prophecy fulfillments and inversions
2. **Chekhov's guns** — current list is 15. Expand to build a *pattern* the scanner can use to find *unknown* Chekhov's guns. Each gun entry should describe:
   - The setup (where the object/fact/character is introduced)
   - The shape of the payoff (or "unfired" if still open)
   - The textual pattern that signals "this matters later" (named in dialogue, dwelt on by POV, contrasted with normal description, etc.)

The pattern library is the actual scanner input. Without it, the scanner can only check for events the user already named. With it, the scanner can flag *candidate* foreshadowing for unknown payoffs — which is the whole point of Pass 4.

**Action when Pass 4 nears:** dedicated session to expand the events list and Chekhov's gun pattern library. Before then, surface this scratch-note in Pass 4 prompt design.
