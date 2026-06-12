# The Weirwood Network — The Story of the Project

> Part of the project-story series, written June 2026 after Session 91. Start here; each
> chapter below tells one era in full. A [glossary](glossary.md) decodes every piece of
> internal vocabulary you'll hit along the way.

## What this project is

The Weirwood Network is a queryable knowledge graph for *A Song of Ice and Fire*. As of June 11, 2026, it holds **8,263 active entity nodes** (excluding `_conflicts/` staging) (characters, locations, houses, events, artifacts, titles, factions, and more) and **4,760 typed edges** — and nearly every edge carries a **verbatim quote from the books plus a file-and-line citation** proving it. Ask the graph who killed whom at the Red Wedding and it doesn't just answer; it points to the sentence George R.R. Martin wrote.

The graph isn't built for humans to browse. It's built for **AI agents to traverse** — so that an agent answering ASOIAF questions, or grounding character dialog, can cite canon instead of producing plausible-sounding hallucination. That goal — *citation-grounded agent traversal* — is the through-line of everything below.

The project was built solo by Matt, orchestrated through 91 Claude Code sessions between **April 13 and June 11, 2026**.

## The arc, in one paragraph

In two days the project split all five books into 344 chapter files and crawled the entire ASOIAF fan wiki (17,945 pages) into a local cache it would never need to re-fetch. It then spent three weeks evolving a "Pass 1" extraction schema and running it — on Opus, for about $234 — across every chapter of all five books, producing structured tables of entities, relationships, food, hospitality, and physical description. A wiki-promotion campaign ("Pass 2") started as an expensive agent-does-everything pipeline, blew its budget 2–3×, and triggered the project's defining pivot: **Python before Agent** — do everything deterministic in code first, spend model dollars only on what genuinely requires reasoning. That rule promoted ~7,000 nodes for roughly nothing. Then came the long middle: five weeks and ~$150–190 trying to make LLMs safely classify edges out of wiki prose ("Stage 4"), a track that was eventually deprecated wholesale — but which built the lockdown-and-validation machinery (locked vocabularies, mechanical validators, drift detection, cross-model audits) that made every later model pass safe. The breakthrough was realizing the project's own Pass 1 tables were a better edge source than the wiki: a deterministic "spine" of 2,834 cited edges for $0, an LLM "tail" for $21, and `edges.jsonl` was born. Two enrichment attempts failed their precision gates and were correctly not promoted (saving roughly $600 of bulk spend); a structural "reification" era then rebuilt events as first-class hub nodes with role edges, validated end-to-end on the Red Wedding. The project ends this chapter of its life with a real, validated, cited graph — and a free, already-parsed wiki layer about to take its connectivity from 15% to over 70%.

## Timeline

| Phase | Sessions | Dates (2026) | What shipped |
|---|---|---|---|
| 0–1. Scaffolding & wiki crawl | S0–S5 | Apr 13–14 | Architecture, 344 chapter files, 17,945-page wiki cache ($0) |
| 2. Pass 1 schema evolution | S6–S15 | Apr 16–25 | v1→v2→v3 extraction schema; D&E + TWOIAF sources; process infrastructure |
| 3. Wiki Pass 2, Stage 1 | S16–S23 | Apr 25–27 | 855 agent-written nodes; 2–3× cost overrun ($95) |
| 4. Python-first pivot | S24–S29 | Apr 27–May 1 | Spoiler gating deferred; 3,314 nodes promoted in ~30s for $0; graph → 7,563 nodes |
| 5. Pass 1 completion | S30–S35 | May 1–6 | All 5 books extracted, 344/344 chapters (~$234 total) |
| 6. Hygiene & indexes | S36–S51 | May 6–13 | Mention/entity indexes, +247 backfilled nodes, case-collision recovery, mission protocol |
| 7. Stage 4: wiki comention | S52–S64 | May 13–22 | Vocab lockdown + validators built; the candidate source itself dead-ended (~$150–190) |
| 8. Pass-1-derived edges | S65–S74 | May 22–26 | **edges.jsonl v1**: 3,811 cited edges (spine $0 + tail $21); extra-tables enrichment NO-GO |
| 9. Events-Haiku attempt | S75–S81 | May 26–Jun 1 | Operationally flawless run, failed cross-model audit — NO-GO, output parked (~$75) |
| 10. Reification plates | S82–S87 | Jun 4–9 | Events as hub nodes: edges 3,811 → 4,757; event nodes 371 → 583; Red Wedding traversal works |
| 11. Validation & renames | S88–S91 | Jun 9–11 | Mode 1 probes, event renames, curator pilot edges → **4,760 edges**; infobox merge greenlit |

