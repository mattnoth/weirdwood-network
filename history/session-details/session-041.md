---
session: 41
date: 2026-05-11
model: Opus 4.7 (1M context)
title: Per-character index roll-up + POV canonical resolution + missing-nodes audit
---

# Session 41 — Per-character index roll-up + missing-nodes audit (2026-05-11)

## Setting

The session opened on a `/continue 2026-05-11-per-character-index-rollup` invocation — a clean, well-scoped pure-Python task: build per-character index files at `graph/index/characters/<slug>.index.json` to mirror the per-chapter mention-index. The continue prompt had been written at the end of Session 40 with full schema, 4 lean-decisions-to-make, smoke-test guidance, and a "do not" list. Effort estimate: 30-60 minutes.

What actually unfolded was three distinct waves of work, each surfaced by Matt's questions during the build.

## Wave 1 — Per-character index, simple version

The continue prompt's four leans were all honored verbatim: (a) include all `character.*` types, (b) use `backlink-counts.json` for in-edge counts, (c) keep POV chapters separate from `mentioned_in`, (d) inherit alias resolution from the mention-index.

The script came together fast — pattern-matching `scripts/build-mention-index.py`'s frontmatter handling, slug computation, and per-book ordering. Output schema as proposed: `stats` block + `chapters.pov[]` + `chapters.mentioned_in[]`.

**One discovery surfaced during smoke testing:** ~200 year pages (`129-ac`, `100-ac`, etc.) were typed `character.human` by the Stage 3 deterministic emitter. On close audit only 10 of these slugs are in `graph/nodes/characters/` — most year pages never made it to graph at all. Per-character indexes emit faithfully for these 10 with 0 chapter mentions and a `year_pages_emitted_as_characters` count in `_summary.json` for discoverability. Added a todo capturing the underlying type-classification bug.

**Smoke-check results:** Eddard POV=15 ✓, Tyrion POV=47 ✓, Jon POV=42 ✓, Daenerys POV=31 ✓ — match canonical POV counts. Continue-prompt's "30-50 chapters mentioned in" estimate for Eddard was wrong — actual is 185 (Eddard referenced post-death throughout AFFC/ADWD). 18 POVs detected.

Initial commit `e737ba4e`.

## Wave 2 — POV canonical resolution (Matt's expansion)

Matt's question: *"can you resolve the aliases for character pov names? I guess important for the story to note when Sansa pov is Alayne, but why should they be separate?"*

The first-pass script resolved POV from the filename stem: `affc-alayne-01` → "alayne" → slug `alayne` (separate graph node from `sansa-stark`). Same for Reek/Theon and all the AFFC/ADWD descriptive-title chapters. 18 POVs detected, but with Alayne/Reek-as-separate and the descriptive-title chapters (The Prophet, The Captain of Guards, etc.) unresolved.

The fix path: parse each Pass 1 extraction's `pov_character:` frontmatter field. Pass 1 already encodes truename canonicalization there:
- `Alayne (Sansa Stark)` — truename in parens
- `Reek (Theon Greyjoy)`
- `Theon Greyjoy (as "The Turncloak" / "Reek")` — alias in parens, prefixed with "as "
- `Arya Stark (disguised as "Arry")` — alias in parens, "disguised" idiom
- `Aeron Greyjoy` — plain truename

