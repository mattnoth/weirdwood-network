# Pass 1 Mechanical Extraction — Resume AFFC, then ACOK / ASOS / ADWD

> **Continue prompt for a fresh session.** Self-contained — pick this up without prior conversation context.
>
> **Drafted:** 2026-05-01 mid-Session 30. AFFC partially complete (16/46 — waves 1, 4, 7, 10) after a `weirwood stop` issued near a usage-limit boundary. User session limit has reset. Resume AFFC, finish the remaining 4 books.

---

## Why this work, why now

Continuation of the Pass 1 mechanical extraction track. Original continue prompt: `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md` (still authoritative for everything below — read it for hard rules, launch-option rationale, per-book acceptance criteria, canary checks). This prompt is the **resume-after-stop** delta.

Pass 1 completion gates Stage 4 v1 prose-edge classification, Pass 3 voice/perception, Pass 4 foreshadowing, Pass 5 theory extraction, and the trigger table / index build.

---

## State at session start (verify before doing anything)

```bash
# Confirm HEAD
git log --oneline -3

# Verify Pass 1 progress per book
for d in extractions/mechanical/*/; do
  b=$(basename "$d")
  [[ "$b" == "status" ]] && continue   # stale empty dir, ignore
  done=$(ls "$d"/*.extraction.md 2>/dev/null | wc -l | tr -d ' ')
  total=$(ls sources/chapters/"$b"/*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "  $b: $done/$total"
done
# Expected:
#   agot:  73/73
#   acok:   0/70
#   asos:   0/82
#   affc:  16/46   ← waves 1, 4, 7, 10 done; waves 2, 3, 5, 6, 8, 9 remain
#   adwd:   0/73

# Confirm stop file is gone (auto-cleared on next launch, but verify)
ls -la /tmp/extraction-stop 2>/dev/null && echo "STOP FILE STILL PRESENT — clear before launching" || echo "no stop file (good)"

# Spot-check for half-written extractions (zero-byte or truncated files)
find extractions/mechanical/affc -name "*.extraction.md" -size -5k -exec ls -la {} \;
# Empty output = good. Any hits = inspect; weirwood detects "incomplete" by file
# presence only, so a half-written file will be SKIPPED on resume. Delete partials
# manually before relaunching.
```

**If any half-written `.extraction.md` exists in `extractions/mechanical/affc/`** (size < 5 KB or missing the closing sections):
1. Delete the offending file
2. Resume — `weirwood` re-discovers the chapter as incomplete and re-runs it

---

## First action: verify and report

Run the state-check commands above. Report to Matt:
- HEAD commit
- AFFC progress (should be 16/46)
- Whether any partial files exist (should be none if `weirwood stop` halted at a wave boundary as designed — but verify)
- Any unexpected state

**Do NOT auto-launch.** Confirm with Matt before firing the next `weirwood` invocation.

---

## Resume plan

### Step 1 — finish AFFC

6 waves remain (2, 3, 5, 6, 8, 9) = 30 chapters. At 4 terminals × 3 waves = 12 wave-slots, that's plenty of capacity for one batch. But the 6 waves are non-contiguous, and `weirwood <book> <terminals> <waves>` distributes the **next N incomplete waves** across the terminal pool — it doesn't care about contiguity.

**Recommended:** `weirwood affc 4 2` — 4 terminals × 2 waves = 8 wave-slots, will pick up the 6 remaining incomplete waves (waves 2, 3, 5, 6, 8, 9) and distribute them across 4 terminals (likely 2+2+1+1). Wall-clock ~50 min at ~25 min/wave.

Alternative: `weirwood affc 4 3` (12 wave-slots; over-provisioned, identical result; tail terminals get fewer waves).

Confirm sizing + who launches with Matt before firing.

### Step 2 — AFFC quality check (canary)

Once AFFC reaches 46/46:

```bash
# Pick 5 random extractions
ls extractions/mechanical/affc/*.extraction.md | gshuf -n 5 2>/dev/null || \
  ls extractions/mechanical/affc/*.extraction.md | sort -R | head -5
```

