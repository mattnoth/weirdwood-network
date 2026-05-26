# Fresh-Eyes Prompt Review — Stage 4 Tail Classifier (smoke4 Haiku, 60% strict precision)

**Reviewer:** Opus (read-only). **Date:** 2026-05-25.
**Target file:** `scripts/stage4-tail-classifier.py` (`render_classify_prompt`, `_PROMPT_PREAMBLE`, `build_vocab_block`, RULES 1-14).
**Audit corpus:** `working/wiki/pass2-buckets/pass1-derived/_smoke4-haiku/` — 103 emits / 96 rejects. Strict precision 60% (62 correct / 21 weak / 20 wrong).

I grounded every recommendation in the actual emitted rows, not just the task summary. Key counts from the emit set:
- Edge-type mix: REVEALS_TO 12, COMMANDS 10, OPPOSES 8, TRAVELS_WITH 7, DISTRUSTS 6, SEEKS 4, COURTS 2, MOTIVATES 2, TEACHES 2, KILLS 3.
- Confidence tiers on emits: tier-1 = 28, tier-2 = 71, tier-3 = 4. **The model almost never uses tier-3** even though most prose-derived inferences belong there. This is itself a signal (see §A).
- The reject rate is already ~48% (96/199 rows seen). Reject discipline is *firing*; the problem is the emits that survive are under-scrutinized, not that the model refuses to reject.

---

## A. Headline conclusion: the core fix is a REJECT-default reframe, not Rules 15-20

You asked directly: *is the core problem that the prompt should reject more aggressively on ambiguity rather than adding type-specific rules?* **Yes — that is the single highest-leverage change, and it should land before any new type-specific rule.**

Evidence from the audit:
- Every "wrong" class is a case where a *defensible-looking* type was reachable from a single sentence (Theon says "Kill him" → OPPOSES; Tyrion "sends Bronn… to protect" → PROTECTS; "plan to murder Mormont" → KILLS). The model is not hallucinating types out of nothing — it is **resolving genuine ambiguity in favor of emitting.** That is a *disposition* problem, not a *vocabulary* problem. Type-specific rules only patch the instances you already saw; the disposition leaks into the next 20 unseen patterns (whack-a-mole).
- The asymmetry the project already believes ("a missed edge is recoverable, a wrong edge pollutes") is **not currently stated in the prompt.** Rules 4 and 9's "when in doubt, REJECT" are buried mid-list and framed as exceptions. Haiku needs the cost asymmetry stated up front as the governing principle, with a concrete decision procedure.

The current 28/103 tier-1 rate is the smoking gun: Haiku is treating "I can see a quote" as "this is explicit canon," collapsing the evidence-strength axis. A reject-default reframe that *also* forces an honest tier choice will catch the unfulfilled-plot and single-moment cases for free.

### Recommendation A1 (RANK 1 — highest precision gain): add a governing REJECT-default principle as a preamble block, above the numbered rules.

Insert immediately after the "Classify each relationship row…" line, **before** "RULES:":

```
GOVERNING PRINCIPLE — WHEN IN DOUBT, REJECT.
A missing edge is recoverable (a later pass will catch it). A WRONG edge permanently
pollutes the graph. Therefore REJECT is the correct, safe answer whenever the evidence
does not CLEANLY and OBVIOUSLY support exactly one type. You are not scored on coverage.
You are scored on the fraction of your EMITS that are correct. Emitting a plausible-but-
shaky type is a LOSS, not a partial win.

Before emitting ANY type, pass all three gates. If any gate fails, REJECT:
  GATE 1 — STATE, not MOMENT: Does the evidence show a STANDING relationship between
    source and target, or just one momentary action/line of dialogue? A single command,
    refusal, question, rebuke, threat, or pass is usually a MOMENT. Most relationship
    edge types (OPPOSES, COURTS, SEEKS, TEACHES, RESPECTS, TRUSTS, DISTRUSTS) assert a
    STANDING disposition. If you only have one moment, REJECT unless the type explicitly
    covers single acts (KILLS, RESCUES, REVEALS_TO, ENCOUNTERS).
  GATE 2 — DIRECT pair: Is the relationship between THIS source and THIS target directly,
    or is one of them only connected through a THIRD party named in the quote? "A orders B
    to do X to C" is NOT an A→C edge. If the link is two-hop, REJECT.
  GATE 3 — FACT, not PLAN: Did the event actually HAPPEN as completed fact in the prose,
    or is it planned / attempted / foiled / hypothetical / urged-but-refused? Outcome edges
    (KILLS, EXECUTES, CAPTURES, DEFEATS, ASSAULTS) require the outcome to have OCCURRED.
    A foiled plot, a refused demand, or an intended action is NOT the completed edge. REJECT.
```

