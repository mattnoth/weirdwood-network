# Chat save / export — build plan

**Date:** 2026-07-11
**Track:** chat-UI (web/)
**Status:** Phase 1 SHIPPED S212 (2026-07-11, Matt-authorized autonomous build+deploy; hidden-attribute visibility pattern instead of the sketched body-class — repo convention; serializer proven by 14-assertion extraction test + live local flow check). Phase 2 (print-to-PDF) still awaiting its own green-light.
**Recommended model:** Sonnet (front-end JS, no deep reasoning)

## Ask

Let a visitor save their conversation with no login — download as a text/PDF
document. Floated by Matt: `.txt` or PDF.

## Scope

- **Phase 1 (recommended MVP): client-side Markdown download.** A "Save chat"
  button serializes the whole conversation (prose + the `chapter:line`
  citations embedded in each answer) to a `.md` file. No login, no backend, no
  dependencies.
- **Phase 2 (fast follow): print-to-PDF.** A print stylesheet + `window.print()`,
  so the OS dialog offers "Save as PDF."

Everything below is Phase 1 unless marked.

## Key facts that shape the design

| Fact | Source | Consequence |
|---|---|---|
| Page is served **raw** — `web/public/app.js` is not bundled | `netlify.toml` `publish = "web/public"` | Edit `app.js`/`app.css` directly; bump the `?v=194` cache-buster in `index.html` (lines 8-9, 125) |
| Conversation `history` is **capped at 8 and shifts** | `app.js:1118` `MAX_HISTORY = 8` | Can't export from `history` — early turns are gone. Need a separate **uncapped** log |
| Full record is in the **DOM thread** + the raw per-turn buffer | `app.js:1116`, `app.js:1435` `bot.finish()` returns `finalProse` | Capture `finalProse` (raw prose **with** `[[q\|…]]` markers) at turn completion |
| Answers embed citations as `[[q\|text\|speaker\|cite]]` markers | `app.js:284` `QUOTE_MARK_RE`, `app.js:267` `parseQuoteFields` | **Reuse** the existing regex + parser for export — don't reimplement |
| Deploy is manual, not git-push | `DEPLOY.md` + memory | Plan ends at "verified locally"; deploy is a separate Matt-run step |

## Phase 1 — build steps

### Step 1 — Capture an uncapped transcript (`app.js`, ~10 lines)

Add alongside `history` at `app.js:1117`:

```js
const transcript = []; // uncapped, export-only; separate from the 8-capped history
```

- In `ask()` after `app.js:1378`: `transcript.push({ role: "user", content: question });`
- In the `finally` block after `app.js:1435`, gated on `answered && finalProse.trim()`:
  `transcript.push({ role: "assistant", content: finalProse, persona });`
  (Capture `persona` per turn so the export labels each answer with the voice it
  was actually written under — matching the thread's behavior.)

### Step 2 — Pure serializer (`app.js`, ~35 lines) — `buildTranscriptMarkdown(transcript)`

- Header block: title, tagline, export date, the fan-project/attribution line
  from `index.html:114`, and the site URL.
- Per entry: a bold role label (`**You**` / `**The Loremaster**` /
  `**The Three-Eyed Raven**`), then the content run through a quote-marker
  converter.
- Quote converter reuses `QUOTE_MARK_RE` + `parseQuoteFields` to turn each
  `[[q|…]]` into a Markdown blockquote:

  ```
  > {text}
  > — {speaker}, {cite}
  ```

- No DOM access — a pure `string → string` function (unit-testable, can't break
  on render state).

Sketch:

```js
function buildTranscriptMarkdown(entries) {
  const lines = ["# The Weirwood Network — saved conversation", "",
    `*Exported ${new Date().toISOString().slice(0,10)} · https://<site>*`, "", "---", ""];
  for (const { role, content, persona } of entries) {
    const who = role === "user" ? "You"
      : persona === "bloodraven" ? "The Three-Eyed Raven" : "The Loremaster";
    lines.push(`**${who}:**`, "", proseToMarkdown(content), "");
  }
  lines.push("---", "", "A fan project · quotes © George R.R. Martin, used for commentary.");
  return lines.join("\n");
}
```

### Step 3 — Download trigger (`app.js`, ~8 lines) — `saveTranscript()`

`new Blob([md], { type: "text/markdown" })` → `URL.createObjectURL` → a
temporary `<a download="weirwood-chat-YYYY-MM-DD.md">` → `.click()` →
`revokeObjectURL`. Pure browser, zero deps.

### Step 4 — The button (`index.html` + `app.js` + `app.css`)

- Add a `Save` button in the header actions next to About (`index.html:24`) —
  always reachable, doesn't crowd the composer.
- Wire a click handler near the other wiring at `app.js:1472`.
- **Hidden until there's ≥1 assistant turn**, and disabled while `busy`
  (mid-stream). Toggle visibility where the landing class flips.
- Minimal CSS to match the About button's styling.

### Step 5 — Cache-buster + verify

- Bump `?v=194` → `?v=195` on `app.js` (and `app.css` if touched) in
  `index.html`.
- Verify against the **already-running** dev server on `:8766` (per memory —
  don't launch a second server; port collision). Ask 2 questions, click Save,
  confirm the `.md` opens with both turns, quote blocks, and cites intact. Test
  the edge cases below.

## Edge cases (all handled in Phase 1)

- **Empty chat** → button hidden, nothing to export.
- **Mid-stream** → button disabled while `busy`.
- **Family-tree answers**: the diagram is suppressed to a thin caption
  (`app.js:1149`); the export gets that caption text, not the SVG tree.
  Acceptable for a text format — add "diagram omitted" note only if wanted.
- **Incomplete trailing quote marker**: can't occur — we serialize `finalProse`
  (post-`finish()`), which is always complete.

## Phase 2 — print-to-PDF (separate green-light)

- Add `@media print` to `app.css`: hide header chrome, composer, and the
  receipts rail; render `.thread` full-width, quotes and cites styled for paper.
- Add a "Print / PDF" button that calls `window.print()`. The OS dialog handles
  "Save as PDF" and pagination — no library, ~1 day.

## Deliberately NOT in the MVP (Matt's call)

The right rail's **graph receipts** (chains walked, searches, themes) are richer
provenance than the in-prose cites, but they'd need a per-turn snapshot of the
`turn` object (reassigned each turn at `app.js:1381`) and they make the file
noisy — this was the earlier "option #3." Easy to bolt on later as a
`## Graph lookups` section per turn if the extra provenance is worth it for the
portfolio.

## Effort & footprint

- **~60 lines of JS, ~15 of HTML/CSS, one cache-bump.** No new files, no
  dependencies, no backend or edge-function changes.
- Half a day for Phase 1 including browser verification; another ~day for Phase 2.

## Open details (decide at build time unless Matt has a preference)

- Button placement — planned: header, next to About.
- Filename format — planned: `weirwood-chat-2026-07-11.md`.
