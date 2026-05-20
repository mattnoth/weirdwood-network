# Stage 4 Haiku Edge-Type Normalizer Report — 2026-05-19

> **Mode:** LIVE RUN — files rewritten in place

## Summary

| Metric | Count |
|--------|-------|
| Canonical vocab size | 159 |
| Files scanned | 70 |
| Total rows scanned | 1752 |
| `emit_edge` rows | 556 |
| Already canonical | 533 |
| Morphological — auto-rewritten | 0 |
| Semantically distinct — NOT rewritten | 22 |
| Schema violations (missing field) | 1 |
| Below difflib threshold — unresolved | 0 |

## Bucket 1 — Morphological: auto-rewritten

Same English verb/noun, differing only by inflection (tense) or literal string corruption.
These are the ONLY rows the normalizer actually rewrites.

_No morphological rewrites in this run._

## Bucket 2 — Non-canonical, semantically distinct: NOT rewritten

These types are different words/concepts — not inflections of a canonical type.
They must stay visible as classification errors so drift-measurement signal
against Sonnet output is not corrupted. Needs re-classification or model escalation.

| Raw | Count | Example file |
|-----|-------|-------------|
| `GRANDCHILD_OF` | 5 | `working/wiki/pass2-buckets/characters-house-frey-t-z/prose-edges-haiku/walder-frey.edges.jsonl` |
| `IMPRISONED_AT` | 5 | `working/wiki/pass2-buckets/characters-house-lorch/prose-edges-haiku/biter.edges.jsonl` |
| `TRAVELS_WITH` | 2 | `working/wiki/pass2-buckets/characters-house-glover/prose-edges-haiku/galbart-glover.edges.jsonl` |
| `SUPERVISES` | 1 | `working/wiki/pass2-buckets/characters-house-glover/prose-edges-haiku/glover-steward.edges.jsonl` |
| `REPORTS_TO` | 1 | `working/wiki/pass2-buckets/characters-house-glover/prose-edges-haiku/glover-steward.edges.jsonl` |
| `ENCOUNTERS` | 1 | `working/wiki/pass2-buckets/characters-house-glover/prose-edges-haiku/robett-glover.edges.jsonl` |
| `ACCOMPANIES` | 1 | `working/wiki/pass2-buckets/characters-house-glover/prose-edges-haiku/robett-glover.edges.jsonl` |
| `TRADED_FOR` | 1 | `working/wiki/pass2-buckets/characters-house-glover/prose-edges-haiku/robett-glover.edges.jsonl` |
| `FOSTERED_BY` | 1 | `working/wiki/pass2-buckets/characters-house-lorch/prose-edges-haiku/biter.edges.jsonl` |
| `USES` | 1 | `working/wiki/pass2-buckets/characters-house-lorch/prose-edges-haiku/jaqen-hghar.edges.jsonl` |
| `ATTACKED_BY` | 1 | `working/wiki/pass2-buckets/characters-house-lorch/prose-edges-haiku/rorge.edges.jsonl` |
| `FOSTERED_BY_INVERSE` | 1 | `working/wiki/pass2-buckets/characters-house-lorch/prose-edges-haiku/rorge.edges.jsonl` |
| `GUARDS` | 1 | `working/wiki/pass2-buckets/characters-house-marbrand/prose-edges-haiku/addam-marbrand.edges.jsonl` |

## Bucket 3 — Schema violations: missing `edge_type` field

emit_edge rows that are missing the `edge_type` field entirely.
Passed through unchanged — these are structural errors, not normalization targets.

| Raw | Count | Example file |
|-----|-------|-------------|
| `<missing>` | 1 | `working/wiki/pass2-buckets/characters-house-glover/prose-edges-haiku/robett-glover.edges.jsonl` |

## Canonical Edge-Type List (full sorted, for eyeball check)

