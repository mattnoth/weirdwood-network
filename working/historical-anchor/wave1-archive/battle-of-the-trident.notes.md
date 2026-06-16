# battle-of-the-trident — Historical Anchor Notes

**Hub slug:** battle-of-the-trident
**Produced:** 2026-06-15

## Pre-flight checks

- **PART_OF roberts-rebellion** already existed (1 outgoing edge confirmed via `--neighbors`). NOT re-emitted.
- **LOCATED_AT**: `ruby-ford` node exists (place.location, aliases: "Ruby Ford, the ford, chief crossing of the Trident"). Emitted.
- **No trident / the-trident / river-trident place node** found. `ruby-ford` is the correct and specific location for this battle.

## Edge counts

| Role | Count |
|------|-------|
| LOCATED_AT | 1 |
| AGENT_IN | 1 (robert-baratheon) |
| VICTIM_IN | 1 (rhaegar-targaryen) |
| COMMANDS_IN | 1 (jon-arryn) |
| FIGHTS_IN | 7 (barristan-selmy, lewyn-martell, lyn-corbray, jason-mallister, eddard-stark, hoster-tully, jonothor-darry, wyman-manderly) |

**Total edges emitted: 12**

## Evidence split

| Tier | Count | Notes |
|------|-------|-------|
| book-pass1, confidence_tier 1 | 6 | robert-baratheon AGENT_IN, rhaegar-targaryen VICTIM_IN, barristan-selmy FIGHTS_IN, lewyn-martell FIGHTS_IN, lyn-corbray FIGHTS_IN, jason-mallister FIGHTS_IN |
| book-pass1, confidence_tier 2 | 1 | eddard-stark FIGHTS_IN (recalled in first-person by Ned, not direct narration of his fighting) |
| wiki-historical-anchor, confidence_tier 2 | 5 | LOCATED_AT ruby-ford, jon-arryn COMMANDS_IN, hoster-tully FIGHTS_IN, jonothor-darry FIGHTS_IN, wyman-manderly FIGHTS_IN |

## Key book quotes used

- `agot-eddard-01.md:79` — Eddard's memory of the duel: "a crushing blow from Robert's hammer stove in the dragon and the chest beneath it. When Ned had finally come on the scene, Rhaegar lay dead in the stream" → AGENT_IN + VICTIM_IN at tier-1.
- `agot-eddard-08.md:43` — Ned to Renly: "On the Trident, Ser Barristan here cut down a dozen good men, Robert's friends and mine." → FIGHTS_IN for Barristan (tier-1); also grounds Eddard's presence (tier-2, recalled).
- `affc-alayne-01.md:67` — Petyr on Lyn Corbray: "Lyn led his charge against the Dornishmen threatening Robert's left, broke their lines to pieces, and slew Lewyn Martell." → FIGHTS_IN for both lyn-corbray and lewyn-martell at tier-1.
- `agot-sansa-02.md:15` — Septa Mordane: "He had cut down three of Rhaegar's bannermen on the Trident." → FIGHTS_IN jason-mallister tier-1.

## Modeling decisions

- **Robert Baratheon**: AGENT_IN only (spec says AGENT_IN captures the signature act; FIGHTS_IN would be redundant; he is not also separately emitted as COMMANDS_IN).
- **Rhaegar Targaryen**: VICTIM_IN only (he also commanded the royalists, but spec says single best-fitting type; being killed is more specific than commanding).
- **Jon Arryn**: COMMANDS_IN rather than FIGHTS_IN — wiki body frames him as co-commander of the rebel coalition host; no book quote places him in the fighting personally. Tier-2.
- **Jonothor Darry**: FIGHTS_IN at tier-2 — the book (asos-jaime-05.md:53) places him rallying forces pre-battle at Stoney Sept, but as a Kingsguard he accompanied Rhaegar's army to the Trident. Wiki body says "Ser Barristan Selmy and Ser Jonothor Darry, also of the Kingsguard, were sent to rally the scattered forces of Lord Connington" — wiki is the source, tier-2.

## Unresolved / skipped participants

- **Lord Corbray (father of Lyonel)** — wiki node body references "Lord Corbray" falling wounded (the elder). The node slug `lord-corbray-father-of-lyonel` was not tested; this figure is peripheral (fell wounded, didn't fight through the battle). Skipped — not a named node likely to exist under a clean slug.
- **Bartimus** — mentioned as saving Wyman Manderly's life. Not a major figure; skipped. No slug tested.
- **Mors Umber's sons** — "the sons of Mors Umber were killed at the Trident" but these are unnamed individuals. Skipped.
- **Lord Grandison** — "died a year later from wounds sustained in the fighting." Node not tested; fringe figure. Skipped.
- **Dornishmen (faction)** — 10,000 Dornishmen under Lewyn Martell; no individual node beyond Lewyn. Skipped.
- **Elder Brother (Quiet Isle)** — "says he 'died' in the Battle of the Trident and was reborn on the island." This is metaphorical language (spiritual rebirth). Skip FIGHTS_IN: the man was a fighter at the Trident but the Elder Brother node, if it exists, represents a post-battle identity. Deferred for a separate decision.
