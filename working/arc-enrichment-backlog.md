# Enrichment Ledger — running list (to-do / in-progress / done)

> **What this is.** The single running list of enrichment work: what's been done, what's in
> progress, what's queued. **Enrichment = second-pass deepening of an already-built unit** —
> adding the braided side-plots, secondary-character sub-arcs, contemporaneous "revelation"
> events, descriptive/quote/object depth, and unproven-but-load-bearing edges that weren't on
> the first-pass spine.
>
> **Created 2026-06-20 (S116)** as the arc-enrichment backlog; **broadened to a full ledger
> 2026-06-22 (S130, Matt)** to cover three UNIT kinds and to track status, not just queue work.

## STATUS: enrichment PHASE is OPEN (gate tripped S130)

The S116/S117 gate was "enrichment opens once Essos is spine-built AND WO5K #3/#4/#5 are built."
**As of S130 ALL 5 approved containers are spine-complete** (essos S119–120 · wo5k S123 · north
S125–126 · aegon S128 · bran S130). The gate has tripped and then some — **enrichment is now the
primary track** (Matt S130: "clear low-value remainders, then enrichment dips"). The
`major-arc-backlog.md` DARK count is down to the deep-lore / theory long tail.

## Enrichment UNITS (Matt S130 — three kinds, not just arcs)

Enrichment isn't only arc/cluster-shaped. A unit is anything with a built skeleton worth deepening:

1. **Arc / cluster** — a built causal spine (the original S116 unit). e.g. Kingsmoot→Euron, Red Wedding.
2. **Major character** — deepen one character's connection web across/within containers. e.g. **Bloodraven**
   (kin, rivalry, office, artifact, D&E links), **Bran** (the greenseer arc), Euron, Littlefinger, Varys.
3. **Major event within a container** — deepen one load-bearing event's surrounding texture / participants /
   revelations. e.g. the Purple Wedding whodunit layer, the Red Wedding's Frey/Bolton sub-plots.

**Multi-pass per unit is expected, not one-and-done** (S116 lesson, reaffirmed S130): the same cluster /
character / event can be enriched repeatedly — each pass (fresh subagents + accumulated harvest finds +
newly-built neighbor units) yields new connections. Track the **pass number** per unit below.

### Sequencing — the descent (Matt S130, SHARPENED S131)

**One enrichment dip per session (Matt S131).** Enrichment is its own session each time — don't bolt it onto a
remainder/build session. The low-value remainders are now CLEARED (S131: AEGON Victarion-voyage + NORTH N6);
the next session opens the enrichment phase proper.

**The order is a top-down DESCENT, not a flat two-bucket split (Matt S131):**
1. **Major narrative arcs FIRST** — the big causal spines (Red Wedding, Robert's Rebellion, the Essos/Dany
   spine, the AEGON invasion, the WO5K, etc.). Deepen the arc as a whole before zooming in.
2. **THEN granular clusters / sub-plots WITHIN those arcs** — the braided side-plots, secondary-character
   threads, and revelation-events that hang off each major arc (e.g. within the Red Wedding: the Frey/Bolton
   mechanics; within Dorne: the Queenmaker informer mystery).
3. **THEN individual characters — maybe, and LAST** (Matt S131: "and then individual characters maybe?").
   The character phase is tentative and comes after the arc + sub-plot work, because by then most of a
   character's web is already built as a by-product of the arcs they appear in.

**"No lead" + a BROAD roster, not a Bloodraven focus (Matt S131):** within any level everything matters — no
single "#1." **Bloodraven is flagged but is one of MANY character candidates, NOT the focus** (Matt S131:
"bloodraven is flagged but there should be more characters so we don't focus solely on him"). The character
roster is wide — Jon Snow, Daenerys (the raw-importance heavyweights), Littlefinger, Varys, Tyrion, Cersei,
Jaime, Stannis, Bran, Euron, Bloodraven, and more. Pick the next unit by what's ready / what a dip shows
demand for, not by a standing favorite.

