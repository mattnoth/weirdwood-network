# Wiki Pass 2 — Orchestration Plan: Independent Review

> **Review of:** `working/runbooks/wiki-pass2-orchestration.md`
> **Reviewer mode:** Fresh-agent independent read (no access to writing agent's self-review notes; findings derived from the plan, the scripts it claims to mirror, and a sampling of the wiki cache).
> **Date:** 2026-04-25

---

## Summary Verdict

**Needs targeted patches before implementation.**

The plan's high-level shape is sound: triage → buckets → wave-of-buckets per terminal tab, mirroring `extract.sh`. The mirror fits well enough for soft-stop, stats CSV, and the per-pass stop file, and §3.3's coherence checker is a real (well-handled) deviation from Pass 1's per-chapter independence.

The patches needed are mostly localized: ~15 small clarifications + 2 design decisions (bucket-disjointness rule, reset command) + 1 reality check on what the wiki cache actually looks like on disk vs. what the runbook seems to assume. Q2 (bucket curation) and Q3 (confidence-tier driver) remain genuinely open — implementation will force partial answers, but neither requires a full re-plan.

The implementation continue prompt at `progress/continue-prompts/2026-04-25-implement-wiki-pass2-orchestration.md` is internally inconsistent in one place (Build Order §5 says "extend `scripts/weirwood.zsh`"; DoD checkbox 5 says "`scripts/weirwood-wiki.zsh` wraps the launcher" — these disagree). Note flagged for the patch session.

The planning continue prompt referenced in this review's "What to Read" (§2) was deleted earlier this session as a superseded predecessor; the review prompt itself should be updated by the patch session to drop that reference.

---

## Issues Found

Numbered by review section. Each entry: (a) section/line reference, (b) what's wrong, (c) suggested resolution.

### 1. `is_bucket_complete()` is not a mirror of `is_complete()` — it's a step-up in complexity

- **Where:** Runbook §5.1, Appendix mapping table.
- **What's wrong:** `extract.sh::is_complete` (lines 99-109) checks: file exists + ≥100 lines + 4 named section headers. It is purely *content-shape* and operates on a single file. The wiki analog must read JSON manifests, validate fingerprints, and verify N node files at once. The runbook treats this as a one-line mirror in the appendix table; it isn't. The mismatch is also a re-run footgun: extract.sh reasons solely from the filesystem, so manual edits never desync from script state. The wiki analog has dual sources of truth (manifest JSON + on-disk nodes) that can disagree (e.g., user manually deletes one node from `graph/nodes/` but manifest still says `complete`).
- **Resolution:** Add a §5.1.1 "Reconciliation rules" subsection: define what happens when the manifest disagrees with the filesystem. Suggested rule: filesystem is canonical; manifest `complete` + missing node files → manifest is downgraded to `partial` on next launch and only the missing entities re-run.
- **Decision (2026-04-25):** Accepted as stated. Patch session implements the `§5.1.1 Reconciliation rules` subsection with the filesystem-canonical rule.

### 2. `update_worklog()` has no target line to mutate

- **Where:** Implementation Sequence §5 says "Worklog auto-update: same pattern as `extract.sh::update_worklog`." Runbook does not specify the worklog line shape.
- **What's wrong:** `extract.sh::update_worklog` (lines 42-96) finds and rewrites a checklist line matching `Pass 1 v3 run on AGOT`. Worklog currently has a `- [ ] Pass 2 wiki ingestion complete` line but nothing per-tier. The implementation will need to either (a) invent a per-tier line and seed it in worklog.md before first run, or (b) generalize the matcher to handle a different line shape.
- **Resolution:** Specify the target line(s) — e.g., `- [ ] Wiki Pass 2 v1 — {tier} ({done}/{total} buckets)`, one per tier. Seed them in worklog.md as part of the first patch.
- **Decision (2026-04-25):** Accepted as stated. Patch session seeds per-tier checklist lines in `worklog.md` and codifies the `update_worklog()` matcher pattern.

### 3. Bucket disjointness rule is implicit, never stated

- **Where:** Runbook §1.2 (triage manifest schema with single `bucket` field), §1.3 (auto-derivation open question), §5.2 (manifest `expected_nodes` list per bucket).
- **What's wrong:** The data model only works if each page belongs to exactly one bucket. Smoke test 4 (Aegon I → 3 plausible buckets) makes this concrete: auto-deriving from wiki categories will produce multi-bucket assignments unless a tiebreaker rule is specified. Cross-bucket validator/coherence checks assume `expected_nodes` lists are disjoint across buckets.
- **Resolution:** Add an explicit rule to §1.2: "Each page → exactly one bucket. Triage's tiebreaker for multi-category pages: most-specific category wins; ties broken by category list order in the wiki HTML." Cross-bucket *references* (e.g., a Lannister character bucket needing to link to House Lannister in a houses bucket) are handled via edges, never by listing the same page in two buckets.
- **Decision (2026-04-25):** Accepted as stated. Patch session adds the disjointness rule + tiebreaker to §1.2.

### 4. Triage assumes a category-on-disk taxonomy that does not exist

- **Where:** Runbook §1.1 ("triage signals: …wiki category set"), §1.2.
- **What's wrong:** Verified against the cache: of `sources/wiki/`'s named subdirectories, only `houses/` (633 files) is populated. `characters/`, `locations/`, `events/`, `artifacts/` are *empty*. 16,943 pages live in `_uncategorized/`, including Eddard_Stark, Jon_Snow, Winterfell, Ghost — exactly the entities the runbook's example buckets (`characters-stark`, `direwolves`, `north-locations`) would draw from. The runbook talks about category-based bucketing as if the cache already had categories, but the on-disk categorization is nearly absent.
- **Resolution:** Add a §1.2.1 note: "Categories come from `<a href=\"/Category:...\">` links inside the cached HTML, parsed by Track B (or the triage script). The on-disk subdirectory layout in `sources/wiki/{characters,locations,events,artifacts}/` is *not* the source — those directories are mostly empty." Triage must extract category links from HTML.
- **L1 page-index deliverable (added per discussion):** Track B's scope expands to emit `working/wiki-parsed/page-index.jsonl` — one row per page with `{page, entity_type_guess, categories[], cite_ref_books[], has_infobox, byte_size}`. This is the queryable index that triage (L2) and per-bucket manifests (L3) build on. Revisits at any review tier grep this file rather than re-parsing 17k HTML blobs. Add to the Track B continue prompt's "Data to Extract" section as item 5; add to the runbook's §1.1 "Deterministic" list.
- **Decision (2026-04-25):** Accepted as stated, including the L1 page-index amendment. Patch session updates §1.2.1 (HTML category source) and §1.1 (L1 deliverable), and amends `progress/continue-prompts/2026-04-24-track-b-wiki-infobox-parser.md` to add `page-index.jsonl` as deliverable item 5.

### 5. `_category-reports/` is referenced as a triage signal but is empty

- **Where:** Runbook implicitly via "wiki category set" signal; the planning continue prompt (now deleted) explicitly told this session to "scan `_category-reports/`."
- **What's wrong:** `sources/wiki/_category-reports/` exists but has no files. If the implementation agent goes looking for category dumps to drive bucketing, it will find an empty directory.
- **Resolution:** Either (a) re-run the wiki-scraper to produce category reports if that was an intended output, or (b) drop references to `_category-reports/` and rely entirely on category-link extraction at parse time. Pick one explicitly in the runbook.
- **Decision (2026-04-25):** Accepted with option (b): drop `_category-reports/` references. The L1 page-index (issue 4) is the canonical category source; any category overview can be derived from L1 in two grep lines. Patch session removes references to `_category-reports/` from the runbook.

### 6. `_conflicts/` directory has no consumer

- **Where:** Runbook §6.5 first hard rule.
- **What's wrong:** The "no overwrite" rule writes conflict files to `graph/nodes/_conflicts/<entity>-<bucket>-<timestamp>.node.md` and "logs a curation entry." Where? `curation/candidates.md` is named elsewhere as the Pass 1 curation surface but isn't connected to `_conflicts/` here. Without a consumer, conflict files accumulate silently — exactly the failure mode this rule is meant to prevent.
- **Resolution:** Either (a) auto-append a structured row to `working/wiki-pass2/conflicts.jsonl` (page, bucket, timestamp, conflict reason) on every conflict write, then have `weirwood wiki status` print conflict count; or (b) define a separate `curation/wiki-pass2-conflicts.md` and specify when/how Matt drains it. Pick one and codify.
- **Decision (2026-04-25):** Accepted with option (a): JSONL conflicts log at `working/wiki-pass2/conflicts.jsonl`. Consistent with Pass 2's other data-layer files (Track B JSONL, triage JSONL, edges JSONL). Status command surfaces conflict count. Optional `wiki-pass2.sh conflicts` subcommand for prose rendering — defer until needed.

### 7. No reset command — manual archival is hand-waved at 10k-node scale

- **Where:** Runbook §5.4 ("User must explicitly archive `graph/nodes/` to a versioned directory"), §6.5 second hard rule ("Reset is an explicit, separate command").
- **What's wrong:** The reset command does not exist. §5.4 describes the result ("archive `graph/nodes/`") but not the mechanism (a script? a `wiki-pass2.sh reset` subcommand? `mv` and pray?). Pass 1 had no reset because 73-344 chapter outputs are tractable to manage manually. Pass 2 will produce ~5,000-10,000 nodes; manual `mv` is a foot-gun (forgetting bucket manifests, leaving stale fingerprints, mixing v1+v2 nodes in one tree). Smoke test 5 stalls here.
- **Resolution:** Define `wiki-pass2.sh reset --version v1` (or similar). Behavior: archives `graph/nodes/{characters,houses,locations,...}/` and `working/wiki-pass2/*/manifest.json` to `graph/archives/wiki-pass2-v1-<timestamp>/`, leaves `working/wiki-parsed/` (Track B output) untouched, prints a summary. Add as DoD item in the implement prompt.
- **Decision (2026-04-25):** Accepted as stated. Patch session adds `wiki-pass2.sh reset` subcommand to the runbook spec and adds "Reset command works on a populated `graph/nodes/`" to the implement prompt's DoD checklist.

### 8. Mid-bucket kill leaves manifest in unrecoverable `in-progress` state

- **Where:** Runbook §5.2 (manifest schema with `status: in-progress`), §6.5 fifth rule.
- **What's wrong:** Soft-stop (`/tmp/wiki-pass2-stop`) checks between buckets, not mid-bucket. A `kill -9` mid-bucket leaves manifest at `in-progress` and `tmp/` files on disk. The runbook says "auto-discarded next launch via fingerprint mismatch" — but fingerprint covers prompt+inputs, not in-flight state. On relaunch, the launcher needs a rule for `in-progress` manifests: treat as `pending` (assume the prior process is dead) or refuse (require manual reset)? Smoke test 3 stalls here.
- **Resolution:** Specify in §5.4: "On launch, any `in-progress` bucket whose `started_at` is older than N minutes (default: 60) is treated as orphaned: its `tmp/` is wiped and the bucket is reset to `pending`. Newer `in-progress` buckets are skipped (assume another tab owns them)." Add an explicit "stuck bucket" reset path: `wiki-pass2.sh unstick <bucket>`.
- **Decision (2026-04-25):** Accepted as stated. Patch session adds the orphan-detection rule to §5.4 and the `unstick` subcommand to the spec.

### 9. Question queue lacks schema, dedup, and drain state

- **Where:** Runbook §6.5 question queue paragraph.
- **What's wrong:** "Agent appends to `working/wiki-pass2/questions-for-matt.md`. No schema. Matt drains by grep." At Pass 2 scale, even 5 questions per bucket × 200 buckets = 1,000 entries. Without a schema, two buckets can ask the same disambiguation and Matt can't tell. Without a drain state (resolved/pending), the file grows unboundedly.
- **Resolution:** Switch to JSONL with a minimal schema: `{question_id, bucket_id, page, type (disambiguation|tier|promotion|other), text, blocking, asked_at, resolved_at, resolution}`. Provide `wiki-pass2.sh questions [--unresolved|--bucket X]` for filtering. Markdown rendering can be a separate `format` subcommand if Matt prefers prose for review.
- **Decision (2026-04-25):** Accepted as stated. Patch session replaces `questions-for-matt.md` with JSONL spec at `working/wiki-pass2/questions-for-matt.jsonl` and adds `wiki-pass2.sh questions` subcommand to the runbook spec.

### 10. Pass 1 contradiction signal has no channel — violates "all decisions traced"

- **Where:** Runbook §6.5 third paragraph (provisional v1), §6.5 hard rule "All decisions traced."
- **What's wrong:** "Cross-check with Pass 1 is a *signal* (logged), not a *gate*." Where is it logged? No file is named. The provisional-v1 design implies contradictions accumulate for a future v2 pass, but they have nowhere to accumulate. Smoke test 2 stalls here. This silently violates the "All decisions traced" rule from the same section.
- **Resolution:** Append every Pass-1-vs-wiki contradiction to `working/wiki-pass2/pass1-contradictions.jsonl` with `{node, claim, pass1_evidence, wiki_evidence, detected_at}`. Surface counts in `wiki-pass2.sh status`. The v2 schema-review session reads this file as direct input.
- **Decision (2026-04-25):** Accepted as stated. Patch session adds `pass1-contradictions.jsonl` spec to §6.5 and surfaces the count in the status command.

### 11. Q2 (bucket curation strategy) is blocking for triage implementation

- **Where:** Runbook §1.3 open question, §Open Questions item 2.
- **What's wrong:** The triage script cannot run without a bucket-derivation strategy. The runbook says "lean: auto-derive a draft, accept hand-edits before launch" but doesn't specify the auto-derivation rule, the draft format, or how hand-edits feed back into bucket manifests. The implement prompt §Open Questions punts Q2 to "next session unless implementation forces them" — implementation forces it.
- **Resolution:** Propose a concrete v1 rule in the runbook to anchor the implementer: "Buckets are derived from wiki categories one-to-one for categories with 5-30 members. Categories with >30 members are split alphabetically. Categories with <5 members are merged into a sibling bucket. Output is `working/wiki-pass2/draft-buckets.jsonl`; user reviews and re-runs triage with `--accept` to commit." The implementer can refine; the plan should at least anchor.
- **Decision (2026-04-25):** Accepted as stated. Patch session adds the v1 bucket-derivation rule to §1.3 and the draft → review → `--accept` flow. Q2 closed for now; revisit if v1 rule proves wrong in practice.

### 12. Q3 (confidence-tier driver) blocks the wiki-ingester prompt

- **Where:** Runbook §Open Questions item 3.
- **What's wrong:** The agent has to assign a confidence tier per claim. The runbook says "likely hybrid: category sets default, agent overrides per claim with justification" but doesn't specify the category→tier defaults. The wiki-ingester prompt cannot be written without them. The implement prompt §Open Questions defers Q3 "if prompt is split out" — but DoD item 6 ("Wiki-ingester agent prompt") expects it written, contradicting the defer.
- **Resolution:** Land a v1 mapping in the runbook: e.g., "Pages in wiki Categories `*Theory*`, `*Speculation*` → default Tier 4. Pages in `*Battle*`, `*Character*`, `*House*`, `*Location*` → default Tier 1. Mixed sections (a character's `Speculation` subsection) → agent assigns per-claim with chapter citation requirement for Tier 1." Refine in implementation.
- **Decision (2026-04-25):** Accepted as stated. Patch session adds the v1 category→tier mapping to the runbook (likely a new §1.4 "Confidence-tier defaults") and references it from the wiki-ingester prompt design. Q3 closed for v1; expect refinement after first scaled run.

### 13. Bucket size budget is a target, not a gate — single page can exceed it

- **Where:** Runbook §1.3 ("Size target per bucket: 10-30 pages, total content ≤ ~150k input tokens").
- **What's wrong:** Verified against cache: `House_Stark.json` alone is 646 KB (~160k tokens, before reasoning overhead). `Jon_Snow.json` is 305 KB (~76k). `Tyrion_Lannister.json` is 261 KB (~65k). A "singleton large page bucket" for House Stark already breaches the 150k target. Page-size variance across the cache is ~12-700x (Shaggydog 26 KB → House Stark 646 KB). The runbook says the agent should "hold the bucket in working context with cache reuse" — but a single oversized page can blow that on its own, and the auto-deriver has no enforcement.
- **Resolution:** Add a triage-time budget check: every bucket manifest's input-page total bytes is computed; buckets exceeding 600 KB raw HTML get flagged for split or for a different prompt strategy (e.g., chunk the page into sections before agent dispatch). Also: state explicitly in the runbook that singleton-mega-pages may need a bespoke bucket-of-one with a chunked-input agent prompt — not just "isolation."
- **Decision (2026-04-25):** Accepted as stated. Patch session adds the triage-time budget check + singleton-mega-page chunking note to §1.3.

### 14. Agent input contract is undefined

- **Where:** Runbook §2.1 (says agent runs "per bucket") and Implementation Sequence §6 (the prompt is downstream).
- **What's wrong:** What does the agent actually receive? Track B JSONL rows for the bucket pages? Raw HTML? Pre-parsed Track B output for related pages? Pass 1 raw entity lists — for which book(s)? The implement prompt §1 says "Input: Track B JSONL + raw wiki cache + Pass 1 raw entity lists." That's three input streams; the runbook never says who composes them or whether the agent reads files itself or receives a pre-composed bundle. Smoke test 1 stalls at this step.
- **Resolution:** Add §2.1.1 "Agent input contract": the launcher writes a `bucket_input.json` next to the manifest containing (a) absolute paths to per-page raw HTML, (b) Track B JSONL rows filtered to the bucket's pages, (c) cross-references from Pass 1 raw entity lists where the page name matches an extracted entity. The agent's prompt instructs it to read this file and proceed. Unifies the input surface and makes resumption deterministic.
- **Decision (2026-04-25):** Accepted as stated. Patch session adds §2.1.1 with the `bucket_input.json` schema and codifies that the launcher composes the bundle (not the agent).

### 15. `graph/nodes/` subdirectory routing by entity_type is unspecified

- **Where:** Runbook §5.1 ("`graph/nodes/<type>/<entity>.node.md`").
- **What's wrong:** Architecture.md's type hierarchy is dotted (e.g., `character.human`, `character.direwolf`, `place.location`). Runbook uses `<type>` as the directory name without specifying the mapping: is `character.direwolf` → `graph/nodes/character/direwolf/ghost.node.md` (nested) or `graph/nodes/characters/ghost.node.md` (flattened to parent type)? CLAUDE.md's directory tree shows `graph/nodes/characters/`, `graph/nodes/locations/`, `graph/nodes/factions/`, `graph/nodes/houses/`, etc. — flattened to parent. That's the existing convention; runbook should adopt it explicitly.
- **Resolution:** Add to §5.1: "Routing rule: `<type>` is the parent type from architecture.md's hierarchy (Character, Place, Organization, …) lowercased and pluralized as in CLAUDE.md (`characters/`, `places/` or `locations/`, `houses/`, …). Leaf type goes in frontmatter `type:` field, not in the path."
- **Decision (2026-04-25):** Accepted as stated. Patch session adds the routing rule to §5.1, matching CLAUDE.md's existing convention.

### 16. Validator caller is unspecified (agent vs. launcher)

- **Where:** Runbook §3.1 ("runs after each bucket completes"), Implementation Sequence §2.
- **What's wrong:** Does the agent self-validate before signaling done, or does the launcher run the validator after `claude -p` returns? Both are defensible; the runbook implies the latter ("validation gate from §3.1 is the only path from `tmp/` to `graph/nodes/`") but never says it. If the agent self-validates, atomic-rename happens inside the agent (more complex agent prompt). If the launcher validates, agent only writes to `tmp/` and exits.
- **Resolution:** State in §3.1: "Validator is invoked by the launcher (`wiki-pass2.sh::cmd_run`) after `claude -p` returns. The agent never moves files out of `tmp/`. Atomic rename happens in the launcher on validator pass."
- **Decision (2026-04-25):** Accepted as stated. Patch session codifies launcher-as-validator-caller in §3.1.

### 17. Bucket discovery mechanism unspecified

- **Where:** Runbook §5 (resumption), Implementation Sequence §1.
- **What's wrong:** `extract.sh::discover_chapters` reads `sources/chapters/<book>/*.md`. The wiki analog must enumerate buckets — from `working/wiki-pass2/*/manifest.json`? From the triage manifest JSONL? Both? They can disagree (manifest dir is canonical for status; triage JSONL is canonical for membership). If a triage re-run adds a new bucket, does the launcher discover it on next launch?
- **Resolution:** Specify in §5: "Bucket discovery reads `working/wiki-pass2/*/manifest.json` first (canonical state). On each launch, the triage manifest JSONL is consulted for buckets without on-disk manifests; missing manifests are generated before the run starts. Triage manifest is the *membership* truth; per-bucket manifests are the *status* truth."
- **Decision (2026-04-25):** Accepted as stated. Patch session adds the discovery rule to §5 with the explicit membership-vs-status truth distinction.

### 18. `tmp/` subdirectory inside bucket dir is implicit

- **Where:** Runbook §3.1 and §6.5 reference `tmp/` repeatedly as a staging location.
- **What's wrong:** The directory layout for in-flight output is referenced but never declared. Smoke test 1 walked through `working/wiki-pass2/<bucket>/tmp/*.node.md` — that's the obvious convention but uncodified.
- **Resolution:** Add to §5.2 manifest section: "Per-bucket on-disk layout: `working/wiki-pass2/<bucket>/manifest.json`, `working/wiki-pass2/<bucket>/tmp/<entity>.node.md` (in-flight output), `working/wiki-pass2/<bucket>/bucket_input.json` (agent input bundle), `working/wiki-pass2/<bucket>/validator-report.json` (last validator run)."
- **Decision (2026-04-25):** Accepted as stated. Patch session codifies the per-bucket on-disk layout in §5.2.

### 19. `wiki-pass2.sh status` output shape is undefined

- **Where:** Runbook §Appendix mapping table.
- **What's wrong:** `extract.sh::cmd_status` produces a wave-by-wave table of missing chapters, completed-waves summary, and a cost roll-up. The wiki analog needs equivalents per-bucket per-tier. Runbook doesn't sketch the output. Smoke test 3 (walk-away recovery) needs this.
- **Resolution:** Add §4.3.1 "Status output": ASCII table with columns `bucket | tier | wave | status | nodes_emitted | last_run`. Roll-up: `{tier}: {ok}/{total} buckets complete, {pending} pending, {failed} failed, ${total_cost} so far`.
- **Decision (2026-04-25):** Accepted as stated. Patch session adds §4.3.1 status-output spec.

### 20. Wave-of-buckets discovery has no `find_incomplete_waves` analog

- **Where:** Runbook §2.1 ("a wave for wiki = a sequence of buckets a single tab processes").
- **What's wrong:** `extract.sh::find_incomplete_waves` (lines 131-151) walks chapter slices and identifies waves where any chapter is incomplete. The wiki version needs to walk bucket lists in tier order and identify waves where any bucket is incomplete. But buckets aren't pre-grouped into waves at triage time — the runbook implies waves are formed at launch time from the incomplete-bucket queue. The grouping rule (sequential? size-balanced? tier-mixed?) isn't specified.
- **Resolution:** Add to §2.1: "Waves are formed at launch from the incomplete-bucket queue, sorted by tier (core first), then by bucket_id. Wave size = 3-5 buckets. Cross-tier mixing only happens if a tier finishes mid-wave."
- **Decision (2026-04-25):** Accepted as stated. Patch session adds the wave-formation rule to §2.1.

### 21. Implement prompt is internally inconsistent (`weirwood.zsh` vs. `weirwood-wiki.zsh`)

- **Where:** `progress/continue-prompts/2026-04-25-implement-wiki-pass2-orchestration.md`. Build Order §5 says "extend `scripts/weirwood.zsh`" (correct, matches the runbook's appendix "stay on `weirwood`, add a `wiki` subcommand"). DoD checkbox 5 says "`scripts/weirwood-wiki.zsh` wraps the launcher" (wrong — would create a sibling script instead of a subcommand).
- **What's wrong:** The two lines contradict. An implementation agent following DoD literally would create `weirwood-wiki.zsh` and bypass the subcommand-on-existing-`weirwood` design. The runbook is canonical and says subcommand.
- **Resolution:** Patch the implement prompt: rewrite DoD item 5 to read "`scripts/weirwood.zsh` extended with `wiki` subcommand (wraps `wiki-pass2.sh` with same UX as existing `weirwood agot ...`)." No new file.
- **Decision (2026-04-25):** Accepted as stated. Patch session edits the implement prompt's DoD item 5.

---

## Smoke Test Results

### Smoke 1 — `direwolves` bucket end-to-end

Trace stalls in five places: bucket discovery (issue 17), agent input contract (issue 14), tmp/ layout (issue 18), validator caller (issue 16), graph/nodes/ subdirectory routing (issue 15). All fixable with small additions; none invalidate the design. Direwolf bucket itself is well-shaped: 7 pages (Direwolf species + 6 named direwolves), ~357 KB total HTML, comfortably under the 150k-token bucket budget.

### Smoke 2 — Pass 1 contradiction

Stalls hard at issue 10: the contradiction has nowhere to go. The runbook acknowledges Pass 1 contradictions are signals but never names the channel. This is the most consequential of the small issues because it silently violates the "All decisions traced" rule the runbook itself sets.

### Smoke 3 — Walk-away with halted run

Recovery works partially: stats CSV gives rate-limit reset times, manifest file gives per-bucket status. Two gaps: (a) `wiki-pass2.sh status` output shape unspecified (issue 19); (b) reconciliation when manifest says `in-progress` but the owning process is dead (issue 8). Matt would have to manually inspect tab-by-tab to figure out who owns what — and the runbook's framing is "session-killable mid-run" and "walk-away safe," so the manual inspection cost contradicts the design intent.

### Smoke 4 — Multi-bucket page (Aegon I)

Stalls at issue 3 (disjointness rule). Auto-derivation will assign Aegon I to multiple buckets unless a tiebreaker is specified. The "lean: auto-draft + hand-edit" path described in §1.3 makes this a manual step; for ~17,000 pages the manual review is impractical. Tiebreaker rule is small but mandatory.

### Smoke 5 — Reset

Stalls at issue 7 (no reset command). The "manually archive `graph/nodes/`" path works for a small first-cut but is a footgun at full scale (10k nodes, hundreds of bucket manifests, multiple stat CSV files). A `wiki-pass2.sh reset` subcommand is small to implement; not specifying it leaves the implementer to invent ad-hoc directory moves.

---

## Open-Question Audit

The runbook's §Open Questions list has 7 items. Classified by whether implementation can proceed without resolving them:

| # | Question | Blocks implementation? | Why |
|---|----------|------------------------|-----|
| 1 | Subagents-in-parent vs. tabs | No | Default is tabs; revisit only if a real disambiguation bucket needs it. |
| 2 | Bucket curation auto vs. hand | **YES** (issue 11) | Triage script needs *some* derivation rule. Plan should anchor a v1 rule. |
| 3 | Confidence-tier driver | **YES** (issue 12) | Wiki-ingester prompt cannot be written without category→tier defaults. |
| 4 | Promotion threshold formula | Partial | Implement prompt explicitly says "pick a formula in `triage.py`." Anchoring in runbook would help but isn't strictly blocking. |
| 5 | Node body length budget | Partial | Implement prompt says "pick a number." Same as Q4 — anchor would help. |
| 6 | Curation queue surface | No | Pass 1 surface (`curation/candidates.md`) can be reused short-term; revisit when volume forces split. |
| 7 | Wiki-cache snapshotting | No | Single static crawl exists; multi-crawl reproducibility is a future concern. |

**Net:** 2 of 7 (Q2, Q3) need anchored answers in the runbook before implementation. The remaining 5 can stay open or get punted to in-code documentation.

---

## Estimated Effort to Patch

**Medium.** Most issues are 1-2 paragraph edits to the runbook. Two require small but real design decisions:

- **Small (≤30 minutes total):** issues 1, 2, 6, 8, 13-20 — clarifications, layout codifications, line-shape specs. Each is a 1-3 sentence addition or a small subsection.
- **Medium (~1-2 hours total):** issues 3, 4, 9, 10 — disjointness rule, on-disk reality acknowledgment, question-queue schema, contradiction-signal channel. Each adds a structured artifact (JSONL schema or rule).
- **Real design (~2 hours):** issues 7 (reset command spec), 11 (Q2 bucket-curation v1 rule), 12 (Q3 tier-default mapping). Each adds a concrete decision with rationale.

Total: a focused patch session should land all of this in a single afternoon. After the patch, the implementation continue prompt's DoD checklist is achievable without further plan revisions.

---

## What Is Not Wrong

To balance the issues list — these decisions in the runbook hold up under independent review:

- §3.3 cross-bucket coherence checker — real deviation from Pass 1, well-justified by cross-page identity matching.
- §3.4 hash-fingerprinted inputs — clean re-run semantics, prevents silent staleness.
- §4 stats CSV column shape — drop-in compatible with Pass 1 tooling, sensible 4-column extension.
- §6.5 walk-away-safe principles — the *intent* is right; only the enforcement mechanisms (issues 6-8) are underspecified.
- §7 storage decision (markdown + JSONL + CSV, no DB) — at the realistic Pass 2 edge volume (~80-100k edges), grep stays under 1s. Trigger conditions in §7.3 are reasonable.
- Mirror-where-it-fits philosophy — soft-stop, stats CSV, status command, separate `/tmp/wiki-pass2-stop` are all clean inheritances. Only `is_complete` and `update_worklog` are forced (issues 1, 2).

The plan is closer to "ready" than "rework." The patches are real but localized.

---

## Patches Applied — 2026-04-25

All 21 decisions logged above were applied in a follow-up patch session on 2026-04-25 (Session 17). Cross-reference for future readers verifying that the runbook reflects this review:

| # | Decision | Patch landed in |
|---|----------|-----------------|
| 1 | Reconciliation rules — filesystem canonical | Runbook §5.1.1 (NEW) |
| 2 | Worklog target line shape codified, lines seeded | Runbook §5.2 (subsection); `worklog.md` Extraction Pipeline |
| 3 | Bucket disjointness rule + tiebreakers | Runbook §1.2 (subsection) |
| 4 | Categories from HTML, not on-disk subdirs; L1 page-index amendment | Runbook §1.1 (deterministic list) + §1.2.1 (NEW); Track B prompt item 5 (NEW) |
| 5 | `_category-reports/` references dropped | Runbook §1.2.1 (note) |
| 6 | `_conflicts/` consumer = `working/wiki-pass2/conflicts.jsonl` | Runbook §6.5 (subsection + schema) |
| 7 | `wiki-pass2.sh reset --version vN` subcommand spec | Runbook §5.4 (subsection); implement-prompt DoD |
| 8 | Orphan `in-progress` 60-min rule + `unstick` subcommand | Runbook §5.4 (subsection) |
| 9 | `questions-for-matt.jsonl` schema replaces markdown | Runbook §6.5 (schema) |
| 10 | `pass1-contradictions.jsonl` channel | Runbook §6.5 (schema) |
| 11 | v1 bucket-derivation rule + draft → `--accept` | Runbook §1.3 (subsection) |
| 12 | v1 confidence-tier defaults mapping | Runbook §1.4 (NEW) |
| 13 | Bucket-size budget gate + singleton-mega-page chunking | Runbook §1.3 (subsection) |
| 14 | Agent input contract — `bucket_input.json` schema | Runbook §2.1.1 (NEW) |
| 15 | `graph/nodes/` routing rule (parent type pluralized) | Runbook §5.1 (paragraph + examples) |
| 16 | Validator caller = launcher, never agent | Runbook §3.1 (paragraph) |
| 17 | Bucket discovery — manifests first, triage JSONL fills gaps | Runbook §5.0 (NEW) |
| 18 | Per-bucket on-disk layout codified | Runbook §5.2 (subsection) |
| 19 | `wiki-pass2.sh status` ASCII output spec | Runbook §4.3.1 (NEW) |
| 20 | Wave-formation rule (tier order, alpha within tier) | Runbook §2.1 (subsection) |
| 21 | Implement prompt DoD item 5 (no new file) | `progress/continue-prompts/2026-04-25-implement-wiki-pass2-orchestration.md` rewritten |

Open Questions in the runbook now reflect Q2 and Q3 closed (with cross-references to §1.3 and §1.4 respectively). Q1, Q4, Q5, Q6, Q7 remain open.

The implement continue prompt was also restructured beyond the patch list per a separate user direction: the smoke test (agent invocation against `direwolves`) is removed and deferred to a later "commence" session. The build session writes scripts and runs non-agentic verification only; a script-review session reads the scripts cold; only then does commence. This is a workflow change, not a runbook change — captured here for the future reader who notices the implement prompt no longer matches the runbook's "Implementation Sequence" §7 smoke-test step.

The patch + review continue prompts (`2026-04-25-patch-wiki-pass2-orchestration.md` and `2026-04-25-review-wiki-pass2-orchestration.md`) were deleted at the end of the patch session.
