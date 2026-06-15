# Continue Prompt — Dialogue + Meals + Mention-Index Pass Design

**Date drafted:** 2026-05-05 (Session 34 follow-up)
**Status:** DESIGN — awaiting Matt's review + approval before any extraction launches
**Model assumption for design discussion:** Sonnet (this is design, not deep reasoning)
**Read-before-acting:** This entire document is self-contained. You do NOT need to read the worklog or architecture.md unless something below points you there. References to specific files/lines below are accurate as of 2026-05-05.

---

## Why this prompt exists

Matt's vision: **a queryable ASOIAF graph that anyone can ask "tell me about X" and get prose, quotes, food, scene context, and entity links — without the build taking forever or costing a fortune.**

By 2026-05-05 we have ~262/344 chapter mechanical extractions (Pass 1 v3 — AGOT, ACOK, AFFC, ADWD; ASOS pending Okey's Opus run on shared Max) and 7,563 wiki graph nodes. Track B / wiki Pass 2 is largely done. The question Session 34 surfaced: **what's the cheapest set of passes that turn the existing data into the queryable, chatbot-ready graph Matt described?**

Answer that came out of the discussion: don't re-read chapters with Opus again. Use Python where possible, Sonnet/Haiku for narrow reasoning, Opus only as a sampling oracle for validation. Three new passes scoped:

1. **Dialogue extraction** (Pass 1.5) — speaker / audience / quote / chapter pointer per line of dialogue
2. **Meals & feasts extraction** (Pass 1.6, Matt's idea) — discrete meal events with attendees, foods, hospitality status
3. **Per-chapter mention index** (Pass 1.7, pure Python) — chapter ↔ node back-references closing the "from a fact, can I find the scene?" gap

Plus a fourth thing already designed in architecture.md but not yet built:

4. **Per-character index** (`graph/index/characters/<slug>.index.json`) — roll-up view that ties everything together per entity, populated from the three passes above

Plus eventually:

5. **Voice profile** (Pass 3 — `extractions/voice/<character>.voice.md`) — narrative voice analysis, downstream of the dialogue pass

---

## Current state (verified 2026-05-05)

- **Pass 1 v3 extractions on disk:** AGOT 73/73, ACOK 70/70, AFFC 46/46, ADWD 73/73. ASOS 0/82 — Okey running Opus on shared Max, will push when complete.
- **Wiki graph:** 7,563 nodes across `graph/nodes/<type>/`, 22-edge-type vocabulary locked, schema-drift audit clean (0 HIGH).
- **Stage 4 prose-edge-classifier** queued in `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md` — gated on 5/5 Pass 1 books.
- **Cleanup committed `ba338ad1`** (Session 34): ADWD landed, chain/race bug fix archive, todos.md URGENT block removed.
- **Standing rules** (memorized, do not violate):
  - Python before agent — wherever a deterministic step works, use it
  - Default to cheapest viable model; Opus only when reasoning depth justifies
  - Never auto-run extractions; always confirm with Matt first
  - Never delete extractions / archives — old versions go to `extractions/archives/<book>-vN-<date>/`
  - Never auto-run `/endsession`

---

## The three new passes — design

### 1. Dialogue pass (Pass 1.5)

**What it produces.** One JSONL row per quote, source-of-truth at:

```
extractions/dialogue/<book>/<book>-<chapter>.dialogue.jsonl
```

Row shape (proposed — open to redirect):

```json
{
  "speaker": "eddard-stark",          // resolved to wiki slug
  "speaker_aliases_used": ["Lord Stark", "Father"],
  "audience": ["catelyn-stark", "robb-stark"],   // canonical slugs; [] if soliloquy
  "quote": "Winter is coming.",
  "chapter_id": "agot-bran-01",
  "paragraph_offset": 47,             // line/paragraph in source chapter
  "scene_phase": "Opening",           // from Pass 1 Spatial Layout (when present)
  "speaker_confidence": "high",       // high / medium / low (Python pre-pass scores)
  "attribution_method": "explicit-tag" // explicit-tag / nearest-speaker / agent-resolved
}
```

**How it gets built.**

- **Step A — Python pre-pass.** Walks each chapter source file, finds quoted strings, extracts speaker via dialogue-tag patterns (`said X`, `X said`, `asked X`, etc.). Cross-references with Pass 1's "Characters Present" list to filter false matches. Resolves names to slugs via wiki-node alias lookup. Estimated coverage: 70-85% of quotes with high-confidence attribution.
- **Step B — Sonnet 4.6 residue.** Only rows where Step A's confidence is medium/low (free indirect, "she said" with two women in scene, multi-party dialogue) get sent to Sonnet with the surrounding paragraph + Pass 1's Characters Present + Spatial Layout phase. Estimated 15-30% of rows.
- **Step C — Validate against Pass 1's "Dialogue of Note".** Pass 1 already extracts ~5-10 key quotes per chapter. Every Pass 1 key quote should appear in the dialogue table. If not, surface for review — likely a Step A miss.

**Cost projection — AGOT only (73 chapters, ~50-100 quotes/ch).**

- Step A: $0 (Python)
- Step B Sonnet: ~$15-25 total
- Step C: $0 (Python diff)
- Wall-clock: 30-60 min parallelized

vs. a fresh Opus pass over the same 73 chapters: ~$300+, 8+ hours.

---

### 2. Meals & feasts pass (Pass 1.6 — Matt's idea, 2026-05-05)

**Why this is its own pass.** Matt's design value: food/hospitality is first-class. The wiki already has `object.food` as a type with 69 nodes in `graph/nodes/foods/`. Pass 1 already extracts a "Food & Drink" section per chapter. What's missing is the **meal-event layer** — a discrete entity per feast/meal that links food + attendees + location + hospitality.

Use cases Matt called out:
- "Tell me about five feasts and what they ate" → returns 5 meal-event nodes with rich food descriptions
- "What was served when Tyrion ate with Cersei?" → query meal nodes by attendee
- The meal node naturally edges to characters (`ATTENDED_BY`), locations (`HELD_AT`), houses (`HOSTED_BY`), and food objects (`INCLUDED_FOOD`)

**What it produces.** One row per meal event in source-of-truth:

```
extractions/meals/<book>/<book>-<chapter>.meals.jsonl
```

Plus promoted meal-event nodes at:

```
graph/nodes/events/<meal-slug>.node.md      # type: event.meal (NEW SUBTYPE — needs schema add)
```

Or possibly `graph/nodes/scenes/` if we add a `scene` type — open question (see below).

Row shape:

```json
{
  "meal_slug": "agot-bran-01-winterfell-feast-king-robert",
  "scene_kind": "feast",     // feast / supper / breakfast / road-meal / ritual-meal / etc.
  "chapter_id": "agot-eddard-03",
  "location": "winterfell-great-hall",
  "attendees": ["eddard-stark", "robert-baratheon", "cersei-lannister", ...],
  "host": "eddard-stark",
  "foods": ["roast-aurochs", "honey-cake", "summerwine"],
  "hospitality_status": "guest-right-invoked",   // from Pass 1 Hospitality section
  "summary": "Welcome feast for King Robert at Winterfell. Robert toasts...",
  "key_moments": ["Cersei refuses to attend", "Jon eats with the guards"],
  "extraction_confidence": "high"
}
```

**How it gets built.**

- **Step A — Python prep.** For each chapter, read its Pass 1 extraction. Extract the Food & Drink section + Hospitality section + Spatial Layout. If Food & Drink is non-empty AND attendees ≥ 2 (or Hospitality is invoked), this is a candidate meal scene.
- **Step B — Haiku 4.5 normalization.** Send Pass 1's Food & Drink + Hospitality + Spatial Layout + Characters Present + ~3-paragraph chapter excerpt (from a script that finds the meal scene in source) to Haiku. Haiku produces the JSONL row above. **Haiku, not Sonnet** — this is genuinely a normalization task; the reasoning is already in Pass 1's output. Smoke-test before committing.
- **Step C — Promote to graph.** Python script writes meal-event node with edges. Same emit pattern as wiki Pass 2 stages 3a/b. Schema-add for `event.meal` subtype required (see Open Questions).

**Cost projection — full corpus (262 chapters today + 82 ASOS later).**

Estimating ~30-50% of chapters have a notable meal scene (some have multiple): ~100-200 meal events total.
- Step A: $0
- Step B Haiku: ~$0.05-0.15 per meal × 200 ≈ **$10-30 total**
- Step C: $0

This is the **cheapest pass yet** because Pass 1 did all the heavy reasoning.

---

### 3. Per-chapter mention index (Pass 1.7 — pure Python)

**Closes the gap Matt's scratch identified:** "from a node fact you can't get back to the scene/quote/food."

**What it produces.**

```
graph/index/chapters/<book>/<book>-<chapter>.mentions.json
```

```json
{
  "chapter_id": "agot-bran-01",
  "mentions": [
    {"slug": "eddard-stark", "type": "character.human", "section": "Characters Present", "line": 12},
    {"slug": "winterfell", "type": "place.location", "section": "Locations", "line": 34},
    {"slug": "ice", "type": "object.artifact", "section": "Artifacts & Objects", "line": 56},
    {"slug": "house-stark", "type": "organization.house", "section": "Raw Entity List", "line": 89},
    ...
  ]
}
```

**How it gets built.** Pure Python script reads each Pass 1 extraction, walks the structured sections (Characters Present, Locations, Artifacts, Houses, Raw Entity List, etc.), resolves named entities to slugs via the wiki-node alias resolver (`scripts/wiki-pass2-build-alias-resolver.py` already exists), emits the JSON. Re-runnable in seconds — no agent, no archival concern.

**Cost: $0. Runtime: minutes.**

This is the connective tissue. Once it exists, "find Tyrion's scenes that include lemon cakes" is a join across `chapters/*.mentions.json` and `extractions/meals/*.meals.jsonl`.

---

## Per-character index (the roll-up view)

Once passes 1.5 / 1.6 / 1.7 land, build:

```
graph/index/characters/<slug>.index.json
```

```json
{
  "slug": "eddard-stark",
  "node_path": "graph/nodes/characters/eddard-stark.node.md",
  "chapters_pov": ["agot-eddard-01", ..., "agot-eddard-15"],
  "chapters_appears": ["agot-bran-01", "agot-catelyn-01", ...],
  "chapters_mentioned": [...],
  "dialogue_count": 412,
  "dialogue_path": "graph/index/dialogue/eddard-stark.dialogue.jsonl",  // derived view
  "voice_profile": "extractions/voice/eddard-stark.voice.md",
  "edges_out": 47,
  "edges_in": 312,
  "meals_attended": ["agot-bran-01-winterfell-feast", ...]
}
```

Pure Python — derived view, rebuilt from sources anytime. This is the chatbot's **retrieval seed**: "talk to Ned" → load this file → fan out to dialogue, voice, POV-internal, and node prose.

---

## Validation — Opus as sampling oracle, NOT replicator

Matt's instinct (2026-05-05): "Opus validation but with discrete reasoning." Yes, totally tractable. The pattern is **sample + characterize**, never replicate.

Five validation patterns scoped:

| Pattern | What Opus reads | Output | Cost (AGOT) |
|---------|----------------|--------|-------------|
| 1. Sample audit | 8 chapter prose files + their dialogue rows | Per-error-class rate (mis-attribution / missed quote / wrong audience) | ~$25 |
| 2. Hard-cases triage | Only rows Sonnet flagged low-confidence | Adjudicated speaker/audience | ~$10-30 |
| 3. Cross-reference check | Pass 1 "Dialogue of Note" vs. dialogue table | Missing-quote list | $0 (pure Python) |
| 4. Voice-coherence per character | Full dialogue corpus per character (no chapters) | "These N lines feel out of voice" | ~$30 (12 characters) |
| 5. Disagreement adjudication | Rows where Python and Sonnet disagree | Tiebreaker call | ~$5-15 |

**Total Opus QA budget for AGOT dialogue: $70-100** (vs. ~$300+ for a full Opus dialogue pass).

**Pattern 4 is the most distinctive for Matt's chatbot use case** — voice coherence IS the deliverable. Same Opus call produces (a) QA signal (likely mis-attributions) AND (b) raw material for the persona prompt ("Ned uses formal address, never sarcasm — these 4 outliers don't fit").

**Recommended ordering:**
- **Pattern 1 first as the gate** — characterize the error distribution before scaling up
- **Pattern 4 second** as both QA AND chatbot persona-prep
- Patterns 2/3/5 only fire if Pattern 1 surfaces something

---

## File organization (proposed — open to redirect)

```
extractions/                              # source of truth — one writer per artifact
├── mechanical/<book>/                    # exists — Pass 1 (Opus)
├── dialogue/<book>/                      # NEW — Pass 1.5 (Python + Sonnet)
│   └── agot-eddard-01.dialogue.jsonl
├── meals/<book>/                         # NEW — Pass 1.6 (Python + Haiku)
│   └── agot-bran-01.meals.jsonl
├── voice/<character>/                    # NEW — Pass 3 (later, Sonnet)
│   └── eddard-stark.voice.md
└── archives/                             # exists — append-only, NEVER deleted
    ├── agot-v1/, agot-v2/, acok-v2/      # existing
    ├── dialogue-v1-<date>/               # future re-runs
    └── meals-v1-<date>/

graph/
├── nodes/<type>/<slug>.node.md           # exists — 7,563 nodes
│   └── events/<meal-slug>.node.md        # NEW subtype: event.meal (schema-add required)
├── edges/                                # exists, currently empty
└── index/                                # mostly NEW — DERIVED, rebuild anytime
    ├── chapters/<book>/<ch>.mentions.json    # Pass 1.7 — pure Python
    ├── characters/<slug>.index.json          # roll-up view
    ├── dialogue/<slug>.dialogue.jsonl        # per-character corpus (derived)
    └── meals/<slug>.attended.jsonl           # per-character meal list (derived)

working/dialogue-smoke-2026-MM-DD/        # NEW — smoke-test outputs land here FIRST
                                          # promote to extractions/dialogue/ only after approval
```

**Source-of-truth invariant:** `extractions/` has exactly one writer per file (Python script OR agent, never both). Re-running the pass overwrites in place ONLY after archiving the prior version to `extractions/archives/`. `graph/index/` is purely derived; overwrite freely.

---

## Smoke-test plan

**Recommended candidates (Matt's calls 2026-05-05):**

| Character | Why a strong test | What it stresses |
|-----------|-------------------|------------------|
| **Ned Stark** | Finite corpus (15 POV chapters in AGOT, posthumous flashbacks in ASOS/ADWD via Bran's vision). Iconic voice. Dies end of AGOT. | Clean POV chapters + cross-POV references after death. The "easy" case where dialogue tags are explicit and the narrator is the speaker. |
| **Robert Baratheon** | **No POV chapters at all.** Dies AGOT Eddard XIII; heavily referenced afterward. Bobby B's voice is extremely distinctive (loud, profane, nostalgic). | **Two distinct stress tests rolled into one character:** (1) **Quote attribution for non-POV speakers** — every line Robert speaks is filtered through someone else's POV. The Python pre-pass needs to handle "Robert laughed and said X" inside Eddard's narration just as well as direct dialogue tags. (2) **Cross-POV perception capture** — what Ned thinks of Robert (gone to seed, beloved old friend), what Cersei thinks of Robert (drunken pig), what Jaime thinks (resented him), what Renly thinks (mocked him). This is the perception-edge layer Pass 3 / Stage 4 was designed for, but the dialogue pass surfaces it as a side effect via the POV chapter's narration around the quote. **For a "talk to Robert" or "what did people think of Robert" chatbot query, this is the only retrieval pattern that works.** |

**Smoke-test scope (1 evening of work, no Opus needed for the smoke itself):**

- Pick 3 chapters where Ned + Robert both appear: `agot-eddard-02` (King's road, Robert and Ned), `agot-eddard-03` (Winterfell feast — meal scene), `agot-eddard-08` (King's Hand, court politics). Or pick 3 differently — just span quiet/political/action.
- Run Step A (Python pre-pass) — measure coverage % and false-positive rate manually
- Run Step B (Sonnet residue) on flagged rows — measure cost and read 100% of output
- Run Step C (Pass 1 cross-check) — measure missing-quote rate
- ALSO smoke the meals pass on `agot-eddard-03` (the Winterfell feast — multi-attendee meal with hospitality invoked)
- ALSO smoke the mention index on the same 3 chapters

**Acceptance criteria for smoking → scaling:**
- Step A coverage ≥ 70%
- Step B Sonnet rows readable + correct on 100% spot-check
- Step C cross-check finds < 5% genuine misses
- Smoke output written to `working/dialogue-smoke-2026-MM-DD/` — NOT promoted to `extractions/`

If smoke passes, scale to AGOT-wide (73 chapters), then run Opus validation Pattern 1, then decide whether to scale further.

---

## Open questions for Matt to resolve next session

1. **Should `extractions/voice/<character>.voice.md` co-locate with `graph/index/voice/`?** I lean separate (voice is narrative analysis, index is structured retrieval data). Open to one canonical "everything about Ned" co-located dir if Matt prefers.
2. **Naming: `dialogue` vs. `quotes` vs. `speech`?** I used `dialogue` because Pass 1 already calls it "Dialogue of Note." If user-facing layer should say "quotes," rename now (cheap pre-launch, expensive post).
3. **Schema-add: `event.meal` subtype** under `event` parent. Or should it be a new top-level `scene` type? Or reuse `event.battle`-shape pattern? Decide before promoting meal-event nodes.
4. **Validation pattern lead.** Three options:
   - "Sonnet missed quotes" worry → Pattern 3 leads (Pass 1 cross-ref)
   - "Sonnet got speakers wrong" worry → Pattern 4 leads (voice coherence)
   - "Don't know what we don't know" → Pattern 1 leads (sample audit)
   - My lean: **Pattern 1 first as gate, Pattern 4 second as chatbot prep, others reactive**
5. **Bobby B vs. Ned for the FIRST smoke test — RESOLVED 2026-05-05.** Ned first (POV-rich, easier to validate), then Robert as the **second smoke** specifically testing two things Ned doesn't stress: (a) quote attribution for non-POV speakers (every Robert line is filtered through someone else's narration), (b) cross-POV perception capture (what Ned/Cersei/Jaime/Renly think *about* Robert as the quote happens). The Python pre-pass and the Sonnet residue prompt likely need NON-POV-specific handling — flag this for the smoke. The dialogue rows for non-POV characters may also need a `narrator_pov` field so retrieval can surface "Robert said X *as Eddard heard it*" — this is critical for the chatbot voice (Robert-via-Eddard sounds different from Robert-via-Cersei).
6. **Meals pass — Haiku 4.5 vs. Sonnet 4.6?** I proposed Haiku. Smoke 5 meals on Haiku, eyeball quality. If sloppy on multi-course feasts (Winterfell, Riverrun wedding, Purple Wedding), upgrade to Sonnet for the corpus run.
7. **Order of operations.** Three viable orderings:
   - **A:** Mention index first (pure Python, free, unblocks per-character index) → dialogue smoke → meals smoke → validation
   - **B:** Dialogue smoke first (the most user-visible deliverable for "talk to Ned") → meals smoke → mention index → validation
   - **C:** All three smokes in parallel → validation across all
   - My lean: **A** — mention index is free and unblocks the per-character index assembly, which is what makes the smoke-test outputs queryable.

---

## What the next session should NOT do

- Do NOT auto-launch any agent extraction. Confirm with Matt first.
- Do NOT use Opus for Steps A/B of the dialogue or meals passes. Sonnet/Haiku only. Opus reserved for validation patterns 1, 2, 4, 5.
- Do NOT modify wiki nodes (`graph/nodes/`). Dialogue / meals / mention-index live in `graph/index/` or `extractions/`. The wiki node prose stays clean per the deterministic-emission contract from Stage 3.
- Do NOT delete any `extractions/archives/` content. Archive new versions, never overwrite history.
- Do NOT promote smoke-test outputs to canonical paths until Matt approves. Use `working/dialogue-smoke-<date>/` as the holding pen.
- Do NOT run `/endsession` without explicit permission.

---

## What the next session SHOULD do (recommended order)

1. **Read this file end to end.** Confirm understanding with Matt, especially Open Questions 1-7.
2. **Resolve Open Questions** — Matt picks the leads, the names, the order.
3. **If approved, build the mention index FIRST** — pure Python, no agent. Validates the alias resolver's coverage on the Pass 1 corpus. Output: `graph/index/chapters/<book>/<ch>.mentions.json` for all 262 chapters. Estimated: 20-40 minutes scripting + minutes to run.
4. **Then draft the dialogue-pass Python pre-pass script.** Test on `agot-eddard-02`, `agot-eddard-03`, `agot-eddard-08`. Measure Step A coverage. Confirm scope before any agent calls.
5. **Then draft the dialogue-pass Sonnet prompt.** Smoke on the residue from step 4. Output to `working/dialogue-smoke-<date>/`.
6. **Then draft the meals pass Haiku prompt.** Smoke on `agot-eddard-03` (Winterfell feast). Same `working/dialogue-smoke-<date>/` dir.
7. **Then draft validation Pattern 1 prompt** for Opus sample-audit. Run on the smoke output (3 chapters). Decide go/no-go for AGOT scaling.
8. **Update worklog at the end of the session** (only if Matt explicitly authorizes).

---

## Cross-references

- **Cleanup commit that landed Session 34:** `ba338ad1` (ADWD + bug fix archive)
- **Architecture spec for entity types & edge vocabulary:** `reference/architecture.md` (especially § Edge Types — vocabulary lock — and § Artifact Formats by Consumer)
- **Stage 4 (queued for after 5/5 Pass 1):** `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`
- **Pass 1 v3 prompt:** `.claude/agents/mechanical-extractor.md`
- **Wiki alias resolver script:** `scripts/wiki-pass2-build-alias-resolver.py`
- **Cross-references index (already built):** `working/wiki/data/cross-references.jsonl`
- **Standing rules (memory):** `~/.claude/projects/-Users-mnoth-source-asoiaf-chat/memory/MEMORY.md`

---

## TL;DR for tired-Matt-coming-back

You wanted: queryable ASOIAF, accessible, not slow.
We don't need a new full Opus pass. Three small passes (dialogue / meals / mention-index) leverage Pass 1 + wiki nodes via Python+cheap-agent. Opus validates as a sampling oracle, not a replicator. Total estimated cost for full AGOT smoke + validation: **$50-150**, completable in one session of work.

First test characters: **Ned (POV-rich, posthumous-flashback test)** and **Robert Baratheon (POV-less, cross-POV attribution stress test)**.

Your meals idea fits perfectly — Pass 1 already captured the Food & Drink + Hospitality data; Haiku just normalizes it into meal-event nodes that edge to characters/locations/houses/foods. Probably the cheapest pass we'll run (~$10-30 for the entire corpus).

Open questions are real — I have leans (Pattern 1 first, mention index first, Ned first, Haiku for meals) but you should redirect freely.

Next session: review this prompt, resolve open questions, build the mention index as the free unblocker, smoke the dialogue pass on 3 Ned chapters, smoke the meals pass on the Winterfell feast.
