# Stage-2 Smoke Eval — `fab-heirs-of-the-dragon-15-p01` (fresh adversarial review)

**Verdict: PASS-WITH-CONCERNS** — the ambiguity machinery mostly held under real same-name load:
all 16 merge-plan UPDATE targets and every person/dragon/event edge endpoint in `candidates.json`
route to the RIGHT individual, the S199 quote repair is 31/31 sound, and CREATE discipline collapsed
from Stage 1's 36 (~19 wrong) to 4 (all genuinely new). But two blocker-class defects remain before
apply: (1) one confident-wrong-match DID occur in the matched-41 — `Lorath` (a Free City, roster type
`place`) resolved `hit-character` score 1.0 onto **`jaqen-hghar`** via a junk character alias, proving
clean-hit routing is type-blind; and (2) the `run_id` drops the `-pMM` part suffix, so a same-day bulk
run of p01/p02/p03 would make `fab_merge_node.py` silently skip parts 2–3's UPDATE prose on every
shared node (Daemon, Viserys, Rhaenyra, Otto, Alicent appear in all three parts). Nothing is minted;
both fixes are small and deterministic.

## Metric read
113 rostered → 41 matched / 85 review / 4 created; 31 edges emitted (edges with review-routed
endpoints correctly held back); quotes 91, 1 quarantined (98.9% located), **31 repaired**; prose
quotes 59/60; needs_vocab 2; disputed_rate 0.065 (= 2/31). Plausible shape — but note 57 of the 85
review rows are exact-1.0 clear-margin matches (over-deferral, quantified in §B7), and the shipped
review rows are **stale relative to the current script** (§B8).

---

## A. Same-name routing — the point of this smoke — HELD, with one wrong match and one recall gap

1. **Matched UPDATEs (sampled all 16 merge-plan targets + ~25 edge endpoints, i.e. >15): every
   person routing is the right individual.** Verified against node files: `jocelyn-baratheon`
   ("married to Aemon Targaryen (son of Jaehaerys I)"), `daemon-targaryen` ("child of Alyssa and
   Baelon (son of Jaehaerys I)"), `alyssa-targaryen` (wiki page = Jaehaerys's daughter; Alyssa
   Velaryon is a separate node), `lord-hightower` (the unnamed elder brother of Otto, `PARENT_OF
   Ormund` — right node for E42), `mysaria` ("sworn to Blacks; Mistress of whisperers"),
   `saera-targaryen`, `maegelle-targaryen`, `vaegon-targaryen`, `yorbert-royce`, `jeyne-arryn`,
   `runciter`, `ryam-redwyne`, `rhea-royce`, `aemma-arryn`, `boremund-baratheon`, dragons
   `syrax`/`seasmoke`/`silverwing`, events `second-quarrel`/`great-council-of-101-ac` (both exist —
   no dupe mint). `Aegon the Conqueror` resolves to `aegon-i-targaryen`, NOT the `aegon-targaryen`
   trap — **the R1 trap held again**; no blocklisted node appears anywhere.
2. **BUT: `Lorath` → `jaqen-hghar`, status `hit-character`, score 1.0 — a confident wrong match
   inside the matched 41.** Root cause: `graph/nodes/characters/jaqen-hghar.node.md` carries
   `aliases: ["Lorath"]` (an alias-hygiene violation — a place name on a character), and the router's
   rule-1 clean-hit path never checks the roster `Type guess` (`place`) against the node category
   (`characters`). Blast radius in THIS unit is zero — Lorath is roster-only (no prose, no edges), so
   nothing lands in `candidates.json`/`merge-plan.json` — but the class is exactly R1: a prose-bearing
   row hitting a junk alias would append F&B prose to the wrong node. The review pile shows two live
   near-misses of the same class: `Cod Queen`/`Summer Maid`/`Ice Wolf` (ships) top-match 1.0 onto
   `titles`-category nodes, and `Merling King` (legendary figure) top-matches 1.0 onto the
   `merling-king` **artifact** while the right target (`merling-king-god`, religions) sits at 0.767.
   **Type agreement must gate clean hits.**
