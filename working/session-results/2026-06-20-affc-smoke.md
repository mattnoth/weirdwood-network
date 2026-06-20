# AFFC Smoke Test — Causal-Layer Coverage Check (read-only)

> **Date:** 2026-06-20 (S114). **Model:** Opus 4.8 orchestrator (read-only dip-as-check).
> **Purpose:** The causal layer has ~zero AFFC/ADWD coverage (S112: reaches ~8% of event nodes, all
> AGOT–ASOS). Run the Loremaster-demo queries against AFFC-centric arc-queries to find where they go
> dark, and produce a **ranked fumble list that re-prioritizes the next build** (may bump Q5).
> **No graph writes.** Local cache only. Grading: `--causal-chain` / `--neighbors` /
> `event_alias_resolver.py --lookup`.

---

## Headline

**All five AFFC arc clusters are causally DARK.** Every anchor node tested returned
**0 upstream + 0 downstream causal edges**. Controls (`the Red Wedding`, `death of Tywin`,
`the Purple Wedding`) all resolve HIT and walk chains — so this is a genuine **coverage gap, not a
tool fault**. The AFFC causal layer is empty; the question is purely build-priority, driven by
**salience × beat-readiness** (how many beat-nodes already exist vs. need minting).

The decisive differentiator is beat-readiness: **Cersei's downfall already has nearly all its
beat-nodes minted** (just no causal spine), whereas the other four arcs need 2–3 node mints each.
That makes Cersei's downfall the cheapest *and* highest-salience AFFC arc — **it bumps Q5** as the
recommended next build.

---

## Per-cluster results

### 1. Cersei's downfall — DARK, but HIGHEST beat-readiness ⇒ #1 build
Small-council paranoia → arming the Faith → arrest → walk of atonement.

| Beat-node | Exists? | Causal | Notes |
|---|---|---|---|
| `cersei-plots-against-margaery` | ✅ (event.conspiracy) | 0+0 | the false-accusation scheme |
| `cersei-fills-in-the-arrest-warrants` | ✅ (event.capture) | 0+0 | |
| `faith-militant-uprising` | ✅ but **TRAP** | 0+0 | node CONTENT is the **historical Targaryen-era (Aenys/Maegor) uprising** from TWOIAF/F&B — NOT Cersei rearming the Faith. (Its 8 PART_OF children are mixed.) See trap list below. |
| Cersei rearms the Faith / forgives crown debt | ❌ MISS | — | the actual AFFC "arming the Faith" beat has **no node** — needs a mint |
| `cersei-is-captured-in-the-sept` | ✅ (event.capture) | 0+0 | **role edges READY**: AGENT_IN the-faith, COMMANDS_IN high-sparrow, VICTIM_IN cersei, LOCATED_AT great-sept-of-baelor (all cited to affc-cersei-10) |
| `cersei-is-stripped-and-imprisoned` | ✅ (event.capture) | 0+0 | |
| `walk-of-atonement` | ✅ (concept.custom, in `customs/`) | 0+0 | a **generic wiki custom** (empty aliases), not Cersei's specific walk — may need a Cersei-specific event beat or can be referenced |
| `cersei-confronts-and-arrests-the-blue-bard` | ✅ | (not walked) | sub-beat of the Margaery frame-up |

> **Note on node richness:** the existing Cersei beats are **Plate-3 skeleton mints** (frontmatter +
> placeholder `## Edges`, no prose, no `## Quotes`) — they exist as causal-wiring targets but carry
> no book text yet.

