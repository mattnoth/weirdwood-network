# Stage 4 Recall Expansion — Session 69 Review (for Matt)

*Written 2026-05-24/25. This is a plain-language review of what happened this session,
what we learned, what it cost, and the three decisions waiting for you. Nothing
irreversible was done — we deliberately stopped at the spending gate. Read this top to
bottom; it assumes you've been away from the project for a bit.*

---

## 1. What this session was trying to do

The goal of Stage 4 is to turn our Pass 1 chapter extractions into **graph edges** —
the typed, cited connections between entities ("Eddard `SERVES_AS_HAND_TO` Robert")
that make the knowledge graph traversable. We already have **8,299 entity nodes** and
**~5,750 edges computed** from earlier sessions, but those edges are still sitting in a
staging folder — `graph/edges/` is still empty. So we are close to a traversable graph,
but not there yet.

This session, you decided you wanted to **squeeze more recall out of the Pass 1
extractions before we "formalize" (land edges into `graph/edges/`).** Specifically, you
wanted to mine four Pass 1 tables that we hadn't turned into edges yet:

- **Dialogue of Note** — notable quotes, recorded as speaker → listener.
- **Events & Actions** — bolded action summaries ("Ned confronts Cersei").
- **Information Revealed** — facts disclosed in a chapter + how they were revealed.
- **Food & Drink** — who ate/drank with whom (a first-class target for you by design).

The key constraint you set, and it's the right one: **this is table-mining, not a full
re-read of the books.** Every row here comes from extractions we *already* produced
(all 5 books, done weeks ago). We are not re-reading 344 chapters and we are not
re-fetching the wiki. The only new money is paying an LLM to *label the relationship
type* of pairs we already extracted. A full source-chapter re-read remains **deferred** —
the plan is "get the graph traversable first, enrich later when a real query exposes a
gap."

---

## 2. How the four tables differ (this is why some are cheap and some aren't)

Not all tables are equally easy to mine. It comes down to **table shape**:

- **Columnar tables** (clear columns) → a Python script can pull both the *pair* and
  sometimes the *type* with zero LLM cost. **Hospitality & Guest Right** is like this —
  it already gave us **529 free edges** (`GUEST_OF`, `VIOLATES_GUEST_RIGHT`) in the
  prior session.
- **Dialogue** is semi-columnar: Python gets the *pair* (speaker → listener) for free,
  but the *type* (is this quote a threat? a vow? a plea?) needs an LLM.
- **Events & Actions / Information Revealed / Food** are **free-text prose**. Python
  can't cleanly pull either the pair or the type. To make them usable, we built a new
  Python "candidate generator" that scans each prose row for known entity names and
  forms pairs — then the LLM types them.

That candidate generator is the new, riskier piece, and the smokes below were largely
about testing whether it works.

---

## 3. What we actually did this session

1. **Cleaned up a stale-state contradiction.** The continue prompt claimed "S67 + S68
   are both uncommitted," but the git log showed S67 was *already committed*. Per our
   rule (trust the worklog/git over continue prompts), only **S68** was pending. I
   committed S68 cleanly (`304192ffb`).
2. **Built the candidate generators** (delegated to the script-builder agent) for
   Events / Info / Food, plus a step that anchors every candidate to its real source
   chapter line, plus the Rule-6 "ENCOUNTERS verb-gate" in the typing prompt. 189 tests
   passing.
3. **Wrote the candidates:** 32,194 untyped rows across 344 chapters. (The Events
   fan-out was bigger than expected — 7,128 prose rows became 20,321 candidate pairs.)
4. **Caught and fixed a safety hazard:** the typing script *appended* output to the
   canonical edge folder (`_tail-typed/`, our 2,385 good edges from S67). A smoke run
   would have polluted them. I added an `--output-dir` flag so smokes write to a
   throwaway folder instead, and verified the canonical folder was untouched the whole
   session.
5. **Ran two ~200-row smokes** (small paid test runs) — one for Dialogue, one for
   Events/Info/Food.
6. **Had each smoke independently audited** by a reviewer agent for quality.
7. **Stopped at the spending gate** and wrote this up.

Total spent: **~$3.60.** Canonical data: **untouched.**

---

## 4. What the smokes measured

| Smoke | rows | got typed | rejected | cost | per-row | wall-clock |
|-------|------|-----------|----------|------|---------|-----------|
| Dialogue | 200 | 144 (72%) | 56 | $1.68 | $0.0084 | ~27 min |
| Events/Info/Food | 200 | 123 (61%) | 77 | $1.89 | $0.0095 | ~30 min |

