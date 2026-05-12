# Worker Snippet — Case-Collision Reconstruction Template

**Purpose:** Reusable worker prompt body for case-collision wiki-page reconstruction missions. Paste into a fresh worker prompt with the slug list and validation step appended.

**Why this exists:** Workers don't reliably load referenced files when instructed to "consult architecture.md" or "read the spec." Drift errors in Session 46 (workers proposing `event.conflict` when `event.war` already exists; framing `object.text` as a "new" type when it's heavy-use existing convention) trace back to workers not loading project context. The fix: inline everything the worker needs directly in the prompt. No indirection.

**How to use:** Copy the body below into a worker kickoff prompt. Replace `<WAVE_ID>` and add the slug list. Append the validation step (also below) with the slug list re-inlined for the validation loop. One worker handles one wave (5 slugs default; up to 10).

---

## ━━━ PASTE-IN BODY (start) ━━━

You are a v1-protocol wave-sized worker for case-collision wiki-page reconstruction (wave <WAVE_ID>). Working dir: /Users/mnoth/source/asoiaf-chat

Reconstruct Identity + Edges for the slugs in your assignment list, sequentially in one session. For each slug, no refetch — work only from the existing graph + cached wiki data.

### Entity types — pick from this list ONLY

Use the EXISTING type strings below. Do NOT invent new types. If your slug doesn't fit any of these, mark `status: partial` and surface the missing-type case in `notes`.

| Type string | Description | Examples |
|---|---|---|
| `character.human` | Named human individual | Jon Snow, Jaqen H'ghar |
| `character.direwolf` | Named Stark direwolf | Ghost, Grey Wind |
| `character.dragon` | Named dragon with narrative agency | Drogon, Balerion |
| `place.location` | Specific named place | Winterfell, Tower of Joy |
| `place.region` | Geographic area containing locations | The North, Dorne, Narrow Sea |
| `organization.house` | Noble house or dynasty | House Stark, House Targaryen |
| `organization.faction` | Non-dynastic org, order, alliance | Night's Watch, Faceless Men, Brotherhood Without Banners |
| `organization.religion` | Belief system + institutions | Faith of the Seven, R'hllor |
| `concept.culture` | Ethnic/regional cultural group | Dothraki, Ironborn, **Free Folk** |
| `concept.magic` | Magical system, ability, phenomenon | Warging, greensight, glass candles |
| `concept.prophecy` | Prophetic statement or vision | Azor Ahai, Maggy the Frog |
| `concept.theory` | Interpretive framework | R+L=J, Grand Northern Conspiracy |
| `concept.language` | In-world language | High Valyrian, Old Tongue |
| `concept.medical` | Disease, poison, treatment | Greyscale, milk of the poppy |
| `concept.custom` | Cultural practice, tradition, ceremony | Bedding, Guest right, Kingsmoot, **Trial of Seven** |
| `species` | Non-human biological lineage | Children of the Forest, Others, giants |
| `title` | Named office or rank | Hand of the King, **King-Beyond-the-Wall**, **Master of Coin** |
| `object.artifact` | Object of narrative significance | Ice, Dragonbinder, Dawn |
| `object.text` | In-world book, document, song | The Jade Compendium, The Rains of Castamere, **Jenny's Song** |
| `object.food` | In-world food or drink | Lemon cakes, Arbor gold, dreamwine |
| `object.material` | Raw material, mineral, substance | Dragonglass, Valyrian steel (substance) |
| `event.battle` | Single tactical engagement | Battle of the Blackwater, Red Wedding |
| `event.war` | Multi-battle named conflict | War of the Five Kings, Robert's Rebellion, **Ghiscari Wars** |
| `event.tournament` | Formal tourney or melee | Tourney at Harrenhal, Hand's Tourney |

