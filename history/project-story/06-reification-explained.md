# 06 — Reification, Explained

> Part of the project-story series. Written 2026-06-12, after Session 91.
> This is the deep explainer for the one **structural** (rather than additive) change the graph has ever undergone. Everything here is shown against the live graph — every node, edge, and query output below is real, pulled with `scripts/graph-query.py` and `grep` over `graph/edges/edges.jsonl` on 2026-06-12.

| Vitals | |
|---|---|
| Sessions | S82–S87 (June 4–9, 2026), plus S88–S91 validation follow-ups |
| Spend | ~$35–36 (Plate 3 Sonnet reify pass + Plate 4 Opus cluster passes) |
| Edges | `edges.jsonl` 3,811 → 4,757 (live today: 4,760 after three S91 curator-pilot edges) |
| Event nodes | 371 → 583 (217 minted, 6 quarantined) |
| New machinery | 897 role edges, 51 SUB_BEAT_OF edges, 55 `superseded_by` stamps, 10 direction flips |
| Vocabulary | 163 → 166 edge types (`AGENT_IN`, `VICTIM_IN`, `SUB_BEAT_OF`) |
| Master design doc | `working/edge-modeling/edge-modeling-reification-design.md` (decisions D1–D8) |
| Merge record | `working/edge-modeling/plate5-merge-diff.md` |

---

## 1. The problem: you can't store the Red Wedding as an arrow

First, the vocabulary. The graph stores **nodes** (one file per entity — Jon Snow, Winterfell, House Frey) and **edges** (one JSON line each in `graph/edges/edges.jsonl`, of the form `source → EDGE_TYPE → target`, with a verbatim book quote as evidence). An edge is an arrow with a label. Arrows are perfect for **binary relations** — relations with exactly two participants and fixed asymmetric roles:

```
eddard-stark --[PARENT_OF]--> robb-stark
```

There is exactly one correct way to draw that arrow. The parent goes on the left. Nothing to decide.

Now try to draw the Red Wedding — the massacre at the Twins in *A Storm of Swords* where Robb and Catelyn Stark are murdered at a wedding feast. Who is the source of that arrow? Walder Frey, who ordered it but never lifted a blade? Roose Bolton, who personally drove a sword through Robb's heart? House Frey, whose soldiers did most of the killing? Catelyn, whose POV chapter it is? The event has an orderer, multiple executors, multiple victims, a location, a violated social institution (guest right) — and **no natural head**. Nothing in the world says a massacre is "about" its instigator rather than its victims.

The design doc's word for what happens when you force it anyway is **underdetermination**: a single deterministic arrow is *not uniquely determined* by a head-less event. Each extraction pass, looking at a different sentence about the same event, independently picks a *different* projection of it. Downstream, that reads as inconsistency — it looks like the model hallucinated different answers, when actually the data model asked an unanswerable question ("which participant is the source?") and got arbitrary answers.

This wasn't theoretical. Two concrete failure classes were sitting in the live graph when Session 82 opened:

**Failure 1 — grammatical-subject leakage.** Pass 1 (the mechanical extraction pass over all 344 book chapters) recorded relationships in a `| Character A | Relationship | Character B |` table with **no rule for which character goes in column A**. The extractor filled column A with the grammatical subject of the sentence it was reading, and the deterministic typer then locked edge direction by column position. So a sentence phrased in the passive voice produced a **backwards edge** — and the edge's own `asserted_relation` field witnessed the bug. The canonical example, verbatim from the pre-fix graph:

```
cressen --[KILLS]--> melisandre        asserted_relation: "Killed by"
```

Maester Cressen did not kill Melisandre. Melisandre's poison killed Cressen — the row even *says* "Killed by" — but because Cressen was the grammatical subject of the sentence, he became the source. Same class: `arya CAPTURES sandor` (the Hound captured Arya), `tyrion BETRAYS shae` (Shae betrayed Tyrion). The audit found **232 unordered pairs carrying the same edge type in both directions** — the statistical fingerprint of head-selection by coin flip.

