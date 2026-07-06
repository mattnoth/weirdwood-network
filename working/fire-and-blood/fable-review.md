# Fable design review — Fire & Blood enrichment plan + wiki-prose disambiguation companion

> **Reviewer:** Fable (claude-fable-5), 2026-07-06, per `fable-review-handoff.md`.
> **Grounding actually read:** both design docs; `architecture.md` (tiers ~:566, edge metadata, `occurred:`/`basis_reliability`/`dispute` ~:500, `era:` conventions); `edge-qualifier-vocab.md`; D&E `pass1-prompt-v4.md`; `longrun.sh`; `mint_enrichment.py`; `finalize_enrichment.py`; `dunk-egg-splitter.py`; live nodes (`rhaenyra-targaryen`, `aegon-targaryen-son-of-baelon`, `aegon-targaryen`); `edges.jsonl` (23,099 rows, evidence_kind histogram); `working/wiki/data/` (infobox-data, page-categories); live `weirwood query resolve` behavior; `worklog-dunk-egg.md` current state.
> **Scope note:** Matt widened the mandate this session — beyond critique, the accepted recommendations have been **applied into both design docs** (each now stamped *v2 — post-Fable-review*). This file is the review-of-record; the docs are the executable spec.

---

## 1. Verdict

**GO-WITH-CHANGES.** Node-first enrichment is the right shape — a mechanical Pass-1 would re-derive what the wiki layer already encodes (the wiki prose on these nodes is itself largely F&B-sourced; **1,634 nodes already carry `Rfab*` cite anchors**), while the actual gaps are exactly what node-first targets: navigable book cite_refs, distinguishing prose, and the causal/dispute texture.

**The single most important change:** §5.1's MATCH-first resolution is not currently safe to run — the live resolver returns a **confident exact HIT for "Aegon Targaryen"** onto `aegon-targaryen`, which is a **zero-edge junk node minted from the wiki's disambiguation page**. MATCH-first as drafted would pour Aegon II/III content onto trap nodes and silently cross-attach same-name Targaryens. The doc treated duplicate-minting as the failure mode; the worse and likelier failure is **confident wrong-match**. Fix = deterministic trap-node blocklist + cluster-aware routing + per-unit candidate packs (all specified in design v2 §5.0–5.1). This is also what makes the companion track genuinely load-bearing rather than nice-to-have — **run it first**.

---

## 2. Corrections to factual claims in the docs (verified against the code/data)

These matter because the plan's §5.3 risk analysis and the companion's §2 "data already on hand" claim were built on them.

