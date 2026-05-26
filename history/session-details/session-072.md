# Session 72 — The node-gap was a false alarm; index + validator + resolver fixed; edges v1→v1.3

**Dates:** 2026-05-25 → 2026-05-26 (one continuous working session, crossed a date boundary).
**Model:** Opus 4.7 (autonomous stretches — Matt stepped away mid-session with "do all of this").
**Commits:** `eb3c6b18b` (node-gap correction + index + edges v1.2), `4f149f7b6` (resolver pass + edges v1.3), plus this `/endsession` commit.
**One-line:** Session 71 handed off "edge formalization PAUSED — ~7,251 staged nodes never promoted." That premise was **wrong** (a file count without a slug check). Verifying it before acting surfaced the truth and three real, smaller fixes — all shipped.

---

## How it started

Matt opened with scratch notes (he flagged that the prior sessions hadn't been interpreting him well, so the explicit ask was: slow down, interpret carefully). The handoff `CONTINUE-node-recovery-and-edges.md` said: a large chunk of the wiki Pass-2 entity schema was never promoted (`graph/nodes/` = 8,299 but ~7,251 staged `.node.md` sit unpromoted in `working/wiki/pass2-buckets/*/skeleton/`), and edge work was PAUSED until "the node layer is whole."

He authorized executing it ("do all of this"). The first move was **verification, not execution** — and that's the whole story.

## The correction (CLAUDE.md #9 in action)

Three independent checks, all pointing the same way:

1. **Slug reconciliation:** of 7,047 unique staged-skeleton slugs, **7,039 are already in `graph/nodes/`**. Only **8** are net-new by slug.
2. **`promote.py` dry-run** (authoritative — same slug + tier logic the pipeline uses): of ~3,730 promotable Tier-A/B pages → **43 net-new / 2,367 byte-equal / 1,307 byte-different / 12 missing-skeleton.**
3. **Promoted (8,299) > staged (7,047).** Promotion having already happened is the only thing that produces that.

**There was no unpromoted backlog. The node layer was whole.** The skeletons under `pass2-buckets/*/skeleton/` are stale *intermediate artifacts*; the promoted nodes are canonical (and in substantive "conflict" cases, *richer* — see below). The S71 health check (file counts) is exactly what manufactured the false alarm. The right check is a **slug intersection**.

I did **not** mass-promote on the false premise.

## What was actually wrong (and got fixed)

### 1. The index, not the nodes
This was Matt's real observation ("I opened graph/index and the entities weren't there"). `graph/index/` had builder configs for only `characters / houses / locations / artifacts` (+ chapters). **14 categories were never indexed** — factions, titles, events, religions, species, texts, concepts, materials, foods, theories, customs, languages, medical, prophecies. The nodes existed in `graph/nodes/` all along; the index never covered them.

Fix (delegated to script-builder): extended `scripts/build-entity-indexes.py` `TYPE_CONFIGS` (modeled on the `houses` no-primary-section pattern) + rebuilt → **1,861 new `*.index.json`**. High zero-mention rates are expected (wiki-sourced entities Pass 1 never tagged).

### 2. The COMMANDS type-contract false-dropped faction targets
The v1.1 refinement was about to drop real edges like `gunthor COMMANDS stone-crows` — not because the factions were missing (`stone-crows`, `iron-fleet`, `brotherhood-without-banners`, `second-sons`, `golden-company` all exist in `graph/nodes/factions/`) but because `stage4-type-contract-validator.py` Contract 4 only consulted `graph/nodes/characters/`.

Fix: COMMANDS now accepts a **character OR a commandable unit (faction/house)**; DROPs place (two-hop) / object / other-non-commandable; soft-FLAGs unknown. `TestCommandsContract` rewritten to the corrected semantics.

### 3. `refine-v1-edges.py` never passed the category index
Latent bug: it called `type_contract_pass(row, character_slugs)` with no `slug_category_index`, so **all** category-based contracts (COMMANDS-unit, CONTRACTED_WITH, MEMBER_OF-flip, HOLDS_TITLE-place) silently never fired in the v1.1 build. Fixed to build + pass the index (`produce-v1-1-candidate.py` already did it correctly — divergence caught by reading both).

### Edges v1.2 (3,842 → 3,825)
Re-ran the refine with the fixed validator over a READ-ONLY `edges.jsonl` → corrected candidate; applied: dropped 17 genuinely-wrong rows (13 COMMANDS→non-commandable + 1 MOTIVATES + 3 VIOLATES_GUEST_RIGHT), retyped 3 RULES→COMMANDS, **kept the 16 real COMMANDS→faction edges**. Clean schema preserved (advisory `_qr_warning` soft-flags stay only in the gitignored `_v1-refine/` candidate). Committed `eb3c6b18b`.

### The 1,307 "conflicts" — no action
≤2 bytes: 73 (trailing-newline) / 3-50: 658 / >50: 576. In every substantive sample the **promoted node is richer** than the staged skeleton (`aegons-conquest` 4714 vs 2738; `battle-of-the-blackwater` 26363 vs 24168). Re-promoting would *downgrade*. That's exactly why `promote.py` routes byte-diffs to `_conflicts/` instead of overwriting. Conclusion: the node layer is healthy; staging is old scratch.

## The resolver pass (Matt back; edges v1.2 → v1.3 = 3,811)

Matt asked: "does fixing the index help the edge scripts achieve better results?" **Honest answer: no** — the edge scripts read `graph/nodes/`, not `graph/index/`; the index is a decoupled query/traversal layer. The real edge-quality lever is the **resolver**. He said: take the resolver pass next.

### The collision class
A `find tywin` from the v1.2 work revealed `lord-tywin` resolves to an `object.artifact` — it's **Cersei's warship** (a dromond named after the man). Tracing the resolver: `to_slug("Lord Tywin") = "lord-tywin"` exact-matches the ship at Rung a, *before* the character path (Rung c: strip "lord" → "tywin" → `tywin-lannister`) can run. Ships/artifacts/titles named after people were capturing person references.

### Measure → simulate → apply (de-risk before touching a core script)
- **Measure:** 408 titled non-character nodes; **42 committed edges** hit one. Dominated by 6 person-collision nodes used in person relationships.
- **Simulate** a character-restricted name ladder on each collision: **6 clean wins** — `lord-tywin→tywin-lannister` (848 backlinks, prior-dominant), `queen-cersei→cersei-lannister` (949), `lord-renly→renly-baratheon` (385), `princess-myrcella→myrcella-baratheon`, `lady-olenna→olenna-tyrell`, `khal-jhaqo→jhaqo`. `lady-catelyns-sept` correctly stays a location (no char candidate). **One trap:** `lady-marya` → `marya-seaworth` — but the edge is `allard-seaworth CAPTAIN_OF lady-marya`, and Lady Marya is **Davos's actual ship**. So that one must stay the artifact.

### The fix
- `stage4_name_resolver.py`: category-aware exact rung. When a title-prefixed name exact-matches a NON-character node, prefer the character via a char-restricted ladder (firstname-unique / context-present / context-prior). New status `resolved-title-person`. `slug_category` threaded through `stage4-pass1-edge-candidates.py`. Ship names whose remainder isn't a bare character first name (`King Robert's Hammer` → "robert's") keep the artifact.
- `stage4-type-contract-validator.py`: added `CAPTAIN_OF` / `CREW_OF` to the target-not-character contract (architecture: target MUST be `object.artifact`). This is the ship-name backstop for future re-runs.

### Applied to edges.jsonl (3,825 → 3,811)
Surgical remap of the 6 collision slugs → characters (kept `lady-marya` as ship), −12 dups. The new CAPTAIN_OF guard caught **2 bonus pre-existing bad edges** — `hallis-mollen` / `areo-hotah` "CAPTAIN_OF" a person (really "captain of the *guard*", mis-typed) — dropped. Remapped edges fold into the character nodes (`cersei-lannister` now 229 edges, `tywin-lannister` 88, …). Committed `4f149f7b6`. 814 tests green.

## Decisions / lessons

- **Verify handoff premises before executing.** A continue prompt written under context pressure asserted a 7,251-node backlock; one slug intersection refuted it. The lesson belongs in the worklog Active Decisions and a memory entry (`project_s72_node_gap_false_alarm`).
- **Health check = slug intersection, not file count.** A file count is what produced the false alarm.
- **`graph/index/` is decoupled from edge-building** — don't expect index work to change edge results; the resolver is the lever.
- **Measure → simulate → apply** for any change to a core deterministic script — the simulation caught the `lady-marya` ship before it became a regression.
- **Frozen baseline discipline held:** `edges.jsonl` was never clobbered mid-flight; each version (v1 3,842 → v1.2 3,825 → v1.3 3,811) is a deliberate, documented, committed step with the candidate kept in gitignored scratch.

## Numbers
- Nodes: 8,299 promoted (no backlog; 8 net-new, all dups of canonical nodes → not promoted).
- Index: +1,861 `*.index.json` across 14 categories.
- Edges: v1 3,842 → v1.2 3,825 → v1.3 3,811. Provenance: python-map 1,964 / sonnet 1,401 / hospitality-table 396 / hospitality-table-violation 50.
- Tests: 805 → 814 green (added title-person + CAPTAIN_OF cases).

## Still open
Folder reorg (`working/wiki/` + `scripts/` are dumps; 2 leftover git worktrees); untrack 2 git-tracked scratch files; optional deeper resolver *recall* work (alias completeness for the ~387 unresolved / ~651 ambiguous S67 endpoints — distinct from this precision pass). The Events+Dialogue Haiku enrichment (v2) remains separately NOT-YET (~62% out-of-sample).