Two things jumped out immediately and they **re-baseline the original estimate**:

- **The full run is ~$270-290, not ~$100.** The earlier ~$100 estimate predated the
  candidate generator. The Events fan-out tripled the row count.
- **The full run is a multi-day job.** Each 40-row batch takes ~5-7 minutes on Sonnet.
  At 32,194 rows that's ~805 batches ≈ **3-4 days of sequential wall-clock**. It would
  have to run on the parallel `run-forever` wrapper, not in one sitting. So the real
  decision isn't "spend $270" — it's "spend $270 *and* babysit a multi-day parallel
  run."

---

## 5. The quality picture (this is the important part)

We didn't just count how many rows got typed — we had a reviewer agent check whether
the typed edges are *correct*. Both reviews came back **"SYSTEMATIC"** — meaning the
errors are not random noise, they're repeatable patterns that would reproduce across the
whole $270 run.

| Measure | Dialogue | Events/Info/Food |
|---|---|---|
| **Strict precision** (clearly correct) | ~60% | ~66% |
| Weak (defensible but thin evidence) | ~28% | ~22% |
| **Wrong** | ~11% | ~12% |
| Reject precision (correctly thrown away) | ~89% | ~91% |
| Direction errors (Events/Info only) | — | ~7% |
| Fan-out spurious pairs (Events/Info only) | — | ~18% |

**The encouraging half:** the pipeline is *good at knowing what to throw away* (~90%
reject precision), and the "relationship-revealing" edge types come through cleanly:
`SIBLING_OF`, `SPOUSE_OF`, `PARENT_OF`, `KILLS`, `DUELS`, `VOWS_TO`, `DISTRUSTS`,
`REVEALS_TO`, `CONSPIRES_WITH`, `BANISHES`, `FIGHTS_IN`. Those are the structurally
valuable edges, and they're solid.

**The problem half:** the damage is concentrated in a handful of fixable places (next
section). At ~60-66% strict precision, a blind full run would put roughly **one wrong or
shaky edge in three** into the graph. For a graph whose whole value is trustworthy
traversal, that's below bar. **But — and this is the headline — the problems are
systematic, which means they're fixable, and the fixes are free.** A noise floor that's
*patterned* is much better news than one that's *random*, because you can target it.

---

## 6. The three problem classes (and why each is cheap to fix)

### Problem 1 — The typing prompt over-uses a few edge types ($0 to fix; needs your input)
The LLM is reaching for certain types where it shouldn't:
- **`INFORMS`** is defined in our schema as a *spy reporting to a handler* (an ongoing
  intelligence relationship). The model used it for any "X told Y something." It was
  **wrong ~100% of the time** in both smokes.
- **`ADVISES`** got applied to rebukes, arguments, and objections — not just genuine
  counsel.
- **`MANIPULATES`** got applied to *open threats*, but the definition requires the
  target to be *unaware* they're being used. (It also caused several
  pointing-the-wrong-direction errors.)
- **`SUPPORTS`** is a theory-evidence type (for our analytical layer) and got misused
  for "one character backs another politically."
- **`ALIAS_OF`** got used for titles like "King Robert" (a title, not an alias).
- **Every single edge was tagged Tier-1 ("verified canon")** — zero confidence
  variation, even for clearly inferred relationships.

*Fix:* restrict which edge types this pass is allowed to emit, and add explicit
"do-NOT-use-X-for-Y" instructions to the prompt. This is the **"lock down the freestyle
surfaces before a long pass"** discipline we already follow. **It's a design decision —
which types to keep vs. drop — so it's yours to make (Decision A below).**

### Problem 2 — The Events/Info candidate generator needs guardrails ($0, pure Python)
This is the new piece, and it has three measurable defects:
- **Fan-out spurious pairs (~18%):** when a row names three+ entities, the
  first-is-the-actor, pair-it-with-everyone-else logic invents edges between people who
  merely appear in the same sentence. Example: `qhorin TRAVELS_WITH ghost` — Ghost is
  Jon's direwolf, not Qhorin's companion; they were just in the same scene.
- **Direction errors (~7%):** "the first-named entity is the actor" fails on passive
  sentences. Example: `varys MANIPULATES sansa` when Varys is actually threatening
  *Ned*, using Sansa as leverage.
