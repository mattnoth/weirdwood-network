# Deletion-Safety & Alias Review — the 138 "safe-to-delete" PARENT_OF edges

Reviewer: fresh independent cold reviewer. **Read-only.** No graph mutation, no git add, no
`sources/` writes. All findings re-derived from the source-of-truth edge store
`graph/edges/edges.jsonl` (23,330 edges; 1,688 PARENT_OF), the built read artifacts
`web/data/{nodes,alias-map,edges}.json`, and the local wiki cache `sources/wiki/_raw/`.

The proposal file `working/graph-cleanup/parent-edge-proposal.jsonl` has been **revised since the
prior verdict**: its three "AUTO-APPLY / safe" classes are now
`EXACT_DUP_EDGE` (1) + `REDUNDANT_CHILD_STUB` (124) + `HOUSE_AS_PARENT` (13) = **138 edges**.
(The unsafe DUPLICATE/namesake/split work is now split into `DUPLICATE_PARENT_NODE`/`WRONG_NAMESAKE`/
`NODE_SPLIT` — NOT part of the 138 and NOT reviewed for deletion here.)

---

## BOTTOM LINE

**All 138 edge deletions are SAFE and non-lossy.** I checked 100% of each class against the edge
store, not a sample. Zero failing edges. Every child retains its correct ≤2 real-person parents
after the delete. Deletion is fully recoverable (git-tracked JSONL).

**BUT the deletion is edge-only — no node is removed — so the "aliases" question is about lookup
quality, not reachability.** Nothing becomes *unreachable* from the 138 deletes (the bare nodes
persist in `nodes.json` and stay alias-resolvable). Two alias workstreams MUST still ride along,
but they are pre-existing gaps the cleanup exposes rather than damage it causes:

1. **`the`-prefix epithet gap (systematic, high value).** **ZERO** of the 12,029 alias phrases
   start with `"the "`. Every "the hound" / "the red viper" / "the queen who never was" /
   "aemon the dragonknight" query **MISSES** today, even though the article-less form resolves.
   Backfill these before the chat-UI ships — the Bloodraven persona will get "the X" constantly.
2. **merge ⇒ preserve retired name as alias** (for the deferred node-merge track, NOT the 138):
   adopt it as a rule; it is **not** currently handled (e.g. "elenda caron" still points at its own
   soon-to-be-retired stub).

---

## Q1 — Why can we delete these? (per-class verdict)

Recoverability (all three classes): **YES, fully recoverable.** `graph/edges/edges.jsonl` is the
git-tracked source of truth; a wrong delete is a `git checkout`/revert away. Low blast radius.

### Class A — `EXACT_DUP_EDGE` (1 edge) — VERDICT: **SAFE**

The single row: `tywin-lannister → tyrion-lannister` (duplicate). Edge-store trace:

```
PARENT_OF tywin-lannister -> tyrion-lannister   (appears TWICE)
PARENT_OF joanna-lannister -> tyrion-lannister
```

Removing one copy leaves `tyrion-lannister` with **tywin + joanna = the correct 2 biological
parents.** Pure de-duplication; no fact removed. (The other two exact-dups the prior verdict
named — `oppo←hop-bean`, `penny←hop-bean` — are NOT in this proposal's EXACT_DUP class; only
tyrion is flagged. If a full `(src,tgt,type)` dedup pass is wanted, those two should be swept too,
but that is out of scope for the 138.)

### Class B — `REDUNDANT_CHILD_STUB` (124 edges) — VERDICT: **SAFE (124/124 verified)**

**What is removed:** edge `P → C` where `C` is a bare conflation bucket and a disambiguated variant
`C-...` already carries `P`. **What remains:** the identical assertion `P → C-variant`, i.e. the
parent fact still lives on the correct disambiguated node.

**I re-verified every one of the 124 against `edges.jsonl` (did not trust the label):** for each
redundant `P → C(bare)`, at least one variant node `C-...` exists AND `P` is present in that
variant's PARENT_OF parent list. **Failures where no variant carries P: 0.**

Traced examples (before → after):
- `stevron-frey → aegon-frey` (bare). Variant `aegon-frey-son-of-stevron` carries `stevron-frey`
  in its parent list. After delete: fact survives on `aegon-frey-son-of-stevron` (alias
  "jinglebell" — the correct son). ✅
- `aenys-frey → aegon-frey` (bare). Variant `aegon-frey-son-of-aenys` ("aegon bloodborn") carries
  `aenys-frey`. ✅
- `maekar-i-targaryen`-era Aemon: the `aemon-targaryen-son-of-maekar-i` variant (= Maester Aemon)
  carries its parent independently; the bare `aemon-targaryen` edge is the redundant double-count.
  ✅