A small `parse_pov_canonical()` distinguishes the two parenthetical idioms by checking whether the inside starts with "as " / " as " / "disguised". Then `to_kebab()` + an alias-resolver lookup + an honorific-strip fallback (`Maester Cressen` → `cressen`) + a mention-disambiguated prefix-match (`Catelyn` → `catelyn-stark` beats `catelyn-bracken` because catelyn-stark is in chapter's Characters Present).

**Identity-layer vs graph-layer separation locked in.** Alayne and Reek remain distinct graph nodes (POV=0 in their indexes after the change, but mentioned_in retained). The character index treats them as Sansa/Theon for retrieval. Graph-level merge (`SAME_AS` edges, node deletion/redirect) is Stage 4 work. The index doesn't need to wait for Stage 4 to apply identity reasoning.

**POV roster grew 18 → 30.** Quentyn 4 (Merchant's Man + Windblown + Spurned Suitor + Dragontamer), Barristan 4 (Discarded Knight + Queensguard + Kingbreaker + Queen's Hand), Victarion 4, Asha 4 (Kraken's Daughter + Wayward Bride + King's Prize + Sacrifice), Aeron 2 (Prophet + Drowned Man), Areo 2 (Captain of Guards + Watcher), Jon Connington 2 (Lost Lord + Griffin Reborn), Arianne 2 (Queenmaker + Princess in the Tower). Plus prologue/epilogue POVs: Will (agot), Chett (asos), Cressen (acok), Varamyr (adwd), Merrett Frey (asos), Kevan (adwd), Arys Oakheart (1 AFFC), Melisandre (1 ADWD).

**Catelyn POV regression:** initially 24, expected 25. Cause: `agot-catelyn-06` has `pov_character: Catelyn` (no surname). Kebab "catelyn" → not in graph (graph slug is `catelyn-stark`) → not in alias-resolver → prefix-match `catelyn-` matches BOTH `catelyn-bracken` and `catelyn-stark`. Disambiguated via Characters Present rows: `catelyn-stark` appears many times in `agot-catelyn-06`, `catelyn-bracken` doesn't → resolve to catelyn-stark.

**1 remaining unresolved POV after wave 2:** `affc-prologue pov_character='Pate'`.

## Wave 3 — Pate the Novice + missing-nodes audit

Matt: *"1 - and what would the node be? Are chapter summaries nodes? 2 - can you do this or not? 3 - so you wrote the script, and got the output, not just the output of smoke tests?"*

Then on follow-up: *"that works - a. but also, if we can catch any other pages that were missed, that would be good"*

**On (1):** Pate the Novice is a regular `character.human` like any other named character. Chapter summaries are NOT nodes in the current graph — chapters live as source markdown + Pass 1 extractions + per-chapter mention JSON, but no `.node.md` files. Whether chapters should be first-class nodes is an open Stage 4+ design question, not a current decision.

**On (2):** Yes — the wiki page is cached locally. Hand-craft from Pass 1's AFFC prologue extraction (which has rich content on Pate). Initially I assumed the Pass 2 deterministic emitter could be re-run scoped to this one page, but investigation revealed a different problem entirely.

**The case-collision discovery.** `sources/wiki/_raw/Pate_(Novice).json` is 909 bytes of pure redirect HTML: `<div class="redirectMsg"><p>Redirect to:</p><ul><li><a href="/index.php/Pate_(novice)" title="Pate (novice)">Pate (novice)</a></li></ul></div>`. The canonical Pate-the-novice content is nowhere on disk. Why? macOS HFS+ is case-insensitive. The wiki has `Pate_(Novice)` and `Pate_(novice)` as separate URLs — the former is a redirect on the wiki, the latter is canonical. Both URL fetches wrote to the SAME filename on disk; the redirect-content write happened last (or the canonical write was preempted by something), and only the redirect survived.

This pattern made me curious: is Pate alone? Or is it 5 cases? 50? I wrote a quick detection: count cached pages whose HTML starts with `<div class="redirectMsg">` AND whose redirect target differs from the page title only by case. **Answer: 125 cached pages are affected.** Sample: Children of the Forest, Free Folk, Red Priest, Valar Morghulis, House Words, Known World, Beyond the Wall (book), POV Character, plus 117 more. Major worldbuilding pages.

That's when the audit script (`scripts/audit-missing-nodes.py`) felt warranted. It also surfaced two parallel gaps:
- **138 Bucket A** — wiki pages that Pass 1 references but were never given a graph node. Top hits: `godswood` (36 Pass 1 mentions), `flea-bottom` (31), `old-gods` (22), `seastone-chair` (14), `chatayas-brothel` (12), `black-cells` (11), `queens-men` (9), `unsullied` (9), `cinnamon-wind` (8), `valyrian-steel-dagger` (8). These were likely categorized as `unknown` by Path B's categorizer.
- **83 Bucket B** — heavily wiki-backlinked but Pass 1 silent. Mostly D&E / historical figures.
- **949 Bucket C** — peripheral, defer.

Plus a separate prose-coverage finding from a quick audit: **5,975 of 7,583 graph nodes (79%) have stub-only Identity** (`"X is a character.human from the AWOIAF wiki."`). The Python prose extractor (`scripts/wiki-pass2-extract-prose.py`) ran for Tier-B in Stage 3a but most Path B promotions (Session 28-29) landed as skeletons-only. Re-running it would close most of the depth gap.

**Pate node hand-crafted** from Pass 1's `affc-prologue.extraction.md` — rich content on Pate the novice, his role tending Walgrave's ravens, his theft of the iron key, the exchange with "the alchemist," his death. Includes dual `KILLED_BY` edges (`alchemist` + `jaqen-hghar`) per memory rule `project_impersonation_edges_redirect.md`. Theory-relevant: Jaqen takes Pate's face and replaces him at the Citadel; this is the Faceless-Men-at-the-Citadel plotline.

**Alias-resolver bare-disambiguation tension.** With `pate-novice` added and aliases including "Pate", I re-ran `scripts/wiki-pass2-build-alias-resolver.py --apply`. Result: "Pate" → `pate-novice` was rejected by the bare-disambiguation filter (which fires when alias-as-prefix matches ≥3 canonical slugs — `pate-` matches 12 slugs). The filter is correctly conservative — "Pate" in any arbitrary Pass 1 mention could mean any of the 12 Pates — but it overcorrects for the case where only ONE node explicitly claims the alias. Compare to "Brienne" which survived the filter because only `brienne-tarth` exists with the `brienne-` prefix.

**Fix kept inside `build-character-indexes.py` rather than mutating the alias-resolver:** added a `raw_name_to_slugs` reverse map built from every character node's `name:` + `aliases:` frontmatter fields. When prefix-match returns multiple candidates, intersect with nodes that explicitly claim the raw name. For Pate POV "Pate": prefix_matches = 12 pate-* slugs, raw_name_to_slugs["Pate"] = {pate-novice} (only pate-novice declares it), intersection = {pate-novice}. ✓

**Final state of POV resolution:** 31/344 POVs detected, all 344 chapter POVs resolve cleanly, zero WARN.

## Matt's policy callout on refetching

When I described the case-collision fix path as "narrow exception refetch via cloudscraper," Matt pushed back hard: *"why do we need to refetch? because I thought I put some fucking HARD RULES that the SOURCE FOLDER has THE ENTIRE WIKI ALREADY. or is this about the footer bullshit"*

Correct framing. The hard rule holds: the wiki IS local; 17,657 files exist in `sources/wiki/_raw/`. The case-collision class is a DIFFERENT failure mode from refetching — it's content-corruption-on-disk caused by a crawl-time filesystem bug. The data isn't elsewhere; it's just wrong locally.

Three options surfaced:
1. **Accept the gap** — affected nodes stay skeleton-only. Rule wins cleanly.
2. **Reconstruct from cross-references** — for high-traffic case-collisions, plenty of other wiki pages quote and describe the entity. Free Folk has 141 backlinks; Children of the Forest has 51; Known World 42; Red Priest 40. No fetch, just synthesis from existing local data.
3. **Narrow-exception refetch** — only if (2) proves inadequate, and only with explicit per-use approval.

Matt's right that agents have repeatedly defaulted to "refetch" instead of "look harder at sources." This pattern needs to be guarded against. Option 2 is now the default for any case-collision work.

## Roadmap doc

Matt asked for a top-level reference doc capturing all queued work, sequencing, and concurrency analysis. Wrote `next.md` at the repo root, gitignored alongside `scratch`. Five tracks, parallel-safety table, sequencing decisions, long-term horizon. Not surfaced during /endsession (per Matt's instruction).

## Three commits

- `e737ba4e` — initial per-character index + first POV canonical-resolution pass
- `1e901d81` — Pate node + missing-nodes audit + the raw-name reverse-map fix
- `f71a74fe` — `.gitignore` add for `/next.md`

## What I didn't do

- **Cross-reference reconstruction for the 125 case-collisions.** Described it as the recommended default in next.md Track 4(a), but no actual reconstruction work was executed. The script doesn't exist yet; no Identity sections were synthesized.
- **Track 1 (wiki prose extraction backfill, 5,975 stub-only nodes).** Identified as the biggest-single-win track; queued as a HIGH todo.
- **Track 2 (138 Bucket A missing-node promotion).** Queued as HIGH.
- **Track 3 (per-LOCATION + per-ARTIFACT index roll-ups).** Queued.
- **Year-page type fix.** Queued (low-priority bundle with Stage 4 temporal edges).
- **Tests for `build-character-indexes.py`.** Matt and I agreed: premature. Schema still evolving. Better moment to lock down behavior is when the resolver code gets extracted into a shared module (Track 3 territory).

## Observations on agent self-correction

A pattern that worked well this session: when Matt's question implied my prior path was wrong, I traced back to the data rather than defending the previous answer. Wave 2 (POV canonicalization) and Wave 3 (the case-collision discovery beyond just Pate) both came from this. The cost was a few extra script revisions; the value was significantly more honest output.

A pattern that didn't work as well: I jumped to "refetch via cloudscraper" as the case-collision fix before fully considering reconstruction-from-cross-references. Matt's pushback was right and the policy in next.md now codifies "reconstruction before refetch" as default. This is a recurring failure mode — agents seem to default to "fetch missing data" because that's the common idiom in non-cached contexts — but the project's hard rule is the opposite.

## What changed in the graph

- 1 new character node: `pate-novice.node.md`
- 1 new index directory: `graph/index/characters/` (3,910 files + _summary.json)
- 1 new script: `scripts/build-character-indexes.py`
- 1 new audit script: `scripts/audit-missing-nodes.py`
- 1 new audit report: `working/audits/missing-nodes-2026-05-11/`
- alias-resolver regenerated (1,205 → 1,206 entries with pate-the-novice)
- mention-index regenerated (resolution rate unchanged at 70.6%; pate-novice now resolves via the new alias)
- character-index regenerated (Pate POV now resolves)

## Carry-over for next session

`next.md` is the canonical handoff. Five tracks, three runnable in parallel (Tracks 1+2+3). Stage 4 (Track 5) is best AFTER Tracks 1+2 land. Case-collision reconstruction (Track 4a) is independent of all others and uses no LLM.
