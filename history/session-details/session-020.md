# Session 20 — Wiki Pass 2 Smoke-Debug Fix + First-Bucket Smoke Test (2026-04-26)

## Frame

Session 19 ended with the silent-exit bug surfaced in `weirwood wiki run` and a continue prompt authorizing autonomous debug-and-fix in a separate Claude session. Matt was away for several hours. This session is the resumption: reviewing the autonomous session's work mid-flight, watching the smoke test execute end-to-end, and discovering on close inspection that the smoke run masks a real upstream bug — but the agent's structured-question discipline caught it transparently.

## Session shape

Two terminals, one orchestration. The autonomous Claude session in iTerm did the silent-exit debug; this session (a separate terminal Claude) was the orchestrator Matt was in to monitor. The orchestrator session sanity-checked the running smoke test, then did the end-of-session writeup after Matt closed the autonomous terminal.

## What the autonomous session did (Session 19's work, completed in Session 20's window)

### Silent-exit bug — root-cause + fix

The autonomous session reproduced the silent-exit under `bash -x` and isolated it precisely:

`scripts/wiki-pass2.sh:286` — final line of `run_orphan_recovery`:

```sh
(( recovered > 0 )) && echo "Orphan recovery: ${recovered} bucket(s) reset to pending"
```

On a clean run, `recovered=0`, the arithmetic test returns 1, the `&&` short-circuits, the function's last command returns 1, and `set -e` terminates the script silently. The `if`-wrapped equivalent in `run_reconciliation` doesn't have this problem because `if (( ... )); then ... fi` always returns 0 when the condition is false.

Fix: replace `&& echo` with `if (( recovered > 0 )); then echo ...; fi`. Comment captures the trap so it doesn't reappear in future edits. Not a `|| true` symptom suppression — the function's contract is "return 0 unless something actually went wrong."

The autonomous session verified the fix by inserting a `WIKI_PASS2_SMOKE_ABORT=1` sentinel just before the `claude -p` invocation, running the launcher to confirm it now reaches bundle composition, then removing the sentinel cleanly. Bundle written: 6 direwolves, all `raw_html_path` resolved to real cache files, all `track_b_row` populated. Manifest reset to `pending`.

Documented in `working/runbooks/wiki-pass2-orchestration-build-self-review.md` § "Smoke-debug fix (2026-04-26, post-Session-19)". Sibling concern flagged: other helpers in `wiki-pass2.sh` may end on similar `&&`-chain or `(( ... ))` patterns; not fixed speculatively.

### Smoke run — end-to-end

Matt gave the green light. `weirwood wiki run core --bucket direwolves` ran cleanly:

- Wall time: 4m 47s
- Cost: $1.15
- Tokens: 19 in / 69k cache-create / 783k cache-read / 13k out
- Validator: 6/6 PASS
- Coherence (`weirwood wiki check`): 0 issues
- 6 nodes promoted: `ghost.node.md`, `grey-wind.node.md`, `lady.node.md`, `nymeria-direwolf.node.md`, `shaggydog.node.md`, `summer.node.md`
- `tmp/` empty, manifest complete (`nodes_promoted: 6`)
- Stats CSV updated: `working/extraction-stats/wiki-pass2-stats-core-v1.csv`

Hand-inspection of `ghost.node.md` and `grey-wind.node.md`: type override (`character.human` → `character.direwolf`) applied with override note, frontmatter complete, citation style consistent (`wiki:Ghost`, `track_b: Owner`, chapter ranges), Edges section populated with `OWNS`, `BORN_AT`, `DIED_AT`, `SIBLING_OF`, `KILLS`. Body sections in spec order. Quality is strong.

## What Matt's session caught on closer inspection

### Slug deviation: `nymeria-direwolf.node.md` instead of `nymeria.node.md`

The manifest's `expected_nodes[]` listed `nymeria.node.md`. Actual emitted file is `nymeria-direwolf.node.md`. Both were "valid" under the v1 validator's count-only check.

Initial read: validator gap (silent-rename masked) + emergent disambiguation pattern. Suggested fix: tighten validator to enforce slug-set equality, add a "no silent renames" prompt rule.

### Reading the bundle changed the conclusion

