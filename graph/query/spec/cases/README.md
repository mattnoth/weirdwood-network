# Golden spec cases — schema

Part of the query-layer Track, step 1 (session A) — see `../operations.md`. These JSON
files are the **cross-language parity fixtures** (design doc D-B): the same case file is
meant to run under **both** `pytest` (Python engine, once it exists) and `deno test`
(`web/src/lib/spec_cases_test.ts`, live today). Divergence between implementations becomes
a red test, not silent drift.

One file per operation family: `resolve.json`, `neighbors.json`, `chain.json`,
`family.json`, `braid.json`, `search.json`, `list.json`, `theme.json`. Add new files as new
ops land — do not grow these into a junk drawer. (`corpus-search` and `mentions` have no
case file — both are CLI-only / live-data-only, no bounded-profile implementation to pin
against; see operations.md's own sections.)

## Case object shape

```jsonc
{
  "id": "resolve-red-wedding-exact",      // stable, kebab-case, unique within the file
  "op": "resolve",                         // one of: resolve | neighbors | chain | family
                                            //   (extend as new op families ship)
  "profile": "both",                       // "bounded" | "full" | "both"
  "input": { "phrase": "the Red Wedding" }, // op-specific args (see per-op shape below)
  "expect": {
    "mode": "exact",                       // "exact" = deep-equal a literal value/subset;
                                            // "invariant" = a named assertion set (below)
    // ...op-specific expected fields...
  },
  "note": "optional — cite the design-doc gap this pins (e.g. 'G19 — flips to hit after step 4')"
}
```

- **`profile`** governs which runner executes the case. `"bounded"` and `"both"` cases run
  under `deno test`. `"full"` and `"both"` cases run under the (optional) Python runner
  (`graph/query/spec/run_cases.py`) once a full-profile implementation for that op exists.
  A runner **skips** (does not fail) any case whose profile it doesn't serve.
- **`expect.mode`**:
  - `"exact"` — the actual op output, or a documented **subset of its fields**, must
    deep-equal `expect.value` (or the sibling expected fields alongside `mode`, for
    readability — see the case files; both patterns appear, the runner keys off whichever
    fields are present in `expect`).
  - `"invariant"` — for outputs too large/order-sensitive to dump wholesale (a family tree,
    a causal chain), assert **specific properties** instead of a full literal: ordered slug
    lists for a subset of the output, membership checks, counts, a truncation flag, a
    generation-count histogram. Each invariant case documents exactly which fields it
    checks in its `expect` block — there is no full dump to diff against.
- **`note`** is free text. Used here specifically to pin known-current-but-eventually-fixed
  behavior (the G19/G2 misses) so a future fix is an intentional, documented case update —
  not a silent "well the test still passes" accident. When a step's fix lands, update the
  case's `expect` AND its `note` (e.g. "G19 — fixed step 4a, 2026-0X-XX") in the same commit
  as the fix, per the design doc's drift-alarm intent.

## Per-op `input` / `expect` shapes used in this v1

- **resolve**: `input: {phrase}`. `expect` either a full `candidates` array (small result
  sets) or `top: {slug, matchType, ...}` + `candidateSlugs: [...]` for larger fuzzy sets
  (avoids over-pinning volatile low-rank fuzzy tail scores).
- **neighbors**: `input: {slug}`. `expect: {outgoingCount, incomingCount, hasOutgoingTypes:
  [...], hasIncomingTypes: [...]}` — invariant-mode; the full type/link dump is too large
  and too volatile (any new edge on Tywin changes counts) to pin exactly, so this asserts
  shape (counts + "these edge types must appear") not a byte-for-byte dump.
- **chain**: `input: {slug, maxDepth?}`. `expect: {upstreamOrder: [{source,edge_type,target,
  depth}...], downstreamOrder: [...], enablesCount, enables: [...]}` — the ordered link
  lists ARE asserted in full for the pivot case (it's small: ≤4 links per direction at
  default depth), because story-time ordering is exactly the behavior worth pinning
  (S185's regression class).
- **family**: `input: {slug, generationsUp?, generationsDown?}`. `expect:
  {root, rootName, memberCount, truncated, generationCounts? (optional; retired from the
  aegon case S212 — 3rd benign prominence-reshuffle failure, per the S210 board todo),
  mustInclude: [slug...], mustExclude: [slug...]}` — invariant-mode; a 96-member dynasty
  dump is not something to hand-maintain, so cases assert root/count/truncation +
  targeted membership checks instead.
- **theme**: `input: {name, category?}`. `expect` mostly invariant-mode (`mustIncludeSlug`,
  `memberCountAtLeast`, `themeNameEquals` for case-insensitivity, `allCategoriesEqual` for
  the category filter) since a theme's full member list (up to ~160 nodes) is not something
  to hand-maintain; one exact case pins the unknown-theme-name error path
  (`memberCount: 0, members: [], hasError: true`).

## Adding a case

1. Run the real TS lib against the real bundle (see the throwaway-script pattern used to
   generate this v1's cases — `deno run --allow-read <script>.ts` from `web/`, importing
   `web/src/lib/{data,resolve,graph}.ts` directly) to get the actual current output.
2. Trim to the smallest assertion that pins the behavior you care about (prefer invariant
   mode for anything order-sensitive-but-large or numerically volatile).
3. Add the case object to the right file. Keep `id`s unique within the file.
4. Run `cd web && deno task test` — it must stay green (or, if you're pinning a
   known-bad behavior, it should pass because you asserted the CURRENT bad output, not the
   fixed one).