- **Fixes:** OPPOSES over-application (Gate 1), COMMANDS/PROTECTS two-hop collapse (Gate 2), unfulfilled KILLS (Gate 3), and most of the "weak" co-presence typings (Gate 1). This single block addresses 4 of the 5 named error classes.
- **Example rows it kills:** `theon→robb OPPOSES` (Gate 1+3 — urged-but-refused moment), `mance→jon OPPOSES` (Gate 1 — single interrogation), `thoros→harwin OPPOSES` (Gate 1 — one refused request), `sansa→joffrey OPPOSES` (Gate 1 — single defiant line), `osha→summer OPPOSES` (Gate 1 — Summer the direwolf refusing to descend stairs is not enmity), `tyrion→guildhall PROTECTS` (Gate 2 — Tyrion orders Bronn; the quote is even about ships, not the guildhall), `green-grace→graces COMMANDS` (Gate 1 — entourage standing behind her), `chett→mormont KILLS` (Gate 3 — the plot was foiled, Mormont not killed).
- **Predicted side-effects / over-rejection risk:** *Moderate and acceptable.* Gate 1 will suppress some valid STANDING-relationship edges that happen to be evidenced by a single line (e.g., a long-running feud quoted via one barb). This is the right trade given the 60% precision floor — those edges are recoverable from other chapters' rows, and the project's own asymmetry rule blesses it. The bigger risk is Gate 1 leaking into genuinely-single-act types; I explicitly whitelist KILLS/RESCUES/REVEALS_TO/ENCOUNTERS to prevent that. Monitor REVEALS_TO recall after this lands — it is the highest-volume type (12 emits) and is single-act by nature; the whitelist protects it, but re-audit.

---

## B. Consolidation beats piling on (your second design question)

You asked whether a single "co-presence is not a relationship" principle would help more than Rules 15-20. **Yes.** The audit shows TRAVELS_WITH (7), SEEKS (4), TEACHES (2), COURTS (2) are all the *same underlying error*: the model sees two named entities in one scene and reaches for the nearest type that "fits the room." This is exactly the failure that Rules 9, 11, and 12 already try to patch piecemeal for INFORMS/ADVISES/CONTEMPORARY_WITH/COMPANION_OF/RESPECTS. You have five rules circling one principle. Consolidate.

### Recommendation B1 (RANK 2): add ONE co-presence principle and point the scattered rules at it.

Add as a new rule (number it Rule 15, but it is a *consolidation*, not an addition — it lets you shorten 11 and 12 later):

```
15. CO-PRESENCE IS NOT A RELATIONSHIP — the master gate behind Rules 11, 12.
    Two entities sharing a scene, room, march, meal, battle, council, or chapter is NEVER
    sufficient evidence for ANY edge. Co-presence is the single most common false-positive
    source. A type requires evidence of the SPECIFIC relationship it names, between THIS
    source and THIS target:
      - TRAVELS_WITH: requires actual JOINT MOVEMENT between places ("rode out together",
        "on the voyage", "they journeyed to X"). Standing in the same room, sept, or hall,
        or arriving at the same court, is NOT travel. If they are merely co-located, REJECT.
      - SEEKS: requires PURSUIT of a person/artifact/knowledge over time ("searched for",
        "hunted", "would not rest until"). A single question, a single errand, or carrying
        a message is NOT SEEKS. REJECT.
      - TEACHES / TUTORS: require KNOWLEDGE OR SKILL TRANSFER framed as instruction. Telling
        a story, sharing an opinion, explaining a situation, or conversing is NOT teaching.
        REJECT unless the prose frames one party as instructing the other.
      - COURTS: requires explicit SUITOR/MARRIAGE-PURSUIT language ("sought her hand", "his
        suitor", "courted her"). A crude pass, a flirtation, a seduction-for-leverage, or
        an introduction is NOT COURTS. REJECT or use the actually-evidenced type.
    When co-presence is all you have, REJECT. Do not "pick the closest type."
```