**Failure 2 — the event hubs existed but were empty.** The graph already had 371 event nodes (battles, wars, tournaments, ingested from the wiki). But they were husks. The Red Wedding node — the most famous massacre in the series — had exactly **three outbound edges**, all wiki-infobox boilerplate:

```
- FIGHTS_IN: War of the Five Kings
- DEFEATS:   Iron Throne
- DEFEATS:   Warden of the North
```

and **zero edges from any participant**. Walder Frey, Roose Bolton, Robb, Catelyn — none of them connected to it. What the graph *did* have was the event smeared across person↔person dyads:

```
roose-bolton --[BETRAYS]--> robb-stark    asserted: "Betrays"
walder-frey --[BETRAYS]--> robb-stark     asserted: "Orchestrates massacre of"
```

So "who killed Robb Stark?" was unanswerable: there was no `KILLS → robb-stark` edge at all, just two `BETRAYS` arrows — one of which was forced to flatten "orchestrates massacre of" into "betrays" because a dyadic arrow has nowhere to put an orderer role. "Who *ordered* the Red Wedding?" was worse than unanswerable: the question mentions an event the edge layer couldn't even refer to.

The fix is the database-design move called **reification**: promote the event from an edge to a first-class **node**, and hang each participant off it with an edge whose *type names their role*. Nothing is lost — the orderer, the executors, the victims, the place all get their own labeled spoke. It's the junction-table move from relational databases: a Prescription is a record, not a foreign key.

---

## 2. What an event hub node is

An event hub is just a node file under `graph/nodes/events/`, exactly like a character node, with `type: event.*`. Two real ones, both load-bearing in the worked example later.

**`graph/nodes/events/red-wedding.node.md`** — a wiki-derived node that existed before reification (this is the husk from Failure 2, now serving as the parent hub). Its actual frontmatter:

```yaml
---
name: "Red Wedding"
type: event.wedding
slug: red-wedding
aliases: []
confidence: tier-1
wiki_source: "https://awoiaf.westeros.org/index.php/Red_Wedding"
bucket_id: battles-p-s
prompt_version: v1-python
node_version: 1
pass_origin: pass2-wiki-deterministic
---
```

(Its `type` was `event.battle` until the Plate 2.5 retype wave — a wedding massacre is not a battle. The body text below the frontmatter still says "Red Wedding is a event.battle from the AWOIAF wiki"; the retype touched frontmatter only. Known cosmetic debt.)

**`graph/nodes/events/catelyn-is-killed.node.md`** — a **minted beat**, created from scratch by the Plate 3 pipeline because no node existed for this specific moment. Its actual frontmatter:

```yaml
---
slug: catelyn-is-killed
type: event.death
name: "Catelyn is killed"
status: minted-plate3
minted_at: 2026-06-07T20:25:57.235078+00:00
evidence_chapters:
  - ASOS Catelyn VII
---
```

