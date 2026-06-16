# Event Dating Dry-Run Report

Generated: 2026-06-16  |  Mode: --apply

## Counts

| Category | Count |
|----------|-------|
| CLEAN (single-year, node exists, will write) | 0 |
| MULTIYEAR (staged, not written) | 5 |
| NOMATCH (no node file, not written) | 1 |
| ALREADY_DATED (skipped, idempotent) | 112 |
| BLOCKLISTED (hard-excluded) | 4 |
| **Total event-typed slugs in chronology** | **122** |

## Apply Results

- Written: 0
- Skipped (already dated): 0
- Errors: 0

## CLEAN — Full Table (slug → ac_year)

These 0 nodes have exactly one attested year and will be dated.

| slug | ac_year |
|------|---------|

## MULTIYEAR — Staged (needs ac_year_end or split decision)

These 5 slugs span multiple attested years. Not written.

| slug | distinct years |
|------|---------------|
| `dance-of-the-dragons` | [129, 130, 131, 132] |
| `first-blackfyre-rebellion` | [196, 212] |
| `greyjoy-rebellion` | [289, 290] |
| `regency-of-aegon-iii` | [131, 136] |
| `war-of-the-five-kings` | [298, 299, 300] |

## NOMATCH — Staged (event year exists, no node file)

These 1 slugs appear in chronology with `target_type: event.*` but have no node file in `graph/nodes/events/`.

- `moon-of-the-three-kings`: [130]

## ALREADY_DATED (idempotent skips)

