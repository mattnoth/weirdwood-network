# Deterministic-First Orchestration — Recon Findings

*Raw material for (a) the whitepaper "Deterministic-First Orchestration: Running Agents Across Long Batches" and (b) a pytest smoke-test suite Matt can own line-by-line. This is **recon, not a finished article and not a committed suite.** Decisions are flagged as Matt's.*

Compiled 2026-06-29. Five parallel read-only recon agents mapped the subsystems; every load-bearing number and the central code citations below were re-verified against the live repo by the orchestrator. Provenance of each claim (verified-by-me vs reported-by-subagent vs inferred) is tagged inline and summarized in the appendix.

---

## 0. Read this first — three honest corrections to the brief

The investigation prompt makes three assumptions that the code contradicts. Surfacing them rather than papering over, because they change the article and the suite:

1. **There is no SQLite schema.** The data store is two flat layers: `graph/nodes/<type>/<slug>.node.md` (markdown + YAML frontmatter, **8,729 files** ✅verified) and a single monolithic **`graph/edges/edges.jsonl`** (**23,330 rows, 17.8 MB** ✅verified). The chat-UI export ([scripts/build-chat-export.py](scripts/build-chat-export.py)) compiles those into compact JSON bundles. So "referential integrity against the schema" means *JSONL-row schema + node-frontmatter schema + slug cross-references*, not SQL constraints. This is **better** for the article — the "schema" is an informal contract that the agent can violate in more ways, which is exactly the point.

2. **A substantial test suite already exists — and it is currently RED.** `tests/` holds **28 files / 1,325 collected tests** ✅verified. The job is *gap-finding + a focused smoke layer*, not greenfield. And right now [tests/test_validate_edge_jsonl.py:31](tests/test_validate_edge_jsonl.py:31) **fails**: it asserts exactly `167` canonical edge types; `reference/architecture.md` now yields **170** ✅verified. That failing assertion is the single best teaching artifact in the repo (see §5, §6, §8) — keep it.

3. **The thesis number ("~18,000 items") is real but needs precision.** The corpus is **17,657 cached wiki pages** ✅verified. The agent fan-out doesn't run once per page — it runs over **6,302 candidate files** (5,686 `source_target` + 344 `comention` + 272 `pass1_relationship` ✅verified), each holding many candidate *rows*. "~18k" is the right order-of-magnitude headline; the honest body text is "a 17.6k-page corpus, decomposed into thousands of candidate files holding tens of thousands of metered classification decisions."

**The one number that proves the thesis:** of the 23,330 edges in the live graph, **16,987 (72.8%) were produced deterministically** (`evidence_kind=wiki-infobox`, from the Stage-3a Python emitter at ~$0) ✅verified. The metered LLM was spent only on the ~27% that genuinely required reading prose. Deterministic-first isn't a slogan here; it's most of the graph.

---

## 1. The pipeline — deterministic vs. agentic step inventory

Two distinct orchestration shapes live in this repo. The article should name both and anchor on the first.

- **Shape A — volume / fan-out** (Wiki Pass 2 + Stage 4): many independent, mechanically-checkable items; the article's "agents across long batches."
- **Shape B — judgment / dip-loop** (enrichment): small batches, adversarial verify, re-probe. Matt already wrote this one up in [PORTABLE-PLAYBOOK.md](PORTABLE-PLAYBOOK.md), which *explicitly* contrasts the two ("Fan-out wins on volume … this loop wins on judgment. Know which you have."). See §8 for why this distinction is the article's strongest framing device.

### 1a. Macro pipeline (whole-corpus)