Minted nodes are deliberately skeletal — a slug, a type, a human-readable name, and the chapter that witnessed them. They exist to be *hubs*: their value is the edges that converge on them, not their prose. (The file's Notes section still says "Staging only — do NOT promote until Plate 5" — boilerplate from the minting script that nobody scrubbed after the Plate 5 merge actually promoted it. It is promoted; the note is stale.)

---

## 3. Role edges: the spoke vocabulary

A **role edge** is an edge whose type names the participant's thematic role in an event. Five types cover every standard slot. A deliberate design decision (D1) kept the new vocabulary minimal: only `AGENT_IN` and `VICTIM_IN` were added; the orderer and instrument roles reused existing types (`COMMANDS_IN`, `WIELDED_IN`).

**Direction convention:** for the three person/house roles, the **participant is the source** and the **event is the target** (`walder-frey → COMMANDS_IN → catelyn-is-killed`). The two exceptions follow pre-existing conventions: `WIELDED_IN` is artifact → event, and `LOCATED_AT` is **event → location** (the long-standing architecture.md rule "Entity → Location" won out over the design doc's glossary, which had grouped LOCATED_AT with the participant→event spokes — a small live-vs-design divergence worth knowing about).

Each row below is a real line from `graph/edges/edges.jsonl`, trimmed to the load-bearing fields.

**`AGENT_IN`** — the executor; the participant who actually performed the act.

```json
{"edge_type": "AGENT_IN", "source_slug": "house-frey", "target_slug": "catelyn-is-killed",
 "evidence_quote": "Someone grabs her scalp and cuts her throat.",
 "rationale": "The executor is unnamed ('someone') but acts within the Frey-orchestrated
   massacre in the Frey hall, making a Frey soldier the strong inference.",
 "confidence_tier": 2}
```

Notice what the role edge buys here: the book never names Catelyn's killer ("someone"), so a dyadic `X KILLS catelyn-stark` edge would have had to either invent an X or drop the fact. The hub lets the graph say *House Frey did it* at tier-2 confidence with the inference written down.

**`VICTIM_IN`** — the patient; the participant the act was done to.

```json
{"edge_type": "VICTIM_IN", "source_slug": "catelyn-stark", "target_slug": "catelyn-is-killed",
 "evidence_quote": "Catelyn is killed — Someone grabs her scalp and cuts her throat.",
 "confidence_tier": 1}
```

**`COMMANDS_IN`** — the orderer/instigator who did *not* personally execute (also still covers its older meaning, military command in a battle). This role is the heart of decision **D7**: orderer and executor live as two differently-typed spokes on *one* event node — not as two event nodes joined by a causal edge, and never collapsed into a fraudulent `orderer KILLS victim` dyad.

```json
{"edge_type": "COMMANDS_IN", "source_slug": "walder-frey", "target_slug": "catelyn-is-killed",
 "evidence_quote": "Walder Frey orchestrates massacre of Robb Stark and his followers —
   watches the slaughter 'greedily' from his throne; mocks Robb; refuses Catelyn's plea.",
 "confidence_tier": 1}
```

**`LOCATED_AT`** — pins the event to a place. Source is the event.

```json
{"edge_type": "LOCATED_AT", "source_slug": "catelyn-is-killed", "target_slug": "twins",
 "evidence_quote": "The wedding feast proceeds — Music pounds through the hall as guests
   eat, drink, and shout.",
 "plate5_location_remap": "the-twins"}
```

(The staged edge said `the-twins`; the Plate 5 merge remapped it to the canonical slug `twins`, and stamped the original so the remap is auditable.)

**`WIELDED_IN`** — the instrument; an artifact used in the event. Only 10 exist, all carrying real narrative weight:

```json
{"edge_type": "WIELDED_IN", "source_slug": "ice", "target_slug": "execution-of-eddard-stark",
 "evidence_quote": "Draws Ice and carries out the beheading",
 "rationale": "Ice, the Stark ancestral Valyrian steel greatsword, is the named artifact
   used to perform the beheading."}
```

Live counts today: **AGENT_IN 335, VICTIM_IN 316, COMMANDS_IN 157, LOCATED_AT 79, WIELDED_IN 10** — 897 role edges merged at Plate 5, give or take post-merge adjustments (the merge diff's own breakdown says 338/317/158/~73/10; the small deltas are S88–S91 validation-era touch-ups, and the LOCATED_AT figure in the diff was explicitly approximate).

---

## 4. SUB_BEAT_OF: events decompose into beats

The Red Wedding isn't one moment. It's a feast, then a bedding ceremony, then crossbows from the gallery, then a sequence of individual killings — across three chapters. Pass 1 sees it the way the books deliver it: as **narrative micro-beats** ("The wedding feast proceeds," "Catelyn is killed"), not as one labeled set-piece. Reification honors that granularity instead of erasing it: each beat becomes its own small hub carrying its own role edges, and a **`SUB_BEAT_OF`** edge (beat → parent event) ties it into the named occasion the wiki knows about.

`SUB_BEAT_OF` is distinct from the older `PART_OF` (which is event-in-*war* scope: Battle of the Blackwater `PART_OF` War of the Five Kings). And it is explicitly *not* an alias: the project's S86 **substitution test** says "Wedding at the Twins" ↔ "Red Wedding" are aliases (swap them in any sentence, truth value unchanged) but "Lord Walder calls for the bedding" ↔ "Red Wedding" fails the test — the bedding-call is a moment *within* the event. Granularity differences get `SUB_BEAT_OF` edges, not alias entries.

The live Red Wedding has **8 beats**, straight from `python3 scripts/graph-query.py --event-participants red-wedding`:

1. `the-wedding-feast-proceeds`
2. `lord-walder-calls-for-the-bedding`
3. `the-bedding-ceremony-begins`
4. `ser-wendel-manderly-is-killed`
5. `crossbows-kill-more-northmen`
6. `robin-flint-is-killed`
7. `robb-is-killed`
8. `catelyn-is-killed`

That ordering *is* the scene — you can read the massacre's structure off the node list.

**Beat-union queries** are why this matters. The parent hub `red-wedding` carries zero direct role edges; all 29 live on the beats. So `--neighbors red-wedding` shows only the 8 incoming `SUB_BEAT_OF` arrows — but `--event-participants red-wedding` (built in the S88–S91 validation era) walks every beat, unions their role edges, and answers at the event level:

```
SUMMARY: red-wedding  |  8 beats, 29 role edges, 13 distinct participants
```

Thirteen participants — Walder Frey, Roose Bolton, House Frey, Ryman Frey, the Greatjon, Catelyn, Robb, Edmure, Roslin, Wendel Manderly, Robin Flint, Donnel Locke, Owen Norrey — each with role, beat, chapter, and quote. No single dyadic edge could ever have held that. (As §8 notes, three unmistakable Red Wedding beats — `ser-ryman-kills-dacey-mormont`, `the-camp-becomes-a-battlefield`, `red-wedding-revealed` — carry role edges but no `SUB_BEAT_OF` link to `red-wedding`, so the beat-union query misses them; 13 is an undercount.)

---

## 5. What the Plates actually did

The work shipped as six "plates" — independently approvable work packages, each a self-contained session prompt in the master design doc, executed one at a time across S82–S87. In plain English:

**Plate 0 — the direction normalizer.** A deterministic, no-LLM, ~$0 script that read all 3,811 existing edges and flipped the ones that self-witnessed the grammatical-subject bug (an `asserted_relation` saying "Killed by" on a `KILLS` edge, etc.). Result: **10 flips** (2 KILLS, 2 BETRAYS, 2 RESCUES, 1 each CAPTURES/TUTORS/HEALS/ATTACKS), 1 flagged mutual-kill left alone (Donal Noye and the giant Mag the Mighty genuinely killed each other). `melisandre → KILLS → cressen` is now correct in the live graph — and the row still carries `asserted_relation: "Killed by / ran afoul of"` as a permanent witness of what it used to be. Plate 0 also repointed 3 edges off the phantom slug `aerys-targaryen` onto the canonical `aerys-ii-targaryen` (the Mad King's node was split in two; Jaime's regicide pointed at the empty half).

**Plate 1 — the head rule + vocabulary.** Doc-only, $0. Added the **head rule** to the Pass-1 extractor prompt — "Column A is always the SEMANTIC AGENT, never the grammatical subject, never the POV character" — so future extractions can't re-import the bug. Added `AGENT_IN` + `VICTIM_IN` to `reference/architecture.md` (vocab 163 → 165; `SUB_BEAT_OF` later made it 166), widened `COMMANDS_IN` to cover the orderer role, and wired a validator contract: `AGENT_IN`/`VICTIM_IN` targets MUST be `event.*` nodes.

**Plate 2 / 2.5 — verification and cleanups.** Plate 2 settled the project's biggest open decision, **D2: replace vs. supplement vs. project.** If you add role edges but keep the old scattered dyads, you've added rows without fixing the inconsistency; if you generate a "canonical dyad" alongside each hub, you've re-imported the underdetermination you set out to kill (which participant becomes the source?). Plate 2 verified that `graph-query.py --path` traverses person → event → person transparently with zero new code, and chose **(a) Replace**: superseded dyads get stamped `superseded_by: <hub-slug>` — never deleted (hard project rule) but marked out of primary traversal. Plate 2's coverage join also corrected a design assumption: of 8,384 Pass-1 event entries, only **1** exact-matched an existing event-node slug. Naively reifying everything would mint ~8,300 junk hubs — which forced **D8** (next plate). Plate 2.5 did the inventory hygiene: 27 wiki event nodes retyped off the wrong `event.battle` (weddings, feasts, trials, assassinations), 12 chapter-article nodes retyped, 4 duplicate battle-node collisions merged.

**Plate 3 — selective reification.** The build. A pipeline (`edge-reify-backfill.py`) mined the Pass-1 `## Events & Actions` tables, and — per **D8, the "selective" decision** — reified on **n-ary structure, not event type**. A clean dyad (one agent, one victim, no third-party orderer, no named occasion — Jaime kills Aerys) stays a direct `KILLS` edge: no hub, no extra hop, because nobody disputes the head. A hub is minted only where the head was genuinely contested: instigator ≠ executor, multiple killers/victims, or a named set-piece. A fuzzy-title reuse pass rebinds beats to existing nodes before minting new ones. Output: **217 minted hubs and 897 role edges** (staged, not merged), all carrying verbatim Pass-1 quotes, plus 55 supersede stamps for the dyads each hub replaced. A Sonnet `claude -p` pass did the role-slot reading; everything else was deterministic Python. This plate also ate the era's two incidents honestly recorded in the audit: an unattended overnight run **burned its retry budget against a silent rate-limit wall** (324 events dropped, fully recovered on resume), and a `--all` flag **bypassed the D8 selectivity gate** and minted junk micro-beat hubs — that contaminated output was discarded outright rather than cleaned.

**Plate 4 — the cluster pass.** The 1,617-edge Events-Haiku bulk from Phase 9 had failed its cross-model drift audit (NO-GO, parked, ~$75–85 sunk). Plate 4 salvaged it as *cluster input* — not promoting its edges, but using its event titles to decide which Plate-3 mints belong inside which wiki-canonical event. Opus passes produced **51 `SUB_BEAT_OF` edges** (the Red Wedding's 8 among them) and 2 `DUPLICATE_OF` merges. Cost ~$35 total for Plates 3+4 — the entire reification spend.

**Plate 5 — the single gated merge.** The one irreversible step, run S87 after Matt's explicit go-ahead with five pre-answered decisions, with a full backup (`graph/edges/_regrounding/edges-pre-reification-2026-06-09.jsonl`) and a published before/after diff. Everything staged landed at once: normalizer flips, Aerys repoint, retypes, 217 mints, 897 role edges (minus 17 filtered for unresolvable targets), 51 SUB_BEAT_OF, 55 supersede stamps, plus carried-forward cleanups from an older session (2 false `LOVES` edges dropped, 21 `ASSAULTS` retyped to `ATTACKS`). **`edges.jsonl` went 3,811 → 4,757 rows; `graph/nodes/events/` went 371 → 583 files.** The post-merge validator flagged 32 SUB_BEAT_OF edges with empty evidence quotes (Plate 4 ran inference-only on those; they carry a rationale instead — a known, documented follow-up, not a silent gap).

---

## 6. The worked example: "Who ordered the killing of Catelyn Stark, and where?"

Pre-reification, this question was unanswerable: no edge mentioned an event, no `KILLS` edge targeted Catelyn at the Twins, and the closest dyads pointed the wrong concepts at each other. Here is the live graph answering it, hop by hop.

**Hop 1 — find the event.** `python3 scripts/graph-query.py --neighbors catelyn-is-killed`:

```
NEIGHBORS: catelyn-is-killed
  Catelyn is killed (event.death)

OUTGOING (2 edges)
  [LOCATED_AT]   -> twins
       quote: "The wedding feast proceeds — Music pounds through the hall..."
  [SUB_BEAT_OF]  -> red-wedding

INCOMING (3 edges)
  [AGENT_IN]    <- house-frey
       quote: "Someone grabs her scalp and cuts her throat."
  [COMMANDS_IN] <- walder-frey
       quote: "Walder Frey orchestrates massacre of Robb Stark and his followers —
               watches the slaughter 'greedily' from his throne..."
  [VICTIM_IN]   <- catelyn-stark
       quote: "Catelyn is killed — Someone grabs her scalp and cuts her throat."
```

One node answers the whole question. **Who ordered it:** Walder Frey (`COMMANDS_IN`). **Who did it:** a Frey soldier, unnamed in the text, attributed to House Frey at tier-2 (`AGENT_IN`). **To whom:** Catelyn (`VICTIM_IN`). **Where:** the Twins (`LOCATED_AT`). **Within what:** the Red Wedding (`SUB_BEAT_OF`). Every spoke carries its book quote.

The hub-and-spokes shape:

```
                         walder-frey
                              │ COMMANDS_IN
                              ▼
   house-frey ──AGENT_IN──> ┌────────────────────┐ ──LOCATED_AT──> twins
                            │  catelyn-is-killed │
 catelyn-stark ─VICTIM_IN─> │    (event.death)   │
                            └─────────┬──────────┘
                                      │ SUB_BEAT_OF
                                      ▼
                            ┌────────────────────┐
        7 sibling beats ──> │    red-wedding     │
        (robb-is-killed,    │   (event.wedding)  │
         the-bedding-..., …)└────────────────────┘
```

**Hop 2 — the path query sees through the hub.** This was the D2 bet: that `--path` would surface event bridges with zero new engineering. `python3 scripts/graph-query.py --path walder-frey catelyn-stark` (trimmed):

```
2-HOP BRIDGES (13 common neighbors)
  walder-frey --[COMMANDS_IN]--> catelyn-is-killed
      --[catelyn-is-killed]--
  catelyn-stark --[VICTIM_IN]--> catelyn-is-killed
```

The man and his victim now connect *through the named act*, with the role types telling you exactly what each was to it — alongside the still-true direct edges (`walder-frey VIOLATES_GUEST_RIGHT catelyn-stark`, three `GUEST_OF` edges dripping with irony).

And the sibling beat answers the other famous question. `--neighbors robb-is-killed`:

```
  [AGENT_IN]    <- roose-bolton
       quote: "A man in dark armor and a pale pink cloak spotted with blood steps up
               and says 'Jaime Lannister sends his regards.'..."
  [COMMANDS_IN] <- walder-frey
  [VICTIM_IN]   <- robb-stark
       quote: "He thrusts his longsword through Robb's heart and twists."
```

**Who killed Robb Stark?** Roose Bolton, executor; Walder Frey, orderer; with the pink-cloak quote attached. The two old `BETRAYS → robb-stark` dyads are still in the file — stamped `superseded_by: robb-is-killed`, exactly as D2-Replace prescribed.

---

## 7. Before and after

**Questions the graph could not answer before reification, and answers now:**

1. **"Who killed Robb Stark?"** Before: no `KILLS` edge existed; two `BETRAYS` dyads pointed at him, one of which had flattened "orchestrates massacre of" into "betrays." Now: `roose-bolton AGENT_IN robb-is-killed`, quote and all.
2. **"Who ordered the Red Wedding?"** Before: the orderer role had no home — a dyadic schema literally cannot say "ordered but didn't execute." Now: `walder-frey COMMANDS_IN` every beat of it (10 events overall answer "what did Walder Frey command," including `ser-ryman-kills-dacey-mormont` and `red-wedding-revealed`).
3. **"Who participated in the Red Wedding, across all its beats?"** Before: the hub had 3 wiki-boilerplate edges and zero participants. Now: `--event-participants red-wedding` → 8 beats, 29 role edges, 13 distinct participants, each with chapter and quote.
4. **"Where was Catelyn Stark killed?"** Before: no event node meant nowhere to hang a location. Now: `catelyn-is-killed LOCATED_AT twins`.
5. **"Who killed Maester Cressen?"** Before: the graph asserted Cressen killed Melisandre. Now: flipped, with the self-witnessing `"Killed by"` field preserved as audit trail.
6. **"What weapon was used to execute Eddard Stark?"** `ice WIELDED_IN execution-of-eddard-stark` — artifact history as graph traversal.

**Questions it still can't answer:**

1. **"Who fought at the Tower of Joy?"** `combat-at-the-tower-of-joy` exists as a node — with **zero edges**, verified live. Reification mined *Pass 1 chapter extractions*, and pre-narrative events (Robert's Rebellion and earlier) have no Pass-1 anchor: nobody POV-witnesses them; characters only *talk about* them. This is the **historical-events dark zone** confirmed by the S88 validation probes.
2. **"Who sacked King's Landing?"** Same shape: `sack-of-kings-landing`, zero edges. The fix is a different pass (mining the wiki's prose or recollection-flagged Pass-1 dialogue), logged as post-Plate-5 follow-up track work — not a flaw in the hub architecture, which is sitting there ready to receive the spokes.
3. **"What beats preceded Dacey Mormont's death?"** Partially dark for a subtler reason — see the honesty section below.

---

## 8. Where the live graph disagrees with the documents (findings from writing this chapter)

Checking every claim above against the live graph turned up real seams. In project tradition, they're listed rather than smoothed over:

1. **Role edges live on beats, not on the parent hub.** The design doc's worked example implies querying the Red Wedding node directly for its participants; in the shipped graph `red-wedding` has zero direct role edges — everything attaches to the 8 beats, and only the beat-union query (`--event-participants`, built *after* the merge, in S88–S91) answers at event level. The architecture works; the doc's sketch of it is one level off.
2. **The Red Wedding's SUB_BEAT_OF cover is incomplete.** Three minted hubs that are unmistakably Red Wedding beats — `ser-ryman-kills-dacey-mormont`, `the-camp-becomes-a-battlefield`, `red-wedding-revealed` — carry role edges but **no `SUB_BEAT_OF` link to `red-wedding`** (Plate 4 emitted only 51 such edges corpus-wide). Consequence: the beat-union query misses Dacey Mormont's death; the "13 distinct participants" answer is an undercount. Candidate follow-up.
3. **`LOCATED_AT` direction contradicts the design glossary.** The glossary groups it with the participant→event spokes ("Source = participant, target = event node"); the live edges follow architecture.md's older `Entity → Location` rule (`catelyn-is-killed → twins`). Architecture.md won; the design doc was never corrected.
4. **32 of 51 SUB_BEAT_OF edges have empty evidence quotes** (documented at merge), and at least one retained "quote" isn't book text at all — `robb-is-killed SUB_BEAT_OF red-wedding` carries `"DEFEATS: Warden of the North (track_b: Result)"`, a wiki-infobox display bullet that leaked into the evidence field.
5. **Stale staging boilerplate on minted nodes** — `catelyn-is-killed.node.md` (and presumably its 216 siblings) still says "do NOT promote to graph/nodes/events/ until Plate 5" in its Notes, post-promotion. Cosmetic.
6. **Frontmatter/body drift on retyped wiki nodes** — `red-wedding.node.md` is `type: event.wedding` in frontmatter but "is a event.battle" in its Identity prose. Cosmetic.
7. **Counts have drifted within tolerance.** Live role-edge counts (335/316/157/79/10) differ by 1–6 from the merge diff's breakdown, and `edges.jsonl` is at 4,760 (not 4,757) after S91's three curator pilot edges. Movement, not contradiction — but anyone re-verifying this chapter later should diff against the live file, not the vitals block.

None of these undermine the result. The structural claim — that an n-ary event is now a node you can stand on, with every participant one labeled hop away and a book quote on every spoke — is true in the live graph, and the Red Wedding proves it end-to-end.