- **Fixes:** the entire "loose co-presence typing (many weak)" class plus 2 wrong COURTS.
- **Example rows it kills/corrects:** `arstan→belwas TRAVELS_WITH` (introduce themselves while kneeling — not joint movement → REJECT), `bowen-marsh→cellador TRAVELS_WITH` (both visit a room → REJECT), `pypar→halder TRAVELS_WITH` (recruits in a sept → REJECT), `bran→gage SEEKS` (one question about the comet → REJECT), `cersei→dorne SEEKS` (a decision to send for a master-at-arms → REJECT or different type), `old-nan→bran TEACHES` (storytelling → REJECT), `qhorin→jon TEACHES` (a conversation about Mance → REJECT), `cersei→hand-of-the-king COURTS` (seduction-for-alliance, and target is a TITLE not a person → REJECT; also flagged by Gate 2 since the real target is Ned), `bella→gendry COURTS` (a come-on → REJECT).
- **Predicted side-effects / over-rejection risk:** *Low-to-moderate.* TRAVELS_WITH recall will drop — this is intended; the type was being used as a co-presence dumping ground (the architecture even invites that with its "retinue/court presence" clause, which is part of the problem — see §D). The genuine road-companion edges ("on the voyage", Dunk+Egg) still pass. SEEKS/TEACHES were already low-volume; the loss is small. Net precision gain is high because these were almost all weak/wrong.

### Note on rule-count economy
After B1 lands you can **shorten** Rules 11 (CONTEMPORARY_WITH/COMPANION_OF clauses) and 12 (RESPECTS) by deleting their now-redundant "co-presence is not enough" prose and replacing it with "see Rule 15." That keeps the prompt from ballooning. I would NOT delete the RESPECTS explicit-language whitelist (it works — 0 RESPECTS emits) but its *co-presence* bullet is now covered by Rule 15.

---

## C. The two clean architecture-violation classes — make them mechanical, not judgmental

MOTIVATES (person→person) and the COMMANDS two-hop are **type-contract violations**, not judgment calls. Haiku is good at hard contracts ("X must be an event," "both must be characters" — Rules 6 and 14 work). Give it the same crisp contract here rather than asking it to reason.

### Recommendation C1 (RANK 3): MOTIVATES source-type contract.

Per architecture: `MOTIVATES` is `Motivation → Actor` — the SOURCE is an event or condition, NOT a person. Add to the GATED list (see §D) and add a one-line contract:

```
16. MOTIVATES type-contract — the SOURCE must be an EVENT or CONDITION, never a person.
    MOTIVATES connects a motivating event/condition → the actor it drives ("the Red Wedding
    MOTIVATES Arya"). If the source of this row is a PERSON, MOTIVATES is IMPOSSIBLE — REJECT
    or pick the actual interpersonal type. "A persuades/rallies/inspires B" is not MOTIVATES;
    it is at most REVEALS_TO or, if B is unaware of being used, MANIPULATES — but usually REJECT.
```

- **Fixes:** MOTIVATES misuse (2 wrong).
- **Example rows it kills:** `jon-snow→toregg MOTIVATES` (person source → REJECT — Jon calling for volunteers and Toregg volunteering is not a graph edge), `aegon→flowers-of-spring MOTIVATES` (person source → REJECT).
- **Predicted side-effects:** *Negligible.* These tail rows are person-pair candidates by construction (fixed source/target slugs that are mostly characters), so valid event→actor MOTIVATES edges are rare-to-absent in this population. The contract simply closes a door that should never have been open here. If anything, consider whether MOTIVATES should be *removed from the candidate population upstream* for person-pair rows — but that is a pipeline change, out of scope for the prompt.

### Recommendation C2 (RANK 4): COMMANDS two-hop guard (largely subsumed by Gate 2, but worth a named bullet because COMMANDS is high-volume — 10 emits).

```
17. COMMANDS / PROTECTS / GUARDS two-hop guard. "A orders/sends B to do X to (or at, or for) C"
    creates AT MOST an A→B COMMANDS edge — never an A→C edge. The thing B is ordered to do is
    a SEPARATE edge from B, not from A. If this row's source is the ORDER-GIVER and the target
    is the OBJECT of the ordered action (not the person receiving the order), REJECT.
    Example error to avoid: "Tyrion sends Bronn to protect the guildhall" is NOT tyrion→guildhall
    PROTECTS. It is at most tyrion→bronn COMMANDS (if both are this row's pair) or bronn→guildhall
    PROTECTS — neither of which is tyrion→guildhall.
```