| # | Step | Class | Where | Notes |
|---|------|-------|-------|-------|
| 1 | Chapter split (.txt → per-chapter .md) | **DET** | [scripts/chapter-splitter.py](scripts/chapter-splitter.py) | 347 chapter files |
| 2 | Pass 1 mechanical extraction | **LLM** | `mechanical-extractor` agent, via `weirwood` pipeline | All 5 books; produces `## Relationships Observed` tables → later become `pass1_relationship` candidates |
| 3 | Wiki crawl (one-time) | DET (archived) | `scripts/archive/` (do not restore) | 17,657 JSON pages cached; never re-fetched |
| 4 | Pass 2 Stage 1 — core node promotion | **LLM** | `wiki-ingester` agent | 855 agent-promoted nodes (37 buckets) |
| 5 | Pass 2 Stage 3a — skeleton emit | **DET** | [scripts/wiki-pass2-emit-deterministic.py](scripts/wiki-pass2-emit-deterministic.py) | frontmatter + infobox `## Edges`; **$0 / ~14s for 3,315 pages** |
| 6 | Pass 2 Stage 3b — prose extract | **DET** | [scripts/wiki-pass2-extract-prose.py](scripts/wiki-pass2-extract-prose.py) | HTML→md via static h2→heading table; $0 |
| 7 | Pass 2 Stage 3-promote — concat + atomic-rename | **DET** | [scripts/wiki-pass2-promote.py](scripts/wiki-pass2-promote.py) | single-writer-per-file; conflict-detect to `_conflicts/` |
| 8 | Stage 4 — prose-edge classification | **LLM** | [scripts/stage4-haiku-run.py](scripts/stage4-haiku-run.py), [scripts/stage4-tail-classifier.py](scripts/stage4-tail-classifier.py) | the long metered batch — detailed in §1b |
| 9 | Stage 4 post-validation | **DET** | [scripts/wiki-pass2-validate-edge-jsonl.py](scripts/wiki-pass2-validate-edge-jsonl.py), [scripts/stage4-type-contract-validator.py](scripts/stage4-type-contract-validator.py), [scripts/wiki-pass2-flag-suspicious-edges.py](scripts/wiki-pass2-flag-suspicious-edges.py) | the trust boundary — §3 |
| 10 | Edge merge → `edges.jsonl` | **DET** | mint/finalize scripts ([scripts/finalize_enrichment.py](scripts/finalize_enrichment.py), [scripts/mint_enrichment.py](scripts/mint_enrichment.py)) | run_id-stamped, backup + double-apply guard |
| 11 | Index / alias rebuild | **DET** | [scripts/build-entity-indexes.py](scripts/build-entity-indexes.py) | derived layer; rebuild after node mutation |
| 12 | Chat-UI export | **DET** | [scripts/build-chat-export.py](scripts/build-chat-export.py) | allowlisted JSON bundles, no LLM/network |
| 13 | Chat-UI tool-loop + cite-gate (runtime) | **LLM + DET gate** | [web/netlify/edge-functions/agent.ts](web/netlify/edge-functions/agent.ts) | live agent boundary — §3 boundary 7 |

> **Article gold (steps 5–7).** The Stage-3b redesign replaced an LLM "prose-fill" agent with a deterministic extractor: the runbook records the trade as **"$0/14sec instead of $70/6h"** and notes the structural payoff — *"The single-writer-per-file invariant … eliminates the agent-paraphrases-skeleton failure mode entirely."* ([working/runbooks/wiki-pass2-pipeline.md:5](working/runbooks/wiki-pass2-pipeline.md:5)) ✅verified. This is the cleanest "we deleted an agent and got cheaper *and* more correct" story in the repo.

### 1b. Micro loop — the Stage 4 batch engine (the article's spine)

This is the metered fan-out. The orchestrator owns *everything* deterministic; the agent is handed a thin classify-only prompt. From the module docstring: *"All bookkeeping lives here. The Haiku model receives only a thin classify-only prompt … No manifest access, no lock files, no state.jsonl, no resume logic inside the agent — this script owns all of that."* ([scripts/stage4-haiku-run.py:2](scripts/stage4-haiku-run.py:2)) ✅verified.

| # | Sub-step | Class | Function / citation |
|---|----------|-------|---------------------|
| 1 | Load batch manifest (read-only) | DET | `load_sonnet_manifest()` [stage4-haiku-run.py:119](scripts/stage4-haiku-run.py:119) |
| 2 | Route candidate → output path by **shape** | DET | `candidate_to_haiku_output()` [:67](scripts/stage4-haiku-run.py:67) — the 3-shape dispatch (§2) |
| 3 | Plan chunks, **skip-if-output-exists** | DET | `plan_batch_chunks()` [:584](scripts/stage4-haiku-run.py:584) |
| 4 | Render prompt — inject file-pairs + locked vocab | DET | `render_prompt()` [:316](scripts/stage4-haiku-run.py:316), `load_locked_vocab()` [:294](scripts/stage4-haiku-run.py:294) |
| 5 | **Invoke the model** (`claude -p`, stream-json) | **LLM** | `invoke_haiku()` [:410](scripts/stage4-haiku-run.py:410) |
| 6 | **Verify outputs** (inline smoke test) | DET | `verify_outputs()` [:334](scripts/stage4-haiku-run.py:334) — *parse-only + non-empty* |
| 7 | Retry loop (re-render only the bad pairs) | DET | `run_chunk()` [:494](scripts/stage4-haiku-run.py:494) |
| 8 | Detect rate-limit in the log | DET | `detect_rate_limit()` [:354](scripts/stage4-haiku-run.py:354) |
| 9 | Count decisions / assemble result | DET | `count_decisions()` [:473](scripts/stage4-haiku-run.py:473) |

