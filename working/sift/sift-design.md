# The Sift — design doc

> # ⏸️ DEFERRED — DO NOT RESUME UNTIL AFTER THE ENRICHMENT CAMPAIGN
> **Status (2026-06-27):** Stage 1 is **BUILT, smoke-tested, and parked.** Matt deferred the **entire Sift track**
> until enrichment work is further along — *"deferring SIFT entirely until after enrichment… I'll pick it back up."*
> **Do not** resume Stage 1, start Stage 2 (`interpret`), tune the lexicon, or run a full-corpus scan until Matt
> reopens it. Stage 2 is also blocked by design until the enrichment track frees the edges layer.
> - **Resume here:** [`progress/continue-prompts/archive/2026-06-27-sift-stage1-deferred-resume-after-enrichment.md`](../../progress/continue-prompts/archive/2026-06-27-sift-stage1-deferred-resume-after-enrichment.md)
> - **Pipeline diagram:** [`working/sift/sift-pipeline-diagram.svg`](sift-pipeline-diagram.svg) — Stage 1 ran (Python); Stage 2 = 0 Haiku calls.
> - **Latest re-smoke (Opus review):** [`working/sift/smoke-test-report-v2.md`](smoke-test-report-v2.md) — 172 pointers → 133 clusters, lens v2.
> - **What exists:** `scripts/sift.py` (engine), `working/sift/lenses/oaths.lens.json` (v2, 74 triggers), `weirwood sift` CLI. Component table: §0 below.

> **What this is:** a fast, reusable two-stage corpus scanner. Stage 1 (Python, deterministic) drops *pointers*
> **What this is:** a fast, reusable two-stage corpus scanner. Stage 1 (Python, deterministic) drops *pointers*
> at every trigger-phrase hit across the chapter corpus. Stage 2 (Haiku, gated, deferred) reads each pointer and
> decides what to do with it. The first lens is **oaths & vows**.
>
> **What this is NOT:** the harvest queue. `working/harvest-queue.md` is *human-authored, opportunistic, mid-task
> breadcrumbs*. The Sift is *machine-exhaustive, single-category, scheduled*. They never share files. The Sift may
> **read** harvest rows to suppress duplicate proposals; it **never writes** to the queue. Every output file carries
> a header line saying so.

---

## §0 — Component status

| # | Component | Path | Status |
|---|-----------|------|--------|
| 1 | Scan engine (`Sift` class, Stage 1 `run`) | `scripts/sift.py` | ✅ built (S-meta 2026-06-27; Opus review pass) |
| 2 | Lens spec format (JSON) | `working/sift/lenses/*.lens.json` | ✅ built |
| 3 | Oaths & vows lens | `working/sift/lenses/oaths.lens.json` | ✅ built (v2 — recall-expanded 2026-06-27) |
| 4 | Smoke test (AGOT) + lexicon tuning | `working/sift/oaths/` | ✅ smoke done; recall tuning done, **exclusions still pending Matt** |
| 5 | `weirwood sift` CLI verbs | `scripts/weirwood.zsh` | ✅ built (`status`/`run`/`sample`/`interpret`/`backfill-aliases` passthrough) |
| 6 | Stage 2 `interpret` (Haiku, gated) | `scripts/sift.py` + prompt | **deferred** (design below) |
| 7 | Alias backfill → node `aliases:` + resolver rebuild | `scripts/sift.py backfill-aliases` | **deferred** (design below) |

Codification still pending Matt's go: one worklog **Active Decision** naming *the corpus-sift track* and the
`sift` / `lens` vocabulary. Not written yet.

**Opus review pass (2026-06-27) — engine deltas beyond the original spec:**
- **`cluster_id` + `cluster_size`** on every pointer. Co-located hits (same chapter, snippet windows overlapping
  within `lines_before+lines_after`) share one `cluster_id` = `<chapter_file>:<first_line>`. The Night's Watch vow
  fires **8 triggers on one line** → ONE cluster, not 8 candidates. **This corrects a spec error:** the original
  smoke report claimed Stage-2 `cand_id` dedups the multi-fire, but `cand_id` keys on *trigger*, so co-located hits
  (different triggers) get distinct ids and would NOT dedup. `cluster_id` is the right grouping key; Stage 2 should
  iterate clusters, not raw pointers (94 clusters vs 116 pointers in AGOT).
- **`ptr_id`** = `sha1(book|chapter_file|line|match_start|trigger_norm)[:12]` — stable per-pointer identity.
- **`<book>.coverage.json`** written alongside each `<book>.pointers.jsonl` — machine-readable trigger coverage
  (hits/trigger, zero-hit list, cluster count), deterministic + diffable across runs.
