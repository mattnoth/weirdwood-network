# Curated-map notes — D&E name resolution

Source review: `out/needs-map.csv` (82 rows), `out/quarantine.jsonl` (218 rows,
cross-checked — no names beyond needs-map required action), `out/emit.jsonl`
(94 `resolved-context-prior` hits audited), `out/identity-flags.jsonl` (17
flags, 5 different-slug flags investigated). All node existence checked
against `graph/nodes/**/*.node.md` — see verification note at bottom.

`curated-map-draft.csv` has 127 rows: 80 mapped, 47 SKIP.

## Non-obvious mappings (name → slug — why)

- **King Daeron / Daeron II / The King → `daeron-ii-targaryen`** — reigning
  king throughout all three novellas (THK ~209 AC, TSS ~211 AC, TMK ~212 AC),
  father of Baelor, Maekar, Aerys, Rhaegel per thk-dunk-01-p05/p06 and
  tmk-dunk-01-p07.
- **Daeron (bare) → SKIP** — genuinely ambiguous within the corpus itself:
  in tmk-dunk-01-p07 ("Daeron | PARENT_OF | King Aerys / Baelor Breakspear /
  Prince Maekar") it's Daeron II; in thk-dunk-01-p05 and tmk-dunk-01-p03
  ("My brother Daeron's dreamed of it") it's Prince Daeron, Maekar's son
  (Egg's brother). A flat name→slug map can't disambiguate a single string
  that means two different people depending on which paragraph it's in.
- **Prince Daeron / Daeron (Egg's brother) → `daeron-targaryen-son-of-maekar-i`**
  — "Daeron the Drunken," Maekar's eldest son, Aerion's brother, Egg's
  brother; distinct from King Daeron II above.
- **Prince Maekar's youngest son → `aegon-v-targaryen`** — this is Egg
  himself; confirmed by thk-dunk-01-p04 ("I cut it off, brother" to Aerion —
  Egg revealed as Maekar's son and Aerion's brother).
- **Aegon Targaryen (bare) → `aegon-v-targaryen`** — in this corpus "Aegon
  Targaryen" without qualifier is Egg's revealed true name (tss-dunk-01-p03:
  "Aegon of House Targaryen was the fourth and youngest son of Maekar").
  The graph's `aegon-targaryen` slug is a 12-way `disambiguation_hub: true`
  stub, never a real person — mapping there was always wrong.
- **Dragonbane / King Aegon (the third) → `aegon-iii-targaryen`** — Ser
  Arlan's tale of the last dragon (thk-dunk-01-p01): "the third Aegon...
  the one they named Dragonbane, or Aegon the Unlucky." `aegon-iii-targaryen`
  carries both exact aliases. This is a Dance-of-Dragons-era king, ~80 years
  before D&E — nothing to do with Egg.
- **old King Aegon / Aegon the Unworthy → `aegon-iv-targaryen`** — the coin-age
  benchmark in tmk-dunk-01-p06, confirmed via identity-flag #14 (Aegon the
  Unworthy resolved correctly elsewhere as alias).
- **Daeron's sister → `daenerys-targaryen-daughter-of-aegon-iv`**, **The
  prince of Dorne → `maron-martell`** — ss-dunk-01-p06: "sold his own sweet
  sister to the prince of Dorne, though it was Daemon that she loved." This
  exact line is quoted verbatim (with wiki cite_refs naming both parties) on
  `daeron-ii-targaryen.node.md` itself — Daenerys Targaryen (daughter of
  Aegon IV) wed to Maron Martell, Prince of Dorne, to bring Dorne into the
  realm (187 AC).
- **Daella → `daella-targaryen-daughter-of-maekar-i`**, **Rhae →
  `rhae-targaryen`** — tss-dunk-01-p03: Egg's two sisters. Both are Maekar's
  daughters, not the ~130-AC-earlier Targaryens the resolver picked (see
  mis-hits below).
- **The Iron Throne → `iron-throne`** (artifact node) — Daemon Blackfyre
  CLAIMS it (tmk-dunk-01-p01); the physical seat/institution node fits.
- **Daemon Blackfyre → `daemon-i-blackfyre`** — the original rebel, Aegon
  IV's elevated bastard, Blackfyre Rebellion (195 AC), distinct from
  `daemon-ii-blackfyre` (John the Fiddler, TMK).
- **Aegon/Aemon (son of Daemon Blackfyre) → `aegon-blackfyre` /
  `aemon-blackfyre`** — the twin sons who died at the Redgrass Field
  (tss-dunk-01-p04); needed an explicit override because "Aemon" bare also
  correctly resolves to Maekar's son elsewhere (see mis-hits below).
- **"the prince" (conspirators' claimant) → `daemon-ii-blackfyre`** —
  tmk-dunk-01-p04's conspiracy scene: the claimant who "dreamed his brothers
  dead" is the Fiddler, per identity-flag #11.
- **King Lancel / King Lancel (fourth or fifth) / Lancel Lannister → SKIP**
  — Ser Eustace's tale of the Little Lion (tss-dunk-01-p02) explicitly says
  "the fourth King Lancel... or mayhaps the fifth," i.e. the text itself is
  unsure whether this ancient King of the Rock is `lancel-iv-lannister` or
  `lancel-v-lannister`. Cannot safely pick one. What's certain: it must
  **never** resolve to the modern `lancel-lannister` (Kevan's son, a
  contemporary of Tyrion) — see mis-hit below.
- **A lord with three castles on his shield → `gormon-peake`** — this exact
  epithet is explicitly unpacked as Gormon Peake in tmk-dunk-01-p01 ("his
  head smashed in by a mace wielded by a lord with three castles on his
  shield at the Redgrass Field — Gormon Peake"); the tss-dunk-01-p04
  occurrence (killing Lord Hayford) uses the identical phrase for the same
  battle, same man.
- **Lord Tully → `lord-tully-successor-of-medgar`** (moderate confidence) —
  THK's Lord Tully (unhorsed by Aerion at Ashford) is unnamed beyond house;
  the node's alias "Young Lord Tully" matches TMK's "Young Lord Tully,
  Butterwell's liege lord" three years later. Plausible same person, not
  certain.
- **the Bastard of Harrenhal → `bastard-of-harrenhal`** — node exists
  (House Lothston bucket), matches the single unnamed mention in the THK
  melee.
- **Pyromancers → `alchemists-guild`** — "Lord Rivers commanded the
  pyromancers to burn them" (tss-dunk-01-p05); pyromancers are the guild's
  members, no separate node exists for the guild-as-acting-collective here.
- **Ser Jay of House Caswell / Lord Joffrey Caswell → `joffrey-caswell`** —
  source text (tmk-dunk-01.md:977) confirms the herald announces "Ser Jay of
  House Caswell" and narration immediately calls him "Lord Joffrey Caswell";
  same person, per identity-flag #12.
- **Ser Theomore Bulwer / Ser Theomore of House Bulwer / the Old Ox →
  `buford-bulwer`** — `sources/wiki/_raw/Theomore_Bulwer.json` is a wiki
  **redirect to Buford Bulwer** (confirmed by reading the cached page). The
  wiki's canonical name for this character is Buford; "Theomore" is the name
  GRRM used in-text. One person, one existing node.

## Namesake mis-hits found in emit.jsonl (resolved-context-prior audit)

All 94 `resolved-context-prior` hits were pulled and cross-checked against
their evidence quotes and the originating Pass-1 extraction tables. Confirmed
wrong resolutions:

| Raw name | Wrong slug | Right slug | Evidence |
|---|---|---|---|
| Lord Quentyn Blackwood | `quentyn-martell` | `quentyn-blackwood` | thk:145, "slaying Lord Quentyn Blackwood... at a tourney at King's Landing" — a Reach lord, not the Dornish prince |
| Aemon (son of Daemon Blackfyre) | `aemon-targaryen-son-of-maekar-i` | `aemon-blackfyre` | tss:703, "Young Aemon took up Blackfyre when the blade slipped from his dying father's fingers" — Daemon I's twin son at Redgrass Field, not Egg's brother |
| Rhae | `rhaena-targaryen-daughter-of-daemon` | `rhae-targaryen` | tss:621, "my sister Rhae" — resolver hit an unrelated node's alias list (`aliases: [..., "Rhae", ...]`) instead of the dedicated Rhae Targaryen (Maekar's daughter) node |
| Daella | `daella-targaryen-daughter-of-jaehaerys-i` | `daella-targaryen-daughter-of-maekar-i` | tss:621, Egg's sister — resolver picked an 82-AC-era Targaryen a century too early |
| Gyles the Third | `gyles-rosby` | `gyles-iii-gardener` | tss:267, "Gyles the Third took his banners east... Gardener King of the Reach" — nothing to do with House Rosby |
| King Lancel (Little Lion tale) | `lancel-lannister` | (ambiguous, see SKIP above) | tss:271 — resolver picked the modern Kevan's-son Lancel via alias `"lancel"`, definitely wrong era |
| Lord Rowan | `rowan` | (no correct node, see SKIP above) | tss:1065/301 — `rowan.node.md` is `SWORN_TO: Mance Rayder`, an ADWD wildling, not the Reach lord |
| Lord Wyman | `wyman-manderly` | `wyman-webber` | tss:1699 etc. — resolver hit the main-series White Harbor Manderly instead of Rohanne's father, whose own dedicated node (`wyman-webber`) already exists |
| Lord Tybolt | `tybolt-lannister` | *(confirmed correct, not a mis-hit)* | node says "d. 212 AC," matches TSS (~211 AC) exactly |
| Lord Costayne | `lord-costayne-aerys-i` | *(confirmed correct, not a mis-hit)* | node is explicitly the Aerys-I-era Costayne |
| Ser Theomore Bulwer | `theomore-manderly` | `buford-bulwer` | tmk:1393 — resolver hit a Manderly namesake instead of the Bulwer wiki-redirect target |
| Ser Clarence Charlton | `clarence-crabb` | `clarence-charlton` | tmk:1375, "making short work of Ser Clarence Charlton" — resolver hit the legendary outlaw Clarence Crabb by first-name match |
| Three Kingsguard | `three-sisters` | SKIP (collective, no node) | thk:1341, "demanded that the Kingsguard fight for his son" — resolver matched a place-name node via the word "three" |
| three suitors of Butterwell's eldest daughter | `three-sisters` | SKIP (collective, no node) | tmk:611, "killing three of her other suitors" — same false "three" match |
| Sons of Daemon Blackfyre | `sons-of-the-harpy` | SKIP (collective, ambiguous individual) | tss:933, "Bittersteel and the sons of Daemon Blackfyre... in Tyrosh" — resolver matched an unrelated Meereenese faction |
| Lord Lannister | `lannister-reprisal-on-the-iron-islands` | `damon-lannister` | thk-dunk-01-p06:274, "Lord Lannister... The Grey Lion" — resolver matched an **event** node, not a character, via a bad firstname-index entry |

Also found via `identity-flags.jsonl` #1: **"King Aegon (the third)" resolved
to `aegon-v-targaryen`** instead of `aegon-iii-targaryen` — same historical
Dragonbane/Unlucky confusion as above, fixed by the override.

## Identity-flag investigations (the 5 different-slug flags)

1. **Red Widow / Lady Webber** — `rohanne-webber` vs `webber`. Source
   (tss-dunk-01-p01): "The Red Widow, she was called... Lady Webber."
   `webber.node.md` is an empty stub (no identity text, no aliases) —
   clearly a mis-resolution, not a second real person. **Recommendation:**
   both sides are the same person; "Lady Webber" should resolve to
   `rohanne-webber` (added as a curated-map override). Not an extraction
   slip — Dunk really is addressing Rohanne both times, the resolver just
   grabbed the wrong node for the honorific form.

2. **Treb / Will** — `treb` vs `will`, both from tss-dunk-01-p02: "After
   that the man was known as Treb" (the rock-chucker's new name after an
   incident). Both `treb.node.md` and `will.node.md` are real wiki-sourced
   nodes for what the text says is **one** character before/after a
   nickname change. This is not a name-resolution bug — the curated-map
   can't merge two distinct existing node files. **Recommendation:** this
   is a genuine duplicate-node case (Will = Treb, same person under an old
   and new name) that belongs to node curation / cross-identity-detector
   territory, not the curated-map. Flagging for a SAME_AS node-level
   decision outside this task's scope.

3. **Egg / Aegon Targaryen** — `aegon-v-targaryen` vs `aegon-targaryen`.
   `aegon-targaryen` is a 12-way disambiguation hub (`disambiguation_hub:
   true`), never a real person node. **Recommendation:** "Aegon Targaryen"
   should resolve to `aegon-v-targaryen` (added as a curated-map override,
   see above) — this is a straightforward resolver mis-hit, not an
   extraction slip.

4. **Theomore Bulwer / the Old Ox** — `theomore-manderly` vs `buford-bulwer`.
   Confirmed via the wiki cache that `Theomore_Bulwer.json` is a **redirect**
   to `Buford_Bulwer.json` — the wiki's canonical name for this exact TMK
   character is Buford. **Recommendation:** both sides should resolve to
   `buford-bulwer` (added as curated-map overrides for both "Ser Theomore
   Bulwer" and "the Old Ox"). Not an extraction slip; a straightforward
   mis-resolution now fixed. Worth a follow-up (out of scope here): adding
   "Theomore" / "Theomore Bulwer" to `buford-bulwer.node.md`'s `aliases:`
   list so future non-curated-map resolution succeeds too.

5. **The Brown Dragon / Glendon Ball** — `daemon-ii-blackfyre` vs
   `glendon-flowers`. Source (tmk:1793 area): "'The Brown Dragon!' shouted
   after Glendon unhorses the mud-covered Daemon." Both resolved slugs are
   individually **correct** — "the Brown Dragon" is the crowd's mocking
   nickname for Daemon (now mud-covered), and Glendon Ball is the separate
   knight who unhorsed him. **Recommendation:** this is a Pass-1 extraction
   labeling slip, not a name-resolution problem — the `ALIAS_OF` relation
   between them is wrong (they are not the same person; the sentence
   structure was misread as an alias rather than "Glendon defeated the
   [now-nicknamed] Brown Dragon"). No curated-map action needed; flag for
   Pass-1 relationship-vocabulary review if that track resumes.

## Could not settle

- **Daeron (bare)** — see above; context-dependent, left SKIP.
- **King Lancel / Lancel Lannister (Little Lion tale)** — ambiguous between
  `lancel-iv-lannister` and `lancel-v-lannister` per the source text's own
  hedging; left SKIP.
- **Lord Tully** (THK) — mapped to `lord-tully-successor-of-medgar` but only
  at moderate confidence (inferred from the TMK "Young Lord Tully" alias
  match, not a direct textual link).
- **Lord Lefford** (killed by Fireball at Lannisport) — no confirmed
  era-matched individual node found among `house-lefford`'s several
  characters; left SKIP rather than guess.
- **Lord Rowan** — no D&E-era character node exists at all; `house-rowan`
  (the house node) actually contains the exact matching prose ("Lord Rowan
  was distant kin to Lady Rohanne Webber...") but mapping a character
  reference to a house-type node would be a type mismatch, so left SKIP.
- **Sons of Daemon Blackfyre** — collective/plural reference to surviving
  Blackfyre kin plotting in Tyrosh (tss-p05); no single individual is named,
  left SKIP rather than force a `house-blackfyre` mapping that would blur
  the "sons of Daemon I specifically" framing.

## Verification

Every non-SKIP slug in `curated-map-draft.csv` (80 of 127 rows) was checked
against `graph/nodes/**/*.node.md` (9,232 node files) and confirmed to
exist. 47 rows are SKIP (unnamed/generic/collective entities with no
dedicated node, or genuinely ambiguous names) — no new nodes were proposed
or minted anywhere in this task.
