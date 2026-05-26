# Stage 4 Tail-Classifier Prompt Review — Independent Reviewer (Opus, #2)

**Date:** 2026-05-25
**Reviewer:** independent fresh-eyes pass (READ-ONLY; proposes text, edits nothing)
**Target file:** `scripts/stage4-tail-classifier.py` — `render_classify_prompt` / `_PROMPT_PREAMBLE` / `build_vocab_block` / gated-type machinery
**Spec:** `reference/architecture.md` (`## Edge Types`)
**Grounding data:** `working/wiki/data/pass1-derived-quote-relevance-measure.md` (smoke3 107-row + v1 3,842-row), `pass1-derived-smoke2-headtohead-review.md`, `pass1-derived-v1-refine-proposal.md`
**Goal:** strict precision 60% → ~75–80% via *surgical, consolidating* prompt changes.

---

## TL;DR — my position

The prompt is already long (14 numbered rules, three overlapping anti-pattern blocks: Rules 9, 11, 12, 14). It grew by **accretion** — one rule per discovered failure mode. The 60% audit is not telling us we need 5 more per-type rules; it is telling us the model is **over-emitting on under-evidenced rows** and **inferring relationships the quote does not state**. Those are two root causes that cut across most of the observed bias list.

My ranked recommendation is therefore **consolidate, don't accrete**:

1. **#1 (biggest gain): an evidence-grounding rule** — the edge must be supported by the `evidence_quote` itself, not the `hint` and not world-knowledge. This single rule directly kills the `chett KILLS mormont`, `cersei COURTS hand-of-the-king`, `jaime PARENT_OF tommen`, and most MOTIVATES/SEEKS/TEACHES over-application cases.
2. **#2: a default-to-REJECT asymmetry statement** — make "a missing edge is recoverable; a wrong cited edge is graph pollution" an explicit decision rule, not just the passive "REJECT if … does not clearly support" in Rule 4.
3. **#3: one consolidated co-presence principle** — fold the scattered "two people in a scene is not an edge" language (currently duplicated across Rules 6, 11 CONTEMPORARY_WITH, 11 COMPANION_OF, 12) into a single stance rule, and add a **completed-vs-planned** clause to it.
4. **#4: targeted gating** — promote OPPOSES, MOTIVATES, COMMANDS, and the courtship/instruction cluster (COURTS / SEEKS / TEACHES / TUTORS) to the `[GATED]` treatment so the directionality + anti-pattern note travels *inline in the vocab list* where the model reads it at decision time.

Crucially, #1–#3 are **net-shorter or net-neutral** if we let them *replace* the redundant per-type prose already in Rules 6/11/12/14. The prompt does not have to get longer to get better.

---

## Part A — Per-bias remedies (exact text)

For each: the exact text to add, the bias it targets, and honest over-rejection risk.

### A1. Evidence-grounding rule (NEW Rule, highest priority)

