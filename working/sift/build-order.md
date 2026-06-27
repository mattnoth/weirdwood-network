# BUILD ORDER — the Sift, Stage 1 (fresh-session kickoff)

**You are a fresh build session.** Your job: build **Stage 1 of "the Sift"** and run a smoke test, then STOP and
report. The full, authoritative spec is `working/sift/sift-design.md` — **read it first; it governs.** This file is
the scope clamp + the gotchas that are easy to get wrong.

**Recommended model:** Sonnet 4.6 (`claude-sonnet-4-6`). This is codegen from a detailed spec — Sonnet is the right
fit. Haiku is too weak for the regex/normalization subtleties; Opus is overkill.

---

## Build ONLY this (Stage 1)

1. **`scripts/sift.py`** — a `Sift` class + an argparse CLI. One public behavior that matters: `run`.
   - `run --lens <name> [--book <book>]` — the Python scan. **Build fully.**
   - `status` — lenses present, last run, pointer counts per lens/book.
   - `interpret --lens <name> [--book <book>]` — **STUB ONLY**: print "Stage 2 (Haiku) is deferred — not implemented"
     and exit. No LLM call, no `claude -p`, nothing.
   - `backfill-aliases --lens <name>` — **STUB ONLY**: print "deferred" and exit. Do NOT mutate any node files.
2. **`working/sift/lenses/oaths.lens.json`** — the oaths & vows lens. Use the seed lexicon in doc §4, `exclusions: []`
   (empty — we tune only after the smoke test), snippet window 2/2.
3. Scaffold dirs (`working/sift/oaths/`, etc.).
4. Wire a `sift` dispatch into `scripts/weirwood.zsh` that forwards to `python3 scripts/sift.py ...` — match the
   existing subcommand style (read the file first). If non-trivial, leave a clear TODO and note it; the smoke test
   can run via direct `python3 scripts/sift.py run ...`.

## Engine correctness — the 5 that bite (full detail in doc §2)

1. **stdlib `re` only — install NO package** (no pyahocorasick). It's the documented future escape hatch, not v1.
2. **Sort triggers longest-first**, `re.escape()` each, join with `|`. Python `re` is first-alternative-wins, not
   longest-wins — ordering is what makes "apple tart" beat "apple".
3. **Boundaries via lookarounds** `(?<!\w)(?:ALTERNATION)(?!\w)`, NOT a blanket `\b` (which breaks on
   multi-word/punctuated triggers). Compile `re.IGNORECASE | re.UNICODE`.
4. **Curly-quote normalization:** prose uses U+2019 `’` and `“ ”`. Normalize quote chars on BOTH triggers and text
   before matching, using **1:1 char swaps only** (’→', “→", ”→") so offsets stay stable. No length-changing
   normalization on the matched copy.
5. **Line numbers:** read the whole file (frontmatter included); build a cumulative line-start offset array; `bisect`
   each match start for the true 1-based line. Don't strip-and-re-zero.

Plus: deterministic sort `(chapter_file, line, match_start, trigger)`; JSONL per-book at
`working/sift/oaths/<book>.pointers.jsonl`; first line of each output file is the header
`# SIFT OUTPUT — lens=oaths — NOT the harvest queue. See working/sift/sift-design.md`; sha256 resume manifest;
trigger-coverage report (hits/trigger, zero-hit triggers).

## Smoke test (do this, then STOP)

- Run `python3 scripts/sift.py run --lens oaths --book agot` (pure Python — safe; no LLM).
- Verify: works end-to-end, fast (well under ~2s), and deterministic (run twice → byte-identical output).
- **Report:** total AGOT pointer count, the trigger-coverage summary, and **~15–20 sample pointer rows** (varied
  triggers, with snippets) for human eyeballing. Flag obvious false positives / recall gaps you noticed — but do
  **NOT** tune the lexicon or add exclusions. That's a human review step.

## Hard stops

- Do NOT implement Stage 2 / interpret logic. Do NOT implement alias backfill. Do NOT tune the lexicon.
- Do NOT write into `graph/nodes/`. NEVER touch `working/harvest-queue.md`.
- Read LOCAL only (`sources/chapters/`, `graph/nodes/`) — no network, ever.
- Stop after the smoke-test report so the human can review the noise before anything is tuned.
