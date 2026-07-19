# SESSION DE-3 — Dunk & Egg Pass-1 v4 SMOKE: judge THK output, then promote or iterate

> **This is the Dunk & Egg track** (Pass-1 extraction of the THK/TSS/TMK novellas). It is
> **parallel-safe** with the graph-enrichment track — they touch different files and run in different windows.
> **Track state file:** this track logs to its OWN worklog → **`worklog-dunk-egg.md`** (read it for the D&E
> Current State; `worklog.md` holds the shared Active Decisions / Principles).
> **Session number:** stamp your entry **`### Session DE-3`** in **`worklog-dunk-egg.md`**, NOT `worklog.md`
> — independent of the global S-number, no cross-track write-order race.
>
> **STATE (after DE-1):** queue **already built** (`queue.jsonl`, 3 units; canonical dirs exist). The v4/THK
> smoke was **attempted DE-1 but hit a 401 auth wall** — a nested `claude -p` cannot authenticate from inside
> a Claude Code session (host-managed OAuth not inherited by a child; confirmed with/without
> `ANTHROPIC_BASE_URL`). **The smoke runs from a logged-in interactive CLI/iTerm only.** Matt was running it
> himself via the `claude` CLI at DE-1 close — so `smoke/v4/thk-dunk-01.extraction.md` may already exist
> (check first; judge if so).
>
> **Recommended model:** Opus 4.8 (you are judging prompt quality + deciding whether to promote/iterate v4
> — design-adjacent judgment). NOTE: the extraction itself runs on Opus regardless — the worker hardcodes
> `claude-opus-4-8` (`project_pass1_all_opus`). The judge subagent can be Haiku (cheap).

## Where this track stands (design DONE in the prior session)
The unattended D&E harness is designed and scaffolded; the v4 prompt is hardened. Everything is under
`working/dunk-egg-pass1/`:
- `run-plan.md` — harness contract, worker config, split decision, run/monitor/resume, fire-checklist.
- `prompts/pass1-prompt-v4.md` — the hardened, versioned prompt (read its appendix change-table rows
  1–15: self-contained rules, harvest+capture pointers, in-text identity→`SAME_AS`, "more room"
  checkpointing, banned interpretive-qualifier leak, **LOCKED relationship vocab** + `NEEDS_VOCAB` hatch
  + required/optional qualifier capture + forward-direction-only + Events→reification-roles +
  `causal-spine` harvest breadcrumb).
- `dunk-egg-pass1-extraction.py` — the worker SCAFFOLD (proven `claude -p` loop; `--smoke`/`--prompt-version`
  aware; runs fine from `working/`, writes smoke output to `smoke/<version>/` — never the canonical tree).

## Goal of THIS session
**Smoke-test v4 on ONE unit (THK), judge the output cold, then either promote v4 to the full run or
iterate to v4b.** This is the first time v4 meets real text — the point is to find where the locked vocab
/ deepened qualifiers / isolation rules actually strain.

## THE GATE (read before doing anything)
A smoke run is a **live `claude -p` extraction**. Per `feedback_no_extraction_without_asking`, get Matt's
**explicit go** before firing it. Do not launch on your own initiative.

## Sequence
1. **Get the THK v4 smoke output.** First check whether it already exists:
   `ls -la working/dunk-egg-pass1/smoke/v4/thk-dunk-01.extraction.md`
   - **Exists** (Matt ran it via CLI) → skip to step 2 (judge).
   - **Missing** → it must run from a **logged-in interactive CLI/iTerm** (a nested `claude -p` from inside a
     Claude Code session 401s — DE-1 finding). Queue is already built, so the command is just:
     ```
     python3 working/dunk-egg-pass1/dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4
     ```
     ~20–35 min on Opus. Output → `smoke/v4/thk-dunk-01.extraction.md`; stream log → `logs/v4-thk.json`;
     telemetry `prompt_version=v4 mode=smoke`. **Do NOT fire it via the Bash tool / a background subagent**
     (auth wall + `feedback_no_extraction_without_asking`). In-session alternative = an Agent-tool subagent
     proxy (authenticated) — offer as an explicit override, don't default to it.
2. **Fresh-judge the output (a separate `extraction-quality-auditor` subagent, Haiku ok).** PASTE the
   vocab line into its prompt (below — subagents don't load CLAUDE.md). Have it check, against
   `working/dunk-egg-pass1/smoke/v4/thk-dunk-01.extraction.md` + the THK source:
   - **Locked vocab held?** Every `## Relationships Observed` Relationship cell is one controlled
     UPPER_CASE type (or a `NEEDS_VOCAB:` flag) — no free-text pseudo-labels (`implicit_hostility`).
   - **Qualifiers captured?** Required ones present (`SIBLING_OF (half)` etc.); optional ones
     (`KILLS (by_ambush)`, `DECEIVES (by_disguise)`) captured where text-evident.
   - **Forward-only?** No inverse/mirror rows; Column A is the semantic agent (Head rule).
   - **Isolation clean?** No cross-unit / reader-knowledge leakage; no analytical types (`FORESHADOWS`).
   - **No interpretive-qualifier leak** (`symbolic`/`ironic`/`(implicit)`) in cells or the Raw Entity List.
   - **Identity reveals → `SAME_AS`** (Egg→Aegon, the old man→Ser Arlan) captured.
   - **Harvest sidecar** (`harvest-dunk-egg.jsonl`) accumulated generic saga-important breadcrumbs
     (Targaryen history, prophecy, food, hospitality, cross-identity, `causal-spine`) — NO entity
     pre-flagging (the v4 de-bias, S132b).
   - **Completeness** — late tables not skimped (the long-generation failure mode); all 12 Raw-List headers.
   Report a SUMMARY to Matt (not an edge-list — `feedback_subagent_verify_not_matt`).
3. **Decide with Matt:**
   - **Promote** → v4 is the winner. Pin `--prompt-version v4` in the weirwood `TRACK_CMD` and proceed to
     the full-run prereqs in `run-plan.md` §6 (graduate worker to `scripts/`, register the track, settle
     the split A/B decision, correct `architecture.md:161` per the Active Decision).
   - **Iterate** → copy `prompts/pass1-prompt-v4.md` → `prompts/pass1-prompt-v4b.md`, change ONE axis to
     fix what strained, smoke v4b on THK, diff `smoke/v4/` vs `smoke/v4b/`. Repeat until a winner.

## Vocabulary (PASTE into the judge subagent — it does not load CLAUDE.md)
Pass = numbered corpus sweep · Track = named workstream · lowercase step = ordered piece · Tier =
confidence 1–5 ONLY. No new capitalized terms.

## DO NOT
Fire any extraction (incl. smoke) without Matt's explicit go (`feedback_no_extraction_without_asking`) ·
write extractions to archive folders (canonical `extractions/mechanical/{thk,tss,tmk}/` only; smoke writes
to `smoke/` scratch) · refetch wiki · edit `architecture.md:161` until v4 is the approved winner (it's the
paired change at promote-time, not now) · `/endsession` without explicit permission.
