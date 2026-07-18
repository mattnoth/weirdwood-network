---
name: "Who is Coldhands?"
type: concept.theory
slug: coldhands-theories
aliases:
  - "Who is Coldhands"
  - "Coldhands identity theory"
  - "Coldhands reanimation theory"
  - "who was Coldhands before he died"
claim: "Coldhands — the mysterious ranger who guides Sam and Gilly, then Bran's group, to the three-eyed crow — is a dead man reanimated by the old gods' nature magic, most likely by Brynden Rivers (Bloodraven); several candidate identities for who he was before he died have been proposed (Benjen Stark, Will or Waymar Royce, Ser Duncan the Tall, the legendary Night's King, a Night's King/Other hybrid), but none is confirmed in the published books and the text deliberately keeps the mystery open."
confidence: tier-4
status: open
wiki_source: "https://awoiaf.westeros.org/index.php/Coldhands/Theories"
origin: "ASOIAF fan community; two linked strands — a reanimation-mechanism synthesis (nature magic vs. the Others' ice magic vs. Thoros/Beric's fire magic) and a cluster of named identity-candidate sub-theories (Benjen Stark, Will/Waymar Royce, Ser Duncan the Tall, the Night's King, a Night's King/Other hybrid)"
video_sources:
  - {channel: "Alt Shift X", id: "Ge6VduBUJFo", title: "Who is Coldhands?", transcript: "working/theories/videos/transcripts-clean/Ge6VduBUJFo.txt"}
bucket_id: tier3-pathb-longtail
prompt_version: v1-python
node_version: 2
pass_origin: theories-wave1-s216
---

## Claim

The theory holds that Coldhands — the cloaked ranger who saves Samwell Tarly and
Gilly from wights in the haunted forest, and who later guides Bran Stark's party
north to the cave of the three-eyed crow — is a dead man, reanimated not by the
Others' ice magic but by a distinct nature magic associated with the old gods, most
likely at the hand of Brynden Rivers (Bloodraven) and the children of the forest. A
linked, more speculative extension holds that Bloodraven may at times skinchange
directly into Coldhands, the way Bran later controls Hodor — though the theory itself
treats this as unlikely to be constant, since Coldhands plainly acts and speaks as his
own person. Separately from the *what*-is-Coldhands question, the theory surveys
several candidate answers to *who* Coldhands was before he died — Benjen Stark, Will
or Waymar Royce, Ser Duncan the Tall, the legendary Night's King, and a hybrid
descendant of the Night's King and an Other — and finds none of them convincing; the
identity question is presented as a real, deliberately-unresolved mystery rather than
a puzzle with a hidden textual answer.

**Relationship to the existing tier-1 character node.**
[`coldhands`](../../../../graph/nodes/characters/coldhands.node.md) already carries,
as settled tier-1/tier-2 fact, most of Coldhands's physical description (black cold
hands, pale face, boiled leather and ringmail, black wool scarf), his command of
ravens, his eyes being black rather than the light blue of wights' eyes, Summer's
dislike of his smell, and his edges `SERVES`/`SWORN_TO` Brynden Rivers, `DIED_AT`
Beyond the Wall, `RESCUES` Samwell Tarly and Gilly, `PROTECTS`/`REVEALS_TO` Bran's
party, and `AGENT_IN` the Black Gate and cave-approach events. None of that is
reargued here as theory evidence — it is the premise the theory builds on. What the
tier-1 node does **not** settle, and what this theory node exists to hold, is (1) the
*mechanism* by which Coldhands was reanimated (nature magic, as one reading among
several possible undeath-mechanisms attested in the books) and (2) *who Coldhands
was in life* — a question the character node leaves entirely open, consistent with
the text.

## Evidence For

### What Coldhands is: a distinct kind of reanimated dead man

The mystery starts with the fact that Coldhands never gives his own name — Sam
coins the nickname from the one physical detail that will not stay hidden:

> Coldhands was the name that the fat boy Sam had given him, for though the
> ranger's face was pale, his hands were black and hard as iron, and cold as iron
> too.
— sources/chapters/adwd/adwd-bran-01.md:19 (edge C1, node coldhands)

He commands the raven flock that serves as his eyes and ears — a power the theory
reads as sharing something with the greenseers among the children of the forest,
who likewise perceive through animals and weirwoods:

> Some would fly to the ranger and mutter at him, and it seemed to Bran that he
> understood their quorks and squawks. They are his eyes and ears. They scout for
> him, and whisper to him of dangers ahead and behind.
— sources/chapters/adwd/adwd-bran-01.md:29 (edge C2, node coldhands)

When his elk finally collapses from exhaustion, Coldhands performs what the theory
reads as a small rite of the old gods rather than simple practicality:

