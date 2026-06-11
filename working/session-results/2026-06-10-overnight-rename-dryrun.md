---
date: 2026-06-10
agent: script-builder
task: rename-event-node dry-run + action-slug audit
status: complete
---

# Overnight Dry-Run: joffrey-orders-execution -> execution-of-eddard-stark

## Script built

**Path:** `/Users/mnoth/source/asoiaf-chat/scripts/rename-event-node.py`
**Line count:** 513
**Flags:** `--dry-run` (read-only, prints full diff) | `--apply` (atomic writes via temp + os.replace)

**Handles:**
- Node file move + frontmatter `slug:` and `name:` rewrite
- All `source_slug` / `target_slug` references in `edges.jsonl`
- `superseded_by` field references in `edges.jsonl` (separate category in output)
- `alias-resolver.json` (canonical values + alias keys)
- `event-node-aliases.json` (key rename if slug is a key)
- `cross-references.jsonl` (line-by-line string replace)
- Body-text references in all other `graph/nodes/**/*.node.md` files
- Guards: no-op if slugs identical; abort if new slug collides with existing node file; abort if source node not found
- Name conversion: `slug_to_name()` uses title case with lowercase prepositions/articles (of, the, a, an, and, etc.)

---

## Full --dry-run output

```
============================================================
rename-event-node.py  [DRY-RUN]
  old slug: joffrey-orders-execution
  new slug: execution-of-eddard-stark
============================================================

STEP 1: Node file
  Old path: graph/nodes/events/joffrey-orders-execution.node.md
  New path: graph/nodes/events/execution-of-eddard-stark.node.md
  Frontmatter changes:
    slug:  'joffrey-orders-execution'  ->  'execution-of-eddard-stark'
    name:  'Joffrey orders execution'  ->  'Execution of Eddard Stark'

STEP 2: Edge rows in graph/edges/edges.jsonl
  Total edge rows scanned: 4757
  Rows with 'joffrey-orders-execution' in source_slug/target_slug: 5
  Rows with 'joffrey-orders-execution' in superseded_by only:      1
  Total rows touching 'joffrey-orders-execution': 6

  [1] line 3861: COMMANDS_IN
       source: 'joffrey-baratheon'  ->  'joffrey-baratheon'
       target: 'joffrey-orders-execution'  ->  'execution-of-eddard-stark'
       quote:  "Joffrey commands Ser Ilyn Payne to bring him Eddard's head"
  [2] line 3862: AGENT_IN
       source: 'ilyn-payne'  ->  'ilyn-payne'
       target: 'joffrey-orders-execution'  ->  'execution-of-eddard-stark'
       quote:  "Draws Ice and carries out the beheading"
  [3] line 3863: VICTIM_IN
       source: 'eddard-stark'  ->  'eddard-stark'
       target: 'joffrey-orders-execution'  ->  'execution-of-eddard-stark'
       quote:  "Ser Ilyn Payne draws Ice and carries out the beheading"
  [4] line 3864: WIELDED_IN
       source: 'ice'  ->  'ice'
       target: 'joffrey-orders-execution'  ->  'execution-of-eddard-stark'
       quote:  "Draws Ice and carries out the beheading"
  [5] line 3865: LOCATED_AT
       source: 'joffrey-orders-execution'  ->  'execution-of-eddard-stark'
       target: 'great-sept-of-baelor'  ->  'great-sept-of-baelor'
       quote:  "Sansa begging for mercy; High Septon kneels before Joffrey; "

  Rows where only superseded_by changes:
  [S1] line 34: EXECUTES  ilyn-payne -> eddard-stark
        superseded_by: 'joffrey-orders-execution'  ->  'execution-of-eddard-stark'

STEP 3: Reference files
  alias-resolver.json: no entries reference 'joffrey-orders-execution'
  event-node-aliases.json: no entries reference 'joffrey-orders-execution'
  cross-references.jsonl: no entries reference 'joffrey-orders-execution'

  Other node files: none reference 'joffrey-orders-execution'

============================================================
SUMMARY
  Node file rename:           1
  Edge rows (source/target):  5
  Edge rows (superseded_by):  1
  Total edge rows updated:    6
  alias-resolver.json:        0 entries
  event-node-aliases.json:    0 entries
  cross-references.jsonl:     0 lines
  Other node files:           0 files
  ----------------------------
  Total artifacts changed:    7

[DRY-RUN] No writes performed.
To apply: python3 scripts/rename-event-node.py joffrey-orders-execution execution-of-eddard-stark --apply
```

