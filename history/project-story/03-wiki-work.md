# 03 — The Wiki Work

> Part of the project-story series. Written 2026-06-11, after Session 91.
> Previous: [02 — The Book Passes](02-book-passes.md) · Next: [04 — The Edge Layer](04-edge-layer.md)

## Vitals

| | |
|---|---|
| **Sessions** | S3–S5 (crawl), S16–S29 (Pass 2 + Python pivot), plus the 2026-06-11 audit coda |
| **Dates** | April 13 – May 1, 2026, with a punchline that landed June 11 |
| **Spend** | Crawl: **$0** (36 hours of wall-clock). Stage 1 agent run: **$95.33**. Secondary-tier work: **$51.83**. Schema-drift audit: **$50** (Opus, pre-approved). |
| **Spend avoided** | ~**$1,200** (the projected agent-promotion path for the secondary tier, replaced by Python) |
| **What shipped** | A 17,945-page local wiki cache; ~**8,263 active graph nodes** (excl. `_conflicts/` staging) across 21 type directories; the alias resolver; the infobox parse — and the project's defining rule, **Python before Agent** |
| **What it's about** | How the wiki became the graph's node layer — and how the wiki's best data sat on disk, fully parsed, for two months while the project paid LLMs to extract a worse version of it |

This chapter is the full arc of the project's relationship with **A Wiki of Ice and Fire** (AWOIAF), the fan-maintained encyclopedia at awoiaf.westeros.org. It has four movements: the crawl, the expensive way to turn wiki pages into graph nodes, the cheap way, and an irony two months in the making.

---

## 1. The crawl (April 13–14)

The plan was always to use the wiki as a *reference layer* — not the graph itself, but the scaffolding the graph would be assembled against. The decision in Session 3 was deliberately blunt: **full crawl, then triage**. Don't decide page-by-page what's worth keeping; fetch everything once, classify against a static local cache forever after.

The wiki had other ideas. It sits behind Cloudflare, and the project's first scraper — a careful, dependency-free, 1,213-line stdlib Python script — was dead on arrival. A session of cookie surgery (`cf_clearance` extraction, custom SSL contexts) bought exactly one working evening before the truth emerged: **Cloudflare's TLS fingerprinting rejects non-browser connections regardless of cookies.** No amount of header forgery fixes a TLS handshake that doesn't look like Chrome.

Session 4 was the capitulation: migrate to **Playwright**, real browser automation. Headed mode, not headless — headless is detectable. Even then there was a fight: a genuine Chromium/Playwright bug where the `cf_clearance` cookie (httpOnly, sameSite=None) was stored in the browser context but silently *not sent* on subsequent navigations. The workaround — a route interceptor that manually injects the cookie header onto every outgoing request — is the kind of fix you only find at 11pm.

Then the crawl ran. The estimate was 6–8 hours. It took **~36** — the first entry in what would become a project-long pattern of estimates low by 2–7×. The result:

- **17,945 of 17,952 pages** fetched, **377 MB** of JSON (page HTML plus metadata) in `sources/wiki/_raw/`
- Total model cost: **$0** — the single best free asset the project ever acquired
- Every later product in this chapter — every node, alias, prose body, category, and (eventually) infobox edge — derives from this one crawl

Two rules hardened around the cache and went into CLAUDE.md as near-constitutional law. **Never re-fetch:** all downstream work reads the local cache; the Playwright scraper was archived with do-not-restore instructions. **Never delete from sources:** stubs, redirects, list pages, disambiguation pages — tier them, defer them, never drop them. Source data is read-only and additive-only, a rule that held for all 91 sessions.

### The bug nobody saw for a month

The crawl had one hidden defect, and it's worth telling straight because of *how long* it stayed hidden. The scraper wrote each page to a file named after its title — and macOS's filesystem is **case-insensitive**. When the wiki had two pages differing only in capitalization (typically a real page and its redirect variant), the second write silently overwrote the first. About **125 pages were lost** this way, and nothing noticed: file counts looked plausible, spot checks passed, and the project built on the cache for **four weeks** before Session 41 reconciled files against the original title list and found the holes.

The recovery (Sessions ~41–48, via the watcher/worker "mission" protocol described in [05 — Infrastructure and Tooling](05-infrastructure-and-tooling.md)) reconstructed **70 of the 125** from redirect targets and adjacent data; the remaining 55 were tail-end stubs, dropped or aliased. The durable lesson entered the project's pattern library: **verify crawl integrity against the source-of-truth list, not against file counts** — a lesson the project would have to re-learn in another costume later (see the Session 71 false alarm in [04 — The Edge Layer](04-edge-layer.md)).

