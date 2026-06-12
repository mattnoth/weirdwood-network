# Continue Prompt: Graph Cleanup — Hub-Triage FIX-22 + Plate-5 Small Followups

**Status:** GATED (see gates below)
**Recommended model:** Sonnet 4.6 (scripted edits + verification; all judgment calls were made in the curation files Matt approves at Step 0)
**Created:** 2026-06-12 (Session 92)

---

## Context

Two curation files produced in S92 contain the full analysis and proposed actions for this cleanup session. Nothing has been applied to the graph yet.

**Source files:**
- `curation/hub-review-triage-2026-06-12.md` — FIX 22 / QUARANTINE 10 / KEEP 81 (full hub-review queue triage + 4 S89 wrong-direction role edges)
- `curation/plate5-small-followups-2026-06-12.md` — 4 followup groups: A (collision merges), B (donal-noye↔mag reverse edge + forward-edge quote fix), C (32 empty-quote SUB_BEAT_OF disposition + robb-is-killed mis-sourced quote fix), D (display-bullet regeneration — DEFERRED)
- `working/todos.md` Track 3 — F1c dangling edge, 3 unlinked Red Wedding beats (incl. Dacey Mormont's death), LOCATED_AT direction doc reconcile

**Expected magnitude:** ~30–45 edge rows touched (adds/drops/retypes) + 2–4 node moves. The point is precision, not volume.

---

## HARD GATE 1 — Infobox merge must have shipped first

**Do not begin any Step beyond Step 0 unless `graph/edges/edges.jsonl` contains `evidence_kind: wiki-infobox` rows and the row count is approximately 21,766.**

```bash
python3 -c "
import json
rows = [json.loads(l) for l in open('graph/edges/edges.jsonl')]
wiki = sum(1 for r in rows if r.get('evidence_kind') == 'wiki-infobox')
print(f'Total rows: {len(rows)}')
print(f'Wiki-infobox rows: {wiki}')
print('GATE OPEN' if wiki > 0 and len(rows) > 20000 else 'GATE CLOSED — infobox merge not yet shipped')
"
```

**Why this gate exists:** The infobox merge script (`scripts/infobox-merge.py`) performs a dry-run-reverification that halts on any `edges.jsonl` drift. If cleanup edits land in `edges.jsonl` before the merge ships, the merge's expected-count check will fail and block the ship. The infobox merge is the higher-priority track and must complete first.

**Sequencing pointer:** `progress/continue-prompts/2026-06-12-infobox-merge-ship.md`

---

## HARD GATE 2 — Matt's approval in curation files

**Matt must review and annotate both curation files before execution begins.**

**Convention:** Matt strikes through or annotates items he rejects. Everything unmarked = approved as proposed. A note of "SKIP" or "REJECT" next to any item is sufficient.

Check for annotations before proceeding. If curation files look untouched (no markup at all), stop and ask.

---

## Step 0 — Pre-flight

Read both curation files in full and confirm Gate 1 and Gate 2 are satisfied:

1. Verify `edges.jsonl` row count ≈ 21,766 with `evidence_kind: wiki-infobox` rows present (Gate 1)
2. Confirm Matt has reviewed and annotated both curation files (Gate 2)
3. Note which FIX items Matt approved vs. rejected (default: all approved if unmarked)

---

## Step 1 — Backup

```bash
TIMESTAMP=$(date +%Y-%m-%dT%H-%M-%S)
cp graph/edges/edges.jsonl "graph/edges/_regrounding/edges-pre-graph-cleanup-${TIMESTAMP}.jsonl"
echo "Backed up to graph/edges/_regrounding/edges-pre-graph-cleanup-${TIMESTAMP}.jsonl"
```

Follows the Plate-5 convention: timestamped backup to `graph/edges/_regrounding/` before any write.

---

## Step 2 — Execute approved FIX items (scriptable batch)

The following items from `curation/hub-review-triage-2026-06-12.md` are tagged **scriptable** and can be executed in a single Python script with a dry-run gate:

**F1a/F1c — Repair the siege-of-storms-end edges:**
- F1a: Repoint the 5 dropped staged role edges from `working/edge-modeling/plate3-full/role-edges-staging.jsonl` to `siege-of-storms-end-299` and append to `edges.jsonl`. (Roles: `mace-tyrell AGENT_IN`, `stannis-baratheon COMMANDS_IN`, `gawen-wylde VICTIM_IN`, `cressen AGENT_IN`, `davos-seaworth AGENT_IN`) — review F1b role-direction note at merge.
- F1c: Repair the dangling LOCATED_AT edge: `{"source_slug":"siege-of-storm-s-end-recalled","target_slug":"storms-end"}` is live with a never-minted source. Repoint `source_slug` to `siege-of-storms-end-299` (or drop if Matt annotated DROP).

**F5 — Retier the false-confession POISONS edge:**
Find the live edge `tyrion-lannister POISONS joffrey-baratheon` where `asserted_relation` contains "Claims to have poisoned (unverified)". Retier to `confidence_tier: 4` and add/update qualifier to note `false-confession`. **Do this in the same step as F3a** (see Step 3) so the graph doesn't briefly have a retiered tier-4 edge as its only Joffrey-death signal.

**F6a–F6l — 12 missing canon-death/attack dyads:**
Emit direct edges using each queue item's participants + evidence quotes (chapter-scope provenance, `evidence_kind: book-pass1`, `typed_by: curator-s92-graph-cleanup`). Use this slug-resolution map:
- `lady-olenna-tyrell` → `olenna-tyrell`
- `sam-tarly` → `samwell-tarly`
- `wun-wun` → `wun-weg-wun-dar-wun`
- `ser-patrek` → `patrek-of-kings-mountain`
- `pate` → `pate-novice`
- `the-alchemist` → `alchemist`

For F6e (`sam-kills-the-other-with-dragonglass`): if no individual Other node exists, point to the species node `others`. For F6a (`golden-wedding-chalice` as WIELDED_IN artifact role): if no artifact node exists, drop the role rather than minting an unreviewed artifact node.

**Write the script to `scripts/graph-cleanup-2026-06-12.py`, run with `--dry-run` first, print a row-count summary, then re-run without `--dry-run` only after the dry-run output looks correct.**

---

## Step 3 — Execute approved FIX items (manual/judgment)

These items from `curation/hub-review-triage-2026-06-12.md` require individual edge edits. Apply only the ones Matt approved:

**F2a–F2d — 4 wrong-direction role edges (live in edges.jsonl, S89 additions):**
- F2a: `robb-stark COMMANDS_IN lord-walder-calls-for-the-bedding` → **Drop** (if approved)
- F2b: `greatjon-umber AGENT_IN the-bedding-ceremony-begins` → **Retype to ATTENDS** (if approved)
- F2c: `catelyn-stark AGENT_IN the-wedding-feast-proceeds` → **Retype to ATTENDS** (if approved)
- F2d: `house-tyrell VICTIM_IN tyrell-plot-revealed` → **Retype to AGENT_IN** (if approved)

**F3a — Mint `death-of-joffrey-baratheon` hub + SUB_BEAT_OF purple-wedding:**
- Slug: `death-of-joffrey-baratheon` (per S91 rename convention: event-named, not action-named)
- Mint node file at `graph/nodes/events/death-of-joffrey-baratheon.node.md`
- Emit role edges: `olenna-tyrell AGENT_IN`, `joffrey-baratheon VICTIM_IN`, `red-keep LOCATED_AT`
- Emit `death-of-joffrey-baratheon SUB_BEAT_OF purple-wedding`
- **MATT'S QUESTION (2026-06-12) — answer before emitting the Olenna edge:** *Is Olenna's agency book canon, or show-only / wiki-imported?* Verified provenance: the queue row is **book-derived (Pass 1, ASOS Sansa chapters), NOT wiki, NOT show** — evidence chain: Dontos gives Sansa the silver hairnet for "the night of Joffrey's wedding" (ASOS Sansa II, `asos-sansa-02.extraction.md`); Olenna fusses with/straightens the hairnet at the feast (queue `evidence_quote`); Sansa discovers a **stone missing from the hairnet** during the escape, and Littlefinger reveals the orchestration aboard the galley (ASOS Sansa V, `asos-sansa-05.extraction.md`); Littlefinger further implicates the Tyrells/Olenna in his later explanations to Sansa. So in the BOOKS Olenna's role is established by inference + Littlefinger's testimony — never witnessed on-page (the show's explicit confession to Jaime is show-only). **Action:** emit `olenna-tyrell AGENT_IN` at **confidence_tier: 2** (the queue row already says confidence 2 — keep it; do NOT let the mint default to tier 1), and carry the hairnet/missing-stone evidence quotes. If Matt wants stricter, tier 3 with qualifier `implied-by-littlefinger-account` is the fallback — note which was chosen in the execution log.
- **Do F3a and F5 together:** after F3a mints the correct attribution hub, execute F5 to retier the false-confession edge. The graph should never have a moment where the retiered tier-4 edge is the only Joffrey-death signal.

**F3b — Mint `wedding-ceremony-at-the-great-sept-of-baelor` + SUB_BEAT_OF purple-wedding:**
- Mint node file at `graph/nodes/events/wedding-ceremony-at-the-great-sept-of-baelor.node.md`
- Emit role edges: `joffrey-baratheon AGENT_IN`, `margaery-tyrell AGENT_IN`, `mace-tyrell ATTENDS`, `great-sept-of-baelor LOCATED_AT`
- Emit `wedding-ceremony-at-the-great-sept-of-baelor SUB_BEAT_OF purple-wedding`

**F4a — Mint `catelyn-secures-guest-right` + SUB_BEAT_OF red-wedding:**
- Mint node file at `graph/nodes/events/catelyn-secures-guest-right.node.md`
- Emit role edges: `catelyn-stark AGENT_IN`, `walder-frey AGENT_IN`, `the-twins LOCATED_AT`
- Emit `catelyn-secures-guest-right SUB_BEAT_OF red-wedding`

**QUARANTINE items: do NOT execute any of the 10 QUARANTINE items.** They wait on Matt or a policy decision (unnamed-victim node policy, Track B routing, individual judgment calls). Leave them exactly as they are.

---

## Step 4 — Execute approved small-followup items

From `curation/plate5-small-followups-2026-06-12.md`:

**A — Collision merges (if approved):**

A1 (`the-conquest-of-dorne` reclassification):
1. Create `graph/nodes/texts/` directory if it does not exist (check `reference/architecture.md` for canonical dir — if `texts/` isn't in the TYPE_DIR_MAP, use the nearest applicable existing dir)
2. Move `graph/nodes/events/the-conquest-of-dorne.node.md` → `graph/nodes/texts/the-conquest-of-dorne.node.md`
3. Update frontmatter: `type: event.war` → `type: object.text`
4. Optionally update `## Identity` stub

A2 (`tourney-at-maidenpool` merge):
1. Add `aliases: ["Tourney of Maidenpool"]` to `graph/nodes/events/tourney-at-maidenpool.node.md` frontmatter
2. Add `same_as: tourney-at-maidenpool` to `graph/nodes/events/tourney-of-maidenpool.node.md` frontmatter
3. Move `tourney-of-maidenpool.node.md` to `graph/nodes/_conflicts/tourney-of-maidenpool.node.md` (per collision-loser convention)

**B — donal-noye ↔ mag mutual-kill reverse edge (if approved):**

B-1: Append the exact JSON row from the curation file to `graph/edges/edges.jsonl`:
```json
{"edge_type": "KILLS", "source_slug": "mag-mar-tun-doh-weg", "target_slug": "donal-noye", "decision": "emit_edge", "candidate_kind": "curator-s92-mutual-kill", "evidence_kind": "book-pass1", "evidence_book": "asos", "evidence_chapter": "asos-jon-08", "evidence_section": "Relationships Observed", "evidence_quote": "Noye's sword was sunk deep in the giant's throat, halfway to the hilt. The armorer had always seemed such a big man to Jon, but locked in the giant's massive arms he looked almost like a child. 'The giant crushed his spine. I don't know who died first.'", "evidence_ref": "sources/chapters/asos/asos-jon-08.md:171", "confidence_tier": 1, "typed_by": "curator-s92", "asserted_relation": "mutual kill — Mag crushed Noye's spine while Noye stabbed Mag in the throat", "schema_version": "pass1-derived-v1", "produced_at": "2026-06-12T00:00:00+00:00"}
```

B-2 (optional): Update the forward edge `donal-noye KILLS mag-mar-tun-doh-weg`'s `evidence_quote` from the trebuchet cite to the mutual-kill passage at line 171 (same quote as the reverse edge). This is cosmetic — only do if Matt approved it.

**C — Empty-quote SUB_BEAT_OF disposition (if approved):**

C-1: Add `SUB_BEAT_OF` to the Contract-6 exemption list in the type-contract validator. Document with the note: "SUB_BEAT_OF structural classification edges are exempt from evidence_quote requirement per 2026-06-12 decision; truth grounded by event-hub structure + rationale field." Find the validator in `scripts/plate5-merge.py` or the type-contract validator module and add the exemption.

C-2: Fix `robb-is-killed SUB_BEAT_OF red-wedding` `evidence_quote`: replace the current value (`"DEFEATS: Warden of the North (track_b: Result)"`) with a verbatim chapter quote from ASOS Catelyn VII. Suggested: *"She saw the crossbows"* or *"'The king!' she heard them cry. 'They're killing all the king's men!'"* — use whichever is most accurate to the chapter text. Verify by reading `sources/chapters/asos/asos-catelyn-07.md` first.

**D — Display-bullet regeneration: DEFERRED.** Do not build `scripts/build-node-display-edges.py` in this session. The curation file's recommendation is to defer until post-infobox-merge graph is stable. No action.

---

## Step 5 — Add 3 missing Red Wedding SUB_BEAT_OF links

Three beats have role edges (AGENT_IN / VICTIM_IN) but are not linked to the Red Wedding hub via `SUB_BEAT_OF`. Verify the current state first:

```bash
python3 -c "
import json
rows = [json.loads(l) for l in open('graph/edges/edges.jsonl')]
red_wedding_beats = [r for r in rows if r.get('target_slug') == 'red-wedding' and r.get('edge_type') == 'SUB_BEAT_OF']
print('Current red-wedding beats:')
for r in red_wedding_beats:
    print(' ', r['source_slug'])
"
```

The beats to add (check each against current output above before adding — only add if not already present):

1. `ser-ryman-kills-dacey-mormont SUB_BEAT_OF red-wedding` — Dacey Mormont's death at the Red Wedding
2. `the-camp-becomes-a-battlefield SUB_BEAT_OF red-wedding` — the wider massacre beat
3. `red-wedding-revealed SUB_BEAT_OF red-wedding` — if this beat slug exists in the graph

For evidence: use `evidence_kind: book-pass1` (structural, chapter-scope), `evidence_book: asos`, `evidence_chapter: asos-catelyn-07`. Per the Contract-6 exemption established in Step 4 C-1, `evidence_quote` is not required for SUB_BEAT_OF structural edges — use the `plate5_evidence_note` field with value: `"SUB_BEAT_OF structural classification; no verbatim book quote — see rationale field"` and set `rationale` to the beat's description.

Verify each beat node exists in `graph/nodes/events/` before emitting the SUB_BEAT_OF edge. If a beat slug does not exist, stop and report — do not mint the event node without Matt's input.

---

## Step 6 — LOCATED_AT direction: reconcile the design doc

**Do NOT flip any data.** The canonical live direction is `event → location` (source_slug = event, target_slug = location). This is the correct convention and the live data is right.

The task here is to reconcile documentation:
1. Read `working/edge-modeling/edge-modeling-reification-design.md` (the design doc) and `reference/architecture.md` (the live reference)
2. If either says LOCATED_AT should have `location → event` direction (inverse of live data), add a dated correction note in that file: *"CORRECTION 2026-06-12: Live data uses event→location direction (source=event, target=location). This supersedes any earlier statement of the inverse convention."*
3. Do not rewrite the whole section — a single clearly-dated correction note is sufficient

---

## Step 7 — Rebuild indexes

After all graph writes are complete:

```bash
# Rebuild entity indexes
python3 scripts/build-entity-indexes.py --all

# Rebuild event-alias-lookup (needed after A1 moves the-conquest-of-dorne out of events/)
python3 scripts/event_alias_resolver.py --rebuild
```

---

## Step 8 — Verification

Run in order; stop on any mismatch:

**8a. Health check:**
```bash
python3 scripts/graph-query.py --health
```
Note: 63 deliberately-left orphan slugs are expected (documented in `working/infobox-merge/spec.md` §5). Any orphan beyond that list is a defect — report to Matt.

**8b. Row-count delta check:**
```bash
python3 -c "
import json
rows = [json.loads(l) for l in open('graph/edges/edges.jsonl')]
print(f'Total rows: {len(rows)}')
from collections import Counter
by_kind = Counter(r.get('evidence_kind','UNKNOWN') for r in rows)
for k, n in by_kind.most_common():
    print(f'  {k}: {n}')
"
```
Expected delta from this session: +~30–45 rows (adds) + drops/retypes net negative. The exact count depends on which items Matt approved.

**8c. Red Wedding beat-union includes Dacey Mormont's death:**
```bash
python3 -c "
import json
rows = [json.loads(l) for l in open('graph/edges/edges.jsonl')]
rw = [r['source_slug'] for r in rows if r.get('target_slug')=='red-wedding' and r.get('edge_type')=='SUB_BEAT_OF']
print('Red Wedding beats:', rw)
dacey = any('dacey' in s for s in rw)
print('Dacey Mormont beat present:', dacey)
"
```

**8d. joffrey-dies hub is present and has olenna-tyrell as AGENT_IN:**
```bash
python3 scripts/graph-query.py --neighbors death-of-joffrey-baratheon 2>/dev/null || echo "Node not found"
```

**8e. False-confession edge is now tier 4 (not tier 1):**
```bash
python3 -c "
import json
rows = [json.loads(l) for l in open('graph/edges/edges.jsonl')]
fc = [r for r in rows if r.get('source_slug')=='tyrion-lannister' and r.get('edge_type')=='POISONS' and r.get('target_slug')=='joffrey-baratheon']
for r in fc:
    print('confidence_tier:', r.get('confidence_tier'), '| asserted_relation:', r.get('asserted_relation',''))
"
```

**8f. Spot-check 5 touched edges** — pick one each from F1c repair, F6 dyads, B reverse edge, F2 retype, and F3a hub. Confirm edge fields are well-formed (no missing required fields, slug resolution correct).

**8g. Full test suite:**
```bash
python3 -m pytest scripts/ -v --tb=short 2>&1 | tail -30
```
Pre-existing failures expected: `test_vocab_count_is_163` ×2 (vocab is now 166) + `test_cwd_is_tmp`. All other tests must be green.

---

## Step 9 — Update project state

**9a. Mark curation file items EXECUTED:**
In both `curation/hub-review-triage-2026-06-12.md` and `curation/plate5-small-followups-2026-06-12.md`, add `[EXECUTED 2026-06-12]` next to each FIX / followup item that was applied in this session. Items that were skipped (Matt rejected or left QUARANTINE) remain unmarked.

**9b. Update `working/todos.md` Track 3:**
- Mark these items done:
  - "NEW S92 — Graph defect: F1c dangling edge"
  - "NEW S92 — Graph defect: 3 Red Wedding beats missing SUB_BEAT_OF"
  - "NEW S92 — Graph defect: robb-is-killed SUB_BEAT_OF red-wedding mis-sourced quote"
  - "NEW S92 — Graph defect: donal-noye KILLS mag quote mismatch" (if B-2 was executed)
  - "NEW S92 — Graph defect: LOCATED_AT direction doc reconcile"
  - "NEW S92 — Hub-triage FIX-22 list is ready to execute"
  - "POST-PLATE-5 followup #2 — 32 SUB_BEAT_OF empty-quote disposition" (if C-1 was executed)
  - "POST-PLATE-5 followup #3 — 109 hub-review-queue triage" (FIX bucket executed; QUARANTINE deferred)
  - "POST-PLATE-5 followup #4 — 2 deferred collision merges" (if A1 + A2 executed)
  - "POST-PLATE-5 followup #5 — donal-noye↔mag mutual-kill reverse direction" (if B-1 executed)

**9c. Update `worklog.md`:**
Add a session entry covering: what was executed, row-count delta, any items skipped/deferred, new state of the Red Wedding beat-union. Keep to ≤30 lines per the worklog lean rule.

---

## Hard rules

- **No writes to `sources/` — ever, regardless.**
- **STOP on any verification mismatch** in Step 8. Report to Matt before proceeding.
- **QUARANTINE items are NOT executed.** The 10 quarantine items wait on Matt's decision or new evidence. Do not apply them.
- **F3a and F5 execute together** — do not retier the false-confession edge (F5) without first minting the `death-of-joffrey-baratheon` hub (F3a), or the graph will briefly have no tier-1 Joffrey-death signal at all.
- **LOCATED_AT data is correct — doc only.** Do not flip any edges in Step 6.
- **Do not mint event nodes for missing Red Wedding beats without confirming the slug exists.** If a slug is absent from `graph/nodes/events/`, stop and report.
