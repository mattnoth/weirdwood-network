# S151 Gravedigger Evidence Layer — Proposal

**Unit:** B3 Sandor's "death" / the Quiet Isle gravedigger (sub-plot of Brienne→Stoneheart arc)
**Session:** S151
**Proposer:** research+propose lens (NOT minted — awaiting synthesis + fresh-verify gate)
**Sources read:** `sources/chapters/affc/affc-brienne-06.md`, `affc-brienne-07.md`

---

## Edges proposed

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter:line | verbatim_quote | note (dedup / rationale) |
|----|-------------|-----------|-------------|------|------|--------------|----------------|--------------------------|
| E1 | stranger-horse | LOCATED_AT | quiet-isle | T1 | affc | affc-brienne-06:191 | "You may have seen a big black stallion in our stables. That was his warhorse, Stranger." | quiet-isle OWNS stranger-horse exists (wiki-sourced, T2); this adds a T1 book-cited LOCATED_AT from the horse's perspective. Not a dup — different edge type + direction. |
| E2 | elder-brother-quiet-isle | HEALS | sandor-clegane | T1 | affc | affc-brienne-06:191 | "I bathed his fevered brow with river water, and gave him wine to drink and a poultice for his wound" | DEDUP WARNING: `elder-brother HEALS sandor-clegane` already exists — BUT that edge is on the TITLE node (`elder-brother`), not the PERSON node (`elder-brother-quiet-isle`). The title node is the wrong subject for this action. PROPOSE the corrected edge on the person node; flag the misfire on the title node for the verify gate. Quote is T1; ref is affc-brienne-06:191. |
| E3 | elder-brother-quiet-isle | TENDS | sandor-clegane | T1 | affc | affc-brienne-06:191 | "I bathed his fevered brow with river water, and gave him wine to drink and a poultice for his wound, but my efforts were too little and too late." | TENDS (healer→patient, care without cure) distinguishes from HEALS (which implies some success). The Elder Brother's account is explicit that his tending failed — "too little and too late." Check edge-type-counts.md: if TENDS is not in the 170, use HEALS for both; flag below. |
| E4 | gravedigger | LOCATED_AT | quiet-isle | T1 | affc | affc-brienne-06:79 | "higher still they passed a lichyard where a brother bigger than Brienne was struggling to dig a grave" | `gravedigger SWORN_TO quiet-isle` already exists (wiki). This adds a T1 book-cited LOCATED_AT: the gravedigger is physically on the isle and observed there. Not a dup. |
| E5 | gravedigger | PERCEIVED_AS | big-lame-novice | T1 | affc | affc-brienne-06:79, 143 | "a brother bigger than Brienne was struggling to dig a grave. From the way he moved, it was plain to see that he was lame" / "the big gravedigger they had encountered on the hill, who walked with the awkward lurching gait of one half-crippled" | **NEW NODE required** — see New nodes section. This models Brienne's on-page perception without asserting identity. |
| E6 | brienne-tarth | ENCOUNTERS | gravedigger | T1 | affc | affc-brienne-06:79 | "higher still they passed a lichyard where a brother bigger than Brienne was struggling to dig a grave" | Brienne directly observes the gravedigger twice (lichyard, then supper hall). ENCOUNTERS = on-page co-presence. No existing edge; not a dup. |
| E7 | elder-brother-quiet-isle | REVEALS_TO | brienne-tarth | T1 | affc | affc-brienne-06:191 | "The Hound died there, in my arms." | DEDUP CHECK: two REVEALS_TO `brienne-tarth` edges already exist on this node (lines 169 + 185 — Arya/Sansa redirect + Saltpans clarification). This is a THIRD distinct disclosure: the explicit death account + Stranger identification. Different quote + claim. Propose as new. |
| E8 | sandor-clegane | TRAVELS_TO | quiet-isle | T2 | affc | affc-brienne-06:191 | "You may have seen a big black stallion in our stables. That was his warhorse, Stranger. A blasphemous name. We prefer to call him Driftwood, as he was found beside the river." | Stranger was found beside the Trident and is now stabled on the Quiet Isle — the Elder Brother's account implies Sandor came to (or near) the isle before dying. T2 (one clean inference; no text says Sandor himself crossed to the isle, but Stranger being there + the dying-by-the-Trident account makes it near-certain he traveled in that direction). |
| E9 | gravedigger-theories | PART_OF | gravedigger | T2 | — | — | — | Wire the dead-end theories node into the evidence cluster: gravedigger-theories PART_OF gravedigger (the character node), which is the on-page subject. This gives the theory node an inbound edge into the evidence layer without asserting the identity claim. Alternatively PARALLELS might be cleaner — see note. |

