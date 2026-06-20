# Major Narrative-Arc Backlog (research-first, magnitude-ordered)

> **Created 2026-06-20 (post-S111), Matt-directed strategy pivot.** Replaces the dip-cheapest
> *prioritizer* with a planned major-arc backlog. The dip stays — but as a coverage/precision
> CHECK after building, not the thing that picks what we build. Cheap dips become a *secondary*
> opportunistic track (captured during major-arc research, batched later).
>
> **Anchor lens (Matt):** "major events that happened in-book that were foreshadowed" →
> `reference/foreshadowing-events.md` (30 events + 15 Chekhov's guns). Foreshadowed = GRRM-planted
> = load-bearing-by-construction, so it's a pre-curated inventory of the *major* arcs worth building.
> Bonus: building these sets up the deferred Pass 4 FORESHADOWS layer.

## How this was scored (verified vs the live graph, not memory)

Each of the 30 events checked against the causal-touched node set (`CAUSES`/`TRIGGERS`/`MOTIVATES`
endpoints in `edges.jsonl`, 2026-06-20). **Causal layer reaches 49 of 619 event nodes (~8%).**
Status = BUILT (causal chain exists) · PARTIAL (some beats wired, spine incomplete) · DARK (0 causal).

## The map — 30 foreshadowed events

| # | Event | Book | Status | Notes / what's missing |
|---|-------|------|--------|------------------------|
| 1 | Jon Arryn's murder | pre-AGOT | **DARK** | The inciting misdirection (Lysa+Littlefinger). High value — roots the whole series. |
| 2 | Bran's fall | AGOT | BUILT | S105 |
| 3 | Ned's execution | AGOT | BUILT | B3 S108 |
| 4 | Robert's death | AGOT | BUILT | B3 S108 (death-of-robert-baratheon) |
| 5 | Drogo's death / dragon birth | AGOT | **DARK** | Essos. Bridges: Robert's assassination order → hardens Dany; Drogo's vow to take Westeros. |
| 6 | Catelyn seizes Tyrion | AGOT | BUILT | Bran arc S105 |
| 7 | Battle of the Blackwater | ACOK | **PARTIAL** | Downstream BUILT (S111); **upstream DARK** (Renly's death → Stannis marches → Blackwater). |
| 8 | Theon takes Winterfell | ACOK | **PARTIAL** | B2 ends at theon-ward; the actual capture + Bolton "sack" DARK (Q13). |
| 9 | House of the Undying visions | ACOK | DARK* | *Prophecy layer — belongs to Pass 4/5, not causal-arc track. |
| 10 | Renly's death (shadow) | ACOK | **DARK** | = the Blackwater UPSTREAM. Shadow assassin → Stannis's path to KL + Tyrell realignment. |
| 11 | Red Wedding | ASOS | BUILT | B1 S107 (rich) |
| 12 | Purple Wedding | ASOS | BUILT | S106 |
| 13 | Oberyn vs the Mountain | ASOS | BUILT | Tywin arc S109 |
| 14 | Tyrion kills Tywin | ASOS | BUILT | S109 |
| 15 | Stoneheart reveal | ASOS | **DARK** | Beric → Catelyn resurrection; ties to Brienne (#19). |
| 16 | Jon becomes Lord Commander | ASOS | **DARK** | NW election; sets up #21. |
| 17 | Cersei's arrest by the Faith | AFFC | **DARK** | Cersei arms the Faith Militant → own downfall (clean self-caused arc). |
| 18 | Pate / Jaqen at the Citadel | AFFC | DARK* | Faceless Men; partly mystery-layer. |
| 19 | Brienne's "death" | AFFC | **DARK** | Stoneheart (#15) downstream. |
| 20 | Euron's Kingsmoot victory | AFFC | **DARK** | Dragonbinder; Greyjoy succession after Balon. |
| 21 | Jon's assassination | ADWD | **DARK** | Pink letter → Shieldhall → "for the Watch." Major. |
| 22 | Dany rides Drogon / escapes Meereen | ADWD | **DARK** | Essos. Slaver's-Bay campaign (the Q11 territory). |
| 23 | Aegon's landing | ADWD | **DARK** | **Varys+Illyrio conspiracy bridge (Essos↔Westeros), seeded AGOT.** |
| 24 | Stannis marches on Winterfell | ADWD | **DARK** | Grand Northern Conspiracy; Manderly; Karstark. |
| 25 | Varys assassinates Kevan | ADWD | **DARK** | Epilogue; clears path for Aegon (#23). |
| 26 | Quentyn's death | ADWD | **DARK** | Dorne↔Essos bridge (Doran's plan). |
| 27 | Manderly's Frey pies | ADWD | **DARK** | Part of #24 (Grand Northern Conspiracy). |
| 28 | R+L=J setup | all | DARK* | *Theory/prophecy layer — Pass 5, not causal-arc. (abduction-of-lyanna IS built as an RR spark.) |
| 29 | The Others' true nature | all | DARK* | *Theory layer. |
| 30 | Doom of Valyria | pre-series | DARK** | **Deep-lore → TWOIAF/F&B ingestion track, NOT curator-minting (strategy doc Tier C). |

**Also BUILT but not in the numbered list (pre-series):** Robert's Rebellion (8-beat chain), Sack of King's Landing (S106). Greyjoy Rebellion → Theon-ward (B2).

### Tally
- **BUILT: ~10** — all AGOT/ASOS Westeros core (+ 2 pre-series).
- **PARTIAL: 2** — Blackwater (upstream dark), Theon-takes-Winterfell.
- **DARK and in-scope for this track: ~14** — concentrated in (a) AFFC/ADWD Westeros late-series, (b) Essos, (c) Blackwater-upstream/Renly.
- **Out of this track:** #9/#18/#28/#29 (prophecy/theory → Pass 4/5); #30 (deep-lore → TWOIAF/F&B).

## What this confirms

We did the **cheap-and-major** arcs (single arc, in-saga AGOT/ASOS, beats-mostly-existed) and the
dip-cheapest gate then started scraping refinements. The **expensive-and-major** structure is all
still dark: the **WO5K connective spine**, the **entire Essos thread**, and the **whole AFFC/ADWD
layer**. Not chronological, not magnitude — it was cheapest-first, which front-loaded the easy wins.

## Recommended build order (magnitude-first, Matt's call = WO5K spine first)

### 1. WO5K causal spine (FIRST) — ties together pieces already built
The single biggest overarching event; 69 sub-battles PART_OF-attached, **0 internal CAUSES**. We do
**NOT** mint the full mesh (strategy hard-rule) — only the load-bearing junctures, and we **never**
chain CAUSES into the `war-of-the-five-kings` terminus node (multi-attributed). The spine connects
the already-built RW / Blackwater / Greyjoy / Tywin sub-arcs and adds the missing connective beats:
- **Renly's death (#10) → Stannis marches on KL → Battle of the Blackwater** — gives Blackwater its missing UPSTREAM (#7 partial → complete) + the Tyrell realignment.
- **Robb's victories → political isolation → Karstark execution (built) → Frey/Bolton defection → Red Wedding (built)** — the "wins battles, loses the war" causal logic PRECEDES already orders but doesn't *cause*.
- **Balon's invasion → Theon takes Winterfell (#8) → Bolton sack → North destabilized** — completes #8.

### 2. Essos thread (NEXT major) — separate theater, SHARED plot (bridges first-class)
- Drogo's death/dragon birth (#5) → Slaver's-Bay campaign (#22, the Q11 territory) → escape from Meereen.
- **Cross-theater bridges (model as first-class edges):** Robert orders Dany assassinated → MOTIVATES Dany / Drogo's westward vow; Jorah spies for Varys (Essos→Westeros info channel); **Illyrio↔Varys** Targaryen-restoration conspiracy → Drogo marriage pact + sheltering "Young Griff"/Aegon (#23) + Golden Company.

### 3. AFFC/ADWD Westeros late-series layer
- Cersei's self-caused downfall (#17, Faith Militant — clean self-arc); Stannis-marches/Grand Northern Conspiracy (#24 + #27 Frey pies); Jon's assassination (#21); Stoneheart→Brienne (#15→#19); Euron's Kingsmoot (#20); Varys kills Kevan (#25, bridges to Aegon).

### Deferred / other tracks (not this backlog)
- Prophecy/theory events (#9, #18, #28, #29) → Pass 4 (foreshadowing) + Pass 5 (theory).
- Deep-lore (#30 Doom, Targaryen Conquest, Dance, Blackfyre) → TWOIAF/F&B ingestion track.

## Process rules locked this session (Matt)

1. **Two tracks.** Primary = planned major arcs (this backlog, magnitude-ordered). Secondary =
   opportunistic cheap dips (the long tail). Don't lose the cheap dips — but they don't drive the roadmap.
2. **Cheap-dip backlog.** During major-arc research, *capture* cheap-dip gaps we pass (like the harvest
   queue, but for small arc gaps) → `working/cheap-dip-backlog.md`. If they cluster logically (by
   event/region), batch them. Build them between major arcs or when a session ends light.
3. **Harvest cadence.** A harvest *consume-pass* triggers at **~20–30 open rows** in
   `working/harvest-queue.md` OR after any text-heavy session — whichever first. The threshold NEVER
   caps pointer-dropping mid-session: pointers stay always-on, a session can end at 40+ rows, the
   next harvest pass clears them. The harvester (push snippet) runs on **any** text-reading pass —
   major-arc research included, not just dips.
4. **Bridges are first-class.** Westeros and Essos are one graph; cross-theater causal/role edges
   (Robert's assassination order, Illyrio↔Varys, Jorah-spies-for-Varys) get modeled, not dropped.
5. **Dip = check, not prioritizer.** Re-dip AFTER building (precision/coverage check); the backlog picks the work.
