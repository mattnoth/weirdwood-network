---
session: 68
date: 2026-05-24
title: "Stage 4 recall ceiling — mine all Pass 1 tables + recall-sample measurement"
model_orchestrator: Opus 4.7
model_delegates: script-builder (default Sonnet), recall-sample agent (Sonnet 4.6)
status: analysis + deterministic build; decisions queued for Matt
---

# Session 68 — Stage 4 recall ceiling: mine all Pass 1 tables + recall-sample

## How the session started

Matt asked two questions about the just-finished S67 Pass-1-derived edge work:
1. How does the most-recent (Pass-1-derived) edge yield compare to the **wiki edge prediction**?
2. How did the **line marking** (the locator's `file:line` citation step) play out?

**Answers (from the S67 audit artifacts):**
- **Wiki comparison.** Of 6,239 resolved book pairs, **1,973 (32%) corroborate** an existing wiki edge (now self-describing via `corroborates_known_edge` + `wiki_edge_type`), and **4,266 (68%) are NEW** (absent from the wiki graph). Against the deprecated wiki-comention path: that path's sink was 29,259 candidates and produced 5,723 rows from only 60/222 batches at $55.66; the Pass-1-derived path produced 5,219 complete edges at $20.88 (deterministic spine = $0), primary-source, with citations.
- **Line marking.** The locator attached a **verbatim quote + `file:line` to 5,816/5,886 candidates = 98.8%**; only 70 (1.2%) fell back to chapter-level. Per book 98.6–99.0%. (Caveat surfaced: that's a *match rate*, not a verified-correct rate — green tests did not catch the S66/S67 misresolution bugs; spot-audits did.)

## The recall-ceiling question

Matt's follow-up was the real design question: *if the Pass 1 extractor didn't tabulate a relationship, it's not in the edge set — so is prose reading required, or will this be good?*

Framed the answer as **layered recall**, not a single ceiling:
- The pipeline mines **only `## Relationships Observed`** (confirmed by reading `scripts/stage4-pass1-edge-candidates.py` — it also reads `Characters Present` for disambiguation and node `## Edges` for corroboration, nothing else).
- **Free headroom #1:** the other relational Pass 1 tables (Dialogue, Information Revealed, Events & Actions, Food, Hospitality) are already extracted — mining them is more Python, $0.
- **Layer #2:** the wiki layer complements it (the 32/68 split proves they cover different territory — wiki = structural/canonical; book = observed/emotional/cited).
- **Layer #3:** Pass 3 voice/perception is the *designed* home for subtextual/POV-memory edges a Relationships table under-captures.

Matt's directives: **(1a)** mine all Pass 1 tables + write tests; run the **recall-sample check**; **note (b)** book∪wiki coverage and **(c)** targeted-prose decision; and a question **(#2)** — can the wiki layer be fast if we look for fewer things?

## What was built / run (two parallel background agents)

### 1a — extra-tables miner (script-builder, deterministic, no LLM)
- NEW `scripts/stage4-pass1-extra-tables.py` (opt-in `--extra-tables`; writes to separate staging `working/wiki/pass2-buckets/pass1-derived/_extra-tables/{book}/`; **canonical spine untouched**).
- NEW `tests/test_stage4_extra_tables.py` (+81 tests; **431 total green**). One ordering bug (shelter pattern firing before refused/denied) caught immediately by `test_shelter_denied`.
- Report: `working/wiki/data/pass1-derived-extra-tables-report.md`. Output: 339 files / 4,951 rows.
- **Yield:**
  - **Hospitality & Guest Right:** 627 rows → **529 deterministic $0 edges** (460 `GUEST_OF` + 69 `VIOLATES_GUEST_RIGHT`). GUEST_OF qualifiers: shelter 211, feast 121, unknown 39, gift_exchange 33, refused 29, safe_conduct 17, bread_and_salt 10. VIOLATES: 93 flagged, 69 emitted (both endpoints resolved), 63 counted-only (unresolved victim e.g. "northern lords").
  - **Dialogue of Note:** 6,317 rows → 4,422 tail rows (clean Speaker→Listener pair; type needs the quote). LLM-type estimate **~$30** at the S67 rate ($0.0068/row).
  - **Food & Drink / Events & Actions / Information Revealed:** counted-only (prose-shaped; no fragile regex, no edges): 1,263 / 8,384 / 5,654 rows.

### Recall-sample check (Sonnet, manual judgment)
- Report: `working/wiki/data/pass1-derived-recall-sample.md`. **7 chapters** (doubled up on Red Wedding instead of an 8th): agot-eddard-07, agot-daenerys-06, acok-tyrion-03, asos-catelyn-06, asos-catelyn-07, affc-cersei-03, adwd-jon-06. 196 relationships enumerated.
- **A (caught now) = 64% · B (table-mineable) = 28% · C (prose-only) = 9%.**
- Bucket-B productivity ranking: **Events & Actions > Information Revealed > Hospitality > Dialogue.**
- Bucket C: ~⅓ high-value (~3% overall) — narrative asides (Gregor killing infant Aegon / raping Elia; Cersei↔Maggy from POV memory; Dany's terror of Viserys), ~⅔ low-value texture.

## The key finding (a tension the original plan didn't anticipate)

Crossing the recall-sample ranking with what the miner can actually emit:
- The **cheap deterministic win (Hospitality, 529 edges)** is only the **#3** recall table.
- The **#1/#2 recall tables (Events & Actions, Information Revealed)** are **prose-shaped → counted-only**, not cheaply deterministic. ~14k rows; capturing them needs a bounded LLM pass (~$95+).
- The one table wired to the tail (**Dialogue, $30**) is the **lowest-yield (#4)** per the recall judgment → likely low ROI.

So **1a-as-built gets A (64%) + Hospitality (~free), NOT the full ~92%** the recall sample implied — because the recall sample assumed *all* of B is mineable, but most of B lives in prose-shaped tables. The remaining recall is an explicit LLM cost decision, and the recall sample says spend it on Events/Info, **not** Dialogue.

## Spot-check (caught a bug the tests didn't)

Read the Red Wedding output (`asos-catelyn-07.extra-tables.jsonl`):
- **Correct:** `GUEST_OF` catelyn/edmure/robb → walder-frey (feast); grey-wind → walder-frey (refused); `VIOLATES_GUEST_RIGHT` walder-frey → robb/catelyn. Exactly the guest-right framing the recall sample flagged as easily lost.
- **Bug:** `walder-frey VIOLATES_GUEST_RIGHT all-for-joffrey` — "All for Joffrey" is the Freys' toast, resolved to a junk node. Same index-pollution misresolution class as the pending Track-1 resolver levers. The 529 new edges inherit the resolver's known endpoint-noise → need the endpoint filter before merge.

## Decisions / recommendations (proposed; Matt decides — all 2-3 are LLM extractions)

1. **Free, do-now:** merge the 529 Hospitality/VIOLATES edges into the canonical set *after* dropping bad-resolution endpoints (`all-for-joffrey` etc.) — folds into the Track-1 resolver-lever cleanup.
2. **Don't blanket-type Dialogue.** Smoke ~200 rows (~$1-2) first to measure typed-vs-just-conversation before the $30.
3. **The real recall lives in Events & Actions + Information Revealed (~14k rows).** A bounded LLM pass (each row = one scoped fact; far safer than open comention) recovers it at ~$95+. Genuine cost-vs-recall tradeoff — Matt's call.
4. **#2 — fast narrow wiki layer:** the wiki's structural edges (infobox fields) are ALREADY deterministic via `scripts/wiki-infobox-parser.py`; the only slow path was prose comention (DEPRECATED). "Fewer things" = extend the deterministic infobox-field→edge map to the unmapped fields (`dynasty`, `vassal`, `cadet branch`, `fathers`, `hatched`) — Python, not LLM.

## Carry-overs
- S67 + S68 work all **uncommitted** (Matt checkpoints via his own `wip` commits).
- Track-1 resolver levers, tail cleanup/dedup, and the canonical merge from the S67 finishing prompt are still open and now must also cover the 529 extra-tables edges.