## The headline numbers

- **8,263 active nodes** (excl. `_conflicts/` staging), **4,760 edges**, 0 orphan edges, 100% endpoint resolution; ~99% of edges carry a verbatim evidence quote, ~3,800 with exact `file:line` references spot-verified against the books (5/5 verbatim on the audit's random check).
- **Recorded spend: ~$770–830** across 91 sessions. Roughly a third went to the deprecated wiki-comention track — which nonetheless funded the safety machinery everything since depends on.
- **~$4,400+ avoided** by smoke tests, precision gates, and pivots: a ~$1,200 agent-promotion path replaced by $0 Python; a $615 Sonnet bulk remainder never run; $270–290 and ~$340 of enrichment bulks held back by NO-GO gates; ~$2,000 of a projected Sonnet-heavy month never spent.
- **Connectivity: 14.7%** of nodes currently touch an edge — the graph is dense around the POV spine and dark everywhere else. The fix has been sitting on disk, fully parsed, since April: 20,614 typed wiki infobox relationship rows, 98.4% additive to the book edges. The merge was **greenlit on June 11, 2026** and is projected to take connectivity to **~71–72%** for $0.

## Reading guide

**[01 — The Scaffolding Era](01-scaffolding-era.md).** Two days in April: the architecture commitments (some of which would later be reversed), a chapter splitter that got all 344 chapters right on the first real run, a fight with Cloudflare that ended in browser automation, a 36-hour crawl that was supposed to take 6–8, and a silent filesystem bug that wouldn't be discovered for a month.

**[02 — The Book Passes](02-book-passes.md).** Pass 1 mechanical extraction across all five novels: how the schema evolved from v1 to v3 (food, hospitality, and physical description promoted to first-class data), what it cost, the `--chain` terminal-explosion incident, and why this ~$234 purchase turned out to be the highest-ROI spend in the project.

**[03 — The Wiki Work](03-wiki-work.md).** Everything downstream of the crawl: the Pass 2 promotion campaigns that built ~7,500 nodes, the cost blowout that triggered the Python-first pivot, the five-week comention saga and its deprecation, and the infobox layer — parsed in April, ignored for two months, and now the single highest-leverage asset on disk.

**[04 — The Edge Layer](04-edge-layer.md).** How `edges.jsonl` was actually built: the S65 forensics that pivoted the candidate source from wiki prose to the project's own Pass 1 tables, the deterministic spine, the LLM tail, the NO-GO'd enrichment attempts, and the reification plates that gave the graph real event structure.

**[05 — Infrastructure and Tooling](05-infrastructure-and-tooling.md).** The unglamorous load-bearing layer: the splitter, the wrappers and run-forever loops, the validators and drift detectors, and the process discipline (worklog, continue prompts, endsession, staleness rules) that let 91 sessions of amnesiac agents behave like one continuous project. Also covers the project's sharpest scope-creep incident: a 27-agent fleet and full chat-UI architecture doc that an agent produced in Session 26, ten sessions before anyone noticed it wasn't what Matt had asked for.

**[06 — Reification, Explained](06-reification-explained.md).** A deep explainer on the project's one structural (rather than additive) improvement — events as hub nodes, role edges, SUB_BEAT_OF — with the Red Wedding as the worked example.

And the **[glossary](glossary.md)**: every internal term (Passes, Stages, Plates, Tracks, the three different Tier systems, Modes, buckets, waves, and the rest) in plain English.

## Where it stands today (June 11, 2026)

The graph is real and validated, and a full read-only audit (accepted by Matt on June 11) finally brought the documentation in line with that fact. The immediate next step is the **infobox merge** — spec'd at `working/infobox-merge/spec.md`: one Python script promoting ~18–19k already-parsed, already-typed wiki relationship rows (genealogy, fealty, titles, vital records) into the edge layer at confidence Tier 2. Wiki edges never get Tier 1 — Tier 1 is earned by verbatim book quotes. The merge moves connectivity from 14.7% to roughly 71–72% and finally answers the lookup-shaped questions ("Who are Walder Frey's 29 children?", "Which houses are sworn to House Tyrell?") that the book layer alone cannot.

After the merge comes **Mode 3** — the real test the whole project has been pointed at: hand an agent the merged graph as a tool and have it answer genuine ASOIAF questions and ground character dialog. Whatever fails in that dip decides what gets built next. One corner stays dark even after the merge: theories and prophecies (45 theory nodes, 2 prophecy nodes, effectively zero edges) — that's Pass 4/5 territory, designed on day one and never built, and it's the most interesting unwritten chapter.