**A dedicated PLANNING session sits between the arc phase and the granular phase (Matt S130):** after the major
arc enrichments are done, run a session whose whole job is to *enumerate and scope the granular cluster/
sub-plot/character dip list*. The character/event entries below are **seeds**, not the final plan — by the
time the arc work is done we'll know far more about what each cluster actually needs, so the real granular list
gets built then. Full sequence: **low-value remainders [DONE S131] → major narrative-arc enrichments →
[planning session: scope the granular dip list] → granular clusters/sub-plots → individual characters (maybe)**
(D&E full-Opus Pass-1 batch slots in after the first enrichment passes).

> **PLANNING-SESSION AGENDA ITEM (deferred S135, Matt — "make sure it comes up after the first round of
> enrichments"):** spec + build the **harvest texture-sweep + grep post-pass** — full parked design in
> `working/harvest-texture-sweep-deferred.md` (Sonnet full-chapter sweep run broadly; Python grep as a
> POST-pass auditor/seeder, never a pre-filter; `dedup_key` + attach cadence). Do NOT build before this
> planning checkpoint. The "split the harvest bar" piece (Tier 1, free) is separate and already in the live
> dip prompts.

---

## Ledger — enrichment passes per unit

> **Status is a COUNT, not a binary** (Matt S130). A unit is never "done" — it's "1 enrichment pass done,"
> "pass 2 done," "3 done," and can always take another (multi-pass is the norm). `0` = no deliberate pass yet
> (may carry incidental overlays from a spine build — noted). Increment the count + log the pass when one ships.

| Unit | Kind | Passes done | Last pass | Notes |
|------|------|:-----------:|-----------|-------|
| Kingsmoot → Euron | arc/cluster | **1** | S116 | +2 beat-nodes, +6 edges, +12 descriptive attachments, +1 edge type (`SUSPECTED_OF`), ~14 harvest pointers; + 3 bridge nodes minted-in-place. Pass 2 candidates: Crow's Eye voyages, dragonbinder, bastard sons. |
| Robert's Rebellion | arc/cluster | **1** | S133 | First major-arc enrichment (board-picked, unanimous A/B/C). +3 nodes (`knight-of-the-laughing-tree-incident`, `exile-of-jon-connington`, `murder-of-jon-arryn`) + 24 edges (22 board + 2 A/B-bonus; 1 junk `GUEST_OF` dropped, 1 ENABLES rejected at fresh-verify) + 4 book-cite overlays + alias fix. Wired the dead-end cluster FORWARD: **RR→AEGON** (`battle-of-the-bells CAUSES exile-of-jon-connington ENABLES aegon-revealed`) + **RR→WO5K** (`coronation ENABLES wedding-of-robert-and-cersei`). Jon-Arryn-murder reified (lysa AGENT_IN; petyr+cersei SUSPECTED_OF — the false in-world misdirection); R+L contested-agency `rhaegar SUSPECTED_OF abduction-of-lyanna`; Howland/Ned WITNESS_IN ToJ; wildfire-cache agents. Fresh-verify 6 CONFIRM/2 ADJUST/1 REJECT (dropped `wedding ENABLES death-of-robert` as agency-collapse — RR→WO5K death-link deferred to a properly-sourced MOTIVATES). 0 drift, 0 new types. **Pass 2 candidates:** RR→Essos seam (`exile-of-viserys-and-daenerys`, deferred to Essos enrichment); Tower-of-Joy interior (gated); the Knight-of-the-Laughing-Tree squire identities; `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` vocab decision (Matt). |
| Bloodraven / Brynden Rivers | character | **0** | — | incidental S130 overlay only (cave-form appearance + self-id book-cite). Pass 1 = the D&E deep-connections dip (scope below). |
| Bran (greenseer arc) | character | **0** | — | incidental S130: 12 anchor quotes on the 8 new beats. Pass 1 = the journey-deepening dip (scope below). |
| AEGON cluster | arc/cluster | **0** | — | S129 prose-only harvest-consume (overlays onto jon-connington/aegon/varys) — not a full pass. |
| WO5K container | arc/cluster | **0** | — | needs MANY passes (Karstark/Frey/Bolton/Riverlands/westerlands). |
| Red Wedding | arc/cluster | **1** | S134 | Second major-arc enrichment (board-picked). +2 nodes (`grey-wind-killed-at-the-twins`, `edmure-taken-hostage-at-the-twins`) + 23 edges + 14 descriptive quote/appearance attaches. **Fixed the dead-end hub** (downstream 1→ traversing chain): RW→roose-warden→{stannis-march, fArya-wedding}; wired 2 causal islands — `ser-wendel-manderly-is-killed MOTIVATES wyman-...-davos` (the North-remembers seam) + `the-rains-of-castamere TRIGGERS red-wedding` (the massacre-signal text node, was edge-less); `red-wedding`/`edmure-hostage ENABLES siege-of-riverrun`. Planner/witness substrate: Lothar AGENT_IN/COMMANDS_IN, Bastard-Walder (`walder-rivers`) AGENT_IN camp, Edwyn/Smalljon/Greatjon/Merrett role edges, Catelyn WITNESS_IN robb-killed, Arya WITNESS_IN camp. **4th causal-wiring lens** added to the board (S133 A/B finding banked) — it produced the 2 island-fixes. Fresh-verify 3 CONFIRM/3 ADJUST (warden→fArya ENABLES→MOTIVATES T2; warden→stannis & rw→siege → T2; merrett AGENT_IN→PARTICIPATES_IN). 0 drift. **REJECTED at synthesis:** `blackfish-escapes-the-twins` node (factually wrong — Blackfish held Riverrun, never at the Twins); `red-wedding CAUSES guest-right`(concept, novel pattern→ATTACH_QUOTE); `roslin SUSPECTED_OF conspiracy` (overclaims coerced victim). **Pass 2 candidates:** Frey-pies/GNC layer, Riverrun-siege downstream, the bedding sub-beats, Manderly-hostage (Wylis) thread, Arya post-RW kill-list node. |
| Purple Wedding | arc/cluster | **1** | S135 | Third major-arc enrichment (board-picked — consensus of 3 advisors; only arc in all three top-3s). +0 nodes (edge-only pass) + 16 edges. **Lit the dead-dark hub** (was 0 causal): `death-of-joffrey-baratheon` now walks **18 edges downstream** (TRIGGERS littlefinger-smuggles-sansa + ENABLES wedding-of-tommen; the existing trial→Oberyn→Tywin→Cersei-imprisonment→GC-landing chain now hangs off the death). **Whodunit layer** (the marquee gap): `tyrion-lannister` + `sansa-stark` SUSPECTED_OF death-of-joffrey (in-world false blame; Olenna/LF stay the true AGENT_IN/COMMANDS_IN). `petyr-baelish MOTIVATES olenna-tyrell` (the framing-seed) + `littlefinger-brokers-tyrell-lannister-alliance ENABLES joffrey-sets-sansa-aside`. Witness substrate: 5 WITNESS_IN (sansa/tyrion/margaery/tommen/loras). Object layer (3 islanded artifact nodes wired first time): joffrey OWNS widows-wail + wedding-chalice; strangler + wedding-chalice WIELDED_IN the death. `killing-of-dontos-hollard` integrated SUB_BEAT_OF. Fresh-verify (independent Sonnet) **6 CONFIRM / 3 REJECT**: dropped `betrothal ENABLES death` (too distal/agency-collapse), `dontos-killing ENABLES smuggle` (TEMPORAL INVERSION — Dontos shot after Sansa aboard), `smuggle ENABLES petyr-lysa-wedding` (incidental co-location). Synthesis also caught the lenses conflating `tyrell-plot-revealed` (the Sansa→Willas plot, NOT the murder). 0 drift, 0 new types (132). +14 harvest rows. **Pass 2 candidates:** the deferred `silver-hairnet-of-sansa-stark` artifact node + `sansa-assumes-alayne-stone-identity` Vale-arc node; the Kettleblack triple-agent web; Dornish-succession (Myrcella) downstream seam; feast food-nodes. |
| Tywin's death · Blackwater · Ned's downfall · Sack of KL | arc/cluster | **0** | — | each has off-spine side-plots. |
| Cersei's downfall · Brienne→Stoneheart | arc/cluster | **0** | — | AFFC secondary beats. |
| Dorne / Myrcella (Queenmaker) | arc/cluster | **0** | — | 19 harvest rows pushed S117. |
| Essos clusters | arc/cluster | **0** | — | Slaver's Bay/Meereen sub-plots; Fire-and-blood reveal. |
| Euron | character | **0** | — | + the gated Euron↔Bloodraven evidence thread (scope below). |
| Jon Snow · Daenerys | character | **0** | — | heavyweight character units (huge cross-container webs) — character phase. |
| Purple Wedding whodunit · Red Wedding Frey/Bolton mechanics | event | **0** | — | event-unit candidates. |

*(The detailed next-pass scope for the Matt-flagged units follows; the table above is the at-a-glance count.)*

---

## Next-pass scope — character units (broad roster — comes LAST, after arcs AND their sub-plots; Matt S131)

> **Characters are the LAST level of the descent and tentative** ("individual characters maybe?", Matt S131).
> Most of a character's web gets built as a by-product of the arc + sub-plot enrichments they appear in, so the
> dedicated character phase is for what's left. **Bloodraven is ONE of many, not the focus** — the roster is wide
> (Jon, Dany, Littlefinger, Varys, Tyrion, Cersei, Jaime, Stannis, Bran, Euron, Bloodraven, …). The Bloodraven
> hooks below are kept because they're concrete, not because he leads.

> No "lead" here (Matt S130). By raw importance the heavyweights are **Jon Snow** and **Daenerys** (each a huge
> cross-container web — queue them when the character phase opens). **Bloodraven, Bran, Euron** below are
> Matt-flagged specifics with concrete hooks, not a ranking. Also eventually: Littlefinger, Varys, Tyrion, etc.

### Bloodraven / Brynden Rivers — deep connections back through Dunk & Egg
**Matt S130: "we def need more bloodraven deep connections going all the way back to dunk and egg bc
bloodraven / brynden rivers big in theories."** Full scope + dedup baseline: memory
`project_bloodraven_enrichment_dip`. Builds the *evidence substrate* (Tier 1–2 connection edges) the
gated theories track was waiting on — **theory READINGS stay gated** (`project_theories_track_deferred`).
- Kin/rivalry: Bittersteel (Aegor Rivers, half-brother + nemesis), Daemon Blackfyre, Melissa Blackwood
  (mother), Aegon IV (father), the Great Bastards; enrich the existing `LOVER_OF shiera-seastar`.
- Office/political: Hand to Aerys I + regency; killed Aenys Blackfyre under guest-right → the Wall; Great
  Council 233; the thousand-eyes spy network.
- **D&E book-cite overlays** (no Pass 1 yet — read the novella files directly): `tmk/tmk-dunk-01.md` (on-page
  at Whitewalls, the Second Blackfyre plot, the Bittersteel capture) primary; `tss`/`thk` references.
- Artifacts/companies: Dark Sister (WIELDED), the weirwood longbow, the **Raven's Teeth** (COMMANDS).
- Wall/cave (some built S130): confirm `coldhands SERVES/SWORN_TO` points to `brynden-rivers` not the
  `three-eyed-crow` species node (S130 slug trap); children of the forest; mentor-to-Bran.

### Bran — the greenseer arc deepening
The S130 spine is built (8 beats). Enrich: the 4 still-open `bran-dip` harvest rows (Old Nan Long-Night
foreshadowing, weirwood-paste food node, cave floor-bones place, the becoming-a-weirwood foreshadowing) +
the research subagents' batchA/batchB rows; the Bran↔Jojen greendreaming dyad (D3, `working/dyad-queue.md`);
descriptive depth on the journey beats. Pairs naturally with the Bloodraven pass (shared cave cluster).

### Euron — incl. the Euron ↔ Bloodraven connection thread
**Matt S130: "theories that Euron is connected to bloodraven."** The Euron spine is built (Kingsmoot, S116).
Enrich Euron's own web (Crow's Eye voyages, the dragonbinder, the bastard sons) AND the textual Euron↔
Bloodraven links (the shade-of-the-evening / sorcery / "thousand eyes" resonances) **as evidence edges only**
— the theory that they're connected is a GATED reading, but the on-page links that fuel it are fair Tier-2
substrate. Surface to the theories track when it opens.

