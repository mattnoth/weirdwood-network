# Sift Stage 1 — Opus Review + v2 Re-Smoke (AGOT oaths lens)
*Opus review pass. Date: 2026-06-27. Supersedes the v1 builder report (`smoke-test-report.md`).*
*Ran in parallel with the D&E enrichment dip — no graph/edge files touched.*

## TL;DR
The v1 build was correct and the smoke test was sound. I made **five engine improvements** to `scripts/sift.py`
and a **recall-only `+33`-trigger lexicon expansion** (v2), then re-ran the AGOT smoke test. Determinism and
sub-second runtime hold. Recall went **116 → 172 pointers**; the multi-fire problem is fixed by clustering
(**172 pointers now collapse to 133 clusters**). Exclusions remain empty — precision tuning is still your call.

| metric | v1 (build) | v2 (this pass) |
|---|---|---|
| triggers | 41 | 74 (+33, recall-only) |
| AGOT pointers | 116 | 172 |
| AGOT **clusters** (Stage-2 work units) | — (not modeled) | 133 |
| runtime | 0.18 s | 0.25 s |
| deterministic (byte-identical re-run) | ✅ | ✅ |

---

## 1. One spec error found & corrected (the multi-fire claim)
The v1 report said the Night's Watch vow's multi-fire is *"handled by Stage-2 dedup by `cand_id`."* **It isn't.**
`cand_id = sha1(book|chapter:line|trigger_norm)` keys on the **trigger**, and the vow fires **8 *different*
triggers on one line** (`agot-jon-06:147`) — so they get 8 distinct `cand_id`s and would survive as 8 candidates
for *one* oath. (v1 also undercounted: 8 on the line, 9 in the ceremony cluster.)

**Fix:** every pointer now carries a **`cluster_id`** (`<chapter_file>:<first_line>`) grouping co-located hits
(same chapter, snippet windows overlapping). The vow ceremony → **one cluster** (`agot-jon-06.md:145`, size 9).
Stage 2 should iterate **clusters, not pointers** → 133 Haiku calls instead of 172, and the vow becomes one
candidate. This is the correct dedup key; `cand_id` is not.

## 2. Engine improvements shipped (`scripts/sift.py`)
1. **`cluster_id` + `cluster_size`** on every pointer (see §1).
2. **`ptr_id`** = `sha1(book|chapter_file|line|match_start|trigger_norm)[:12]` — stable per-pointer identity
   (includes `match_start`, so the same trigger twice on a line stays distinct — the design's `cand_id` would collide).
3. **`<book>.coverage.json`** written next to the pointers — machine-readable trigger coverage (hits/trigger,
   zero-hit list, cluster count), deterministic and diffable across runs (no timestamp inside).
4. **`sift sample --lens X [--book Y] [-n N]`** — deterministic, trigger-stratified preview for human eyeballing,
   so re-reviewing a lens is reproducible instead of hand-picked. Wired through `weirwood sift sample`.
5. **Manifest honesty** — the sha256 manifest now records **input *and* output** hashes as an audit/idempotency
   record. It was being written but never read; per-file skip is deliberately **not** built (a full scan is
   sub-second — YAGNI; the documented escape hatch is `pyahocorasick` if the corpus ever grows past ~2 s).

All additive — no behavior change to existing fields; the engine still "emits every literal hit," Haiku still judges.

## 3. Lexicon v2 — recall-only expansion (+33, attested)
A grounded recall-audit sub-agent read `sources/chapters/agot/` and proposed precise, **AGOT-attested** additions
(it explicitly rejected noisy stems like bare `kneel`/`guest`/`to one knee`). I folded in the low/med-risk set.
Highlights of what the additions catch that v1 missed:

- **Two recall gaps from the audit are now closed:** Robb crowned King in the North — `laid his sword at`
  (`agot-catelyn-11:211`); Jaime's Kingsguard investiture — `protect and defend` + `making his vows` (`agot-eddard-15:41`).
- **Guest-right (was 0 useful hits in AGOT):** `the hospitality of` ×3, `came a guest into` — the latter is the
  guest-right **violation** seed ("came a guest into my house, and there conspired to murder my son", `agot-catelyn-05:153`).
- **Marriage (a 0-hit category in v1):** `to wife` ×3, `man and wife`.
- **Institutional vows:** `sworn brother` ×7, `sworn brotherhood` ×2, `holy vows`, `knightly vows`, `seven oils` ×4,
  `anointed knight` ×2, `stand your vigil`, `take your vows`, `swore to obey`, `sworn to defend/protect/serve`.

`exclusions` is still **`[]`** — I did **not** add stop-phrases (the v1 report reserved that for your review of the
32 `I swear` rows, and I'm respecting it). The change is fully reversible: delete the v2 trigger block in
`working/sift/lenses/oaths.lens.json` (v1 backed up at the session scratchpad).

## 4. Answers to the v1 report's 5 Opus-review questions
1. **Lexicon complete enough?** Closer. +33 attested triggers added; the audit's remaining "true recall gaps"
   are paraphrase-only moments no literal scanner can catch (e.g., "dipped their banners", the shouted
   "The King in the North!" acclamation) — documented as the ceiling of the keyword approach, not bugs.
2. **Tighten `'I swear'`?** Left as-is. It's a precision problem (≈80% casual), and precision is Haiku's job +
   your exclusion call — not a recall change. Don't tighten the trigger; let Stage 2 reject.
3. **15 zero-hit triggers correct?** Yes — confirmed absences for Book 1 (guest-right ritual = ASOS/Red Wedding;
   `do you swear` knighting ceremonies aren't in AGOT). v2 adds 2 new zero-hit recall-insurance triggers
   (`take a vow`, `keep faith`) that will earn their keep in later books.
4. **Multi-fire design right?** No — fixed (§1). Cluster, don't rely on `cand_id`.
5. **Edge types latent (SWORE_TO / BROKE_OATH_TO / guest-right)?** Confirmed visible in the pointers, but stays
   **deferred** per spec — the edges layer is frozen during the enrichment track. Stage 1's cluster map is a
   *ready-made oath index* the enrichment track can read meanwhile (it helps, doesn't compete).

## 5. Recommendation
Stage 1 is solid and worth committing as **the corpus-sift track** (one worklog Active Decision naming `sift`/`lens`).
Before a full-corpus run (~400 chapters): (a) eyeball this v2 AGOT output once and veto any of the 33 additions you
dislike (table in the recall-audit; all reversible); (b) decide whether to seed the first `exclusions` from the 32
`I swear` rows or leave that to Haiku. Stage 2 (`interpret`) stays gated/deferred until you greenlight, and it must
iterate **clusters**. Nothing here writes to `graph/` or the harvest queue.
