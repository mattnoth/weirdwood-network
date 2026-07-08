# Fresh adversarial verify — 4 CREATE candidates (fab-heirs-of-the-dragon-15-p01)

Date: 2026-07-07 · Verifier: fresh read-only subagent · Method: graph-wide Grep (names, years, participants, aliases) + local wiki cache cross-check. No network.

## Verdict table

| Candidate | Verdict | Existing node |
|---|---|---|
| `baelon-avenges-aemon-on-tarth` | **DUPE-OF: `myrish-bloodbath`** | `graph/nodes/events/myrish-bloodbath.node.md` (tier-1) |
| `nghai` | **SAFE-TO-CREATE** | none (prose mentions only) |
| `great-tourney-of-the-fiftieth-year` | **SAFE-TO-CREATE** (naming/type notes below) | none |
| `summoning-of-vaegon` | **SAFE-TO-CREATE** (edge to Great Council required) | none |

## Evidence per candidate

### 1. `baelon-avenges-aemon-on-tarth` — DUPE-OF: `myrish-bloodbath`
Same failure class as the `aegons-second-coronation` → `aegons-coronations` precedent.

- Existing node `graph/nodes/events/myrish-bloodbath.node.md` (event.battle, tier-1, wiki_source Myrish_Bloodbath) narrates this exact event end-to-end: Myrish exiles seize eastern Tarth → Prince Aemon killed by a Myrish crossbow bolt in **92 AC** → "Prince Baelon Targaryen, enraged at his brother's death, soon arrived on his dragon Vhagar, and burned all the Myrish ships … wiped out the Myrish invaders, cutting down thousands and leaving them to rot along the beaches of Tarth."
- Candidate's entire body is "Myrmen driven into the sea" (92 AC, event.battle) — that IS the Myrish Bloodbath climax.
- Corroboration: `graph/nodes/characters/baelon-targaryen-son-of-jaehaerys-i.node.md:49` ("Baelon flew on Vhagar to Tarth to avenge his brother") and :65 explicitly names it "during the [Myrish Bloodbath](wiki:Myrish_Bloodbath)".
- Note: `graph/nodes/events/invasion-of-tarth.node.md` is a DIFFERENT event (Golden Company, ADWD era) — not the dupe target.
- **Action: do not create. Attach the F&B enrichment (and `occurred: 92 AC` sort key — the existing node has null sort_keys) to `myrish-bloodbath`.**

### 2. `nghai` — SAFE-TO-CREATE
- `find graph/nodes -iname "*ghai*"` → no node under any type dir; no alias hits.
- N'ghai appears only as prose mentions in existing nodes: `graph/nodes/locations/nefer.node.md` (:25, :33 — "remnants of the kingdom of N'ghai"), `locations/mossovy.node.md`, `locations/thousand-islands.node.md`, `concepts/great-voyages.node.md`, `concepts/necromancy.node.md`, `characters/corlys-velaryon.node.md`.
- Wiki cache: `sources/wiki/_raw/N'Ghai.json` is a **redirect page** ("Redirect to: N'ghai") — the case-collision class means the canonical `N'ghai` article body may have been overwritten on the case-insensitive FS. Canonical title: **N'ghai** (lowercase g) — candidate name matches.
- Caution (not a dupe issue): candidate body is nearly empty (F&B section blank). Suggest edges: NEAR/relates to `nefer` (its remnant capital region) and mention-link from `corlys-velaryon` third voyage.

### 3. `great-tourney-of-the-fiftieth-year` — SAFE-TO-CREATE
- Adversarial suspect `graph/nodes/events/tourney-at-kings-landing-on-the-anniversary-of-the-kings-coronation.node.md` is a **different tourney**: celebrates "the first decade" of Jaehaerys's reign (~58 AC), young Ryam Redwyne sole champion. Candidate = **98 AC, fiftieth year, Ryam Redwyne + Clement Crabb co-champions**. Distinct events, both real.
- Scanned all 25 `tourney*` event nodes + `anniversary-tourney` (Aerys II, 272 AC) — no 98 AC node exists.
- The 98 AC tourney is narrated only inside `characters/clement-crabb.node.md:27`, `characters/ryam-redwyne.node.md:39`, `events/tourney-grounds-kings-landing.node.md:36`. No dedicated wiki page exists (checked all `sources/wiki/_raw/*[Tt]ourney*`); `List_of_tourneys_in_Westeros` names it "Tourney to celebrate the fiftieth year of King Jaehaerys's reign" — add as alias.
- Schema note: existing tourney nodes use type `event.tournament`; candidate uses `event.tourney` — normalize before create.

### 4. `summoning-of-vaegon` — SAFE-TO-CREATE (wire edges)
- No event node exists: no Vaegon/Baelon/summon hits across `graph/nodes/events/`; `great-council-of-101-ac.node.md` is a 27-line Path-B stub with empty Edges (and is mistyped `event.battle`, incidentally).
- The event is narrated in `characters/vaegon-targaryen.node.md:40`, matching the candidate's disputed framing exactly: "According to some, Jaehaerys summoned Vaegon to offer him the throne (which Vaegon refused); according to others Jaehaerys only sought Vaegon's counsel … It was Vaegon who eventually suggested that the king should call a Great Council."
- **Required edges on create: CAUSES → `great-council-of-101-ac`** (Vaegon's suggestion convened it) and PRECEDES → same; TRIGGERED_BY/context: death of Baelon (101 AC — no death-of-baelon event node exists either).

## Incidental flags (out of scope, surfaced for triage)
- Pre-existing character dupe pair: `graph/nodes/characters/vaegon.node.md` (wiki "Vaegon" stub) vs `characters/vaegon-targaryen.node.md` — candidate for SAME_AS/merge review.
- `great-council-of-101-ac.node.md` typed `event.battle` (should be event.council) with empty body/edges — enrichment target.
- All 4 candidates stamped `era: dance-of-dragons`, but the events are 92–101 AC (Jaehaerys's reign, pre-Dance) — era stamp looks unit-level, not event-level.
