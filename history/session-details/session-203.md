---
session: 203
date: 2026-07-09
model: Fable 5 (orchestrator) + Haiku (fresh-verify ×2) + Sonnet (attachers ×3, script-builder ×1)
---

# Session 203 — F&B close-out + show-watcher ship + harvest drain

The handoff scoped this as the F&B close-out (Sonnet-recommended); it ran on Fable and grew
into a triple session on Matt's live direction: (1) the planned close-out, (2) a show-watcher
product push with four prod deploys, (3) the full 337-row harvest drain that the continue
prompt had marked "may split."

## Arc 1 — Show-watcher push (Matt-driven, mid-session)

Matt opened asking whether the F&B bulk apply was deployed (it wasn't — live bundle was
pre-S200, confirmed by probing `/api/node` for a fresh node) and whether show-watchers
("House of the Dragon") could find the Dance. Shipped across four prod deploys:

- **Dance aliases** on `dance-of-the-dragons` ("House of the Dragon", "the Dance", "the
  Targaryen civil war"…) — fuzzy candidates were weak 0.55s, no shadowing.
- **Show-watcher rule in SHARED_RULES** (Matt: "ship it now"): map GoT/HotD phrasings to book
  entities, flag book-vs-show divergence in one plain clause, never detail/cite show scenes.
  Test pin 11768→12489. Live probe ("Rhaenyra eaten by a dragon?") answered from the
  *session-minted* `death-of-queen-rhaenyra` node with Gyldayn quotes and a clean divergence
  clause — the whole loop verified end-to-end.
- **GoT rename aliases**: Yara→asha-greyjoy, Robin Arryn→robert-arryn, Three-Eyed
  Raven→three-eyed-crow, White Walkers→others. Deliberately did NOT alias "Night King"→
  nights-king (different figures; divergence is the persona's job, not the resolver's).
- **Cross-era backfill track logged** (Matt's "backfill GoT edges" ask): the probe's EMPTY
  `walk_chain` on death-of-queen-rhaenyra is the evidence — new F&B nodes have role edges but
  no causal spine. Matt confirmed my reading over his original (edge-vocab retrofit, now a
  separate backlog item) and sequenced: harvest → causal → cross-era seams (+ D&E) → theories-era.

## Arc 2 — F&B close-out proper

**Deferred-events triage (38 rows):** deterministic token-screen vs event-slug inventory
first (the fuzzy resolver alone was misleading — it missed real nodes and proposed wrong
ones). 6 skip-exists / 2 folds (cremation→death-of-aegon-ii; Gay Abandon→
capture-of-prince-viserys) / 30 CREATE. Two Haiku fresh-verify agents, then orchestrator
re-verify caught: 7 invented character slugs (real nodes existed under other names), a
dead-Daemon hallucination on the 131 AC Dragonstone garrison fall, 2 harm-gate violations
(childbirth ≠ harm), and one false PROBLEM (quote was exactly at the cited line). Minted 30
nodes + 47 edges via a hand-built candidates pack; mint's strict quote-locator forced curly-
quote/wrap fixes my normalized checker had passed. death-of-aegon-ii carries `larys-strong
SUSPECTED_OF` (tier-2, `gyldayn-synthesis`, disputed) per the B6-R9 adjudication.

**Golden repin:** the mint broke `family.json:family-aegon-i-targaryen-default-window` —
generationCounts only. Root cause understood before touching it: family-tree spine selection
is prominence-weighted (degree + 4×quoteCount); 47 new edges raised Dance principals' degree,
so gen-5 membership grew 3→8 under the 96-member cap. mustInclude (the real invariant) held.
Repinned with an explanatory note; py+ts suites both green after.

**KNIGHTED_BY audit:** architecture.md defines Knight→Dubber, so B5's "majority convention"
note was backwards — the 6 dubber→knight edges were the mislabeled ones. Retyped them to
`BESTOWS_KNIGHTHOOD_ON` (which exists for exactly that direction); the 3 "outliers" were
correct all along. Lesson recorded: majority-in-data ≠ convention; the schema doc wins.

**capture-of-prince-viserys:** 129→130 AC on the Gullet's "fifth day of the 130th year"
primary anchor.

**Lineages §3.4 (script-builder):** the appendix unit turned out NOT to contain the family-
tree diagrams (raster images, never text) — only a 17-monarch succession list + an interview
transcript glued on by the known scrambled-toc bug. `fab-lineages-diff.py` parsed 17 triples →
13 confirm / 0 new / 0 conflict; 4 bare-name royals conservatively unresolved. Two real bugs
the agent caught and fixed: bare "Viserys" confidently resolving to Dany's brother (collision
guard added) and redirect-stub slugs producing false conflicts (redirect_to followed). Thin
validation, honestly labeled in the design doc.

**Review-bucket plan (1,440 rows):** grouped by reason. Headline: `event-dedup-risk` (221) +
`composite-name` (57) are a SECOND deferred-events vein hiding real majors (Death of Queen
Helaena, Battle of the Stepstones) behind nonsense fuzzy matches; a ~147-entry curated map
recovers 514/929 unresolved-name rows; small classes are minutes each.
`REVIEW-BUCKET-TRIAGE-PLAN-s203.md` has the policy table + sequencing.

**Zero-edge stub sweep (new find):** 38 pass-fab-enrichment event nodes have no edges at all
(`zero-edge-stubs-s203.jsonl` w/ unit provenance). Absorbs the B1 PART_OF re-adds; wired into
the causal-session scope.

## Arc 3 — Harvest drain (337 rows, in-session on Matt's go)

S152 disjoint-dir architecture, adapted: Python pre-pass parsed the slash-delimited pointers,
wrap-tolerantly located 96% in the fab chapters, and routed by kind. **53 causal-spine rows
staged** to `causal-spine-seeds-s203.jsonl` — they're literal chain sketches ("Moon's
assassination → host disintegrates → way clear → Jaehaerys crowned"), i.e. the next session's
input, not attach material. Three Sonnet attacher waves (events-dirs 34; chars-desc 65;
chars-hist 104 grouped-by-monarch; chars-xid 51) + orchestrator handled handback cross-routing
(4 event-homed, 19 event/medical/concept-homed, 11 char-homed re-packeted) and 12 OCR-garbled
rows recovered by fragment-grep. **Total ~278 quote blocks attached across ~200 nodes.**
Notable agent calls: post-Dance "Lady Alysanne" = alysanne-blackwood (timeline trap);
Maidenpool rows homed to the in-world text node `chronicles-of-maidenpool`; pipe-for-I OCR
artifacts preserved verbatim after verifier FAILs. Cross-identity wave needed ZERO new aliases
— every alternate name was already on its node. 3 no-home rows logged as future-mint
candidates. Verifier closed at **1079/1079 book-cited quotes PASS** (was 803 pre-session).

## Deploys (4)

1. Bulk-apply graph + Dance/HotD aliases. 2. Show-rule + S203 mint. 3. GoT rename aliases.
4. Harvest-drain quotes (bundle: 8,719 nodes / 25,035 edges / 6,382 quotes / 29,170 alias
phrases). Model/env untouched (Opus, $50/day cap).

## Sequencing set by Matt (end of session)

Harvest ✅ (this session) → **causal spine** (seeds staged) → **cross-era seams** (Blackfyre,
Dark Sister, D&E included) → then his edge-vocab-retrofit idea rides as backlog. Strip track
un-park remains Matt-gated. Theories still gated.
