# Bloodraven cluster — proposal (S216, staging-only)

**Session:** S216 theories wave-1, Bloodraven multi-theory unit. **Graph mutation:
NO.** All files confined to `working/theories/bloodraven-cluster/`. Staged at the
mint gate per the standing S214 rule (Matt: staging-only, no mint without explicit
go).

## Shape decision

Five ASX headers from `1oEqnDAbCfE` ("Bloodraven: what's the three-eyed raven's
secret plan?"), 71 beats, 25 byte-verified-grounded:

| header | beats (total / grounded) | disposition |
|---|---|---|
| "Bloodraven's grand plan (Azor Ahai bloodline + Bran/Jon)" | B01–B27 (11 grounded) | absorbed into **`bloodravens-grand-plan`** (NEW mint) |
| "Bloodraven is secretly a villain" | B44–B66 (9 grounded) | absorbed into **`bloodravens-grand-plan`** (same node — see below) |
| "Bloodraven trained (and traumatized) Euron Greyjoy" | B37–B43 (2 grounded) | absorbed into `bloodravens-grand-plan`'s **Ungrounded material** only — the two grounded beats (B37/B38) are general Euron-villainy color, not a Bloodraven connection; the connecting claim itself never grounds. No edges. |
| "Maynard Plumm is Bloodraven" | B28–B31 (2 grounded) | **ENRICH** `maynard-plumm-theories` stub (already a named wiki-stub theory) |
| "Quaithe is Shiera Seastar" | B32–B36 (1 grounded) | **folded** as a deferred-future-unit note inside `bloodravens-grand-plan`'s Ungrounded material — below the 3-edge mint bar, and the one grounded beat doesn't itself evidence the identity claim |

**Why the "grand plan" and "villain" headers share one node, not two.** The source
video itself treats these as two readings of the *same* evidence (Brynden's cave
mentorship, the raven pattern, his D&E-era rule), not two separate claims with
disjoint evidence sets — its own conclusion is that the ambiguity is deliberate
("something more interesting" than a simple hero). Splitting them would have forced
duplicate premise-prose and, worse, duplicate edges off the same character node for
opposite readings of identical facts. One node with paired `## Evidence For`
(covering both the agenda-reading and the villain-reading, since most edges serve
both) and a short `## Evidence Against` mirrors how R+L=J handles its own
throne-claim extension inside one node rather than splitting it out.

**Why Euron got zero edges despite two "grounded" beats existing.** B37 (Euron's ship
painted red) and B38 (Euron's shade-of-evening/warlock retinue) byte-verified fine —
but neither mentions Brynden Rivers at all. They support "Euron is a mystical
villain," a premise the `eldritch-apocalypse` cluster already owns in more depth.
The actual connecting claim — that Brynden ever contacted, trained, or traumatized
Euron — appears in this substrate only as B39–B43, **none of which grounded**
(same conclusion the `eldritch-apocalypse` S216 adjudication reached independently
for the identical claim, fenced there as "community-ungrounded"). Edging B37/B38 to
this theory node would have implied a textual link between Euron and Bloodraven that
doesn't exist in either cluster's corpus. Result: the sub-claim stays entirely
prose-fenced, cross-referenced to `eldritch-apocalypse.node.md` to avoid double-mint,
zero edges in both places.

**Why Quaithe/Shiera didn't mint.** Only 1 of 5 source beats (B32, Quaithe's plain
self-introduction) byte-verified. It proves Quaithe exists; it says nothing about
Shiera Seastar. The task's stated bar (3+ edges for a respectable small node) isn't
close to met, so it's held out per the task's own instruction — noted as a deferred
future unit, cross-referenced to `shiera-seastar.node.md`'s existing "Fan theories
connect her to Quaithe" line.

## Nodes

- **`bloodravens-grand-plan`** (NEW, `working/theories/bloodraven-cluster/nodes/`) —
  concept.theory, tier-3, status open. 9 edges (7× SUPPORTS tier-3, 2× SUPPORTS
  tier-4 — no CONTRADICTS edge; the video's own counter-argument material didn't
  ground to citable text, see Evidence Against/Ungrounded).
- **`maynard-plumm-theories`** (ENRICH existing stub, `working/theories/bloodraven-cluster/enrich/`)
  — concept.theory, tier-2 stub → tier-3, status open, node_version 1→2, bucket_id/
  prompt_version preserved. 2 edges (1× tier-3, 1× tier-4).

## Edge list by target

**`bloodravens-grand-plan`** (source → this node, all SUPPORTS):
| id | source | tier | what |
|---|---|---|---|
| G1 | brynden-rivers | 3 | Leaf frames Brynden's purpose ("for the realms of men") |
| G2 | jon-snow | 4 | Mormont's raven fixates on "Snow" (wildling-gate scene, corrected from source's mis-stated "election" framing) |
| G3 | jon-snow | 3 | raven says Jon's full name — narration itself flags it "queer" |
| G4 | brynden-rivers | 3 | "Targaryens who dreamed" extended with the Daemon/Whitewalls prophecy detail (book-cites a fact currently only wiki-sourced on brynden-rivers.node.md) |
| G5 | jaehaerys-ii-targaryen | 3 | AA-prophecy-driven arranged marriage of Aerys II/Rhaella (book-cites a fact currently only wiki-sourced on aerys-ii-targaryen.node.md) |
| G6 | brynden-rivers | 3 | Sefton's "no one to oppose him" rant — clearest textual anchor for the villain reading |
| G7 | melisandre | 4 | Melisandre's fire vision ("was this the enemy?") pairing a corpse-white wooden face with a wolf-faced boy |
| G8 | bran-stark | 4 | Bran's own dread/disillusionment on meeting Brynden (deliberately narrowed from the source's stronger, ungrounded "lured a child, got friends killed" framing) |
| G9 | bran-stark | 3 | AGOT crow-dream: "the bones of a thousand other dreamers impaled" |

