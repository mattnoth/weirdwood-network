# Citation-validator full-corpus re-run dispatch prompt

**Date:** 2026-05-06
**Sub-agent type:** `citation-validator`
**Trigger:** Pass 1 v3 reached 344/344 across all 5 main books on 2026-05-06 (AGOT 73 + ACOK 70 + ASOS 82 + AFFC 46 + ADWD 73). The previous citation audit (2026-04-30) flagged 9 chapter-cite occurrences pointing to AFFC/ACOK/ADWD chapters that didn't exist at audit time. Those should now resolve.

**Dispatched prompt:**

```
Re-run the citation audit on the full 5-book corpus. Pass 1 is now 344/344
across all 5 main books (AGOT 73 + ACOK 70 + ASOS 82 + AFFC 46 + ADWD 73).
Previously-deferred chapter-cite checks for missing chapter files should now
resolve. Output the dated report to:
  /Users/mnoth/source/asoiaf-chat/working/audits/citation-corpus-rerun-2026-05-06/execution/citation-issues.md

Expected: zero broken chapter-cite targets except the known Stage-1 cite-format
limitations (bare `(wiki:R{book}{N})` cite_refs, comma-joined multi-source cites,
multi-cite_ref chained cites, paragraph-bracketed missing-cite pattern). These
were already documented in the prior audit and aren't new findings.
```

**Why this folder layout:** Q10 of the 2026-05-06 handoff established the per-audit folder convention. `prompt/` keeps the dispatch record alongside `execution/` (the report itself), `validation/` (independent re-checks), and `prompt-planning/` (any pre-audit notes).
