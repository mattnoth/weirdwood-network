# Handoff — Fable design review of the Fire & Blood enrichment plan

> **Recommended model:** Fable (`claude-fable-5`) — this is a reasoning/design-analysis task, no code execution.
> **Mode:** DESIGN REVIEW ONLY. Nothing here is built or approved. Do **not** build, split, extract, or mutate the graph. Produce an analysis, not an implementation.
> **How to fire:** open a Fable session at the repo root and say *"Read `working/fire-and-blood/fable-review-handoff.md` and execute it."*

---

## Your role

You are **Fable**, doing an adversarial-but-constructive design review of two design docs for the **Weirwood Network** (a structured ASOIAF knowledge graph; ~8,700 nodes / ~23,000 edges, currently in an enrichment phase, feeding a chat-UI alpha). Matt wrote the plan with Claude (Opus 4.8) and wants your independent read **before** any of it is built. Your job is to pressure-test it: find the flaws, judge the trade-offs, recommend on the open decisions, and catch what's missing. Be direct — a rubber-stamp is useless here.

## The work being reviewed

A long-running **Opus 4.8** extraction pass over **Fire & Blood** (the Targaryen history book; ~264K words, no POV structure, in-universe narration by Archmaester Gyldayn). The graph already holds most F&B figures as **thin wiki-derived stub nodes** (boilerplate Identity, wiki-infobox-only edges, no book citations), so the pass is **~70% UPDATE / 30% CREATE**: overlay real book-grounded prose + navigable book cite_refs onto the existing dynasty layer, mint nodes for what's genuinely new, wire book-cited controlled-vocab edges. Framing was decided as **node-first enrichment** (not a full mechanical Pass-1). A companion track proposes cheaply giving same-name nodes (~12 Aegons, many Daerons/Aemons) distinguishing Identity prose.

## Read these, in order

**Primary (the docs under review):**
1. `working/fire-and-blood/fire-and-blood-enrichment-design.md` — the main plan. Pay closest attention to: §1.1 (in-universe provenance / confidence), §3 (splitter + OCR handling), §4 (the node-first prompt schema), §5 (reconciliation — MATCH-first + the §5.3 merge gap), §6 (harness), §7 (verify/drift gates), §11 (the 10 open decisions).
2. `working/node-enrichment-wiki-prose/design.md` — the companion disambiguation track.

**Grounding (so your critique is concrete, not abstract):**
3. `reference/architecture.md` — esp. the **Confidence Tiers** table (~line 566), the **Edge Types** vocabulary, and the event-dating schema's `basis_reliability`/`dispute` fields (~line 500). The plan's confidence scheme must fit this.
4. `reference/edge-qualifier-vocab.md` — the qualifier enums the prompt must enforce.
5. `working/dunk-egg-pass1/prompts/pass1-prompt-v4.md` — the closest existing analog (non-POV book, locked-vocab relationships, harvest sidecar, SAME_AS reveals). Judge whether the F&B prompt correctly borrows vs. diverges.
6. `scripts/longrun.sh` (the supervisor exit-code contract), `scripts/mint_enrichment.py` + `scripts/finalize_enrichment.py` (the apply path — confirm the §5.3 overwrite-vs-merge claim is accurate), and `scripts/dunk-egg-splitter.py` (splitter template).
7. A live stub node to see what "UPDATE" acts on: `graph/nodes/characters/rhaenyra-targaryen.node.md`.

## Answer these

**A. Plan-shape verdict.** Is **node-first enrichment** the right framing for a history book whose entities mostly already exist, or would a different shape (mechanical-Pass-1-first, or a hybrid) serve better? Give a go / go-with-changes / no-go on the overall approach.

**B. Rule on each of the 10 open decisions in F&B §11.** For each, state your recommendation + one-sentence rationale. Flag any where the doc's lean is wrong. The ones that matter most:
- **§11 #1 — UPDATE merge semantics (§5.3).** The single biggest correctness risk: `mint_enrichment.py` overwrites nodes by slug; blindly overwriting a rich wiki node destroys its edges + frontmatter. Is additive-section (option A) sufficient, or is the Identity-rewrite+edge-merge (option B) worth the complexity? Is there a third option?
- **§11 #9 — in-universe provenance / confidence (§1.1).** Is claim-by-claim `in_universe_source` + `disputed` tagging (Tier-1 uncontested Gyldayn / Tier-2 cap for hedged-or-partisan) the right model, or a blanket per-source ceiling? Should `in_universe_source`/`disputed` be real schema fields or note strings? Does this fit the existing tier framework cleanly?
- **§11 #10 + the whole second doc — sequencing.** Should the wiki-prose disambiguation track run **first / parallel / after**? How much does it actually de-risk F&B's MATCH-first reconciliation (§5.1)?
- **§11 #4 — the Lineages/Family-Tree appendix.** Deterministic table-parse vs Opus pass, given genealogy OCR errors can corrupt kinship edges.

**C. MATCH-first robustness (§5.1).** Is the resolver's match/ambiguous/create routing strong enough to prevent duplicate-node minting (`rhaenyra-targaryen-2`) across ~12 same-name Targaryens? What would you add?

**D. Completeness critic.** What's **missing** from the plan? Consider at least: failure/rollback if a bulk run half-completes; idempotency of re-runs; how conflicting F&B accounts interact with edges that *already exist* from the wiki (does F&B contradict an infobox fact?); handling of the OCR noise beyond the splitter; whether the verify/drift gate (§7) is proportionate; observability/telemetry gaps; and anything in the confidence model that could silently inflate or deflate tiers.

**E. Cost/effort realism.** Is the §9 estimate (~30–34 units, order-of-tens-of-dollars one-time) sane? Where's the risk of it ballooning?

## Output

Write your review to **`working/fire-and-blood/fable-review.md`** with:
1. **Verdict** — one line: go / go-with-changes / no-go on the plan shape, + the single most important change.
2. **Per-decision table** — each F&B §11 item (1–10): your call + rationale + (if applicable) where the doc is wrong.
3. **Ranked risk list** — most-to-least severe, each with a concrete failure scenario and a mitigation.
4. **Missing considerations** — the completeness-critic findings (D).
5. **Companion-track assessment** — is the wiki-prose disambiguation track sound, cheap as claimed, and correctly sequenced?

Cite doc section numbers. Don't rewrite the design docs — critique them. If you need a fact from the codebase to judge a claim, read it rather than assume.