3. **Cluster routing (all 10 `smoke-auto-accept-disabled` rows examined): 9/10 top-scored candidates
   are the right individual** (Aemon→`-son-of-jaehaerys-i`, Rhaenys→`-daughter-of-aemon`,
   Maegor→`maegor-i`, Gaemon→`-son-of-aenar`, Laena, Daella, Corlys, Balerion vs `balerion-cat`,
   Baelon top-of-tie). The 1 wrong-at-top: **Rhaena Targaryen** — top pick
   `rhaena-targaryen-daughter-of-daemon` (score 1, pack-expected only); the text's Rhaena ("sister of
   Jaehaerys I", dragon-egg-cradle originator) is `rhaena-targaryen-daughter-of-aenys-i` (scored 0 —
   the registry has no sibling field, and pack-expectedness is a unit-level prior that actively
   misleads on retrospective mentions). Under the bulk accept rule (≥2 discriminators AND runner-up
   zero) Rhaena stays in review — **the rule contains the error** — but a lazy triager accepting
   top-of-list would mis-route her. Simulating the bulk rule on current code: it would fire on ~4/10
   (Laena, Maegor, Gaemon, Rhaenys), all four correct. Conservative and safe.
4. **Candidate-recall gap (HIGH): the review row for `Septon Eustace` omits the correct node.** The
   graph HAS Septon Eustace — `eustace-dance-of-the-dragons` ("sworn to Faith of the Seven; Septon",
   the F&B chronicler) — but the row's five candidates are eustace-braavos/brune/hightower/hunter/
   osgrey. A reviewer (agent or Matt) cannot pick the right answer from that list; the likely triage
   outcome is a duplicate CREATE for one of the two in-universe *sources* this whole Track leans on.
   `Septon Barth` is fine (`barth` is listed first).
5. **Review sample (>10 examined): no case was confidently resolvable that the router got wrong**, but
   over-deferral is heavy — see §B7.

## B. Everything else

6. **Extraction fidelity/coverage — STRONG (prompt ships as-is).** All load-bearing content present:
   the 92 AC crack in the succession, Rhaenys passed over + her protest quote, Alysanne's dissent +
   Second Quarrel, the 98 tourney, Baelon's death, Vaegon and the Great Council (fourteen claims, the
   Saera bastards, Viserys-vs-Laenor primogeniture-vs-proximity), Corlys's nine voyages/High
   Tide/Hull/Spicetown, Viserys's accession, Otto/Alicent, Daemon's whole arc (Dark Sister, Rhea,
   City Watch/gold cloaks, Mysaria, coveting Dragonstone), and the Eustace/Mushroom source preamble
   (both rostered with prose). Spot-checked ~20 factual claims against the source — **zero
   hallucinations, zero cross-part leakage**. OCR garbles handled per rule (`"| have my own kingdom
   here"` kept verbatim; canonical spellings confined to the roster note column). Only nit: Baelon
   `SPOUSE_OF (widowed)` Alyssa — her death is series knowledge, not in this text (edge held in
   review anyway, since Baelon is cluster-routed).
7. **Over-deferral quantified (cost, not a blocker): 57/85 review rows (67%) have an exact-1.0
   top candidate with clear margin** (all 7 houses, ~40 locations, Iron Throne, Dark Sister, the
   Testimony, Red Keep…). Root cause: the resolver only returns clean-hit status for unique matches
   (`hit`/`hit-character`); any name with fuzzy neighbors comes back `candidates` and rule 1 never
   fires — in bulk, auto-accept (which only covers bucket-2 clusters) won't drain this either, so
   ~60% of every unit's roster would hit review triage. Fix: accept exact-normalized-name 1.0 single-
   top with margin **AND type agreement** — the Merling King/Cod Queen rows above are the proof the
   type gate is mandatory, not optional.
8. **Shipped review artifacts are STALE vs the current script (verify-provenance rule).** Outputs are
   14:41; `fab-reconcile-candidates.py` is 14:47. Re-running `score_candidates` on Aemon with current
   code yields `disambiguator~parent:jaehaerys` (the S199 parent-recall fix) where the shipped row
   says `disambiguator~prince` — the on-disk rows predate the recall fix. Routing decisions
   (matched/review/created) are unaffected (auto-accept disabled), but **do not tune thresholds on
   these rows; regenerate first.**