- **`sift sample --lens X [--book Y] [-n N]`** — deterministic trigger-stratified preview for human review.
- **Manifest honesty:** sha256 manifest records input *and* output hashes (audit/idempotency record), NOT a skip
  cache. Per-file skip is deliberately NOT built — a full corpus scan is sub-second (YAGNI; escape hatch documented).

---

## 1. Architecture — one wrapper, lenses are data

A single generic `Sift` class with effectively **one public entry point**. Each lens is **data, not code** — a JSON
file the wrapper reads. Adding a lens = drop a new `*.lens.json`; **zero code change**. No per-lens subclass, no
hardcoded per-lens methods. (We revisit that only if a future lens needs genuinely different *logic* rather than a
different word list — the whole keyword-scan family shares this one engine.)

```
Sift(lens_path)            # load + compile a lens
  .run(book=None)          # Stage 1 — Python scan → pointers JSONL   (the public method)
  .interpret(book=None)    # Stage 2 — Haiku over pointers → candidates JSONL   (deferred)
  .backfill_aliases()      # optional — write surface forms into node aliases:  (deferred)
```

**The seam (the core design call):** the **engine owns *where*** — it emits a pointer for every literal trigger hit,
with zero interpretation. The **lens owns *what* and *what-next*** — the trigger lexicon, exclusion regexes, the
snippet window, and (Stage 2) the interpret prompt + candidate schema. Do not let meaning-judgment leak into the
engine; "is this *really* a vow" is Haiku's job, not the scanner's. **Python points, Haiku judges.**

---

## 2. Stage 1 — the scan engine (`scripts/sift.py`)

Pure Python, deterministic, resumable. **stdlib `re` only — no dependency.** (Verified workload: 371 files / ~11 MB,
a few hundred triggers per lens → one compiled alternation scans the corpus in well under a second.)

**Switch-trigger to `pyahocorasick`:** only if total pattern count exceeds ~2,000 or a profile shows the scan past
~2 s. Document it; don't pre-install.

### Algorithm
1. **Build the matcher once per lens:**
   - Collect every trigger surface form. `re.escape()` each.
   - **Sort longest-first**, join with `|`. Python `re` alternation is *first-alternative-wins*, not longest-wins —
     ordering is what makes `apple tart` beat `apple` / `Night gathers, and now my watch begins` beat `watch`.
   - Wrap with **content-keyed lookarounds**, not a blanket `\b`: `(?<!\w)(?:ALTERNATION)(?!\w)`. A blanket `\b`
     breaks on multi-word / punctuated triggers (a trigger ending in `’` or `.`). Lookarounds reject `Crabapple`
     while allowing triggers that start/end on punctuation.
   - Compile with `re.IGNORECASE | re.UNICODE`.
