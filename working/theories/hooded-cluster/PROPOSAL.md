# Hooded Man cluster — proposal (S216)

**Session:** theory-cluster proposer pass (Hooded Man / Winterfell murders).
**Graph mutation: NONE.** All files under `working/theories/hooded-cluster/`.
Cluster is STAGED at the mint gate only — no mint without Matt's explicit go
(standing rule from S214).

## Structural decision: ONE node, not two

The source video (`36Ntv75CfqE`) carries two theory headers — "Hooded Man
identity" and "Winterfell murderer identity" — but they do not warrant separate
canonical theory nodes. Reasons:

1. **The murderer-identity thread is almost entirely event-layer, not theory-layer.**
   The live graph already has `graph/nodes/events/the-winterfell-murders.node.md`
   (tier-1, minted S149) which states as confirmed fact that Mance Rayder/Abel's
   spearwives (incl. Rowan) committed the killings of Yellow Dick, the Ryswell
   groom, and the Frey squire, with `SUSPECTED_OF` edges already live for
   `mance-rayder` and `rowan` (tier-2) and `theon-greyjoy` (tier-1, exonerated).
   The event node's own text already states "The murder of Little Walder Frey is
   the one death the spearwives explicitly disclaim — it remains a genuine open
   mystery," which is exactly where the video's Big Walder accusation adds real,
   ungrounded-elsewhere content (edge H12). Everything else the video argues for
   the murderer thread (wildlings did it, Flint was an accident, Little Walder is
   the odd one out) duplicates the tier-1 node rather than adding a genuinely
   *theoretical* (unconfirmed, contested) claim — so per the LAYER RULE it stays
   premise prose pointing at the event node, not a parallel theory node.
2. **The video itself treats the murderer-identity thread as subordinate** — its
   own framing is that solving "who's the killer" (confidently, in-video) is the
   necessary first step to clear the ground for the real open question, "who/what
   is the Hooded Man." Minting a second theory node for a thread the video itself
   doesn't present as an unresolved mystery would misrepresent its own argument
   structure.
