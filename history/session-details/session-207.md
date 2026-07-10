---
session: 207
date: 2026-07-10
track: graph
model: Sonnet 4.6 (orchestrator; deterministic scripts + one schema design call + a read-only de-risk)
graph_mutation: "YES — node type retypes + quote-section merges; edges untouched (25,313)"
---

# Session 207 — Graph vocabulary / schema hygiene (event schema-drift + quote dedup)

## Purpose

Execute the `graph-vocab-hygiene` continue prompt. Two jobs were queued: **Part A** — the
systemic **F&B event schema-drift** found in S206 (marquee mistypes + ~20 off-schema `event.*`
subtypes not in `architecture.md`); **Part B** — the Matt-sequenced **edge-vocab retrofit**
(KNIGHTED_BY / role edges / SUSPECTED_OF). Part A was the concrete, gated deliverable. Matt then
steered the remaining budget to a deterministic backlog win (the S205 dup-`## Quotes` dedup) and
re-oriented the roadmap onto the **F&B review-bucket triage** as the next major track.

## Part A — event schema-drift (the design fork)

The audit found the drift was **bigger than the continue prompt flagged**:
- **347 off-schema event nodes** (subtype not in architecture.md's 16-row Type Reference Table),
  led by `event.death` ×141, `capture` ×42, `other` ×35, `ceremony` ×24, `decree` ×10, `council` ×9.
- **~28 `event.war` mistyped as `event.battle`** — a *separate* straight-wrong category (event.war
  is already sanctioned): Robert's Rebellion, the Dance of the Dragons, Aegon's Conquest, all four
  Blackfyre Rebellions, most Dornish/turtle/spice wars.

**Key finding that shaped the disposition:** `event.death` is **already referenced normatively** in
architecture.md — the `SUSPECTED_OF` row (line 419) says an unproven killing "stays `event.death`,
not `event.assassination`." So the schema already treats it as canonical; it just never got a table
row. That made *sanctioning* death (not retyping it away) the schema-consistent move.

**The fork presented to Matt (AskUserQuestion):** (a) sanction most, (b) retype all down to the 16
leaves, (c) **hybrid** — sanction the high-count justified ones, retype the tail. **Matt chose (c)**,
and separately chose to fix the 25 clean war-mistypes → war while holding 4 for review.

**Sanctioned 5** into the Type Reference Table (+ worklog Active Decision, CLAUDE.md rule #6 lockstep):
`event.death` (141), `event.capture` (43), `event.ceremony` (27), `event.decree` (11),
`event.council` (10). (Note: an S199 todo had already flagged 4 of these as undocumented — now closed.)

**Retype (deterministic, `scripts/s207-event-retype.py`):**
- Off-schema tail → existing leaves: `other`(35) + the long singleton tail → `incident`; clean 1:1s
  `marriage`→wedding, `siege`/`raid`/`occupation`→battle, `assassination_attempt`→assassination,
  `banishment`→exile, `succession`→investiture, `funeral`→ceremony, `reform`→decree,
  `imprisonment`→capture, `coming-of-age`→ceremony.
- **26 war-mistypes** `event.battle`→`event.war` (25 clean + `anarchy-in-the-reach`, whose own prose
  says "an open war of succession").
- **3 held nodes → incident** (Matt-dispositioned, text-grounded): `great-spring-sickness` (a plague,
  no `disaster` type sanctioned), `hour-of-the-wolf` (post-Dance reckoning period), `lysene-spring`
  (Lysene captivity interlude).
- The script also rewrites the auto-stub prose line ("is a event.X from the AWOIAF wiki") to stay
  consistent with the retyped frontmatter.

**Result:** 139 event nodes retyped; **0 off-schema subtypes remain**; all 21 live event.* types are
now within the sanctioned set of 21. `_summary.json` reconciles exactly (war 30→56, battle 288→263,
incident 170→269).

**Surgical index revert (S206 recipe).** `weirwood refresh` rebuilt all derived artifacts (8,566
files changed, mostly `generated_at`-only churn). The retype only meaningfully changed the **events
index** (per-node `type` + `_summary.json` counts). Discriminator care was needed: (1) the 112 retyped
*source* node files with a lone `type:` change have the same `1 1` numstat as timestamp churn, so
`graph/nodes/**` was excluded from the revert; (2) minified single-line derived JSONs (search-index)
show `1 1` even for real changes — checked their content diffs directly (the deployed
`web/data/search-index.json` was unchanged, confirming the retype doesn't touch search). Reverted
8,285 timestamp-only derived files; kept 140 events-index + architecture.md + the 139 source nodes.

## Bonus — dup-`## Quotes` dedup (S205 backlog)

84 nodes carried two `## Quotes` sections. Confirmed the loader is **last-wins**
(`split_sections` dict-overwrite), so the bundle rendered only *one* section and dropped the other;
`## Quotes (continued)` (1 node, robb-weds-jeyne-westerling) became a never-read key. Also: `parse_quotes`
only renders `>`-blockquote style, so wiki-plain-line "quotes" don't render regardless (dedup there is
pure file hygiene, non-breaking).

`scripts/s207-dedup-quotes-headers.py` merges all `## Quotes` sections into one via **line-level union**
(dedup non-blank lines by normalized text, preserve order + blank structure), with a per-file data-loss
guard. Validated against the real loader: **+29 previously-hidden quotes surfaced across 15 nodes, 0
regressions** (every currently-rendered quote is a subset of the post-merge render). 39 exact-dup (2nd
copy dropped) + 45 union-merge. 0 nodes with 2+ Quotes headers remain.

## Review-bucket triage — orientation + de-risk

Matt (getting his bearings, queued messages) surfaced the **F&B review-bucket triage** as the biggest
genuinely-open piece. Read the [S203 plan](../../working/fire-and-blood/apply/REVIEW-BUCKET-TRIAGE-PLAN-s203.md):
1,440 quarantined `reconcile-review` rows from the bulk apply. The content payload is the
**second deferred-events vein** — `event-dedup-risk` (221) + `composite-name` (57) = real missing canon
(Death of Queen Helaena, Dance principals' births, Battle of the Stepstones, Betrothal of Aegon III &
Daenaera). Plus `unresolved-status` (929 → head-map recovers ~514) and `no-decisive-margin` (172).

**De-risk (read-only) of the plan's open mechanics question:** `fab-reconcile-candidates.py` has a
`--redirect-map`, but it is **slug→slug** (applied *after* a slug is found, line 1087) — NOT a raw
name→slug override for the unresolved names. The reconciler resolves names via **clusters + the alias
resolver**, so recovery doesn't need a new override arg: add missing names as node `aliases:`/cluster
entries (or mint nodes for genuinely-missing events) → `weirwood refresh` → re-run. **The real open
question is re-injection idempotency** — re-running a unit re-processes *all* its rows, so the triage
session must first confirm the `mint_enrichment` P4 dedup guard makes re-runs safe (or add a
`--only-names` filter). This goes at the top of the triage continue prompt.

## Matt's steer (captured to todos)

- `event.betrothal` (and "might be worth the betrays part" too) may deserve their own types after all —
  currently folded into `incident`. **Decide when the review-bucket betrothals land** (volume-driven),
  then **retrofit** the S207-folded nodes up.
- **Edge-vocab retrofit is confirmed wanted** ("edges need retrofit as well") — deferred behind the
  review-bucket triage, not dropped.
- **Node-type promotion sweep** — Part A was conservative (ambiguous → incident); a follow-on should
  promote `death-of-*`/`arrest-of-*`/etc. up to the specific leaves.

## Gate

pytest **1457 passed** (1 skipped) · deno **100 passed** · 0 off-schema event subtypes · 0 dup Quotes
headers. Edges untouched (25,313); event nodes 1,032 (retyped, not added). Harvest queue: 2 open
(the S206 pair, below the ~30 bar — no action). web/data bundle untouched (deploy Matt-gated).

## What's next

**F&B review-bucket triage** (S208) — the deferred-events vein first
(`event-dedup-risk` + `composite-name`, 278 rows). Then the node-type promotion sweep + edge-vocab
retrofit. Strip-boilerplate track still Matt-gated.