2. **Curly-quote normalization (the real trap):** the prose uses U+2019 `’` apostrophes and `“ ”` quotes. A trigger
   typed with a straight `'` will **silently miss**. Normalize quote chars on *both* the trigger list and the text
   before matching — but use **1:1 char swaps only** (’→', “→", ”→") so character offsets stay stable. Do **not** do
   length-changing normalization (NFKD etc.) on the matched copy, or line/offset math desyncs.
3. **Line numbers (frontmatter-safe):** read the whole file (frontmatter included — readers want a line that opens
   the file at the right place). Build a cumulative line-start offset array; `bisect` each match start into it to get
   the true 1-based line. The ~9-line YAML header just falls out correctly; don't strip-and-re-zero.
4. **Snippet:** slice ±N lines around the hit line from the line list; clamp at file ends. N from the lens
   (`snippet.lines_before` / `lines_after`, default 2/2).
5. **Longest-match / overlap:** with longest-first ordering, `re.finditer` over the lookaround pattern gives one hit
   per position; if two triggers genuinely overlap at different starts, keep both (Stage 2 dedups by `cand_id`).
6. **Emit + sort:** one pointer row per hit. Sort the output deterministically by
   `(chapter_file, line, match_start, trigger)`.
7. **Resumability:** store `sha256(raw_bytes)` per file in a sidecar manifest (`working/sift/<lens>/.manifest.json`);
   skip unchanged files, rewrite only changed files' pointer blocks. Output is idempotent — same input → byte-identical.

### Pointer schema (Stage 1 output, JSONL)
```json
{"lens":"oaths","book":"AGOT","chapter_file":"agot-jon-01.md",
 "line":342,"match_start":1187,"trigger":"I shall take no wife",
 "snippet":"…±N lines of context…"}
```
Path: `working/sift/oaths/<book>.pointers.jsonl` (per-book partition). First line of every file is a comment header:
`# SIFT OUTPUT — lens=oaths — NOT the harvest queue. See working/sift/sift-design.md`.

---

## 3. Lens spec (JSON)

One file per lens at `working/sift/lenses/<lens>.lens.json`. Curated, version-controlled. Self-documenting; do not
write a separate prose doc per lens.

```jsonc
{
  "name": "oaths",
  "version": 1,
  "category": "oath_or_vow",
  "snippet": { "lines_before": 2, "lines_after": 2 },
  "triggers": [
    // surface form; optional node_slug hint for Stage 2 resolution; word_boundary defaults true
    { "surface": "I vow" },
    { "surface": "by the old gods and the new" },
    { "surface": "Night gathers, and now my watch begins" }
  ],
  "exclusions": [],                 // Python stop-phrase regexes — START EMPTY, populate AFTER smoke test
  "interpret": {                    // Stage 2 (deferred)
    "model": "claude-haiku-4-5-20251001",
    "prompt_file": "working/sift/lenses/oaths.interpret.md",
    "candidate_schema_ref": "#oaths-candidate"
  }
}
```

**Triggers as data, not hand-edited-forever:** once a lens's surface forms are confirmed, write them back into the
matching graph nodes' `aliases:` field (step 7) so the resolver and future scans benefit — closing the loop.

---

## 4. First lens — oaths & vows

**Why first:** crisp ritual triggers (cleaner to grep than food), genuinely needs Haiku (who swore what to whom,
kept or broken?), central to the books (Kingslayer, Robb's broken Frey pact → Red Wedding, Night's Watch deserters),
and **not a harvest staple** → keeps the Sift↔harvest boundary unmistakable. Heraldry is queued second.

**What a hit captures (Stage 2):** the *transaction + the verbatim vow*. One oath recurs across the books as separate
pointers — sworn, recalled, kept, broken — which is exactly the loyalty/betrayal spine.

- *Jon takes the black* → taker `Jon Snow`, oath `Night's Watch vow`, to `the Night's Watch`,
  quote `"Night gathers, and now my watch begins…"`, status `sworn`.
- *Jaime brooding on the white cloak* → same Kingsguard oath, status `broken/anguished`, different quote.
- *"You have eaten my bread and salt"* → `guest right`, status `invoked`; later Red Wedding → status `violated`.

### Seed lexicon (expand from corpus during smoke test)
- **Swearing:** `I swear`, `I vow`, `I pledge`, `you have my word`, `on my honor`, `swore an oath`, `sworn sword`,
  `say the words`, `said the words`, `took the black`, `do you swear`, `I do solemnly swear`.
- **Night's Watch vow lines:** `Night gathers, and now my watch begins`, `I shall take no wife`, `hold no lands`,
  `father no children`, `the sword in the darkness`, `the watcher on the walls`, `the shield that guards the realms of men`.
- **Fealty:** `swear fealty`, `pledge fealty`, `bend the knee`, `I am your man`, `your liege`, `your grace's man`.
- **Kingsguard / knighthood:** `white cloak`, `knight of the Kingsguard`, `in the name of the Warrior`, `Arise, Ser`.
- **Marriage / betrothal:** `take this woman`, `take this man`, `one flesh, one heart, one soul`, `with this kiss I pledge`.
- **Guest right:** `bread and salt`, `guest right`, `eaten my bread`, `under my roof`, `a guest beneath`.

`exclusions` starts **empty**. Run the raw scan, eyeball the noise, *then* add stop-phrases (e.g. idle "I swear I'll
kill you" threats vs. true vows) — and only the ones the smoke test proves we need. Don't pre-build against imagined
problems.

### Oaths candidate schema (`#oaths-candidate`, Stage 2 output — gated)
```json
{"cand_id":"<sha1 of book|chapter:line|trigger_norm>",
 "lens":"oaths","book":"ASOS","chapter_file":"asos-...","line":342,
 "evidence_quote":"<verbatim, line-verified>",
 "oath_taker":"<entity slug or name>","to_whom":"<entity/institution>",
 "oath_name":"Night's Watch vow | Kingsguard vow | guest right | marriage vow | fealty | <free>",
 "vow_quote":"<verbatim words of the vow, if quoted>",
 "status":"sworn | recalled | kept | broken | invoked | violated | refused",
 "confidence_tier":"1 (verbatim) | 2 (inferred)",
 "dup_against":"<existing node quote already covering this, if any>",
 "verdict":"accept | reject | escalate",
 "record_status":"candidate"}
```
**`verdict:reject` is expected and fine** — that's Haiku throwing away false positives Python couldn't (the whole
point). Candidates are gated: they go to a review file, **never** auto-merged into `graph/nodes/`.

---

## 5. Stage 2 — `interpret` (deferred design)

Separate verb so Python-before-Agent is *structural*, not just intended. For each pointer, a Haiku call reads the
snippet (± context) and emits one candidate row per the schema, or rejects. Cheapest viable model = Haiku
(`claude-haiku-4-5-20251001`), never Sonnet/Opus for the bulk pass.

**Gating (hard rules):** `interpret` prints volume + cost estimate and **requires confirmation** — it does not fire
on invocation (per "never run extractions without asking"). Output is candidates for Matt's review.

**Edge ambition is DEFERRED until enrichment frees the edges layer.** Stage 2 v1 emits *candidate rows + node
`## Quotes` enrichment only*, NOT typed edges. Turning oaths into `SWORE_TO` / `BROKE_OATH_TO` /
`GRANTED_GUEST_RIGHT` edges waits — two tracks writing into the monolithic `edges.jsonl` in parallel is the exact
conflict that keeps enrichment serialized. The pointer maps the Sift produces *now* are useful **input** to the
enrichment track meanwhile (a ready-made "here's everywhere oaths happen" index), so Stage 1 helps rather than competes.

---

## 6. Delta + integrity discipline

- **Delta:** before proposing, diff each candidate against what the target node already cites in `## Quotes`. Surface
  only *new* moments. "Diff against existing quotes, show the delta" = don't re-propose what the graph already has.
- **Resolve-before-mint:** every accept attempts resolution against existing nodes by name+alias; a `new_node` flag
  requires asserting "no existing slug matches." Default action for an existing entity = **append to its `## Quotes`**,
  not spawn a duplicate node.
- **Idempotency:** `cand_id = sha1(book|chapter:line|trigger_norm)`. Re-runs produce identical ids → clean dedup.
- **Harvest separation:** outputs live only under `working/sift/`; Sift may *read* harvest food/oath rows to suppress
  dupes, never writes the queue.

---

## 7. Alias backfill (deferred sub-step)

While assembling a lens's lexicon, write confirmed surface forms back into the matching graph nodes' `aliases:` field
(they're mostly `[]` today). This is a **node mutation** → it must be followed by an index + alias-resolver rebuild
(`weirwood refresh` / the build-*-index scripts), or new aliases aren't discoverable. Aliases must be natural spaced
phrases ("bread and salt"), never kebab slugs. Separate verb: `weirwood sift backfill-aliases --lens <lens>`.

---

## 8. CLI integration (`scripts/weirwood.zsh`)

Mirror the existing subcommand-dispatch pattern; `status` is the bare default.

```
weirwood sift                                   # status: lenses present, last run, pointer counts
weirwood sift run --lens oaths [--book agot]    # Stage 1 — Python scan → pointers   (safe, additive)
weirwood sift interpret --lens oaths [--book X] # Stage 2 — Haiku → candidates (gated; prints cost, asks)
weirwood sift backfill-aliases --lens oaths     # optional — alias writeback + resolver rebuild
```

Keeping `run` and `interpret` as separate verbs makes the Python/LLM split enforceable.

---

## 9. Build sequence (for the builder)

1. Scaffold `working/sift/` and `working/sift/lenses/`. (This design doc already lives here.)
2. Write `scripts/sift.py` — the `Sift` class + engine exactly per §2 (stdlib `re`, longest-first ordering,
   `(?<!\w)…(?!\w)` lookarounds, 1:1 curly-quote normalization, bisect line-map, sha256 resume). Implement `run()`
   first; stub `interpret()` / `backfill_aliases()`.
3. Write `working/sift/lenses/oaths.lens.json` with the §4 seed lexicon, **empty** `exclusions`, snippet 2/2.
4. **Smoke test:** `weirwood sift run --lens oaths --book agot` (or one POV file first). Eyeball the pointers
   *together with Matt*. Tune the lexicon + add only smoke-test-proven `exclusions` (JSON data — no code change).
5. Emit **trigger coverage** as a first-class report: hits per trigger, triggers with zero hits (recall gaps).
6. Wire the `weirwood sift` verbs (§8) into `scripts/weirwood.zsh`.
7. **[Deferred]** Stage 2 `interpret` driver + `oaths.interpret.md` prompt + candidate schema (§4/§5).
8. **[Deferred]** alias backfill (§7).

---

## 10. Compliance checklist

- [ ] Read **local only** (`sources/chapters/`, `graph/nodes/`) — no external fetch, ever.
- [ ] Python-before-Agent: `run` is pure Python; `interpret` (Haiku) only does what needs reasoning.
- [ ] Cheapest viable model: Haiku for Stage 2; never Sonnet/Opus for bulk.
- [ ] Deterministic + resumable: sorted output, sha256 skip, idempotent re-write.
- [ ] Agents propose, Matt decides: Stage 2 → gated candidates, never auto-merged.
- [ ] Separate from harvest: own dir, header lines, never writes the queue.
- [ ] No new capitalized concept-term minted in code (`sift` = command, exempt; `lens` = lowercase artifact).
- [ ] Edge-minting deferred until the enrichment track frees the edges layer.
```