- **Bare/garbled entity slugs (~15%):** it emitted edges pointing at `ser`, `lord`,
  `king`, `maester`, bare `mormont` (Jeor or Jorah?), and even `alayne` (which is
  Sansa's alias and should route to our cross-identity logic).

*Fix:* add a direction-validation step and a "slug-quality gate" that escalates
ambiguous references instead of emitting them. **Importantly, this is the same
"endpoint-pollution" problem we already flagged on the 529 Hospitality edges (`walder-frey
VIOLATES all-for-joffrey`, where "All for Joffrey" is a toast, not a person). So this one
fix cleans up several pending threads at once.**

### Problem 3 — A provenance bug ($0, one line)
The typing script hardcodes every emitted edge's source-tag to `pass1_relationship`,
regardless of which table it actually came from. So we'd lose the ability to tell a
dialogue-derived edge from an events-derived one. One-line fix: preserve the real tag.

---

## 7. Which tables are worth it (the reviewer's read)
- **Events & Actions** — most productive; clean movement/conflict/kinship edges.
- **Information Revealed** — noisiest; its multi-entity rows maximize the fan-out
  problem. Recommendation: **defer it** from the first real run.
- **Food & Drink** — lowest signal (who-ate-with-whom is rarely a meaningful edge).
  Recommendation: **separate small audit**, not the bulk run.

---

## 8. Recommended path forward (nothing costs money until step 5)

1. **[$0 — your call]** Decide the restricted edge-type vocabulary + anti-patterns for
   the typing prompt (Decision A).
2. **[$0 — Python]** Add the generator's direction-validation + slug-quality gate (=
   the endpoint filter; also cleans the 529 Hospitality edges).
3. **[$0]** Fix the `candidate_kind` provenance line.
4. **[~$4]** Re-smoke Dialogue + Events (drop Info, hold Food) and confirm strict
   precision climbs to ~80%+.
5. **[decision — Decision C]** Approve the scoped full run at the measured rate, run via
   the parallel wrapper, with drift-detection on.
6. **[$0 — the actual milestone]** Merge everything — the deterministic spine, the S67
   typed tail, the 529 Hospitality edges, and the new typed edges — into `graph/edges/`.
   *This* is the step that turns "edges computed" into "graph you can traverse."

---

## 9. The three decisions I need from you

- **Decision A — Prompt vocabulary.** Should the typing pass be restricted to the
  relationship-revealing types (keep `SIBLING_OF`, `VOWS_TO`, `KILLS`, `DUELS`,
  `REVEALS_TO`, `CONSPIRES_WITH`, `DISTRUSTS`, `BANISHES`, `FIGHTS_IN`, etc.) and drop or
  tightly gate the noisy ones (`INFORMS`, `ADVISES`, `MANIPULATES`, `SUPPORTS`,
  `ALIAS_OF`)? My recommendation: yes.
- **Decision B — Table scope.** For the first real run: **Events + Dialogue only**,
  defer Information Revealed until the generator can handle its multi-entity rows, and
  treat Food as a separate small audit? My recommendation: yes (matches the reviewer).
- **Decision C — Full run.** After the $0 fixes and the ~$4 re-smoke confirm ≥80%
  precision, do we approve the scoped full run (~$200-ish at the restricted scope, via
  the parallel wrapper)? My recommendation: decide *after* seeing the re-smoke numbers.

---

## 10. State of the repo right now

- **Committed:** S68 (`304192ffb`).
- **Uncommitted (this session):** the candidate-generator + `--output-dir` changes to
  `scripts/stage4-pass1-extra-tables.py` and `scripts/stage4-tail-classifier.py` and
  their tests (273 tests green), plus the smoke report and these docs. The
  `candidate_kind` and slug-gate fixes are **not yet done** (they're in the plan above).
- **Gitignored / regenerable:** the 32,194 candidate rows and the smoke output
  (`pass1-derived/_extra-tables/`, `pass1-derived/_smoke-*`).
- **Canonical `_tail-typed/` (2,385 S67 edges):** untouched.
- **`graph/edges/`:** still empty — the formalize/merge (step 6 above) is the milestone
  still ahead.

Full technical detail is in `working/wiki/data/pass1-derived-smoke-report.md`. The
resume instructions for the next session are in
`progress/continue-prompts/2026-05-25-stage4-smoke-fixes-and-formalize.md`.
