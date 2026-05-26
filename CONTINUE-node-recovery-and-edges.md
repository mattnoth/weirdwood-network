# CONTINUE — Edge re-validation done; the "node gap" was a FALSE ALARM

> **Rewritten Session 72 (2026-05-25, Opus, autonomous) — supersedes the Session-71 version
> of this file, whose central premise was WRONG.** Trust `worklog.md` over this doc (CLAUDE.md #9).
> Next session: any model — remaining work is deterministic + a couple of Matt decisions. Opus
> only if you want judgment on whether to apply the v1.2 edge candidate.

---

## TL;DR — Session 71's premise was a file-count error (corrected + verified S72)

S71 handoff claimed: *"~7,251 staged `.node.md` were never promoted; nodes staged not lost; edge
formalization PAUSED until the node layer is whole."* **That was a count of files without a slug
intersection.** Verified three independent ways this session:

- **Slug reconciliation:** 7,039 of 7,047 unique staged-skeleton slugs are **already in
  `graph/nodes/`**. Only **8** are truly net-new by slug.
- **`promote.py` dry-run (authoritative — same slug+tier logic):** of ~3,730 promotable Tier-A/B
  pages → **43 net-new / 2,367 byte-equal / 1,307 byte-different / 12 missing-skeleton.**
- **Promoted (8,299) > staged (7,047):** the signature of promotion having already happened.

**There is NO unpromoted backlog. The node layer is whole.** The skeletons under
`working/wiki/pass2-buckets/*/skeleton/` are **stale intermediate artifacts**; the promoted nodes
are canonical (and in the substantive conflict cases, *richer* than the staged skeleton). The
one-line health check the S71 doc proposed (file counts) is what *produced* the false alarm — the
correct check is a **slug intersection**, not a file count.

---

## What was ACTUALLY wrong — and is now FIXED (S72)

1. **The index, not the nodes** (this is what Matt saw when "the entities weren't there").
   `graph/index/` only had builder configs for `characters / houses / locations / artifacts`.
   **14 categories were never indexed** (factions, titles, events, religions, species, texts,
   concepts, materials, foods, theories, customs, languages, medical, prophecies). The *nodes*
   existed in `graph/nodes/` all along; the *index* never covered them.
   **FIX (done):** extended `scripts/build-entity-indexes.py` `TYPE_CONFIGS` to all categories +
   rebuilt → **1,847 new `*.index.json`** across 14 dirs (factions 191, titles 542, events 371,
   religions 63, species 188, texts 159, concepts 57, materials 58, foods 74, theories 45,
   customs 37, languages 26, medical 34, prophecies 2). Zero errors. (High zero-mention rates are
   expected — wiki-sourced entities Pass 1 never tagged.)

2. **Type-contract validator false-dropped `COMMANDS→faction`** — NOT because factions were
   missing (`stone-crows`, `iron-fleet`, `brotherhood-without-banners`, `second-sons`,
   `golden-company` all exist in `graph/nodes/factions/`) but because Contract 4 only consulted
   `graph/nodes/characters/`.
   **FIX (done):** `scripts/stage4-type-contract-validator.py` Contract 4 now accepts a **character
   OR a commandable unit (faction/house)** target; DROPs place (two-hop collapse) / object /
   other-non-commandable; soft-FLAGs unknown (no-node). New constant `_COMMANDABLE_ORG_CATEGORIES`.
   `TestCommandsContract` rewritten to the corrected semantics. **805 tests green.**

3. **`refine-v1-edges.py` never passed `slug_category_index`** → the category-based contracts
   (COMMANDS-unit, CONTRACTED_WITH, MEMBER_OF-flip, HOLDS_TITLE-place) **never fired** in the v1.1
   build (latent bug — only character-based contracts ran).
   **FIX (done):** builds + passes the index; test stub updated.

---

## Edge re-validation — DONE (this was Matt's "re-resolve + re-validate, not re-extract")

Re-ran `stage4-refine-v1-edges.py --apply` with the fixed validator over the **READ-ONLY**
committed `edges.jsonl`. Output = **corrected v1.2 candidate, 3,825 rows** at
`working/wiki/pass2-buckets/pass1-derived/_v1-refine/edges-v1.1-candidate.jsonl`.

- **16 `COMMANDS→faction` edges RECOVERED** (gunthor→stone-crows, victarion→iron-fleet,
  beric→brotherhood-without-banners, ben-plumm→second-sons, jon-snow→nights-watch, yoren→nights-watch,
  vargo-hoat→brave-companions, caggo→windblown, hizdahr/skahaz→brazen-beasts, melisandre→queens-men,
  tyrion→mountain-clans, nymeria→wolf-pack, …).
- **17 hard-drops** = 13 genuinely-wrong COMMANDS (target = artifact/place/title/species/text/
  concept) + 1 MOTIVATES + 3 VIOLATES_GUEST_RIGHT. (3 RULES→char also RETYPE→COMMANDS.)
- 1,944 rows carry `_qr_warning` (quote-relevance soft-flag; **kept**, not dropped).
- **Pre-fix v1.1 preserved** at `_v1-refine/superseded-2026-05-25-preCommandsFix/` (provenance).
- **`graph/edges/edges.jsonl` = 3,842 rows, FROZEN, UNTOUCHED** (md5 `9617c73b4548a3ae43dea333dbc55a0e`,
  git clean).

> **"Will we redo edges once the schema enlarges?" — No.** Re-resolve was effectively a no-op
> (the nodes were never missing), and re-validate is deterministic ($0) over the existing
> candidates. Done. No re-extract.

---

## RESOLVED (Session 72, Matt back) — ①②③ closed

- **① APPLIED + COMMITTED.** `graph/edges/edges.jsonl` is now the **3,825**-row v1.2 (was 3,842):
  17 wrong rows dropped, 3 RULES→COMMANDS retyped, 16 real faction-COMMANDS kept. Clean schema
  preserved (advisory `_qr_warning` soft-flags stay only in the gitignored `_v1-refine/` candidate).
  README + worklog updated.
- **② net-new promotion CANCELLED — they're all dups.** Every one of the 8 "net-new" is a
  singular/variant of an existing canonical node: `andal→factions/andals`,
  `dornishman→factions/dornishmen`, `wildlings→concepts/free-folk`,
  `war-of-five-kings→events/war-of-the-five-kings`, `stormlander→factions/stormlanders`,
  `lhazarene→factions/lhazareen`, `lysene→factions/lyseni`. Promoting would create duplicate nodes.
  At most they're alias candidates — and they don't appear to be edge endpoints, so no edge benefit.
  **Do not promote.**
- **③ `lord-tywin` is NOT a mis-type — it's a real ship.** The wiki page "Lord Tywin" is Cersei's
  dromond (warship), correctly typed `object.artifact`. The edge `gregor→lord-tywin COMMANDS`
  *mis-resolved* the man's name to the ship; the fixed type-contract **correctly dropped it**
  (and it was wrong-direction anyway). No node action. (`lord-tywin→tommen COMMANDS` survives as the
  same-class resolver noise — see below.)

## STILL OPEN — next sessions

- **Resolver name-disambiguation (the real edge-quality lever — NOT the index).** `graph/index/`
  is decoupled from the edge scripts (they read `graph/nodes/`), so the index rebuild doesn't change
  edge results. The genuine lever is the **resolver**: same-name-different-entity disambiguation
  (the `lord-tywin` ship-vs-man class) + alias completeness. Scoped pass on `stage4_name_resolver.py`.
- **1,307 skeleton↔node "conflicts" — NO ACTION.** Breakdown: ≤2 bytes 73 (trailing-newline) /
  3–50 bytes 658 / >50 bytes 576. In every substantive sample the **promoted node is richer** than
  the staged skeleton (`aegons-conquest` node 4714 vs staged 2738; `battle-of-the-blackwater` 26363
  vs 24168). Re-promoting would *downgrade* nodes — exactly why `promote.py` routes byte-diffs to
  `_conflicts/` instead of overwriting. Leave skeletons as-is; archive the staging tree in the reorg.
- **Folder reorg (its own session):** `working/wiki/` and `scripts/` are dumps (dozens of
  `stage4-*.py`). Reorganize by epic. Also clutter: leftover git worktrees
  `.claude/worktrees/{mystifying-burnell-*,admiring-benz-*}` (`git worktree remove`).
- **0.1 scratch check — mostly already correct.** `endsession.md:21` already says "do NOT triage
  scratch"; `.gitignore` `scratch*` (line 34) covers all scratch files. **But:** two scratch files
  are *committed/tracked* — `scratch-do-not-delete.txt` + `scratch-stage4-considerations-haiku.txt`
  (`git rm --cached` to untrack, keep on disk — note "do-not-delete"). And `.gitignore` line 11 still
  has a stale comment "(only /endsession triages it)" worth deleting. No active hook/promotion
  mechanism exists — the scratch content reached the agent as an IDE text-selection.

---

## State of the scripts — STILL UNCOMMITTED (Matt checkpoints)

Modified this session: `scripts/stage4-type-contract-validator.py`,
`scripts/stage4-refine-v1-edges.py`, `scripts/build-entity-indexes.py`,
`tests/test_stage4_type_contract_validator.py`, `tests/test_stage4_refine_v1_edges.py`.
Plus 1,847 new `graph/index/**/*.index.json`. **805 tests green.** Nothing committed.

## Key pointers
- Promoter (reuse, conflict-safe): `scripts/wiki-pass2-promote.py` (dry-run = no flag; `--apply`).
- Index builder (now all categories): `scripts/build-entity-indexes.py` + `build-character-indexes.py`.
- Edge refine (read-only on edges.jsonl): `scripts/stage4-refine-v1-edges.py`.
- Type-contract validator: `scripts/stage4-type-contract-validator.py` (Contract 4 = COMMANDS).
- Frozen edge layer: `graph/edges/edges.jsonl` (3,842) + `README.md`.
- Corrected candidate: `working/wiki/pass2-buckets/pass1-derived/_v1-refine/edges-v1.1-candidate.jsonl`.
- SECONDARY track (independent): `progress/continue-prompts/2026-05-25-stage4-locator-grounding.md`
  (Events+Dialogue enrichment ~62% out-of-sample — still NOT-YET; unrelated to the node correction).