One more deferred liability from the crawl era: the scraper's entity classifier never really ran, leaving **17,305 of the pages uncategorized**. That deferral is the quiet thread connecting everything below — most of the wiki work that followed was, one way or another, the project figuring out what those pages *were*.

---

## 2. Pass 2, the expensive way: the Stage 1 agent run (April 25–27)

"Pass 2" in project vocabulary means **promotion**: turning a cached wiki page into a typed graph node. A node is a markdown file — `graph/nodes/characters/eddard-stark.node.md` — with YAML frontmatter (entity type, aliases, wiki source), an Identity section, prose, and an `## Edges` section listing the relationships the wiki asserts. The question Pass 2 had to answer 17,945 times: *what kind of thing is this page about, and what does the graph need from it?*

The first answer was to let an agent do everything. Pages were grouped into ~536 alphabetical "buckets" (`stark-h-q`, `houses-reach-h`, …); a **wiki-ingester** subagent received each bucket's bundle and wrote complete nodes — classification, frontmatter, prose synthesis, edges, the lot. A one-bucket smoke test (the direwolves, $1.15) looked fine, and the 37 core buckets launched.

The run itself was a baptism in operational reality: it hit Anthropic's **7-day rate limit** nine buckets in, burned $3–4 per failed retry against the wall, and surfaced a bucket-overlap bug (multi-letter character buckets like `stark-h-p` and `stark-h-q` shared 26 of 27 pages — wasted runs Matt chose to accept rather than re-engineer mid-flight). But it finished: **37 buckets, 855 agent-written nodes**, all validator-clean.

Then came the invoice. Stage 1 cost **$95.33 — $2.58 per bucket against a budget of $0.71–$1.43**, a 2–3× overrun driven by prompt-plus-page-bundle weight the planning estimates had missed. Projected over the 472 secondary-tier buckets still waiting: **~$1,200**. Session 23 flagged the number and deliberately *didn't* decide anything — it handed the decision to a cold reviewer.

Those 855 Stage-1 nodes still exist, and they're a permanent, visible seam in the graph: the only nodes with agent-written narrative richness, sitting alongside thousands of leaner deterministic ones. Not a defect exactly — more like rings in a tree.

---

## 3. The great reversal: Python before Agent (April 27)

Session 24 is arguably the most consequential single session of the project.

It began by the book: a fresh, context-free subagent ran the planned Stage 2 cold review of the Stage-1 output and returned **`remediate`** — two HIGH findings, fix the process before scaling. The orthodox path was remediation: patch the agent prompts, audit the bundles, then spend the $1,200.

Matt overturned it the same session, with two decisions that rewired the project.

**First: spoiler gating was deferred entirely.** From day one, the architecture had declared `first_available` — the field marking when each fact becomes spoiler-safe — "architectural, not optional." But the field was a tax on everything: agents burned context reasoning out individual values, a parser bug class made existing values wrong anyway, and the wiki's own citation data meant one deterministic script could backfill the whole corpus later. The "architectural" commitment was reversed to *deferred backfill, post-first-release*. (Honest aside: the reversal was never fully propagated — the worklog's Principles section still asserted the original position as late as the June audit. Reversals are easy; consistency is the hard part.)

**Second: Python before Agent became project law.** The insight was sitting in Stage 1's own statistics. The agent-written nodes averaged 5.83 edges each — and almost all of those edges came from **infobox fields**, the structured fact-table in the corner of every wiki article. That's deterministic data. Paying an agent ~$2.58 a bucket to transcribe it across 5,000+ secondary pages was paying reasoning prices for copying. The new rule, verbatim from the memory file it spawned: *whenever a deterministic Python step can produce part of the output, it runs first. Agents only do what genuinely requires reasoning.*

Stage 3 was rebuilt around the rule, and the results were almost comically lopsided. A deterministic skeleton emitter read the parsed infobox data and produced frontmatter, identity, and edges for every page. Even the step everyone assumed needed an LLM — extracting prose — fell to Python once someone looked: the wiki HTML *already contains the prose*; a ~770-line extractor mapped section headings to the node schema and processed 3,315 pages in about 14 seconds. Net effect:

> **3,314 nodes promoted in roughly 30 seconds, for $0** — against the ~$1,200 agent path they replaced.

The rule went on to win at least six more times across the project (mention indexes, entity indexes, the edge spine, hospitality edges, temporal scoping, alias resolution). Every time a pipeline stage was re-examined, more of it turned out to be deterministic than anyone had assumed.

---