**Grade: DARK but most build-ready of the five.** The spine is entirely dark; five real beats exist
(one already role-wired), but the "arming the Faith" beat needs a mint (the existing
`faith-militant-uprising` is the historical trap). Realistic build ≈ **1–2 mints + ~5–7 causal edges**
(CAUSES/MOTIVATES) wiring plots-against-margaery → [rearms-the-Faith, new] → captured-in-sept →
stripped-imprisoned → walk-of-atonement, plus the self-caused-irony MOTIVATES (Cersei arms the Faith
→ the Faith destroys her). Clean self-caused arc (backlog #17). **Still the clear #1 AFFC fumble** —
highest salience and lowest mint cost of the five.

### 2. Kingsmoot → Euron → Reach raids — DARK, missing key beats ⇒ #2
| Beat | Exists? | Notes |
|---|---|---|
| `death-of-balon-greyjoy` | ❌ MISS | the trigger for the whole arc — no node |
| `kingsmoot-on-old-wyk` | ✅ but near-bare | only 1 PRECEDES *incoming* (from `battle-on-the-green-fork` — wrong-context chronology backbone); 0 causal; 0 participant role edges; **mistyped `event.battle`** (it's an assembly/election → `event.ceremony`) |
| Euron wins / seizes Seastone Chair | ❌ MISS | no node |
| `anarchy-in-the-reach` | ✅ | the raids exist as a node but Euron-causation dark |
| `victarion-admits-euron-s-role-in-his-wife-s-death` | ✅ | 0+0 |

**Grade: DARK, ~2–3 mints needed** (death-of-balon, euron-wins-kingsmoot/seizes-chair) + retype +
aliases on kingsmoot. Matches J8 in `wo5k-decomposition.md` (no upstream attach-point — stands as
its own mini-arc; Balon's death is standalone).

### 3. Brienne's hunt → Lady Stoneheart — DARK, missing beats + a TRAP ⇒ #3
| Beat | Exists? | Notes |
|---|---|---|
| Lady Stoneheart / Catelyn resurrected | ❌ | "Lady Stoneheart" resolves to the **`catelyn-stark` character node**, not an event |
| Brienne hanged / given the choice (sword-or-noose) | ❌ | **TRAP:** `brienne-arrested` looks right but is the **ASOS Harrenhal** event (Jaime orders Balon Swann to cell, asos-jaime-07) — NOT the AFFC Stoneheart hanging |

**Grade: DARK, ~2–3 mints** (Stoneheart-reveal, Brienne-captured-by-the-BWB). Clean cross-book
upstream attach at `red-wedding` (built) — Beric→Catelyn resurrection is downstream of the RW.
Backlog #15→#19.

### 4. Dorne / Myrcella / Sand Snakes vengeance — DARK, missing beats + a TRAP ⇒ #4
| Beat | Exists? | Notes |
|---|---|---|
| `arrest-of-the-sand-snakes` | ✅ (bare) | 0+0; Doran jails them after the failed plot |
| Myrcella wounded (Darkstar) | ❌ MISS | no node |
| Sand Snakes' vengeance plot / "crown Myrcella" | ❌ | the conspiracy beats dark |
| `conquest-of-dorne` | ✅ but **TRAP** | this is **Aegon's historical conquest**, NOT the AFFC plot |

**Grade: DARK, ~2–3 mints.** Lower salience than 1–3; the Dornish plot is a slow-burn setup arc.

### 5. Greyjoy succession / Reach — folds into #2 (Kingsmoot). Not scored separately.

---

## Discoverability fumbles (resolver) — a second, orthogonal finding

Independent of the causal gap, **natural-phrase resolution is broken for almost every AFFC arc
anchor**. Of ~20 phrases tested, only `Lady Stoneheart`→catelyn-stark and `Sand Snakes`→sand-snakes
HIT (both to *character* nodes, not the events meant). Everything else — `the Kingsmoot`,
`Cersei's arrest`, `arming the Faith Militant`, `death of Balon Greyjoy`, `Cersei's downfall`,
`walk of shame`, `Euron seizes the Seastone Chair` — returned **CANDIDATES (fuzzy)** or **MISS**.

This is the **S109 spaced-alias gap at AFFC scale**: the nodes exist but lack natural-spaced
`aliases:`, so a reader's phrase never resolves. Controls (`the Red Wedding`, `death of Tywin`,
`the Purple Wedding`) HIT because their arcs were built with spaced aliases. **Any AFFC arc build
must add spaced aliases to the beat-nodes it touches** (bake into the mint, per the arc-mint
machine).

### Three discoverability TRAPS to flag (wrong node looks right)
- `faith-militant-uprising` = **historical Targaryen-era** uprising (Aenys/Maegor, TWOIAF/F&B), NOT Cersei rearming the Faith in AFFC.
- `brienne-arrested` = **ASOS Harrenhal** (Jaime/Balon Swann), NOT the AFFC Stoneheart hanging.
- `conquest-of-dorne` = **Aegon's historical conquest**, NOT the AFFC Dornish vengeance plot.

---

## Bare nodes surfaced (→ harvest queue, demo-as-QA)

These AFFC event nodes have **no `## Quotes` block** (demo's wow-factor would come up empty):
`cersei-is-captured-in-the-sept`, `cersei-is-stripped-and-imprisoned`, `walk-of-atonement`,
`faith-militant-uprising`, `cersei-plots-against-margaery`, `brienne-arrested`,
`arrest-of-the-sand-snakes`. (Rows appended to `working/harvest-queue.md`.)

---

## RANKED AFFC FUMBLE LIST → re-prioritizes the next build

| Rank | Arc | Salience | Beat-readiness | Est. cost | Verdict |
|------|-----|----------|----------------|-----------|---------|
| **1** | **Cersei's downfall** | major (backlog #17) | **HIGH — beats exist, 1 with role edges** | 0–1 mint + ~5–7 edges | **BUILD NEXT — bumps Q5** |
| 2 | Kingsmoot → Euron | major (#20) | low — death-of-balon + euron-wins MISS | 2–3 mints + edges + retype | after #1 |
| 3 | Brienne → Stoneheart | major (#15/#19) | low — Stoneheart + hanging MISS | 2–3 mints; clean RW attach | after #2 |
| 4 | Dorne / Myrcella | medium | low — myrcella + plot MISS | 2–3 mints | defer |
| 5 | Greyjoy/Reach | — | folds into #2 | — | with #2 |

**Recommendation:** Make **Cersei's downfall the next build** instead of Q5. It is the single
cheapest-and-most-major AFFC arc (beats already minted, one already role-wired, clean self-caused
shape) and it opens the entire AFFC/ADWD layer that is currently 100% dark. Q5 (Crag→Jeyne) remains
queued as the cheap secondary dip. Final call is Matt's at session start.

---

## BUILD OUTCOME — Cersei's downfall arc SHIPPED (S114, same session)

Matt greenlit building the #1 fumble immediately. **The AFFC causal layer is no longer 100% dark.**

- **2 new beat-nodes:** `cersei-rearms-the-faith-and-forgives-the-debt` (event.incident, AFFC Cersei IV+VI) + `osney-kettleblack-confesses-to-high-sparrow` (event.incident, AFFC Cersei X) — both with spaced aliases + `## Quotes`.
- **5 causal Tier-2 edges** (all fresh-subagent CONFIRMED vs local cache → `verified_by: subagent-local-source-check-2026-06-20`) + **5 role Tier-1 edges**. edges.jsonl 22,279 → 22,289.
- **The self-caused irony walks:** `cersei-rearms-the-faith --CAUSES--> cersei-is-captured-in-the-sept --CAUSES--> cersei-is-stripped-and-imprisoned`, while the Margaery plot backfires: `cersei-plots-against-margaery --CAUSES--> osney-confesses --TRIGGERS--> capture`. `--causal-chain cersei-is-stripped-and-imprisoned` returns 4 upstream edges (was 0).
- **Discoverability fixed:** spaced aliases added to the 4 wired existing nodes + `walk-of-atonement`; `Cersei's arrest`, `arming the Faith Militant`, `Cersei rearms the Faith`, `Osney confesses to the High Sparrow`, `Cersei's plot against Margaery` all now HIT (were fuzzy/MISS).
- **Bonus data fix:** `cersei-is-stripped-and-imprisoned LOCATED_AT` retargeted `tower-of-the-hand` → `great-sept-of-baelor` (its own rationale/participant_name said Great Sept).
- Verifier adjudications (none refuted): edge 2 kept CAUSES (MOTIVATES type-invalid for event target; the High-Sparrow hinge is carried by the COMMANDS_IN role edge); edge 5 kept CAUSES (distinct durable states). The dropped `rearm→plot` edge correctly excluded (the plot is paranoia/valonqar-driven, independent of the rearming — preserving the irony).
- Mint: `scripts/mint_cersei_downfall_arc.py`; backups in `_regrounding/`.

**Remaining AFFC ranked queue (next builds):** #2 Kingsmoot→Euron (needs `death-of-balon` + `euron-wins` mints) · #3 Brienne→Stoneheart (needs Stoneheart + hanging mints; clean RW attach) · #4 Dorne/Myrcella. Plus the secondary Q5 (Crag→Jeyne, ASOS) still queued.

---

## Cross-cutting fixes worth folding into whichever AFFC arc is built first
- Add natural **spaced aliases** to every AFFC beat-node touched (resolver gap above).
- Retype `kingsmoot-on-old-wyk` `event.battle` → `event.ceremony` (assembly/election, not a battle).
- Consider whether `walk-of-atonement` should be an `event.*` rather than `concept.custom`.