**DEDUP SKIPS (already in graph, not re-proposed):**
- `elder-brother HEALS sandor-clegane` — EXISTS (but on wrong node — title not person; flagged in E2 above)
- `gravedigger SWORN_TO quiet-isle` — EXISTS
- `elder-brother-quiet-isle HOLDS_TITLE elder-brother` / `SWORN_TO quiet-isle` — EXISTS
- `sandor-clegane OWNS hound-helm` / `OWNS stranger` / `BONDED_TO stranger` — EXISTS
- `hound-helm WIELDED_IN raid-on-saltpans` — EXISTS
- `hound-helm LOOTED_BY rorge` — EXISTS
- `hound-helm LOOTED_BY lem` — EXISTS (chain is COMPLETE through lem; no new helm-chain edges needed)
- `elder-brother-quiet-isle REVEALS_TO brienne-tarth` (lines 169, 185) — EXISTS; E7 is a third distinct disclosure
- `quiet-isle OWNS stranger-horse` — EXISTS (wiki-sourced T2); E1 adds T1 book-cited LOCATED_AT

**HELM CHAIN STATUS:** Sandor→Rorge (LOOTED_BY, T1, affc-brienne-08:215) → Lem (LOOTED_BY, T1, same cite) is fully wired. No new helm-chain edges needed.

---

## New nodes proposed

### N1: `big-lame-novice` (concept or descriptor)

Actually: do NOT mint a separate node for the physical description. Instead, use `PERCEIVED_AS` with a free-text description in the `asserted_relation` field, pointing at the existing `gravedigger` node with a description qualifier. If the schema requires a target node for PERCEIVED_AS, use `gravedigger` itself as target with note = "perceived as: a big lame novice, bigger than Brienne, half-crippled gait." This avoids minting a one-use descriptor node.

**Revised E5:** `gravedigger PERCEIVED_AS gravedigger` is circular. Better: use `brienne-tarth PERCEIVED_AS gravedigger` with note "Brienne perceives him as a huge lame novice" — modeling the observer→subject perception from Brienne's POV.

**Revised E5 (final):**

| id | source_slug | EDGE_TYPE | target_slug | tier | book | chapter:line | verbatim_quote | note |
|----|-------------|-----------|-------------|------|------|--------------|----------------|------|
| E5 | brienne-tarth | PERCEIVED_AS | gravedigger | T1 | affc | affc-brienne-06:79 | "a brother bigger than Brienne was struggling to dig a grave. From the way he moved, it was plain to see that he was lame" | Observer=Brienne; subject=gravedigger. Captures on-page perception (huge, lame) without identity claim. Note in asserted_relation: "perceived as a big lame novice, half-crippled gait." |

**No new nodes minted.** The gravedigger node already exists; no hub or descriptor node is warranted.

---

## GATED-IDENTITY NOTE

The books never confirm "the gravedigger IS Sandor Clegane." The on-page evidence cluster is: (1) a dying man found by the Trident → tended → died in the Elder Brother's arms; (2) Stranger stabled on the isle; (3) a huge, lame, silent novice digging graves; (4) the Hound's helm taken from a cairn by Rorge. The Elder Brother's statement "The Hound died there, in my arms" is widely read as referring to the persona/identity ("the Hound" = the killer aspect), not the man — consistent with his philosophical framing ("Some wounds do not show"). The convergence of Stranger's presence + the giant limping mute + the buried-then-stolen helm is the strongest fandom evidence for Sandor's survival, but GRRM has not confirmed it. **Do not propose `gravedigger SAME_AS sandor-clegane`, `gravedigger ALIAS_OF sandor-clegane`, `gravedigger IMPERSONATES sandor-clegane`, or any identity link.** The `gravedigger-theories` node already exists for this reading; wire it to the evidence layer via E9 above, not via identity edges.

---

## NEW-TYPE-REQUEST

**TENDS** — confirmed NOT in the 170-type vocabulary (`edge-type-counts.md` has ATTENDS but not TENDS). **E3 is withdrawn.** The nuance (care that failed — "too little and too late") is absorbed into the `asserted_relation` / note field of E2. The distinction is preserved in the quote; the edge type collapses to HEALS. No new type request filed.

---

## MISFIRE FLAG (not a proposal — an audit note)

`elder-brother HEALS sandor-clegane` (in `graph/edges/edges.jsonl`) has `source_slug: "elder-brother"` — the TITLE node — not `elder-brother-quiet-isle` (the person). The action belongs to the person, not the title. This is a Pass 1 tail-LLM resolution artifact (slug resolved to the title rather than the person). The verify gate should flag this for correction. E2 proposes the correct edge on the right node; the title-node misfire edge should be marked for removal or suppression.

---

## Summary counts

- **Edges proposed:** 8 net (E1–E9 minus E3 withdrawn; E5 revised above)
- **New nodes:** 0
- **Dedup skips:** 10 (listed above)
- **Helm chain:** Complete — no new edges
- **REVEALS_TO brienne-tarth:** 2 already exist; E7 proposes a 3rd distinct disclosure ("The Hound died there, in my arms")
- **Misfire flagged:** `elder-brother HEALS sandor-clegane` on wrong node
- **GATED:** gravedigger identity — NOT minted