## 4. The promotion campaigns (April 28 – May 1)

What followed was a grinding, satisfying week of **campaigns**: run the infobox parser, find what it misclassifies, fix the parser, promote another tranche, audit, repeat. The graph grew from 855 nodes to **7,563** in five sessions, and the parser (`scripts/wiki-infobox-parser.py`) accreted the project's institutional knowledge of the wiki: category mappings, entity-type overrides (the Iron Throne is an artifact, not a place; Wildfire is an artifact "with narrative weight, like Ice and Dawn"; a Dragon is a species but Drogon is a character), exclusion patterns for chapter-summary pages (a 338-node mistake, reverted and re-run cleanly), and a new `object.food` type — because in this project, food and hospitality are first-class data, by explicit design value.

Three episodes from the campaign era deserve their own lines:

**The one approved exception-fetch.** The original crawl used MediaWiki's `action=parse` API, which strips the category footer from every page — and the entity classifier needed exactly those categories. This was the single narrow case where the never-re-fetch rule bent: a bounded, audit-logged, single-purpose script (`wiki-fetch-categories.py`, using `cloudscraper` for the Cloudflare handshake — the Playwright scraper stayed archived) fetched *category metadata only* for all pages, writing to the working directory, never to `sources/`. The exception was written into CLAUDE.md with the precision of a treaty clause: per-use approval, one data field, lightweight client, audit log. It has been used exactly once.

**The $50 schema-drift audit.** With ~7,500 nodes promoted mostly by deterministic code, Session 29 paid for a full-corpus Opus audit of schema consistency. Verdict: **0 HIGH findings**, 4 medium, 4 low. Money spent specifically to find out the cheap pipeline hadn't quietly rotted — and it hadn't.

**The long tail of types.** By the end, the node layer spanned 21 type directories — beyond the obvious characters/houses/locations/events, the campaigns minted `materials/`, `languages/`, `medical/`, `customs/`, `foods/`, `theories/`, `texts/`, `species/` and more. Later backfills (missing-node recovery, the case-collision reconstructions) brought the layer to its present **~8,263 active nodes** (excl. `_conflicts/` staging). The biggest unresolved finding was structural: 70% of wiki pages classified as `unknown` not because the crawl missed anything but because **many pages simply have no infobox** — the parser, not the scraper, was the bottleneck. Worth holding onto that sentence; it's the hinge of the irony coming in section 6.

---

## 5. The comention saga (teaser)

Nodes are only half a graph. From late April onward, the open question was **edges**: the wiki's prose is dense with relationship claims, and Stage 4 was conceived to extract them — generate candidate pairs from co-mentions in wiki chapter-summary text, then have an LLM classify each pair against a controlled vocabulary.

That effort ran **five weeks and roughly $150–190**, produced the most sophisticated safety machinery in the project — locked vocabularies, qualifier enums, mechanical validators, drift detection, cross-model audits — and was then **deprecated in its entirety** when Session 65 concluded the candidate source itself was structurally noisy. The full story, told honestly, is the first half of [04 — The Edge Layer](04-edge-layer.md). It belongs in this chapter only as setup, because of what was sitting on disk the whole time.

---

## 6. The infobox irony

Here is the punchline of the entire wiki arc, and Matt wants it told properly.

Recall what the infobox parser had been doing since **April**. For every cached page, it pulled apart the infobox — the structured fact-table in the top-right corner of every wiki article: Title, Allegiance, Father, Mother, Spouse, Born, Died, Seat, Overlord, Culture. And it didn't just extract the fields. Its `FIELD_EDGE_MAP` translated each field **into the project's own locked edge vocabulary**: `Allegiance` → `SWORN_TO`, `Father` → `PARENT_OF`, `Seat` → `SEAT_OF`, `Title` → `HOLDS_TITLE`. The output, `working/wiki/data/infobox-data.jsonl`, contained **4,786 pages and 20,614 relationship rows, already typed to 23 edge types** from the master vocabulary.

A real row, from the spec ([§1](../../working/infobox-merge/spec.md)):

```json
{"page": "Abelar Hightower", "entity_type": "character.human", "relationships": [
  {"field": "Title", "target": "Ser", "edge_type": "HOLDS_TITLE", "direction": "forward"},
  {"field": "Allegiance", "target": "House Hightower", "edge_type": "SWORN_TO", "direction": "forward"},
  {"field": "Culture", "target": "Reach", "edge_type": "CULTURE_OF", "direction": "forward"},
  {"field": "Born", "target": "Oldtown", "edge_type": "BORN_AT", "direction": "forward"}], "cite_refs": {}}
```

