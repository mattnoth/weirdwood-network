# S186 follow-up — production logging fixes + Opus cutover + deploy doc

**For the S186 usage-logging agent: fold the below into your S186 worklog entry
(and the shared Active Decisions block in `worklog.md`) at endsession.** This work
was done in a separate window on top of your logging track — all on `chat.ts` and
docs, already committed + pushed + DEPLOYED to production. Reconcile with your own
`chat.ts` edits (we both touched it; a concurrent linter added the `persona` field,
which is already merged in what's live).

## What was done (worklog-entry bullets)

- **Closed two usage-logging blind spots** in `web/netlify/edge-functions/chat.ts`:
  the cost-cap early-return and the api-error `catch` now log via a new `failedTurn()`
  helper (`stopState` = `cost-cap-tripped` / `api-error`, zero usage). Previously a
  cap trip logged nothing and an api-error was a bare `console.error` — both invisible.
- **Fixed the empty-`question` bug** (every real turn was logging `question: ""`):
  `runAgent` mutates the `messages` array in place (appends the assistant turn +
  a `role:"user"` tool_result turn with no text block — agent.ts:410/438), so a
  post-loop `lastUserText()` read the tool_result turn and returned `""`. Fix: capture
  `const question = lastUserText(messages)` once right after parse, reuse in all three
  `logTurn` sites. **Verified in prod** — a live turn now logs the real question text.
- **Production model flipped Sonnet → Opus.** `WEIRWOOD_MODEL` was set to
  `claude-sonnet-4-6` in Netlify's production context, silently overriding chat.ts's
  Opus code default. Set `WEIRWOOD_MODEL=claude-opus-4-8` (production context) +
  redeployed. Verified: live log records now stamp `model: claude-opus-4-8`.
- **Raised the daily spend cap $5 → $50** (`DAILY_SPEND_CAP_USD` in chat.ts) as an
  Opus backstop (Opus is 5×/25× Sonnet pricing on a public URL).
- **Discovered the site has NO git continuous deployment** (`repo_url` unset) —
  `git push` ships nothing; prod is a manual `netlify deploy --prod --build` from the
  repo root (the `--build` regenerates the ~8.8 MB `web/data/` bundle). Shipped via
  two manual deploys this session.
- **Created `DEPLOY.md`** (repo top level) — deploy procedure + gotchas + cost/usage
  log guide — and a Claude-memory pointer (`project_deploy_procedure.md` + MEMORY.md
  line) so future deploy work reads it first.

## For Active Decisions (shared, `worklog.md`)

- **Chat-UI production model = Opus (`claude-opus-4-8`)** as of 2026-07-04 (S186),
  set via the `WEIRWOOD_MODEL` Netlify env var. This is a **deliberate exception to the
  default-to-cheapest-model rule** — Matt asked for Opus on the portfolio demo; do not
  "correct" it back to Sonnet. Local dev stays Sonnet (`web/scripts/dev.ts`).
- **Daily spend cap = $50/day** (`DAILY_SPEND_CAP_USD`, chat.ts). Load-bearing cost
  control on the public URL.
- **Deploys are manual, not git-triggered.** Canonical procedure lives in `DEPLOY.md`.

## Commits (all on `main`, pushed, live)

- `0ed1c16e0e` — log cost-cap + api-error turns; raise daily cap 5→50 for Opus
- `8516b83cd4` — fix empty question in logs (capture before runAgent mutates messages)
- `f529f02590` — add DEPLOY.md

## Notes / caveats

- **Historical logs before `8516b83cd4` have blank `question`** — not backfillable
  (only the output was stored, not the request). All turns from the fix onward capture it.
- Verification spend this session ≈ **$0.06** (a few live Opus turns).
- **Offered but NOT built:** an aggregate cost-rollup tool (`cost-report.ts`) that sums
  `costUsd` / the `spend-*` counters over a date range. `read-logs.ts` is per-turn only.
  Matt hasn't said go — leave as a backlog item unless he asks.