## Next-pass scope — arc / cluster units (these go first; multi-pass expected)
- **WO5K container** — needs MORE than one pass (Matt: "gonna need more than that treatment"): Karstark, Frey,
  Bolton, the Riverlands chevauchée, Robb's westerlands campaign.
- Red Wedding · Purple Wedding · Tywin's death · Blackwater · Ned's downfall · Robert's Rebellion · Sack of KL —
  each has side-plots not on its spine.
- Cersei's downfall + Brienne→Stoneheart (AFFC, S114/S115) — the Blue Bard, the Faith Militant's rise, the
  Brotherhood's hangings.
- **Dorne / Myrcella (Queenmaker, S117)** — the "Someone always tells" informer mystery; Arys Oakheart's
  seduction sub-arc; the conspirator dispersal (Drey→Norvos, Garin→Tyrosh, Sylva→Greenstone); Darkstar's escape
  (downstream-dark). 19 harvest rows pushed S117.
- **Essos clusters** — the Slaver's Bay / Meereen braided sub-plots; the Quentyn/Doran "Fire and blood" reveal
  (Essos-bridge seed).

## Next-pass scope — event units within containers
- Purple Wedding whodunit layer (the poisoner attribution — `SUSPECTED_OF` candidates).
- Red Wedding internal Frey/Bolton mechanics.
- (add as dips surface them.)