**S89 probe said 6 edge rows — confirmed.** The 6 are: 5 with source/target == old slug (lines 3861-3865) + 1 with superseded_by == old slug (line 34, the original `ilyn-payne EXECUTES eddard-stark` pass1-derived edge that was superseded when the event hub was minted). The script detects and displays both categories separately and handles both in --apply.

---

## Action-slug pattern audit

**Command run:**
```bash
ls graph/nodes/events/ | grep -E '^[a-z-]*-(orders|claims|demands|calls-for|grants|swears|denies)-'
```

**29 matches found.** Audit table below. Recommendation logic:

- **rename**: slug is action-named for a ONE-TIME specific event; the action is not a recurring behavior of the actor; victim-phrasing or event-phrasing is clearly better
- **keep**: the event IS the recurring behavior (e.g., Cersei ordering multiple executions at once); or the action-framing is the canonical identity of the event; or the specific instance is genuinely ambiguous
- **flag for Matt**: the slug is a sub-beat of a larger event (structural) where renaming would have wider ripple; or the action names a politically-significant command that might need a more descriptive victim name; or the slug is a SUB_BEAT_OF with no clear victim to name it after

| Slug | Display name (from frontmatter) | Sample evidence | Recommendation | Reasoning |
|------|--------------------------------|-----------------|----------------|-----------|
| `aeron-damphair-demands-benfred-s-death` | Aeron Damphair demands Benfred's death | (SUB_BEAT_OF — empty quote) | **keep** | The victim is already in the slug (`benfred`). Action-naming is redundant but the event IS Aeron's specific demand. Victim-phrasing "death-of-benfred-tallheart" would be ambiguous (Benfred appears in other contexts). Keep as-is. |
| `cersei-claims-ned-s-men-attacked-first` | Cersei claims Ned's men attacked first | "She says Ned was returning drunk from a brothel and his men attacked Jaime's guards." | **keep** | This is an act of deception / false testimony, not an execution or appointment. The "claims" verb IS the event — it's Cersei lying to the small council. A victim-phrasing doesn't fit. |
| `cersei-orders-executions` | Cersei orders executions | "Commands Ser Ilyn to behead the would-be deserters and put their heads on pikes" | **flag for Matt** | The plural "executions" suggests multiple victims without names. Could rename to `cersei-orders-deserters-executed` or `beheading-of-deserters-at-cersei-s-command` but neither is clearly better. Also: this is a recurring pattern for Cersei. Matt to decide whether to keep plural action form or collapse into something. |
| `cersei-orders-ned-s-arrest` | Cersei orders Ned's arrest | (SUB_BEAT_OF — wiki-participant quote) | **flag for Matt** | This is a SUB_BEAT_OF a larger event (arrest-of-eddard-stark exists as a node). Renaming risks confusion with the parent. However `arrest-of-eddard-stark` is the cleaner victim-phrasing for the event overall; this is the sub-beat of the specific ORDER. Keep as sub-beat with action naming if the parent node already has the victim-phrasing. |
| `cersei-orders-osney-to-kill-jon-snow` | Cersei orders Osney to kill Jon Snow | "At the Wall, with a hundred men, he kills Jon Snow and receives a royal pardon..." | **rename** | This is a specific assignment (Cersei → Osney Kettleblack → Jon Snow). The action is the command; the event is the assassination plot. Consider `cersei-plots-jon-snow-assassination` or similar. However, Jon Snow is NOT actually killed by Osney — this is a failed plot. A more accurate name would convey the conspiratorial nature. Rename candidate: `cersei-contracts-osney-against-jon-snow`. Flag: this involves a `COMMANDS_IN` edge, so any rename should coordinate with NEW TODO #8 alias resolver. |
| `cersei-orders-the-sleeping-guards-executed` | Cersei orders the sleeping guards executed | "She tells Ser Boros to let them 'sleep forever.'" | **keep** | Specific event, victim group unnamed (generic guards). Action-naming is appropriate because there's no better victim identifier. The "sleeping guards" description is canonical enough to be unambiguous. |
| `doran-orders-arrest-of-the-sand-snakes` | Doran orders arrest of the Sand Snakes | "Commands Hotah to find and confine all eight of Oberyn's daughters..." | **rename** | Victim-group is named: "the Sand Snakes". Cleaner slug: `arrest-of-the-sand-snakes`. The action-phrasing is redundant — Doran as orderer is captured by `COMMANDS_IN`. |
| `hizdahr-orders-drogon-killed` | Hizdahr orders Drogon killed | "Shouts 'Kill it! Kill the beast!' to the spearmen" | **keep** | This is Hizdahr's specific command at the Great Pit of Daznak. Drogon is not killed. A victim-phrasing would be misleading. The action framing captures the political weight of the command (Hizdahr trying to assert control over Daenerys's dragon). |
| `jaime-demands-the-red-wedding-captives` | Jaime demands the Red Wedding captives | "tells Edwyn to inform Lord Walder that King Tommen requires all prisoners" | **keep** | The "demands" verb is the event — a political negotiation moment. No single victim; the group is "Red Wedding captives" which is already in the slug. Action framing is correct here. |
| `jaime-orders-siege-equipment-and-gallows-burned` | Jaime orders siege equipment and gallows burned | (SUB_BEAT_OF — empty quote) | **keep** | Highly specific, unambiguous act. The order IS the event (symbolic end of siege). No cleaner victim-naming exists for burning siege equipment. |
| `jaime-sheathes-his-sword-but-orders-ned-s-men-killed` | Jaime sheathes his sword but orders Ned's men killed | "He tells Tregar to ensure no harm comes to Lord Stark, then orders 'kill his men'" | **rename** | This is too wordy and action-heavy. Consider `massacre-of-ned-s-men-by-lannister-guards` or `killing-of-stark-household-guard`. The victims (Ned's household guard) are the meaningful entity. The "sheathes his sword" detail is prose color, not the slug identity. Rename candidate: `slaughter-of-stark-household-guards`. |
| `joffrey-calls-for-the-bedding` | Joffrey calls for the bedding | (SUB_BEAT_OF — empty quote) | **keep** | This is a sub-beat of a larger event (the Tyrion-Sansa wedding). The "bedding" is a named ASOIAF cultural practice. The action naming captures the specific moment Joffrey makes the demand. Keep as sub-beat. |
| `joffrey-demands-coronation` | Joffrey demands coronation | "Commands coronation within the fortnight and oaths of fealty from councillors." | **keep** | This is Joffrey's specific political act at Robert's deathbed. The "demands" verb IS the event (his first assertion of kingship before the coronation itself). Keep. |
| `joffrey-orders-execution` | Joffrey orders execution | (the primary rename target) | **rename** | Already handled — rename to `execution-of-eddard-stark`. |
| `jon-orders-slynt-hanged-then-changes-to-beheading` | Jon orders Slynt hanged, then changes to beheading | "I will want to speak with Bedwyck and with Janos Slynt" | **rename** | Victim is named (Janos Slynt). The "then changes to beheading" detail is important prose but too wordy for a slug. Cleaner: `execution-of-janos-slynt`. The Jon-orders framing is redundant (captured by COMMANDS_IN/EXECUTES edges). |
| `littlefinger-orders-dontos-killed` | Littlefinger orders Dontos killed | "Ser Lothor, the reward." Brune dips his torch; three crossbows..." | **rename** | Victim is named (Dontos Hollard). Cleaner: `killing-of-dontos-hollard` or `assassination-of-dontos-hollard`. The Littlefinger-orders framing is redundant — his agency is captured by COMMANDS_IN. |
| `lord-walder-calls-for-the-bedding` | Lord Walder calls for the bedding | (SUB_BEAT_OF — empty quote) | **keep** | Sub-beat of Red Wedding. The "calls for the bedding" is the specific trigger moment — Walder invoking the bedding custom as cover for the massacre. Canonical event in ASOIAF. Keep; the action IS the event identity here. |
| `lord-wyman-orders-arrest` | Lord Wyman orders arrest | "Guards surround Davos with silver tridents." | **flag for Matt** | The victim is Davos Seaworth (from the evidence). Cleaner slug: `arrest-of-davos-seaworth`. However, this event may overlap with other Wyman-Manderly scenes. Flag: verify the evidence chapter and ensure `arrest-of-davos-seaworth` doesn't collide with another node. |
| `lord-wyman-orders-execution` | Lord Wyman orders execution | "Gods be good, thought Davos..." (VIOLATES_GUEST_RIGHT edge) | **flag for Matt** | Same concern as above — victim is presumably Davos (threatened execution before Wyman reveals his true allegiance). Cleaner: `wyman-s-threatened-execution-of-davos`. This event is unusual because the "execution" is a fake/deceptive one (Wyman is actually on Davos's side). The action-naming obscures this complexity. Flag: needs human judgment on whether the deceptive nature of the event warrants special framing. |
| `ned-claims-the-execution` | Ned claims the execution | "He refuses to let Ilyn Payne do it; he asks Jory to take the girls away..." | **keep** | The slug captures a very specific moment: Ned asserting his right as a lord to carry out his own execution (of a Night's Watch deserter, Will). This is a distinct event from the execution itself. "Claims the execution" is the canonical identity of this beat. Keep. |
| `ned-orders-daenerys-s-assassination-cancelled` | Ned orders Daenerys's assassination cancelled | "Ned tells Varys to unmake whatever arrangements were made regarding Daenerys." | **keep** | The cancellation-of-assassination is the event. The action ("orders cancelled") IS the entire event identity. No victim-phrasing makes sense (Daenerys is not a victim here; she's being saved). Keep. |
| `ned-orders-janos-slynt-to-arrest-cersei` | Ned orders Janos Slynt to arrest Cersei | (SUB_BEAT_OF — empty quote) | **flag for Matt** | Sub-beat. Victim named (Cersei). Consider `ned-orders-cersei-s-arrest` (cleaner). But: Ned's plan fails — Janos Slynt betrays him. The action framing captures the failed plan identity. Could also be `slynt-betrays-ned-during-cersei-arrest`. Flag: the betrayal is the narratively-significant outcome, not the order itself. |
| `qhorin-orders-ygritte-s-execution` | Qhorin orders Ygritte's execution | "You are my captive, Ygritte." (CAPTURES edge) | **rename** | Victim named (Ygritte). The order is a command; the event is the threatened execution. However: Ygritte is NOT executed — Jon refuses and lets her go. Cleaner: `qhorin-orders-ygritte-killed` (more accurate to what happens narratively) or keep the action form since the event is specifically about the command, not the act. Given the failed nature, `jon-defies-qhorin-s-order-to-kill-ygritte` captures the actual event better. This is a judgment call — flagging for Matt. |
| `quentyn-orders-the-attack` | Quentyn orders the attack | "He croaks 'Take them,' and the fight begins." | **keep** | The attack on the dragons. "The attack" is specific enough in context (Quentyn's disastrous dragonstealing attempt). This is already the canonical form in the graph. |
| `skahaz-demands-hostage-executions` | Skahaz demands hostage executions | "Barristan refuses again, as he has a hundred times..." | **keep** | Recurring demand with plural unnamed victims (Meereenese hostages). Action-naming is appropriate because there's no single victim to name the event after. |
| `styr-orders-jon-to-kill-the-old-man` | Styr orders Jon to kill the old man | "The Magnar commands Jon to prove his loyalty by executing the captive." | **keep** | The event IS the loyalty test. Victim is unnamed ("the old man"). Action framing is appropriate. The significant moment is Jon's refusal/compliance decision, not the old man's death. Keep. |
| `the-crew-calls-for-moqorro-s-death` | The crew calls for Moqorro's death | "Burton Humble and others urge killing him." | **keep** | This is a group demand at sea, with no single orderer. Moqorro is not killed. Action framing captures the crew's collective call. Keep. |
| `tyrion-orders-symon-s-assassination` | Tyrion orders Symon's assassination | (KILLS edge from evidence) | **rename** | Victim named (Symon Silver Tongue). Cleaner: `assassination-of-symon-silver-tongue`. The Tyrion-orders framing is redundant (captured by COMMANDS_IN). This is a clean rename candidate. |
| `victarion-orders-kerwin-killed` | Victarion orders Kerwin killed | "Pointing with his smoking hand, he orders the maester's throat cut..." | **rename** | Victim named (Kerwin — actually "Maester Kerwin" of the Iron Victory). Cleaner: `killing-of-maester-kerwin` or `victarion-kills-maester-kerwin`. The order-framing is redundant. |

---

## Surprises

**None — the graph is clean on this slug.** `joffrey-orders-execution` does not appear in:
- `alias-resolver.json` (not registered as a canonical target for any alias)
- `event-node-aliases.json` (not a key in the event alias map)
- `cross-references.jsonl` (no wiki cross-refs to this slug)
- Any other node body file

This means the rename only touches: 1 node file + 6 edge rows. Minimal blast radius. The one surprise worth noting: the **superseded_by field** on line 34 (`ilyn-payne EXECUTES eddard-stark`) — S89 counted "6 edges" and the script correctly finds all 6, including this superseded marker. The S89 probe was using `grep -c '"joffrey-orders-execution"'` which counts raw string matches, matching the script's total of 6.

**Name field is auto-derived from slug:** The script converts `execution-of-eddard-stark` to `"Execution of Eddard Stark"` using title-case logic with lowercase prepositions. This matches the architecture.md example format. However, Matt may want to manually set the `name:` field to `"Execution of Eddard Stark"` in the node frontmatter if the auto-derived form isn't exactly right.

---

## Action-slug audit summary

Of the 29 action-named slugs scanned:

| Recommendation | Count | Slugs |
|----------------|-------|-------|
| **rename** | 6 | `joffrey-orders-execution` (primary), `doran-orders-arrest-of-the-sand-snakes`, `jon-orders-slynt-hanged-then-changes-to-beheading`, `littlefinger-orders-dontos-killed`, `tyrion-orders-symon-s-assassination`, `victarion-orders-kerwin-killed` |
| **keep** | 14 | `aeron-damphair-demands-benfred-s-death`, `cersei-claims-ned-s-men-attacked-first`, `cersei-orders-the-sleeping-guards-executed`, `hizdahr-orders-drogon-killed`, `jaime-demands-the-red-wedding-captives`, `jaime-orders-siege-equipment-and-gallows-burned`, `joffrey-calls-for-the-bedding`, `joffrey-demands-coronation`, `lord-walder-calls-for-the-bedding`, `ned-claims-the-execution`, `ned-orders-daenerys-s-assassination-cancelled`, `quentyn-orders-the-attack`, `skahaz-demands-hostage-executions`, `styr-orders-jon-to-kill-the-old-man`, `the-crew-calls-for-moqorro-s-death` |
| **flag for Matt** | 9 | `cersei-orders-executions`, `cersei-orders-ned-s-arrest`, `cersei-orders-osney-to-kill-jon-snow`, `jaime-sheathes-his-sword-but-orders-ned-s-men-killed`, `lord-wyman-orders-arrest`, `lord-wyman-orders-execution`, `ned-orders-janos-slynt-to-arrest-cersei`, `qhorin-orders-ygritte-s-execution`, `jaime-sheathes-his-sword-but-orders-ned-s-men-killed` |

The 5 clean rename candidates (besides the primary `joffrey-orders-execution`) share a pattern: named victim + order-framing that's redundant with existing role edges. They are low-risk renames. The 9 flagged ones have complexity: plural victims, sub-beat status, failed/deceptive events, or unusual narrative weight in the action itself.

---

## APPLY COMMAND

```bash
python3 scripts/rename-event-node.py joffrey-orders-execution execution-of-eddard-stark --apply
```

---

## Readiness note

Dry-run looks clean and ready to apply. 6 edge rows confirmed (matches S89 probe count), no references in alias-resolver, event-node-aliases, cross-references, or other node files. Minimal blast radius. The only human judgment call is whether to accept the auto-derived `name: "Execution of Eddard Stark"` or manually set a different surface form — but the auto-derived form matches architecture.md conventions.
