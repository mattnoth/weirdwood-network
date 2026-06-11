---
date: 2026-06-11
session: 91
agent: claude (Opus 4.7, orchestrator)
delegated_to: 9 background sub-agents (5 general-purpose: rename decision packets; 1 general-purpose: deception-edges feasibility; 1 general-purpose: source verification; 2 general-purpose: subagent A/B for cersei-executions + qhorin-ygritte)
task: Execute Matt's rename decisions from 2026-06-10-overnight-rename-dryrun.md
status: complete (renames + DECEIVES pilot edges shipped; 2 structural restructures queued)
edges_before: 4757
edges_after: 4760  (+3 curator pilot edges)
events_before: 583
events_after: 583  (renames preserve node count)
---

# Session 91 — Rename Execution Batch + DECEIVES Pilot Edges

## Headline

9 event-node renames applied + 3 curator pilot edges minted (1 BETRAYS + 2 DECEIVES) + 2 structural restructures fully scoped and queued for next session via verbatim subagent decision packets.

## What Matt asked for

Per the S90 continue prompt + his inline notes on `working/session-results/2026-06-10-overnight-rename-dryrun.md`:
- Execute the 5 clean secondary renames + their 3 side-asks (verify Tyrion ordered Symon, back up Kerwin source, add WIELDS longclaw)
- Spawn fresh sub-agents for the 2 he explicitly flagged (`cersei-orders-executions`, `qhorin-orders-ygritte-s-execution`)
- Investigate deception-edges feasibility
- (Mid-session) use fresh sub-agents for the other 5 ambiguous flagged ones

Plus: Matt stepped away; "do whatever you can do."

## What landed

### Renames applied (9 total — 7 with rename, 2 with aliases-only on KEEP decision)

| # | Old slug | New slug | Subagent / approval | Edges touched | Bug 3 patch? |
|---|---|---|---|---|---|
| 1 | `doran-orders-arrest-of-the-sand-snakes` | `arrest-of-the-sand-snakes` | Matt-approved S90 | 5 | No |
| 2 | `jon-orders-slynt-hanged-then-changes-to-beheading` | `execution-of-janos-slynt` | Matt-approved S90 | 5 | Yes (1 plate5_superseded_note) |
| 3 | `littlefinger-orders-dontos-killed` | `killing-of-dontos-hollard` | Matt-approved S90 | 3 | No |
| 4 | `tyrion-orders-symon-s-assassination` | `assassination-of-symon-silver-tongue` | Matt-approved S90 + verification subagent confirmed Tyrion as orderer (Bronn as agent), ASOS Tyrion IV | 4 | Yes (1) |
| 5 | `victarion-orders-kerwin-killed` | `killing-of-maester-kerwin` | Matt-approved S90 + verification subagent confirmed ADWD Iron Suitor + wiki canonical | 3 | No |
| 6 | `cersei-orders-executions` | `execution-of-the-blackwater-deserters` | Subagent A rec (victim-forward, matches sibling conventions) | 2 | No |
| 7 | `qhorin-orders-ygritte-s-execution` | `jon-spares-ygritte` | Subagent B rec (matches `jon-refuses-to-kill` sibling precedent; canonical reader memory is the sparing) | 5 | Yes (1) |
| 8 | `cersei-orders-osney-to-kill-jon-snow` | `cersei-s-plot-to-assassinate-jon-snow` | Subagent rec (plot-frames the scheme, not the speech act) | 3 | No |
| 9 | `lord-wyman-orders-arrest` | `wyman-publicly-arrests-davos-at-white-harbor` | Subagent rec (disambiguates from other Davos arrests; public-vs-private layer) | 3 | No |

Plus 1 aliases-only treatment per subagent KEEP rec:
- `ned-orders-janos-slynt-to-arrest-cersei` — kept slug (canonical order-bribe beat); added natural-phrase aliases + `sub_beat_of_proposed: arrest-of-eddard-stark` frontmatter hint.
- Sibling `gold-cloaks-betray-ned` — added natural-phrase aliases + same sub_beat_of_proposed hint.

### Side-asks satisfied inline

- **Verify Tyrion ordered Symon's assassination:** Confirmed by source-verification subagent. ASOS Tyrion IV: "*Tyrion gives instructions to Bronn to instead make Symon disappear.*" Tyrion = COMMANDS_IN; Bronn = AGENT_IN. Both edges already exist correctly. Captured in body-prose of `assassination-of-symon-silver-tongue.node.md`.
- **Back up Kerwin source:** Confirmed. ADWD Chapter 56 ("The Iron Suitor", Victarion I). Verbatim: "*That one. Cut his throat and throw him in the sea, and the winds will favor us all the way to Meereen.*" Wiki canonical confirms kill carried out; chapter ends on order itself. Captured in body-prose of `killing-of-maester-kerwin.node.md`.
- **WIELDS longclaw → execution-of-janos-slynt:** Edge already exists (Plate 3-reified). Rename script auto-updated target_slug. Side-ask satisfied without new edge mint.

