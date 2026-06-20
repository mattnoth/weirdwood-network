# Demo + harvest pass (parallel demo window) — 2026-06-20

> **Non-track parallel window**, sidecar to the S112/S113 causal-arc track. Ran the
> `working/demo-asoiaf-loremaster.md` Loremaster demo for Matt, then (at Matt's request)
> ran a harvest pass over the open rows in `working/harvest-queue.md`.
> **Model:** Opus 4.8 orchestrator + 2 `general-purpose` Sonnet subagents (1 verify-and-attach, 1 fresh-verify).
>
> **IMPORTANT — worklog/harvest-queue NOT updated by this window.** A parallel session
> was live and actively writing `worklog.md` + `working/harvest-queue.md` (it advanced to
> S113 mid-window — appended harvest row 123 "S113 J3 research"). To avoid clobbering its
> in-progress work, this window committed ONLY its own uncontested files (8 node files +
> the demo-prompt fix + this record). **The settling session must fold the items below into
> `worklog.md` and flip the consumed harvest rows.** See "TO FOLD IN" at the bottom.

## Demo

Ran the Loremaster persona against the live graph. Showpiece = `--causal-chain
assassination-of-tywin-lannister` (7-hop upstream chain → Sansa's poisoned hairnet), narrated
with verbatim quotes pulled from each beat node. Matt: "demo is badass, quotes are sick."

**Matt's notes from the demo (captured):**
1. Do these demos **periodically as a testing/QA instrument** during the narrative-arc process —
   they surface graph gaps (e.g. the `gregor-confesses-and-kills-oberyn` node has no `## Quotes`).
2. **Spoiler gate is DEFERRED** — the demo prompt should NOT do a spoiler check. **FIXED this
   window** in `working/demo-asoiaf-loremaster.md` (replaced the "quick spoiler check" section
   with a "gating is deferred, don't ask" note).
3. **Candidate next ask:** add death quotes to `gregor-confesses-and-kills-oberyn` (Oberyn's
   death beat is bare). Not done — logged as a future harvest/quote candidate.

## Harvest pass — attachments (all verified, fresh-subagent PASS)

Verify-and-attach subagent opened each cited `chapter:line`, confirmed verbatim, attached to the
named node; a fresh independent subagent re-verified all 9 attachments across 8 files → **PASS**
(all SUPPORTED, well-formed, no dupes, no mis-attribution).

| harvest row | node | attachment |
|---|---|---|
| 104 | events/battle-of-the-blackwater | Davos "mouth of hell" — added navigable book cite `acok-davos-03:147` to existing wiki blockquote |
| 106 | events/battle-of-the-blackwater | Tyrion "lie here rotting" — book-cite overlay `asos-tyrion-01:79` |
| 112 | events/battle-of-the-blackwater | "Thousands sailed up the Blackwater Rush, and hundreds came back" — `asos-davos-02:153` (new) |
| 117 | events/stannis-retreats-to-dragonstone | "Did none keep faith?" / fox-and-flowers loyalty exchange — `asos-davos-02:27` |
| 122 | events/execution-of-eddard-stark | **NEW `## Quotes` block** (node was bare): Joffrey "Ser Ilyn, bring me his head!" `agot-arya-05:161` + "Ice ... he has Ice!" `:171` (Matt-flagged item) |
| 116 | characters/tywin-lannister | war-armor appearance ("burnished red steel ... rondels were sunbursts ... ruby eyes ... cloth-of-gold") `acok-sansa-08:17` |
| 110 | characters/mace-tyrell | "a once-powerful man gone to fat, yet still handsome" `acok-sansa-08:23` |
| 110 | characters/loras-tyrell | shared green-velvet-trimmed-with-sable Tyrell dress `acok-sansa-08:23` |
| 110 | characters/garlan-tyrell | shared green-velvet-trimmed-with-sable Tyrell dress `acok-sansa-08:23` |
| 115 | characters/salladhor-saan | shipboard hospitality (cracked green olives / white cheese / hot wine with cloves & lime, aboard *Bountiful Harvest*) `asos-davos-02:49` |

**No-op / already-attached (S111 minted these nodes with the quotes already present):** rows
107, 108, 111, 113, 114 — confirmed present, nothing duplicated. (These rows are still marked
`open` in the queue; a future harvest pass will flip them as no-op-confirmed.)

**NOT minted any nodes, NOT touched edges.jsonl** — pure quote/appearance/hospitality attachment.

## Harvest rows left OPEN (deliberately deferred)

- **Row 105** (Garlan-as-Renly "tall spear" line) — **cite is wrong**: the line is NOT in
  `acok-sansa-08` (no "tall spear" match). It's Sansa seeing Ser Garlan dressed as Renly's ghost
  at the Blackwater — likely `acok-sansa-07` or an `asos` Sansa chapter. **Cite needs re-resolving
  before attach.** Target node: `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` (exists;
  Matt confirmed "we talked about this node" — it's the fuller slug, not missing).
- **Row 109** (Cersei "set Sansa Stark aside" — `acok-sansa-08:41`, **verified verbatim, ready**) —
  target `joffrey-sets-sansa-aside-and-agrees-to-wed-margaery` (no `## Quotes` block yet).
  Held per Matt ("not necessarily in this session"). Attach next harvest pass.
- **Rows 118–121** (AGOT Varys/Illyrio/Robert-Dany conspiracy + Drogo westward vow + Jorah
  channel) — these want NEW nodes/edges (gated mints per dip-driven / no-mass-mint rule).
  Left for the causal-arc track's bridge work, not a harvest pass.

## TO FOLD IN (settling session — whoever runs the last /endsession)

1. **worklog.md:** add a sidecar note that this demo window attached 9 verified quotes/appearance
   overlays across 8 nodes (rows above). Does NOT advance the integer session counter.
2. **harvest-queue.md:** flip rows **104, 106, 107, 108, 110, 111, 112, 113, 114, 115, 116, 117, 122**
   to `done`. Fix row **105**'s cite (see above). Leave **109** open-ready, **118–121** open-gated.
3. Consider a recurring "demo-as-QA" cadence (Matt note #1) + the Oberyn-death-quotes candidate (note #3).
