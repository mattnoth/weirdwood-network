# Continue — Deferred structural restructures from S91 rename pass

> **Recommended model:** Opus 4.7 — structural restructures touching multiple node files + new parent-event minting + role-edge reassignment. Sonnet 4.6 acceptable for the Jaime-sheathes case if budget tight.
>
> **Read first:** `working/session-results/2026-06-11-rename-execution.md` — the S91 session that applied 9 renames + 3 pilot edges. The two restructures below were *intentionally deferred* because they are bigger than a slug-swap: each requires minting a new parent event, reassigning role-edges from two sibling stubs, and resolving type-field ambiguity. Subagent decision packets are reproduced in full in this prompt.

## What this session does

Apply the two structural restructures S91 left queued for Matt's review:

1. **Wyman-execution arc** — restructure the Davos / White Harbor deception into a parent event + clarified children (current `lord-wyman-orders-execution` slug is unambiguously about a *fake* execution; the deception layer is missing from the slug name).
2. **Jaime-sheathes-his-sword arc** — consolidate `jaime-sheathes-his-sword-but-orders-ned-s-men-killed` + sibling `jaime-lannister-ambushes-ned-s-party` (both Plate-3 stubs covering the same ~30-second street brawl, both citing AGOT Eddard IX) under a single canonical parent.

Both restructures are well-scoped — subagent decision packets below contain proposed slugs, evidence quotes, edge specs, and chapter pointers.

---

## Restructure 1 — Wyman-execution arc

### Current state
- **Node:** `graph/nodes/events/lord-wyman-orders-execution.node.md` (Plate 3, ADWD Davos III)
- **Sibling:** `graph/nodes/events/wyman-publicly-arrests-davos-at-white-harbor.node.md` (renamed in S91 from `lord-wyman-orders-arrest`; same deception arc; DECEIVES edge already minted)
- **Related:** `graph/nodes/events/learning-about-manderly-s-hostage.node.md` (Davos II — Wylis-as-hostage is the motive); `graph/nodes/events/davos-seaworth-captured.node.md` (Cersei's belief about Davos's death — downstream propagation)

### Subagent recommendation (verbatim)

**Option C (restructure):** Mint a new parent event `wyman-manderly-stages-fake-execution-of-davos` (type=event.deception or similar), make BOTH existing nodes SUB_BEAT_OF that parent, rename `lord-wyman-orders-execution` → `wyman-publicly-orders-davos-execution` for clarity (note: NOT victim-forward because the executed body is a substitute criminal, not Davos), mint a DECEIVES edge wyman-manderly → house-frey (qualifier="staged-execution"), and a SECRETLY_ALLIED_WITH edge wyman-manderly → stannis-baratheon (qualifier="via-davos-envoy", condition="return-of-rickon-stark").

### Steps

1. **Mint new parent node** `graph/nodes/events/wyman-manderly-stages-fake-execution-of-davos.node.md`:
   - type: `event.deception` (or whatever Matt prefers — flag if new type)
   - aliases: `["the mummer's farce", "Manderly's fake execution of Davos", "the staged beheading at White Harbor", "Davos's official death"]`
   - evidence_chapters: `[ADWD Davos III, ADWD Davos IV, AFFC Cersei IV]`
2. **Rename** `lord-wyman-orders-execution` → `wyman-publicly-orders-davos-execution` via `scripts/rename-event-node.py` (dry-run first per S91 pattern; expect ~3-5 edge rows).
3. **Patch body-text** + add aliases per Bug 1 inline form + Bug 3 plate5_superseded_note patching (see S91 patterns).
4. **Add SUB_BEAT_OF edges:**
   - `wyman-publicly-orders-davos-execution` → SUB_BEAT_OF → `wyman-manderly-stages-fake-execution-of-davos`
   - `wyman-publicly-arrests-davos-at-white-harbor` → SUB_BEAT_OF → `wyman-manderly-stages-fake-execution-of-davos`
5. **Mint DECEIVES edge:** wyman-manderly → house-frey, qualifier="staged-execution", evidence_quote: "another man's tarred head and shortened-finger hands were mounted above the Seal Gate with an onion in his mouth; the substitute was a criminal ... the mummer's farce is almost done", evidence_chapter: "adwd-davos-04".
6. **Mint optional second DECEIVES edge:** wyman-manderly → cersei-lannister, qualifier="staged-execution", evidence_chapter: "affc-cersei-04" (Frey-witnesses-attest propagation).
7. **Mint SECRETLY_ALLIED_WITH:** wyman-manderly → stannis-baratheon (or → davos-seaworth), qualifier="via-davos-envoy", condition="return-of-rickon-stark", evidence_chapter: "adwd-davos-04". (Check if SECRETLY_ALLIED_WITH is in locked vocab — if not, escalate before mint.)
8. **Optionally:** Mint `execution-of-davos-lookalike-at-white-harbor` as a separate node for the substitute criminal's actual execution. The lookalike has no name; the current node ambiguously covers either the order or the act. Matt's call.

### Open questions for Matt before running