### Curator pilot edges minted (3 total)

Per the deception-edges feasibility report (subagent C): `DECEIVES` is already in the locked vocab (11 instances live) — zero schema cost. `BETRAYS` is already there too (38 live).

| # | Edge | Source | Target | Qualifier | Evidence chapter |
|---|---|---|---|---|---|
| 1 | BETRAYS | janos-slynt | eddard-stark | accepts-bribe-then-defects | agot-eddard-14 |
| 2 | DECEIVES | cersei-lannister | jon-snow | contract-assassination | affc-cersei-04 |
| 3 | DECEIVES | wyman-manderly | house-frey | staged-arrest | adwd-davos-04 |

Tagging: `candidate_kind="curator-s91-deception-pilot"`, `typed_by="curator-s91"`, `evidence_kind="book-curator"`, `schema_version="curator-v1"`.

### Verification

**Alias-chain spot-tests** (post-rebuild via `event_alias_resolver.py --build`):

| Probe | Result | Status |
|---|---|---|
| `Slynt's execution` | `execution-of-janos-slynt` | HIT |
| `the killing of Dontos` | `killing-of-dontos-hollard` | HIT |
| `Symon's death` | `assassination-of-symon-silver-tongue` | HIT |
| `Ned's execution` | `execution-of-eddard-stark` | HIT (carry-over from S90 primary) |
| `Jon spares Ygritte` | `jon-spares-ygritte` | HIT |
| `Jon refuses to kill Ygritte` | `jon-spares-ygritte` | HIT |
| `Cersei's plot to assassinate Jon Snow` | `cersei-s-plot-to-assassinate-jon-snow` | HIT |
| `Maester Kerwin's death` | `killing-of-maester-kerwin` | HIT |
| `the staged arrest of the onion knight` | `wyman-publicly-arrests-davos-at-white-harbor` | HIT (after switching kebab-form aliases to space-form) |
| `arrest of the Sand Snakes` | `arrest-of-the-sand-snakes` | HIT |
| `Execution of the Blackwater deserters` | `execution-of-the-blackwater-deserters` | HIT |

10/10 HIT after the kebab-vs-space alias fix (see "Surprise" below).

**`--neighbors` probes** for each renamed slug — all 9 renamed events show their expected role-edge sets attached (AGENT_IN / COMMANDS_IN / VICTIM_IN / WIELDED_IN / LOCATED_AT). No orphan edges introduced. `--health` clean.

**Final residual grep:** `grep -r '<old-slug>' graph/ | grep -v _regrounding` returns only the deliberate old-slug-as-alias entries for each of the 9 renamed slugs. Zero unintended residuals.

**Alias lookup stats post-rebuild:**
- Unambiguous lookups: 876 → **922** (+46 from new frontmatter aliases)
- Ambiguous collisions: **1** (pre-existing `conquest-of-dorne` vs `the-conquest-of-dorne` — NOT introduced by S91; flagged as separate cleanup item)
- Source breakdown: node-frontmatter-alias 67, node-name 583, node-slug 583, wiki-canonical-name 355, wiki-redirect 176, wiki-slug-self 371

## Deferred to next session

Two of the 5 ambiguous flagged decisions are **structural restructures** (not rename-only). Full subagent decision packets reproduced verbatim into:

→ `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md`

1. **`lord-wyman-orders-execution` arc** — subagent rec: new parent `wyman-manderly-stages-fake-execution-of-davos` (type=event.deception), SUB_BEAT_OF link from this + the renamed `wyman-publicly-arrests-davos-at-white-harbor`, DECEIVES + SECRETLY_ALLIED_WITH edges, possible new `execution-of-davos-lookalike-at-white-harbor` node for the substitute criminal. Open Q for Matt: type of new parent + how to handle the unnamed substitute.
2. **`jaime-sheathes-his-sword-but-orders-ned-s-men-killed` arc** — subagent rec: consolidate with sibling `jaime-lannister-ambushes-ned-s-party` under a new parent `attack-on-ned-stark-in-the-streets-of-kings-landing` (type=event.battle), DECEIVES edge for the sheathes-sword-while-ordering-kill act, RELATED_TO link to existing `cersei-claims-ned-s-men-attacked-first` (downstream deception). Open Q for Matt: merge vs SUB_BEAT_OF. **Chronology confirmed:** AGOT Eddard IX (NOT X as the prompt initially guessed); IS Jaime's retaliation for Catelyn-captures-Tyrion; IS before Ned's arrest (Ned wounded here, arrest comes in Eddard XIV).

## Surprise — alias resolver doesn't auto-convert kebab to spaces

