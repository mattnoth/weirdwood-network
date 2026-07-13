# R+L=J cluster — S216 staging review record (2026-07-13)

**Session:** S216 (theories staging review — the validation Matt required in S214).
**Model:** Fable orchestrator + fresh Sonnet adversarial pressure-tester.
**Graph mutation: NO.** All edits confined to `working/theories/rlj-cluster/` staging
files + `working/harvest-queue.md`. Cluster remains AT THE MINT GATE — no mint
without Matt's explicit go (S214 standing).

## Matt's adjudications (the 5 queued S214 questions — all settled)

| question | decision |
|---|---|
| S214 convention set (node-per-canonical-theory · evidence→theory SUPPORTS/CONTRADICTS w/ byte-verified quotes · claim: frontmatter · ungrounded domain-labelled in body, never edges · umbrella "X/Theories" stubs stay dark unless they ARE the canonical theory) | **RATIFIED as-is** |
| Per-edge tier variance (T6 tier-4 under a tier-3 node) | **RATIFIED** (part of the set) |
| CITED_BY / out-of-world source node type | **STAYS DEFERRED** — provenance in frontmatter (`video_sources`/`origin`); revisit only if a real query needs source→theory traversal |
| KotLT display name | **RENAME DISPLAY ONLY** → `name: "Lyanna was the Knight of the Laughing Tree"`; slug/wiki_source unchanged; alias "Knight of the Laughing Tree theory" added (applied this session) |
| Chat exposure of the theory layer | **DEFERRED — explicitly OPEN** in worklog Active Decisions; guardrail untouched; decide when the layer is minted and stable |

## Pressure-test (Matt's picked validation): BLOCK → repaired → CLEAR-WITH-NOTES

Fresh Sonnet adversarial agent, no prior context, read-only, byte-checked **all 13
edge quotes + 8 body cites** (all verbatim at cited lines — zero fabrication).
Initial verdict **BLOCK** on 4 MAJOR + 3 MINOR prose findings; orchestrator repaired
all 7 in the staged files; same agent re-verified **7/7 PASS, no new leaks → FINAL
CLEAR-WITH-NOTES** (full end-to-end re-read of both files).

Repairs applied (staging files only):
1. R+L=J `## Claim` no longer states the theory as fact — opens "The theory holds that…".
2. "Jon's true identity" → "the parentage the theory proposes".
3. GRRM-interview sentence moved from `## Status Notes` into `## Ungrounded material`
   as a **GRRM-interview** bullet; Status Notes now labels the show outcome as the
   basis for `status: show-confirmed` and points at the fenced **show** entries.
4. Cherry-picked `agot-eddard-12.md:127` "list that excludes Jon" citation **dropped**
   (the full source line names Jon in the very next clause).
5. Fourteen-year-lie lead-in re-attributed: the Jon-age link is the theory's note,
   not the narration's.
6. KotLT genre-reasoning counter-argument moved to `## Ungrounded material`
   (**community** bullet); Evidence Against keeps a one-line pointer.
7. Crypt-statue passage: quote marks removed from the narration sentence
   (only "Promise me, Ned" is speech), parenthetical added.

Accepted caveats (documented, no file change):
- **T7 scoping** — the CONTRADICTS edge targets the whole theory node while the
  vow-contradicts-throne-claim-only scoping lives in the edge `note`. Downstream
  surfaces that render CONTRADICTS should carry note text. (Schema change declined.)
- **she-wolf = Lyanna** decode unhedged in KotLT prose — near-universal, textually
  unambiguous background; the contested claim (she-wolf = mystery knight) IS hedged.
- ASX-verdict paragraphs report the videos' own stance as *their* verdict, not the node's.

## Gates (re-run fresh this session, post-repair)

- `quotecheck_enrichment.py` → **13/13 ALL FOUND** (edges untouched by prose repairs)
- all 9 edge-source slugs resolve to live node files
- tier audit: no tier-1/2 anywhere in staged artifacts (node tier-3 ×2; edges 12×tier-3 + 1×tier-4)

## Structural observation (recorded, no action — Matt ratified conventions as-is)

The live graph carries THREE KotLT nodes: the theories stub (this enrich target),
`events/knight-of-the-laughing-tree-incident` (tier-1, S133, role edges incl.
`lyanna-stark SUSPECTED_OF …-incident` tier-2), and `characters/knight-of-the-laughing-tree`
(wiki persona node). The staged theory node has **no edge to the incident node it is
about** (a possible future "subject-link" convention — offered S216, not adopted).
The tier-2 in-world SUSPECTED_OF vs. tier-3 fan-theory node coexistence is deliberate:
different registers (in-world suspicion vs. out-of-world theory).

## Residue notes

- The continue prompt's "`--nodes-root` fix needed" line is **stale** — the flag
  landed in the S214 endsession commit (`0685bbf49f`) and is wired through
  `load_node_specs`. Validation dry-runs can no longer write nodes into the live graph.
- 3 pressure-test harvest pointers appended to `working/harvest-queue.md` (S216
  pressure-test origin) — 2 of the agent's cites line-checked + corrected before
  append (186→191, 114-116→117).

## Mint gate (unchanged)

On Matt's explicit go: `scripts/mint_enrichment.py --candidates
working/theories/rlj-cluster/candidates.json --nodes-dir working/theories/rlj-cluster/nodes`
+ apply `enrich/knight-of-the-laughing-tree-theories.node.md` over the stub +
`weirwood refresh` + architecture.md sync (new `concept.theory` frontmatter fields:
`claim`, `status` [open | show-confirmed | jossed], `origin`, `video_sources`,
`pass_origin` — per orchestration rule 6).
