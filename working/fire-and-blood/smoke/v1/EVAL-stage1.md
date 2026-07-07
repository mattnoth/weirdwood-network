# Stage-1 Smoke Eval — `fab-aegons-conquest-03` (fresh adversarial review)

**Verdict: PASS-WITH-CONCERNS** — the *extraction* half is strong; the *reconciler* half has a
CREATE-routing bug class that WOULD corrupt the graph if applied as-is. Nothing corrupts the graph in
its current dry-run state (nothing minted), and no fix touches the prompt — all blockers live in
`fab-reconcile-candidates.py`. Do not proceed to apply until the CREATE guard is fixed and re-run;
Stage 2 (quality) can proceed in parallel.

## Metric read
148 rostered → 39 matched / 108 review / **36 created**. disputed_rate 0.034. Quotes 135, 89.6% located,
14 quarantined. The headline numbers are plausible for a flat-narration section, BUT the 36 CREATEs are the
tell: ~19 of 36 are **wrong** (dupes / bogus entities), not new nodes. The "89.6% located" 14-quote miss is
**100% line-wrap false-negatives, 0% fabrication** — a reconciler locator gap, and actually a *good* signal
for the extractor.

---

## A. Extraction quality — STRONG (ship the prompt as-is)

1. **Roster (148): reasonable, not padded.** Every named entity in a dense conquest narrative is present;
   houses/places/objects correctly typed. **Disambiguator column is filled and genuinely useful** on every
   same-name-prone entity: `Aegon I Targaryen` vs `Aegon Targaryen (son of Gaemon)` vs the Conqueror's
   forebear chain (Aerys/Baelon/Aerion each carry "disambiguate from later King/Aerion" notes). OCR garbles
   flagged in the note column (`King Aegon | Targaryen`, `Loren | Lannister`) — exactly per rule. No dupes,
   no obvious misses.
