# Theories wave 1 — transcript extraction spec (S214)

> Contract for the per-video extraction agents. Input: one cleaned ASX transcript
> (`working/theories/videos/transcripts-clean/<id>.txt`). Output: one JSONL file
> (`working/theories/extractions/<id>.jsonl`). The downstream re-grounding step
> matches every beat against OUR book corpus — ASX is the *map*, the books are the
> *truth*. Nothing mints on the video's authority alone.

## Vocabulary (canonical — use these words)

Pass = big numbered corpus sweep · Track = named chunk of work (this is the
**Theories track**) · step (lowercase) = ordered piece inside a Track · **Tier =
confidence rating 1–5 ONLY, never for work/process**. Theories are Tier 3–5 always.

## Output format

JSONL — one JSON object per line. Line 1 is the theory header; every following
line is one beat.

### Line 1 — theory header (`"kind": "theory"`)

```json
{"kind": "theory",
 "video_id": "kHqzFwodZqQ",
 "video_title": "R+L=J: who are Jon Snow's parents?",
 "channel": "Alt Shift X",
 "theory_name": "R+L=J",
 "claim": "<ONE falsifiable sentence stating the theory as the video presents it>",
 "sub_claims": ["<numbered distinct sub-claims or competing variants the video weighs>"],
 "asx_verdict": "<how confident the video says the theory is, in one sentence, if stated>",
 "notes": "<anything structural worth knowing: covers 2 theories, mostly show-based, etc.>"}
```

If the video genuinely adjudicates MORE THAN ONE distinct named theory (not
variants of one), emit an additional `"kind": "theory"` line for each, and tag
beats with `"theory": "<theory_name>"`.

### Beat lines (`"kind": "beat"`)

One line per discrete piece of evidence or counter-evidence the video cites.
Be exhaustive — a typical ASX video walks 10–40 beats. Do NOT merge distinct
beats; do NOT add evidence you know from outside the video.

```json
{"kind": "beat",
 "beat_id": "<video-id-prefix>-B01",
 "stance": "supports" | "contradicts",
 "sub_claim": <index into sub_claims, or null if it bears on the main claim>,
 "paraphrase": "<the evidence in one or two sentences, as the video presents it>",
 "source_domain": "book" | "dunk-egg" | "twoiaf" | "fab" | "show" | "grrm" | "community" | "unknown",
 "book_hint": "<whatever location the video gives: book name, POV, chapter, scene — or null>",
 "spoken_quote": "<the exact words ONLY where the narrator is clearly quoting book text verbatim, else null>",
 "quote_speaker": "<in-world speaker of the quoted line, if identifiable, else null>",
 "strength_as_presented": "strong" | "moderate" | "weak"}
```

## Rules

1. **Video-faithful only.** Extract what THIS video asserts. Your own knowledge of
   the theory is off-limits (it contaminates re-grounding). If the video is wrong
   about a detail, extract it wrong — re-grounding catches it.
2. **`spoken_quote` discipline.** Only fill it when the transcript is clearly
   reading/quoting the text (signals: "quote", "Martin writes", "she says",
   verbatim archaic phrasing). Spoken quotes may differ slightly from the printed
   line — copy the transcript's words exactly; do not "fix" them toward the book.
   **Contiguous transcript words ONLY — never insert `[...]`, `[himself]`-style
   bracket edits, or stitched ellipses** (they defeat the downstream matcher).
   If the narrator interleaves commentary mid-quote, capture the longest
   contiguous verbatim run (or the best single run if several).
3. **`source_domain` matters.** Beats groundable in our chapter corpus =
   `book` (AGOT/ACOK/ASOS/AFFC/ADWD) / `dunk-egg` / `fab`. Show-only evidence =
   `show` (kept, but it can never re-ground — books are the truth layer).
   GRRM interviews/SSM = `grrm`. TWOIAF = `twoiaf`. Community artifacts (essays,
   forum history) = `community`.
4. **Counter-evidence is first-class.** ASX always weighs objections — capture
   every one as `"stance": "contradicts"`.
5. Final message: 3–4 lines of stats only (beats by stance/domain, quotes
   captured, anything malformed about the transcript). No prose recap.