**Targets:** `chett KILLS mormont` (foiled-plot → completed KILLS), `cersei COURTS hand-of-the-king`, `gerris-drinkwater MOTIVATES quentyn`, `jaime PARENT_OF tommen` (Sonnet's worst error — world-knowledge overrode a denial in the quote), and the broad class of "model leaned on the hint or series knowledge."

**Exact text (insert as Rule 4a, immediately after Rule 4):**

```
4a. EVIDENCE-GROUNDING — the edge MUST be stated by the evidence_quote itself.
    - The `hint` is a candidate label, NOT proof. The `evidence_quote` is the only
      proof. If the quote does not state the relationship, REJECT — even if the hint
      asserts it and even if you know it is true from the books.
    - Do NOT supply a relationship from world-knowledge. If the quote shows a character
      DENYING or merely DISCUSSING a relationship, that is not evidence FOR it.
      (Error to avoid: emitting PARENT_OF from a quote where the parent denies paternity.)
    - PLANNED, ATTEMPTED, FORGOTTEN, or HYPOTHETICAL actions are NOT completed facts.
      A foiled or merely-intended killing is NOT KILLS. A planned meeting is NOT
      ENCOUNTERS. If the quote frames the action as future, conditional, failed, or
      hypothetical ("would", "tried to", "if … should", "planned to", "forgot and tried"),
      REJECT or pick a type that fits the actual (non-completed) state.
```

**Over-rejection risk: MEDIUM-LOW, and acceptable.** This is the highest-leverage rule but it interacts with a known data artifact: per `pass1-derived-v1-refine-proposal.md`, ~50.9% of v1 quotes do not name both endpoints by literal token (pronoun substitution, window artifacts). A naive reading of "stated by the quote" could push the model to reject valid pronoun-referenced edges (`catelyn TRUSTS brienne` from `"…Brienne, she prayed"`). The rule above is deliberately worded around *the relationship being stated* (semantic), not *both names appearing* (lexical) — pronoun/"my father"/title references still count as long as the relationship is asserted in the quote. The real precision win here is the planned-vs-completed clause and the "hint is not proof / deny is not assert" clause, which carry near-zero recall cost because those rows are genuinely wrong. Pair this rule with the existing deterministic quote-relevance *soft-flag* (not a hard drop) downstream — the measurement doc already concluded the lexical filter is too blunt to gate on alone.

### A2. OPPOSES → require sustained enmity, not a one-off argument

**Targets:** `jaime OPPOSES tywin` ("I am tired of having highborn women…"), `sansa OPPOSES joffrey` ("I don't want to marry you…"), `val OPPOSES jon`, `stannis OPPOSES melisandre` — one-off disagreements, refusals, and rebukes, frequently *between allies/family*, typed as standing enmity. OPPOSES is the #3 most QR-flagged type in v1 (125 flags).

**Recommended remedy: fold into the gated-vocab note (see Part C), with this text:**

```
OPPOSES — sustained active enmity or standing political/personal opposition, symmetric.
  NOT for a single argument, refusal, rebuke, or moment of friction — especially
  between allies, kin, or a master and servant who are otherwise aligned. A one-time
  disagreement is not enmity. If the quote shows only a single clash, REJECT or use a
  narrower evidenced type (REVEALS_TO, RESENTS) — do NOT default to OPPOSES.
```

**Over-rejection risk: MEDIUM.** Some genuine OPPOSES edges are evidenced by a single sharp exchange. But OPPOSES is symmetric and standing-state; the cost of a missed OPPOSES is one recoverable edge, while a wrong OPPOSES between allies (Jaime/Tywin, Davos/Stannis) is actively misleading for traversal ("who opposes whom"). Net positive.

### A3. COMMANDS → forbid the two-hop A→C collapse

**Targets:** `joffrey COMMANDS tyrion` ("The men would carry her up to her wedding bed…"), `cersei COMMANDS ilyn-payne` / `cersei COMMANDS mandon-moore` (orders given *about* a third party, or to a guard about a task), `robert COMMANDS kingsguard`. The classic pattern is "A orders B to do something involving C" being typed COMMANDS A→C. COMMANDS is the #6 QR-flagged type (93 flags).

**Recommended remedy (gated note text):**

```
COMMANDS — direct military/organizational command from a superior to the person under
  their command. Direction: Commander → the COMMANDED person.
  - When the quote is "A orders B to act on/against C", the edge is A → B (the person
    commanded), NEVER A → C. Do NOT collapse the chain to the third party.
  - Requires a standing command relationship or an explicit order in the quote, not
    mere authority or co-presence. If the row pairs A with C (the object of the order,
    not the subordinate), REJECT.
```

**Over-rejection risk: LOW.** The candidate's `source_slug`/`target_slug` are FIXED — the model cannot re-target to B. So in the A→C two-hop case the *only* correct action is REJECT, which is exactly what we want. This rule has essentially zero recall downside because A→C COMMANDS is always wrong by directionality.

### A4. TRAVELS_WITH / SEEKS / COURTS / TEACHES / TUTORS → the co-presence/single-act gate

**Targets:** `gendry TRAVELS_WITH arya` (window artifact), `old-nan TEACHES bran` ("Dragons… It be dragons, boy" — a single line of storytelling), `grenn SEEKS mormont` (checking a body for a pulse), `bella COURTS gendry` / `quentyn COURTS drinkwater-twins` (a flirtation / a line of banter), `cersei COURTS hand-of-the-king` (a touch + a political line). These all share one root: **a single question, flirtation, casual instruction, or co-presence inflated into a sustained directed relationship.**

**Recommended remedy: handle via the consolidated co-presence principle (B3) plus inline gated notes:**

```
SEEKS — an active, stated pursuit of a person/artifact/knowledge across the narrative.
  NOT a single question, a glance, or checking on someone. REJECT if the quote shows
  only a one-off interaction.
COURTS — an active suitor relationship (pre-betrothal pursuit of marriage). Requires
  suitor language in the quote ("sought her hand", "courted", "asked for her hand").
  A flirtation, a single touch, banter, or one charged line is NOT courtship. REJECT.
TEACHES / TUTORS — transmission of a skill/knowledge over time. A single anecdote,
  story, or remark is NOT teaching. TUTORS additionally requires a sustained one-on-one
  mentorship explicitly evidenced. If the quote shows one casual exchange, REJECT.
```

**Over-rejection risk: MEDIUM for COURTS/SEEKS, LOW for TEACHES/TUTORS.** COURTS is rare and high-signal when right; the risk is missing a genuine suitor named only obliquely. But the failure rows (`bella`, `cersei`, `quentyn`) are clearly wrong and pollute a low-volume, high-value edge type. TEACHES/TUTORS over-application is almost always wrong (`old-nan TEACHES bran` from a single line), so the gate is nearly free.

### A5. MOTIVATES → person-as-source is a directionality/type error

**Targets:** `gerris-drinkwater MOTIVATES quentyn` (person→person). Spec: `MOTIVATES = Event or condition drives a character's actions`; direction `Motivation → Actor`. The source must be an event/condition, not a person acting on another person.

**Recommended remedy (gated note text):**

```
MOTIVATES — an EVENT or CONDITION drives an actor's behavior. Direction: Motivation
  (event/condition) → Actor (person). The SOURCE must be an event or condition node,
  NOT a person. Person → person is never MOTIVATES — if a person persuades/urges another,
  that is REVEALS_TO, ADVISES (if an institutional advisor), or REJECT. If the source
  of this row is a character, do NOT emit MOTIVATES.
```

**Over-rejection risk: VERY LOW.** This is a hard type-contract: MOTIVATES with a character source is categorically wrong. Could be promoted to a mechanical type-contract validator (like the existing ECHOES_char_char check) rather than living in the prompt at all — see B4.

---

## Part B — Position on the four framing questions

### B1. Default-to-REJECT vs more type rules — **YES, make REJECT the dominant lever.**

This is my second-highest-leverage recommendation. Rule 4 today is passive ("REJECT if hint+evidence does not clearly support any vocab type") and — note the bug — it tells the model to lean on the **hint**, which A1 explicitly forbids. The asymmetry of the two error types is never stated to the model. Add this as a top-of-prompt stance, right after Rule 1:

```
1a. WHEN IN DOUBT, REJECT. The two outcomes are NOT symmetric:
    - A missing edge is recoverable — a later pass can add it.
    - A wrong cited edge is graph pollution — it asserts a false relationship with a
      real citation, which is worse than no edge at all.
    Therefore: only emit a type when the evidence_quote makes it CLEAR. If you are
    weighing two plausible types, or talking yourself into a type, REJECT.
    REJECT is a correct, expected, common answer — not a failure.
```

**Why this over N more type rules:** the 60→76% gain already documented (`smoke2-headtohead`) came partly from *gates that push toward REJECT* (the ENCOUNTERS verb gate, the RESPECTS evidence gate). The residual errors are overwhelmingly **over-emission** (Haiku "over-emits on thin evidence" per the head-to-head; emit/reject was 137/63 — REJECT is under-used). A general REJECT-bias rule attacks the *shared* cause of OPPOSES, COURTS, SEEKS, TEACHES, MOTIVATES, COMMANDS-two-hop, and KILLS-foiled-plot simultaneously. Per-type rules attack them one at a time and the prompt is already saturated with them.

**Honest caveat:** REJECT-bias trades precision for recall. Given the project's stated value ("graph quality for agent traversal" — `project_real_goal_graph_for_agents`) and the explicit framing that a missing edge is recoverable while a polluted edge is not, this trade is correct *for this project*. If a later session finds recall has collapsed (emit rate << current ~68%), dial it back. The smoke harness already measures both, so this is observable.

### B2. Evidence-grounding rule — **YES, this is the single highest-value change.** See A1.

The grounding data proves the case. `pass1-derived-quote-relevance-measure.md` shows the `chett KILLS mormont` row's quote is *"Or Small Paul forgot and tried to kill Mormont during the second watch…"* — a hypothetical foiled plot, typed as a completed KILLS at emit-confidence. `cersei COURTS hand-of-the-king` rests on *"…Her hand touched his face…"* — a touch, not courtship, with the relationship inferred from world-knowledge of the Cersei/Hand dynamic. `smoke2-headtohead` documents `jaime PARENT_OF tommen` from a quote where Jaime *denies* paternity. Every one of these is the model trusting the hint or its own knowledge over the quote. A1 is the direct fix and it generalizes beyond the named cases.

The lexical/pronoun caveat (B's risk) is real but already solved by keeping the *lexical* quote filter as a downstream **soft flag** (`_qr_warning`), per the existing v1-refine decision. The prompt rule should be *semantic* ("the relationship must be stated"), the Python filter *lexical* ("are both tokens present") — two complementary layers, neither over-applied.

### B3. Co-presence principle — **YES, consolidate; it replaces more than it adds.**

Today the "co-presence is not an edge" idea is spelled out **four separate times**: Rule 6 (ENCOUNTERS), Rule 11 CONTEMPORARY_WITH, Rule 11 COMPANION_OF, and implicitly Rule 12 RESPECTS. That is accretion. Replace the redundant fragments with **one principle stated once**, then let the per-type notes reference it tersely:

```
CO-PRESENCE PRINCIPLE (applies to every type):
  Two entities sharing a scene, room, meal, march, battle, court, or passage is NOT,
  by itself, a typed relationship. An edge requires an ACTION or STANCE directed from
  the SOURCE to the TARGET, stated in the evidence_quote.
  - Same scene → not COMPANION_OF, not TRAVELS_WITH, not ENCOUNTERS, not RESPECTS.
  - Two people co-present in time → not CONTEMPORARY_WITH (that is for two EVENTS).
  - If the only thing the quote establishes is that both were present, REJECT.
```

**Net effect on length:** this lets you *cut* the bulk of Rule 11's CONTEMPORARY_WITH and COMPANION_OF prose and Rule 12's first two bullets, because they become instances of the principle. The prompt gets **shorter and clearer**. And it fixes more than piecemeal rules because it states the *general* failure (co-presence inflation) once, so the model applies it to types you didn't enumerate.

**Over-rejection risk: LOW.** TRAVELS_WITH legitimately covers co-presence "in attendance at court/event" per spec — so the principle should *not* nuke TRAVELS_WITH outright. The wording above says co-presence is not *automatically* an edge and requires a directed action/stance; TRAVELS_WITH's spec already requires the journeying/attendance relationship to be evidenced, so a real "Robett kneeling among Catelyn's welcomers" still qualifies. Watch TRAVELS_WITH recall in the next smoke; if it dips, add one carve-out line.

### B4. Additional gating candidates — promote these to `[GATED]`

Current `DEFAULT_GATED_TYPES = (INFORMS, ADVISES, MANIPULATES, SUPPORTS, ALIAS_OF)`. The `[GATED]` marker is valuable specifically because it appears **inline in the vocab list** (`build_vocab_block`), i.e. at the exact moment the model is scanning for a type — far more likely to be read than a rule 200 lines up. Add, in priority order:

1. **OPPOSES** — highest-volume false-positive in the bias list (one-off arguments). #3 QR-flagged.
2. **MOTIVATES** — categorical direction/type error (person source). Cheap, near-zero recall cost.
3. **COMMANDS** — two-hop collapse; #6 QR-flagged. The `[GATED]` note carries the directionality reminder inline.
4. **COURTS** — low-volume, high-value, easily polluted by flirtation/banter.
5. **SEEKS** — single-question inflation.
6. **TEACHES** / **TUTORS** — single-anecdote inflation (TUTORS especially, since "sustained one-on-one" is its whole definition).
7. **KILLS** — to carry the planned-vs-completed reminder inline (`forgot and tried to kill` → REJECT).

Note: CONTEMPORARY_WITH, COMPANION_OF, ASSAULTS, NURSED_BY, CITED_BY, CONTRADICTS, ECHOES, RESPECTS already have anti-pattern coverage (Rules 11/12/14). Folding them under the consolidated co-presence principle (B3) + the gated-vocab inline notes lets you **retire the standalone Rules 11/12/14 prose** and move their essential one-liners into the inline `[GATED]` annotations — net reduction in prompt length.

**Type-contract validator candidates (move OUT of the prompt entirely):** MOTIVATES-with-character-source and COMMANDS-A→C-where-target-is-not-a-subordinate are mechanically checkable, like the existing `ECHOES_char_char` / `RULES_char_target` contracts in `stage4-type-contract-validator.py`. Mechanical enforcement is more reliable than prompt text and frees prompt budget. MOTIVATES (source must be `event.*`/`concept.*`) is the cleanest candidate.

---

## Part C — Concrete consolidation sketch (what the prompt becomes)

The recommendation is a **refactor, not an expansion**. Target structure:

- **Rule 1** (JSON format) — unchanged.
- **Rule 1a** (NEW) — when-in-doubt-REJECT asymmetry (B1).
- **Rule 4** — fix the bug: change "REJECT if hint+evidence does not clearly support" to "REJECT if the **evidence_quote** does not clearly support" (the hint is not proof).
- **Rule 4a** (NEW) — evidence-grounding + planned-vs-completed (A1).
- **CO-PRESENCE PRINCIPLE** (NEW, stated once) — (B3), replacing the duplicated fragments in Rules 6/11/12.
- **Rules 5, 13** (direction) — keep; these are load-bearing and correct.
- **Rule 6** (ENCOUNTERS verb gate) — keep (validator-enforced), but trim the co-presence prose now covered by the principle.
- **Rules 9, 11, 12, 14** — collapse into the **inline `[GATED]` notes** in the vocab block. Each gated type gets a one-line anti-pattern note shown *where the model picks the type*. Expand `DEFAULT_GATED_TYPES` per B4.
- **Rule 10** (tier assignment) — keep.

Net: ~4 fewer free-standing rule blocks, one new principle, one new stance line, the gated set carrying the per-type guidance inline. **Shorter prompt, sharper REJECT bias, evidence-anchored.**

---

## Ranked recommendations by expected precision gain

| Rank | Change | Targets | Expected gain | Over-reject risk |
|------|--------|---------|---------------|------------------|
| 1 | **Evidence-grounding + planned-vs-completed** (A1, B2) | KILLS-foiled, COURTS-touch, PARENT_OF-denied, MOTIVATES, most over-inference | **High** — attacks the dominant root cause | Med-low (mitigated: semantic rule, lexical filter stays a soft flag) |
| 2 | **Default-to-REJECT asymmetry stance** (B1) | OPPOSES, COURTS, SEEKS, TEACHES, COMMANDS, all over-emission | **High** — single lever across many biases | Med (recall trade — but correct for this project; measurable) |
| 3 | **Consolidated co-presence principle** (B3) | TRAVELS_WITH, COMPANION_OF, CONTEMPORARY_WITH, SEEKS, RESPECTS | **Med-high** — generalizes; also shortens prompt | Low (carve-out for TRAVELS_WITH court-attendance) |
| 4 | **Inline `[GATED]` notes for OPPOSES/MOTIVATES/COMMANDS/COURTS/SEEKS/TEACHES/TUTORS/KILLS** (B4, A2–A5) | the named per-type biases | **Med** — places guidance at decision point; retires Rules 11/12/14 | Low–med per type |
| 5 | **MOTIVATES (+COMMANDS-A→C) → mechanical type-contract validator** (B4) | person-source MOTIVATES; two-hop COMMANDS | **Low-med** but **certain** (mechanical, not prompt-dependent) | None (deterministic) |

**Net expectation:** #1 + #2 together should move the needle most (they share the root cause and reinforce each other). #3 is the highest-value *structural* change because it makes the prompt shorter while fixing a generalizable bias. Combined, 60% → ~75–80% is plausible without adding net length — the gains come from a stronger REJECT default and evidence-anchoring, not from more enumerated cases.

---

## One skeptical note

The current prompt already tried the "add a rule per failure" strategy (Rules 6, 9, 11, 12, 14 are all that pattern) and plateaued at ~76% per the head-to-head. Adding a sixth and seventh anti-pattern block would likely yield diminishing returns and risk the model losing the thread in a wall of caveats. The leverage now is in the two *general* levers (REJECT-asymmetry, evidence-grounding) and in *consolidation* — moving from a long list of "don't do X" toward a short list of "only emit when the quote clearly states a directed source→target relationship; otherwise REJECT." That is the change most likely to clear 80%.
