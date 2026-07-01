# Epithet Redirect Alias Backfill Report

Harvests `"The …"`-prefixed wiki redirect pages from the local `sources/wiki/_raw/` cache and resolves each redirect target to a graph node slug, so epithet-form queries ("the hound", "the red viper", "the queen who never was") resolve in the chat-UI alias lookup.

Read-only on `sources/`. No writes to `graph/nodes/` or `graph/edges/edges.jsonl`.

## Summary

- `"The_*"` pages found on disk: **792**
- Of those, genuine MediaWiki redirects: **671**
- Non-redirect "The …" pages skipped (real content pages — episode titles, in-world texts, etc.): **121**
- Resolved via node-direct (kebab-slug(target) is a real node): **455**
- Resolved via existing-index (target phrase already resolves): **5**
- Unresolved (target didn't resolve anywhere — skipped, not guessed): **211**
- Total distinct redirect-title phrases emitted: **460**
- **NEW** phrases not already present in `all-node-alias-lookup.json` pre-backfill: **111**

## Examples — resolved via node-direct

- `The Abomination on the Iron Throne` → `Maegor I Targaryen` → `maegor-i-targaryen`
- `The Adventurers` → `Adventurers` → `adventurers`
- `The Andal` → `Jorah Mormont` → `jorah-mormont`
- `The Annals of the Black Centaur` → `Annals of the Black Centaur` → `annals-of-the-black-centaur`
- `The Antlers` → `Antlers` → `antlers`
- `The Anvil` → `Maekar I Targaryen` → `maekar-i-targaryen`
- `The Arbor` → `Arbor` → `arbor`
- `The Arrow of Jhahar` → `Xanda Qo` → `xanda-qo`
- `The Axe` → `Axe` → `axe`
- `The Barrowlands` → `Barrowlands` → `barrowlands`
- `The Bastard King` → `Addam Rivers` → `addam-rivers`
- `The Bastard of Barrowton` → `Denys Snow` → `denys-snow`
- `The Bastard of Bitterbridge` → `Tom Flowers` → `tom-flowers`
- `The Bastard of Bolton` → `Ramsay Snow` → `ramsay-snow`
- `The Bastard of Bronzegate` → `Cedrik Storm` → `cedrik-storm`
- … and 440 more

## Examples — resolved via existing-index (transitive chain)

- `The Hand's tourney` → `Hand's tourney` → `the-hands-tourney`
- `The Hound` → `Hound` → `sandor-clegane`
- `The Ice Dragon (Novel)` → `The Ice Dragon` → `ice-dragon`
- `The Maid of Tarth` → `Brienne of Tarth` → `brienne-tarth`
- `The gift of mercy` → `Gift of mercy` → `the-gift-of-mercy`

## Examples — unresolved (skipped, not guessed)

- `The Age of Heroes` → `The World of Ice & Fire` (no node / no index hit)
- `The Andals Arrive` → `The World of Ice & Fire` (no node / no index hit)
- `The Arrival of the Andals` → `The World of Ice & Fire` (no node / no index hit)
- `The Arrival of the Targaryens` → `The Rise of the Dragon` (no node / no index hit)
- `The Art of Ice and Fire` → `The Art of George R. R. Martin's A Song of Ice and Fire` (no node / no index hit)
- `The Ascension of Jaehaerys I` → `Fire & Blood` (no node / no index hit)
- `The Basilisk Isles` → `The World of Ice & Fire` (no node / no index hit)
- `The Beast` → `List of characters created for the Telltale game` (no node / no index hit)
- `The Black Blood` → `The World of Ice & Fire` (no node / no index hit)
- `The Black Brides` → `Black Brides` (no node / no index hit)
- `The Black Brides (The Rise of the Dragon)` → `The Rise of the Dragon` (no node / no index hit)
- `The Blacks and the Greens` → `The Princess and the Queen` (no node / no index hit)
- `The Breaking` → `The World of Ice & Fire` (no node / no index hit)
- `The Brutal Cost of Redemption` → `Beyond the Wall (book)` (no node / no index hit)
- `The Chainmaker` → `Chainmaker` (no node / no index hit)
- … and 196 more

## Examples — non-redirect "The …" pages (correctly out of scope)

- `The Anguish of the Archon`
- `The Art of George R. R. Martin's A Song of Ice and Fire`
- `The Bear and the Maiden Fair`
- `The Bear and the Maiden Fair (TV)`
- `The Bells`
- `The Black Queen`
- `The Bloody Cup`
- `The Bloody Hand`
- `The Book of Holy Prayer`
- `The Book of Lost Books`
- `The Broken Man`
- `The Burning Mill`
- `The Burning of the Ships`
- `The Children`
- `The Chronicles of Longsister`
- … and 106 more

## Verification spot-checks

- `the hound` → PASS — resolved slugs = ['sandor-clegane'], expected `sandor-clegane`
- `the red viper` → PASS — resolved slugs = ['oberyn-martell'], expected `oberyn-martell`
- `the queen who never was` → PASS — resolved slugs = ['rhaenys-targaryen-daughter-of-aemon'], expected `rhaenys-targaryen-daughter-of-aemon`

## Integration (DONE)

This backfill has been wired directly into `scripts/event_alias_resolver.py`'s `build_and_save()` as a new source (`load_the_redirect_aliases()`), so a future `--build` rebuild of `all-node-alias-lookup.json` includes these phrases automatically — no manual merge step needed. The standalone `working/wiki/data/epithet-redirect-aliases.json` file is kept as an independent, inspectable artifact of this backfill run; it is NOT itself read by the resolver at runtime (the resolver recomputes the same redirects directly from `sources/wiki/_raw/` on every `--build`, so the two will always agree in content — this file is a point-in-time snapshot for review, not a live dependency).

`build_and_save()` was run after wiring and verified: (a) phrase count only grew (12,029 → 12,140, +111), (b) every pre-existing phrase key is still present and unchanged (spot-checked `hound`, `red viper`, `eddard stark`), (c) new epithet phrases resolve (see below).

**Important nuance found during verification:** the project's `normalize()` (in `event_alias_resolver.py`, ported to `web/src/lib/normalize.ts` for the front-end) strips a leading article (`the`/`a`/`an`) from BOTH stored keys and incoming queries. So `"The Hound"` was already normalizing to the key `"hound"` before this backfill ran, and `"hound" -> sandor-clegane` was already indexed — meaning the 3 examples named in the task brief (`the hound`, `the red viper`, `the queen who never was`) **already resolved correctly before this script ran**, via article-stripping + the existing article-less entries. They are NOT among the 111 new phrases for that reason (their normalized keys already existed). The genuinely new value this backfill adds is multi-word/non-substring epithets whose normalized form doesn't already exist and which fuzzy token-overlap cannot reliably resolve — e.g. `"the bastard of barrowton"` (-> `bastard of barrowton` -> `denys-snow`) previously had NO confident match (fuzzy top candidates were `barrowton` / `bastard` at a tied, non-decisive 0.55 score); it now resolves correctly. Single-word epithet redirects like `"The Crone"` -> `crone` -> `crone-the-seven` and `"The Butcher"` also land in the new-111 bucket for the same reason (no prior article-less entry existed under that exact word).

Orchestrator note: this script does NOT run `build-chat-export.py` or `weirwood refresh` — that happens once, downstream, after this backfill is reviewed. `event_alias_resolver.py --build` HAS already been run as part of this backfill (needed to prove the integration didn't break anything); if the orchestrator's downstream rebuild step re-runs it, it will be a no-op (idempotent — verified by running `--build` twice in a row, same 12,140-phrase output both times).

## Pre-existing CLI quirk surfaced (worth a human look — NOT a bug in this backfill)

`event_alias_resolver.py`'s CLI `resolve()` has a `_character_candidates()` fast-path (status `HIT-CHARACTER`) that is scoped to `node_category == "characters"` ONLY, ahead of the fuzzy fallback. Non-character epithets this backfill adds — e.g. `"the crone"` -> `crone` -> `crone-the-seven` (a `religions` node) — therefore fall through to fuzzy in the `--lookup` CLI tool and print `CANDIDATES` instead of a clean hit, even though the phrase IS correctly present as an exact match in `all-node-alias-lookup.json`. This is a **pre-existing scope limitation** of the CLI debugging tool, not something this backfill introduced or was asked to fix. **It does NOT affect the chat-UI**: `build-chat-export.py`'s `build_alias_map()` and the front-end `resolve.ts` are category-agnostic and both resolve `"the crone"` / `"the bastard of barrowton"` as clean exact hits (verified). Flagging for whoever next touches `event_alias_resolver.py`'s CLI: consider adding a generic any-category exact-hit step ahead of the character-only fast-path, to match `resolve.ts`'s behavior.
