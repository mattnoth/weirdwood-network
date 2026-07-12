---
session: 212
date: 2026-07-11
track: graph
model: Fable 5 orchestrator · Sonnet 4.6 proposers/builders · Haiku 4.5 fresh-verifiers
---

# Session 212 — Roles slice round 1 + save/export ship + UI polish + drain (autonomous multi-task)

## Shape of the session

Matt opened with the S211 roles-slice handoff but directed an orchestrator-with-subagents
session that would go beyond it, then stepped away mid-session with three escalating grants:
(1) "do not wait for me before minting — get a fresh sub agent [for review], I usually go
with your recommendation"; (2) pick further tasks from top recent items and continue;
(3) do the prod deploy without him. Everything below ran without further input.
**Process note for the record: this was a session-scoped grant, not a new default** — the
no-mutation-without-go rule stands; the substitute protocol used here (dry-run on scratch +
an adversarial fresh pressure-test subagent with explicit BLOCK authority) is the shape to
reuse WHEN Matt grants it.

## Task 1 — roles slice round 1 (the handoff)

The S211 machine, reused wholesale (scan → SHARED-RULES → proposers → VERIFY-RULES →
adjudicate → quotecheck → mint): script-builder regenerated the zero-role list from live
edges.jsonl (312; S211's 313 minus one absorbed), ranked deterministically
(degree·10 + quotes·5 + container-bonus + prose), built top-50 packets. 4 Sonnet proposers
(2×2 batches per the quota-headroom rule) → 244 candidates; 4 Haiku adversarial verifiers
→ 233C/5A/6P; adjudication dropped 8. The two catches worth remembering:

- **The verifier missed a harm-gate violation** (`lyanna VICTIM_IN abduction-of-lyanna`,
  node typed `event.incident`) that a deterministic post-verify audit caught — the audit
  (every kept VICTIM_IN's target subtype vs HARM_EVENT_SUBTYPES) is cheap and should be a
  standing step. The drop doubled as an honesty call: the `incident` typing reads as
  deliberate abduction-vs-elopement neutrality; VICTIM_IN would assert the contested side.
- **Two AMBIGUOUS quote upgrades beat re-litigating**: Renly/Robert war-COMMANDS_IN kept,
  quotes swapped for command-evidencing lines found by grep in minutes.

Mint +236 (edges 26,618), gate 4/4, pytest 1458, deno 100. Live probe: WO5K neighbors
returns all five kings COMMANDS_IN with verbatim quotes; Green Fork prose named both
command tiers, cite-check 10/10, $0.06. Remainder: 262 ranked events saved so round 2
never re-ranks; round-2 go is Matt's (value thins toward wiki stubs).

## Task 2 — chat save/export Phase 1 (Matt's same-day design doc)

Built exactly per `working/chat-save-export-design-2026-07-11.md` by one Sonnet builder;
only deviation: native `hidden` attribute over the sketched body-class (repo convention).
Verified by a 14-assertion test that extracts the REAL functions from app.js into a vm
sandbox (not a retyped copy — worth reusing as a pattern for testing unbundled browser JS),
plus a live local turn + prod DOM check. Phase 2 (print-PDF) untouched per the doc's
separate green-light.

## Task 3 — UI-polish pair (S210 board)

searchCard boilerplate gate landed as designed. The thin-node fix corrected the task's own
premise: dossiers never rendered connections for ANY node (`/api/node` returns
name/type/identity/quotes only; the neighbors rail card is chat-turn-driven) — so the fix
is the graceful placeholder, and chip-dimming is blocked on a bundle `thin` flag from the
node-bundle emitter (todos [LOW]).

## Close-out extras

- **generationCounts golden pin retired** after its 3rd benign prominence-reshuffle failure
  (this time from the new role edges) — implemented the S210 board's own recommendation
  instead of a 3rd repin.
- **Harvest drain 46→0** (the +29 roles pointers tripped the bar): Sonnet triage mapping
  every row to target/action/byte-copied quote, then 2 disjoint-dir attachers (characters |
  events+locations) — 22 attaches / 20 nodes / 15 already-present / 8 parked. The
  deterministic `verify_node_quotes.py` (1145/1145) both validated the drain AND surfaced
  that "straight-quote normalization" is the recurring cite-drift class: fixed the S145
  mormonts-raven dup, the osney spliced quote, and the fresh robb-stark attach — all the
  same disease. Attacher prompts should say "byte-copy, never normalize" louder.
- 3 prod deploys (`6a52de30`, `6a52e331`, `6a52e9a5`); commits `5d924945b8` → `223594a802`
  pushed.

## What Matt decides next

Roles round 2 (262 ranked, thinning) vs next enrichment vs remaining board items. Residues
filed in todos §S212: reyne-tarbeck Tytos/Tywin book-vs-wiki conflict · Tommard Heddle
sub-event candidate · riots-in-KL `event.battle` typing · aemond citation-upgrade ·
thin-chip bundle flag.

## Addendum — Matt's phone-testing round (post-endsession, 2026-07-11/12)

Matt tested on his phone and flagged two things + one fix. (1) *"What is the most vile
meal…"* hit the loop bound — the pulled log (`log/2026-07-12/1cf79a22…`, 9 tool calls,
$0.27) showed a GOOD walk spent inefficiently: two noisy broad searches, a
`resolve("Frey pie at Winterfell")` miss (aliases are article-prefixed plurals), then the
correct Frey-pies → Rat Cook trail bound-out just before composing. The sharper finding:
the agent never called the S190 `theme` tool — the tool built for exactly this question
shape. (2) The Save button wasn't visible on his phone even after a completed turn — the
hide-until-first-turn gate was suspect on `loop-bound-hit` turns; replaced with
always-visible + disabled-until-saveable (v197), verified at 375px. (3) Matt signed the
`MAX_TOOL_ITERATIONS` raise — first 7, then revised to **10** before execution — guard
test repinned with the sign-off recorded; he monitors spend (the $50/day cap backstops).
Open follow-ups live in todos §MATT-FLAGGED S212: the theme-routing SHARED_RULES row
(likely the higher-leverage fix), Frey-pie bare aliases, receipts dup-quote dedupe, and a
standing weird-walks log sweep.
