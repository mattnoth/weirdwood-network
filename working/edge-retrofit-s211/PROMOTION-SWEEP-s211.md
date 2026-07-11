# Node-type promotion sweep — S211 (piggybacked on the edge-retrofit session)

The todos-294 MED item: promote nodes S207 Part A conservatively parked in
`event.incident` (and battle→war stragglers) up to the sanctioned leaf where the node
genuinely is one. Deterministic slug-pattern candidates + per-node content verification;
promote ONLY where slug AND content agree.

## Applied (12 retypes; node frontmatter + surgical per-node index patch)
- `event.capture` ×2: arrest-of-eddard-stark · arrest-of-queen-alicent
- `event.assassination` ×2: murder-of-jon-arryn · murder-of-the-old-high-septon
  (comparables settle it: planned killings are `assassination` — death-of-joffrey,
  assassination-of-tywin, shadow-assassination-of-renly; NOT `event.death`, which is
  the unproven/combat/natural bucket)
- `event.death` ×1: the-winterfell-murders (whodunit deaths, agency disputed — exact
  event.death territory)
- `event.war` ×7: war-of-the-ninepenny-kings · war-for-the-stepstones ·
  war-across-the-water · war-of-the-wolves · faith-militant-uprising ·
  jaehaerys-targaryens-uprising · peake-uprising (S207 precedent: the four Blackfyre
  rebellions went battle→war; armed risings are wars, not single battles)

## Held as-is (5 — pattern matched but content disagreed; deliberate, don't re-sweep)
- `abduction-of-lyanna` — retyping to `event.capture` would ASSERT the abduction
  reading of the central R+L ambiguity; `incident` is the neutral truth.
- `capture-of-loren-lannister` — node content models the bend-the-knee/Warden-of-the-
  West submission, not the battlefield capture.
- `remaking-of-the-small-council` — mass office-replacement (appointments), not a
  council session; `event.appointment` is singular-office shaped, so held at incident.
- `assault-on-lucinda-penrose` — personal attack, not a battle ("assault-on" regex
  over-match).
- `burning-of-the-seven-at-dragonstone` — iconoclastic act, not combat.

## Safety checks run
- Harm-gate interaction verified BEFORE applying: `war` is NOT in HARM_EVENT_SUBTYPES
  (`battle` is) — none of the 7 war-promotions carry VICTIM_IN; the 2 VICTIM_IN edges
  in scope (jon-arryn, yellow-dick) move INTO harm subtypes. No S208-P1-style flips.
- No hardcoded `event.incident`/`event.battle`/`event.war` filters in
  `graph/query/weirwood_query/`, `web/src/lib/`, or the index builder.
- Post-apply: fab-semantic-gate 4/4 PASS · pytest 1452+7skip · deno 100. Census:
  incident 306→301, battle 280→273, war 56→63, capture 44→46, assassination 28→30,
  death 216→217. All 22 live types remain sanctioned.

## Not in scope (noted for the future)
- The ~301 remaining `event.incident` nodes are content-ambiguous or genuinely
  incidents — a judgment-based LLM triage could squeeze more, but the deterministic
  tail is now closed.
- `remaking-of-the-small-council`-style mass-appointment events: if more accumulate,
  consider whether `event.appointment` should cover them or a disposition is needed.
