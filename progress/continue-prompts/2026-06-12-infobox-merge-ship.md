# Continue Prompt: Infobox Merge — Ship

**Status:** LIVE
**Recommended model:** Sonnet 4.6 (deterministic apply + verification; the 11 open-question judgments are Matt's, made before launch)
**Created:** 2026-06-12 (Session 92)

---

## Context

The infobox-structural wiki merge was greenlit by Matt on 2026-06-11. All pre-ship work is done as of S92:

- **Spec v2:** `working/infobox-merge/spec.md` — adversarial critic confirmed the FIELD_EDGE_MAP direction-inversion on 10 fields; fact-key quarantine closes the Joffrey-mirror leak (Jon Snow's two listed "Mothers" quarantined, does NOT mint false PARENT_OF edges).
- **Script + tests:** `scripts/infobox-merge.py` — 75 tests green. Supports `--dry-run` (default) and `--apply --yes-i-reviewed-the-dry-run`. Auto-backs-up to `graph/edges/_regrounding/` before any write.
- **Dry-run report:** `working/infobox-merge/dry-run-report-2026-06-12.md` — reproduces spec v2 EXACTLY. Expected counts:
  - 20,614 in → **17,006 merged** / 1,128 filtered / 1,037 quarantined / 1,356 deduped / 87 corroborations
  - `edges.jsonl` would go **4,760 → 21,766** (17,006 new edges)
  - Node connectivity **14.7% → 71.0%**
  - Hygiene fixes folded in: 115 orphan endpoint slugs remapped + 948 role edges backfilled with `typed_by` + `evidence_ref`
- **Nothing has touched `graph/` yet.** No graph writes in S92.

---

## Step 0 — Matt does this before launch

Review `working/infobox-merge/dry-run-report-2026-06-12.md`. The report includes:

- An **expected-vs-actual count table** (all counts matched on the dry-run; re-run will re-verify)
- A **20-edge seeded sample** for spot-check
- **2 semantic-remap flags** requiring Matt's explicit OK:
  - `lady-stoneheart` → does this map to `catelyn-stark` for infobox edges? (She IS Catelyn, post-resurrection)
  - `abel` → does this map to `mance-rayder` for infobox edges? (Abel is Mance's disguise in ADWD)
- **11 YOUR-DECISIONS items** (decided-by-default in the dry-run; Matt's override wins):
  - Review each item in the report's YOUR-DECISIONS section
  - Record your overrides directly in the report file (or leave blank = accept the default)

**Do not launch Step 1 until Matt has reviewed the report and recorded any overrides.**

---

## Step 1 — Re-run dry-run to confirm no drift

```bash
cd /Users/mnoth/source/asoiaf-chat
python3 scripts/infobox-merge.py --dry-run
```

Expected counts must still match the report. Guards against any interim graph changes (e.g., the hub-triage FIX-22 list, if applied before this lands). If counts deviate, STOP and report to Matt — do not force.

---

## Step 2 — Apply

```bash
python3 scripts/infobox-merge.py --apply --yes-i-reviewed-the-dry-run
```

The script auto-backs-up canonical `edges.jsonl` to `graph/edges/_regrounding/` before writing. Expected result:
- `graph/edges/edges.jsonl` grows from 4,760 → **21,766 rows**
- Hygiene fixes applied in-place (115 orphan slug remaps + 948 `typed_by`/`evidence_ref` backfills)

---

## Step 3 — Verification

Run in order; stop if any check fails:

**3a. Health check (0 orphans target):**
```bash
python3 scripts/graph-query.py --health
```
Note: spec §5 documents 63 deliberately-left orphan slugs (non-graph-node wiki pages intentionally included as edge endpoints — they are expected and OK). If `--health` flags any, cross-check against spec §5's list before treating as a defect.

**3b. Row count check:**
```bash
python3 -c "
import json
rows = [json.loads(l) for l in open('graph/edges/edges.jsonl')]
print(f'Total rows: {len(rows)}')
print(f'Wiki-infobox: {sum(1 for r in rows if r.get(\"evidence_kind\")==\"wiki-infobox\")}')
"
```
Expected: ~21,766 total; ~17,006 `evidence_kind: wiki-infobox`.

**3c. Spot checks (10 probes):**
```bash
# 1. Walder Frey children present
python3 scripts/graph-query.py --neighbors walder-frey | grep -i "parent_of\|child_of" | head -20

# 2. Jon Snow — NO new PARENT_OF from quarantined Mothers field
python3 scripts/graph-query.py --neighbors jon-snow | grep -i "parent_of" | head -10

# 3. SWORN_TO house chains traverse
python3 scripts/graph-query.py --path jon-snow house-stark --max-hops 3

# 4. Lady Stoneheart / Catelyn (per Matt's semantic-remap decision)
python3 scripts/graph-query.py --neighbors catelyn-stark | head -20

# 5. Mance Rayder / Abel (per Matt's semantic-remap decision)
python3 scripts/graph-query.py --neighbors mance-rayder | head -20

# 6. Spot-check a PARENT_OF edge (should have evidence_kind=wiki-infobox)
python3 -c "
import json
rows = [r for r in (json.loads(l) for l in open('graph/edges/edges.jsonl'))
        if r.get('type')=='PARENT_OF' and r.get('evidence_kind')=='wiki-infobox']
print(f'PARENT_OF wiki-infobox count: {len(rows)}')
if rows: print(json.dumps(rows[0], indent=2))
"

# 7. Confirm typed_by backfill landed on reified role edges
python3 -c "
import json
missing = [r for r in (json.loads(l) for l in open('graph/edges/edges.jsonl'))
           if r.get('evidence_kind')=='book-pass1-reified' and not r.get('typed_by')]
print(f'Reified role edges still missing typed_by: {len(missing)} (target: 0)')
"

# 8–10: Run edge type distribution for sanity
python3 -c "
import json
from collections import Counter
rows = [json.loads(l) for l in open('graph/edges/edges.jsonl')]
c = Counter(r.get('type','UNKNOWN') for r in rows)
for t, n in c.most_common(15):
    print(f'{t}: {n}')
"
```

**3d. Rebuild entity indexes:**
```bash
python3 scripts/build-entity-indexes.py --all
```

**3e. Rebuild event-alias-lookup if needed:**
```bash
python3 scripts/event_alias_resolver.py --rebuild
```

**3f. Full test suite:**
```bash
python3 -m pytest scripts/ -v --tb=short 2>&1 | tail -30
```
Pre-existing failures to expect (predate this session, not introduced by merge): `test_vocab_count_is_163` ×2 (vocab is now 166) + `test_cwd_is_tmp`. All other tests should be green.

---

## Step 4 — Update project state

**4a. Update worklog.md STATUS block:**
- Connectivity: 14.7% → **71.0%**
- Edge count: 4,760 → **21,766**

**4b. Update todos.md Track 1:**
- Mark the "Ship" item DONE
- Track 1 is now fully complete

**4c. Unblock the Mode 3 dip:**
- The Mode 3 continue prompt at `progress/continue-prompts/2026-06-11-phase2-mode3-dip.md` references "after the infobox merge lands" as its gate. That gate is now open. Add a note to that prompt or to todos Track 2 that the gate is cleared.

---

## Hard rules

- Backup before write (script handles this automatically via `graph/edges/_regrounding/`)
- No writes to `sources/` (never, regardless)
- If any count in Step 1 deviates from the dry-run report, STOP and report to Matt — do not force
- If `--health` returns unexpected orphans beyond the 63 documented in spec §5, STOP and report
- Do not proceed past Step 1 if Matt has not completed Step 0