3. **The only genuinely open, unconfirmed, multi-candidate identity question is
   the Hooded Man himself** — three named human candidates (Robett Glover,
   Harwin, Hallis Mollen) plus two non-literal readings (ghost/hallucination of
   Theon's former self; the Stranger/death), explicitly unresolved by both the
   text and the video ("maybe it doesn't matter who's under the hood").

**Shape chosen:** one enrich of the existing `hooded-man-theories` stub. The
Hooded Man identity claim is the node's primary claim; the murderer-identity
material is a `### The Winterfell murderer identity (event-layer premise)`
subsection under Evidence For that (a) points at `the-winterfell-murders` as the
confirmed substrate via a CONTRADICTS-scoped subject-link edge (H11, mirroring
the GNC cluster's G1 retarget precedent), and (b) carries the one genuinely new
claim (Big Walder killed Little Walder) as its own SUPPORTS edge (H12).

## Node

`enrich/hooded-man-theories.node.md` — stub rewrite. Slug/wiki_source/bucket_id/
prompt_version preserved; `node_version` 1→2; `pass_origin` set to
`theories-wave1-s216`. Display name changed to a question — **"Who is the Hooded
Man of Winterfell?"** — a deliberate departure from the R+L=J/KotLT convention of
a declarative claim-name, because this theory (unlike those two) does not
converge on a single answer; both the corpus and the source video's own verdict
are genuinely split three-plus-ways. `confidence: tier-4` at the node level
(weaker than KotLT's tier-3, reflecting the compounded uncertainty of an
unresolved multi-candidate whodunit with heavy symbolic content), with honest
per-edge variance (tier-2 through tier-4) inside. `status: open` (never
show-depicted, never book-resolved).

## Edges — 12 total (candidates.json)

| id | type | source | tier | what |
|---|---|---|---|---|
| H1 | SUPPORTS | theon-greyjoy | 3 | core encounter — "Theon Turncloak. Theon Kinslayer." |
| H2 | SUPPORTS | rowan | 3 | Rowan's own "kinslayer" epithet — shared vocabulary chain |
| H3 | SUPPORTS | rowan | 4 | "Lord Eddard's words" — Stark-sympathy inference |
| H4 | SUPPORTS | mors-umber | 4 | Crowfood's daughter taken by wildlings — Rowan-ID chain |
| H5 | SUPPORTS | robett-glover | 3 | present in Manderly's anti-Bolton conclave |
| H6 | SUPPORTS | hallis-mollen | 4 | real Ned's-bones escort mission (arrival unconfirmed) |
| H7 | CONTRADICTS | hallis-mollen | 3 | "a loose tongue" — poor fit for covert operative |
| H8 | SUPPORTS | ygritte | 4 | "gods hate kinslayers, even when they kill unknowing" |
| H9 | SUPPORTS | theon-greyjoy | 3 | miller's boys passed off as Bran/Rickon (confirmed) |
| H10 | SUPPORTS | theon-greyjoy | 3 | Theon's own suspicion + "not afraid" (Stranger reading) |
| H11 | CONTRADICTS | the-winterfell-murders | 2 | event-node subject-link; scoped to "HM = the murderer" only |
| H12 | SUPPORTS | walder-frey-son-of-jammos | 3 | Big Walder's blood-caked gloves — Little Walder's real killer |

9× SUPPORTS, 2× CONTRADICTS(scoped), 1× CONTRADICTS(layer-link). Tiers: 1×
tier-2, 6× tier-3, 5× tier-4. All 12 quotes independently byte-verified against
`sources/chapters/` at the cited lines (Python exact-substring check, not just
trusting upstream regrounding status — see below).

## Source-node verification

All 12 edge-source slugs resolve to live node files: `theon-greyjoy`, `rowan`,
`mors-umber` (alias "Crowfood"), `robett-glover`, `hallis-mollen`, `ygritte`,
`the-winterfell-murders` (event), `walder-frey-son-of-jammos` (alias "Big
Walder"). No fabricated slugs.

## A finding: three "grounded" substrate rows were actually mislocated

The regrounding-agent pipeline (`working/theories/regrounding-agent/36Ntv75CfqE-p1.jsonl`)
marked beats hooded-B33, B34, B35 (Harwin candidate backstory: Ned assigning
"the boys" to Harwin's care; Arya recognizing Harwin at the Brotherhood; Sam
searching for a "loose-tongued" Dareon) as `status: byte-fail` with a
`"repair": "not-in-corpus-or-ambiguous"` tag. Per the hard rule (quotes only
from grounded rows), these were already excluded on status alone — but I
independently opened all three cited files/lines to see what was actually
there, since Harwin losing all three of his candidate-establishing quotes is a
significant gap worth confirming rather than assuming. Result: **none of the
three cited passages mentions Harwin at all** — B33's line is a wet-nurse scene
in `agot-eddard-09.md`, B34's is the Jaqen H'ghar prophecy scene in
`acok-arya-09.md`, and B35's is Sam searching Braavos for Dareon in
`affc-samwell-03.md`. The `byte-fail` status was correct to block them; the
underlying beats were essentially hallucinated citations, not near-misses. As a
result, **Harwin — one of the video's three named human candidates — has zero
grounded textual support** in this pass and carries no edges; he's held as
premise/backstory prose only. This is flagged explicitly in the node's
Ungrounded material section as an open gap, not silently dropped.

## Held-out material (Ungrounded, fenced in the node body)

- **community** — Blackfish/Benjen as undeveloped fan candidates (video doesn't
  elaborate).
- **book-interpretive** — "identity doesn't matter" northman-symbol reading; the
  "north remembers" quote used to support it is real but is Robb Stark speaking
  about Karhold, not about the Hooded Man — re-quoted in full context, not edged.
- **community** — Shakespearean-ghost (Hamlet/Macbeth) literary comparison.
- **community (speculative)** — miller's-boys-as-Theon's-actual-sons; explicitly
  hedged thin by the source video itself.
- **not-groundable (synthesis)** — the video's own "murder mystery solved"
  wrap-up paragraph and its Jon/Melisandre motive-reasoning are its synthesis of
  facts the tier-1 event node already owns, not new textual beats.
- Robett-knows-Bran/Rickon-are-alive counter-evidence and the
  Harwin-recognition-problem rebuttal are both kept as **prose-only premise** in
  Evidence Against (real arguments from the video, but not independently
  groundable to a specific quote beyond what H5/H1 already establish).

## Open questions for orchestrator adjudication

1. Is the CONTRADICTS-scoped-to-a-sub-claim treatment of H11 (event node →
   theory node) the right typing, or should it be SUPPORTS (the confirmed fact
   anchors/enables the rest of the theory, GNC G1-style) instead of CONTRADICTS
   (it specifically rules out one sub-claim)? I chose CONTRADICTS because the
   sub-claim it defeats ("the Hooded Man is the murderer," hooded-B17) is a live
   claim in the source extraction, not scaffolding — but this is a judgment call
   worth a second look, same as the R+L=J T7-scoping caveat Matt already
   accepted for that cluster.
2. Node-level `confidence: tier-4` vs tier-3 — is compounding "no single named
   candidate confirmed" into a lower node tier than KotLT (tier-3, ~70%
   "probably Lyanna") the right call, or should node tier stay tier-3 with the
   spread expressed only in per-edge variance? Both R+L=J and KotLT are tier-3.
3. Claim-style display name as a question ("Who is the Hooded Man of
   Winterfell?") breaks from the R+L=J/KotLT declarative-claim convention
   on purpose (see Node section) — confirm this is an acceptable exception
   rather than a drift to patch.

## HARVEST

- `sources/chapters/adwd/adwd-a-ghost-in-winterfell-01.md:189` / dialogue / Roger
  Ryswell: `"If not him, who? Stannis has some man inside the castle, that's
  plain."` — in-world voicing of the "spy inside Winterfell" suspicion; not used
  as an edge here (interpretive/redundant with the event-layer premise already
  cited) but a clean quote if a future pass wants to attach it to
  `the-winterfell-murders` or `roger-ryswell` directly.
- `sources/chapters/adwd/adwd-theon-01.md:229` / narration / Theon: `"In songs,
  the hero always saved the maiden from the monster's castle, but life was not a
  song, no more than Jeyne was Arya Stark. Her eyes are the wrong color. And
  there are no heroes here, only whores."` — strong stand-alone quote about
  Theon's disillusionment during the escape; the regrounding-agent had
  mis-attached this to the Harwin candidate (no such connection in the text) but
  it's a good homeless quote for `theon-greyjoy` node prose on its own merits.
- `sources/chapters/adwd/adwd-the-prince-of-winterfell-01.md:55` / description /
  Theon: `"He had never seen the godswood like this, though—grey and ghostly,
  filled with warm mists and floating lights and whispered voices that seemed to
  come from everywhere and nowhere."` — atmospheric godswood description, not
  used as an edge (interpretive-only beat) but notable descriptive-depth
  material per the standing "physical descriptions are first-class extraction
  targets" design value.