2. **Node prose (sampled Aegon I, Visenya, Rhaenys, Orys, Harren, Torrhen, Meria, Loren): factual,
   book-grounded, budget-respecting.** Principals get 3–5 sentences; minors (Garse VII) get one line; pure
   mentions get roster-only. Disputed claims correctly carry inline attribution ("Some said…", "it was
   whispered"). No banned editorial words (`symbolic`/`ironic`/`foreshadows`), no invented facts, no
   cross-unit leakage. Prose quote anchors are verbatim.
3. **Edges (sampled ~12): clean.** LOCKED vocab only; direction correct (Column A = semantic agent, e.g.
   `Argilac KILLS(in_combat) Garse VII`, passive "slain by" resolved to agent; `Orys KILLS(in_duel)
   Argilac`; `Rhaenys KILLS(by_creature) Dickon Morrigen`). Required qualifiers present (`SPOUSE_OF(current)`,
   `SIBLING_OF(full/half)`, `SWORN_TO(current/former)`). No `KNOWS`, no FORESHADOWS/analytical types, no
   reverse/mirror rows. Minor nit: `Aegon KILLS(by_creature) Harren` and `event.battle Burning of Harrenhal`
   double-encode the same act — intended per §5.4 duplicate-with-better-evidence, fine.
4. **Dispute tagging (0.034): correctly calibrated for this section.** Only 2 disputed edges — Orys's
   whispered half-brother status and the Hightower-daughter offer — both real hedges ("it was whispered",
   "Some say"), both correctly `unattributed` + `disputed:true` + tier-2. Spot-checked the obvious hedge
   passages ("It was said by some that Aegon wed Visenya out of duty…", "accounts differ" re: Lannisport,
   "Some say three thousand; others…") — the flat-narration ones the extractor left untagged are defensible
   (Gyldayn confirms them as fact); it did NOT miss a load-bearing dispute. Low rate is right here; the real
   dispute stress-test is Stage 2 (Heirs of the Dragon).
5. **OCR: quotes verbatim, garbles intact.** Confirmed `"| built in stone,"`, `"Mother, can | go flying
   with the lady?"`, `"nor will | kneel to you"` copied byte-for-byte with the `|`-for-`I` garble; canonical
   spellings confined to the roster note column. Rule followed exactly.

## B. Reconciler mechanics — the problem area

6. **36 CREATEs: ~19 are duplicate-mints or bogus — highest-risk failure, CONFIRMED.**
   - **9 house dupes:** `blackwoods`, `mallisters`, `vances`, `brackens`, `pipers`, `strongs`, `mudds`,
     `fishers`, `hooks` — every one already exists as `house-blackwood` / `house-mallister` / … in
     `graph/nodes/houses/`. The extractor emitted plural bare surnames ("Blackwoods"); the resolver MISSes
     (no alias) and the reconciler CREATEd instead of routing to review.
   - **2 missed-match mints:** `daenys` (exists as `daenys-targaryen`) and `arrec` (exists as
     `arrec-durrandon`). These are the *worst* class — the resolver returned `CANDIDATES` (fuzzy, multiple),
     which per design §5.1 rule 3 is **not** "confidently empty" and must route to review, yet they were
     minted. `contradictions-report.md` even shows the collision (`aenar PARENT_OF daenys` vs wiki
     `aenar PARENT_OF daenys-targaryen`) — proof the dupe fractures an existing edge.
   - **4 composite-name mints:** `mern-ix-gardener-loren-i-lannister`, `lord-darklyn-lord-mooton`,
     `sharra-arryn-ronnel-arryn`, `visenya-targaryen-rhaenys-targaryen` — these are **two entities joined by
     `;` in an Events-table agent/patient cell**, minted as one garbage node.
   - **3 abstract/collective mints:** `the-targaryen-fleet`, `the-targaryen-host-at-storms-end`,
     `aegons-host-at-the-field-of-fire`, all typed `character.human` — not entities at all; leaked from edge
     `COMMANDS` targets / event roles.
   - The **10 event.* CREATEs are legit** (battles/surrenders/coronations genuinely new). Individual-lord
     CREATEs (`lord-darklyn`, `lord-errol`, `lord-oakheart`, `lord-bar-emmon`) look plausibly new (not found
     in graph), acceptable pending duplicate-detector.
7. **39 matched + 108 review split: sane; NO trap node accepted.** The 14 UPDATE targets in `merge-plan.json`
   are all correct principals (`aegon-i-targaryen`, `orys-baratheon`, `harren-hoare`, …). **The R1 trap held:**
   bare `aegon-targaryen` (the disambiguation-page node) appears as an edge endpoint **zero** times — every
   Conqueror edge resolved to `aegon-i-targaryen`. The 108 review pile is 95 `unresolved:candidates` +
   13 `smoke-auto-accept-disabled`; skimming it, most are clean names that would auto-accept in bulk (good),
   but the house-plural and short-name cases sitting in *both* review and CREATE reveal the routing bug —
   the reconciler is CREATE-ing entities that also have live fuzzy candidates.
8. **14 quarantined quotes: 100% OCR/line-wrap, 0% fabrication — GOOD signal.** Every one recovers under a
   full whitespace-collapse of the source (e.g. "…Warden of the South and Lord ⏎⏎ Paramount of the Mander",
   "the boy king of the Eyrie, Ronnel ⏎⏎ Arryn"). The extractor quoted verbatim; the reconciler's locator
   only joins **2 adjacent physical lines** and fails when a quote straddles a **blank-line paragraph gap**.
   No invented quotes anywhere.

---

## Ranked issues (all in `fab-reconcile-candidates.py`; prompt is fine)

1. **CREATE guard too weak → duplicate-mint (BLOCKER).** `CANDIDATES`/fuzzy-hit names (`daenys`, `arrec`)
   and MISS-but-obviously-a-known-house names (`blackwoods`→`house-blackwood`) are being minted.
   *Fix:* (a) never CREATE when the resolver returned any fuzzy candidate — route to review (design §5.1 rule
   3 already says this; enforce it); (b) add a de-pluralize + "House X" alias probe (surname → `house-<sing>`)
   before deciding new; (c) require the duplicate-detector to run on the CREATE batch (design §5.1) — it isn't
   gating here.
2. **Composite/collective cells minted as nodes (BLOCKER).** Split Events-table `agent`/`patient` on `;` into
   individual entities before resolution; drop/《don't-mint》 collective military referents ("the Targaryen
   fleet", "Aegon's host at …") — they are not graph entities. 7 of 36 CREATEs are this class.
3. **Quote locator misses paragraph-spanning quotes (HIGH, cheap).** All 14 quarantines are line-wrap false
   negatives. *Fix:* run the `norm()`+grep against a whitespace-collapsed (or ≥N-line-joined) view of the unit
   file, not just single-line + two-line-join. This alone lifts located% from 89.6 → ~100 and shrinks the
   review/quarantine load before any LLM re-touch.
4. **`contradictions-report.md` is polluted by the dupe bug (MEDIUM).** Its `aenar→daenys` vs
   `aenar→daenys-targaryen` and `valaena→aegon-i-targaryen` vs `valaena→rhaenys/visenya` rows are
   slug-mismatch/expected-multi-child noise, not real F&B-vs-wiki conflicts. Once issue 1 is fixed, re-diff on
   canonical slugs so the report surfaces *genuine* contradictions only.
5. **New-node `type` defaulting to `character.human` (MEDIUM).** The composite and collective mints are all
   stamped `character.human`; the reconciler should carry the extractor's `Type guess` through and refuse to
   mint places/objects/collectives as people.

## Does anything corrupt the graph if applied as-is?
**Yes — issues 1 and 2.** Applying this `candidates.json` + `created-nodes.jsonl` would mint ~9 duplicate house
nodes, 2 dupes of existing characters (fracturing live kinship edges per the contradictions report), and 7
junk nodes — permanent graph pollution requiring cleanup. But this is a **dry run; nothing is minted**, and
every blocker is a deterministic reconciler fix with no bearing on the extractor or the prompt. Fix the CREATE
guard + composite-split + wrap-aware locator, re-run the reconciler on this same unit (expect CREATEs to drop
from 36 to ~14, quarantine to ~0), then gate to apply.