- **Fixes:** COMMANDS two-hop collapse (named example `tyrion→guildhall PROTECTS`); reinforces Gate 2 for the highest-volume command-ish types.
- **Example rows:** `tyrion→guildhall-of-the-alchemists PROTECTS` (REJECT). Also pressure-tests `green-grace→graces COMMANDS` (no order is given — entourage merely arrays itself behind her → REJECT via Gate 1).
- **Predicted side-effects:** *Low.* Genuine A→B COMMANDS (Mormont→Jon, Qhorin→Jon, Tywin→Gregor) are untouched — those rows' target IS the person receiving the order. Risk is the model over-reading "for C" constructions; the explicit example anchors it.

---

## D. Should TRAVELS_WITH / MOTIVATES / COURTS be GATED like RESPECTS? (your third design question)

**Partially yes — gate MOTIVATES and COURTS; do NOT gate TRAVELS_WITH the same way.** Reasoning, type by type:

- **MOTIVATES — YES, gate it.** It has a hard, mechanical misuse (person-as-source) and near-zero legitimate use in the person-pair tail population. Adding it to `DEFAULT_GATED_TYPES` with the Rule 16 contract is cheap and safe. The `[GATED]` marker in `build_vocab_block` will make Haiku pause on it. **Concrete change:** add `"MOTIVATES"` to `DEFAULT_GATED_TYPES` (line 312-318) and route it to Rule 16.

- **COURTS — YES, gate it.** Audit shows 2/2 COURTS emits were wrong (seduction-for-leverage; a come-on). It has a crisp positive test (suitor/sought-her-hand language) just like RESPECTS, and an obvious over-reach (any flirtation). It is a good fit for the gated/explicit-language pattern that already works for RESPECTS. **Concrete change:** add `"COURTS"` to `DEFAULT_GATED_TYPES`; its anti-pattern is the COURTS bullet already in Rule 15.

- **TRAVELS_WITH — NO, do not gate it as an anti-pattern type; instead fix its CONTRACT (Rule 15) and consider an upstream/architecture tightening.** The real problem is that the *architecture definition itself* is too loose: it explicitly says TRAVELS_WITH "covers… retinue/court presence (Robett kneeling among Catelyn's welcomers)." That clause is what licenses the co-presence dumping (7 emits, several weak). Gating it won't help because the definition the model is being faithful to is the thing that is wrong. **Recommendation:** narrow the TRAVELS_WITH *definition* in `architecture.md` to require joint MOVEMENT, and split the "retinue/court presence" sense into ATTENDS or drop it — but that is an architecture edit requiring your sign-off (rule 6: prompt and architecture must stay in sync), so I flag it rather than propose silently. In the interim, Rule 15's TRAVELS_WITH bullet ("standing in the same room is NOT travel") is the surgical patch.

Gating discipline note: the gated mechanism is a *blocklist annotation* (type stays in vocab, gets `[GATED — see Rule 9]`). Adding MOTIVATES/COURTS costs ~2 vocab lines and one Rule-16/Rule-15 cross-reference. That is well within budget and keeps these two from being silent emits.

---

## E. Secondary findings (lower rank, flag-and-defer)

### E1. Confidence-tier discipline is broken and it matters for the KILLS-on-foiled-plot class.
28/103 emits are tier-1, but Rule 10 reserves tier-1 for "explicit prose statements." `theon→robb OPPOSES` was emitted at **tier-1** (an urged-and-refused moment is not explicit-canon enmity), and `chett→mormont KILLS` at tier-2 (a foiled plot). The model is not using tier as a confidence brake. Gate 3 (§A1) is the primary fix for the foiled-plot case. Additionally, tighten Rule 10 with one line:

```
   - If the relationship is a single momentary action, an inference, or anything you hesitated
     over, it is NOT Tier-1. Tier-1 is reserved for relationships the prose STATES outright as
     standing fact. Default prose-derived inferences to Tier-3.
```
- **Side-effect:** none harmful; pushes the tier distribution toward tier-3 (currently near-empty), which is more honest and lets downstream consumers filter on confidence. Note the terminology collision worth knowing: the prompt's `confidence_tier` (1/2/3 evidence strength, Rule 10) is a DIFFERENT axis from the qualifier-vocab's "Tier 1/2/3" (whether a qualifier is required). The code's `tier1_types` set is the qualifier axis; Rule 10's tier is the confidence axis. They are not wired together, which is correct — but the shared word "tier" is a latent trap for any future editor. Consider renaming Rule 10's field to `evidence_tier` in a later pass.

