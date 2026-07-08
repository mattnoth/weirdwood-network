# Stage-2 reconciler work — quote repair + §5.1 auto-accept tuning + eval-fix response (S199 continued)

Companion to `EVAL-stage1-reconciler-fix.md` (the Stage-1 fix record) and `EVAL-stage2.md`
(the fresh-subagent quality eval of the Stage-2 extraction). All deterministic, `--smoke`,
nothing minted. Build-time tests `scripts/test-fab-reconcile.py`: **51/51 pass**.

## 1. Quote repair (new, this session)

First Stage-2 reconcile located only **63.7%** of quotes (33/91 quarantined) — far under the
90% gate. Diagnosis (all 33 checked against the source): the extractor **clips quotes
mid-sentence and appends a synthetic terminal '.'** where the source continues with ',' etc.
Content verbatim; only the synthetic final punctuation broke the strict match. 31/33 were
this class; 1 was the known OCR doubled-apostrophe artifact (`Mushroom’'s`); 1 a genuine
comma-inside-close-quote deviation.

**Fix — repair the quote, never loosen the matcher:**
- `locate_or_repair()` (reconciler): strict verbatim first; on miss, retry with trailing
  `[.,;:!?]+` stripped. On a repair hit the **canonical quote** (stored in candidates.json /
  minted to edges) is the stripped, strictly-verbatim form — so `mint_enrichment.authoritative_line`
  matches it **unchanged**; no locator change on the mint side. Repairs logged to a new
  sidecar `quotes-repaired.jsonl` + `quotes_repaired` in run-summary.
- `norm()`: collapse OCR doubled apostrophes (`''`→`'`) — mirrored **byte-identically** in
  `mint_enrichment.py` (lockstep; covered by 3 lockstep tests).

**After:** Stage 2 = **98.9% located** (1 quarantined — the genuine deviation, correctly held).
Stage-1 re-run: routing/edges byte-identical (39 matched / 134 review / 6 created / 51 edges);
quarantine 4→3 (the `Aegon’'s` quote recovered via the norm change; the 2 `Dorne,"` deviations
still correctly quarantined). No regression.

## 2. §5.1 auto-accept tuning (design bucket 2: tiered discriminator accept)

Tuning population: the **23 `smoke-auto-accept-disabled` rows** across both smoke units
(10 heirs + 13 conquest), each hand-ground-truthed against canon + node files.

**Original rule** (top ≥2 discriminators AND runner-up has ZERO hits): 6/23 accepted, all
correct — 100% precision, ~30% recall. It blocked correct 2-vs-1 cases where the runner-up's
only hit was one the top candidate also carries (a shared "prince" title hit discriminates
nothing).

**Three changes:**
1. **Scorer recall — parent/spouse base-name matching.** Cluster members store parents/spouse
   as full slugs (`jaehaerys-i-targaryen`) but roster Disambiguators write "son of Jaehaerys I"
   (no surname), so the token-subset match never fired. New fallback: match the relative's
   base first name (first slug token, ≥4 chars). ALL matching (a)-fields are now recorded
   (needed for the margin rule below); category (a) still contributes max 1 to the score.
2. **Scorer recall — punctuation-tolerant tokens.** Disambiguators are ';'-separated;
   a token adjacent to the separator ("the Tides;", "Princess;") failed to match its
   discriminator. Tokenization now strips punctuation (scorer-local; the shared
   `weirwood_query.normalize` is untouched).
3. **Margin rule.** Accept iff top ≥2 AND top **strictly** outscores runner-up AND the
   runner-up brings **no evidence the top lacks** (hit-set subset, anchor-count normalized).
   Ties and runner-up-only evidence still go to review.