For each sampled file, verify:
- All 12 Raw Entity List categories present (Characters, Locations, Houses, Factions, Religions, Cultures, Artifacts, Texts, Magic, Wars, Titles, Other) — "None" for empty categories, never elided
- Top-level v3 sections all present: Physical Environment, Characters Present, Character Appearances, Characters Referenced, Locations, Location Descriptions, Artifacts, Food & Drink, Hospitality & Guest Right, Events & Actions, Spatial Layout & Movement, Information Revealed, Dialogue of Note, POV Character's Internal State, Relationships Observed, Unanswered Questions
- File size sanity: ~30-50 KB per extraction (AGOT v3 baseline)
- No truncation / no `_FAILED` markers

If quality is good → proceed to ACOK. If drift detected → surface to Matt before scaling.

### Step 3 — ACOK / ASOS / ADWD

Per the original continue prompt's Option B (chained): `weirwood acok --chain 4` etc. ~3-3.5 hrs each. Plan to checkpoint at book boundaries (each book is ~one usage window).

Per-book commit cadence (Matt-decided Session 30 launch).

### Step 4 — Final verification + handoff

Once 344/344 across all 5 books:
- Confirm `working/extraction-stats/extraction-stats-{book}-pass1-v3.csv` populated for each
- Update `worklog.md` Current State checklist (4 per-book lines already exist; tick remaining)
- New Session N entry with totals, cost, duration
- Hand off to Stage 4 v1: `progress/continue-prompts/2026-05-02-stage4-v1-prose-edge-classifier.md`

---

## Hard constraints (carry-forward, non-negotiable)

- **NEVER auto-launch agent runs without confirming each batch with Matt.**
- **NEVER run `/endsession` without explicit permission.**
- **NEVER commit copyrighted source content.** `sources/raw/` and `sources/chapters/` are gitignored and stay that way. Extractions in `extractions/mechanical/` ARE committed.
- **Extraction goes through the `weirwood` pipeline in iTerm, not background subagents.** Hard memory rule. Do NOT spawn `mechanical-extractor` agents.
- **`first_available` deferred** — agent prompts already updated; do not re-introduce.
- **Don't modify the v3 prompt mid-run.** If a quality issue surfaces, stop, fix, archive partials to `extractions/archives/<book>-v3-partial/`, restart cleanly.

---

## Known cosmetic issues (do NOT fix mid-run)

- **`scripts/extract.sh:484` per-chapter summary shows `0 events / 0 relationships`** — stale counter regex (`grep -c "^\*\*.*\*\*"`) targets v2 bolded-row format, not v3 tables. Extractions themselves are healthy. Patch as a one-liner AFTER all extractions complete (don't disturb a running pipeline).
- **Terminal name reverts from `claude` to `-zsh` on early-finishing tabs.** Expected behavior — `claude` exits, tab name reverts. Not a failure indicator.

---

## Files / commands reference

**Launcher:**
- `scripts/weirwood.zsh` — entry point: `weirwood <book> <terminals> <waves>` or `weirwood <book> --chain <terminals>`
- `scripts/launch-extraction.sh` — iTerm tab launcher
- `scripts/run-extraction-wave.sh` — per-wave executor
- `scripts/extract.sh` — status / launch dispatcher; **already has graceful rate-limit detection** (lines 478-535: detects `"status":"rejected"` + `"rateLimitType"`, breaks wave cleanly, marks remaining chapters as `skip-rate-limit` in stats)

**Soft-stop:**
- `weirwood stop` (touches `/tmp/extraction-stop`) — halts at next **wave boundary**, not chapter boundary. Each terminal finishes its current wave's remaining chapters before bailing. Auto-cleared on next launch.

**Outputs:**
- `extractions/mechanical/{book}/` — per-chapter `.extraction.md` files
- `working/extraction-stats/extraction-stats-{book}-pass1-v3.csv` — token + timing stats

**Reference:**
- Original continue prompt (still authoritative): `progress/continue-prompts/2026-05-02-pass1-mechanical-remaining-books.md`
- v3 prompt: `.claude/agents/mechanical-extractor.md`
- AGOT v3 baseline for quality comparison: `extractions/mechanical/agot/`
- Architecture: `reference/architecture.md`

---

## Open questions for Matt at session start

1. AFFC resume sizing: `weirwood affc 4 2` (recommended, exactly covers 6 remaining waves) or `weirwood affc 4 3` (over-provisioned, same result)?
2. Who launches: Matt in iTerm, or orchestrator via `! weirwood ...` from this session?
3. Per-book commit cadence confirmed Session 30 launch — proceed with per-book commits.
