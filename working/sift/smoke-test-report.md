# Sift Stage 1 — Smoke Test Report (AGOT oaths lens)
*For Opus review. Date: 2026-06-27.*

## What ran
`python3 scripts/sift.py run --lens oaths --book agot`
Pure Python, no LLM. 73 AGOT chapters scanned.

## Results
- **116 pointers** emitted to `working/sift/oaths/agot.pointers.jsonl`
- **Runtime:** 0.18 s
- **Determinism:** ✅ byte-identical on two consecutive runs (sha256 matched)

## Trigger coverage (41 triggers)
26 triggered, 15 zero-hit.

Top hitters:
```
  32  'I swear'
  11  'take the black'
  10  'white cloak'
   9  'said the words'
   7  'bend the knee'
   5  'swear fealty'
   4  'say the words'
   4  'I vow'
   3  'knight of the Kingsguard'
   3  'taken the black'
   3  'on my honor'
   2  (each) 'the shield that guards the realms of men', 'the sword in the darkness',
             'the watcher on the walls', 'father no children', 'taking the black',
             'took the black', 'swore an oath', 'sworn sword', 'your liege', 'I pledge'
   1  (each) 'Night gathers, and now my watch begins', 'I shall take no wife',
             'you have my word', 'hold no lands', 'Arise, Ser'
```

Zero-hit triggers (15):
```
'one flesh, one heart, one soul'  'in the name of the Warrior'  'with this kiss I pledge'
'I do solemnly swear'  "your grace's man"  'take this woman'  'a guest beneath'
'eaten my bread'  'bread and salt'  'pledge fealty'  'take this man'  'under my roof'
'I am your man'  'do you swear'  'guest right'
```

## Noise / false-positive assessment

**`'I swear'` (32 hits) — expected to be noisy.** Many casual uses: threats, assurances, exclamations. Stage 2 Haiku exists precisely to filter these. Do not add exclusions before human review of the 32 rows.

**`'white cloak'` (10 hits)** — hits include Sandor wearing it as a costume detail, not oath invocations. Haiku call.

**`'said the words'` / `'say the words'` (13 hits combined)** — catches both vow-invocations and generic narration. Needs eyeball pass.

## Recall gaps worth noting

**`'guest right'`, `'bread and salt'`, `'eaten my bread'` — zero hits in AGOT.** This is *correct*: the guest-right drama is ASOS (Red Wedding). Good sanity check that the scanner is accurate, not misconfigured.

**`'do you swear'` — zero hits.** Knighting ceremonies and formal oath-taking use this phrase; may be a real recall gap vs. AGOT just not having them. Worth checking once the full corpus runs.

**Night's Watch vow (agot-jon-06:147):** Five triggers fire on the *same passage* — one ceremony, five pointer rows. Stage 2 deduplication by `cand_id` handles this by design.

## Likely graph edges hiding in the pointers

Even before Stage 2, these clusters are visible in the 116 rows:

1. **Jon's Night's Watch oath** (agot-jon-06:147) — 5 pointer rows, same passage. Clear SWORE_TO(jon-snow → night's-watch). Status: `sworn`.
2. **"take the black" references** (11 hits) — mix of: Jon himself taking it, Ned offered it by Joffrey (refused/overridden), Donal Noye backstory, Alliser Thorne context. At least 3–4 distinct oath-events.
3. **Joffrey ordering Ned to "take the black"** (agot-arya-05:161) — this is a *refused* / *overridden* oath: offered, not taken. An interesting `refused` status candidate.
4. **Catelyn / Frey negotiation** (agot-catelyn-09:185 `'swore an oath'`) — "You swore an oath to my father" / Frey waffling. Foreshadows the broken Frey pact. A `recalled` / context-of-betrayal pointer.
5. **Greatjon "your liege" / bares steel** (agot-bran-06:85) — fealty oath context; Greatjon then becomes Robb's champion. SWORE_FEALTY(greatjon → robb-stark) latent here.
6. **Roose Bolton "I vow"** (agot-catelyn-08:57) — casual use; probably a Stage 2 reject, but worth flagging.
7. **Ser Jared Frey "on my honor"** (agot-catelyn-09:165) — corroborates Walder Frey's claimed intent to march; another pre-Red-Wedding thread.

## Recommendation for Opus review

1. **Is the lexicon complete enough for AGOT?** Notably missing: `"as you love me"`, `"by the gods"`, `"I give you my word"`, `"keep faith"`. Check if these matter for the oath/loyalty spine.
2. **Should `'I swear'` stay as-is or get a tighter variant?** E.g., `"I swear to you"` is more oath-like than bare `"I swear"`. The spec says tune only after smoke test — this is the moment.
3. **The 15 zero-hit triggers in AGOT** — are they correct absences (guest right = ASOS) or gaps? Most look correct for book 1.
4. **Night's Watch vow multi-fire** — 5 triggers on one passage produces 5 rows with the same snippet. Stage 2 dedup by `cand_id` handles it, but worth confirming the design is right before running the full corpus (~400 chapters).
5. **Edge types latent in the data** — items 1–7 above suggest the oaths lens will produce edges: `SWORE_TO`, `BROKE_OATH_TO`, `OFFERED_OATH` (refused), `GRANTED_GUEST_RIGHT`. These are deferred per spec (edges layer frozen during enrichment track), but flagging so Opus can assess whether Stage 1 alone is worth committing to the worklog as a track.
