# Plate 3 Full Corpus — Summary

**Run date:** 2026-06-07
**Script:** `scripts/edge-reify-backfill.py --all`
**Model:** claude-sonnet-4-6
**DryRun:** False
**Resume:** True

---

## Coverage

| Item | Count |
|------|-------|
| Chapters scanned | 344 |
| Trigger events found | 628 |
| Unique hub groups | 413 |
| Skipped by ledger (--resume) | 404 |
| Events attempted this run | 9 |

## Disposition

| Item | Count |
|------|-------|
| Reified (n-ary) | 7 |
| Skipped (clean dyad) | 1 |
| Borderline → review queue | 1 |
| Errors | 0 |

## Hub Resolution

| Item | Count |
|------|-------|
| Hubs reused | 0 |
| Hubs minted | 7 |
| Hubs queued for review | 0 |

## Role Edges

| Edge Type | Count |
|-----------|-------|
| AGENT_IN | 9 |
| COMMANDS_IN | 7 |
| LOCATED_AT | 2 |
| VICTIM_IN | 7 |
| **Total** | **25** |

## Contract 10

**ALL PASSED** — all AGENT_IN/VICTIM_IN targets resolve to event.*

## Cost

| Item | Value |
|------|-------|
| Total LLM cost | $0.5661 |
| Events reified | 7 |
| Avg cost/event | $0.0809 |

## Output Files

- `/Users/mnoth/source/asoiaf-chat/working/edge-modeling/plate3-full/role-edges-staging.jsonl`
- `/Users/mnoth/source/asoiaf-chat/working/edge-modeling/plate3-full/skipped-clean-dyads.jsonl`
- `/Users/mnoth/source/asoiaf-chat/working/edge-modeling/plate3-full/hub-review-queue.jsonl`
- `/Users/mnoth/source/asoiaf-chat/working/edge-modeling/plate3-full/supersede-candidates.jsonl`
- `/Users/mnoth/source/asoiaf-chat/working/edge-modeling/plate3-full/processed-events.jsonl`
- `/Users/mnoth/source/asoiaf-chat/working/edge-modeling/plate3-full/minted-event-nodes`
