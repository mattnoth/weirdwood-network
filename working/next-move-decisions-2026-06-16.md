# Next-Move Decisions — START HERE (post-/endsession, 2026-06-16)

> **Purpose:** the four decision entry points for the next session. This session (2026-06-16) re-ran the
> Mode 3 dip, decided the events/time + era schema, and SHIPPED deterministic event dating + `narrative_first`.
> Everything below is a DECISION for Matt, not mechanical work. Pick one to make it the live continue prompt.
> Session detail: `working/session-results/2026-06-16-event-dating-APPLIED.md`.
>
> **UPDATE (S102, 2026-06-16):** Decision **#3 (dating leftovers) is DONE** — see the struck §3 below and
> `history/session-details/session-102.md`. S101's dating + S102's cleanup are both committed. **3 decisions
> remain (#1 PRECEDES/FOLLOWS · #2 causal TRIGGERS · #4 Fable).** Board roadmap: #1 → #2 → #4.

---

## 1. `PRECEDES` / `FOLLOWS` ordering edges  — GATED on a schema decision + a grouping strategy
- **Why gated:** these edge types are NOT in the locked vocab; they're an *explicitly deferred* schema decision
  (roadmap **D3**: "OCCURRED_IN_YEAR/PRECEDES/FOLLOWS are NOT in the schema"). And **0 of the 112 dated events
  share a `PART_OF` parent**, so there's no cluster to derive *meaningful* local ordering from.
- **Decisions needed:** (a) approve adding `PRECEDES`/`FOLLOWS` (and maybe `OCCURRED_IN_YEAR`) to the locked
  edge vocab in `architecture.md` — NOTE this shifts the vocab-count test baseline (currently 3 documented fails
  reference a 163 count). (b) Pick the grouping basis: order within a shared war/conflict? globally within an
  `era`? cross-year only (safe) with same-year left unordered (or broken by `narrative_first`)?
- **Cost/risk:** $0 deterministic once decided; additive + reversible. Cross-year ordering is rock-solid;
  same-year needs `narrative_first` (now available on 29 events) as tiebreaker.

## 2. Causal `TRIGGERS` / consequence edges  — the dip's MEASURED gap; needs sign-off
- **Why it matters:** both dips flagged this (Battle of the Trident has participants + now a date, but 0
  consequence edges → can't answer "what did X lead to"). Highest measured query-value.
- **Why gated:** causation is interpretive — pollution-sensitive ("a wrong cited edge is worse than none").
  Not safe to auto-execute.
- **Recommended approach:** curator-guided pilot on the **Robert's Rebellion chain** (Harrenhal 281 → Trident 283
  → Sack 283 → Tower of Joy), which now has participants (historical-anchor waves 1+2) + dates. Sonnet, small
  pilot, Matt reviews before any bulk. Vocab: `TRIGGERS` may also need a vocab add (check before minting).

## 3. ~~Staged leftovers from the dating pass~~  — ✅ DONE S102 (advisory board pick; all sub-items resolved)
> **Resolved S102:** 4 spans dated as ranges (`dance` 129–132, `wo5k` 298–300, `greyjoy` 289–290, `regency` 131–136);
> `first-blackfyre` = single-year 196 (212 dropped as wiki cross-link error); `long-night` = `ac_year:null`/
> `precision:relative-only` (297 mention-index error excluded); `conquest-of-dorne` verified (date on event, not book);
> 10 mistyped year-page nodes DELETED + indexes/alias-resolver resynced. Detail: `history/session-details/session-102.md`.

- **5 multi-year spans** need `ac_year_end`/split decisions: `dance-of-the-dragons` [129–132],
  `war-of-the-five-kings` [298–300], `greyjoy-rebellion` [289–290], `regency-of-aegon-iii` [131–136],
  `first-blackfyre-rebellion` [196,212] (the 212 looks like a wiki page error).
- **`long-night`** — excluded from dating (prehistoric; wiki mis-listed it at 297 AC). Should get
  `ac_year: null` + `precision: era` (or epoch era) rather than stay bare.
- **`conquest-of-dorne`** — dated as an event, but an S96 cleanup retyped a `conquest-of-dorne` to `object.text`
  (it's also an in-world book). Confirm the dated node is the event, not the book.
- **10 mistyped year-page nodes** (`283-ac.node.md` etc.) sit in `graph/nodes/characters/` as `character.human`
  — they're year pages. Type/dir decision (the deferred `event.year`/chronology-dir question in architecture.md
  TYPE_DIR_MAP). The dip's Q4 ("what happened in 283 AC") tripped on this.

## 4. Fable cleanup — the original loose end (your S100 observation)
- **Nomenclature sweep** (the "track/plate" verbiage) — GATED on you picking a scheme from
  `working/nomenclature-reform-proposal.md`.
- **Repo / working-dir reorg** — plan exists at `working/repo-reorg-plan-2026-06-12.md` ("plan only, no moves");
  never executed. Risk-ordered sequencing inside.
- Both were delivered by the Fable audit as proposals only; neither was ever executed.

---

### Suggested ordering (not binding)
If the goal is query-value: **#3 cleanups (cheap, finishes the dating track) → #1 ordering edges → #2 causal
(the real measured gap) → #4 Fable cleanup**. But #4 is your call — it's been waiting since the audit.