That is not a candidate. That is not prose needing interpretation. That is an edge, parsed, typed, and directed, waiting for a filter script.

The data wasn't even *hidden*. It was rendered into every node file's `## Edges` display bullets — 21,129 of them across 4,684 files — where humans could read it. It just was **never promoted into the canonical edge file**, `graph/edges/edges.jsonl`. The promotion pipeline that produced it was a node pipeline; edges were "Stage 4 territory"; and Stage 4 went chasing wiki *prose* instead. So:

> While the project spent **five weeks and ~$150–190** teaching LLMs to extract relationship edges from wiki prose — building vocabulary lockdowns, drift detectors, and cross-model audits to make them safe, and ultimately deprecating the whole track — **20,614 relationship rows of the wiki's structured data sat fully parsed on disk, typed to the project's own vocabulary, from April to June.** Genealogy, fealty, titles, successions, vital records: exactly the lookup-shaped facts the book-derived edge layer is thinnest on.

The 2026-06-11 audit (a read-only deep-dive across the graph and the project's history — the same audit this story series is built from) found it, measured it, and made the case in three numbers:

- **98.4% additive.** Of 20,614 infobox pairs, only 340 connect a pair the canonical edge layer already connects; only 159 match on pair *and* type. This isn't a redundant copy of the book edges — it's the complementary half. The book layer owns *lived* relationships (Jon Snow has 336 edges: LOVES, PROTECTS, OPPOSES, each with a quote). The wiki layer owns *structure*: Walder Frey has 2 family edges in canon and **8 spouses + 29 children** in his infobox.
- **14.7% → ~71%.** Today only 1,216 of 8,263 nodes touch any edge — dense around the POV characters, dark everywhere else (houses 4.5% connected, locations 5.2%, titles 2.6%). Simulated post-merge connectivity: **~71%** overall; characters 20% → 97%, houses → 94%, titles → 87%.
- **$0.** The merge is one deterministic Python script. After a carefully specified rule set — noise filtering, a resolution ladder for display-strings → node slugs, endpoint type contracts, direction corrections, and a quarantine for the wiki's habit of *encoding rumor with a straight face* (Jon Snow's infobox lists **two** "Mothers," Wylla *supposedly* and Ashara Dayne *rumored* — naive promotion would graph-canonize the series' most famous red herrings) — **17,040 of the 20,614 rows merge**, all at confidence Tier 2, because Tier 1 is earned only by verbatim book quotes.

Matt accepted the verdict and **greenlit the merge the same day**. The full specification — every rule, every count, every quarantined Jon Snow mother — lives at `working/infobox-merge/spec.md`, with a dry-run gate before anything touches the graph.

The fairest framing, from the audit's own synthesis: *the deprecation of the prose track was right; the merge was just never sequenced.* Nobody chose to ignore the infobox layer. It fell into the gap between a node pipeline that produced it and an edge pipeline that was looking somewhere else — and the project's documentation surface had lagged its actual state badly enough that no session ever tripped over it. The irony isn't that the project was foolish. It's that the project's best idea (Python before Agent, April 27) had already quietly done the work, and it took a $50 history audit in June to notice.

---

## What it taught

1. **Crawl once, hoard everything, never re-fetch.** The 36-hour, $0 crawl is the highest-leverage asset in the repo. Every product of three months of work derives from it. The narrow, audit-logged exception process proved you can keep a hard rule and still fix real gaps.
2. **Verify against the source-of-truth list, not file counts.** ~125 pages vanished into a case-insensitive filesystem and stayed invisible for a month because every count looked plausible.
3. **Estimates run 2–7× low; build the gate, not the forecast.** Crawl 6–8h → 36h; Stage 1 $0.71–1.43 → $2.58/bucket. What saved the project wasn't better estimating — it was the habit of stopping at the invoice and handing the decision to a cold reviewer.
4. **Python before Agent is the project's best idea.** The same data that cost $2.58/bucket through an agent cost ~$0 through a parser. The rule won every time it was tested, and the deterministic layers are also *regenerable* — re-run the script, get the same graph.
5. **A reversal isn't done until the documents agree.** Spoiler gating was reversed cleanly in one session, and its ghost still haunted the Principles list two months later.
6. **Your most valuable data may already be parsed.** The infobox irony is the chapter's whole lesson in one line: before paying a model to extract something, check whether a deterministic process already extracted it — *especially* if that process was your own.

*Next: [04 — The Edge Layer](04-edge-layer.md) — the five-week comention grind, the pivot to the project's own extractions, and how the graph learned to refuse edges it couldn't cite.*
