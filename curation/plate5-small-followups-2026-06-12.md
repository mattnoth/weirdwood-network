# Plate-5 Small Followups — Analysis & Proposals
**Date:** 2026-06-12  
**Scope:** Track 3 followups #1 / #2 / #4 / #5. All proposals only — nothing writes to graph/ or sources/.

> ## ✅ MATT REVIEW — 2026-06-14 (S96 walkthrough): GATE 2 CLEARED
> - **A (collision merges A1 conquest-of-dorne → object.text; A2 tourney-of-maidenpool merge):** APPROVED as proposed.
> - **B (donal-noye ↔ mag mutual-kill reverse edge + optional forward-quote fix):** APPROVED (do B-2 too — fix the forward quote).
> - **C (Contract-6 exemption for SUB_BEAT_OF):** APPROVED. **Clarification of what the exemption means (Matt asked):** it waives ONLY the verbatim `evidence_quote` requirement — `evidence_kind` + `evidence_book` + `evidence_chapter` + `rationale` are STILL required (Contract 5 enforced). SUB_BEAT_OF is a structural grouping claim, not a single-sentence fact, so it's grounded by hub-structure + chapter, not a quote. Also fix the `robb-is-killed` mis-sourced quote (C-2).
> - **D (display-bullet regeneration):** DEFER confirmed — no action.

---

## A. Two Deferred Collision Merges (followup #4)

### A1. `conquest-of-dorne` — reclassify `the-conquest-of-dorne` book→object.text [EXECUTED 2026-06-14]

**Live node inventory:**
| Slug | Path | Type | Pass |
|---|---|---|---|
| `conquest-of-dorne` | `graph/nodes/events/conquest-of-dorne.node.md` | `event.battle` | pass2-wiki-deterministic |
| `the-conquest-of-dorne` | `graph/nodes/events/the-conquest-of-dorne.node.md` | `event.war` | pass2-wiki-deterministic |
| `conquest-of-dorne-battles-b-d-2026-05-01T20-22-20` | `graph/nodes/_conflicts/` | `event.war` | pass2-wiki (v1, Stage-1 agent) |

**Wiki verification (from `sources/wiki/_raw/`):**
- `Conquest_of_Dorne.json` → the historical war/military campaign (157–161 AC, Daeron I). Correct as `event.war` (currently typed `event.battle` — minor subtype question but not a merge issue).
- `The_Conquest_of_Dorne.json` → "is a book written by the Young Dragon, King Daeron I Targaryen, in which he recorded his version of his invasion of Dorne." Clearly `object.text` — a literal in-world book. Currently mis-typed `event.war`.
- `Conquest_of_Dorne_(book).json` → redirect to `The_Conquest_of_Dorne`. Not a separate node.

**S91 flagged issue:** `event-alias-lookup.json` has a multi-canonical collision: the alias "conquest of dorne" resolves to BOTH `conquest-of-dorne` AND `the-conquest-of-dorne` (8 conflicting entries visible in the lookup JSON — the list-value shape). This was flagged as a pre-existing ambiguous collision at S91 alias-resolver rebuild (876→922 phrases, "1 pre-existing ambiguous collision").

**Affected edges:** 0 in `edges.jsonl` (verified — neither slug appears in any edge row).

**Proposed checklist (Matt-approvable):**

- [ ] **A1-1.** Move `graph/nodes/events/the-conquest-of-dorne.node.md` → `graph/nodes/texts/the-conquest-of-dorne.node.md` (create `graph/nodes/texts/` directory if it does not exist, or route to nearest applicable dir per architecture.md).
- [ ] **A1-2.** Update frontmatter: `type: event.war` → `type: object.text`. Optionally update `## Identity` stub line from "a war from the AWOIAF wiki" to "a book written by Daeron I Targaryen (the Young Dragon) recounting his conquest of Dorne."
- [ ] **A1-3.** The `_conflicts/` node (`conquest-of-dorne-battles-b-d-...`) is a Stage-1 agent version of the *event* (same slug `conquest-of-dorne`) — leave in `_conflicts/` per existing convention. No action needed.
- [ ] **A1-4.** Rebuild `event-alias-lookup.json` after reclassification — once `the-conquest-of-dorne` is no longer an event, the alias collision resolves: "conquest of dorne" should map unambiguously to `conquest-of-dorne` (the war). Run: `python3 scripts/event_alias_resolver.py` (rebuilds from `graph/nodes/events/`).
- [ ] **A1-5. Deferred/future:** Add `WRITTEN_BY: daeron-i-targaryen` edge for `the-conquest-of-dorne` once texts pass is underway. (From `cleanup-decisions-resolved.md` §3.)
- [ ] **A1-6. Subtype check (low-priority):** `conquest-of-dorne` is currently `event.battle` but the wiki describes it as a multi-year war/campaign. Consider `event.war` — same as the `_conflicts/` node's type. Not blocking.