**The exact LLM invocation** (✅verified, [:418](scripts/stage4-haiku-run.py:418)):

```python
cmd = ["claude", "-p", "--dangerously-skip-permissions",
       "--model", model, "--verbose", "--output-format", "stream-json", prompt]
```

LLM calls are **CLI subprocesses, not the SDK/API.** A sibling path ([scripts/stage4-tail-classifier.py](scripts/stage4-tail-classifier.py)) adds `cwd=/tmp` so the subprocess doesn't cold-load the repo's `CLAUDE.md` — recorded as **~49% cheaper per call** (memory + [stage4-tail-classifier.py](scripts/stage4-tail-classifier.py) docstring; ⚠️cost figure reported, not independently re-measured).

**`verify_outputs()` is the inline smoke test the article is about** — and it's deliberately shallow (✅verified, I read it):

```python
def verify_outputs(chunk_pairs):
    ok, bad = [], []
    for _, out_path in chunk_pairs:
        if not out_path.exists() or out_path.stat().st_size == 0:
            bad.append(out_path); continue
        try:
            for line in out_path.read_text().strip().splitlines():
                if line.strip(): json.loads(line)   # parse-ability only
            ok.append(out_path)
        except json.JSONDecodeError:
            bad.append(out_path)
    return ok, bad
```

It checks **exists + non-empty + every line parses as JSON** — and *nothing else*. No required fields, no vocab membership, no slug validity. Those live in a **separate deterministic stage** (§3). That split — cheap inline gate at the agent boundary, heavyweight schema validation downstream — is itself an article point: not every smoke test belongs in the hot loop.

> **Where a step *could* be more deterministic but isn't:** the two `claude -p` paths re-implement rate-limit detection, retry, and cost parsing independently ([stage4-haiku-run.py](scripts/stage4-haiku-run.py) `subprocess.Popen` stream-json vs [stage4-tail-classifier.py](scripts/stage4-tail-classifier.py) `subprocess.run` `--output-format json`). One shared "invoke-and-parse-claude" helper would remove a class of drift. Honest "what I'd refactor" note for the article.

---

## 2. The generic-wrapper pattern (one real example)

**The cleanest instance: one classifier path handles three structurally different candidate shapes, routed by a `candidate_kind` discriminator and fed an injected locked vocabulary.** The differences are *data*, not forked code.

**The injection mechanism** (✅verified, [stage4-haiku-run.py:316](scripts/stage4-haiku-run.py:316)) — a generic template with two placeholders; hard-fails if either is missing (a nice "fail-closed on a broken contract" detail):

```python
def render_prompt(chunk_pairs):
    template = CLASSIFY_TEMPLATE.read_text()
    pairs_block = "\n".join(f"{cand} -> {out.relative_to(REPO)}" for cand, out in chunk_pairs)
    if "%%FILE_PAIRS%%"  not in template: sys.exit("ERROR: template missing %%FILE_PAIRS%%")
    if "%%LOCKED_VOCAB%%" not in template: sys.exit("ERROR: template missing %%LOCKED_VOCAB%%")
    template = template.replace("%%LOCKED_VOCAB%%", load_locked_vocab())
    return template.replace("%%FILE_PAIRS%%", pairs_block)
```

The template itself is the generic body; placeholders are at [.claude/commands/stage4-haiku-classify.md:204](.claude/commands/stage4-haiku-classify.md:204) (`%%LOCKED_VOCAB%%`) and `:212` (`%%FILE_PAIRS%%`) ✅verified.

**The dispatch** distinguishes shapes by *path structure*, not config flags (✅verified, [stage4-haiku-run.py:67](scripts/stage4-haiku-run.py:67)): bucket prefix `meta-chapters-` → comention; bucket `extractions-pass1` → pass1_relationship; everything else → source_target.

**Two real candidate rows through the same path** (✅verified — pulled from disk, *not* reconstructed):

`source_target` — [characters-house-hastwyck/.../morgil-hastwyck.candidates.jsonl](working/wiki/pass2-buckets/characters-house-hastwyck/prose-edge-candidates/morgil-hastwyck.candidates.jsonl):
```json
{"candidate_kind":"source_target","source_slug":"morgil-hastwyck","source_section":"## Origins",
 "target_slug":"aemon-targaryen-son-of-viserys-ii","anchor_text":"Aemon the Dragonknight",
 "snippet":"...killed by her brother, Prince [LINK] ), in [trial by combat]...","backlink_count":61}
```

