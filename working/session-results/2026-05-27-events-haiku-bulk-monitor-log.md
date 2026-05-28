# Events Haiku bulk — monitor log

Run: `_events-haiku-bulk/` (Haiku `claude-haiku-4-5-20251001`, `v5-precision-rules`, sha `d31ca56c4768`).
Candidates: 16,502 cleaned `pass1_events` rows from `_extra-tables/`. 411 batches @ ≤40, 600s pacing, validate-every 25 (drift-halt exit 43, reject floor 0.70).
Bar (Matt's S77 calibration): EDGE CORRECTNESS — flag only when the cited evidence actively fails to support the type; do NOT down-flag a less-than-verbatim quote.

## Checkpoint 1 — first flush (~batch 18, 58 edges on disk) — 2026-05-27 ~19:11 CDT
- Process alive (classifier PID 65078 + wrapper 65068), sleeping between batches. Reject rate ~90% (expected). ~$0.10–0.14/batch.
- Schema clean: `typed_by=haiku`, `prompt_version=v5-precision-rules`, `evidence_kind=book-pass1` on all 58. No ASSAULTS emitted (v5 sexual-only rule holding). `model` field null (provenance carried by `typed_by`).
- **Precision: ~93–96% strict on 58 emitted edges.** 2 clear errors + 2 soft/borderline:
  - `[17]` bran-stark TEACHES joseth-maester — WRONG (direction + bad slug; Joseth is a stableman leading Bran's horse, not a maester, and Bran isn't teaching him). Candidate-slug class.
  - `[57]` robb-stark FEARS sansa-stark — WRONG (Robb fears *for* Sansa the hostage, not *of* her; object/direction error).
  - `[10]` jaime-lannister RESCUES bran-stark — borderline-wrong (the pull-to-sill moment before the push; ATTACKS is captured separately at `[11]`). Over-eager moment-typing.
  - `[19]` bran-stark LOCATED_AT winterfell — borderline-wrong (derived from "I'm Brandon Stark *of Winterfell*" while he's actually ambushed in the wolfswood 2mi out).
- Error class = candidate-slug/disambiguation + over-eager moment-typing, NOT vocab drift or systematic bias. Consistent with the pre-run validation (~85% AGOT / ~90% ACOK).
- Expected dedup at merge: several `(source,target,chapter)` repeats (catelyn→kings-landing ×2, →moat-cailin ×2, →wendel ×2, hodor→bran ×2, osha→bran ×2).
- classify_failed: 1 row (`catelyn ~ trident`, "idx missing or duplicated") = 0.14%. Negligible.
- **Verdict: HEALTHY. Above 75% gate. No action; let it run.**

## Checkpoint 2 — automated validates (batches 25/50/75) — through 2026-05-28 ~10:26 CDT
- `[validate@batch 25: emits=93 rejects=906 reject_rate=0.907 unresolved=0 OK]`
- `[validate@batch 50: emits=184 rejects=1815 reject_rate=0.908 unresolved=0 OK]`
- `[validate@batch 75: emits=297 rejects=2702 reject_rate=0.901 unresolved=0 OK]`
- All > 0.70 floor, unresolved=0, **no drift halt, no rate-limit walls (exit 42), still alive** (PIDs 65068/65078).
- **Position @ 2026-05-28 10:26:** batch **92/411** (319 left); **$11.34 spent** (avg $0.122/batch); proj total ~**$50**; ~2.7 days left @ 600s pacing.
- Edges on disk: **389** (AGOT 236, ACOK 153; ASOS/AFFC/ADWD 0 — candidates are book-ordered, later books not yet reached). All `typed_by=haiku`, 0 ASSAULTS.
- **Verdict: HEALTHY. Run self-driving; no action.**

## Reject-recall (false-reject) baseline — 2026-05-28 ~batch 94 (Matt flagged "most rows getting rejected")
- ~90% reject is **by design**: high-recall candidate set (one row per event line) × precision filter, inflated because the same real pair recurs across many event rows (only one needs to type).
- **25 random AGOT rejects judged: ~0 clear missed edges; ~4 borderline** (`aggo→daenerys` protect, `bowen-marsh→nights-watch` member, `bronn→tyrion` serve, `ogo→lhazareen` sack) — each already captured from a cleaner row OR a group/bad slug (`lhazareen`/`tyroshi`/`royal-fleet`, which *should* be rejected). Large share of rejects = `SIBLING_OF`/`SPOUSE_OF`/`PARENT_OF` duplicates whose edge already exists.
- **Estimated unique-edge recall loss < ~15%** — acceptable per the Haiku trade. The completion read must repeat this check (now a required validation step in the continue prompt).

## Checkpoint 3 — completion
- _pending — must include BOTH a ~25-emit precision read AND a ~25-reject recall read (expect recall loss < ~15%)._