---

### A2. `tourney-at-maidenpool` — merge redirect node into canonical [EXECUTED 2026-06-14]

**Live node inventory:**
| Slug | Path | Type | Edges |
|---|---|---|---|
| `tourney-at-maidenpool` | `graph/nodes/events/tourney-at-maidenpool.node.md` | `event.tournament` | 0 |
| `tourney-of-maidenpool` | `graph/nodes/events/tourney-of-maidenpool.node.md` | `event.tournament` | 0 |

**Wiki verification (from `sources/wiki/_raw/`):**
- `Tourney_at_Maidenpool.json` → the real page. Tourney held at Maidenpool in **208 AC** (from "The Hedge Knight" source). Melee won by Ser Humfrey Hardyng; Joust: Hardyng defeated Donnel of Duskendale, Donnel Arryn, and Lord Royce. Separate note: "For the tourney at Maidenpool in 103 AC, see Tourney for King Viserys I's accession." — i.e., the 103 AC tourney is a different event with its own wiki page.
- `Tourney_of_Maidenpool.json` → redirect to `Tourney at Maidenpool`. Confirmed: this is just a spelling-variant redirect.

**`cleanup-decisions-resolved.md` §4 decision (Matt 2026-06-06):** canonical = `tourney-at-maidenpool`; merge `tourney-of-maidenpool` into it (SAME_AS/ALIAS_OF + redirect, not deleted).

**Affected edges:** 0 in `edges.jsonl`.

**Proposed checklist (Matt-approvable):**

- [ ] **A2-1.** Add `aliases: ["Tourney of Maidenpool"]` to `tourney-at-maidenpool.node.md` frontmatter.
- [ ] **A2-2.** Add `same_as: tourney-at-maidenpool` to `tourney-of-maidenpool.node.md` frontmatter. Move the file to `graph/nodes/_conflicts/tourney-of-maidenpool.node.md` (per collision-loser convention used in Plates 2.5+5). Do NOT delete.
- [ ] **A2-3.** Rebuild entity index for events dir: `python3 scripts/build-entity-indexes.py --type events --all`.
- [ ] **A2-4. Enhancement (optional):** `tourney-at-maidenpool.node.md` `## Edges` and `## Identity` sections are empty stubs. The wiki content gives: melee winner = Humfrey Hardyng; joust = Hardyng defeated three named opponents; year = 208 AC; source = The Hedge Knight. These could be added as Tier-2 edges (`WINS_TOURNEY_AT` / `PARTICIPATES_IN` / `LOCATED_AT: maidenpool`) in a future texts/events enrichment pass — not required now. Note: the 103 AC tourney (`Tourney for King Viserys I's accession`) is a distinct node and should NOT be conflated.

---

## B. donal-noye ↔ mag-mar-tun-doh-weg Mutual-Kill Reverse Edge (followup #5) [EXECUTED 2026-06-14]

### Existing forward edge (line 1154 in edges.jsonl)

```json
{
  "edge_type": "KILLS",
  "source_slug": "donal-noye",
  "target_slug": "mag-mar-tun-doh-weg",
  "evidence_kind": "book-pass1",
  "evidence_book": "asos",
  "evidence_chapter": "asos-jon-08",
  "evidence_quote": "Donal Noye turned toward the two great trebuchets that Bowen Marsh had restored to working order.",
  "evidence_ref": "sources/chapters/asos/asos-jon-08.md:45",
  "confidence_tier": 1,
  "typed_by": "python-map"
}
```