**No REDUNDANT delete loses a fact.** Correct-but-worth-flagging side effect (NOT a blocker):
**9 bare children lose ALL their PARENT_OF edges** and become parent-less buckets —
`aegon-frey, aemon-targaryen, daella-targaryen, daeron-targaryen, gaemon-targaryen,
leo-tyrell, luthor-tyrell, rhaena-targaryen, robert-frey`. This is *correct* (each bare slug is an
ambiguous multi-person bucket whose real parentage lives on the variants), and the **nodes still
exist and stay alias-reachable** — but see Q2a for the lookup-routing nuance these buckets create.

### Class C — `HOUSE_AS_PARENT` (13 edges) — VERDICT: **SAFE (13/13 verified)**

**What is removed:** an edge where the "parent" is actually a HOUSE node (a bare house token), not a
person. A House cannot be a biological parent. **What remains:** the child's real person parent(s).

Wiki cache confirms all seven distinct parent tokens are house redirects (verbatim):
`Sunderly.json`, `Bracken.json`, `Mormont.json`, `Piper.json`, `Belmore.json`, `Baelish.json`,
`Charlton.json` each = **"Redirect to: House <X>."**

**I confirmed a real PERSON parent remains for every one of the 13** (full trace below). Examples:
- `sunderly → victarion-greyjoy`: parents = `[quellon-greyjoy, sunderly, lady-sunderly-wife-of-quellon-greyjoy]`
  → after delete: `[quellon-greyjoy, lady-sunderly-wife-of-quellon-greyjoy]` — **father + mother
  both remain.** ✅ (Same shape for aeron/balon/euron/urrigon-greyjoy — all keep Quellon +
  Lady Sunderly.)
- `bracken → catelyn-bracken`: `[jonos-bracken, bracken, lady-bracken]` → `[jonos-bracken, lady-bracken]`
  — father + mother remain. ✅ (alysanne/bess-bracken identical.)
- `charlton → walda-rivers`: `[aemon-rivers, walder-rivers, charlton]` → `[aemon-rivers, walder-rivers]`
  — two person parents remain. ✅
- `belmore → elbert-arryn`: → `[ronnel-arryn, ronnel-arryn-son-of-jasper]` remain. ✅

**No HOUSE_AS_PARENT delete strips a child's only parent.** Two rows carry a *pre-existing,
unrelated* data smell that the delete does not worsen and is worth a separate note:
- `baelish → petyr-baelish`: remaining parents include `alayne-baelish` and `alayne` — "Alayne" is
  Sansa's alias / Petyr's *fake* daughter, mis-wired as his parent. Deleting the `baelish` house
  edge is still correct; the Alayne mis-parent is a separate bug (not in the 138).
- `mormont → alarra-stark`: leaves `alaric-stark` + `lady-mormont-wife-of-alaric-stark`. ✅

---

## Q2 — Aliases

### (a) Bare-name resolvability after edge deletion — findings per name

**Critical framing:** the 138 deletes are **edge-only; the bare NODES are not deleted.** They
persist in `nodes.json` (e.g. `brandon-stark` still has 7 quotes) and stay in the alias map. So
**no name becomes unreachable because of the 138 deletes.** The real observation is a *routing*
issue that predates the cleanup: the bare natural phrase resolves to the (now parent-less)
conflation bucket, **not** to the disambiguated variants.

Actual `alias-map.json` contents for the flagged bare names (normalized lowercase):

| query | alias-map resolves to | routes to variants? |
|---|---|---|
| `aemon targaryen` | `aemon-targaryen-son-of-maekar-i` **and** `aemon-targaryen` (bare) | **partly** — bare phrase reaches Maester Aemon + the bucket |
| `brandon stark` | `brandon-stark` (bare only) | **no** — 13 real Brandons unreached by plain name |
| `rhaenys targaryen` | `rhaenys-targaryen` (bare only) | no |
| `daenerys targaryen` | `daenerys-targaryen` (bare only) | n/a (single person; fine) |
| `rhaella targaryen` | `rhaella-targaryen` (bare only) | no |
| `daella targaryen` | `daella-targaryen` (bare only) | no |
| `daeron targaryen` | `daeron-targaryen` (bare only) | no |
| `rhaena targaryen` | `rhaena-targaryen` (bare only) | no |
| `aegon frey` | `aegon-frey` (bare only) | no |
| `leo tyrell` / `luthor tyrell` / `robert frey` / `gaemon targaryen` | bare only | no |

Every disambiguated variant **is** independently reachable by its own spaced phrase
("brandon stark the breaker", "brandon the shipwright", "daeron the drunken", "maester aemon",
"prince aemon the dragonknight", "jinglebell", "aegon bloodborn", "leo longthorn", "lazy leo").
What's missing is a router from the *bare* phrase to the *set* of variants.

**Verdict for Q2a:** deleting the 138 edges does **not** orphan any name. The 9 parent-less bare
buckets remain queryable. **Recommended (not blocking the deletes):** when a later track redirects
or splits these bare buckets, make the bare natural phrase resolve to the **list of variant slugs**
(a disambiguation fan-out), so "brandon stark" offers the real Brandons instead of a hollow bucket.

