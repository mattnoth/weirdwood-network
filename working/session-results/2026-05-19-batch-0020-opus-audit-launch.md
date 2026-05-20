# batch-0020 Opus Audit — Launch Info

**Launched:** 2026-05-19 (Session 58 continued)
**Launched by:** Opus 4.7 orchestrator → spawned to fresh iTerm2 window
**Worker model:** Opus 4.7 (claude-opus-4-7)
**Run mode:** **fresh iTerm2 window** (not background subagent)

---

## What was launched

Opus diagnostic audit of batch-0020 prose-edge classifier output. batch-0020 is the hot zone surfaced by STEP 4's suspicious-edges flagger: 153 flagged of 437 emits (35% flag rate); 140 of 163 KNOWS-as-fallback flags project-wide.

## Why a fresh terminal

Audit will consume substantial Opus tokens (full file reads + sample analysis of 50 emits + wiki page context). Running it in this orchestrator session would balloon context. Fresh iTerm2 window isolates the work.

## Spawn method

iTerm2 window opened via osascript. Initial command:
```bash
cd /Users/mnoth/source/asoiaf-chat && claude --model claude-opus-4-7 -p "$(cat progress/continue-prompts/2026-05-19-batch-0020-opus-audit.md)"
```

## Expected output

- `working/session-results/2026-05-19-batch-0020-opus-audit.md` — the audit doc

## Verification post-completion

1. Confirm audit doc exists with 5 expected sections
2. Read the Haiku smoke readiness verdict (Section 5)
3. If verdict is "ready" → STEP 5 unblocks
4. If verdict is "needs prompt change first" → encode the recommended changes (mechanical Sonnet 4.6 task), then STEP 5

## Cost estimate

~$10-25 Opus for full audit. Includes corpus read of batch-0020's ~437 emits, 50 sampled evidence-snippets, surrounding wiki context, classifier prompt re-read, recommendation generation.
