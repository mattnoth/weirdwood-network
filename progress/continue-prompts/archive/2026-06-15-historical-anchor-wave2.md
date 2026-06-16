# Continue — Historical-Anchor Structural Attachment, WAVE 2 (POST-PLATE-5 followup #9)

> **Recommended model:** Sonnet 4.6 — deterministic surfacing + per-hub research subagents + mechanical validation. Opus only to orchestrate if you want insurance on a graph-mutating run.
>
> **Status (2026-06-15, S97):** Wave 1 SHIPPED (8 Robert's-Rebellion / R+L=J hubs, +118 edges, edges.jsonl 21,829 → 21,947). This prompt is the OPTIONAL wave-2 continuation. Not urgent — wave 1 already cleared the dip's named gaps (Q5 Harrenhal, Q10 Trident).

## What this track is
Major historical event hubs sit ISOLATED in the graph (0–2 edges) even though their facts
already exist — in the hub's own wiki node body (Known Attendees / battle results) and, for
some participants, as cited Pass-1 book dyads. The fix = mint attach edges (participants →
hub via FIGHTS_IN/ATTENDS/AGENT_IN/VICTIM_IN/COMMANDS_IN; hub → place via LOCATED_AT; hub →
war via PART_OF). NO new fact extraction — connect what exists. Dip §6 Q5 is the prototype.

## What wave 1 did (reuse this exact machine)
- **Spec the subagents follow:** `working/historical-anchor/SPEC.md` (edge types, provenance rules, output schema).
- **Surfacing:** `scripts/historical-anchor-candidates.py` (finds isolated hist hubs; note: its blind quote-matcher is NOISY — used only for sizing, NOT for picking. Curate target hubs by hand from the isolated-hub list it prints.)
- **Per-hub research:** one Sonnet `general-purpose` subagent per hub, each writing `working/historical-anchor/<hub>.candidates.jsonl` + `.notes.md`. Prompts embedded the hub's known participants + place/war slugs + "verbatim-quote-only, no meta-descriptions."
- **Validation:** `scripts/historical-anchor-validate.py` — checks JSON, slug resolution, book quotes verbatim-in-chapter, wiki quotes verbatim-in-node-body-or-raw-json (strips `[x](wiki:)` markup). MUST reach 0 issues before mint.
- **Mint:** `scripts/historical-anchor-mint.py` — DROP list + quote-FIX list (curator dispositions) + dedup vs edges.jsonl; `--apply` backs up + appends. Re-validate the `_merged.candidates.jsonl` (0 issues) before `--apply`.

## Provenance discipline (HARD — core project value)
- Tier-1 ONLY from a real book quote. Wiki-only attendees → `evidence_kind: "wiki-historical-anchor"`, `evidence_ref: "wiki:<Page>"`, `confidence_tier: 2` MAX.
- Every `evidence_quote` must be a VERBATIM substring of its cited source. Watch for two wave-1 failure modes the validator now catches: (1) meta-descriptions ("listed in Known Attendees") instead of real quotes; (2) semantically-wrong grounding (a verbatim quote that doesn't support the asserted role — e.g. a wedding quote under COMMANDS_IN; Theon's hostage-quote under FIGHTS_IN). Drop or repoint those.

## Wave-2 candidate hubs (curate; don't mass-mint)
Target main-saga-RECALLED historical events that POV characters witnessed or vividly remember
(so book dyads + rich wiki bodies exist). Likely set, pending a degree check (`scripts/historical-anchor-candidates.py` lists isolated hubs):
- **WO5K battles POV chars were present at** (check current degree first — many may already have infobox/Pass-1 edges): `battle-of-oxcross`, `battle-of-the-green-fork`, `battle-of-the-camps`, `battle-of-the-fords`, `sack-of-winterfell` / `capture-of-winterfell`, `siege-of-riverrun`, `siege-of-storms-end` (Davos/Stannis). Skip any already well-connected.
- **Other named tourneys with on-page/recalled detail:** `tourney-at-lannisport` (Tournament in honor of Viserys's birth), `ashford-tourney` / `tourney-at-ashford-meadow` (D&E — only if D&E nodes resolve), `melee-at-bitterbridge`.
- **D> approach (b) deep-lore wiki-only set** (Doom of Valyria, Blackfyre Rebellions, Targaryen Conquest, etc.): LOWER value — no Pass-1 anchor, pure `wiki-historical-anchor`. Defer unless a future dip shows agents asking about them.

## Hard rules
- No writes to `sources/`. Backup before any `edges.jsonl` write (the mint script does this). Do NOT auto-`/endsession`.
- Re-validate to 0 issues before `--apply`. Verify after: `--health` (orphans not worse), flagship `--neighbors`, pytest (3 documented pre-existing fails OK: vocab-count 166≠163 ×2, cwd-is-tmp).
- No new NODES expected (hubs + participants already exist). If a needed participant has no node, SKIP + list under `unresolved` — never invent nodes.

## Downstream queue (Matt's sequence)
- After #9 fully done → **Track 6 / B — script consolidation / hygiene** (MATT DIRECTIVE 2026-06-14; own session; standardize long-runs onto `longrun.sh` + `weirwood run`; archive dead one-offs). The 3 new `historical-anchor-*.py` scripts are one-offs that could fold into that cleanup.
- Narrative-arc wave 1 mint (`progress/continue-prompts/2026-06-15-arc-wave1-mint.md`) remains DRAFTED + reviewed but UNMINTED — still gated on Matt's 3 open decisions (RW-4 parent role edges, arc boundaries, RECIPIENT_IN vocab). De-prioritized by the dip; pick up when Matt wants it.