### E2. OPPOSES needs a positive contract, since it is symmetric and high-volume (8 emits).
Even with Gate 1, OPPOSES is the single worst offender. Add one targeted bullet (can live inside Rule 15's spirit or as its own line):
```
   - OPPOSES asserts STANDING enmity or active opposition between two parties (a feud, a war,
     rival claimants). A single disagreement, refusal, rebuke, or argument between ALLIES is NOT
     OPPOSES. If source and target are on the same side and merely disagree in one moment, REJECT.
```
- **Fixes:** `theon→robb`, `mance→jon`, `thoros→harwin`, and the borderline ally-friction emits.
- **Side-effect:** could suppress early-stage enmity shown via one scene. Acceptable per the asymmetry; OPPOSES between true rivals is usually evidenced repeatedly across chapters.

### E3. Empty-evidence emits.
One emit (`jon-connington→tyrion COMMANDS`) has an **empty `evidence_quote`** and was still emitted at tier-2 off the `hint_raw` alone. Add a hard line to Rule 4:
```
   - If evidence_quote is empty/blank, you may rely ONLY on the hint, and you must NOT emit
     Tier-1. If the hint alone does not cleanly support one type, REJECT.
```
- **Side-effect:** none; this is pure tightening on a known-thin signal.

---

## F. Ranked implementation order (highest precision-gain first)

| Rank | Change | Error classes fixed | Over-rejection risk |
|------|--------|---------------------|---------------------|
| 1 | **A1** — Governing REJECT-default + 3 gates (STATE/DIRECT/FACT) preamble | OPPOSES over-app, COMMANDS/PROTECTS two-hop, foiled-KILLS, much co-presence | Moderate (intended) |
| 2 | **B1** — Rule 15 "co-presence is not a relationship" (consolidates 11/12) | TRAVELS_WITH/SEEKS/TEACHES/COURTS weak typings | Low-moderate |
| 3 | **C1** — Rule 16 MOTIVATES source-type contract + gate it | MOTIVATES person→person (2 wrong) | Negligible |
| 4 | **C2** — Rule 17 COMMANDS/PROTECTS two-hop guard | COMMANDS two-hop (high-volume reinforcement) | Low |
| 5 | **D** — Add MOTIVATES + COURTS to `DEFAULT_GATED_TYPES` | MOTIVATES, COURTS | Negligible |
| 6 | **E2** — OPPOSES positive standing-enmity contract | OPPOSES residual | Low |
| 7 | **E1** — Tier-1 discipline line in Rule 10; default-to-tier-3 | foiled/single-moment over-confidence | None |
| 8 | **E3** — Empty-quote → no Tier-1, reject-if-thin | thin-signal emits | None |

**Do NOT** add separate per-type rules for every weak type. Ranks 1-2 are the leverage; everything below is cleanup. If you ship only A1 + B1 + C1, I expect the bulk of the wrong/weak set to clear and precision to move into the mid-70s, because those three cover 4 of the 5 named wrong-classes and the entire weak co-presence bucket. C2/D/E are insurance against regression and high-volume residuals.

## G. One thing to verify after the next smoke run (don't over-correct)
The reject rate is already ~48%. A1's gates will push it higher. **Watch the reject pile for false rejects** — specifically genuine single-act edges (KILLS, RESCUES, REVEALS_TO, ENCOUNTERS) caught by an over-eager Gate 1, and real road-companions caught by Rule 15's TRAVELS_WITH bullet. The whitelist in Gate 1 is designed to prevent the former; spot-check ~20 rejects to confirm it holds. If recall on REVEALS_TO (the highest-volume type) drops materially, the Gate 1 whitelist needs to be made louder, not the gate removed.

## H. Architecture-sync flag (CLAUDE.md rule 6)
Two proposals touch type *definitions*, not just the prompt:
- **TRAVELS_WITH** (§D): the loose "retinue/court presence" clause in `architecture.md` line ~284 is the root cause of the co-presence dumping. Recommend narrowing it to joint-movement and moving court-presence to ATTENDS. **This is an architecture edit and needs Matt's sign-off** — flagged, not proposed for silent change.
- **MOTIVATES gating** (§C1/§D): adding it to the gated list is a prompt-only change, but if you decide person-pair MOTIVATES candidates should never reach the classifier, that's an upstream candidate-generation filter (`stage4-pass1-edge-candidates.py`), not a prompt rule.
