# SESSION 213 — Roles slice round 2: the next ~50 ranked zero-role events

> **This is Session 213.** Stamp your worklog entry `### Session 213` at endsession.
> **Recommended model:** any orchestrator (the machine is fully proven) + **Sonnet 4.6**
> proposers + **Haiku 4.5** fresh-verifiers. No Fable/Opus needed.
> **PRE-REQ:** S212 committed+pushed (`9832b56def` or later). If `git log` disagrees with
> worklog.md S212, STOP and reconcile.

## Why (S212 continuation)

S212 round 1 minted +236 role edges onto the top-50 zero-role events (edges 26,618); the
**262-event ranked remainder is saved at `working/roles-slice-s212/ranked-all.json`** —
do NOT re-rank. Round 2 = the next ~50 by rank. Value thins toward wiki stubs, so this
round carries an explicit early-stop rule (below). After round 2, the slice is expected
to be DECLARED DONE — the tail isn't worth agent passes.

## Machine (reuse `working/roles-slice-s212/` verbatim — it is the proven template)

1. **Deterministic prep:** re-run `working/roles-slice-s212/scan-rank.py` REGENERATED for
   round 2 (copy to `working/roles-slice-s213/`, point packet-building at ranks 51–100 of
   a FRESH zero-role scan — S212's edges will have absorbed some; events already carrying
   roles drop out naturally). Keep the same score formula.
2. **Early-stop rule (NEW for round 2):** after building packets, eyeball the score curve.
   If the batch's median degree < ~4 or bodies are mostly 1-paragraph wiki stubs, CUT the
   round to only the packets above that floor and note the cut in the worklog. An honest
   30-edge round beats a padded 150.
3. **Sonnet proposers** (3–4, disjoint chunks) using `working/roles-slice-s212/SHARED-RULES.md`
   AS-IS, plus these S212 lessons pasted into each prompt:
   - **Byte-copy quotes, never normalize** — straight-vs-curly apostrophe drift was the
     recurring failure class (S212 fixed 3 cases); copy exact bytes from the chapter file.
   - Umbrella `event.war` nodes: COMMANDS_IN per side + sparing FIGHTS_IN; NO VICTIM_IN.
   - Weddings/incidents/sieges are NOT harm subtypes — no VICTIM_IN onto them.
4. **Haiku adversarial fresh-verify** using `working/roles-slice-s212/VERIFY-RULES.md` AS-IS.
5. **Adjudication with the STANDING deterministic audit** (S212 addition): after verify,
   run the Python check that every kept VICTIM_IN's target event subtype ∈
   HARM_EVENT_SUBTYPES (list in `scripts/fab-reconcile-candidates.py:102`) — the Haiku
   verifier missed one in S212. Also grep prior ADJUDICATION files (S211/S212) for
   re-proposals.
6. `scripts/quotecheck_enrichment.py` → `scripts/mint_enrichment.py` DRY-RUN on scratch →
   **Matt's explicit go** (the S212 autonomous grant was session-scoped — default rule
   applies) → real mint → `scripts/fab-semantic-gate.py` + pytest + deno →
   `python3 scripts/verify_node_quotes.py` if any node prose was touched.
7. Deploy only on Matt's go (bundle regen ships the new edges).
8. **Harvest**: proposers drop pointers per SHARED-RULES; queue is at 0 — a dip adds
   ~25–40, likely tripping the ~30 bar → drain or stage per the endsession rule.

## Watch-outs carried from S212

- `abduction-of-lyanna` stays `event.incident` (deliberate neutrality) — decided S212,
  don't re-propose retyping or the lyanna VICTIM_IN.
- 5 wiki_only + 2 no_node rows parked in `working/roles-slice-s212/parked.json` — don't
  re-propose; wiki-only facts park, they don't mint.
- `riots-in-kings-landing` is typed `event.battle` (questionable but gate-passing) —
  residue note exists in todos; don't relitigate mid-dip.

## Success criteria

A quote-grounded, fresh-verified, deterministically-audited role-edge batch on ranks
51–~100 (mint on Matt's go); the early-stop rule applied honestly; zero gate/suite
regressions; the slice either DECLARED DONE or the remaining tail explicitly documented
as not-worth-it.

## DO NOT

- Do NOT re-rank (use `ranked-all.json` minus newly-roled events).
- Do NOT mint or deploy before Matt's explicit go (S212's grant was session-scoped).
- Do NOT re-propose S211/S212 adjudicated drops or parked wiki_only rows.
- Do NOT pad thin packets to hit a number — apply the early-stop rule.
- Do NOT run /endsession without permission.