`pass1_relationship` — [extractions-pass1/affc/affc-samwell-04.candidates.jsonl](working/wiki/pass2-buckets/extractions-pass1/affc/affc-samwell-04.candidates.jsonl):
```json
{"candidate_kind":"pass1_relationship","evidence_chapter":"affc-samwell-04","evidence_book":"affc",
 "source_slug":"gilly","target_slug":"kojja-mo","asserted_relation":"trusts",
 "evidence_quote":"Gilly trusts Kojja with the babe; was afraid of her at first but now likes her",
 "extraction_file":"extractions/mechanical/affc/affc-samwell-04.extraction.md"}
```

Same four-decision gate (`emit_edge` / `reject_just_mention` / `escalate_cross_identity` / `escalate_disambiguation`), different evidence-reading path per `candidate_kind` ([.claude/agents/prose-edge-classifier.md](.claude/agents/prose-edge-classifier.md)).

**Where the abstraction leaks (be honest in the article):**
- The **output schema differs per shape** (comention carries `direction`; pass1 carries `evidence_quote`+`asserted_relation`; source_target carries `evidence_snippet`+`evidence_section`). One gate in, three row shapes out — so the *downstream validator* must itself branch on `candidate_kind` (`REQUIRED_FIELDS_BY_DECISION` keyed by the `(decision, candidate_kind)` pair, [wiki-pass2-validate-edge-jsonl.py](scripts/wiki-pass2-validate-edge-jsonl.py)). The wrapper unifies the *decision*, not the *schema*.
- A `reverse-direction-edge-belongs-on-other-node` special-case for kinship edges ([prose-edge-classifier.md](.claude/agents/prose-edge-classifier.md)) — domain knowledge the abstraction can't fully absorb.

