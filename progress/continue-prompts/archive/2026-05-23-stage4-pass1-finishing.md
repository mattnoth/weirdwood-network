# Stage 4 Pass-1-derived — finishing work (post-tail cleanup + resolver levers + merge)

> **Recommended model:** **Sonnet 4.6** for the deterministic cleanup/dedup/merge (Tracks 2–4). **Opus 4.7** only for the Track-1 resolver-lever *decision review* (not per-item work). Do NOT use Opus for bulk edits.
> **Trust worklog.md over this prompt if they differ** (CLAUDE.md #9). Authoritative state: worklog Session 67 + the Stage 4 Current-State line.

## Where things stand (end of Session 67, 2026-05-23)
Stage 4 Pass-1-derived edges now total **5,219 book-pass1 edges**:
- **2,834 deterministic** (`typed_by: python-map`) — `working/wiki/pass2-buckets/pass1-derived/{book}/*.edges.jsonl`. Regenerate: `python3 scripts/stage4-pass1-edge-candidates.py --apply && python3 scripts/stage4-pass1-evidence-locator.py --apply`.
- **2,385 LLM-tail** (`typed_by: sonnet`) — `working/wiki/pass2-buckets/pass1-derived/_tail-typed/{book}/*.edges.jsonl`. Regenerate: `python3 scripts/stage4-tail-classifier.py --apply` (Sonnet via `claude -p`, ~$21, ~2h; or `--book <b>` to parallelize, or `--smoke N` to test). 667 rejected in `_tail-typed/{book}/*.rejected.jsonl`.
- All output is **gitignored/regenerable**. 350 tests green (`python3 -m unittest discover tests`).
- **Everything from S67 is UNCOMMITTED** — first decide whether to commit (ask Matt). Matt has been checkpointing via his own `wip` commits.

## Open questions for Matt (decide before/at start)
- **Commit S67's work?** (scripts + 133 stamped comention files + supplementary-aliases.json + regenerated audit reports + worklog/session-067/continue-prompts/todos.)
- **Approve the 2 resolver levers** (Track 1)? Both change core resolution semantics — his "how aggressive" call.
- Throwaway `classify_*` scripts cleanup is still **ON HOLD** (his choice, S66).

## Tracks (1 needs Matt; 2–5 deterministic, no permission)

### Track 1 — Resolver levers (MATT DECIDES; measured in S67, NOT implemented)
Over 651 ambiguous endpoints in `working/wiki/data/pass1-derived-ambiguous-review.md`:
- **Full-surname rung (~72, ~11%, high-confidence):** "Ser Rodrik **Cassel**" lands ambiguous across 5 `rodrik-*` though `rodrik-cassel` is in the candidate set — the resolver uses only the first non-title token and discards the surname. Add a rung in `scripts/stage4_name_resolver.py`: if `to_slug(title-stripped raw)` exactly equals one candidate slug, take it. Strictly more-correct, low risk. Add tests + spot-audit. Recovers Ser Rodrik Cassel (many), Brynden Tully, Jason Mallister, Donnel Waynwood, …
- **Index-pollution filter (~417, ~64%, clears NOISE):** collective/generic cells collide with non-person nodes sharing a leading common word ("The council"/"The Kingsguard" → songs/texts `the-book-of-holy-prayer`; "Golden face" → `golden-skulls`; "House Stark / Eddard Stark" → `house-hornwood`). Fix: exclude non-person node types (text/song/place/house/event) from firstname candidates, OR extend the leading-common-word stoplist. Same disease as the type-contract violations below. Makes `ambiguous-review.md` actually reviewable (~234 genuine endpoints).
After either lever: re-run the two spine `--apply` scripts + spot-audit new resolutions (green tests did NOT catch the S66/S67 misresolution bugs).

### Track 2 — Tail-violation cleanup (deterministic). 21/2,385 (0.88%) from the validator:
- **6× `HOLDS_TITLE → place`** (model maps "Lord of <seat>" to a place target): deterministically re-type to the correct seat/rule relationship, OR drop. Systematic.
- **4× `ENCOUNTERS` verb-gate-failure** (no whitelisted staging verb): the tail prompt in `scripts/stage4-tail-classifier.py` OMITS the S61/S63 Rule-6 ENCOUNTERS gate — add that constraint to the prompt before any re-run, and drop/repair the 4 existing.
- **1× `SPOUSE_OF` qualifier `'claimed'`** (Ramsay→fake-Arya): not in enum — re-map to `current`/`unknown`.
- **~6 wrong-TARGET-NODE-type** (`GUARDS→place`, `MEMBER_OF→character`, `WORSHIPS→godswood`, `CLERGY_OF→house-of-black-and-white`, `princess-myrcella` typed `object.artifact`): these are **graph node-typing bugs**, edges are semantically correct — fix the node types in `graph/nodes/`, not the edges.
  Get the live list: `python3 scripts/wiki-pass2-validate-edge-jsonl.py --file <concat of _tail-typed/**/*.edges.jsonl>`.

### Track 3 — Tail dedup (deterministic)
The spine emits some duplicate rows (e.g. `arya-stark SIBLING_OF sansa-stark` ×2, same chapter+quote) → duplicate edges in `_tail-typed/`. Dedup on (source_slug, target_slug, edge_type, evidence_chapter) — keep one. Decide whether to dedup the deterministic spine too.

### Track 4 — Merge `_tail-typed/` into the main book-pass1 edge set (deterministic)
Combine the 2,834 `python-map` + 2,385 `sonnet` edges into the canonical per-chapter edge files (or a single merged set), preserving `typed_by` provenance. This is the step that makes the 5,219 edges queryable as one set. Decide target location with Matt (likely promote into `graph/edges/` — but check architecture.md for the edge-file convention first; Stage 4 edges have not yet been promoted to `graph/edges/`).

### Track 5 — (optional) First-class `book-pass1` validator schema
`scripts/wiki-pass2-validate-edge-jsonl.py` validates book-pass1 edges only via the `(emit_edge, pass1_relationship)` contract path. Add a proper `evidence_kind: book-pass1` branch validating `evidence_chapter`/`evidence_quote`/`evidence_ref`/`hint_raw`/`source_resolution_status` directly. Low priority.

## DO NOT
- Mutate `working/wiki/data/alias-resolver.json` (use `pass1-derived-supplementary-aliases.json` for additive aliases).
- Re-launch the wiki chapter-summary comention bulk (DEPRECATED; the 133 files are stamped `superseded`).
- Use Opus for bulk edits or per-item typing. Refetch wiki. Run `/endsession` without explicit permission.
- Trust green tests as correctness proof on resolution/typing output — spot-audit random samples.
- Re-run the LLM tail without adding the ENCOUNTERS Rule-6 gate to the prompt first (else it re-emits the 4 verb-gate failures).
