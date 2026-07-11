# Edge-vocab retrofit Part B — S211 adjudication record

**Machine:** deterministic prep (`scan-candidates.py`: 41 knighting + 75 suspicion passage
packets, `_conflicts/` + `meta.chapter` filtered, existing-pair exclusion sets baked in)
→ 3 Sonnet proposers (SHARED-RULES.md; every candidate book-quote-grounded) → 3 Haiku
adversarial fresh-verifiers (VERIFY-RULES.md) → orchestrator adjudication (this file)
→ `assemble-final.py` → `quotecheck` 30/30 ALL FOUND → mint DRY-RUN on scratch copies
(30 appended / 0 dup / 0 nodes). **Apply gated on Matt.**

## Verdict totals
- knighting: 10 proposed → 10 CONFIRM → **10 accepted** (all tier-1)
- suspicion-a: 12 proposed → 10 CONFIRM / 2 AMBIGUOUS → **10 accepted / 2 dropped**
- suspicion-b: 12 proposed → 11 CONFIRM / 1 PROBLEM → **8 accepted / 3 dropped / 1 retyped**
- orchestrator additions: **+1** (Corlys)
- **Final: 30 edges** — 18 SUSPECTED_OF (tier-2) · 10 KNIGHTED_BY (tier-1) · 1 AGENT_IN ·
  1 COMMANDS_IN. Zero new nodes. Zero live-graph triple clashes, zero intra-batch dups.

## Orchestrator decisions (all primary-text- or precedent-anchored)

1. **DROP a-S4/a-S5** (`karyl-vance`/`clement-piper SUSPECTED_OF blackfish-escapes-riverrun`)
   — re-proposals of S159 fresh-verify REJECTS E14/E15 ("diffuse class distrust, not pointed
   suspicion; Edmure confessed HE arranged it" — `working/enrichment/jaime-riverlands/
   fresh-verify.md:25`). Residue: the live node's Edges-narrative prose still documents this
   pair as SUSPECTED_OF (stale vs the drop) → prose-cleanup todo.
2. **DROP b-S2** (`petyr-baelish SUSPECTED_OF murder-of-jon-arryn`) — S148 deliberately
   retired this exact edge and upgraded Petyr to COMMANDS_IN (Lysa's confession proves
   instigation). Haiku verifier independently flagged PROBLEM `proven-not-suspected`.
   Residue: the node's Identity prose still says "SUSPECTED_OF as instigator" → same
   prose-cleanup todo.
3. **DROP b-S10/b-S11** — exact duplicates of a-S10/a-S11 (both proposers found the
   Helaena murder-rumor from adjacent packets).
4. **ACCEPT a-S10/a-S11** (Haiku AMBIGUOUS: rumor explicitly debunked with alibi) —
   disproven-but-load-bearing in-world suspicion is established SUSPECTED_OF territory
   (precedents: `brienne SUSPECTED_OF shadow-assassination-of-renly`, `tyrion/sansa
   SUSPECTED_OF death-of-joffrey`); this rumor ignites the KL riot, textbook load-bearing.
   Same reasoning covers b-S6 (Sandor/Saltpans) and b-S12 (Marillion frame-up).
5. **RETYPE b-S5** `tyrion SUSPECTED_OF plot-to-free-jaime-lannister` → **COMMANDS_IN
   tier-1**: Catelyn's suspicion is proven in Tyrion's own POV — the four-false-guardsmen
   scheme is his ("part of my scheme to free Jaime", acok-tyrion-06:217). S148 pattern.
   The event node previously had ZERO edges in edges.jsonl.
6. **ADD R30** `corlys-velaryon AGENT_IN death-of-aegon-ii` tier-1 — adjudicating the
   a-flag against `fab-hour-of-the-wolf-20`: Corlys "did not attempt to deny his guilt"
   + declared guilty of murder/regicide/high treason ⇒ proven complicity ⇒ role edge, NOT
   SUSPECTED_OF. **Larys Strong's existing tier-2 SUSPECTED_OF stands** per S202 ("the
   hand will never be known") + S203 — he never confirmed; not re-litigated.
7. **Withheld (proposer-honest, endorsed):** Bronn's mass-knighting (3 possible dubbers,
   none singled out); the possibly-fabricated "Ser Robert" (Osmund Kettleblack's story);
   Rhaegar/"shadow host" wiki-only (superseded anyway — b-S9 grounds the same suspicion
   in adwd-the-kingbreaker-01); house-level "the Hightowers" rumor on Septon Moon (no
   named suspect); Robb-warg Red Wedding tale (propaganda, not whodunit); Tessario
   third-order "fancy"; Unwin-Peake near-dups on lysene-spring/secret-siege (S3 targets
   the-treason-trials as the single canonical hub).

## Wiki-only holdouts (NOT minting; parked for a possible wiki-evidence slice)
- `aerys-ii KNIGHTED_BY tywin` (TWOIAF-only), `daemon-sand KNIGHTED_BY oberyn` (dubbing
  never on-page), `jorah KNIGHTED_BY robert` (book has "For that I won my knighthood",
  acok-daenerys-01:151, but never names Robert as dubber — verified this session).

## Residue / follow-ups (→ todos at endsession)
- Prose-staleness cleanup: `blackfish-escapes-riverrun` (S159-dropped pair still narrated
  as SUSPECTED_OF) + `murder-of-jon-arryn` Identity ("Petyr SUSPECTED_OF" vs actual
  COMMANDS_IN edge).
- a-flag: `death-of-queen-ceryse` carries `AGENT_IN maegor` while node prose says
  "rumored murder" — confidence mismatch worth a look.
- b-flag: no event node for Tyrek Lannister's disappearance (a varys SUSPECTED_OF
  candidate exists in text once minted).
- Roles follow-on slice: 313 event nodes have zero role edges (this session's scan);
  a ranked subset is the natural Part B continuation.
- Gormon Peake (R27) accepted as SUSPECTED_OF on the egg-planting accusation quote;
  his (arguably proven) instigator role in the wider rebellion has no AGENT_IN — a
  D&E-familiar future dip could upgrade with a proving quote.