### (b) Merge ⇒ preserve retired name as alias — RULE + current state

For the deferred node-merge track (`DUPLICATE_PARENT_NODE` etc., **not** the 138), when a slug is
merged/retired into a survivor, the retired slug's **natural name must be added as a spaced-phrase
alias on the survivor** — otherwise the maiden/old name stops resolving.

Current state (checked): **not handled.**
- `elenda caron` → still points only at `elenda-caron` (its own stub). `Elenda_Caron.json` is a
  wiki redirect to Elenda Baratheon, so on merge into `elenda-baratheon` the phrase "elenda caron"
  must be preserved as an alias on `elenda-baratheon`, or the maiden name goes dark.
- `damon lannister` → `damon-lannister` (disambig stub); if merged toward the `-son-of-jason`
  variant, "damon lannister" must survive as an alias.
- Both source nodes (`elenda-caron`, `elenda-baratheon`, `damon-lannister`) still exist.

**Rule Matt should adopt:** *any node merge/retirement MUST add the retired node's name (and any of
its aliases) as natural spaced-phrase aliases on the surviving node, then rebuild the alias
resolver.* Bake this into the merge tooling so it can't be forgotten.

### (c) Epithet-alias backfill gap (Step 5) — the systematic "the"-prefix miss

Spot-check result: epithets resolve **without** a leading article but **not with** one.

- `aerion the monstrous` → `aerion-targaryen` ✅ (note: this is the bare/Monstrous slug — the
  two-Aerions conflation the prior verdict flagged; `Aerion_the_Monstrous.json` = "Redirect to:
  Aerion Targaryen")
- `queen who never was` → `rhaenys-targaryen-daughter-of-aemon` ✅ … but **`the queen who never
  was` → None.**
- `dragonknight` → `aemon-targaryen-son-of-viserys-ii` ✅ … but **`aemon the dragonknight` → None**
  and **`the dragonknight` → None** (only `prince aemon the dragonknight` happens to exist).

**Quantified:** **0 of 12,029 alias phrases begin with `"the "`.** So *every* "the X" epithet query
misses. This is the single highest-leverage alias fix for the chat-UI.

Concrete backfill table (phrase → target slug → evidence; all natural spaced phrases):

| missing alias phrase | target slug | evidence |
|---|---|---|
| `the hound` | `sandor-clegane` | `The_Hound.json` = "Redirect to: Hound"; `hound` already resolves |
| `the red viper` | `oberyn-martell` | `The_Red_Viper.json` = "Redirect to: Oberyn Martell"; `red viper` resolves |
| `the queen who never was` | `rhaenys-targaryen-daughter-of-aemon` | `The_Queen_Who_Never_Was.json` = "Redirect to: Rhaenys Targaryen (daughter of Aemon)" |
| `aemon the dragonknight` | `aemon-targaryen-son-of-viserys-ii` | `Aemon_the_Dragonknight.json` = "Redirect to: Aemon Targaryen (son of Viserys II)" |
| `the dragonknight` | `aemon-targaryen-son-of-viserys-ii` | same redirect; `dragonknight` already resolves |
| `the mad king` | `aerys-ii-targaryen` | `mad king` resolves; add article form |
| `the young dragon` / `daeron the young dragon` | `daeron-i-targaryen` | `young dragon` resolves |
| `the knight of flowers` | `loras-tyrell` | `knight of flowers` resolves |
| `the mountain that rides` | `gregor-clegane` | `mountain that rides` resolves |
| `the onion knight` | `davos-seaworth` | `onion knight` resolves |
| `the smiling knight` | `smiling-knight` | `smiling knight` resolves |
| `the maid of tarth` | `brienne-tarth` | `maid of tarth` resolves |
| `the kingmaker` | `criston-cole` | `kingmaker` resolves |
| `aerion the monstrous` (already OK) | `aerion-targaryen` | listed only to flag the wrong-Aerion conflation, not a backfill |

**Simplest fix:** generate a `"the " + phrase` alias for every existing epithet/title phrase that a
reader would article-prefix (regex-driven, then keep natural spaced form), rather than hand-listing.
The table above is the substantiated seed.

---

## What MUST accompany the 138-edge cleanup

1. **Deleting the 138 is safe now** — no gate needed on alias work; nothing goes unreachable.
2. **Before chat-UI ship:** backfill `"the "`-prefixed epithet aliases (0/12,029 today) and rebuild
   the alias resolver — highest-leverage lookup fix.
3. **Adopt the merge⇒alias rule** for the *later* node-merge/split track; it is not yet handled.
4. **Optional follow-up (not the 138):** make the 9 parent-less bare buckets fan out to their
   variant slugs by name, and sweep the two remaining exact-dup PARENT_OF edges (`oppo`, `penny`
   ← hop-bean) the prior verdict named.
