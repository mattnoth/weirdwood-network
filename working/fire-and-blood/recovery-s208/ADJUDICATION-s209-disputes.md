# S209 — Dispute-held recovery rows: adjudication + landing record

**Session 209 · 2026-07-11 · closes the LAST review-bucket step.**

Drained the **76 dispute-held rows** that the S208 review-bucket recovery quarantined
under the reconciler's §7.2 hedge-proximity guard (`out/*/dispute-review.jsonl`). Pipeline:
`fab-dispute-preclassify` → primary-text adjudication of the residue → `fab-dispute-inject`
→ per-unit `mint_enrichment` (fresh run_ids) + a consolidated dispute-only `fab_merge_node`.

## Disposition of all 76 rows

| kind | count | disposition |
|------|-------|-------------|
| edge | 47 | 44 **landed** (22 AUTO_CLEAR + 20 verdict-clear + 2 excluded-unit AUTO_CLEAR) · **3 DROP** (primary-text-anchored) |
| prose | 24 | 24 **landed** (23 AUTO_CLEAR + 1 AUTO_DISPUTED + 2 of those from excluded units) on 11 nodes |
| event | 5 | **deferred** (never minted here — event-kind rows are out of scope for dispute-inject by policy; logged to `out/*/dispute-events-deferred.jsonl`) |
| **total** | **76** | 68 landed · 3 dropped · 5 event-deferred |

Preclassifier auto-resolved 49/72 of the non-excluded rows (68%); 23 NEEDS_READ edges went to
primary-text adjudication. Every hedge_term on these rows was a **chronicler-name
paragraph-proximity false-positive** (mushroom / eustace / avers / "can be believed") — none
was a genuine in-universe dispute, so no NEEDS_READ row needed a tier-2 `disputed` tag.

## The 3 DROPs (each anchored to the chapter text)

1. **`CAPTURES Corlys Velaryon → Alicent`** (`fab-hour-of-the-wolf-20:195`). Quote ties the
   seizure of the Queen Dowager to men who "had worn the seahorse badge of House Velaryon."
   At the Judgment of the Wolf these captors are tried as individual opportunists
   ("gutter knights… granted knighthood by Ser Perkin"), condemned/spared on their own —
   the text gives Corlys **no agency** in ordering the capture. Over-attribution of house-badge
   → house-lord. Dropped.
2. **`RULES Tyland Lannister → Seven Kingdoms`** (`fab-the-hooded-hand-21:87`). Quote:
   the Hand "gathered more and more power to himself" while the council of regents "convened
   less and less often." That is informal power-accretion by the **Hand under a regency**, not
   sovereignty over the realm. `RULES <realm>` is a monarch relation; Tyland is not king. Dropped
   (his Hand office is already modeled elsewhere).
3. **`SAME_AS Nettles → Netty`** (`fab-the-red-dragon-and-the-gold-17-p04:37`). "Netty" is a
   diminutive of Nettles used for the same girl in the same passage — not a separate identity.
   Per the project's alias-not-`SAME_AS` convention (Reek/Alayne handling), a nickname belongs in
   the node's `aliases:` frontmatter, **not** a cross-identity edge. Dropped; **"Netty" logged as
   an alias candidate for `nettles`** (harvest-queue pointer, below).

## The 20 CONFIRMs (flat F&B canon, tier-1 clear)

All 20 verified against the chapter text; the chronicler hedge was proximity noise. Highlights:
`BETROTHED_TO aegon-iii→jaehaera`, `RULES cregan-stark→winterfell` (×2 units, two quotes),
`IMPRISONS cregan→corlys` ("dragged him to the dungeons"), `APPOINTS aegon-iii→corlys`
(restored to the small council), `RESCUES perkin-the-flea→corlys` (freed the dungeon prisoners),
`BETRAYS house-mooton→rhaenyra` (Maidenpool defected — corroborated by the attainder decree, so
flat not disputed), `ADVISES corlys→aegon-ii` (counseled a general pardon), `ALLIES_WITH
corlys→rhaenyra`, `CONSPIRES_WITH blood→cheese`, `EXECUTES lady-caswell→sly`,
`PROTECTS corlys→{addam,nettles}` (spoke in defense of the dragonseeds),
`APPOINTS/DEPOSES unwin-peake→{bernard,eustace}`, `MEMBER_OF mervyn-flowers→kingsguard`,
`WARD_OF rhaena→lady-arryn`, `ADVISES rhaena→aegon-iii`, `SWORN_TO lyonel-hightower→tyrell`.

Full machine-readable verdicts: `verdicts-s209-disputes.jsonl` (23 rows: 20 clear / 3 drop).

## Landing mechanics (why this was a re-merge, not a fresh apply)

The S208 recovery had already minted + merged each unit's **non-dispute** rows. So this drain
re-touched already-applied units — handled to avoid both silent-skip and double-apply:

- **Edges** — bumped each unit's `candidates._meta.run_id` to `…-recovery-disputes-s209` (fresh,
  passes mint's re-run guard); mint's edge-level same-quote dedup then **skipped every
  S208-landed edge** and appended only the 44 new `DISP*` edges. Verified: `edges.jsonl` +44 / −0.
- **Prose** — a fab_merge_node re-run under the *old* run_id would have hit `skipped_marker`
  (dropping the new bullets); under a fresh run_id on the *augmented* merge-plan it would have
  **duplicated** the S208 bullets. Fix: built a **dispute-only** merge-plan by diffing each
  unit's post-inject merge-plan against a pre-inject snapshot, **consolidated to one entry per
  slug** (11 slugs / 24 bullets, run_id `fab-recovery-disputes-s209`), so fab_merge_node
  `section_extended` each node with a single new block. Zero duplicate bullets (verified).
  Record: `dispute-merge-plan-s209.json`.
- **Excluded-units caveat** — `fab-heirs-of-the-dragon-15-p01`/`-p02` (4 rows) collide **by name**
  with the S200-smoke `EXCLUDED_UNITS` guard baked into both scripts. That guard protects the
  *standard* `apply/` dir's historical S200 data; here in `recovery-s208/out/` these same-named
  dirs hold **fresh, unlanded** S208 recovery rows. Ran preclassify+inject on just those two
  units with the guard patched off (`scratchpad/run_excluded.py` — reuses 100% of the real
  deterministic logic; `chapter=unit` provenance preserved). All 4 were flat AUTO_CLEAR.

## Gates (all green)

- `fab-semantic-gate` → **OVERALL PASS, 4/4** (victim_in_harm / junk_nodes / orphan_edges /
  duplicate_edges). No new VICTIM_IN, no disputed edges (all 44 are tier-1), so the harm-gate and
  disputed-invariant were trivially clean.
- `pytest` → **1457 passed**, 1 skipped. `deno task test` (web/) → **100 passed**, 1 ignored.
- **No `weirwood refresh`** — prose-append changes node bodies only (no new slugs/aliases/nodes),
  so `graph/index/` stays valid (S205 quote-only precedent). Deploy of the enlarged bundle is
  Matt-gated as always.

## Totals

`edges.jsonl` **26,308 → 26,352** (+44). 11 character nodes gained a dispute FAB block (+24
bullets). Event nodes unchanged (1,242). 5 events deferred; 3 edges dropped with logged reason.

## Harvest-queue pointer

- `nettles` — add **"Netty"** as an `aliases:` entry (diminutive used at
  `fab-the-red-dragon-and-the-gold-17-p04:37`); the dropped `SAME_AS` was the wrong mechanism.