9. **Quote repair — SOUND, 31/31.** Programmatically verified every row of `quotes-repaired.jsonl`:
   the canonical (stripped) form is a verbatim substring of the norm()-collapsed source AND the raw
   form is absent — i.e., every repair was both necessary and correct. Sampled 9 for meaning
   (Dragonpit, "heir", birthright, "co-champion", "claim descent from", Barth "in his [sleep]",
   Saera's kingdom, wasting illness, rightful heir): all clip at phrase boundaries; none inverts or
   shades meaning (worst is the dangling "could claim descent from." — ugly, harmless as an anchor).
   The 1 quarantine (`whom he called "my bronze bitch".`) is CORRECT strictness: the source has the
   comma *inside* the quotes ("my bronze bitch,") so even the stripped form isn't verbatim — the
   repairer refused to loosen the matcher, exactly as designed. The `’'` doubled-apostrophe collapse
   is what lets the Mushroom-chronicle quote (`Mushroom’'s`) locate. 63.7%→98.9% on the same unit is
   real, not laundering.
10. **CREATE batch (4) — form/type OK-ish, all genuinely absent by name.** `nghai` (no node, only
    prose mentions elsewhere), `baelon-avenges-aemon-on-tarth`, `summoning-of-vaegon` (no vaegon/
    avenge/tarth events exist), `great-tourney-of-the-fiftieth-year` — checked the near-names:
    `anniversary-tourney` is Aerys II's 272 AC tourney, `tourney-at-kings-landing-on-the-anniversary-
    of-the-kings-coronation` is Jaehaerys's *tenth* (58 AC); only `tourney-grounds-kings-landing`
    *mentions* the 98 AC event in prose — no name collision. Composite/dedup guards worked: "Wedding
    of Daemon and Rhea Royce" → `composite-name` review, all Death-of-X events → `event-dedup-risk`
    review, `Myrmen` → `bare-first-name-miss`. Defects: (a) **non-canonical types pass through
    unvalidated** — `event.tourney` (canonical is `event.tournament`, 34 live nodes) and bare `place`
    (canonical `place.location`); (b) **era stamp is wrong on two**: `dance-of-dragons` on 92 AC and
    98 AC events (the §5.5 section→era map stamps the *section's* era, not the event's — these are
    Jaehaerys's reign); (c) node **bodies are outcome fragments** ("Myrmen driven into the sea",
    "disputed: throne offered and refused…" duplicated as both Identity and F&B section, no quote/
    cite in body). `occurred:` blocks are right, incl. tier-2 on the disputed summoning.
11. **merge-plan quality (read all 16; cites spot-checked 12, incl. the required 5): prose accurate
    and durable** — phrased as node facts ("Eldest son of Baelon and Alyssa, chosen heir by the Great
    Council…"), not chapter narration; nothing editorializes. Cite lines verify: 15:17, :21, :45,
    :47, :49, :79, :103, :145, :155, :157, :161, :171, :175, :177, :181, :185, :191 all contain the
    claimed text. **But:** (a) **the cite unit id drops `-p01`** — spec locks `(fab-<unit>:LINE)` and
    the source on disk is three part-files; `fab-heirs-of-the-dragon-15:17` is ambiguous across
    p01/p02/p03 (line 17 exists in each) — non-navigable provenance, which is the whole point of the
    overlay; (b) two join-window cites land on the blank line one before the quote (`:86` → text at
    87; `:202` → text at 203) — the window scan returns the first index whose join contains the
    quote, including a leading blank line; (c) the Jaehaerys entry has a malformed orphan bullet
    (`- . He and Queen Alysanne…`) from quote-anchor splitting; (d) the Daemon entry carries
    `(fab-quote-unlocated)` for the quarantined quote — acceptable as a quarantine surface, but merge
    must refuse to write a bullet with a dead cite.
12. **Disputed tagging — correct for THIS part, and honestly: p01 is not yet the dispute stress
    test.** The only genuine dispute in p01 is what passed between Jaehaerys and Vaegon ("Some say…
    offered the throne… Others assert…") — tagged on both role edges (`unattributed`, `disputed:
    true`, tier-2) and carried into Vaegon's node prose with both variants. Swept the remaining
    hedges: "twenty to one" ("it was said afterward") wasn't extracted as a claim; "if their family
    histories can be believed" and the Merling-King legend are roster/prose-level and handled;
    everything else Gyldayn asserts flat. **No Mushroom/Eustace-attributed claims exist in p01** —
    the digression introducing them ENDS this part; the he-said/she-said density this stage was
    picked for lives in p02/p03. 0.065 is calibrated, not under-tagged — but the
    attribution machinery (`in_universe_source: septon-eustace/mushroom`) remains effectively
    unexercised until a p02/p03 unit runs. Nit: the `disputed` flag on the summoning edges slightly
    over-taints — the *summons* is undisputed fact; only the offer is disputed.
13. **UPDATE/CREATE mix 41/85/4 — reasonable for this unit.** 36% matched is right for a text whose
    principals are mostly pre-existing wiki nodes; 4 CREATEs on a dense 113-roster is believable
    (this era is wiki-saturated). The 85 review is inflated by §B7, not by genuine ambiguity (~10
    cluster rows + ~8 event-dedup + oddballs is the true ambiguity load). One observability gap: the
    matched-41's name→slug assignments are persisted **nowhere** (not in candidates.json unless
    edge-bearing, not in the review file) — that's exactly how Lorath→jaqen hid. Emit a
    `matched.jsonl` sidecar.

---

## Ranked fixes

1. **BLOCKER — type-blind clean-hit routing (R1 class).** `Lorath` (place) matched `jaqen-hghar`
   (character) at 1.0 via a junk alias and counted as a matched UPDATE. Fix in
   `fab-reconcile-candidates.py::Router.route`: rule-1 UPDATE requires roster `Type guess` ↔ node
   category agreement (person↔characters, place↔locations, house↔houses, event↔events, ship/sword↔
   artifacts…); mismatch → review. Separately: strip the `"Lorath"` alias off `jaqen-hghar` (alias
   hygiene — `project_node_alias_spaced_phrases` class) — but the guard, not the alias fix, is the
   real defense.
2. **BLOCKER (bulk, multi-part sections) — `run_id` drops the part suffix.** `base_slug_from_unit`
   + `run_id = fab-<slug>-NN-<date>` (reconciler line ~848, and the same format is locked in
   build-spec-s198.md) gives p01/p02/p03 identical run_ids on a same-day run; `fab_merge_node.py`'s
   `skipped_marker` idempotency then silently drops p02/p03 prose on every node shared across parts —
   the exact R3 silent-drop failure the design outlaws. Fix: `run_id = fab-<unit>-<date>` (keep
   `-pMM`); update spec + marker docs. Harmless for single-part sections.
3. **HIGH — cite unit id must carry the part.** Merge-plan cites read `(fab-heirs-of-the-dragon-15:LINE)`
   but line numbers are per part-file; emit `(fab-heirs-of-the-dragon-15-p01:LINE)` per the spec's
   `(fab-<unit>:LINE)`. Without this the Tier-1 overlay's cites don't open.
4. **HIGH — review candidate recall.** `Septon Eustace`'s row omits `eustace-dance-of-the-dragons`
   (the actual Septon Eustace). Augment review-row candidates with (a) candidate-pack members whose
   name shares the roster row's first/last name and (b) a first-name index probe, so the right answer
   is always *presentable* at triage. (Also add `septon eustace` aliases to that node at triage time.)
5. **HIGH (cost) — drain the exact-1.0 review flood before bulk.** 57/85 rows are exact-name 1.0
   clear-margin. Extend rule 1: `candidates` status with a single exact-normalized-name 1.0 top,
   margin ≥0.2 to #2, AND the type-agreement gate from fix 1 → UPDATE. The Merling King and Cod
   Queen rows are the regression tests (both 1.0-top and both must STILL route to review on type
   mismatch).
6. **MEDIUM — regenerate the smoke artifacts with the current script before threshold tuning.**
   Shipped `reconcile-review.jsonl` (14:41) predates the parent-recall fix (14:47); scored-candidate
   hits differ on re-run (verified on Aemon). Cheap: re-run the reconciler on both smoke units.
7. **MEDIUM — validate CREATE `type` against the canonical vocab + fix era-by-year.**
   Map/reject `event.tourney`→`event.tournament`, bare `place`→`place.location`; for `event.*`
   CREATEs with `ac_year`, derive `era` from year ranges (92/98 AC ≠ `dance-of-dragons`) instead of
   the section map.
8. **MEDIUM — merge-plan prose hygiene.** Drop empty/orphan bullets (`- . He and…`), refuse to write
   bullets citing `(fab-quote-unlocated)` (hold them with the quarantine), and make the join-window
   locator return the first *non-blank* line of the match (`:86`→87, `:202`→203). Emit a
   `matched.jsonl` (name→slug for all matched roster rows) for auditability.
9. **NICE — modeling nits.** `VICTIM_IN` on Jaehaerys for a marital estrangement (mechanical
   patient-mapping; consider `AGENT_IN` both or a softer role); `disputed` on the summoning role
   edges taints the undisputed summons; `SIBLING_OF (full)` for Otto/Lord Hightower and Baelon
   `SPOUSE_OF (widowed)` Alyssa are series-knowledge inferences beyond this text (both currently
   harmless — review-held or conventional).

## Does anything corrupt the graph if applied as-is?
**This unit's sidecars: no.** Every write-bearing routing (16 merge-plan slugs, 31 edges, 4 CREATEs)
was verified correct; the Lorath wrong-match produces zero writes here, and the run_id collision only
bites when a second part of the same section runs the same day. But both are certainties at bulk
scale — fix 1 and 2 before any apply, re-run the reconciler (fix 6 falls out for free), and validate
the fix-5 threshold change on ≥2 fresh units per §7. The extractor prompt needs no changes. The
dispute-attribution machinery should get one p02/p03 unit smoked before bulk, since p01 never
exercises `in_universe_source: mushroom/septon-eustace`.
