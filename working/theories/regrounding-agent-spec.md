# Theories wave 1 — residue re-grounding spec (S214)

> Contract for agents that ground the beats the deterministic matcher
> (`scripts/theories-reground.py`) could not. Input: one regrounding file
> (`working/theories/regrounding/<id>.jsonl`). You process every row whose
> `status` is `needs-agent`, `no-match`, or `ambiguous`. Output:
> `working/theories/regrounding-agent/<id>.jsonl`.

## Vocabulary (canonical)

Pass = big numbered corpus sweep · Track = named chunk of work (this is the
**Theories track**) · step (lowercase) = ordered piece inside a Track · **Tier =
confidence rating 1–5 ONLY, never for work/process**.

## The job

ASX (the video) is the *map*; the books are the *truth*. For each beat, find the
actual book passage in `sources/chapters/` that the beat points at, and return
its VERBATIM text + location. Never invent; never quote from memory — every
returned quote must be byte-copied from a chapter file you actually read.

Corpus layout: `sources/chapters/{agot,acok,asos,affc,adwd}/<book>-<pov>-<nn>.md`
plus D&E novellas `{thk,tss,tmk}/` and Fire & Blood `fab/`.

## Method (per beat)

1. Build 2–4 distinctive search phrases from `spoken_quote` (if present) and
   `paraphrase`. Prefer rare words/names over common ones.
2. Grep `sources/chapters/` (case-insensitive; try variants — curly vs straight
   apostrophes exist in the corpus).
3. Read the hit's surrounding lines. The passage must actually SAY what the
   beat claims — a name co-occurrence is not enough. If the beat is
   `ambiguous` (matcher found 2+ hits, listed in `hits`), pick the one whose
   context matches the beat and say why in `note`.
4. Byte-copy the passage's full line(s) exactly as printed (do not trim
   mid-sentence; 1–3 lines max).

## Output rows (JSONL, one per processed beat)

```json
{"beat_id": "rlj-B04",
 "status": "grounded" | "ungrounded",
 "file": "sources/chapters/agot/agot-eddard-09.md",
 "line": 39,
 "verbatim_quote": "<the exact line(s) from the chapter file>",
 "note": "<only when needed: ambiguity pick rationale, near-miss explanation, TWOW/semi-canon reason>"}
```

`ungrounded` is an honest and expected outcome (TWOW samples, wiki paraphrases,
show memories, ASX misattributions). Never force a weak match — a wrong cite is
worse than none. For `ungrounded` rows include a one-line `note` saying what you
tried.

## Anti-giveup contract (MANDATORY — added S219; the S216 jonsnow-p2 lesson)

Residue grounding has TWO recorded failure modes, and only one is machine-catchable:

1. **Invent** (S214): quoting from memory instead of the file. The deterministic
   byte-check (`scripts/theories-reground-repair.py`) catches every instance.
2. **Blanket-giveup** (S216 jonsnow-p2): the agent grounds its first few rows,
   then returns `ungrounded` for everything after. The byte-check CANNOT catch
   this — an ungrounded row has no quote to check. Only an orchestrator
   smell-test on the sequential-give-up pattern caught it.

Because mode 2 is invisible to the gates, these rules are part of the contract,
not advice:

- **≥2 logged grep attempts per `ungrounded` row.** The `note` must show the
  actual search patterns you ran (e.g. `note: "tried 'blue rose', 'wall of ice
  chink'; no hit"`). An `ungrounded` row without logged attempts is a contract
  violation and gets redone.
- **Famous-line calibration.** Iconic series lines ("You know nothing, Jon
  Snow", "Kill the boy…", "daggers in the dark") are near-certainly in the
  corpus. An `ungrounded` verdict on a famous line means YOUR SEARCH failed —
  retry with curly-vs-straight apostrophe variants, shorter sub-phrases, and
  rare-word anchors before giving up. (The S216 redo rescued 11 famous lines a
  giveup pass had marked ungrounded.)
- **Event-vs-interpretation distinction.** Ground the EVENT/PASSAGE the beat
  points at, not ASX's interpretation of it. If a beat is interpretive framing
  over an on-page scene, find and cite the scene; `ungrounded` is reserved for
  material with NO corpus referent (show-only, TWOW, community lore, GRRM
  interviews) — not for beats whose framing is speculative but whose underlying
  scene is right there in the text.

The deterministic byte-check outranks every agent verdict: a "grounded" row
whose quote fails the byte-check is a fail, whatever the agent claimed.

## Harvest rule (standing, applies while you're in chapter text)

If you stumble on a notable OFF-TASK find (a load-bearing quote, food/meal,
physical description, hospitality beat, foreshadowing), drop a one-line pointer
`chapter:line / kind / note` into `working/theories/harvest-s214-<id>.md`.
POINT, don't extract. Don't go looking — only capture what you trip over.

## Final message

Stats only: grounded / ungrounded counts + any systematic problem you noticed.