> Coldhands had knelt beside it in the snowbank and murmured a blessing in some
> strange tongue as he slit its throat.
— sources/chapters/adwd/adwd-bran-02.md:65 (edge C3, node coldhands)

The theory's central comparative argument is that Coldhands is dead but is *not* an
ordinary wight of the kind the Others raise. The clearest textual contrast is eye
color: wights encountered fighting outside the cave of the three-eyed crow are
explicitly blue-eyed —

> All of them had pale flesh and black hands. Their eyes glowed like pale blue
> stars.
— sources/chapters/adwd/adwd-bran-02.md:93 (edge C4, node wights)

— against Coldhands's own black eyes (already recorded on the `coldhands` node
itself, not re-quoted here as a separate edge). A second contrast is his visible
aversion to fire, which the theory reads as a residual wight-vulnerability even
though he is otherwise unlike a standard wight:

> Reflections from the flames glittered off four black eyes. He does not eat, Bran
> remembered, and he fears the flames.
— sources/chapters/adwd/adwd-bran-01.md:185 (edge C5, node coldhands)

Most strikingly, Coldhands is capable of calm, self-aware, clinical reflection on
his own condition — a degree of retained personhood and intelligence the theory
treats as incompatible with the mindless wights the Others raise:

> "Once the heart has ceased to beat, a man's blood runs down into his extremities,
> where it thickens and congeals."
— sources/chapters/adwd/adwd-bran-01.md:201 (edge C6, node coldhands)

**The Thoros/Beric fire-magic parallel (book-interpretive, not independently
grounded this pass).** The video's core explanatory model is that just as the
Others reanimate wights with ice magic, and Thoros of Myr repeatedly restores Beric
Dondarrion to life through R'hllor's fire magic, Bloodraven may be reanimating
Coldhands through a third, nature-magic channel tied to the old gods and the
weirwoods — making all three "kinds of zombie" variations on the same underlying
phenomenon. This is a structural comparison across widely separated parts of the
books (Beric/Thoros material lives outside this session's search coverage) rather
than a single citable passage, and is not represented as an edge.

## Evidence Against

**No book text shows Coldhands's own reanimation, or any prior identity, stated
outright.** The strongest textual fact working against every specific identity
candidate is the same one that makes the mystery a mystery: nothing in the five
published books names who Coldhands was before he died. The clearest per-candidate
counter-evidence this pass could ground concerns the Will/Waymar Royce candidate.
Both men die at the Others' hands in the Prologue of *A Game of Thrones*, and what
the text shows happening to them afterward is the ordinary Other-to-wight
transformation, not anything resembling Coldhands's retained self-awareness:

> The watchers moved forward together, as if some signal had been given. Swords
> rose and fell, all in a deathly silence. It was cold butchery.
— sources/chapters/agot/agot-prologue.md:213 (edge C7, node waymar-royce,
CONTRADICTS)

The passage itself only depicts the killing, not any subsequent restoration of
mind or self — and the Prologue's closing image shows what a standard Other-kill
actually produces: The right eye was open. The pupil burned blue. It saw.
(agot-prologue.md:227 — narration; Waymar risen as a blue-eyed wight, mindless, no
retained self). That is exactly the theory's point: nowhere in the Prologue, or
anywhere else in the corpus searched this pass, is a wight's mind ever shown being
restored after the Others take it. If Waymar or Will became Coldhands,
the text would need to explain how a standard Other-kill-and-raise became something
categorically different soon after; it does not.

Separately, the identity mystery is itself treated as deliberate and unresolved
within the story — Meera Reed's extended suspicion of Coldhands ("Who is he? What
is he? Anyone can put on a black cloak…") is already quoted verbatim on the
`coldhands` tier-1 node itself and is not re-quoted here as a second edge; it is
premise for the whole theory cluster, not new theory-side evidence.

## Ungrounded material (outside the corpus)

- **grrm** — A Reddit user (u/_honeybird) reportedly located a note in George R.R.
  Martin's original *A Dance with Dragons* manuscript explicitly rejecting the
  Benjen Stark identity for Coldhands. This is the marquee piece of evidence
  against the single most popular fan candidate, and it is entirely out-of-book: an
  author's private manuscript annotation reported secondhand, not a published-text
  beat, and not independently verifiable against the local corpus. It is never
  treated as an edge.
- **community** — The Benjen Stark candidate itself (Ned's brother, last seen
  riding beyond the Wall in *A Game of Thrones* and never returning) is popular
  fan reasoning built from Benjen's disappearance and the timing of Coldhands's
  first appearance, not from any book passage connecting the two directly.
- **dunk-egg** — The Ser Duncan the Tall candidate (Dunk's known relationship with
  Bloodraven at the end of *The Mystery Knight*, escorting him to the Wall, as a
  hypothetical bridge to Dunk himself later joining the Watch and dying beyond it)
  could not be grounded to any verbatim passage this pass, in either the D&E
  novellas or the main series. The video's own counter-arguments (Dunk's known
  height contradicts Coldhands's apparent build; Dunk is generally understood to
  have died at Summerhall; Night's Watch membership for so famous a hedge knight
  would likely have been remarked on) are the video's reasoning, not independently
  cited text.