**Note on forward edge's quote:** The cited quote ("Donal Noye turned toward the two great trebuchets...") does not actually describe the kill — it describes Noye commanding the trebuchets. The mutual kill is described ~125 lines later (around line 171 of asos-jon-08.md). This is a locator-inexactness from the Pass-1 spine; the forward edge would benefit from a better quote but that is a Track-A backfill concern, not blocking the reverse-edge addition.

### Chapter evidence for the mutual kill (ASOS Jon VIII, ~line 171)

> *"Noye's sword was sunk deep in the giant's throat, halfway to the hilt. The armorer had always seemed such a big man to Jon, but locked in the giant's massive arms he looked almost like a child. 'The giant crushed his spine. I don't know who died first.'"*

This confirms the mutual kill unambiguously: Noye killed Mag by stabbing him in the throat; Mag killed Noye by crushing his spine. Jon witnesses the aftermath and explicitly says "I don't know who died first."

### Proposed reverse-direction edge (full JSON, append-ready)

```json
{"edge_type": "KILLS", "source_slug": "mag-mar-tun-doh-weg", "target_slug": "donal-noye", "decision": "emit_edge", "candidate_kind": "curator-s92-mutual-kill", "evidence_kind": "book-pass1", "evidence_book": "asos", "evidence_chapter": "asos-jon-08", "evidence_section": "Relationships Observed", "evidence_quote": "Noye's sword was sunk deep in the giant's throat, halfway to the hilt. The armorer had always seemed such a big man to Jon, but locked in the giant's massive arms he looked almost like a child. 'The giant crushed his spine. I don't know who died first.'", "evidence_ref": "sources/chapters/asos/asos-jon-08.md:171", "confidence_tier": 1, "typed_by": "curator-s92", "asserted_relation": "mutual kill — Mag crushed Noye's spine while Noye stabbed Mag in the throat", "schema_version": "pass1-derived-v1", "produced_at": "2026-06-12T00:00:00+00:00"}
```