---

## ROADMAP — Dunk & Egg full Opus Pass-1 batch (Matt S130)

**D&E Pass 1 is being UN-DEFERRED.** Matt S130: "we can do Dunk And Egg full Opus analysis batch job soon …
cake compared to doing an analysis over a whole book, plus we have come so far since the first book passes, we
can def make those prompts better." So:
- **Scope:** the 3 novellas (THK/TSS/TMK), full Opus mechanical Pass 1 — small vs a full book.
- **Improve the prompts first:** the v3 Pass-1 prompt predates everything we've learned; revise before running
  (the "make those prompts better" step). The D&E extractions then feed the Bloodraven enrichment with proper
  structured nodes instead of book-cite-overlay-only.
- **RUN IT UNATTENDED via `longrun.sh` — and use it to TEST that machinery (Matt S130).** D&E is the ideal
  test payload for the unified worker script (`scripts/worker-template.py`) + `longrun.sh` supervisor (S97/S99;
  survives rate-limit walls, auto-resumes — cf. `scripts/stage4-run-forever.sh`, memory
  `project_stage4_run_forever_wrapper`): small, self-contained, mechanical. Write a D&E **sub-script** (worker
  config for the 3 novellas) and let longrun drive it. This **decouples D&E from the enrichment ordering** — it
  no longer has to wait for "after the first enrichment passes"; it can run **CONCURRENTLY / in the background**
  whenever Matt has spare usage or is away during the (interactive, one-at-a-time) enrichment runs. Two wins in
  one: get D&E extracted AND exercise the unattended-longrun pipeline that hasn't been run in a while.
  **Caveat:** per `feedback_no_extraction_without_asking`, confirm with Matt before launching any extraction.
