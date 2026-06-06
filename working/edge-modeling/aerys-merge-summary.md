# Aerys Slug Merge — Summary

**Phantom slug:** `aerys-targaryen`  
**Canonical slug:** `aerys-ii-targaryen`  

## Node file confirmation

- Phantom node `graph/nodes/characters/aerys-targaryen.node.md`: exists  
- Canonical node `graph/nodes/characters/aerys-ii-targaryen.node.md`: exists  

Both nodes were inspected and confirm the same person: Aerys II Targaryen, the Mad King (262–283 AC). The phantom node (`aerys-targaryen`) is a stub created by the wiki scraper from the plain 'Aerys Targaryen' page, while the canonical node (`aerys-ii-targaryen`) is the richly populated article page. They are the same individual.  

**DO NOT CONFUSE with:** `aerys-i-targaryen` (an earlier Targaryen king), `aerys-targaryen-son-of-aegon`, or `aerys-ii-targaryens-last-mistress` — these are distinct entities and were NOT touched.

## Edges affected: 3

| # | Source → Target | Edge Type | Asserted Relation |
|---|-----------------|-----------|-------------------|
| 1 | `jaime-lannister` → `aerys-targaryen` | KILLS | killed |
| 2 | `jaime-lannister` → `aerys-targaryen` | SERVES | formerly served (conflicted) |
| 3 | `lord-redwyne` → `aerys-targaryen` | SERVES | loyal to (past) |

## Rewritten rows

- **BEFORE:** `jaime-lannister` → `aerys-targaryen` (KILLS)  
  **AFTER :** `jaime-lannister` → `aerys-ii-targaryen` (KILLS)  
- **BEFORE:** `jaime-lannister` → `aerys-targaryen` (SERVES)  
  **AFTER :** `jaime-lannister` → `aerys-ii-targaryen` (SERVES)  
- **BEFORE:** `lord-redwyne` → `aerys-targaryen` (SERVES)  
  **AFTER :** `lord-redwyne` → `aerys-ii-targaryen` (SERVES)  

## Quarantine recommendation (for Plate 5)

After the Plate 5 merge, the phantom node `graph/nodes/characters/aerys-targaryen.node.md` will have zero edges pointing to it. Per project convention, it should be moved to `graph/nodes/characters/_conflicts/aerys-targaryen.node.md` with a stale-preamble noting the redirect to `aerys-ii-targaryen`.  

**Do NOT delete the node file** — source data is read-only/additive-only per CLAUDE.md. The `_conflicts/` quarantine preserves the record while preventing the phantom from polluting traversal queries.  

This quarantine step is **out of scope for Plates 0-4**. It is bundled into the Plate 5 merge step (gated on Matt's sign-off).
