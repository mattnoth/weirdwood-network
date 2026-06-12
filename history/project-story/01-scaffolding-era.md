# 01 — The Scaffolding Era

> Part of the [project-story series](00-overview.md). Previous: [overview](00-overview.md) ·
> Next: [02 — The Book Passes](02-book-passes.md)

**Vitals**
- **Sessions:** S0–S5 (Phases 0–1)
- **Dates:** April 13–14, 2026
- **Recorded spend:** $0 (the crawl cost time, not dollars — ~36 hours of wall clock)
- **Shipped:** the architecture, the repo scaffold, 344 chapter files split from all five books, and a 17,945-page local mirror of the entire ASOIAF wiki

Two days. Everything else in this story — the $234 extraction campaign, the 8,263 active nodes (excl. `_conflicts/` staging), the cited edge layer — runs on assets created in these two days for nothing.

## The design commitments

Session 0 was pure design: Matt and Claude sketched the whole system before a line of tooling existed. The commitments made that day:

- **Two layers:** a *trigger table* (an index mapping textual mentions to entities) plus a *knowledge graph* (typed nodes and edges). Both survive to today.
- **A six-pass extraction pipeline:** mechanical extraction, wiki ingestion, voice analysis, foreshadowing, theory extraction, open discovery. Only the first two would ever be built — Passes 3–6 are still stubs as of Session 91, and the dark theories-and-prophecies corner of today's graph is the visible cost of that.
- **Five confidence tiers**, verified-canon down to crackpot, tagged on everything. Survives intact; it's why a wiki fact and a book quote never carry the same authority.
- **Spoiler gating via `first_available`**, declared *required from the start* — every node and edge would record the earliest book where it becomes known, so queries couldn't spoil later books. This was the era's boldest commitment and its most prominent reversal-in-waiting: eleven days later (Session 24) it was deferred outright, and it has stayed deferred ever since. Remember this one — it comes back as the hinge of the project's biggest pivot.
- Smaller calls that quietly endured: a `PERCEIVED_AS` edge type for cross-POV perception, and `real_identity` mapping so descriptively-titled chapters ("The Prophet") still resolve to their POV character.

Session 1 built the skeleton — and made one decision with teeth: **the `.gitignore` was created before anything else**, because copyrighted book text must never enter git history. Source text, chapters, and the wiki cache have been gitignored ever since; only derived structure gets committed. Seven subagent definitions went in as stubs, and the repo got its split identity: local directory `asoiaf-chat`, eventual public name *the-weirwood-network*. (The local name is itself a fossil — the "chat app" framing it encodes was retired as a stale sketch in May. The graph outlived its first excuse.)

## The splitter: 344 chapters, first try

Session 2 produced `scripts/chapter-splitter.py`, which cuts the raw `.txt` of each novel into per-chapter markdown files with YAML frontmatter. The design choice that mattered: chapters are detected by a *prose heuristic* (what chapter headings look like against running text), not by blank-line gaps.

It worked immediately. AGOT 73, ACOK 70, ASOS 82, AFFC 46, ADWD 73 — **344 chapters, every count matching the expected POV tables on the first real run.** The only fix needed was upstream: six chapter headings missing from the reference POV list. In a project whose history is mostly estimates missing by 2–7× and bulk runs melting down overnight, the splitter is the rare thing that just worked — and all ~3,800 file-and-line edge citations in today's graph point into the files it made.

## The Cloudflare fight

The same session wrote a wiki scraper for AWOIAF — 1,213 lines, deliberately stdlib-only, no dependencies. It was dead on arrival: Cloudflare blocked it.

Session 3 planned the crawl anyway, and made a scope decision that aged extremely well: **crawl everything, triage later.** Not a curated list of important pages — all 17,952 titles the wiki reported. The reasoning: scraping is cheap, classification can be endlessly refined against a static local cache, and the cache is a reference layer, not the graph itself. A cookie-based workaround (borrow a browser's `cf_clearance` token) passed a smoke test that day.

By Session 4 the cookie had expired, and a fresh one didn't help — which forced the real diagnosis: **Cloudflare was rejecting the connection by TLS fingerprint.** No cookie could fix that; urllib simply doesn't shake hands like a browser. The scraper was migrated to Playwright, driving a real (headed — headless is detectable) Chromium window, with a Turnstile-polling warmup. Even then there was one more trap: a Chromium bug where the `cf_clearance` cookie was stored but silently *not sent* on navigations. The workaround — a route interceptor manually injecting the cookie header onto every outgoing request — is the kind of fix you only find by refusing to give up at 2 a.m.

## The 36-hour crawl

Session 5 ran it: **17,945 of 17,952 pages, 377 MB of JSON**, throttled and unattended. The estimate was 6–8 hours; it took roughly 36 — the project's first data point in what became a reliable pattern (estimates low by 2–7×, essentially every time). The page classifier was also supposed to sort pages into characters/locations/houses as it went; it left 17,305 of them uncategorized. That got shrugged off as "triage later" — correctly, it turned out, since categories were eventually backfilled by other means.

What nobody noticed: the crawl wrote one file per page title onto a **case-insensitive filesystem**. Wiki titles that differ only by case — a page and its redirect variant — silently overwrote each other. About 125 pages were lost this way, and because the file *count* looked right, nothing flagged it. The bug sat undiscovered for four weeks, until Session 41; reconstruction missions later recovered 70 of the pages, and the remaining 55 were dropped or aliased. The lesson — *verify crawl integrity against the title list, not file counts* — foreshadowed a whole family of count-based false alarms to come.

And then: never again. The cache became permanent, with an escalating series of hard rules against ever re-fetching (one narrow, individually-approved exception was granted weeks later, for category metadata only). Every node, alias, infobox edge, and cluster in today's graph derives from this one crawl.

## What this era seeded

Almost everything, disproportionately to its 48-hour length. The 344 chapter files became the substrate for Pass 1, whose tables became the edge layer's primary source. The wiki cache became ~7,500 nodes, the alias resolver, and — parsed in April, ignored until June — the infobox layer now poised to quintuple the graph's connectivity for $0. The crawl-everything-triage-later instinct previewed Python-before-Agent before that rule had a name; the case-collision bug previewed the count-based-health-check failure mode; the 36-hour estimate miss previewed every estimate after it. And the era's proudest architectural commitment — mandatory spoiler gating — became the project's first lesson that commitments made at design time are hypotheses, not laws. The next era would start spending real money to find out which of the others held. → [02 — The Book Passes](02-book-passes.md)
