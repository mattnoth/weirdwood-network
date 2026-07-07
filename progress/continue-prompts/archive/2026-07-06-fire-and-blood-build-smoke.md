# SESSION 198 — Fire & Blood ingestion: build the pipeline + two-stage smoke

> **This is Session 198** (graph track). Stamp your worklog entry `### Session 198` at endsession.
> **Recommended model:** **Sonnet** for the build + orchestration (splitter / reconciler / harness are script-builder-class). The F&B *extraction worker itself* is a separate `claude -p` process — per the design's decision #3 it runs **Opus** for node-prose quality (that's the portfolio product). Do NOT run extractions yourself: they go through the weirwood/`claude -p` pipeline and are **Matt-fired from iTerm** (`feedback_no_extraction_without_asking`).
> **Gate:** building the pipeline is a go. Any **graph mutation / node writes** from the smoke needs Matt's explicit go on the smoke output first (`feedback_no_graph_mutation_without_goahead`). The architecture.md batch (below) also needs Matt's go — it lands WITH the first apply, not at build time.

## Where S197 left this (read these first)
- **Spec (execute this):** `working/fire-and-blood/fire-and-blood-enrichment-design.md` **v2** — top to bottom. §5 reconciler, §6 harness, §7 smoke, §10 sequencing, §11 rulings.
- **The S196 review of record:** `working/fire-and-blood/fable-review.md` (verdict GO-WITH-CHANGES; the 8 ranked risks R1–R8 — your build must honor their mitigations).
- **S197 delivered the reconciler's deterministic inputs** (its dependency, design §5.0/§5.1):
  - `working/wiki/data/same-name-clusters.json` — per-cluster discriminators (parents/spouse/born-died/regnal/era/title).
  - `working/wiki/data/disambig-node-blocklist.json` — **236 trap nodes**, `trap_kind`-tagged (39 disambiguation + 197 redirect).
  - `working/wiki/data/redirect-node-map.json` — redirect-slug → canonical target slug.
  - `disambiguation_hub: true` / `redirect_to:` frontmatter now live on the trap/redirect nodes (documented in `reference/architecture.md` §Node Frontmatter).

## The load-bearing hand-off (S197 verified live)
`weirwood query resolve "Aegon Targaryen"` STILL returns a confident `HIT` on the trap node `aegon-targaryen`; `"Aenys Targaryen"` HITs the redirect node. **The raw resolver does not honor the blocklist/redirect-map/hub flags.** So **F&B step 1 = make the reconciler consult them**: a resolver hit that is blocklisted OR in a same-name cluster is routed as *ambiguous* (discriminator scoring, ≥2-independent-discriminator auto-accept — design §5.1 / ruling #5), and a `redirect_to` hit resolves to its target. This is the S196-R1 confident-wrong-match mitigation. Without it the pass silently pours Aegon II content onto trap nodes.

## Build order (design §10)
1. **Reconciler resolution core** — consumes the three S197 files + `disambiguation_hub`/`redirect_to`. Tiered auto-accept (ruling #5); trap/cluster hits → review. Unit-test against the known traps (`aegon-targaryen`, `aenys-targaryen`).
2. **`fab` chapter splitter** — `scripts/` (reuse the D&E splitter shape). Output `sources/chapters/fab/`. **QA-gate then FREEZE** `sources/chapters/fab/` (append-never-modify — cite_refs are line-anchored; a re-split after extraction is a provenance-breaking event; design ruling #2/#6).
3. **`fab_merge_node.py`** — the NEW merge writer (design §5.3; mint SKIPS existing nodes per C1, so UPDATEs need this or they silently drop — R3). Additive `## Fire & Blood` section + boilerplate-Identity swap + insert-if-absent + idempotency marker. Handle the three node shapes (C2). Consider sharing a `node_merge_lib.py` with the S197 composer's writer.
4. **Quote pre-validation** (design §5.2 / R2) — reconciler `norm()`+grep every evidence_quote BEFORE mint; unlocatable → `quotes-review.jsonl` row-level quarantine, never abort the unit.
5. **Two-stage smoke (design §7 / ruling #7), Matt-fired from iTerm:** Stage 1 = `fab-aegons-conquest-01` (003) — small/clean, proves splitter/worker/harness/reconciler plumbing (also the FIRST end-to-end run of the D&E-shaped `claude -p` + `longrun.sh` pattern — R6; expect harness bugs, budget a fix loop). Stage 2 = `fab-heirs-of-the-dragon-15` — the ambiguity/dispute/density quality test.

## architecture.md batch (Matt's go; lands WITH the first apply, per rule #6)
Still staged from S196 (S197 already landed the `disambiguation_hub`/`redirect_to` slice): the **`fab` book code** + **`evidence_kind: book-fab`** + edge fields **`in_universe_source`** (enum incl. `orwyle`/`unattributed`) + **`disputed`** (invariant: `disputed ⇒ tier ≤ 2`). Log the Active Decision in `worklog.md` when it lands.

## DO NOT
- Do NOT run/launch extractions yourself — Matt fires the smoke from iTerm; you build + propose the command.
- Do NOT write `graph/nodes/` or `edges.jsonl` from the smoke without Matt's go on the output.
- Do NOT re-split/modify `sources/chapters/fab/` after the QA-gate freeze.
- Do NOT re-fetch the wiki (`feedback_no_external_wiki_fetch`) or auto-run /endsession.