**Critical type clarifications:**
- **Wars are NOT battles.** A war spans multiple battles. War of the Five Kings = `event.war`, NOT `event.battle`. Ghiscari Wars = `event.war`. If your slug describes a multi-battle conflict, use `event.war`.
- **Songs are `object.text`.** Not `object.song`, not `concept.cultural`. Songs (Rains of Castamere, Jenny's Song) live at `graph/nodes/texts/` with `type: object.text`.
- **Books (in-world) are `object.text`.** The Jade Compendium, A Caution for Young Girls. Real-world book titles (`a-feast-for-crows`, `beyond-the-wall-(book)`) are NOT in-world entities — mark them `status: fail` with note "real-world publication metadata."
- **Cultures vs factions:** Free Folk = `concept.culture` (their faction-ness emerges via member/conflict/leader edges, not a second type). Ironborn = `concept.culture`. Dothraki = `concept.culture`. Children of the Forest = `species` (biological lineage).

### Edge vocabulary — pick from this list ONLY

Locked 22-type vocabulary. Never invent new edge types. If a candidate edge doesn't map to one of these, surface in `notes` — don't emit it.

**Kinship + relationships:**
`PARENT_OF`, `SIBLING_OF`, `SPOUSE_OF`, `BETROTHED_TO`, `LOVER_OF`, `WARD_OF`, `ANCESTOR_OF`, `HEIR_TO`, `CADET_BRANCH_OF`

**Power + authority:**
`RULES`, `OVERLORD_OF`, `SWORN_TO`, `COMMANDS`, `SERVES`, `ADVISES`, `HOLDS_TITLE`, `SUCCEEDS`, `CLAIMS`, `APPOINTS`, `DEPOSES`

**Organizational:**
`MEMBER_OF`, `FOUNDED`, `ALLIES_WITH`, `OPPOSES`, `MANIPULATES`, `BETRAYS`, `NEGOTIATES_WITH`

**Geography + events:**
`LOCATED_AT`, `RULES_REGION_OF` (use sparingly), `FIGHTS_IN` (Person → Event/War), `COMMANDS_IN` (Person → Event/War), `KILLS`, `DIED_AT`, `BORN_AT`

**Religion:**
`WORSHIPS` (Person → Religion), `RELIGION_OF` (Location → Religion)

**Text:**
`WRITTEN_BY` (Text → Author)

**Containment:**
`PART_OF` (Battle → War) — "this battle is a component of this war". Use when a discrete named battle belongs to a larger named war.

### Reconstruction steps (per slug, sequential)

1. Read `working/wiki/data/backlink-counts.json`. The entry for your slug is at `data["backlinks"][<slug>]`. Use the `top_sources` list (highest-backlink source slugs that reference this target).

2. For each top source slug (form `<name>.prose` or `<name>`), locate the node file under `graph/nodes/<type>/<slug>.node.md`. Strip `.prose` if present. Try directories in this order: `characters/`, `houses/`, `factions/`, `religions/`, `locations/`, `events/`, `titles/`, `concepts/`, `species/`, `texts/`, `artifacts/`, `foods/`, `materials/`, `languages/`, `medical/`, `customs/`. Use Glob/find as fallback.

3. For each source file, grep for sentences mentioning the slug. Try kebab form (e.g., `free-folk`), Title Case form (`Free Folk`), and obvious aliases (`wildlings`, `the free folk`).

4. **Alias-merge check (before writing output):** grep `graph/nodes/` for existing nodes whose slug or aliases overlap with yours. Examples to look for: feminine forms (`red-priest` vs `red-priestess`), plural variants (`pit-fighter` vs `pit-fighters`), alternate casings/spellings (`inn-at-the-crossroads` vs `crossroads-inn`), known phrasing variants. If an overlapping node exists, mark `status: partial` and propose alias-merge in `notes` — do NOT create a duplicate node.

5. Synthesize a 1-3 paragraph Identity section from the sentences you found. Conservative paraphrase — do NOT invent. If sources are thin, write a shorter Identity and reflect that in confidence.

6. **Edges — reverse-lookup is the DEFAULT strategy, not a fallback.** Most case-collision slugs are redirect/list pages with no direct infobox, so reverse-lookup is the primary source of edges.
   - First: check `working/wiki/data/infobox-data.jsonl` for a direct infobox keyed to your slug. If present, derive edges from infobox fields per the architecture.md infobox→edge mapping (locked 22-type vocab).
   - Always: grep `working/wiki/data/infobox-data.jsonl` for entries whose fields *target* your slug (e.g., `HOLDS_TITLE: <slug-as-Title-Case>`, `SWORN_TO: <slug>`, `MEMBER_OF: <slug>`, `RELIGION_OF: <slug>`, `LOCATED_AT: <slug>`, `BORN_AT: <slug>`). Emit those as Edges in your output. Reverse-lookup is the primary mechanism for redirect/list-page slugs.
   - Never invent edge types. If a candidate edge has no vocab fit, note it; don't emit.

7. Write `working/missions/<MISSION_SCRATCH_DIR>/worker-<slug>/output.md`:

```markdown
---
slug: <slug>
type: <one of the type strings above>
pass_origin: pass2-wiki-reconstruction-mission-<batch-id>
reconstructed_at: <real ISO 8601 UTC>
aliases: [<known aliases>]
---
## Identity
<1-3 paragraphs, paraphrased from sources, no invention>

## Edges
<EDGE_TYPE: target-slug — one per line>
```

8. Write `working/missions/<MISSION_SCRATCH_DIR>/worker-<slug>/status.json` per v1 schema (MANDATORY — validated in step 10):

```json
{
  "worker_id": "<mission-id>-<slug>",
  "started_at": "<real ISO 8601 UTC>",
  "completed_at": "<real ISO 8601 UTC>",
  "status": "pass" | "partial" | "fail",
  "confidence": <numeric float 0.0-1.0>,
  "source_count": <int>,
  "source_files_consulted": [<list of strings>],
  "notes": "<string or array of strings>"
}
```

**Schema lock — do NOT drift on these fields:**
- `status`: EXACTLY one of `"pass"`, `"partial"`, `"fail"`. NOT `"complete"`, NOT `"done"`, NOT `"complete"`.
- `confidence`: numeric `0.0`-`1.0`. NOT `"high"`, NOT `"tier-1"`, NOT any string.
- `started_at` + `completed_at`: real ISO 8601 UTC from `datetime.utcnow().isoformat()+"Z"`. NOT placeholder `T00:00:00Z` values.
- Field names exactly as written above: `started_at` (NOT `started`/`created_at`), `completed_at` (NOT `completed`/`updated_at`).

9. If blocked on a question, write `working/missions/<MISSION_SCRATCH_DIR>/worker-<slug>/questions-for-matt.jsonl` with one row per question.

### Allowed `fail` cases

Some slugs are NOT canonical in-world entities and should fail with `confidence: 0.0` + `notes` explanation:
- Real-world publication metadata (`a-feast-for-crows`, `beyond-the-wall-(book)`)
- Disambiguation pages (`<name>-(disambiguation)`)
- List articles (`list-of-rivers`, `timeline-of-major-events`, `list-of-characters`)
- Meta-wiki concepts (`pov-character`)
- Too-generic phrases that don't refer to a discrete entity (`rule-of-thumb`, `trade-talk`)

Do NOT invent content for these. Mark `status: fail`, write the status.json, skip the output.md.

## ━━━ PASTE-IN BODY (end) ━━━

---

## Schema-validation step (append to every worker prompt)

After all slugs are written, run this validation:

```python
import json, re, os
slugs = [<inline list of slugs for this worker>]
mission_dir = '<mission scratch dir, e.g., working/missions/case-collision-batch-3>'
errors = []
iso_re = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')
for slug in slugs:
    p = f'{mission_dir}/worker-{slug}/status.json'
    if not os.path.exists(p):
        errors.append(f'{slug}: status.json missing'); continue
    try:
        d = json.load(open(p))
    except Exception as e:
        errors.append(f'{slug}: cannot load ({e})'); continue
    if d.get('status') not in ('pass','partial','fail'):
        errors.append(f'{slug}: bad status {d.get("status")!r}')
    c = d.get('confidence')
    if not isinstance(c, (int, float)) or not 0.0 <= c <= 1.0:
        errors.append(f'{slug}: bad confidence {c!r}')
    for f in ('worker_id','started_at','completed_at','source_count','source_files_consulted','notes'):
        if f not in d:
            errors.append(f'{slug}: missing {f}')
    if not iso_re.match(d.get('started_at','')):
        errors.append(f'{slug}: bad started_at')
    if str(d.get('started_at','')).startswith('2026-05-12T00:0'):
        errors.append(f'{slug}: placeholder timestamp')
print('VALIDATION:', errors if errors else 'PASS')
```

If `VALIDATION: PASS`, you're done. If errors, fix the offending status.json files before exiting.

---

## DO NOT (every worker)

- Refetch wiki pages (CLAUDE.md hard rule — wiki cache is local-only)
- Write to `graph/nodes/` (this is mission scratch; promotion is a separate step)
- Touch other workers' scratch dirs
- Auto-run `/endsession`
- Invent edge types or entity types (locked vocabularies)
- Skip the schema-validation step (mandatory in v1)

---

## Return summary (every worker)

Per-slug row: `slug | status | confidence | source_count | canonical?`
Plus: validation result (PASS or list of errors)
Plus: any flags — multi-type cases, alias-merge candidates, edge-vocab gaps, type-collision against existing graph nodes.
