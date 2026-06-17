# Project Vocabulary — Canonical (forward)

> **Status:** DECIDED 2026-06-16 (S103, Matt). This is the **forward** vocabulary — the words to use
> for new work. For decoding *retired* terms in old docs, see `history/project-story/glossary.md`.
>
> **The rule of thumb that generated this list** (keep it in mind before coining anything):
> *"Is this a **thing**, or me **doing** a thing? A thing gets a Word; doing it gets a sentence."*
> A term earns a capital letter only if it names a durable noun in the project. Process mechanics —
> executing, checking, sequencing — stay lowercase and get **described**, not named.

## The canonical terms

There are **three** capitalized terms, plus one default lowercase word. That's the whole vocabulary.
Adding a new capitalized term requires a worklog **Active Decision** entry.

| Term | Plain-English definition | Rules |
|---|---|---|
| **Pass** | A big, numbered sweep over the whole book corpus (Passes 1–6). | Whole numbers only — no "Pass 1.5". A smaller effort is a Track. Grandfathered: the 1–6 numbering is baked into the pipeline and `extractions/`; don't rename it. |
| **Track** | A **named** chunk of work you carry across sessions toward one deliverable — e.g. *the infobox-merge track*. | The name is a deliverable noun phrase. **Never lettered or numbered as its primary identifier** (the old `Track A/B/C` / `Track 1–6` idiom is retired — it was the one genuinely ambiguous term). A Track lives in `working/todos.md` and gets a continue prompt. |
| **step** (lowercase) | An ordered piece of work inside one Track — "step 2 of the infobox track". | The default word for sub-units. It **replaces** the old Stage / Plate / Phase / Wave proliferation — don't mint a fresh word each time you sequence work. Plain lowercase English; not a glossary "term", just the standard word. |
| **Tier** | How much you trust a fact: **1 (verified canon) → 5 (crackpot)**. | **Reserved EXCLUSIVELY for confidence.** Never used for work, process, promotion-classes, or qualifier levels. This is the one rule with teeth — Tier is stamped *on the data* (every edge), so a stray meaning is graph corruption, not just doc friction. Other graded systems use *class* / *level* / *priority*. |

**Version numbers attach only to artifacts** (schema v3, prompt v5, `edges.jsonl` v1.3) — never to
efforts, eras, or workstreams. Always qualify with the artifact name ("Pass-1 prompt v3").

## Retired from reuse (historical-only)

These are valid when **citing a past session** ("the Plate-3 work", "Stage 4 of Pass 2") and never
coined anew. The history glossary decodes them in old docs; living docs use the canonical terms above.

- **Stage, Plate, Phase, Wave, Bucket** → for new sequencing, use lowercase **step**.
- **Mode** → "the validation probes"; "Mode 3" specifically = "the grounded-agent dip".
- **Sprint** → never actually used; ignore.
- **Letter/number tracks** (`Track A/B/C`, `Track W`, `Track 1–6` as identifiers) → use the Track's **name**.
- **Mission / watcher / worker** → stay inside the mission-protocol namespace only; not general vocabulary.

## Exemptions

**Script, file, and registered skill/command names keep their names** — `stage4-*.py`,
`worker-stage4`, `check-fleet`, etc. are functional references wired into the harness and tooling;
renaming them for vocabulary hygiene isn't worth the churn. This glossary carries the mapping.

## Keeping it consistent — how the vocabulary reaches every actor

The hard case is **spawned subagents**: they do not inherit the orchestrator's context and never load
`CLAUDE.md`. So consistency relies on two channels plus a record:

1. **Push** — the orchestrator (which holds the rule via `CLAUDE.md`'s `## Vocabulary` stub) pastes the
   canonical terms into any subagent prompt whose task involves **naming a Track, numbering steps, or
   labeling a sequence**. For `claude -p` subprocesses (cwd=/tmp, no project context) this is the *only*
   channel. This is the same vocab-lockdown discipline already used for edge passes.
2. **Pull** — (queued follow-up) a one-line pointer in the live `.claude/agents/*` definitions:
   *"Before naming or sequencing work, read `reference/glossary.md` and use only those terms."*
3. **Record** — this file is the single source of truth; the worklog Active Decision is the dated
   ratification; `CLAUDE.md` carries the short stub + pointer.

A grep linter (flag retired terms used as *new* coinages in living docs) is **deferred** — build it
only if drift demonstrably recurs, not preemptively.

## Queued follow-ups (NOT done at lock-in; see `working/todos.md`)

- Rename the handful of live **non-confidence "Tier"** uses → *class/level* (architecture.md qualifier
  levels; the wiki promotion-class). The one set of renames that prevents a data error.
- Add the **pull-channel pointer** to the ~8 live `.claude/agents/*` definitions.
- A full retroactive living-doc sweep is **NOT planned** — it was judged churn-for-tidiness (the S102
  "timestamp diffs bury the real change" lesson). The history glossary decodes old docs; we move forward.