- `arrest-of-eddard-stark`: existing ac_year=298
- `assault-on-dragonstone`: existing ac_year=284
- `assault-on-harrenhal`: existing ac_year=129
- `attack-on-castle-black`: existing ac_year=299
- `battle-above-the-gods-eye`: existing ac_year=130
- `battle-at-acorn-hall`: existing ac_year=130
- `battle-at-the-burning-septry`: existing ac_year=299
- `battle-at-the-red-fork`: existing ac_year=130
- `battle-beneath-the-gods-eye`: existing ac_year=43
- `battle-beneath-the-wall`: existing ac_year=300
- `battle-by-the-lakeshore`: existing ac_year=130
- `battle-in-the-hills-below-the-golden-tooth`: existing ac_year=298
- `battle-in-the-whispering-wood`: existing ac_year=299
- `battle-near-yunkai`: existing ac_year=299
- `battle-of-ashford`: existing ac_year=282
- `battle-of-oxcross`: existing ac_year=299
- `battle-of-the-bells`: existing ac_year=283
- `battle-of-the-blackwater`: existing ac_year=299
- `battle-of-the-burning-mill`: existing ac_year=129
- `battle-of-the-camps`: existing ac_year=299
- `battle-of-the-fords`: existing ac_year=299
- `battle-of-the-gullet`: existing ac_year=130
- `battle-of-the-honeywine`: existing ac_year=130
- `battle-of-the-kingsroad`: existing ac_year=131
- `battle-of-the-redgrass-field`: existing ac_year=196
- `battle-of-the-trident`: existing ac_year=283
- `battle-of-wendwater-bridge`: existing ac_year=236
- `battle-on-the-green-fork`: existing ac_year=299
- `battle-outside-the-gates-of-winterfell`: existing ac_year=299
- `battle-under-the-walls-of-riverrun`: existing ac_year=298
- `battles-at-summerhall`: existing ac_year=282
- `burning-of-pinkmaiden-castle`: existing ac_year=298
- `burning-of-stone-hedge`: existing ac_year=298
- `capture-of-darry`: existing ac_year=298
- `capture-of-winterfell`: existing ac_year=299
- `conquest-of-dorne`: existing ac_year=161
- `defenestration-of-sunspear`: existing ac_year=5
- `faith-militant-uprising`: existing ac_year=41
- `fall-of-dragonstone`: existing ac_year=130
- `fall-of-harrenhal`: existing ac_year=299
- `fall-of-moat-cailin`: existing ac_year=299
- `fall-of-raventree-hall`: existing ac_year=298
- `fight-above-shipbreaker-bay`: existing ac_year=129
- `fight-at-the-bridge-of-skulls`: existing ac_year=299
- `fight-at-the-fist`: existing ac_year=299
- `fight-at-the-holdfast`: existing ac_year=299
- `fight-by-deepwood-motte`: existing ac_year=300
- `first-battle-of-tumbleton`: existing ac_year=130
- `first-sack-of-maidenpool`: existing ac_year=298
- `fourth-blackfyre-rebellion`: existing ac_year=236
- `fourth-dornish-war`: existing ac_year=83
- `golden-wedding`: existing ac_year=49
- `great-spring-sickness`: existing ac_year=209
- `harrying-of-the-stony-shore`: existing ac_year=299
- `harvest-feast-299`: existing ac_year=299
- `invasion-of-the-iron-islands`: existing ac_year=2
- `kingsmoot-on-old-wyk`: existing ac_year=300
- `landing-of-the-golden-company`: existing ac_year=300
- `liberation-of-raventree-hall`: existing ac_year=299
- `liberation-of-stone-hedge`: existing ac_year=299
- `lysene-spring`: existing ac_year=135
- `mutiny-at-castle-black`: existing ac_year=300
- `peake-uprising`: existing ac_year=233
- `purple-wedding`: existing ac_year=300
- `raiding-along-the-westerlands-coast`: existing ac_year=299
- `recapture-of-darry`: existing ac_year=299
- `red-wedding`: existing ac_year=299
- `reyne-tarbeck-revolt`: existing ac_year=261
- `sack-of-bitterbridge`: existing ac_year=130
- `sack-of-darry`: existing ac_year=299
- `sack-of-duskendale`: existing ac_year=129
- `sack-of-winterfell`: existing ac_year=299
- `second-battle-of-tumbleton`: existing ac_year=130
- `second-blackfyre-rebellion`: existing ac_year=212
- `second-dornish-war`: existing ac_year=37
- `second-quarrel`: existing ac_year=92
- `secret-siege`: existing ac_year=135
- `seizure-of-westerlands-gold-mines`: existing ac_year=299
- `siege-of-astapor`: existing ac_year=300
- `siege-of-darry`: existing ac_year=299
- `siege-of-dragonstone`: existing ac_year=300
- `siege-of-longtable`: existing ac_year=130
- `siege-of-moat-cailin`: existing ac_year=300
- `siege-of-raventree`: existing ac_year=300
- `storming-of-the-crag`: existing ac_year=299
- `storming-of-the-dragonpit`: existing ac_year=130
- `taking-of-ashemark`: existing ac_year=299
- `taking-of-deepwood-motte`: existing ac_year=299
- `taking-of-gulltown`: existing ac_year=282
- `taking-of-stone-hedge`: existing ac_year=129
- `taking-of-the-shields`: existing ac_year=300
- `third-blackfyre-rebellion`: existing ac_year=219
- `tourney-at-harrenhal`: existing ac_year=281
- `tourney-at-lannisport`: existing ac_year=289
- `vulture-hunt`: existing ac_year=37
- `war-for-the-stepstones`: existing ac_year=106
- `war-of-the-ninepenny-kings`: existing ac_year=260
- `wedding-of-drogo-and-daenerys-targaryen`: existing ac_year=298
- `wedding-of-hizdahr-zo-loraq-and-daenerys-targaryen`: existing ac_year=300
- `wedding-of-lyonel-corbray-and-lady-corbray`: existing ac_year=300
- `wedding-of-petyr-baelish-and-lysa-arryn`: existing ac_year=300
- `wedding-of-ramsay-bolton-and-arya-stark`: existing ac_year=300
- `wedding-of-renly-baratheon-and-margaery-tyrell`: existing ac_year=299
- `wedding-of-rhaena-targaryen-and-androw-farman`: existing ac_year=49
- `wedding-of-roose-bolton-and-walda-frey`: existing ac_year=299
- `wedding-of-sigorn-and-alys-karstark`: existing ac_year=300
- `wedding-of-tommen-i-baratheon-and-margaery-tyrell`: existing ac_year=300
- `wedding-of-tyrek-lannister-and-ermesande-hayford`: existing ac_year=299
- `wedding-of-tyrion-lannister-and-sansa-stark`: existing ac_year=299
- `wedding-of-walder-frey-and-joyeuse-erenford`: existing ac_year=298
- `wildfire-plot`: existing ac_year=283
- `yielding-of-harrenhal`: existing ac_year=298

## BLOCKLISTED (hard-excluded)

- `first-dornish-war`: [4, 5, 9, 10, 12, 13]
- `great-council`: [101, 103, 233]
- `long-night`: [297]
- `tourney`: [209, 295]

## Narrative First — DRY-RUN (compute only, NOT written to nodes)

Candidate `narrative_first` = minimum (book_order, chapter_number) across edges for each CLEAN event.

**Format note:** edges.jsonl contains two chapter-ref formats:
  - kebab: `agot-arya-01`
  - roman-style: `ASOS Catelyn VII`
Normalization is best-effort. Mixed-format nodes are flagged.

| slug | candidate_book_order | candidate_chapter | raw_ref | confidence | issues |
|------|---------------------|------------------|---------|------------|--------|