- **community** — The Night's King candidate (a legendary Lord Commander from
  eight thousand years ago, said to have taken an Other or wight bride and ruled
  from the Nightfort — which would explain Coldhands's knowledge of the Black
  Gate) rests entirely on the in-world legend (Old Nan's tale) and community
  synthesis; no book passage ties the legend to Coldhands specifically, and this
  session could not ground a citable line for either the theory or its own
  counter-arguments (that the Night's King was reportedly cast down and his name
  struck from memory, that eight thousand years is implausibly long for a mind to
  survive intact, or that Coldhands shows no sign of controlling animals on the
  Night's King's scale). The **grrm**-domain claim that George R.R. Martin has
  publicly implied the Night's King did not survive to the present day is likewise
  an out-of-book author statement, not cited text.
- **community** — The Night's King/Other-hybrid candidate (a descendant of the
  Night's King and his non-human bride) is the weakest and most speculative of the
  named candidates in the source video's own telling; no supporting or
  counter-arguing passage could be grounded this pass.
- **book-interpretive** — The video's fallback reading — that Coldhands may simply
  be an unnamed, otherwise-unremarkable Night's Watchman killed by the Others and
  reanimated by Bloodraven, with no larger identity secret at all — is presented as
  unsatisfying by the video itself (it does not explain why he hides his face or
  why the text keeps drawing attention to the mystery), but this is the video's own
  narrative-craft argument rather than a citable textual beat.
- **KNOWN GAP** — Two beats from the source extraction (`coldhands-B30`, the
  argument that the Others killing Coldhands sits oddly against the Night's King
  legend's own "sacrifices to the Others" framing, and `coldhands-B35`, the
  argument that Coldhands shows none of the Others' own distinguishing features)
  have no grounded quote on disk: the S214 regrounding-agent pass died at a spend
  wall before appending rows for either beat. Neither is asserted as fact or
  represented as an edge; both are simply absent from this build rather than
  deliberately excluded. See PROPOSAL.md.

## Status Notes

**Status: open.** The published books never confirm what animates Coldhands or who
he was before death; the mystery is written as deliberately unresolved narrative
craft (Meera's repeated, pointed questioning that is never answered on the page),
not as a puzzle with a hidden textual solution waiting to be assembled.

**Show complication.** *Game of Thrones* cut the Coldhands character entirely — he
never appears on screen under that name. Instead, the show gave Coldhands's book
*function* (an undead-but-still-a-person ranger beyond the Wall who rescues and
guides Bran and his companions south, ultimately sacrificing himself to hold back
the army of the dead) to a reworked Benjen Stark, reintroduced in Season 6 as a man
stabbed by the Others and saved mid-transformation by the Children of the Forest.
This is the show's own de facto answer to "who is Coldhands" — but it is a show-only
identity merge, not a book confirmation: the books' Coldhands (first seen fully
formed in *A Storm of Swords*) and the books' Benjen (vanished beyond the Wall in
*A Game of Thrones*, unaccounted for as of *A Dance with Dragons*) remain two
un-reconciled figures on the page. Status stays `open` rather than
`show-confirmed` because the show's Benjen-as-ranger substitution is a
narrative-adaptation choice for its own continuity, not a depiction or confirmation
of anything stated in the books — and it sits in direct tension with the
**grrm**-domain manuscript note (fenced above) reportedly rejecting Benjen
specifically as Coldhands's book identity. Show and (reported) author intent point
in opposite directions; neither is book text.

**ASX verdict:** the source video concludes it does not know who Coldhands was, but
is fairly confident about what he is — a Night's Watchman (of some kind) killed by
the Others and reanimated with old-gods nature magic, probably by Bloodraven and the
children of the forest — while treating every named identity candidate (Benjen
Stark, Will/Waymar Royce, Ser Duncan the Tall, the Night's King, and the
Night's King/Other hybrid) as unconvincing. This node's `confidence: tier-4`
reflects that split: the *what*-is-Coldhands reading has reasonable textual
support (six edges above); the *who*-was-Coldhands question — the theory's own
title — has essentially none, which is the honest, lower-confidence half of the
claim.
