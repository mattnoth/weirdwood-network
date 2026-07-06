# Wiki-Prose Node Enrichment & Same-Name Disambiguation — Track Design

> **Version: v2 — post-Fable-review (2026-07-06).** Reviewed alongside the F&B plan (`working/fire-and-blood/fable-review.md`). v2 fixes a false data claim (birth/death years are NOT in the graph as edges — see §2), adds the two things the review found missing (the machine-readable **disambiguation pack** that F&B's reconciler actually consumes, and the **disambiguation trap nodes**), specifies the three node shapes the writer must handle, and adds an execution plan detailed enough for a cheaper agent.
>
> **Status:** DESIGN — Matt's go gates the build. **Sequencing RESOLVED: this track runs FIRST**, before F&B extraction (F&B design §10–§11 #10).
>
> **One-line goal:** every node — especially same-name ones in big houses — gets a **distinguishing Identity line** plus a **machine-readable discriminator record**, built as cheaply and deterministically as possible from data already local.

---

## §0 — Component status

| # | Component | Path (proposed) | Status |
|---|-----------|-----------------|--------|
| 1 | Cluster detector + discriminator assembler + Identity composer | `scripts/wiki-prose-identity-composer.py` | **DESIGN** |
| 2 | **Disambiguation pack** (machine-readable; consumed by F&B reconciler) | `working/wiki/data/same-name-clusters.json` | **DESIGN — new in v2** |
| 3 | **Trap-node blocklist + hub stamping** (disambiguation-page-derived nodes) | part of #1 → `working/wiki/data/disambig-node-blocklist.json` | **DESIGN — new in v2** |
| 4 | Node writer (additive Identity merge; shared shape-handling rules with F&B `fab_merge_node.py`) | part of #1 (or a shared `node_merge_lib.py`) | **DESIGN** |
| 5 | Haiku residue pass (only if smoke shows need — §3 step 2) | gated | **DESIGN — deferred until composer smoke** |

---

## §1 — The problem

Pass-2 wiki ingestion minted nodes deterministically from **infoboxes only** — the `## Identity` prose is boilerplate:

> *"Aegon Targaryen is a character.human from the AWOIAF wiki."*

This is fine until you have **13 Aegon-Targaryen-named character nodes** (verified: `aegon-i…v-targaryen`, 6 `aegon-targaryen-son-of-*`, `aegon-targaryen-young-griff`, plus the bare `aegon-targaryen`), a pile of Daerons, Aemons, Baelons, Alysannes, Viseryses. The slug disambiguates for the *machine*, but a human, an agent, the chat-UI, or the F&B reconciler's *reviewers* cannot tell which is which without tracing edges.

**Worse — verified 2026-07-06:** the bare-name nodes (`aegon-targaryen`, `aemon-targaryen`, `baelon-targaryen`, `daeron-targaryen`, `jaehaerys-targaryen`, `rhaena-targaryen`, …) were minted from the wiki's **disambiguation pages** (`page-categories.jsonl` category `Disambiguation pages`; 350 such pages, 144 explicit `*_(disambiguation)` files also cached). They are contentless zero-edge traps — and `weirwood query resolve "Aegon Targaryen"` returns a **confident HIT** on one. Any matcher that trusts exact hits will pour content onto them. This track fixes both the human-legibility problem and the trap-node problem.

## §2 — The insight: the distinguishing data already exists locally (v2 — corrected sources)

No LLM read of the wiki is needed. Per node, the discriminators are on hand — with one correction from review:

1. **Kinship/allegiance/title edges** — `graph/edges/edges.jsonl` (16,757 `wiki-infobox` rows): `PARENT_OF` (both directions), `SPOUSE_OF`, `SWORN_TO`, `HOLDS_TITLE`, `DIED_AT` (sometimes with an `[NNN AC]` qualifier).
2. **Birth/death years — NOT in the graph** (v1 claimed they were edges on `aegon-targaryen-son-of-baelon`; verified false — that node has 6 edges, none dated). **Correct deterministic source: `working/wiki/data/page-categories.jsonl`** — MediaWiki categories carry them directly: `"84 AC births"`, `"85 AC deaths"` (verified for that exact page). Regex `^(\d+) (AC|BC) (births|deaths)$` over each node's wiki page categories → life-years for nearly every dated character. No HTML parsing, no LLM.
3. **Regnal number / parenthetical** — already in the node `name:` / slug.
4. **The local wiki cache lead paragraph** — `sources/wiki/_raw/<Page>.json` → first prose sentence(s) — the *fallback* for nodes the above leaves thin. **No re-fetch** (`feedback_no_external_wiki_fetch` / `project_wiki_already_local`). Note the parse machinery already exists in `scripts/wiki-pass2-extract-prose.py` — reuse its HTML→lead-text path rather than writing a new one.
5. **`era:`** where present; else derivable from death-year (e.g. died ≤ 26 AC → conquest era) — optional garnish, not required.

So this is **deterministic composition**, not generation.

### §2.5 — The three node shapes the writer must handle (verified; shared finding with F&B design §1)

- **(a) Boilerplate-Identity stub** — `## Identity` holds only the boilerplate line (~2,753 character nodes). → swap the line.
- **(b) Rich node with boilerplate Identity** — boilerplate line + real wiki prose sections below (e.g. `rhaenyra-targaryen`, ~90 lines of cited Origins/Appearances/Quotes). → swap ONLY the one line; **touch nothing else**.
- **(c) No `## Identity` section at all** — body starts at `## Origins` (e.g. `aegon-targaryen-son-of-baelon`; ~545 character nodes). → **insert** an `## Identity` section immediately after frontmatter.

Boilerplate detection is an exact regex: `^.+ is a [a-z][a-z.]* from the AWOIAF wiki\.$` — a non-matching Identity line is REAL prose and is never replaced.

## §3 — Approach (model ladder: deterministic → Haiku → Fable)

Per `feedback_backfill_model_ladder` (diagnose deterministically first; cheap model for residue; never default to a reasoning model for bulk):

1. **Deterministic composer (Python, no LLM)** — for each node, assemble a one/two-line Identity from §2 sources, template with field priority **life-years (categories) → parents (edges) → spouse (edges) → seat/allegiance (edges) → signature title (edges)**, skipping absent fields gracefully:
   > *"Aegon Targaryen (84–85 AC) — infant son of Baelon Targaryen and Alyssa Targaryen; died before his first nameday."*

   Cluster members additionally get a cross-pointer sentence: *"One of N Aegon Targaryens — see the Aegon Targaryen disambiguation entry."*
2. **Haiku cleanup — only where deterministic output is too thin.** Operationalized (v2, review-ruled): run the composer first; a cluster member is "too thin" if its composed line has **fewer than 2 discriminator fields**. If >20% of same-name-cluster members are too thin after the composer smoke, run a bounded Haiku pass that reads the local `_raw` lead paragraph and emits ONE distinguishing sentence (Tier-2 wiki-sourced, cite'd like any wiki claim). Below that threshold, skip Haiku entirely for v1.
3. **Fable — only for genuine reasoning residue** (rare: nodes where sources conflict on identity). Not the default; expected count ≈ 0 for v1.

### §3.5 — Output #2: the disambiguation pack (what F&B actually consumes) — NEW in v2

The review's key structural point: the F&B reconciler is *deterministic* — it never reads Identity prose, so prose alone de-risks only human review. The same assembly work therefore also emits a machine-readable pack, `working/wiki/data/same-name-clusters.json`:

```json
{
  "aegon targaryen": {
    "members": {
      "aegon-i-targaryen":            {"regnal": "I", "parents": ["aerion-targaryen", "valaena-velaryon"], "born": -27, "died": 37, "era": "targaryen-conquest", "key_title": "King of the Andals..."},
      "aegon-targaryen-son-of-baelon": {"regnal": null, "parents": ["baelon-targaryen-son-of-jaehaerys-i", "alyssa-targaryen"], "born": 84, "died": 85, "era": "targaryen-rule", "key_title": "Prince"},
      "...": {}
    },
    "trap_nodes": ["aegon-targaryen"]
  }
}
```

Plus `working/wiki/data/disambig-node-blocklist.json`: every node slug whose `wiki_source` page carries the `Disambiguation pages` category. Build both from: node frontmatter (`wiki_source` → page name) × `page-categories.jsonl` × `edges.jsonl` kinship rows. Pure joins.

### §3.6 — Trap-node handling — NEW in v2

The disambiguation-page-derived nodes (bare `aegon-targaryen` etc.) become **navigation hubs instead of traps**:

- Frontmatter: add **`disambiguation_hub: true`** (schema touch — goes into the same architecture.md Active-Decision batch as F&B's `fab`/`book-fab`/`in_universe_source` changes; one batch, not two).
- Identity: *"Disambiguation entry — 'Aegon Targaryen' may refer to: Aegon I 'the Conqueror' (r. 1–37 AC); Aegon II (r. 129–131 AC); … (12 more)."* Composed from the pack, one line per member with its top discriminator.
- **Never an UPDATE target** for any enrichment pass (F&B design §5.1 consumes the blocklist).
- Do NOT delete or merge them (they're legitimate wiki-derived index pages; also the additive-only instinct applies) — they just stop masquerading as people.

## §4 — Scope, cluster detection & prioritization

- **Cluster key (RESOLVED, review):** strip parentheticals + regnal numerals from `name:` → key on the **(first-name, surname)** pair — so "Aegon Targaryen" clusters separately from "Aegon Frey" (both exist). v1's worry about cross-house first-name over-merge dissolves with the surname in the key. Single-name characters (e.g. "Nettles") key on the bare name.
- **Cluster-first:** any cluster of **size ≥ 2** (counting trap nodes separately) is the MVP — highest confusion, highest payoff-per-token, and the part F&B needs. Singletons are a later long tail (the composer is reusable as-is).
- **Graph-wide eventually**, but v1 scope = character same-name clusters + their trap nodes.
- Where the wiki has an explicit `*_(disambiguation)` page (144 cached), record it in the pack for navigability.

## §5 — Safety, confidence, reuse

- **Additive merge only** (same rules as F&B `fab_merge_node.py` §5.3 — consider sharing a `node_merge_lib.py`): touch ONLY the boilerplate Identity line (exact-regex-matched) or insert the section if absent (§2.5 shapes); **preserve** all frontmatter (except `node_version` +1), all edges, all real prose. Idempotency: skip if the composed line is already present. Atomic write (temp + rename). Zero data-loss risk.
- **No tier inflation.** The composed Identity restates facts already in the node/categories at their existing tiers — a *presentation* upgrade, not a new claim. (If the Haiku step pulls a *new* fact from wiki lead prose, that fact is Tier-2 wiki-sourced and cite'd, same as any wiki claim.)
- **Reuses:** local wiki cache; `page-categories.jsonl` (the 2026-04-30 exception-fetch output — this is its second consumer); `edges.jsonl`; `build_search_index.py` / `build_alias_table.py`; `wiki-pass2-extract-prose.py`'s lead-paragraph parse (Haiku step only); `weirwood refresh` afterward (Identity text becomes searchable — node-mutation rule `project_rebuild_derived_artifacts_after_node_mutation`); `duplicate-detector` to confirm cluster members are distinct entities, not accidental dupes.

## §6 — Execution plan (for a cheaper agent) — NEW in v2

1. **Build** `scripts/wiki-prose-identity-composer.py` with subcommands:
   - `--build-pack` → `same-name-clusters.json` + `disambig-node-blocklist.json` (§3.5). No node writes.
   - `--compose --dry-run` → `working/node-enrichment-wiki-prose/preview.md`: every cluster, per-member composed Identity line, thin-flag counts. No node writes.
   - `--apply` → node writes per §5 (gated).
2. **Acceptance criteria (dry-run, before Matt sees it):**
   - Pack: "aegon targaryen" cluster has ≥12 members + `aegon-targaryen` in `trap_nodes`; son-of-baelon shows born 84 / died 85 (from categories); every blocklist entry's wiki page really carries `Disambiguation pages`.
   - Composer: zero writes outside `## Identity`; shapes (a)/(b)/(c) each verified on a named example (`aegon-i-targaryen` or similar / `rhaenyra-targaryen` / `aegon-targaryen-son-of-baelon`); re-run of `--apply` on an applied copy is a no-op; thin-rate reported.
3. **Matt reviews the dry-run preview** → explicit go (`feedback_no_graph_mutation_without_goahead` — a validated dry-run earns confidence in the design, not permission to apply).
4. **Apply** → `weirwood refresh` → spot-check `weirwood query resolve` + chat-UI search on "Aegon"/"Daeron".
5. Decide Haiku residue by the >20%-thin threshold (§3 step 2); if triggered, it's a separate gated mini-run.
6. Hand the pack path to the F&B track (its reconciler dependency — F&B design §5.1) and log the architecture.md `disambiguation_hub` field in the shared Active-Decision batch.

**Recommended model:** the composer build + dry-run is script-builder work (Sonnet-class); no Opus anywhere; Haiku only in the gated residue step.

## §7 — Why it's worth doing (and when) — RESOLVED

- **De-risks Fire & Blood, now for real:** the pack + blocklist feed F&B's hardened reconciler directly (its trap-node and cluster-scoring inputs — F&B §5.1); the Identity lines make its review files legible. **Sequencing: FIRST** — pure Python, can run this week; F&B extraction gates on the pack.
- **Direct chat-UI / portfolio value** — HotD viewers searching "Aegon" or "Daeron" currently hit interchangeable boilerplate stubs (or a contentless trap node); this makes results legible and the trap nodes navigable.
- **Cheap** — one Python script + a bounded, probably-skippable Haiku residue; no Opus, no re-fetch.

## §8 — Open questions — RESOLVED (v2) / remaining

1. ~~Composer-only vs composer+Haiku for v1~~ → **composer-only; Haiku gated on the >20%-thin smoke threshold** (§3).
2. ~~Where does the disambiguation pointer live~~ → **both**: `disambiguation_hub: true` frontmatter on trap nodes + a cross-pointer sentence in cluster members' Identity lines. No new node types, no new edge types.
3. ~~Cluster boundary~~ → **(first-name, surname) key** after stripping regnal numerals/parentheticals (§4).
4. ~~Priority vs F&B~~ → **first** (§7).
5. **Remaining for Matt:** approve the track + the `disambiguation_hub` schema field (batched with the F&B architecture.md changes); approve apply after the dry-run preview.
