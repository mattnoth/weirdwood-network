# Fire & Blood pipeline — S198 build spec (the three scripts after splitter + candidate-packs)

> Companion to `fire-and-blood-enrichment-design.md` v2. Interfaces below are LOCKED so the scripts compose.
> Shared data contracts: candidate pack schema (§5.0, built), `candidates.json` (mint schema), `merge-plan.json`.

## Interfaces already fixed
- **Resolver:** `from weirwood_query.resolve import resolve` (package at `graph/query/weirwood_query/`, add its
  parent to `sys.path`). `resolve(name) -> (slug|None, status, candidates)`, status ∈
  {`hit`,`hit-character`,`ambiguous`,`candidates`,`miss`}. Normalize via `weirwood_query.normalize.normalize`.
- **Trap blocklist:** `working/wiki/data/disambig-node-blocklist.json` — `{slug: {page, trap_kind}}`.
- **Redirect map:** `working/wiki/data/redirect-node-map.json` — `{slug: {target_page, target_slug}}`.
- **Same-name clusters:** `working/wiki/data/same-name-clusters.json` — `{"first surname": {members:{slug:{parents,
  spouse, born, died, era, key_title, regnal, allegiance}}, trap_nodes:[...], redirect_nodes:[...]}}`.
- **Candidate packs:** `working/fire-and-blood/candidate-packs/fab-<slug>-NN.json` (keyed by NN) —
  `{nn, slug, expected_slugs:[...], per_slug:{slug:{name,aliases,type,anchor_count}}}`.
- **Mint candidates.json** (consumed by `scripts/mint_enrichment.py`): `{_meta:{run_id, evidence_kind:"book-fab",
  new_node_slugs:[...], unit, session, produced_at}, edges:[{id,type,source,target,book:"fab",chapter:"<unit
  filename w/o .md>",quote,tier,note,qualifier?,in_universe_source?,disputed?,verify?}]}`. CREATE-node bodies →
  `<candidates_dir>/nodes/<slug>.node.md`.
- **Source files for quote grep:** `sources/chapters/fab/<unit>.md`. Use the SAME `norm()`+single-line-then-
  two-line-join grep that `mint_enrichment.py:authoritative_line` uses (copy it — identical normalization).

## MINT PATCH (3 lines — lands WITH the architecture.md batch, Matt-gated; do NOT apply at build time)
`make_edge_row` in `mint_enrichment.py` must pass through two optional fields so book-fab edges carry them:
```python
if e.get("in_universe_source"): row["in_universe_source"] = e["in_universe_source"]
if e.get("disputed"): row["disputed"] = True
```
Until patched, the reconciler still WRITES these into candidates.json (harmless; mint ignores unknown keys are
not emitted). Flag in the endsession handoff. The validator invariant `disputed ⇒ tier ≤ 2` is enforced by the
reconciler AND re-checked by the schema validator.

---

## Script 1 — `scripts/fab-reconcile-candidates.py` (the crux; design §5.1–5.5)
Turns one `extractions/fire-and-blood/<unit>.enrichment.md` into: `candidates.json` (+ `nodes/`),
`merge-plan.json`, `contradictions-report.md`, `run-summary.jsonl` row, and three review files.

Parse the proposal by exact header (`## Entity Roster`, `## Node Prose`, `## Relationships Observed`,
`## Events of Note`). Then:

**A. Name→slug routing (§5.1 — the R1 mitigation).** For each roster entity + every edge/event endpoint:
1. `resolve(name)`. If the resolved slug is in the **redirect map** → replace with `target_slug` (transparent).
2. If status is a clean `hit`/`hit-character` AND slug NOT in blocklist AND name NOT in any same-name cluster
   → **UPDATE** (accept). This is the common case.
3. If slug in **blocklist** OR name in a **same-name cluster** → **discriminator scoring** against every cluster
   member: score each candidate on (a) roster Disambiguator ↔ member parents/spouse/regnal/key_title, (b) unit
   `era` ↔ member era, (c) candidate-pack membership (expected_slugs + anchor_count), (d) born/died if the
   roster gives a year. **Auto-accept only if** top candidate has **≥2 independent discriminators** AND runner-up
   has **0** (decisive margin). Else → `reconcile-review.jsonl` (one row: name, unit, disambiguator, scored
   candidates+evidence).