Parser returned 159 types. Locked count of record is 159.
If the count differs by ±2, check for non-edge-type backticked tokens in the
Edge Types section of architecture.md (book abbreviations, file extensions, etc.).

  1. `ADVISES`
  2. `AFFLICTED_BY`
  3. `ALIAS_OF`
  4. `ALLIES_WITH`
  5. `ANCESTOR_OF`
  6. `ANCESTRAL_WEAPON_OF`
  7. `APPEARS_TO_FULFILL`
  8. `APPOINTS`
  9. `ASSAULTS`
 10. `ATTACKS`
 11. `ATTENDS`
 12. `BANISHES`
 13. `BESIEGES`
 14. `BESTOWS_KNIGHTHOOD_ON`
 15. `BETRAYS`
 16. `BETROTHED_TO`
 17. `BONDED_TO`
 18. `BORN_AT`
 19. `BREAKS_VOW`
 20. `BUILT`
 21. `BURIED_AT`
 22. `CADET_BRANCH_OF`
 23. `CAPTAIN_OF`
 24. `CAPTURES`
 25. `CAUSES`
 26. `CITED_BY`
 27. `CLAIMS`
 28. `CLERGY_OF`
 29. `COMMANDS`
 30. `COMMANDS_IN`
 31. `COMPANION_OF`
 32. `CONSPIRES_WITH`
 33. `CONTEMPORARY_WITH`
 34. `CONTRACTED_WITH`
 35. `CONTRADICTS`
 36. `CONTRASTS`
 37. `COURTS`
 38. `COUSIN_OF`
 39. `CREW_OF`
 40. `CROWNS_QUEEN_OF_LOVE_AND_BEAUTY`
 41. `CULTURE_OF`
 42. `CURSES`
 43. `DECEIVED_BY`
 44. `DECEIVES`
 45. `DEFEATS`
 46. `DEPICTED_IN`
 47. `DEPOSES`
 48. `DIED_AT`
 49. `DIED_OF`
 50. `DISGUISED_AS`
 51. `DISTRUSTS`
 52. `DREAMS_OF`
 53. `DUELS`
 54. `ECHOES`
 55. `ENABLES`
 56. `EXECUTED_WITH`
 57. `EXECUTES`
 58. `FEARS`
 59. `FIGHTS_IN`
 60. `FORESHADOWS`
 61. `FORGED_BY`
 62. `FOUNDED`
 63. `FULFILLS`
 64. `GIFTED_TO`
 65. `GRANTS_SAFE_CONDUCT`
 66. `GUEST_OF`
 67. `HATES`
 68. `HEALS`
 69. `HEIR_TO`
 70. `HELD_BY`
 71. `HOARDS`
 72. `HOLDS_TITLE`
 73. `IGNORANT_OF`
 74. `IMPERSONATES`
 75. `IMPRISONS`
 76. `INFORMS`
 77. `INHERITED_BY`
 78. `INVESTIGATES`
 79. `IN_LAW_OF`
 80. `KILLED_BY`
 81. `KILLED_WITH`
 82. `KILLS`
 83. `KNIGHTED_BY`
 84. `KNOWS`
 85. `LOCATED_AT`
 86. `LOOTED_BY`
 87. `LOVER_OF`
 88. `LOVES`
 89. `MADE_OF`
 90. `MANIPULATES`
 91. `MARRIES_OFF`
 92. `MEMBER_OF`
 93. `MILK_BROTHER_OF`
 94. `MOTIVATES`
 95. `MOURNS`
 96. `NAMED_AFTER`
 97. `NEGOTIATES_WITH`
 98. `NEPHEW_OF`
 99. `NURSED_BY`
100. `OFFICIATES`
101. `OPPOSES`
102. `OVERLORD_OF`
103. `OWNS`
104. `PARALLELS`
105. `PARENT_OF`
106. `PARTICIPATES_IN`
107. `PART_OF`
108. `PERCEIVED_AS`
109. `POISONS`
110. `PRACTICES`
111. `PREVENTS`
112. `PRISONER_OF`
113. `PROPHESIED_BY`
114. `PROPOSED_AS_BRIDE`
115. `PROTECTS`
116. `PURCHASED_FROM`
117. `RANSOMS`
118. `REFORGED_INTO`
119. `REGION_OF`
120. `REPUTED_AS`
121. `RESCUES`
122. `RESENTS`
123. `RESPECTS`
124. `RESURRECTS`
125. `REVEALS_TO`
126. `RULES`
127. `SACRED_TO`
128. `SACRIFICES`
129. `SAME_AS`
130. `SEAT_OF`
131. `SEEKS`
132. `SERVES`
133. `SIBLING_OF`
134. `SPIES_ON`
135. `SPOUSE_OF`
136. `STEP_CHILD_OF`
137. `STEP_PARENT_OF`
138. `SUBJECT_OF_PROPHECY`
139. `SUBVERTS`
140. `SUBVERTS_PROPHECY`
141. `SUCCEEDS`
142. `SUPPORTS`
143. `SWORN_TO`
144. `TEACHES`
145. `TORTURES`
146. `TRAVELS_TO`
147. `TRIGGERS`
148. `TRUSTS`
149. `TUTORS`
150. `UNCLE_OF`
151. `VIOLATES_GUEST_RIGHT`
152. `VOWS_TO`
153. `WARD_OF`
154. `WARGS_INTO`
155. `WET_NURSE_OF`
156. `WIELDED_IN`
157. `WIELDS`
158. `WORSHIPS`
159. `WRITTEN_BY`

---

*Generated by `scripts/stage4-haiku-normalize-edge-types.py` — 2026-05-19*