| # | Doc claim | Reality (verified) | Consequence |
|---|-----------|--------------------|-------------|
| C1 | F&B §5.3: "`mint_enrichment.py` currently **overwrites** a node file by slug" | It does the opposite — **skip-if-exists** (`mint_enrichment.py:262-268` prints `SKIP node (exists)`). | There is **no data-loss path**, but also **no UPDATE path at all**: every UPDATE proposal would be **silently dropped**. The merge writer is a NEW component, not a patch to an overwrite. |
| C2 | F&B §1: existing F&B figures are "thin wiki-derived stub nodes" | Three distinct shapes exist: (a) true stubs (boilerplate Identity, nothing else); (b) **rich nodes** — `rhaenyra-targaryen` has ~90 lines of wiki-cited prose (Origins/Appearances/Narrative Arc/Quotes) under a boilerplate Identity line; (c) nodes with **no `## Identity` section at all** but real prose (`aegon-targaryen-son-of-baelon` starts at `## Origins`). ~2,753 character nodes carry the boilerplate line; ~545 have no Identity section. | The merge writer must handle all three shapes; "replace the Identity" is under-specified; on rich nodes the F&B prose must **not** displace the existing wiki prose (it's good, and its wiki cite anchors are the Tier-2 provenance layer). |
| C3 | F&B §5.3: overwrite "would destroy its existing track_b edges" | The infobox merge already shipped edges to `edges.jsonl` (16,757 `wiki-infobox` rows, run_id `infobox-merge-20260613/-0701`). Node-file `## Edges` sections are a display copy; the queryable graph would survive node-file damage. | Softens the stated risk, but the node files still hold the prose + frontmatter (aliases feed the resolver) — merge-not-overwrite still stands. |
| C4 | Companion §2: `aegon-targaryen-son-of-baelon` "already carries born 84 AC / died 85 AC … as edges" | **False.** That node has 6 edges (title/allegiance/culture/parents) — no birth/death data in node or `edges.jsonl`. | The composer can't assume dates are in the graph. **However** — the dates ARE available deterministically: `working/wiki/data/page-categories.jsonl` carries MediaWiki categories like `"84 AC births"`, `"85 AC deaths"` per page. That's the composer's date source (design v2 fixed). |
| C5 | Both docs: "~12 `aegon-targaryen-son-of-…` nodes" | Actual: 6 `son-of-*` + `young-griff` + bare `aegon-targaryen` (disambig trap) + `aegon-i…v-targaryen` = **13 Aegon-Targaryen-named character nodes**. Order of magnitude right; the important miss was the **bare-name trap node**, which neither doc mentioned. | Bare-name disambiguation-page nodes exist for Aegon, Aemon, Baelon, Daeron, Jaehaerys, Rhaena (verified in `page-categories.jsonl`: category `Disambiguation pages`) — every one is a confident-exact-hit trap for the resolver. |

---

## 3. Per-decision rulings (F&B §11, items 1–10)

| # | Decision | Ruling | Rationale / where the doc's lean was wrong |
|---|----------|--------|--------------------------------------------|
| 1 | UPDATE merge semantics | **A+, as a new script** (`fab_merge_node.py`): additive `## Fire & Blood` section + swap of the one boilerplate Identity line (exact-regex-matched) + insert-Identity-if-absent + idempotency marker. **Reject B for the bulk run** — on rich nodes (C2b) a full Identity rewrite would displace good wiki-cited prose and its Tier-2 anchor layer. B-by-hand for Dance principals stays, as ordinary post-run curation dips. The doc's framing "mint needs `--merge`" was wrong per C1 — this is a new component with its own §0 row and smoke. |
| 2 | Unit granularity | **Accept 8–12K, cap the Dance core at ~10K.** Files 005/014/015/017 get the finer cut. Sub-split threshold 15K OK. One addition: **freeze `sources/chapters/fab/` after the QA gate** — cite_refs are line-anchored, so a re-split after extraction starts is a provenance-breaking event (see #6). |
| 3 | Node-prose vs slim | **Keep `## Node Prose`, with a budget rule:** 2–5 sentences for the unit's ~10–15 entities of substance, one line for the rest, nothing for pure mentions. "Let the UI compose prose" is a false economy — the node prose IS the portfolio product (HotD motivation, §Purpose), and Opus output tokens are the cheap part of this run. |
| 4 | Lineages appendix (025) | **Deterministic parse, but reframed: it is a *validation corpus*, not an edge source.** The infobox merge already carries the genealogy (16,757 edges incl. dense PARENT_OF/SPOUSE_OF). Parse the appendix → diff against existing kinship edges → three buckets: **confirm** (no action; optionally log), **new** (route to review with an OCR-suspicion flag — never auto-mint kinship from OCR'd tables), **conflict** (route to the contradictions report). Expected new-edge yield is low; expected *error-catch* yield (wiki vs book disagreements, OCR tells) is the real value. No Opus. |
| 5 | Reconciler ambiguity policy | **Tiered auto-accept.** Auto-accept ONLY: exact/alias hit AND not blocklisted AND not in a same-name cluster. Cluster members go through discriminator scoring (parents/spouse/regnal/era/section-prior); auto-accept a scored match only when the top candidate is supported by **≥2 independent discriminators** AND the runner-up margin is decisive; else review. Bias to review during smoke; tune thresholds only on out-of-sample units (`feedback_fresh_review_and_out_of_sample`). |
| 6 | cite_ref granularity | **Section-level line anchors sufficient** — consistent with all 344 existing chapters; the deterministic quote→line locator re-derives lines from verbatim quotes anyway, so the *quote* is the durable anchor. Paragraph ids = overengineering. The real requirement is the **freeze rule** (#2): after QA-gate pass, `sources/chapters/fab/` is append-never-modify, like every other chapter dir. |
| 7 | Smoke unit | **Two-stage smoke, not one.** Stage 1: `fab-aegons-conquest-01` (003) — small, clean, proves splitter/worker/harness/reconciler plumbing (and is the first-ever completed run of the D&E-shaped `claude -p` + `longrun.sh` pattern — see risk R6). Stage 2: `fab-heirs-of-the-dragon-15` — the ambiguity/dispute/density stress test, judged for quality. The doc's single dense smoke conflates two failure classes that are cheaper to isolate. |
| 8 | `fab` code | **Accept.** Decisive extra argument the doc missed: the wiki's own F&B cite anchors are literally `Rfab<section_slug>` — the graph's existing Tier-2 provenance layer already uses this code. Update architecture.md §File Naming in lockstep (CLAUDE.md rule #6) + worklog Active Decision. |
| 9 | In-universe provenance | **Claim-by-claim (doc's lean is right); blanket per-source ceiling is wrong** — Gyldayn synthesizes across sources and even Mushroom is sometimes reporting uncontested fact; a source-level cap throws away exactly the account-vs-account texture Matt wants captured. **Make both REAL schema fields**, not note strings: optional edge fields `in_universe_source` (enum) + `disputed: bool` in `edges.jsonl`, validated; prose claims carry the attribution inline in the text ("According to Mushroom, …"). Enum needs two additions the doc missed: **`orwyle`** (Grand Maester Orwyle's account is a primary named source for the Dance) and **`unattributed`** (bare "some say / it is said" is not `gyldayn-synthesis`). Validator invariant: `disputed: true` ⇒ tier ≤ 2 (reject tier-1+disputed). This slots cleanly under the existing tier table — same pattern as the `occurred.dispute` staging at architecture.md:504 and the SUSPECTED_OF tier-cap precedent. |
| 10 | Sequencing vs companion track | **Companion first — but restructured to make the dependency real.** As drafted, the companion only helps *humans reading review files*: the deterministic reconciler never reads Identity prose. Fixed in companion v2: its deterministic step now emits a machine-readable **disambiguation pack** (`same-name-clusters.json`: per-cluster, per-slug discriminators — parents, born/died years from page-categories, era, key title) that F&B's reconciler consumes directly, plus the human-readable Identity lines composed from the same pack. Composer is pure Python — it can run this week; F&B splitter build can proceed in parallel; F&B *extraction* gates on the pack existing. |

---

## 4. Ranked risks (most → least severe), each with failure scenario + mitigation

**R1 — Confident wrong-match in MATCH-first resolution (severity: graph corruption, silent).**
Scenario: unit 016 rosters "Aegon Targaryen" (meaning Aegon II); `weirwood query resolve` returns `HIT` on the disambig-derived junk node `aegon-targaryen` (verified live); reconciler routes UPDATE; Aegon II's biography and KILLS/CLAIMS edges land on a contentless trap node — and nothing errors. Variants: "Prince Aegon" in a Jaehaerys section is Aegon-son-of-Baelon, in a Dance section Aegon II or III; Gyldayn habitually uses bare first names.
Mitigation (design v2 §5.0–5.1): (a) deterministic **blocklist** of disambiguation-page-derived nodes (page-categories `Disambiguation pages` ∩ node wiki_source) — a blocklisted hit is *always* routed as ambiguous; (b) **same-name cluster registry** from the companion pack — any hit on a cluster member requires discriminator scoring regardless of resolver confidence; (c) **per-unit candidate packs** from `Rfab` cite anchors (deterministic prior: the 221 nodes whose wiki prose cites "heirs of the dragon" are the expected roster of unit 15); (d) prompt-level: roster carries a mandatory **Disambiguator column** (parent/spouse/regnal/epithet as the text gives it).

**R2 — Whole-unit mint aborts on one unfindable quote (severity: operational, guaranteed to fire).**
Scenario: extractor silently "fixes" `che Dragon` → `the Dragon` in one evidence_quote out of 60; `mint_enrichment.py:authoritative_line` fail-fast `sys.exit`s the entire unit's candidates.json; with OCR-noisy source across ~30 units this fires repeatedly and each firing blocks a whole unit at the most expensive point in the pipeline.
Mitigation (design v2 §5.2): reconciler **pre-validates every quote** with the same `norm()`+grep before mint; unlocatable quotes are split out to `quotes-review.jsonl` (row-level quarantine) instead of poisoning the unit; prompt rule strengthened: *quote the file text verbatim even when garbled* — canonical-spelling notes go in the roster column, never inside the quote string.

**R3 — Silent UPDATE-drop (severity: the pass quietly doesn't happen).**
Scenario: per C1, mint skips existing nodes; if the merge writer isn't built (or a candidates.json routes UPDATEs through the CREATE path), the run "succeeds" while ~70% of its value (the UPDATE overlays) is never written. Nobody notices until someone opens Rhaenyra's node.
Mitigation: `fab_merge_node.py` is a first-class §0 component with its own smoke + idempotency marker; the apply step's summary must report `nodes merged / created / skipped` counts and **skipped-with-UPDATE-payload is a hard error**.

**R4 — Dispute/tier mis-tagging in both directions (severity: data quality, subtle).**
Scenario A (inflation): a hedge lives two sentences before the claim ("*Mushroom tells it differently.* … Daemon then …") — extractor emits the claim untagged → false Tier-1. Scenario B (deflation): extractor over-triggers on every "it is said" → half of F&B lands `disputed`, gutting the Tier-1 upgrade that is the pass's point.
Mitigation (design v2 §7): the fresh-verify sample is **stratified on this axis** — it must include N tagged-disputed and N untagged-Tier-1 claims from Dance units specifically, checking hedge-scope in ±10 lines; both mis-directions are counted and gate the bulk run.

**R5 — OCR-corrupted kinship from the Lineages appendix (severity: high if #4 ruled wrong).**
Scenario: `Jaehaerys | Targaryen`-class garbling in a genealogy table → deterministic parse emits a wrong PARENT_OF → poisons kinship traversals used by everything downstream (incl. the companion composer and the F&B reconciler's discriminators).
Mitigation: ruling #4 — appendix is a validation corpus; **no auto-minted kinship edges from OCR'd tables**; new/conflicting rows go to review only.

**R6 — The long-run harness pattern has never completed a unit (severity: schedule, not data).**
Scenario: F&B §6 says "reuse the D&E track's exact shape" — but D&E Pass-1 is still at *smoke-attempted, auth-blocked* (worklog-dunk-egg: DE-1/DE-2; zero completed extractions of the `claude -p` worker under `longrun.sh`). F&B inherits unproven glue: prompt-file resolution, `{HARVEST_PATH}` plumbing, exit-code contract in the worker, telemetry rows.
Mitigation: stage-1 smoke (#7) explicitly doubles as the pattern's first end-to-end proof; if the D&E smoke lands first, harvest its lessons before the F&B bulk; expect harness bugs at smoke-time and budget a fix loop.

**R7 — Contradiction-blind edge accretion (severity: consistency).**
Scenario: F&B (book) says X disputed/different where the wiki infobox asserted it flat — e.g. differing spouse ordering, a parentage F&B hedges. New book-cited edge is appended; the old wiki-infobox edge stays; the graph now asserts both with no cross-reference, and the chat-UI surfaces whichever it hits first.
Mitigation (design v2 §5.4): deterministic post-reconcile diff of proposed F&B kinship/allegiance/title edges vs existing `wiki-infobox` edges on the same source node → `contradictions-report.md` for review (duplicate-triple-with-better-evidence is fine and expected — that's the Tier-1 overlay working; *conflicting-target* triples are what get flagged).

**R8 — Harvest queue re-balloon (severity: process debt).**
Scenario: ~30 units × harvest sidecar lines rebuilt the 0→149 pile the S153–S156 lapse produced.
Mitigation: a scheduled drain is part of the run plan (design v2 §10), not left to endsession happenstance.

---

## 5. Missing considerations (completeness critic) — now applied to design v2

1. **Rollback & idempotency had no story.** Now specified (§8): git-commit checkpoint before each apply batch; per-unit `run_id` (`fab-<slug>-NN-<date>`) so the existing re-run guard gives unit-level idempotency; merge writer stamps `<!-- fab-enriched: <run_id> -->` and skips on re-run; per-run-id revert = edges backup (already exists) + `git checkout` of touched node files.
2. **`era:` stamping was absent.** New mints must stamp `era:` (architecture.md forward-only convention). Deterministic: NCX section → era map (001–014 `targaryen-rule` / conquest sections `targaryen-conquest` / 015–019 `dance-of-dragons` / 020–024 `targaryen-rule`). Zero LLM cost.
3. **`occurred.ac_year` for new event nodes was absent.** Gyldayn dates everything; the Events table now carries a `year (AC)` column; reconciler stamps `occurred:` blocks (`basis_source: narrative-prose`, `basis_reliability: primary-source`) — materially better than the existing tertiary-fan/tier-3 wiki-year dating.
4. **`meta.chapter` nodes:** the graph has 344 chapter nodes; whether fab units mint them (and what consumes them) is now an explicit open item rather than an implicit gap.
5. **Observability:** per-unit summary JSONL (entities rostered / matched / ambiguous / created; edges by type; quote-location rate; NEEDS_VOCAB count; disputed-tag rate) — these are the gate's inputs and the drift alarm (a unit whose quote-location rate drops to 60% is an OCR hotspot; a unit with 0 disputed tags in the Dance core is a prompt failure).
6. **Duplicate-edge policy made explicit:** same (type, source, target) with `evidence_kind: book-fab` alongside an existing `wiki-infobox` row is **intended** (the Tier-1 overlay), not a dedup bug; queries prefer max-tier evidence. Stated in §5.4 so nobody "cleans it up" later.
7. **Cost-ballooning modes named (E):** the estimate (~$40–80 one-time at current Opus list) is sane; the three balloon risks are (a) whole-unit re-extraction to fix quote failures — capped by R2's row-level quarantine, (b) sub-split creep in the Dance core (34 → 40+ units — accept, it's linear), (c) review-bucket human time, which is the real bottleneck and exactly what the companion pack shrinks. Verify arm on Haiku ≈ noise. The §9 numbers hold if R2's mitigation ships; without it, budget 1.5–2× for re-runs.

---

## 6. Companion-track assessment (wiki-prose disambiguation)

**Sound, genuinely cheap, correctly identified as a de-risker — but as drafted it de-risked less than claimed, and one of its two "verified" data claims was false.**

- **Sequencing: FIRST.** Confirmed, with the restructure (ruling #10): its deterministic output is now the machine-readable disambiguation pack that F&B's reconciler consumes. Without that, the deterministic matcher never benefits — only human reviewers do.
- **C4 correction:** born/died are *not* in the graph as edges. The fix is better than the original claim: `page-categories.jsonl` categories (`"84 AC births"`, `"85 AC deaths"`) give **deterministic life-dates for every character page** — no HTML parsing, no LLM. Composer field priority is now: dates (categories) → parents (infobox-data relationships) → allegiance/title (infobox-data) → era.
- **Missed entirely, now added:** the **disambiguation trap nodes** (bare `aegon-targaryen` etc., minted from `Disambiguation pages`). The companion is the natural place to fix them: stamp `disambiguation_hub: true` frontmatter + an Identity line listing cluster members. That single change gives the F&B reconciler its blocklist for free and turns the traps into navigation aids for the chat-UI.
- **Node-shape blindness fixed:** the composer must handle boilerplate-Identity, rich-prose-with-boilerplate-Identity (touch ONLY the one line), and no-Identity-section (insert) — same three shapes as C2.
- **Open questions ruled:** composer-only for v1 (Haiku residue only if smoke shows >20% of cluster members still indistinguishable); disambiguation pointer = frontmatter field + Identity prose line; cluster key = (first-name, surname) after stripping regnal numerals/parentheticals — cross-house first-name collisions were a non-problem the doc over-worried.
- **Cost:** as claimed — one Python script + a bounded review. The only spend is the optional Haiku residue.

---

## 7. What was applied where

- `working/fire-and-blood/fire-and-blood-enrichment-design.md` → **v2**: C1–C3/C5 corrections; §5.0 candidate packs; §5.1 hardened resolution algorithm; §5.2 quote pre-validation; §5.3 merge-writer spec; §5.4 contradiction diff + duplicate policy; §7 dispute-axis audit; §8 rollback/idempotency; §9 balloon modes; §10 re-sequenced; §11 rulings recorded; §0 component table extended.
- `working/node-enrichment-wiki-prose/design.md` → **v2**: C4 correction + page-categories date source; disambiguation-pack output; trap-node handling; three node shapes; cluster algorithm; execution plan with acceptance criteria for a cheap agent.
- **Not done (still gated on Matt):** anything build- or graph-touching; architecture.md edits (they land with the `fab` Active Decision when Matt approves the plan); worklog updates (session close-out).
