# Advisory board — `read_passage` to the public chat? (design.md §8, fork 1)

Board convened per design.md §5 session-C fan-out / §8. Single-agent internal deliberation,
four advisors. Read: design.md §3 D-C + D-D + §5 step-5e; `web/README.md`; `DEPLOY.md`;
`web/netlify/edge-functions/lib/agent.ts` (the cite gate). Publishing/copyright is SETTLED
and out of scope for this board — the question here is a product/abuse-exposure question,
not a legal one.

## Decision

**CLI-ONLY for now.** `corpus-search` over `sources/chapters/` (grep-class, chapter:line
cites) ships CLI/in-repo this session per step 5e. The edge-side `read_passage` (static-asset
fetch of chapter files, serving verbatim passages through the public chat) stays **designed,
not shipped** — gated on a concrete condition below, not on a vibe.

## Rationale (5 lines)

1. The public chat's whole shippability rests on a deliberately small, curated, non-
   reconstructable evidence surface (6,053 quotes across 1,595 nodes) — `read_passage` swaps
   that for "fetch any chapter, any span, on request," a categorically different exposure than
   the essential-shrink the chat was designed around (D-D).
2. Full book text is only ~11 MB across 344 chapters; nothing in `chat.ts` today bounds
   *volume of verbatim text served per session/day* (the spend cap bounds dollars, the cite
   gate bounds fabrication — neither bounds extraction-by-iteration), so shipping this without
   a quota is shipping a full-text extraction oracle to anonymous users.
3. Engineering is not the blocker: static-asset serving (network I/O outside the Edge 50 ms
   CPU budget) is cheap and the cite gate already generalizes — a `read_passage` result would
   carry a real `chapter:line` ref, harvestable by `harvestResult` exactly like a quote cite,
   same as the G9 per-node-asset pattern already designed for `narrative_arc`.
4. The researcher archetype this Track cares about (design.md §2d) already gets full-text
   reach via CLI `corpus-search` — the users who most need passage-level recall are in-repo
   sessions with full profile access; the public chat's anonymous researcher is a different,
   higher-risk consumer of the same capability.
5. This Track's job is query-surface plumbing with a documented profile split (full vs
   bounded), not a new public-product abuse-guardrail design (rate limits, per-session/day
   text-volume quotas, extraction-pattern monitoring) — none of which exist yet and none of
   which this Track owns; bundling that decision into step 5e either rushes it unguarded or
   blocks the Track on unrelated infra.

## Advisor positions

- **Researcher user:** genuinely wants this — passage access answers "what does the text
  actually say around X," not just a pre-selected highlight. But notes the CLI ships the same
  underlying capability today, just not to the anonymous public surface; the researcher who
  needs it most (deep textual work) is better served working in-repo anyway.
- **Safety/abuse lens:** hard no *as currently bounded*. The ≥2-quote floor and 6-iteration
  cap were sized around curated-quote grounding, not full-chapter fetch; extended across
  unlimited turns/sessions from one visitor, `read_passage` is a slow but complete book-text
  extraction path. Wants a concrete quota mechanism before this ships, not "the cite gate
  covers it" (the cite gate verifies truthfulness, not volume).
- **Engineer:** no architectural objection — static-asset fetch is the right mechanism
  (matches the G9 fallback design), cite-gate integration is a few lines. Flags that
  `read_passage` results are much larger than a quote (full paragraphs/pages vs a dozen
  words), which touches per-turn token cost and context budget, not just abuse surface —
  worth measuring before it ships even under a gate.
- **Scope-discipline lens:** keep it out of this Track's shipped scope. `corpus-search`
  (CLI) is the step-5e deliverable and satisfies the design intent S172 named. `read_passage`
  is correctly *designed* here (mechanism, cite-gate compatibility) but shipping it is a
  product decision gated on infrastructure (quotas, monitoring) this Track doesn't build.

## Dissents

- Researcher lens dissents partially: would prefer a narrowly-scoped middle ground — e.g. a
  `read_passage` capped to a small fixed span (a handful of lines around a cite, not a whole
  chapter) — rather than waiting on full quota infrastructure. Not adopted as the decision
  because it still needs the same missing guardrail work (even a small span, repeated across
  enough turns, reconstructs a chapter) and because no one has scoped what "small" means yet.
- No advisor dissents from keeping this out of step 5e's shipped surface.

## The condition that would flip it

Ship `read_passage` to the public chat only once **both** of the following exist:
1. A concrete per-session (or per-day-per-visitor) cap on verbatim text volume served by
   `read_passage` — a quota mechanism, not just the existing dollar spend cap — designed and
   Matt-approved as its own small feature (belongs to the chat-UI/product track, not
   query-layer).
2. A measured per-turn cost/context impact from a smoke test (a handful of live
   `read_passage` calls through `weirwood-live`, never prod) showing it doesn't blow the
   token/cost budget the way `narrative_arc` inlining was measured for G9.

Until both land, `read_passage` stays a designed-but-gated mechanism (fetch chapter file as
static asset, harvest its `chapter:line` ref into `validCites` exactly like a quote). Revisit
this fork after those two pieces exist, not on a timer.
