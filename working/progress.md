# Working Progress — Agent Handoff Document

> **Purpose:** This file tracks the state of in-progress work across agent invocations and sessions. When an agent finishes a batch of work, is interrupted, or surfaces something interesting, it logs here. The next agent (or session) reads this to pick up where things left off.
>
> **Convention:** Newest entries at the top. Each entry is dated and tagged with the agent/task that produced it.

---

## Pass 1 Mechanical Extraction — AGOT Full Run (2026-04-22)

Using patched mechanical-extractor agent (chapter-isolation, Tier 1 default, first_available field). Overwriting 5 pre-patch extractions. Waves of 5 subagents.

- **Wave 1** — agot-prologue, agot-bran-01, agot-catelyn-01, agot-daenerys-01, agot-eddard-01 ✅ (5/5)
- **Wave 2** — agot-jon-01, agot-catelyn-02, agot-arya-01, agot-bran-02, agot-tyrion-01 ✅ (5/5)
- **Wave 3** — agot-jon-02, agot-daenerys-02, agot-eddard-02, agot-tyrion-02, agot-catelyn-03 ✅ (5/5)
- **Wave 4** — agot-sansa-01, agot-eddard-03, agot-bran-03, agot-catelyn-04, agot-jon-03 ✅ (5/5)
- **Wave 5** — agot-eddard-04, agot-tyrion-03, agot-arya-02, agot-daenerys-03, agot-bran-04 ✅ (5/5)

---

## How To Use This File

### For Agents
- **Before starting work:** Read this file to see if there's prior context relevant to your task.
- **During work:** If you find something unexpected, ambiguous, or potentially valuable but outside your scope, log it here under "Scratch Notes" rather than discarding it.
- **After finishing a batch:** Log what you completed, what's left, and any issues encountered.

### For Matt
- Check this between sessions to see what agents were doing and whether anything needs human review.
- Anything that graduates from scratch notes to a real project artifact should be moved to the appropriate location and removed from here.

---

## Current Focus

Chapter splitter complete (all 5 books). Wiki scraper script written but blocked on Cloudflare — needs browser cookies to scrape AWOIAF. Next unblocked task: mechanical extraction testing on AGOT chapters.

---

## Active Handoffs

### Wiki Scraper → Matt (2026-04-13)
**Blocker:** AWOIAF sits behind Cloudflare's managed challenge. Automated API access fails with 403.
**Action needed:** Visit https://awoiaf.westeros.org in browser, copy `cf_clearance` cookie, save to `sources/wiki/_raw/.cookies`:
```
cf_clearance=PASTE_VALUE_HERE
```
Then run: `python3 scripts/wiki-scraper.py --mode targeted --batch characters -v`

---

## Scratch Notes

### POV Reference Table Gaps (Session 2, chapter-splitter)
The original `reference/pov-characters.md` was missing 6 chapter headings. All have been added:
- AFFC: THE REAVER (Victarion Greyjoy)
- ADWD: THE BLIND GIRL (Arya), A GHOST IN WINTERFELL (Theon), THE IRON SUITOR (Victarion), THE KINGBREAKER (Barristan), THE QUEEN'S HAND (Barristan)

### Smart Quotes in Source Files (Session 2, chapter-splitter)
Source .txt files use Unicode curly/smart quotes (U+2019 right single quote mark instead of U+0027 straight apostrophe). The chapter splitter normalizes these before heading matching. The wiki scraper may also need to be aware of this if cross-referencing chapter text.
- **Wave 6** (2026-04-22 04:02) — agot-eddard-05,agot-jon-04,agot-eddard-06,agot-catelyn-05,agot-sansa-02 ⚠️ (0/5, failed: agot-eddard-05,agot-jon-04,agot-eddard-06,agot-catelyn-05,agot-sansa-02)
- **Wave 6** (2026-04-22 04:16) — agot-eddard-05,agot-jon-04,agot-eddard-06,agot-catelyn-05,agot-sansa-02 ✅ (5/5)
- **Wave 9** (2026-04-22 04:16) — agot-catelyn-07,agot-jon-05,agot-tyrion-06,agot-eddard-11,agot-sansa-03 ✅ (5/5)
- **Wave 8** (2026-04-22 04:17) — agot-eddard-09,agot-daenerys-04,agot-bran-05,agot-tyrion-05,agot-eddard-10 ✅ (5/5)
- **Wave 7** (2026-04-22 04:17) — agot-eddard-07,agot-tyrion-04,agot-arya-03,agot-eddard-08,agot-catelyn-06 ✅ (5/5)
- **Wave 10** (2026-04-22 11:46) — agot-eddard-12,agot-daenerys-05,agot-eddard-13,agot-jon-06,agot-eddard-14 ✅ (5/5) [715s, 1052 tokens]
- **Wave 13** (2026-04-22 11:47) — agot-jon-08,agot-daenerys-07,agot-tyrion-08,agot-catelyn-10,agot-daenerys-08 ✅ (5/5) [715s, 1108 tokens]
- **Wave 11** (2026-04-22 11:47) — agot-arya-04,agot-sansa-04,agot-jon-07,agot-bran-06,agot-daenerys-06 ✅ (5/5) [730s, 1063 tokens]
- **Wave 12** (2026-04-22 11:47) — agot-catelyn-08,agot-tyrion-07,agot-sansa-05,agot-eddard-15,agot-catelyn-09 ✅ (5/5) [731s, 1020 tokens]
- **Wave 15** (2026-04-22 13:05) — agot-jon-09,agot-catelyn-11,agot-daenerys-10 ✅ (3/3) [407s, 574 tokens]
- **Wave 14** (2026-04-22 13:09) — agot-arya-05,agot-bran-07,agot-sansa-06,agot-daenerys-09,agot-tyrion-09 ✅ (5/5) [687s, 1209 tokens]