- Today (before that batch): Bloodraven D&E links come via the **book-citation-overlay** pattern
  (`feedback_book_citation_overlay_value`) — read the novella files directly, attach `chapter:line` cites.

---

## A/B model experiment — Sonnet-lens board vs. max-effort Opus (S133, Matt-requested)

**Setup.** After shipping the RR pass via the standard machine (3 Sonnet lenses + Opus orchestrator synthesis +
Sonnet fresh-verify), we ran ONE max-effort **Opus** analyst doing the ENTIRE RR enrichment scope as a single
blind pass (deduped against `baseline.md` only; did not read the lens/synthesis files; treated the parallel-minted
nodes as non-existent). Proposal: `working/enrichment/rr/proposal-opus-ab.md` (51 items).

**Verdict — a MODEST but real difference; orchestration matters more than proposer-tier.**
- **~90% convergence on the high-value core.** Opus independently arrived at the SAME 3 new nodes (KotLT-incident,
  exile-of-jon-connington, murder-of-jon-arryn), the SAME RR→AEGON bridge, the SAME Jon-Arryn substrate
  (lysa AGENT_IN / petyr+cersei SUSPECTED_OF), the SAME ToJ witnesses, the SAME wildfire overlays, the SAME junk-drop
  and the SAME `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY` NEEDS_VOCAB hold. → **strong validation of the cheaper Sonnet board.**