Inspecting `working/wiki-pass2/direwolves/bucket_input.json` revealed:

- `page: "Nymeria"`, `raw_html_path: sources/wiki/_raw/Nymeria.json` (75,693 bytes)
- `track_b_row.aliases: ["Nymeria of the Rhoyne"]`
- `track_b_row.relationships`: titles → Princess of Dorne; allegiances → House Martell; consorts → Mors Martell, Davos Dayne; issue → Four daughters with Mors
- `track_b_row.first_available: ADWD chapter 6 (Tyrion II POV)`

This is **Princess Nymeria of Ny Sar** — the Rhoynish warrior queen, ancestor of House Martell. Not the direwolf.

The actual direwolf wiki page is `Nymeria (direwolf)` (a separate file: `sources/wiki/_raw/Nymeria_(direwolf).json`, 53,330 bytes). The triage script's direwolf override matches on the bare name "Nymeria" without disambiguator, routing the wrong page into the bucket.

### How the agent handled it

`working/wiki-pass2/questions-for-matt.jsonl` (after the smoke run) contains exactly one row:

```json
{"question_id": "q-2026-04-26-001", "bucket_id": "direwolves", "page": "Nymeria",
 "type": "disambiguation", "blocking": false,
 "text": "The bucket's raw_html_path and track_b_row for 'Nymeria' point to the
 historical Princess Nymeria of the Rhoynar (sources/wiki/_raw/Nymeria.json), not
 Arya's direwolf. The correct page is sources/wiki/_raw/Nymeria_(direwolf).json.
 I built the node from the direwolf page and ignored the track_b_row data (which
 contained titles like Princess of Dorne, allegiances to Rhoynar/House Martell,
 etc.). The triage script should map this bucket entry to 'Nymeria_(direwolf)'
 instead of 'Nymeria'. Node emitted as nymeria-direwolf.node.md using wiki
 infobox data from the correct page.", ...}
```

The emitted node's `## Notes` section also discloses the override:

> **Disambiguation:** The bucket's `raw_html_path` and `track_b_row` pointed to the "Nymeria" page, which is about the historical Princess Nymeria of the Rhoynar, not Arya's direwolf. This node was built from `sources/wiki/_raw/Nymeria_(direwolf).json` instead. A question has been filed in `questions-for-matt.jsonl`. The track_b aliases and relationships from the bucket input belong to the historical Nymeria and were NOT used here.

The agent:
- Detected the source mismatch
- Found the correct cache file (inferred from the wiki URL pattern + Glob over `sources/wiki/_raw/*Nymeria*` is the most likely path; agent had Read+Glob+Grep+Write available)
- Built a wiki-grounded node from the correct page
- Filed a structured question with full context and a suggested resolution
- Disclosed the override in the node body
- Set the slug + `wiki_source` URL to the disambiguated form

This is the structured-channel discipline the wiki-ingester prompt prescribes. **It worked.** The agent's "wrong" slug is in fact a signal — it was correctly disambiguating output for a bundle that was wrong.

### Reframing the suggested updates

Initial suggestions (before reading the question file):
- Tighten validator to enforce slug-set equality against `expected_nodes`
- Add wiki-ingester prompt rule against silent renames

After reading the question file:
- A slug-equality check would **fail** the existing nymeria-direwolf node, which is correct output. Wrong fix.
- The agent's behavior was correct under its existing prompt. No prompt change needed.
- The actual root cause is in the **triage layer**: the direwolf override hard-codes "Nymeria" without disambiguator. Should map known-collision names to their disambiguated wiki page names (`{"Nymeria": "Nymeria (direwolf)"}` is the only collision in this bucket).
- The actual process gap is that the **smoke-summary did not surface `questions-for-matt.jsonl`**. The autonomous session's wrap reported "0 coherence issues / Promoted 6" but didn't mention the question. At scale (42 core × N pages, 495 secondary × N pages), manually grepping the question file after every run is not viable. Launcher should print unresolved-question counts per bucket as part of its summary.

Documented in detail in `working/runbooks/wiki-pass2-orchestration-build-self-review.md` § "Smoke-run findings (2026-04-26, Session 20 review)".

## Decisions