**`maynard-plumm-theories`** (source → this node, all SUPPORTS):
| id | source | tier | what |
|---|---|---|---|
| P1 | maynard-plumm | 4 | Plumm's evasive non-answer about his own kinship |
| P2 | maynard-plumm | 3 | the "single pale white eye" startle-beat, resolved into the brooch |

## Layer-rule application (brynden-rivers premise vs. theory edges)

Per the assignment's layer rule, several grounded beats duplicated facts
`brynden-rivers.node.md` already owns verbatim and were **dropped to premise prose,
no edge**, exactly like GNC's G2/G3 precedent:

- B01 (Aegon IV/Blackwood parentage) — already Identity-section fact
- B04 (dog/wolves/crows skinchanging rumors) — already an exact Quotes-section entry
- B06 (weirwood-throne description) — already cited at the same line on the node
- B08 ("I have watched you...") — already an exact Quotes-section entry
- B44/B57 (duplicate of each other, "Mother marked Lord Rivers...Bittersteel...Redgrass Field") — already an exact Quotes-section entry (a *different* sentence from the same tss-dunk-01:937-943 passage, "Make no mistake, 'tis Lord Rivers..." at line 943, was fresh and became edge G6 instead)
- B48 ("half-corpse and half-tree...ghastly statue") — already quoted verbatim in the node's Appearances & Description section, same line (115)
- B49/B50 ("Never fear the darkness"/"Darkness will make you strong") — same passage (line 45) the node already quotes as the "signature mentorship line"; the villain theory's re-reading of this line as sinister grooming is discussed in prose (Evidence For, via the adjacent B58 edge), not re-edged

## Two mis-groundings caught and excluded (not evidence, not prose, not edges)

The regrounding-agent pass returned two false-positive "grounded" rows where the
matched text has nothing to do with its paired paraphrase:

- **B22** — paraphrase claimed "King Aerys (II) was into prophecy, and Shiera Seastar
  was into 'ancient scrolls.'" The matched quote (`acok-jon-01.md:13`) is simply Jon
  entering the Castle Black library — a keyword collision on "scrolls." Dropped
  entirely.
- **B45** — paraphrase claimed "As Hand of the King, Brynden basically ruled the
  realm as a spymaster with a huge informer network." The matched quote
  (`adwd-bran-03.md:73`) is Brynden teaching Bran what a greenseer is ("a thousand
  eyes, a hundred skins...") — a keyword collision on "eyes"/"thousand." Dropped
  entirely; the real "spymaster network" textual support is G6 instead.

Both would have byte-verified cleanly under `quotecheck` (the text really does
appear at that line) while being substantively false as evidence — a reminder that
byte-verification catches fabrication, not mis-attribution; each grounded row was
read in full file context before use, not just string-matched.

## Held-out material (Ungrounded, fenced in the nodes, not edges)

- Century-long Targaryen "breeding program" as a *Brynden-orchestrated* project
  (video's own hedge: "there's no knowing how deep this goes")
- The full Bloodraven-trained-Euron connecting claim (B39–B43, all ungrounded)
- Quaithe=Shiera identity argument beyond B32's bare fact of Quaithe's existence
- Brynden-wants-Bran's-body, Brynden-aids-the-Others, weirwood-network-as-hivemind,
  Coldhands-fed-Bran-human-flesh/Jojen's-body, Brynden-edited-Bran's-memories, and
  the show-only "robotic and dehumanized" Bran detail — all B51/B52/B54/B55/B56/B59/
  B60/B61, none grounded
- Stannis/Davos "what is the life of one bastard boy... Everything" thematic
  counterpoint (B62/B63) — video's own moral counterpoint, byte-fail on regrounding
- GRRM's other evil-hivemind stories (craft note, not a plot claim)

## Open questions for the orchestrator

1. Should G6's edge `source` instead be a new/existing `hand-of-the-king` office
   node or stay on `brynden-rivers` directly? Followed R+L=J precedent (source =
   subject of the claim) rather than inventing an office-node convention.
2. `bloodravens-grand-plan` carries no CONTRADICTS edge (unlike R+L=J's T7 or GNC's
   G12) because the video's own rebuttal material didn't ground to citable text this
   pass. Worth a second regrounding attempt specifically at the Stannis/Davos
   parallel (asos-davos-05) if this cluster gets revisited before mint.
3. G2's tier-4 (vs. G3's tier-3) reflects that G3's "queer"/unprecedented framing is
   textually stronger than G2's plainer raven behavior — flag if a fresh
   adversarial pass disagrees with the split.

## HARVEST

(one-line pointers to notable off-task finds while reading the substrate — POINT,
not extracted)

- `sources/chapters/tss/tss-dunk-01.md:940-945` / worldbuilding / Septon Sefton's
  full rant is a dense, unmined block of D&E-era political texture (Great Spring
  Sickness aftermath, Dagon Greyjoy's raids, the Bracken/Blackwood feud, Aerys I's
  neglect of the throne) — most of it untouched by this pass beyond the two excerpted
  sentences.
- `sources/chapters/adwd/adwd-bran-03.md:58` (approx, "Do you like to read books,
  Bran?" exchange right after the B45 mis-ground) / character beat / Bran's own
  reading preferences ("fighting stories," dismissing "kissing stories") — minor
  characterization color, unused.
- `sources/chapters/adwd/adwd-melisandre-01.md:15-20` / foreshadowing / the vision
  sequence immediately preceding G7 (towers by the sea crumbling under a dark tide,
  "shadows in the shape of skulls") reads as separate Long Night / apocalypse
  imagery, likely relevant to the `eldritch-apocalypse` cluster or a future
  Melisandre-visions dip — not pulled into this unit.
