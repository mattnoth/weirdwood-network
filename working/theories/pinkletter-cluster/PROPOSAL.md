# Pink Letter authorship cluster — proposal (S216)

**Session:** theory-cluster proposer pass (Pink Letter authorship).
**Graph mutation: NONE.** All files under `working/theories/pinkletter-cluster/`.
Cluster is STAGED at the mint gate only — no mint without Matt's explicit go
(standing rule from S214).

## Structural decision: ONE node, five authorship candidates + one entangled sub-question

The source video (`T-j01uhSdGo`) frames a single question ("is Stannis dead,
and did Ramsay really write this letter") that decomposes into six sub_claims
in the extraction substrate: five competing authorship candidates (Ramsay,
Mance, Stannis, Melisandre+Mance, Barbrey Dustin/Wyman Manderly) plus a
distinct-but-tightly-interwoven claim that Stannis is still alive via a
false-beacon/frozen-lake trap. This matches the existing stub's scope
(`bastard-letter-theories`) and the video's own single-theory framing
(`theory_name: "Pink Letter authorship"`), so this is ONE enrich, not a
node-per-candidate split — the same shape decision Hooded Man made for its
identity-vs-murderer threads, generalized to five candidates instead of three.

The "Is Stannis Really Dead?" thread earns its own subsection (not folded to
premise/event-layer prose) because, unlike Hooded Man's murderer-identity
thread, **no event node yet covers this material** — a false-beacon battle at
the frozen lake has not happened on the page. It is genuinely unresolved,
forward-looking theory content, not a restatement of settled fact. The one
adjacent fact that IS already event-layer (Stannis's camp being snowbound and
starving) is pointed at via the live `stannis-s-army-stalls-at-crofters-village`
event node rather than re-argued from scratch, and two of its scene-detail
quotes (watchtower beacon; frozen lake ice-holes) are reused as the anchor for
the theory's own predictive synthesis (PL10, PL11) — the same subject-link
reuse pattern GNC's G1 and Hooded's H11 established.

No new node minted — see below for why an "Asha Greyjoy authorship" candidate,
suggested as a possibility in the task brief, does not appear: the actual
substrate (65 beats, ASX's own sub_claims list) contains no such candidate.
Asha appears only as the addressee of an earlier, non-Pink Letter comparison
letter used for the wax-seal style contradiction (PL1) — a Barbrey
Dustin/Lady Dustin correspondence, not an Asha-authorship claim. I did not
invent a candidate the source material doesn't carry.

## Node

`enrich/bastard-letter-theories.node.md` — stub rewrite. Slug/wiki_source/
bucket_id/prompt_version preserved; `node_version` 1→2; `pass_origin` set to
`theories-wave1-s216`. Display name changed to a question — **"Who Wrote the
Pink Letter?"** — following the S216 Hooded Man precedent for genuinely
multi-candidate theories, flagged for the same pending ratification (the
video does lean toward a preferred answer, Ramsay, so this is a softer case
for question-form than Hooded's genuinely-unresolved whodunit — noted
explicitly in the node's own Status Notes for Matt's call).
`confidence: tier-4` at the node level (five candidates, one with zero
grounded edges, plus an entangled unresolved sub-question — comparable
compounded uncertainty to Hooded Man's tier-4). `status: open` (never
show-depicted at all — GoT has no Pink Letter equivalent — never book-resolved
as of ADWD's end).

## Edges — 11 total (candidates.json)

| id | type | source | tier | what |
|---|---|---|---|---|
| PL1 | CONTRADICTS | ramsay-snow | 3 | earlier Ramsay letter: wax "button" baseline |
| PL2 | CONTRADICTS | bastard-letter | 3 | Pink Letter's wax "smear" — breaks the baseline |
| PL3 | CONTRADICTS | bastard-letter | 4 | wildling hostage demands don't fit Ramsay alone |
| PL4 | SUPPORTS | mance-rayder | 3 | Mance's confirmed lying pattern (Horn of Winter) |
| PL5 | SUPPORTS | mance-rayder | 4 | Abel/Mance discusses Stannis's position with Theon |
| PL6 | CONTRADICTS | mance-rayder | 3 | Mance: "my people have bled enough" — motive problem |
| PL7 | SUPPORTS | melisandre | 4 | Melisandre orchestrated Mance's Winterfell mission |
| PL8 | SUPPORTS | barbrey-dustin | 4 | Barbrey personally leads Theon into the crypts |
| PL9 | SUPPORTS | davos-seaworth | 4 | false-beacon precedent (Sistermen wrecking-lights) |
| PL10 | SUPPORTS | stannis-s-army-stalls-at-crofters-village | 4 | Stannis's camp watchtower beacon |
| PL11 | SUPPORTS | stannis-s-army-stalls-at-crofters-village | 4 | frozen lake, ice already cut/dangerous |

7× SUPPORTS, 4× CONTRADICTS. Tiers: 4× tier-3, 7× tier-4. No tier-1/2
anywhere. All 11 quotes independently byte-verified against
`sources/chapters/` at the cited lines (Python exact-substring check across
both `candidates.json` and the node body's own blockquotes — both checked,
not just the edges file).

## Source-node verification

All 11 edge-source slugs resolve to live node files: `ramsay-snow` (alias
"Ramsay Bolton" — the character node's actual slug is `ramsay-snow`, NOT
`ramsay-bolton`; the live `bastard-letter`/`pink-letter-delivered` event/
artifact nodes both link to a `ramsay-bolton` slug internally, which does not
exist as a file — flagging this as a pre-existing dangling link in the live
graph, out of scope for this staging pass to fix, but worth a future graph
health-check note), `bastard-letter` (artifact), `mance-rayder` (alias
"Abel" — confirmed in the node's own frontmatter), `melisandre`,
`barbrey-dustin`, `davos-seaworth`, `stannis-s-army-stalls-at-crofters-village`
(event). No fabricated slugs.

## A finding: two "grounded" substrate rows didn't actually support their claim

The regrounding-agent pipeline marked pinkletter-B47 and pinkletter-B48
(both citing the same Roose Bolton war-council passage in
`adwd-theon-01.md:75`) as `status: grounded` for the Stannis-letter-faker
candidate's claim that "Stannis has captured a Bolton maester" who could
forge the letter. On independent inspection, the cited passage is Roose
Bolton ordering an attack on Stannis's snowbound, starving host — it
confirms Stannis's dire situation (already established elsewhere, e.g. B02/
B04, and already owned by the live tier-1 event node
`stannis-s-army-stalls-at-crofters-village`) but says nothing about a
captured maester. This is a smaller-scale version of the Hooded cluster's
Harwin mislocation finding: not a hallucinated citation (the quote is real
and does exist at that line), but a mismatch between what the row claims to
ground and what the passage actually establishes. Both rows are excluded
from edges; the Stannis-letter-faker candidate is carried entirely as
premise/backstory prose and earns zero edges (documented in both the node's
Ungrounded material and its own Evidence For subsection).

## Byte-verification note: 11 of 22 candidate rows needed curly-quote repair

Of the 22 `status: grounded`/`matched` rows in the substrate (20 from
`regrounding-agent/T-j01uhSdGo-p1.jsonl` + `-p2.jsonl`, 2 from
`regrounding/T-j01uhSdGo.jsonl`), 11 initially failed a naive exact-substring
check against `sources/chapters/`. All 11 failures were the same class of
error flagged in this session's brief (straight quote marks `'`/`"` in the
JSONL transcription versus curly `'`/`"`/`"` in the actual source text) —
none were content mismatches or mislocations. All 11 were re-copied
byte-exact from the source file at the cited line before use. Final
candidates.json + node body: 11/11 and 11/11 ALL FOUND respectively (checked
separately, since only 11 of the 22 available grounded rows were selected for
edges — see below for what was held out).

## Held-out material (Ungrounded, fenced in the node body)

- **community** — Ramsay's tone/cruelty personality-fit reasoning (sub_claims
  B16/B17/B19/B22/B24/B25/B27) — mostly ungrounded by the regrounding agent;
  the one grounded quote in this space (B18, the letter's own heart-cut
  threat) is already fully quoted on the live `bastard-letter` artifact node
  and adds little beyond what PL1–PL3 already carry, so it's referenced in
  prose rather than re-edged.
- **grrm-interview** — GRRM's stated intent to show Stannis's Winterfell
  battle in a future book (B03).
- **book-interpretive (regrounding failure)** — B47/B48 (see finding above).
- **community** — Three Mance-candidate language-parallel beats (B33 "red
  witch"/recent-dialogue echoes, B34 "burned for all the world to see" vs. the
  letter's actual "for all the north to see", B35 opportunity-to-learn-
  household-detail) — all `status: ungrounded`. B34 in particular looks like
  the video's own misquote/conflation, flagged explicitly in the node.
- **community** — Melisandre's specific foresight-of-the-letter and
  engineering-Jon's-death claims (B54, B56, B58) — technically `grounded` in
  the substrate but, on inspection, only loosely adjacent to the specific
  claims they were graded against (see node Ungrounded material for detail);
  not re-edged.
- **community** — Barbrey Dustin's introduction scene (B59) — grounded but
  atmospheric (Roose's "hint of fear" reaction), doesn't establish Barbrey's
  motive; not edged per the no-atmosphere-edges hard rule.
- **community** — Mance+Melisandre co-authorship motive "unclear" per the
  video itself (B55); Melisandre foreseeing Jon's resurrection (B57);
  Barbrey/Manderly crypt intrigue as "probably unrelated" (B61/B62) — all
  explicit video-side hedges, not textual claims.
- **community (wordplay)** — "Abel" as an anagram of Bael the wildling raider
  (B43).
- **video-synthesis** — the video's own closing verdict (B63, B64, B65) —
  captured in Status Notes, not re-edged.
- **not independently row-verified but self-checked** — the "Cut so many
  holes in the ice it's a bloody wonder more haven't fallen through" line
  (adwd-the-sacrifice-01.md:172), referenced only inside B09's substrate
  *note* field rather than as its own graded row. I independently opened and
  byte-checked it (it's real and at that line) since it materially
  strengthens the frozen-lake danger premise, but per the hard rule that
  quotes come only from formally graded rows, I carried it as prose detail
  rather than minting a 12th edge from it.

## Open questions for orchestrator/Matt adjudication

1. Question-form display name, softer case than Hooded Man's (this video does
   lean toward a preferred answer — Ramsay). Confirm as within the same
   ratified convention, or should a video with a stated preferred verdict get
   a declarative name (R+L=J-style) even with multiple live candidates?
2. PL10/PL11 source the live event node `stannis-s-army-stalls-at-crofters-village`
   directly (subject-link reuse of its own scene detail) rather than a
   character node — same typing question Hooded's H11 and GNC's G1 raised:
   confirm this is the right convention for "confirmed event detail repurposed
   as theory-layer predictive evidence," distinct from H11/G1's "confirmed
   event fact contradicts/anchors a theory claim" usage.
3. The dangling `ramsay-bolton` slug referenced by the live `bastard-letter`
   and `pink-letter-delivered` nodes (should be `ramsay-snow`) — flagged, not
   fixed, since it's outside this staging pass's scope (no graph mutation).
   Worth a future graph-health-check ticket.

## HARVEST

- `sources/chapters/adwd/adwd-jon-13.md:227` / dialogue+narration / Jon:
  `"You were right to come at once," Jon said.` followed by the narration
  `You were right to be afraid.` — Jon's own dread reading the letter's
  address line before opening it; strong standalone material for `jon-snow`
  node prose, not used here (off-topic for authorship).
- `sources/chapters/adwd/adwd-the-sacrifice-01.md:172` / dialogue / Ned Woods:
  `"Cut so many holes in the ice it's a bloody wonder more haven't fallen
  through. Out by the island, there's places look like a cheese the rats been
  at."` — vivid, quotable description of the frozen lake's danger; verified
  in this pass (see above), a clean quote for a future `stannis-s-army-stalls-at-crofters-village`
  enrichment or for `the-sacrifice` chapter-level description work.
- `sources/chapters/adwd/adwd-theon-01.md:33` / narration / Theon: `Dead is
  dead. Better dead than Reek.` (a few lines before the Rowan/Abel handoff
  passage used in PL5's chapter) — sharp, quotable Theon interiority; not
  used here, good `theon-greyjoy` node candidate.