4. `miss` + a full/unique name (NOT a bare first name) + no cluster collision → **CREATE**. Bare first name or
   any cluster collision → review, NEVER auto-create. Log CREATEs to `created-nodes.jsonl`.
- **`--smoke` flag DISABLES step-3 auto-accept** (everything scored → review) so thresholds get tuned on what
  review reveals (design §5.1 smoke policy). Default (bulk) enables it.

**B. Quote pre-validation (§5.2).** For every quote (edge evidence + prose anchors + event quotes): norm()+grep
against `sources/chapters/fab/<unit>.md`. Located → keep; attach `evidence: fab-<unit>:LINE`,
`evidence_kind: book-fab`; tier = `tier-1` (plain) or `tier-2` + `in_universe_source`/`disputed` (hedged).
Not located → quarantine the row to `quotes-review.jsonl` (row-level; the unit PROCEEDS — never abort).

**C. Tier/dispute invariant.** Any row with `disputed:true` is forced to `tier-2` (reject/repair tier-1+disputed).
`in_universe_source` must be in the enum. Blank provenance → tier-1.

**D. Emit.**
- `candidates.json` (mint schema above) — all located edges; `_meta.evidence_kind="book-fab"`,
  `run_id="<unit>-<date>"` (**AMENDED S199 Stage-2** — the full unit slug INCLUDING any `-pMM`
  part suffix; the original `fab-<slug>-NN-<date>` form gave p01/p02/p03 identical run_ids, so
  `fab_merge_node`'s idempotency marker silently dropped parts 2–3's prose on shared nodes),
  `new_node_slugs` = CREATE slugs.
- CREATE node bodies → `nodes/<slug>.node.md`: frontmatter (name, type from roster type-guess mapped to schema,
  slug, aliases:[], confidence, `era:` from unit frontmatter (§5.5), `pass_origin: pass-fab-enrichment`) +
  `## Identity` (book-grounded one-liner) + `## Fire & Blood` prose section. For `event.*` CREATE nodes with a
  year → add an `occurred:` block (`ac_year, precision:year, basis_source:narrative-prose,
  basis_reliability:primary-source, date_confidence: tier-1|tier-2`).
- `merge-plan.json` (for script 2): `[{slug, identity_line?(only if roster/prose gives a clean book identity),
  fab_section_md (the entity's Node-Prose block, each claim with its (fab-<unit>:LINE) cite), run_id}]` — one
  entry per UPDATE-routed entity that has node prose.
- `contradictions-report.md` (§5.4): diff proposed kinship/allegiance/title/succession edges vs existing
  `wiki-infobox` edges (read `graph/edges/edges.jsonl`) on the same source node. Same (source,type) with a
  DIFFERENT target, or a `disputed` F&B tag against a flat wiki claim → flag (grouped by node). Duplicate-triple-
  with-better-evidence is INTENDED (the Tier-1 overlay) — do NOT flag those.
- `run-summary.jsonl` (§7a): one row `{unit, entities_rostered, matched, ambiguous_to_review, created,
  edges_by_type, quotes_total, quotes_located_pct, quotes_quarantined, quotes_repaired, needs_vocab_count,
  disputed_rate}`.
- **AMENDED S199 Stage-2 — two additional sidecars:** `quotes-repaired.jsonl` (quotes canonicalized by the
  trailing-punct repair: the extractor clips mid-sentence + appends a synthetic '.'; the STORED quote is the
  stripped strictly-verbatim form, so mint's strict locator is unchanged) and `matched.jsonl` (every
  name→slug UPDATE routing — the wrong-match audit surface; roster-only wrong-matches must not hide).
  Routing hardened same session: type-agreement gate on clean hits (roster Type guess ↔ node category;
  `Lorath`→`jaqen-hghar` and `Sea Snake`→`corlys-velaryon` were live wrong-matches), exact-1.0 accept
  (score 1.0, margin ≥0.2, POSITIVE type agreement) to drain the exact-name review flood, review-candidate
  probes (pack + name-token) so the right answer is always presentable at triage, and year-aware `era:`
  refinement for dated CREATE events.