1. **Don't ship the originally-suggested validator/prompt updates.** The agent's existing behavior is correct. Slug-equality enforcement would regress on a node that's actually right. (Reasoning: the slug deviation is a signal, not a defect.)

2. **Don't scale to core tier yet.** Two issues need to land before fanout makes sense:
   - **T1 (triage direwolf override)** — single-bucket re-run to fix the only known collision. Optional before scale; nymeria-direwolf will need re-emission afterward.
   - **P1 (smoke-summary surfacing of questions/conflicts/contradictions)** — strongly suggested before scale. Without it, structured questions accumulate silently across the 42-bucket core run.

3. **Existing `nymeria-direwolf.node.md` content stays for now.** Wiki-grounded, well-cited, transparent in its `## Notes`. Mark for re-emission after T1 fix lands so the node is reproducible from a clean bundle.

4. **First Pass 2 cost data point captured:** 6 pages, 4m 47s, $1.15, 783k cache-read tokens. Single bucket — too noisy to extrapolate to tier scale, but the cache-read ratio (~91% of tokens) suggests the prompt + architecture.md + bundle parsing dominates, with relatively cheap per-page output. Larger buckets should be sub-linear in cost-per-page. CSV row landed in `working/extraction-stats/wiki-pass2-stats-core-v1.csv`.

## Surprises

- **The agent went outside the bundle to read `Nymeria_(direwolf).json` directly.** Strictly the prompt says "the bundle and the files it points at" — and the bundle did not point at `Nymeria_(direwolf).json`. But the agent inferred the correct file from the wiki URL pattern. This is a soft prompt-rule violation that produced correct output and was disclosed transparently. Worth deciding deliberately: tighten the prompt to forbid this behavior (and risk losing the self-correction capability), or formalize the pattern (any time the agent reaches outside the bundle, file a question). Leaning toward the latter — the agent's discipline is the safety mechanism, not the bundle-isolation rule alone.
- **Validator + coherence-checker green-passed a node from a wrong source.** Both checks are structural (frontmatter completeness, no orphan edges, no name collisions). Neither verifies that node body is grounded in the bundled HTML. That gap is by design (content-quality checks are out-of-scope for v1) but a partial mitigation is to surface questions filed during the run.
- **Cache-read tokens dwarf cache-create.** 783k read vs. 69k create. The agent loaded the wiki-ingester prompt + architecture.md + bundle from cache aggressively. Suggests Pass 2 is highly cache-friendly and the per-bucket marginal cost will scale roughly with bundle size + output token count, not full prompt re-read.

## End-state on disk

- `scripts/wiki-pass2.sh:286-290` — `if`-block fix for orphan-recovery summary
- `graph/nodes/characters/` — 6 direwolf nodes (ghost, grey-wind, lady, nymeria-direwolf, shaggydog, summer)
- `working/wiki-pass2/direwolves/manifest.json` — status `complete`, `nodes_promoted: 6`
- `working/wiki-pass2/direwolves/bucket_input.json` — preserved for forensics; will be regenerated when bucket re-queued
- `working/wiki-pass2/direwolves/validator-report.json` — passed
- `working/wiki-pass2/questions-for-matt.jsonl` — 1 unresolved disambiguation question (Nymeria)
- `working/extraction-stats/wiki-pass2-stats-core-v1.csv` — 1 row (direwolves)
- `working/runbooks/wiki-pass2-orchestration-build-self-review.md` — extended with smoke-debug fix + smoke-run findings sections
- Worklog Session 20 entry, todos updated, continue prompt swap (smoke-debug → triage-disambiguation+summary-surfacing)

## What's next

Continue prompt: `progress/continue-prompts/2026-04-26-wiki-pass2-triage-disambiguation.md`

Sequence:
1. Fix T1 (triage direwolf override → use disambiguated page names)
2. Fix P1 (launcher prints unresolved-question counts in smoke summary)
3. Reset direwolves bucket and re-emit (`weirwood wiki reset --bucket direwolves`, then run)
4. Confirm smoke-summary now surfaces "0 unresolved questions" after re-run
5. Then scale to remaining 41 core buckets via `weirwood wiki core <terms> <waves>`
