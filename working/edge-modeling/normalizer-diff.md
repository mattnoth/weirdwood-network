# Edge Direction Normalizer — Diff Report

Input: `graph/edges/edges.jsonl` (3811 rows)  
Output: `working/edge-modeling/normalizer-candidates.jsonl`  

## Summary

| Action | Count |
|--------|-------|
| flipped | 10 |
| kept | 3800 |
| flagged | 1 |
| **total** | **3811** |

## Per-edge-type breakdown (flipped rows)

| Edge Type | Flipped Count |
|-----------|---------------|
| RESCUES | 2 |
| KILLS | 2 |
| BETRAYS | 2 |
| HEALS | 1 |
| CAPTURES | 1 |
| TUTORS | 1 |
| ATTACKS | 1 |

## Verification probes

Known-inverted rows from design doc §1:

- **cressen → melisandre KILLS (asserted: 'Killed by')**: YES — flipped correctly
- **arya → sandor CAPTURES (asserted: 'Conflicted captor-dependent relationship')**: YES — flipped correctly
- **tyrion → shae BETRAYS (asserted: 'Betrayed by (former lover)')**: YES — flipped correctly

## Flipped rows (detailed)

### HEALS — gared → aemon-targaryen-son-of-maekar-i
- **BEFORE:** `gared` → `aemon-targaryen-son-of-maekar-i` (`Treated by`)  
- **AFTER :** `aemon-targaryen-son-of-maekar-i` → `gared`  
- **Signal:** reverse signal: passive: treated by  

### RESCUES — daenerys-targaryen → barristan-selmy
- **BEFORE:** `daenerys-targaryen` → `barristan-selmy` (`rescued by`)  
- **AFTER :** `barristan-selmy` → `daenerys-targaryen`  
- **Signal:** reverse signal: passive: rescued by  

### CAPTURES — arya-stark → sandor-clegane
- **BEFORE:** `arya-stark` → `sandor-clegane` (`Conflicted captor-dependent relationship`)  
- **AFTER :** `sandor-clegane` → `arya-stark`  
- **Signal:** reverse signal: role-noun patient: captor-dependent  

### KILLS — cressen → melisandre
- **BEFORE:** `cressen` → `melisandre` (`Killed by / ran afoul of`)  
- **AFTER :** `melisandre` → `cressen`  
- **Signal:** reverse signal: passive: killed by  

### RESCUES — jaime-lannister → brienne-tarth
- **BEFORE:** `jaime-lannister` → `brienne-tarth` (`rescued by/protects`)  
- **AFTER :** `brienne-tarth` → `jaime-lannister`  
- **Signal:** reverse signal: passive: rescued by  

### BETRAYS — tyrion-lannister → shae
- **BEFORE:** `tyrion-lannister` → `shae` (`Betrayed by (former lover)`)  
- **AFTER :** `shae` → `tyrion-lannister`  
- **Signal:** reverse signal: passive: betrayed by  

### TUTORS — brienne-tarth → goodwin
- **BEFORE:** `brienne-tarth` → `goodwin` (`Mentored by (memory)`)  
- **AFTER :** `goodwin` → `brienne-tarth`  
- **Signal:** reverse signal: passive: mentored by  

### KILLS — oberyn-martell → gregor-clegane
- **BEFORE:** `oberyn-martell` → `gregor-clegane` (`killed by`)  
- **AFTER :** `gregor-clegane` → `oberyn-martell`  
- **Signal:** reverse signal: passive: killed by  

### BETRAYS — jorah-mormont → lynesse-hightower
- **BEFORE:** `jorah-mormont` → `lynesse-hightower` (`Betrayed by`)  
- **AFTER :** `lynesse-hightower` → `jorah-mormont`  
- **Signal:** reverse signal: passive: betrayed by  

### ATTACKS — ghost → eagle
- **BEFORE:** `ghost` → `eagle` (`Attacked by`)  
- **AFTER :** `eagle` → `ghost`  
- **Signal:** reverse signal: passive: attacked by  