- Is `event.deception` an acceptable type, or should we use existing types (e.g. `event.conspiracy` is what `gold-cloaks-betray-ned` uses)?
- Should the unnamed substitute criminal get their own event node, or fold the execution into the parent's notes?
- The wiki ([Wyman_Manderly.json]) says Cersei small council is told Davos is dead via Frey witnesses — that's the wider deception's terminal beat. Worth a third sub-beat node, or capture via DECEIVES edge only?

---

## Restructure 2 — Jaime-sheathes-his-sword arc

### Current state
- **Node:** `graph/nodes/events/jaime-sheathes-his-sword-but-orders-ned-s-men-killed.node.md` (Plate 3, AGOT Eddard IX, event.death)
- **Sibling:** `graph/nodes/events/jaime-lannister-ambushes-ned-s-party.node.md` (Plate 3, AGOT Eddard IX, event.incident)
- **Related:** `graph/nodes/events/cersei-claims-ned-s-men-attacked-first.node.md` (AGOT Eddard X — downstream deception by Cersei to Robert)

### Chronology answer (subagent verified)
- This is AGOT **Eddard IX** (not Eddard X as the prompt initially guessed).
- It IS Jaime's retaliation for Catelyn capturing Tyrion at the crossroads inn (Jaime explicitly: "I'm looking for my brother").
- It happens BEFORE Ned's arrest. Ned is wounded here (broken leg from horse falling) but not arrested — arrest comes later in Eddard XIV after Robert's death.

### Subagent recommendation (verbatim)

**Option B + D combined:** Rename current slug to a canonical short form (mint new parent `attack-on-ned-stark-in-the-streets-of-kings-landing`, type=event.battle, Tier 1), SUB_BEAT_OF link both existing nodes (or merge them), and mint a DECEIVES edge (Jaime → Ned, qualifier="sheathes-sword-while-ordering-kill", evidence_chapter "agot-eddard-09").

### Steps

1. **Mint new parent node** `graph/nodes/events/attack-on-ned-stark-in-the-streets-of-kings-landing.node.md`:
   - type: `event.battle` (street brawl)
   - aliases: `["Jaime attacks Ned in King's Landing", "slaughter of Ned's Stark household guards", "Jaime's retaliation for Tyrion's capture", "street brawl outside Chataya's brothel"]`
   - evidence_chapters: `[AGOT Eddard IX]`
2. **Decide merge vs. SUB_BEAT_OF** between the two existing children:
   - Merge: collapse `jaime-sheathes-his-sword-but-orders-ned-s-men-killed` into `jaime-lannister-ambushes-ned-s-party` (or vice versa). Single child.
   - SUB_BEAT_OF: keep both as distinct beats (ambush opens, then sheathes-but-orders-kill is the cinematic climax). Both link to parent.
   - **Subagent recommends merge** — they're "overlapping segments of the same ~30-second brawl" and keeping both creates "ambiguous role-edge attachment for Jory/Heward/Wyl/Tregar deaths."
3. **Mint DECEIVES edge:** jaime-lannister → eddard-stark, qualifier="sheathes-sword-while-ordering-kill", evidence_quote: "He tells Tregar to ensure no harm comes to Lord Stark, then orders 'kill his men'", evidence_chapter: "agot-eddard-09".
4. **Mint downstream DECEIVES edge** (the propagation): cersei-lannister → robert-baratheon, qualifier="false-claim-about-instigator", evidence_chapter: "agot-eddard-10". This is the existing `cersei-claims-ned-s-men-attacked-first` event already in the graph — link as a RELATED_TO edge to the new parent.

### Open questions for Matt before running

- Merge or SUB_BEAT_OF? The two existing nodes have ~6 role-edges between them. Merging is cleaner but loses the "sheathes-but-orders" cinematic detail; SUB_BEAT_OF preserves it but creates the role-edge attachment ambiguity the subagent flagged.
- Type for the new parent: `event.battle` (subagent's pick) vs. `event.ambush` vs. `event.incident`? Check `reference/architecture.md`.

---

## Files / artifacts referenced

- `working/session-results/2026-06-11-rename-execution.md` — S91 results (the prior session's work)
- `scripts/rename-event-node.py` — rename tool (use --dry-run first; same Bug 1 / Bug 3 workarounds as S91)
- `scripts/build-entity-indexes.py --type events --all` — rebuild events index
- `scripts/event_alias_resolver.py --build` — rebuild alias lookup
- `graph/nodes/events/lord-wyman-orders-execution.node.md`
- `graph/nodes/events/jaime-sheathes-his-sword-but-orders-ned-s-men-killed.node.md`
- `graph/nodes/events/jaime-lannister-ambushes-ned-s-party.node.md`
- `graph/edges/edges.jsonl` — append 3-5 new edges per restructure (see specs above)

## Hard rules

- **DO NOT** re-run any rename without re-running its `--dry-run` first.
- **DO NOT** auto-/endsession.
- **DO** ask Matt about the open questions above before minting new node files or new edge types.
- **DO** preserve old slugs as the last entry in aliases (back-compat pattern from S91).
- **DO** add a Bug 3 plate5_superseded_note patch after each rename (S91 found 3 hits across its 9 renames).
- **DO** use INLINE-form aliases (Bug 1).

## End-of-session checklist

- Write `working/session-results/2026-06-12-deferred-restructures.md`
- Update `worklog.md` with a new session entry
- /endsession requires explicit Matt permission per standing rule