The `event_alias_resolver.py` normalize function lowercases + strips leading "the/a/an" + collapses whitespace. **It does NOT convert hyphens to spaces.** So a kebab-form alias like `the-staged-arrest-of-the-onion-knight` only resolves when queried in kebab form — natural-language queries miss.

Caught mid-session when Wyman-arrest's 4 subagent-recommended aliases (all kebab) failed the spot-test. Fixed by rewriting Wyman-arrest aliases to space-form (`"Wyman Manderly arrests Davos"` etc.). Same fix applied to Qhorin/Ygritte aliases.

**Lesson:** subagents proposing aliases default to kebab when the slug is kebab. Bug-1-style workaround note in next continue prompt: always use space-form for natural-phrase aliases; only the old-slug back-compat entry should be kebab.

## What's strange (for Matt to look at twice)

1. **`jon-spares-ygritte.node.md`** still has `type: event.execution` — misleading because the execution doesn't happen. Flagged in body-prose; type-field review queued for Plate 5 typing pass per subagent C report.
2. **`cersei-s-plot-to-assassinate-jon-snow.node.md`** still has `type: event.death` — misleading because Jon doesn't die. Same flag, same queue.
3. **Auto-derived name `"Cersei S Plot to Assassinate Jon Snow"`** had a bad apostrophe-handling. Manually corrected to `"Cersei's Plot to Assassinate Jon Snow"` in frontmatter. The `slug_to_name()` function in `rename-event-node.py` doesn't handle `-s-` infix → `'s` conversion. Minor script-hardening candidate.
4. **`execution-of-the-blackwater-deserters` has only 2 edge-types attached (COMMANDS_IN + AGENT_IN)** — no VICTIM_IN edge currently exists. The "Blackwater deserters" are not modeled as a victim entity. Subagent A flagged this as a gap surfaced by the rename. Candidate for a future event-victim-group node mint (or leave as nameless plural).
5. **Plate 3 "minted-plate3" status field is stale** on all 9 renamed nodes — the body says "Staging only — do NOT promote" but the edges have `plate5_merged_at` timestamps confirming Plate 5 merge happened. Subagent A flagged this: rename script doesn't auto-flip status. Cleanup pass needed.
6. **1 pre-existing ambiguous alias-resolver collision:** `conquest-of-dorne` exists as both `conquest-of-dorne` and `the-conquest-of-dorne` — duplicate node. Flagged as separate cleanup item; NOT introduced by S91.
7. **Cersei-claims-Ned's-men-attacked-first** — subagent C and the Jaime-sheathes subagent BOTH independently flagged this as a downstream DECEIVES candidate (Cersei → Robert, false-claim-about-instigator). Not minted this session (the slug isn't being renamed); queued as a curator-pilot follow-on.

## Files touched

### graph/ (canonical writes)
- `graph/nodes/events/` — 9 file renames (Sand Snakes, Slynt, Dontos, Symon, Kerwin, Blackwater deserters, Jon spares Ygritte, Cersei-Osney plot, Wyman-arrest) + 1 aliases-only edit (Ned-Slynt) + 1 sibling aliases-only edit (gold-cloaks-betray-ned)
- `graph/edges/edges.jsonl` — atomic field updates across 29 edge rows (5+5+3+4+3+2+5+3+3 = 33 edge rows touched by rename script across the 9 applies; 3 plate5_superseded_note fields manually patched in Python afterward); +3 new curator-pilot edge rows appended

### Reference / index rebuilds
- `graph/index/events/` — rebuilt via `scripts/build-entity-indexes.py --type events --all`
- `working/wiki/data/event-alias-lookup.json` — rebuilt via `scripts/event_alias_resolver.py --build` (876 → 922 phrases)

### Continue-prompts + worklog + session-results
- NEW `progress/continue-prompts/2026-06-12-deferred-structural-restructures.md` — fully self-contained, reproduces both subagent decision packets verbatim with open questions enumerated for Matt
- `worklog.md` — archived S86, added S91 entry
- `history/worklog-archives/archive018.md` — S86 appended (now 5/5)
- NEW `working/session-results/2026-06-11-rename-execution.md` (this file)

## Hard rules respected

- ✅ Re-ran `--dry-run` before every `--apply`
- ✅ Did NOT auto-/endsession (this is just the session-results writeup; Matt grants /endsession explicitly)
- ✅ Did NOT proceed to Phase 2 Mode 3 dip in this session (still queued via `2026-06-11-phase2-mode3-dip.md`)
- ✅ All aliases used INLINE form (Bug 1 workaround)
- ✅ Body-text + plate5_superseded_note free-text patched per rename (Bug 3 workaround — 3 plate5_superseded_note hits across the 9 renames)
- ✅ Subagent decision packets surfaced for Matt's review for structural restructures (not auto-applied)
