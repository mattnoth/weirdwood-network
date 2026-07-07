# SESSION 197 — Wiki-prose disambiguation composer: cluster pack + Identity dry-run

> **This is Session 197.** Stamp your worklog entry `### Session 197` at endsession.
> **Recommended model:** Sonnet (script-builder-class work — deterministic Python + a dry-run report; no Opus, no Haiku unless the gated residue step triggers later).
> **Gate status:** Matt greenlit the reviewed plan when he fired this prompt (firing it = the go for the BUILD + DRY-RUN; **applying to nodes still needs his explicit go after he reads the preview** — `feedback_no_graph_mutation_without_goahead`). If he fires it with caveats, honor those first.

## Context (1 paragraph)

S196 was a Fable design review of the Fire & Blood enrichment plan (verdict: go-with-changes — `working/fire-and-blood/fable-review.md`). Ruling #10: this **companion track runs FIRST** because its deterministic outputs are the F&B reconciler's inputs. The spec you are executing is **`working/node-enrichment-wiki-prose/design.md` (v2)** — read it top to bottom before writing code; it has the algorithm, data sources, three node shapes, and acceptance criteria. This prompt only orients you.

## Task

Build `scripts/wiki-prose-identity-composer.py` per design §6, with three subcommands:

1. **`--build-pack`** → `working/wiki/data/same-name-clusters.json` + `working/wiki/data/disambig-node-blocklist.json`. Pure joins over: node frontmatter (`name:`, `wiki_source`) × `working/wiki/data/page-categories.jsonl` (life-years from `"NN AC births/deaths"` categories; blocklist from `Disambiguation pages`) × `graph/edges/edges.jsonl` (parents/spouse/allegiance/title). Cluster key = (first-name, surname) after stripping regnal numerals + parentheticals (design §4).
2. **`--compose --dry-run`** → `working/node-enrichment-wiki-prose/preview.md`: per-cluster composed Identity lines + trap-node hub lines + thin-flag counts. **No node writes.**
3. **`--apply`** → NOT this session unless Matt has already said go on the preview. The writer rules (three node shapes, boilerplate exact-regex, insert-if-absent, idempotency, atomic write) are design §2.5/§5 — build the code path, keep it gated.

## Success criteria (from design §6 — verify all before showing Matt)

- Pack: "aegon targaryen" cluster ≥12 members with `aegon-targaryen` in `trap_nodes`; `aegon-targaryen-son-of-baelon` shows born 84 / died 85 (sourced from categories, NOT edges); every blocklist slug's wiki page genuinely carries `Disambiguation pages`.
- Composer dry-run: shapes (a)/(b)/(c) each demonstrated on a named example (see design §2.5); zero writes outside `## Identity` in the planned diffs; thin-rate reported (drives the >20% Haiku-residue decision, design §3).
- End state: preview file + a short chat summary for Matt → his apply-go is the next gate. If he gives it in-session: `--apply` → `weirwood refresh` → spot-check `weirwood query resolve "Jaehaerys"` and the pack consumers.

## DO NOT

- Do NOT write to any `graph/nodes/` file without Matt's explicit apply-go on the preview.
- Do NOT fetch anything from awoiaf.westeros.org (`feedback_no_external_wiki_fetch` — everything is local).
- Do NOT delete/merge the trap nodes — they become hubs (`disambiguation_hub: true`), design §3.6. The frontmatter flag is part of the staged architecture.md batch — if you apply it, update `reference/architecture.md` §Node Frontmatter in the same session (CLAUDE.md rule #6) and log the Active Decision in `worklog.md`.
- Do NOT start any Fire & Blood build steps (splitter/prompt/worker) — that's the next track, sequenced behind this one.
- Do NOT auto-run /endsession.

## After this lands

The F&B track unblocks: architecture.md batch → splitter build → QA gate → two-stage smoke. Its spec: `working/fire-and-blood/fire-and-blood-enrichment-design.md` (v2), sequencing §10.