- **Opus caught a real coverage SEAM the lens-division missed:** existing-node→existing-node causal edges that no
  single Sonnet lens "owned." Two were genuine, well-grounded, structural-gap fixes and were **minted as A/B bonus**
  (run_id `rr-enrichment-s133-ab`): **`roberts-rebellion MOTIVATES robert-orders-daenerys-assassination`** (gave the RR
  hub its FIRST real outgoing edge — the cluster head was a dead-end; also a clean RR→Essos seam) +
  **`wildfire-plot MOTIVATES slaying-of-aerys-ii-the-kingslaying`** (Jaime's stated motive for the kingslaying).
- **Opus was slightly NOISIER on dedup** (re-proposed 4 already-existing nodes; correct per its blind rule but it would
  have needed a synthesis pass to filter). Its rejection reasoning was strong (caught agency-collapse, Rhaegar-died-first,
  granularity overclaim) — comparable to our fresh-verify.
- **Caveat (not a clean RCT):** the Sonnet path had Opus orchestration + a fresh-verify layer; the Opus path was a raw
  single agent with neither. The honest lesson: **the model tier of the proposal agents is NOT the bottleneck — the
  orchestration structure (shared dedup baseline + holistic causal-wiring lens + fresh-verify) is.** The lens division
  itself created the only real gap, and a holistic causal pass (any tier) closes it. RECOMMENDATION for future dips: keep
  the cheap fanned-out board, but ADD one explicit "existing-node↔existing-node causal wiring" lens to the board so the
  seam doesn't recur (Opus-as-proposer is not required to get those edges).
- **Held for RR pass 2** (Opus-found, lower-priority / more interpretive): `murder-of-elia… MOTIVATES landing-of-the-golden-company`
  (Tier-2, the survival-claim premise — wants fresh-verify); trident book-cite overlay (Robert "drove the spike… into his
  black heart", agot-eddard-10:171); `lyanna LOCATED_AT tower-of-joy`; atrocity-node AGENT_IN re-targeting.

## The enrichment-pass machine (smoke-tested S116)

1. **Fan out 2–3 fresh subagents, each a different lens** on the built unit:
   - secondary-character sub-arcs (the braided side-POVs),
   - thread/revelation + contemporaneous events + any unproven-but-load-bearing claims,
   - descriptive/quote/object depth (the "what does X look like" layer).
   Paste vocab + the harvest snippet; tell them PROPOSE-don't-mint + dedup-check every node.
2. **Synthesize + decide** what's worth minting vs deferring (forward-dangling cross-book nodes defer).
3. **Verify every cited line against the files** (subagents reconstruct quotes — always check),
   mint nodes/edges via a `scripts/mint_<unit>_enrichment.py` (backup + re-run guard),
   **fresh-verify the interpretive edges**, stamp, rebuild derived artifacts.
4. **Consume the harvest pointers** the dip refilled.

## Enrichment yield is real (S116 evidence)

One already-harvested cluster → **+2 beat-nodes, +6 edges, +12 descriptive attachments, +1 new edge type
(`SUSPECTED_OF`), ~14 fresh harvest pointers**, almost no overlap with the first harvest pass. The hypothesis
("a cluster can be enriched several times and keep yielding") held.

## Process rules
- Forward-dangling cross-book nodes **defer to the downstream container's enrichment**, not minted into a void.
  (S116 refinement: a node is only forward-dangling if its UPSTREAM is missing; if upstream exists, mint now.)
- Interpretive/causal enrichment edges get the same **fresh-subagent verify** as spine edges.
- `SUSPECTED_OF` (S116) is the type for unproven-but-load-bearing agency (Tier-2, never asserts the act).
  Reuse for Jon Arryn's murder, Joffrey's parentage, the Purple Wedding poisoner, etc.
- **Theory READINGS stay gated** (`project_theories_track_deferred`); enrichment builds the Tier-1/2 evidence
  substrate those theories will later traverse, but does not assert the theory.
- "Log it for later" is the same fragile deferral as parking a node — if you have the verbatim quote + a valid
  home NOW, attach it now. The only true deferrals are missing-upstream or missing-source.