- **AMENDED S199 (§7.2 gate response) — dispute-proximity quarantine + `dispute-review.jsonl`:** untagged
  edges/events/prose bullets located within ±1 line of a STRONG hedge term (chronicler names / divergence
  framing; certainty markers clear the neighborhood) and ALL untagged `LOVER_OF`/`PARAMOUR_OF` edges are
  HELD to `dispute-review.jsonl`, never emitted. Adjudication at apply via the per-unit fresh-verify
  (verdict-gates-apply). Also: mechanical edge-type vocab guard (canonical 170 via
  `working/wiki/data/edge-type-counts.json`; off-vocab → review). run-summary gains `dispute_held`.

**Unit tests (build-time, no smoke needed):** feed a synthetic roster with "Aegon Targaryen" (→ must route
ambiguous, NOT accept the `aegon-targaryen` trap), "Aenys Targaryen" (→ redirect resolves to
`aenys-i-targaryen`), and a clean name like "Criston Cole" (→ UPDATE accept). Quote-grep test against a real
`sources/chapters/fab/*.md` file (one findable quote + one garbled-unfindable → quarantine).

## Script 2 — `scripts/fab_merge_node.py` (design §5.3 — new UPDATE writer; mint is skip-if-exists)
Input `--merge-plan merge-plan.json`. Per entry:
1. Read the node file (find by slug across `graph/nodes/*/`). Never touch frontmatter (except `node_version`
   +1), existing `## Edges`, or any existing prose section.
2. Identity by shape: boilerplate line matching `^.+ is a [a-z][a-z.]* from the AWOIAF wiki\.$` → replace THAT
   ONE line with `identity_line`. Real Identity → leave it. No `## Identity` section → insert one (with
   `identity_line`) right after frontmatter.
3. Append/extend a `## Fire & Blood` section with `fab_section_md`, opened by idempotency marker
   `<!-- fab-enriched: <run_id> -->`. If the marker for this run_id already present → SKIP (re-run safe).
4. Atomic temp-file + rename. Summary MUST report `merged / skipped(marker) / not-found`. **A merge-plan entry
   whose slug is not found is a HARD ERROR** (that's the silent-UPDATE-drop failure, R3).
**Smoke test:** copy one node of each shape (a boilerplate stub, b `rhaenyra-targaryen`, c a no-Identity node)
to /tmp, run against copies, assert: frontmatter byte-identical except node_version; wiki prose untouched;
boilerplate line swapped; section inserted on (c); second run = no-op.

## Script 3 — `working/fire-and-blood/fire-and-blood-extraction.py` (worker; design §6 — mirror the D&E worker)
Copy `working/dunk-egg-pass1/dunk-egg-pass1-extraction.py` shape. Changes:
- Queue from `sources/chapters/fab/*.md`; output `extractions/fire-and-blood/<unit>.enrichment.md`.
- `_build_prompt` replaces `{SOURCE_PATH} {OUT_PATH} {HARVEST_PATH}` PLUS `{ROSTER_HINT_PATH}` (path to the
  unit's candidate-pack names-only hint — generate a tiny `<unit>.roster-hint.txt` from the pack), and reads
  frontmatter for `{SECTION_TITLE} {ERA} {FIRST_AVAILABLE}`.
- `MODEL = "claude-opus-4-8"` hardcoded. `DEFAULT_PROMPT_VERSION = "v1"`, prompt dir
  `working/fire-and-blood/prompts/`. Harvest file `working/fire-and-blood/harvest-fire-and-blood.jsonl`.
- Same exit-code contract (0/2/10/crash), `--build-queue`/`--smoke --only <unit>`/`--prompt-version`/`--resume`.
  Real `claude -p` fires ONLY on `--smoke`/`--resume` (safety). cwd=/tmp. Telemetry track `fire-and-blood`.
- Wire `weirwood run start fire-and-blood` → `longrun.sh python3 .../fire-and-blood-extraction.py --resume
  --prompt-version v1` (add to the run registry the D&E track uses).
**Do NOT run --smoke/--resume** — those call `claude -p` and are Matt-fired from iTerm.
