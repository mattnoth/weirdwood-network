---
session: 194
date: 2026-07-05
model: Fable 5 (handoff recommended Opus 4.8; Fable ran it — capability step up, flagged at session start)
track: meta (chat-UI)
---

# Session 194 — Receipts rail for all 8 tools + node-UX boost + fuller dossiers + About in Matt's voice — DEPLOYED (ships S193 quotes)

## The S193 discovery (session start)

The handoff said S194 "runs AFTER S193" and its deploy ships the S193 quotes — but
worklog.md and git log both topped out at S192. Investigation: **S193 ran in a remote
cloud container on branch `claude/quote-minting-census-k5lonc`** (pushed, unmerged;
that container had no Netlify credentials, which is also why S193's Matt-approved
deploy was blocked). The branch fast-forwarded cleanly onto main (`d926b8c2b5`), and
its endsession commits carried an addendum to this very session's continue prompt.
Rule-#9 discipline paid off: verify the handoff's claims against worklog/git before
proceeding.

## Design decisions

- **One clickable-node atom.** `nodeChip(slug, name, type)` — a button that opens
  the dossier — is now the single interaction for a node name in every receipt card
  (search/list/theme/neighbors/resolve), matching what the chain spine and family
  tree already did. The neighbors card's `▶ <details>` disclosure rows (the one
  card on a different pattern, Matt: "the expand thing just doesn't really make
  sense") were retired; each neighbor row is chip + always-visible evidence, same
  as spine edges.
- **The affordance is a dotted accent underline** (solid on hover), applied
  uniformly: chips, spine node names, and prose links. One visual grammar for
  "this opens a record." The per-chain "click any node" hint was retired in favor
  of ONE rail header ("How this was answered — live graph lookups, click any name").
- **Prose entity-linking shipped at tier 1 only** (client-side post-stream pass
  over `turn.entities`, the slug→name map every receipt feeds; first occurrence
  per entity, wiki convention; quote blocks untouched; single-word names matched
  case-sensitively so a character named "Will" never claims the verb). **Tier 2
  (model-emitted `[[n|slug|Name]]` markers) was presented to Matt as a design
  decision, not built** — recommendation: judge tier 1 live first. Tier 3
  (full-graph name map to browser) out of scope per the prompt.
- **Dossier "fuller markdown" = ship the body sections via the existing per-node
  asset pipeline.** `build_node_assets.py` now emits `sections: [{heading, text}]`
  for every reader-facing `##` section (Origins, Appearances & Description,
  Culture, Aftermath, Heraldry & Sigil, …). Internal sections never ship:
  Identity/Quotes/Edges (already structured), Narrative Arc (own key), **Notes**
  (curator provenance — the sampled Tywin Notes is a parser-artifact flag), and
  overlay-ledger headings (`book.?cit|overlay|harvest` regex). Assets 4,395 →
  6,693 (20.1 MB total, on-demand per-slug fetch so size is a deploy cost only).
  The netlify build command now regenerates the assets too — before this, a
  clean-checkout deploy would silently ship whatever `web/public/node/` the
  working tree held.
- **Grounding fix (small server change, live-caught):** a turn grounded ONLY by
  list_nodes/theme rows answered fine but tripped the `no-grounding` "no scene
  here" banner — `harvestResult` counted every evidence-bearing tool but not
  `items` rows. Rows now count as grounding (no cites added). Regression test
  pinned.

## Verified live (dev turns, Sonnet, ~pennies)

Three dev questions exercised every new surface: meals (theme + 2 search cards,
37 chips, prose links "harvest feast"/"Purple Wedding"/"bowl of brown", 9 pull
quotes), Davos connections (neighbors 77-out/30-in with chip+evidence rows,
resolve card), materials (list card paging "25 of 58" ×3 + theme + the grounding
mislabel that led to the fix). Dossier verified end-to-end from a prose link:
"Bowl of brown" → 2 quotes + Origins + 4-book narrative arc. Mobile + desktop
rail behavior confirmed (desktop: sticky, scrolls within viewport; mobile: static,
joins page scroll — first attempt LOST the cascade because the mobile media block
sits earlier in app.css than the base `.receipts-col` rule; the override moved
after the base rule).

## About page (two rounds)

First pass: provenance-story rewrite. Matt then dictated his own copy — wiki
credit ("would not be possible without it"), theories-NOT-integrated / no
post-ADWD-outcome-inference disclaimer, "Provenance is the point" killed as
AI-sounding, the citation-gate paragraph corrected to what the UI actually does
(marks the answer unverified; does NOT identify the offending quote), the
trace-to-line claim dropped (markdown line numbers unverified against printed
books), one font size, small "Built by Matt Noth → mattnoth.com" contact line.
One flagged word swap: Matt's "watch the LLM utilizing python scripts" →
"working its graph tools" (the live lookups are the TS tools), offered to revert.
Then title/header: `<title>` = "The Weirwood Network — ASOIAF Knowledge Graph
Interface" + a small header descriptor (hidden <640px).

## Incident (minor, recovered)

A sloppy compound command ran `git stash` mid-session and stashed all working-tree
changes; the harness flagged the files reverting. `git stash pop` restored
everything; suites re-verified green. Lesson: never bundle speculative git
commands into a verification one-liner.

## Deploy

Matt's go at session close. `npx netlify deploy --prod --build` from repo root
(per DEPLOY.md) — build regenerated the 5-file bundle + 6,693 node assets;
4,951 files uploaded; prod-smoked: new title live, `/api/node?slug=lemon-cake`
serves 2 S193 quotes + Culture section + arc. **The S193 quotes are live.**

## Residue (noted, not fixed — S195 vein)

- Some wiki-derived arc/section prose embeds internal provenance lines ("Navigable
  book cite overlay on the wiki cite above") — data artifact in node bodies.
- Some curated quote attributions bake the chapter into both attribution and cite
  ("— ADWD Chapter 66 (Tyrion XII), ADWD Tyrion 12") — `bookQuote`'s dedup only
  catches literal substring matches. Cosmetic.