**Notes:**
- Uses `evidence_ref` line 171 (where the aftermath is described) rather than line 45 (the forward edge's mismatched cite — the reverse edge gets the better quote).
- `typed_by: curator-s92` matches the S91 deception-pilot convention.
- No schema changes required — `KILLS` is already in locked vocab.
- Also propose updating the forward edge's `evidence_quote` to the same passage (same line 171) to fix the forward edge's mismatched cite. This is cosmetic / Track-A territory, but can be folded in at the same time (no schema change).

**Checklist:**
- [ ] **B-1.** Append the reverse edge JSON row to `graph/edges/edges.jsonl`.
- [ ] **B-2.** (Optional / Track A) Update forward edge's `evidence_quote` from the trebuchet quote to the mutual-kill passage for accuracy.
- [ ] **B-3.** Run `python3 scripts/graph-query.py --neighbors donal-noye` and `--neighbors mag-mar-tun-doh-weg` to verify both KILLS edges are present and traversable.

---

## C. 32 Empty-Quote SUB_BEAT_OF Disposition Memo (followup #2) [C-1 EXECUTED 2026-06-14; C-2 EXECUTED 2026-06-14; C-3 deferred]

### Data summary

32 SUB_BEAT_OF rows in `edges.jsonl` have empty `evidence_quote`. All carry a `plate5_evidence_note` field: "SUB_BEAT_OF structural classification; no verbatim book quote — see rationale field." These are Plate 4 Pass-B/Pass-C Haiku inference-only emissions. The type-contract validator (Contract 6: empty evidence_quote → drop) flagged them at Plate 5 as read-only audit; they remain in `edges.jsonl` live. 2 of 32 also have empty `evidence_chapter` (`tyrell-plot-revealed→purple-wedding`, `trail-followed-north-northwest→sack-of-winterfell`).

### Sample of 8 (randomly drawn)

| Beat slug | Parent event | Chapter | Beat quote findable? |
|---|---|---|---|
| `gendry-captured` | `fight-at-the-holdfast` | ACOK Arya V | YES — "gendry" + "captured" both in chapter; "fight at the holdfast" verbatim present |
| `aeron-damphair-demands-benfred-s-death` | `harrying-of-the-stony-shore` | ACOK Theon III | LIKELY — "benfred" + "damphair" in chapter; harrying-of-the-stony-shore context present |
| `taena-recounts-renly-s-wedding-night` | `wedding-of-renly-baratheon-and-margaery-tyrell` | AFFC Cersei VI | LIKELY — "taena" + "renly" + "wedding night" phrase in chapter |
| `guards-killed` | `fall-of-harrenhal` | ACOK Arya IX | LIKELY — "guards" + "killed" + "jaqen" in chapter |
| `wedding-morning-daario-leaves-angrily` | `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen` | ADWD Daenerys VII | LIKELY — "daario" + "morning" in chapter; anger context retrievable |
| `crossbows-kill-more-northmen` | `red-wedding` | ASOS Catelyn VII | LIKELY — "crossbow" + "northmen" in chapter; the massacre scene is there |
| `wedding-feast-begins` | `wedding-of-tyrion-lannister-and-sansa-stark` | ASOS Sansa III | YES — "wedding feast" phrase + "music" + feast description present |
| `trail-followed-north-northwest` | `sack-of-winterfell` | (empty) | NO — no chapter reference; context is Bran/Rickon hiding in crypts |

**Estimate from sample:** 7/8 beats have identifiable prose in the correct chapter. The 1 miss (`trail-followed-north-northwest`) has no chapter reference at all. Extrapolated: ~27–29 of the 32 rows are deterministically backfillable; 2–4 (those with empty/wrong chapter or abstract structural beats) require either inference or exemption.

### 33rd data point: `robb-is-killed SUB_BEAT_OF red-wedding`

This row is **NOT** in the 32 empty-quote set — it has a non-empty `evidence_quote`. But the quote is: `"DEFEATS: Warden of the North (track_b: Result)"` — a wiki display-bullet string copied from the red-wedding node's `## Edges` section, not a chapter quote. It passed Contract 6 (non-empty) but carries a qualitatively mis-sourced quote. This is a distinct defect class from the 32 empty-quote rows: the evidence string exists but is drawn from the wrong source layer (wiki display-bullet vs book prose). The forward-edge quote fix in §B above is the same defect class.

### Three options

**(a) Targeted LLM re-emit pass (~$1–3, 32 rows)**  
Re-run the Plate 4 Haiku classifier on these 32 rows with an explicit "you must provide a verbatim `evidence_quote` from the chapter or emit nothing" constraint. Input: beat slug + parent event + `evidence_chapter` field + chapter file content. Model: Haiku 4.5 (same as Plate 4). Per drift-detection rule: validate first batch of ~10 before committing. Cost: 32 rows × ~2K tokens context each ≈ 64K input + 32 × 100-token outputs ≈ $0.10–$0.50 Haiku; orchestration overhead 5–10× → ~$1–5. Risk: some Haiku-class quotes may be paraphrase rather than verbatim (same Plate 4 drift issue that emptied these quotes in the first place). Requires: smoke-test 5 rows by hand, compare quote vs chapter text.

**(b) Deterministic quote-backfill script (~$0, ~27–29 rows fixable)**  
Python script: for each row, load the chapter file, search for a passage containing key terms from the beat slug (e.g., "crossbow" ∩ "northmen" for `crossbows-kill-more-northmen`), extract the best-matching sentence as the `evidence_quote`. Success rate from sample: 7/8 = 87.5% → ~28/32 rows. The remaining 2–4 (empty chapter, abstract structural beats like `trail-followed-north-northwest`) fall through to option (c). Script output is deterministic and reviewable before write. No LLM cost; no drift risk. Limitation: quote is located by keyword proximity, not by semantic match — may pick a nearby sentence about the same event rather than the best one-line quote.

**(c) Contract-6 exemption for SUB_BEAT_OF structural edges**  
Add `SUB_BEAT_OF` to the Contract 6 exemption list in the type-contract validator: structural parent-linking edges whose truth is established by the event-hub structure rather than a single prose sentence do not require `evidence_quote`. The 32 rows are cleared; the robb-is-killed mis-sourced quote is a separate cleanup. Zero cost, zero risk. This is the lightest path and is architecturally defensible — a structural edge saying "beat X is a sub-beat of event Y" is grounded by the event's chapter and the existence of the hub, not a single quotation. The `plate5_evidence_note` + `rationale` fields already provide human-readable justification. Contract 5 (evidence_kind + evidence_book/chapter) remains enforced for all SUB_BEAT_OF rows.

### Recommendation: **(c) + targeted cleanup for the robb-is-killed mis-source**

Add the Contract-6 exemption now (zero cost, removes the validator noise). Separately, queue the mis-sourced `robb-is-killed` quote fix alongside the forward-edge quote fix in §B (same session, cosmetic). Option (b) is worth building if/when the Track-A backfill script is being written anyway (reuse the keyword-proximity pattern); at that point the 28 recoverable quotes become a byproduct of the same pass at no additional cost.

**Checklist:**
- [ ] **C-1.** Add `SUB_BEAT_OF` to Contract-6 exemption list in the type-contract validator (or in the plate5-merge.py validator logic). Document: "SUB_BEAT_OF structural classification edges are exempt from evidence_quote requirement per 2026-06-12 decision; truth grounded by event-hub structure + rationale field."
- [ ] **C-2.** Fix `robb-is-killed SUB_BEAT_OF red-wedding` `evidence_quote`: replace `"DEFEATS: Warden of the North (track_b: Result)"` with a real chapter quote. Suggested: *"'The king!' she heard them cry. 'They're killing all the king's men!'"* or *"She saw the crossbows"* (ASOS Catelyn VII) — pick whatever verbatim line is most accurate. (This can share a session with §B-2.)
- [ ] **C-3.** (Future/optional) When Track-A backfill script is built, include a keyword-proximity pass to recover ~28 quotes for the 32 rows as a byproduct.

---

## D. Display-Bullet Regeneration Dry-Run (followup #1)

### Current state

All 5 sample nodes exist. Their `## Edges` sections show pre-Plate-5 state (wiki track_b bullets only — the pass2-wiki deterministic emitter wrote them):

| Node | Node-file bullets | Active edges in edges.jsonl |
|---|---|---|
| `red-wedding` | 3 (FIGHTS_IN, DEFEATS ×2 — all wiki track_b) | 8 incoming SUB_BEAT_OF |
| `walder-frey` | 49 (all wiki track_b: HOLDS_TITLE, SWORN_TO, SPOUSE_OF, PARENT_OF, etc.) | 45 outgoing + incoming active |
| `catelyn-stark` | 19 (all wiki track_b) | 168 outgoing + incoming active |
| `jon-snow` | 8 (all wiki track_b) | 331 outgoing + incoming active |
| `twins` | 2 (RULES, WORSHIPS — wiki track_b) | 10 incoming LOCATED_AT |

**Diff shape:**
- `red-wedding`: 3 pre-Plate-5 wiki bullets (none of which are SUB_BEAT_OF) → 8 SUB_BEAT_OF incoming. Net: +8 new bullet types, 3 old bullets effectively superseded (they reflect pass2-wiki track_b, not edges.jsonl). High divergence.
- `catelyn-stark`: 19 node bullets vs 168 active edges — massive gap. The 19 bullets are wiki infobox (SWORN_TO, SPOUSE_OF, PARENT_OF, etc.); the 168 edges include rich book-pass1 edges (MOURNS, RESENTS, CAPTURES, COMPANION_OF, etc.) that are not in the node file at all.
- `jon-snow`: 8 node bullets vs 331 active edges — extreme gap. The node file shows only title/allegiance; the graph has 187 outgoing + 144 incoming edges for this node.
- `twins`: 2 bullets (RULES, WORSHIPS) vs 10 incoming LOCATED_AT — all 10 incoming LOCATED_AT edges are Plate 3 reified role edges that post-date the node file entirely.

### Script proposal

**Option 1: Build `scripts/build-node-display-edges.py` (regenerate-all)**  
Script reads `edges.jsonl`, groups by source and target slug, writes a regenerated `## Edges` section to each node file. Scope: 1,330 unique node slugs in active edges × average write cost = straightforward Python. Estimate: 2–4 hours to build + test + dry-run report; ~30 min to apply after review. No LLM cost. Risk: node file structure varies (some have `## Origins`, `## Narrative Arc`, etc.); the script must parse section boundaries carefully and avoid overwriting non-Edges content. The current node files mix wiki-infobox bullets (some of which have `(track_b: X)` annotations useful for display) with nothing — a regenerator would homogenize the display format.

**Option 2: Declare node-file bullets human-legacy**  
Accept that `## Edges` in node files is a human-readable legacy snapshot (pre-Plate-5 state). Canonical authority is `edges.jsonl` + `graph-query.py --neighbors`. Do not build the regenerator now; revisit after the infobox merge (~18–19k new wiki edges) and Mode-3 dip have landed and the graph shape is stable.

### Infobox merge changes the math

The greenlit infobox merge (~18–19k Tier-2 wiki edges from `working/wiki/data/infobox-data.jsonl`) will add edges to ~5,279 pages' worth of nodes. After the merge, the `walder-frey` and `catelyn-stark` type nodes will each have dozens more edges (infobox fields: SWORN_TO, PARENT_OF, SPOUSE_OF, CULTURE_OF, etc.). Building the display-edge regenerator *before* the infobox merge means running it again immediately after. The per-node edge count will roughly double for well-connected characters and triple for event hubs that pick up FOUGHT_IN / LOCATED_AT infobox edges.

**Recommendation: Option 2 (declare legacy), build the regenerator after infobox merge lands.**  
The right sequence: infobox merge → Mode 3 dip → *then* build `scripts/build-node-display-edges.py` once the graph is stable. Building it now produces output that will be immediately stale after the merge. The 1,330 nodes with active edges are already fully traversable via `graph-query.py`; node-file display bullets are cosmetic for human browsers and have zero effect on agent queries.

**Checklist:**
- [ ] **D-1.** Defer `build-node-display-edges.py` until post-infobox-merge.
- [ ] **D-2.** When built: design the script to read `edges.jsonl` directly (not node files), group edges by slug (outgoing and incoming separately), render as `- EDGE_TYPE: target_slug [tier, evidence_kind]` per bullet, write only the `## Edges` section, leave all other sections intact.
- [ ] **D-3.** Scope confirmation for the build session: 8,516 total `.node.md` files; 1,330 currently have active edges (will grow post-infobox merge to ~5,000–6,000+). The regenerator is a 1–2 hour Python task.

---

## Summary (≤20 lines)

**A. Collision merges:**  
- `the-conquest-of-dorne`: reclassify `event.war` → `object.text`, move to `graph/nodes/texts/`. 0 affected edges. Alias resolver collision resolves as byproduct (rebuild alias lookup after move). No merge needed between `conquest-of-dorne` (the war) and `the-conquest-of-dorne` (the book) — they are distinct entities.  
- `tourney-at-maidenpool`: merge `tourney-of-maidenpool` (redirect node, 0 edges) into canonical; add alias; quarantine loser. Simple 3-step apply.

**B. Mutual-kill reverse edge:**  
Propose exact JSON row: `mag-mar-tun-doh-weg KILLS donal-noye`, evidence_quote from ASOS Jon VIII ~line 171 ("Noye's sword was sunk deep in the giant's throat... The giant crushed his spine. I don't know who died first."). Also note: forward edge's quote is mismatched (trebuchet cite) and can be fixed at same time.

**C. 32 empty-quote SUB_BEAT_OF:**  
Sample of 8 → 7/8 beats have prose findable in the chapter (est. ~28/32 deterministically backfillable). **Recommend (c): Contract-6 exemption for SUB_BEAT_OF** (zero cost, architecturally sound). Separately fix `robb-is-killed`'s mis-sourced wiki-display-bullet quote (33rd data point — non-empty but wrong source layer).

**D. Display-bullet regeneration:**  
Diff is large: `jon-snow` has 331 active edges vs 8 node-file bullets; `red-wedding` has 8 SUB_BEAT_OF in edges.jsonl vs 3 stale wiki bullets in node file. **Recommend: defer `build-node-display-edges.py` until after infobox merge** (~18–19k incoming edges doubles/triples per-node counts; building it now produces immediately stale output). 1,330 nodes currently have active edges; will grow to ~5,000+ post-merge. Scope: 2–4 hour Python build when the graph is stable.