**Two weaker examples** (mention, don't lead with): the parameterized enrichment minter ([scripts/mint_enrichment.py](scripts/mint_enrichment.py)) — *"the ONE script every enrichment dip uses … the only genuinely per-dip content is DATA"* — replaced ~33 near-identical per-dip scripts; and the mode-dispatch in [scripts/graph-query.py](scripts/graph-query.py) (`edge_types` frozenset injected per query mode). The minter is the better second example: it's the same pattern on the *write* side and the docstring states the rationale outright.

---

## 3. Trust-boundary inventory (where agent output meets deterministic code)

Seven boundaries. Each is a candidate smoke-test anchor (§5). Failure modes below are drawn from real validation code, assertion messages, and `# Session NN` comments; I verified the boundary *locations* and the live evidence-kind/resolution-status distributions, and tag the per-rule line numbers as ⚠️reported (subagent-sourced, robust to cite by function name even if line numbers drift).

| # | Boundary | Entry point | Guard today | Headline real failure modes |
|---|----------|-------------|-------------|------------------------------|
| 1 | Stage 4 JSONL emit → disk | `verify_outputs()` [stage4-haiku-run.py:334](scripts/stage4-haiku-run.py:334) | parse-ability + non-empty only | truncated/invalid JSON; empty file; missing output file |
| 2 | JSONL row → graph | `validate_edge_row()` [wiki-pass2-validate-edge-jsonl.py](scripts/wiki-pass2-validate-edge-jsonl.py) | full schema contract (~14 violation kinds) | missing required field; bad `confidence_tier` (string `"tier-1"` vs int `1`); stale `notes` field (deleted S57); `evidence_snippet` that's a bare section header |
| 3 | `edge_type` value | `load_canonical_vocab()` + normalizer ([stage4-haiku-normalize-edge-types.py](scripts/stage4-haiku-normalize-edge-types.py)) | locked vocab + alias table + difflib≥0.80 | invented types (`GRANDCHILD_OF`, `SUPERVISES`); tense variants (`TRAVELED_TO`→`TRAVELS_TO`); direction-unsafe synonyms (`FOSTERED_BY` ≠ `WARD_OF`) routed to unresolved log |
| 4 | `edge_type` + endpoint types | `type_contract_pass()` [stage4-type-contract-validator.py](scripts/stage4-type-contract-validator.py) | keep / drop / flip / retype / flag | `nights-watch MEMBER_OF jon-snow` (reversed → FLIP); `RULES` a person (→ retype `COMMANDS`); `CONTRACTED_WITH` a ship (→ drop) |
| 5 | emit rows (soft) | `check_patterns()` [wiki-pass2-flag-suspicious-edges.py](scripts/wiki-pass2-flag-suspicious-edges.py) | 6 soft-flag patterns (flag, don't drop) | `KNOWS` with no knowing-verb (fallback tell); `ATTENDS`/`FIGHTS_IN` a non-event; tier-3 with <20-char evidence |
| 6 | `target_slug` → node | `orphan-edges-audit.py` / `graph-conflict-pairs.py` | post-hoc audits (read-only) | dangling/hallucinated slug; alias mismatch; date-bleed (`BORN_AT → "298-ac"`); contradictory pairs (`LOVES`+`HATES` same direction) |
| 7 | Chat-UI prose cites → user | `verifyCites()` [agent.ts:253](web/netlify/edge-functions/agent.ts:253) | regex-extract cites, check against tool-returned allowlist | **fabricated chapter:line citation**; off-by-one line; `grounding==0`; `MAX_TOOL_ITERATIONS=6` loop-bound hit |

**Boundary 7 is the most article-ready single artifact** — small, modern, self-contained, and *designed to be testable without spend*. The module header says it outright: *"everything here is pure logic over the bound retrieval tools so it can be driven by a stubbed model in `deno test` (no API spend, no network)"* ([agent.ts:1](web/netlify/edge-functions/agent.ts:1)) ✅verified. `harvestResult()` builds the valid-cite allowlist from tool returns ([:201](web/netlify/edge-functions/agent.ts:201)); `verifyCites()` flags any `CITE_RE` match in prose not in that allowlist ([:253](web/netlify/edge-functions/agent.ts:253)); `dispatchTool()`'s comment names the philosophy — *"the trust boundary's far side: bad input yields data, never an exception"* ([:176](web/netlify/edge-functions/agent.ts:176)) ✅verified.

**Live-graph evidence that these boundaries are load-bearing** (✅verified distributions):
- `evidence_kind`: `wiki-infobox` 16,987 · `book-pass1` 5,179 · `book-pass1-reified` 895 · `derived-chronology` 167 · `plate4-wiki-cluster` 51 · `wiki-historical-anchor` 39 · `book-curator` 12.
- `target_resolution_status`: `resolved-exact-parens` 16,641 · `tail-llm` 1,394 · `resolved-exact` 1,320 · `resolved-alias` 428 · `?`(absent) 2,543 · … The **2,543 rows with no resolution status** and **1,394 `tail-llm` rows** are exactly the population a referential-integrity smoke test would scrutinize.
- *Note:* the live graph shows **no `wiki-entity` / `wiki-chapter-summary` edges** despite the classifier emitting those kinds — consistent with the memory that the wiki-comention path was **deprecated** in favor of the pass1-derived path. ⚠️Confirm against `worklog.md` before asserting this in print; it materially affects how you describe what Stage 4 *shipped* vs. what it *can* do.

---

## 4. Determinism / cost decisions already in the code (evidence the philosophy is practiced)

All ✅verified to exist; cost figures ⚠️as-recorded-in-repo unless noted.

1. **"Python before Agent" is a written default**, not a vibe — [working/runbooks/wiki-pass2-pipeline.md:9](working/runbooks/wiki-pass2-pipeline.md:9) and [reference/design-philosophy.md](reference/design-philosophy.md) (exists, 12 KB).
2. **Deleting an agent to save money + correctness:** Stage-3b prose-fill agent → Python extractor, "$0/14s instead of $70/6h" ([wiki-pass2-pipeline.md:5](working/runbooks/wiki-pass2-pipeline.md:5)).
3. **Single-writer-per-file invariant** eliminates the agent-paraphrase failure mode structurally (same runbook).
4. **Vocabulary lock-down injected at render time** so the prompt can't drift from the source of truth — `load_locked_vocab()` *"keeps a single source — the prompt never holds a hand-maintained copy that can drift"* ([stage4-haiku-run.py:294](scripts/stage4-haiku-run.py:294)). Out-of-vocab → rejected as `no-fitting-type-vocab-locked`, never an open question (avoids a human-in-the-loop re-run cycle).
5. **`cwd=/tmp` subprocess trick** to skip cold-loading `CLAUDE.md`, ~49% cheaper/call ([stage4-tail-classifier.py](scripts/stage4-tail-classifier.py)).
6. **Skip-if-output-exists** short-circuit for resumable, no-double-spend re-runs ([stage4-haiku-run.py:584](scripts/stage4-haiku-run.py:584)).
7. **Targeted retry** — re-render only the *bad* pairs, not the whole chunk ([stage4-haiku-run.py:530](scripts/stage4-haiku-run.py:530)).
8. **Generic long-run supervisor with a clean exit-code contract** ([scripts/longrun.sh:16](scripts/longrun.sh:16)) ✅verified by reading: `0`=done (stop), `2`=rate-limit wall (sleep `LONGRUN_WALL_SLEEP`=3600s, relaunch), `10`=progress+more (sleep `LONGRUN_SLEEP_BETWEEN`=1200s, relaunch), other=crash (sleep 300s; give up after `LONGRUN_MAX_CRASHES`=5). *Resume semantics belong to the supervised command, not the supervisor* — a clean separation worth a paragraph.
9. **Telemetry-driven sleep defaults**, not guesses — [scripts/pace.py](scripts/pace.py) computes recommended `LONGRUN_SLEEP_BETWEEN ≈ max(600, 2×median_unit_seconds)` from historical run logs (⚠️formula reported).
10. **Every mutation is a re-runnable script with backup + double-apply guard** ([mint_enrichment.py](scripts/mint_enrichment.py): `run_id` guard `ABORT: run_id already minted`).

---

## 5. Smoke-test target MENU (options + trade-offs — not a chosen design)

Candidate cheap deterministic checks on agent output, each mapped to a §3 boundary and a real failure mode. **Columns: what it catches · cost to build · false-positive/flakiness risk.** No recommendation — these are yours to pick from (§7).

| # | Candidate check | Boundary | Catches (real failure) | Build cost | FP / flake risk |
|---|-----------------|----------|------------------------|-----------|-----------------|
| A | **Every emitted line parses as JSON** | 1 | truncated/garbage agent output | trivial (mirrors `verify_outputs`) | ~none |
| B | **Required-fields-present per `(decision, candidate_kind)`** | 2 | agent omits `source_slug`/`evidence_snippet` | low (reuse `REQUIRED_FIELDS_BY_DECISION`) | low |
| C | **`confidence_tier` is int 1–3** | 2 | `"tier-1"` string drift | trivial | ~none |
| D | **No deprecated fields (`notes`)** | 2 | S57-era schema bleed | trivial | low (must track schema changes) |
| E | **`edge_type ∈ locked vocab`** | 3 | hallucinated/variant types | low | **medium — see drift caveat below** |
| F | **Type-contract: endpoint categories legal for `edge_type`** | 4 | `RULES` a person, reversed `MEMBER_OF` | medium (needs node-category index) | medium (depends on node store freshness) |
| G | **Referential integrity: `target_slug`/`source_slug` resolve to a node or alias** | 6 | dangling/hallucinated slug | medium (load node slugs + alias map) | medium (2,543 rows already lack status — expect noise) |
| H | **Dedup / idempotence: re-running a fixture batch yields no new/changed rows** | 1,10 | double-apply, non-deterministic merge | medium (fixture + run twice) | low if `run_id` guard works |
| I | **Soft-pattern sanity (KNOWS-without-verb etc.)** | 5 | LLM fallback tells | low (reuse `check_patterns`) | **high as a hard assert** — these are *flags*, not errors; only smoke-test that the flagger *fires*, not that data is clean |
| J | **Cite-gate: fabricated citation rejected** (TS/Deno) | 7 | hallucinated chapter:line | low (stub model, no spend) | ~none — pure function |
| K | **Cross-count invariant: emitted edges == decisions counted** | 1,9 | silent row loss in parse/merge | low | low |
| L | **Vocab-count *direction* check (monotonic / ≥ floor), not exact** | 3 | the §6 RED test's brittleness | trivial | **this is the fix for E's caveat** |

**The E/L trade-off is the heart of the validation section.** The existing [tests/test_validate_edge_jsonl.py:31](tests/test_validate_edge_jsonl.py:31) hard-codes `== 167` and is **failing at 170 right now**. Options, with the trade you're buying:
- **Assert exact count** — catches *any* drift incl. accidental deletions; **breaks on every legitimate addition** (current state). High signal, high maintenance.
- **Assert `>= floor` / monotonic-vs-committed-baseline** — catches deletions/regressions; tolerates growth. Lower maintenance, misses "added a junk type."
- **Assert membership of a frozen critical subset** (the types queries depend on) — catches removal of load-bearing types; ignores the long tail. Decouples the test from vocabulary churn entirely.

**Infra reality for the menu:** mock the agent boundary, never spend tokens. The house pattern already exists — `patch.object(module, "invoke_claude", return_value=_mock_claude_response(objects))` ([tests/test_stage4_tail_classifier.py](tests/test_stage4_tail_classifier.py)) and a fake-CLI that asserts `cwd=='/tmp'` and `--output-format json` without spawning `claude`. The TS side stubs the model via the `RunTurn` type ([agent.ts:44](web/netlify/edge-functions/agent.ts:44)).

---

## 6. Existing vs. missing test infra

**Exists** (✅verified): 28 files, **1,325 collected tests**, runs under pytest with **no `pytest.ini`/`pyproject`/`conftest.py`** (default autodiscovery). Hyphenated scripts are imported via [tests/_helpers.py](tests/_helpers.py) `load_script()` (importlib `spec_from_file_location`, hyphens→underscores). Mixed `unittest.TestCase` + pytest-native styles; both run under pytest. Fixtures are inline `_make_*_row()` helpers + frozenset vocab, `tempfile.TemporaryDirectory()`, `unittest.mock.patch`. **Closest existing models for a new smoke layer:** [tests/test_validate_edge_jsonl.py](tests/test_validate_edge_jsonl.py) (schema), [tests/test_stage4_tail_classifier.py](tests/test_stage4_tail_classifier.py) (mocked agent boundary), [tests/test_longrun_supervisor.py](tests/test_longrun_supervisor.py) (bash state machine via real subprocess + scripted exit codes).

**Current health (✅verified by running):** `tests/test_validate_edge_jsonl.py` + `tests/test_longrun_supervisor.py` → **24 passed, 1 failed**; the failure is the brittle `== 167` vocab assertion (actual 170). I did **not** run the full 1,325 — Matt should, to learn the true baseline before adding to it.

**Missing / thin** (the gaps a smoke layer would fill):
- **No end-to-end batch-loop test** (fixture candidate file → `verify_outputs` → schema-validate → merged row) with the agent mocked.
- **No referential-integrity test** over `edges.jsonl` (dangling targets — check G).
- **No idempotence test** for the live re-run path (`--skip-existing` is tested only in mock-isolation; the mint double-apply guard is partially covered).
- **Narrow malformed-agent-output coverage** (code-fence stripping is tested; truncated JSON, extra fields, encoding errors are not).
- **No CI** — no `.github/workflows/`. A green-on-PR gate is absent; the RED test above would have been caught by one.
- **Chat-UI cite-gate** is covered by `deno test` ([web/netlify/edge-functions/agent_test.ts](web/netlify/edge-functions/agent_test.ts)), *not* pytest — a cross-runtime boundary to decide on (§7).

---

## 7. Decisions for Matt (options + trade-offs — I did not pick)

1. **Which trust boundary anchors the suite?**
   - *(a) Edge-JSONL schema (boundary 2)* — highest volume, most failure modes, reuses `REQUIRED_FIELDS_BY_DECISION`; but partly already covered.
   - *(b) Referential integrity over `edges.jsonl` (boundary 6)* — the biggest real gap; most "graph actually traversable" value; needs node-index fixtures.
   - *(c) Cite-gate (boundary 7)* — smallest, cleanest, zero-spend, most portfolio-legible; but it's TS/Deno, not Python.
   - *Trade:* (a) reinforces, (b) fills the real hole, (c) is the prettiest demo. You could do (c) as the article's hero example and (b) as the suite's substance.

2. **Python-only or cross-runtime?** Keep the suite pytest-only (boundaries 1–6) for one-command simplicity, or include the Deno cite-gate test (boundary 7) and accept two runners. Trade: narrative coherence (the cite-gate is your best agent-boundary story) vs. toolchain simplicity.

3. **Fixture strategy** — (a) hand-authored minimal JSONL rows (full control, you can defend every byte), (b) checked-in golden files sampled from real output (realistic, but you must vet them), or (c) tiny synthetic graph built in `tmp_path`. Trade: ownership/clarity vs. realism.

4. **How to make agent calls testable without spend** — (a) `patch.object(..., "invoke_claude", ...)` (matches house style), (b) inject a fake-CLI on `PATH`, (c) the TS `RunTurn` stub pattern. Trade: (a) is the path of least resistance and already proven here.

5. **Vocab-count assertion** — exact / floor-monotonic / critical-subset-membership (see §5 E vs L). You're choosing how much maintenance you'll accept to catch how much drift. *Fixing the current RED test is itself a clean opening anecdote — decide whether to fix it as part of this work.*

6. **What counts as a regression case?** Curate a small `regressions/` of real historical failures (the smoke5 type-contract cases; the `notes`-field bleed; a fabricated-cite example) as named tests, or keep tests synthetic. Trade: a regression corpus is the most credible artifact in an interview, but it's manual to assemble.

7. **CI or not?** A `.github/workflows` running `pytest -q` on PR would prevent the RED-on-main situation. Trade: setup + green-keeping discipline vs. a defensible "tests gate merges" claim.

---

## 8. Ideas on the article (editorial — you asked; still your call)

These are suggestions, not a draft. Take or leave.

- **Lead with the failing test.** Open cold on `AssertionError: 170 != 167`. It's true *right now*, it's small, and it earns the whole reliability section: the lesson isn't "write tests," it's "a test that asserts an exact count of a thing designed to grow is a liability." It also lets you be the practitioner who ships honest red, not the one who pretends everything's green.

- **Make the *constraint fulcrum* literal and numeric.** Your strongest sentence is already in the data: *"73% of the graph's 23,330 edges were produced deterministically at ~$0; the metered model was spent only on the 27% that required reading prose."* That single ratio justifies the entire thesis better than any prose. Lead the body with it.

- **Use the two-shapes distinction as the article's backbone.** You have *two* orchestration patterns and they're genuinely different: **volume/fan-out** (Stage 4, this article) vs **judgment/dip-loop** ([PORTABLE-PLAYBOOK.md](PORTABLE-PLAYBOOK.md)). Stating "here's when deterministic-first fan-out is right, and here's the *other* mode I use when it isn't" is exactly the "when NOT to use this" honesty your register calls for — and it shows range without diluting the piece.

- **The "$0/14s instead of $70/6h" trade is your single best paragraph.** It's the thesis in miniature: deleting an agent made the step cheaper *and* removed a failure mode (paraphrase) *and* simplified the design (single-writer-per-file). Don't bury it.

- **Frame the wrapper section around "the difference is data, not code."** The `render_prompt` placeholder injection + 3-shape `candidate_kind` dispatch is clean; the *honest* version admits the leak (three output schemas, so the validator branches too). That admission is more credible than a tidy diagram.

- **Give the cite-gate its own short section as the modern face of the thesis.** It's the same idea (smoke-test agent output before it crosses into trusted code) but in TypeScript, at request-time, against hallucinated citations — and it was *built to be tested without spending money*. That's the whole article in 40 lines, and it's the most demo-able thing you have for an interviewer who won't read Python.

- **One sub-theme worth a sidebar:** *who owns state.* The supervisor relaunches the same argv and owns nothing; the worker owns resume; the orchestrator owns all bookkeeping and hands the model a context-free prompt. "Push every deterministic responsibility *out* of the agent" is a crisp, quotable design rule and it's literally in the docstring.

- **Caveat to resolve before publishing:** verify (against `worklog.md`) whether the wiki-comention/source_target prose-edge paths actually *shipped* into the live graph or were deprecated in favor of the pass1-derived path — the live `evidence_kind` distribution suggests the latter. The article shouldn't claim Stage 4 typed the whole wiki if 73% of edges are deterministic infobox rows and the LLM's shipped contribution is mostly the pass1 path. Precision here is what makes it defensible.

---

## Appendix — provenance of claims

- **✅ Verified by orchestrator (direct read / command):** no-SQLite; 8,729 nodes; 23,330 edges; 17,657 wiki pages; 6,302 candidate files (5,686/344/272); 531 buckets; edge-row 26-field schema; `evidence_kind` + `resolution_status` distributions; 16,987 wiki-infobox edges (72.8%); 1,325 collected tests; 24-pass/1-fail spot run; vocab actual = 170; the RED `==167` assertion; `invoke_haiku`/`verify_outputs`/`render_prompt`/`candidate_to_haiku_output`/`run_chunk` code; full `agent.ts`; `longrun.sh` exit-code contract; `_helpers.load_script` trick; real candidate rows for all three shapes; existence of the three validator scripts.
- **⚠️ Reported by recon subagents (plausible, not independently re-verified):** per-rule line numbers inside the validator/type-contract/flagger scripts; `pace.py` sleep formula; the ~49% `cwd=/tmp` saving; `$70/6h` historical figure; `REQUIRED_FIELDS_BY_DECISION` exact contents; git-history fix-commit hashes.
- **🔎 Inferred (stated as such):** that the comention path was deprecated (from the live distribution + memory) — confirm in `worklog.md`; that no SDK/API path exists anywhere (only `claude -p` seen).
