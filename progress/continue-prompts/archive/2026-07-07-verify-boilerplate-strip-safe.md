# Fresh-eyes review: is the boilerplate-strip script safe to apply, and does it break Fire & Blood?

> **Track:** graph cleanup review (read-only audit — this is NOT the apply session).
> **Recommended model:** Sonnet. Deterministic verification + reading two design docs; no reasoning-heavy judgment calls beyond the one flagged below.
> **Gate:** this session is READ-ONLY. Do not write `graph/nodes/`, do not edit any script, do not run `--apply`. Produce a verdict + findings; Matt decides next steps.

## Why this session exists
The prior session built `scripts/strip-wiki-boilerplate.py` to remove the auto-generated `"<Name> is a <type> from the AWOIAF wiki."` Identity-line boilerplate that 6,711 nodes carry (dry-run report: `working/node-enrichment-wiki-prose/strip-boilerplate-dryrun.md`). Matt reviewed a 3-agent advisory board's recommendation and approved the approach. Before running `--apply` on the whole graph, Matt wants a **fresh, independent** session to (1) verify the script's logic is actually correct and safe, and (2) check whether it collides with the **parallel Fire & Blood (F&B) build track**, which is designed to also touch Identity lines on these same nodes.

## Decision already made (do not re-litigate — verify it was IMPLEMENTED correctly, that's it)
- **Rich nodes** (5,490 — have real content elsewhere in the body: `## Appearances`/`## Origins`/`## Narrative Arc`/`## Quotes`/`## Description`): strip only the `" from the AWOIAF wiki"` tail. Keep the type-gloss **exactly as-is, including raw dotted strings** like `character.human`, `organization.house`, `event.battle` — Matt explicitly said he likes this in-world/schema detail, do NOT humanize it. Result: `"House Warrick is a organization.house."`
- **Thin nodes** (1,221 — Identity + Edges only, nothing else in the body): **drop the boilerplate line entirely**, leaving the `## Identity` section present but empty. Board reasoning: a contentless one-liner ("Eon is a person.") is worse than an honest empty section — it fakes curation. Humanizing the gloss and an LLM composer pass for these 1,221 nodes are explicitly OUT OF SCOPE / deferred to a future track.
- Never touch `wiki_source`, `confidence`/tier, or `cite_refs`. This is a prose-only change.

## Step 1 — Verify the script itself
Read `scripts/strip-wiki-boilerplate.py` in full. Check:
1. **Regex correctness**: `BOILERPLATE_LINE_RE` and the rich/thin classifier (`RICH_SECTIONS_RE`). Run it in dry-run (default, no `--apply`) and inspect the full output, not just the printed sample — `python3 scripts/strip-wiki-boilerplate.py --sample 6711 > /tmp/full-dryrun.txt` and grep for anything that looks wrong (multi-line Identity paragraphs, nodes where the boilerplate sentence isn't the whole line, glosses with weird punctuation, the `unmatched` bucket should be 0).
2. **Blank-line cleanup on the thin-drop path** — confirm the regex collapse (`## Identity\n\n\n## Edges` → clean single blank line) doesn't mis-fire on any node whose body shape differs slightly (e.g. something between Identity and Edges, or a node where Edges section is itself empty/missing).
3. **Frontmatter is never touched** — spot check 5-10 files' frontmatter blocks before/after in a temp copy; confirm byte-identical except the body.
4. **Idempotency** — does running the script a second time after a first `--apply` correctly report 0 remaining matches (nothing double-stripped)? (You can test this on a scratch copy of a handful of files — do NOT apply to the real repo.)

## Step 2 — Verify it does not corrupt the Fire & Blood plan (the real risk)
Read `working/fire-and-blood/fire-and-blood-enrichment-design.md` (v2), specifically:
- **§ node shapes** (around line 42-44): F&B's reconciler/merge-writer classifies every node into exactly 3 shapes — (a) true stub = boilerplate Identity, no other prose; (b) rich wiki node = boilerplate Identity line **but** real prose below; (c) no-Identity node = no `## Identity` heading at all, body starts at `## Origins`.
- **§5.3 merge-writer spec** (around line 281): the NOT-YET-BUILT `fab_merge_node.py` is designed to detect boilerplate via the **exact regex** `^.+ is a [a-z][a-z.]* from the AWOIAF wiki\.$` and swap that one line for book-grounded prose. Real (non-boilerplate) Identity is left alone. No-Identity nodes get one inserted after frontmatter.

**The concern to verify:** after this strip runs,
- Rich nodes (shape b) no longer match `...from the AWOIAF wiki\.$` (the strip removed exactly that tail) — F&B's merge-writer would then treat them as "real Identity, skip the swap" and permanently leave the stripped one-liner (`"X is a organization.house."`) in place instead of ever replacing it with F&B book-grounded prose.
- Thin nodes (shape a) become a **4th, undesigned shape**: `## Identity` heading present but empty (not "no heading at all" like shape c, and not "boilerplate line present" like shape a). F&B's merge-writer has no branch for this.

Confirm or refute this reading. If confirmed, this is a real ordering/interface conflict between the two parallel tracks — not a reason to abandon either, but it means **one of these must happen before the strip is safe to apply globally**:
1. Sequence the tracks: F&B's merge-writer build + its first real run happens BEFORE the boilerplate strip is applied (so F&B still sees its 3 designed shapes), and the strip runs afterward on whatever nodes F&B didn't touch — OR
2. Patch F&B's `fab_merge_node.py` shape-detection (before it's built, so no rework needed) to also recognize: stripped-tail lines (`^.+ is an? [a-z][a-z.()\w\s,-]*\.$` without the wiki-tail, i.e. anything one-line under a certain length with no wiki-style cite markers) as "boilerplate-equivalent, swap it", and an empty `## Identity` section as "shape (c)-equivalent, insert into it" — OR
3. Some other reconciliation Matt prefers once he sees this laid out.

Do not pick one of these yourself — surface the conflict clearly with your confirmation/refutation of the reasoning above, and let Matt decide. If F&B's build (S198) has already progressed since this prompt was written, check `worklog.md`'s Session Log first — if `fab_merge_node.py` already exists, read its actual code instead of just the design doc, and check whether it was built to only match the literal wiki-tail regex or something broader.

## Step 3 — Report
Produce a short verdict: **GO** (script is correct + no F&B conflict, or conflict is fine because of X), **GO-WITH-CHANGES** (script needs a specific fix first — name it), or **NO-GO / SEQUENCE FIRST** (name what has to happen first, per the three options above or your own). Do not apply anything. Do not touch worklog.md's Session Log (that's the applying session's job) — this is a review-only session, note your findings in your reply to Matt, not in graph/worklog files, unless Matt asks you to persist them.

## DO NOT
- Do NOT run `--apply`.
- Do NOT edit `scripts/strip-wiki-boilerplate.py`, `fire-and-blood-enrichment-design.md`, or any node.
- Do NOT re-fetch the wiki.
- Do NOT auto-run `/endsession` (this is a sub-task review, not a full session close-out) unless Matt asks for one.