**Result on the 23-row tuning sample: 15 accepted — 0 wrong — 8 to review.**
Both danger rows behave: *Rhaena Targaryen* (top candidate is the WRONG person, scored 1 on
pack-expected alone) stays in review — proof pack-expected alone must never accept; *Ronnel
Arryn* (only candidate is Jon Arryn's brother, not the boy king) stays in review at score 0.
The direction-confusion trap self-contains: Baelon the Brave's disambiguator names his son
Viserys, which hands the wrong candidate (`…son-of-viserys-i`) a parent hit → 2-2 tie → review.

**✅ VALIDATED OUT-OF-SAMPLE (same session, later window).** Matt fired the two fresh units
(`fab-heirs-of-the-dragon-15-p02`, `fab-sons-of-the-dragon-05-p01`); both reconciled `--smoke`
and every would-accept row was adversarially ground-truthed by a fresh subagent
(`EVAL-oos-accept-validation.md`): **0 wrong accepts across 66 rows** (8 discriminator + 58
exact-1.0) — gate PASSES. Highlights: the two different Rhaenys Targaryens across units resolved
to different correct nodes; `Samwell Tarly` → `samwell-tarly-lord` (Savage Sam, 37 AC), not POV
Sam; the review-held rows were exactly the dangerous ones (sons' `Vulture King` candidate is the
Dance-era third Vulture King — an accept would have corrupted; the tie forced review as designed).
Rule errs conservative-only: Corlys/Jason Lannister/Balerion (pack-only score 1) review-held
despite correct tops.

**p02 also surfaced a NEW extractor drift class, fixed same window:** the p02 worker wrapped
every evidence-quote cell in literal `"…"` marks → 35.6% located / 0 edges. `locate_or_repair`
now strips one enclosing quote pair as a repair variant (dialogue quotes match strict-first,
untouched; canonical stays strictly verbatim; tests 54/54). After: **94.1% located, 69 edges,
disputed_rate 0.101** — the Mushroom/Eustace dispute machinery works under real load (the
EVAL-stage2 open question). Sons unit: 95.0% located, clean. Also added: mechanical edge-type
vocab guard (canonical 170 from `edge-type-counts.json`; off-vocab → review, never emitted) —
zero drift found across all 4 units.

**CREATE fresh-verify on the fresh units** (`EVAL-oos-create-verify.md`): one firm semantic dupe
in EACH unit (3-for-3 units now — the step stays mandatory): `accession-melee-at-maidenpool` =
existing `tourney-for-king-viserys-is-accession`; `death-of-alyn-stokeworth` = existing
`harren-the-reds-rebellion`. Plus: `daemon-slays-craghas-crabfeeder` = DUPE-RISK of
`war-for-the-stepstones` (fold or mint-with-PART_OF); renames `birth-of-aegon` →
`birth-of-aegon-ii-targaryen` and `birth-of-maegor-targaryen` → `birth-of-maegor-i-targaryen`
(bare `maegor-targaryen` is a declared disambiguation hub); **schema decision — DECIDED (Matt,
2026-07-07): the 4 novel event subtypes are ADOPTED** — `event.appointment`/`event.exile`/
`event.birth`/`event.investiture` added to the architecture.md type table (rule 6 sync done same
window), incl. the `birth-of-<canonical-char-slug>` slug convention. Incidental drift noted while
in there: `event.death`/`event.capture`/`event.ceremony`/`event.council` are live in the graph
but undocumented in the table (pre-existing, todo). Undated events fall back to section era
(2 of 8 p02 CREATEs) — acceptable, reviewable.

## 2b. Response to EVAL-stage2's ranked fixes (all reconciler-side items landed)

EVAL-stage2 verdict: **PASS-WITH-CONCERNS** — extraction strong, zero hallucinations, quote
repair verified sound 31/31; two NEW blockers, both fixed same session:

1. **Type-agreement gate (BLOCKER, R1 class)** — clean-hit routing was type-blind: `Lorath`
   (place) UPDATE-routed onto `jaqen-hghar` (character) via a junk alias. Rule-1/redirect hits
   now check roster `Type guess` ↔ node category (`GUESS_CATEGORY` map); mismatch → review.
   Re-run caught a SECOND live wrong-match the eval passed: `Sea Snake` (ship) → `corlys-velaryon`
   (person). Both now review. (`jaqen-hghar`'s junk `"Lorath"` alias = graph fix at apply-go.)
2. **`run_id` part-suffix (BLOCKER, bulk)** — now `<unit>-<date>` incl. `-pMM` (was: p01/p02/p03
   shared a run_id → merge idempotency silently dropped parts 2–3). Spec amended.
3. **Cites carry the part** — merge-plan cites now `(fab-…-15-p01:LINE)` (line numbers are
   per part-file; cites must open).
4. **Review-candidate recall** — review rows now get pack + name-token probe suggestions
   (the `Septon Eustace` row now presents `eustace-dance-of-the-dragons`).
5. **Exact-1.0 accept (review-flood drain)** — accept iff exact-normalized 1.0 top, margin ≥0.2,
   not blocklisted, and **POSITIVE** type agreement (no roster guess → never accepts; ships/legends
   `Cod Queen`/`Merling King` stay review). Would-accept on the two smoke units: **130 rows**
   (48 heirs + 82 conquest — houses, seats, cities; spot-checks incl. `Stone`/`Sky` waycastles all
   correct). Real-run review load drops ~60%: heirs 87→~31, conquest 134→~44.
6. **Type normalization** — `event.tourney`→`event.tournament`, bare `place`→`place.location`,
   bare `house`→`organization.house`, `dragon`→`character.dragon` (TYPE_SYNONYMS + BARE_TYPE_DEFAULTS).
7. **Merge-plan hygiene** — orphan-punctuation bullets cleaned, dead-cite bullets held (never
   written), blank-start join-window cites now point at actual text (mirrored byte-identically
   in mint's `authoritative_line`), and a new `matched.jsonl` sidecar (name→slug audit surface).

NOT done here (out of reconciler scope): extractor `VICTIM_IN`-for-estrangement nit (eval fix 9,
harmless/review-held); `jaqen-hghar` alias strip (graph write — apply-go). The dispute-machinery
smoke happened via the out-of-sample p02 unit (see the validated section above).

## 2c. `identity_line` — DECIDED (Matt 2026-07-07): WIRED
`derive_identity_line()`: first Node-Prose bullet → `"<Name> — <text>."` (skip on pronoun-opener /
empty / >300 chars; un-doubled when the bullet already starts with the name). The merge writer
swaps ONLY boilerplate Identity lines, so supplying it is always safe. Coverage on the 4 smoke
units: **58/58 merge-plan entries**; 18 of 48 distinct target nodes currently carry the literal
"…from the AWOIAF wiki." placeholder and will be upgraded at apply. Strip-boilerplate track's
sequencing premise (parked behind F&B *because* F&B swaps these lines) is preserved.

## 2d. §7.2 dispute-axis gate: FAIL → dispute-proximity quarantine → re-audit
First formal stratified audit (`EVAL-dispute-axis-audit.md`): **FAIL** — over-tag 0.0% but
missed-hedge **26.9%** (tier inflation). Root cause: the extractor tags sentence-LOCAL hedges
perfectly but is blind to PASSAGE-scope dispute framing ("Here is where our sources diverge" …
"Of the aftermath, these things are certain") — one un-hedged sentence in the p02 exile zone
minted 6 tier-1 artifacts, incl. an event node whose slug encodes the disputed cause.

**Fix (reconciler, deterministic — extraction prompt untouched):** dispute-proximity quarantine.
Untagged edges/events/prose whose located line sits within ±1 line (fab files are
paragraph-per-line) of a STRONG hedge term — chronicler names + explicit divergence framing —
are HELD to a new `dispute-review.jsonl` sidecar (never emitted) unless a certainty marker sits
at least as close; untagged `LOVER_OF`/`PARAMOUR_OF` always held (insinuation-inflation class).
Held ≠ demoted: adjudication happens at apply via the per-unit fresh-verify (verdict-gates-apply)
so the quarantine cannot cause tier deflation. Lexicon+window tuned empirically
(`scratchpad/tune_window.py`): weak generic hedges ("rumor", "it was said", "some say") EXCLUDED —
measured, they caused 100% of false holds on audit-certified-clean units and 0 real catches.
Result: p02 holds 17 (the full exile cluster + Mushroom's wedding-tourney version + romance
class), p01 holds 2, sons/conquest hold 0.

**Re-audit (`EVAL-dispute-axis-audit-v2.md`): GATE PASS** — missed-hedge 0.0% (0/26; was
26.9%), over-tag 0.0% (0/7), quarantine recall 100% on the prior failure set; the certainty
rescue verified in both directions. Non-gating residuals, documented for bulk-scale refinement:
(a) false-hold rate 52.6% — mostly "mushroom" in non-attributive roles (nickname
parentheticals, Mushroom-as-courtier) and the self-referential trap (prose ABOUT Mushroom);
cheap fixes if adjudication volume annoys: attributive-frame check, sentence-window proximity.
(b) weak narrator hedges ("it was said", "reportedly") aren't in the lexicon — zero escapes in
these 4 units (the extractor tags sentence-local hedges reliably), but `disputed_rate`+
`dispute_held` in run-summary are the bulk drift alarms for this class.

## 3. Stage-2 CREATE batch fresh-verify (standing per-unit step)

`fresh-verify-creates.md` (fresh adversarial subagent): **1 semantic dupe caught of 4** —
`baelon-avenges-aemon-on-tarth` = existing `myrish-bloodbath` (92 AC, same event; the Baelon
node names it). Disposition at apply: fold as UPDATE onto `myrish-bloodbath`, don't CREATE.
Second unit in a row where the fresh-verify caught what the deterministic resolver can't —
the step stays mandatory per unit. Also flagged: `summoning-of-vaegon` should carry
CAUSES → `great-council-of-101-ac`; `nghai` body is nearly empty; type-name normalize
`event.tourney` → `event.tournament`; all 4 CREATEs stamped `era: dance-of-dragons` though
they're 92–101 AC events (section-map granularity — acceptable? flag for apply-go).
Incidental graph flags for triage (NOT this track): `vaegon` vs `vaegon-targaryen` dupe pair;
`great-council-of-101-ac` mistyped `event.battle` with empty body.
