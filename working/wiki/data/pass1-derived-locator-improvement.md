# Pass-1-Derived Locator Improvement — Measurement Report

> Generated: 2026-05-25T18:14:04+00:00

## 1. locate_quality Distribution (All 199+ Smoke3 Rows)

| locate_quality | Count | % |
|----------------|-------|---|
| both-named | 144 | 72.0% |
| one-named | 39 | 19.5% |
| nearest-fallback | 14 | 7.0% |
| chapter-level | 3 | 1.5% |

**Note:** `chapter-level` rows are cases where the chapter file was missing or
no sentence cleared the minimum score threshold.  `nearest-fallback` means the
best sentence named neither endpoint (content-word match only).

## 2. Recall-Recovery Signal (emit_edge rows only)

The smoke3 run produced **107 emit_edge rows** (the other 93 were
rejected/classify_failed and also get re-located for the re-smoke).

| Metric | Count |
|--------|-------|
| emit_edge rows total | 107 |
| Originally passing quote-relevance | 33 |
| Originally failing quote-relevance | 74 |
| Now passing with improved locator | 82 |
| **Recall-recovered (fail→pass)** | **50** |
| Regressions (pass→fail) | 1 |
| Still failing after improvement | 24 |

**Before→after both-named count:** 33 → 82 (+50 recovered, 1 regression)

Recovery rate on originally-failing rows: **67.6%**

### Residual Failure Reasons

| Reason | Count |
|--------|-------|
| coreference | 14 |
| genuinely-not-co-located | 7 |
| stoplist-filtered | 3 |

Reason definitions:
- **coreference**: quote has pronouns/generic phrases instead of a name — unfixable by window selection
- **genuinely-not-co-located**: both entities appear in different paragraphs/scenes not captured
- **stoplist-filtered**: name token filtered by stoplist (rare; usually a very short or generic name)

## 3. Before/After Examples (Improved Quotes)

Showing up to 10 of 50 recovered rows.

### Example 1: tyrion-lannister → gunthor

**Original quote:** ""What do the Stone Crows do, but hide behind rocks and shiver with fear as the knights of the Vale ride by?""

**Improved quote** (`locate_quality=both-named`): "We will gladly pay you for the goat we ate.” “What do you have to give us, Tyrion son of Tywin?” asked the one who named himself Gunthor, who seemed to be their chief."

### Example 2: petyr-baelish → joffrey-baratheon

**Original quote:** "“Until the tourney on Prince Joffrey’s name day,” he said, crossing the room to wrench the dagger from the wood."

**Improved quote** (`locate_quality=both-named`): "“It’s mine.” “Yours?” It made no sense. Petyr had not been at Winterfell. “Until the tourney on Prince Joffrey’s name day,” he said, crossing the room to wrench the dagger from the wood."

### Example 3: tyrion-lannister → shagga

**Original quote:** "Bronn managed to keep Shagga from chopping off the dead man’s cock, which was fortunate, but even so Ulf is demanding blood money, which Conn and Shagga refuse to pay.” “When soldiers lack discipline,"

**Improved quote** (`locate_quality=both-named`): "“He still had that wood-axe of his strapped to his back.” “Shagga is of the opinion that three axes are even better than two.” Tyrion reached a thumb and forefinger into the salt dish, and sprinkled a"

### Example 4: catelyn-stark → robb-stark

**Original quote:** "“Catelyn, you shall stay here in Winterfell.” His words were like an icy draft through her heart."

**Improved quote** (`locate_quality=both-named`): "There must always be a Stark in Winterfell."

### Example 5: sandor-clegane → sansa-stark

**Original quote:** ""You're like one of those birds from the Summer Isles, aren't you? A pretty little talking bird, repeating all the pretty little words they taught you to recite.""

**Improved quote** (`locate_quality=both-named`): "“No,” he growled at her, “no, little bird, he was no true knight.” The rest of the way into the city, Sandor Clegane said not a word."

### Example 6: daenerys-targaryen → jhiqui

**Original quote:** "Jhiqui had scented the water with the oils she had found in the market in Vaes Dothrak; the steam rose moist and fragrant."

**Improved quote** (`locate_quality=both-named`): "Irri and Jhiqui fanned her dry, while Doreah brushed her hair until it fell like a river of liquid silver down her back."

### Example 7: sansa-stark → joffrey-baratheon

**Original quote:** ""I don't want to marry you. You chopped off my father's head!""

**Improved quote** (`locate_quality=both-named`): "You had better do what I say.” Joffrey reached for her, and Sansa cringed away from him, backing into the Hound."

### Example 8: arya-stark → weese

**Original quote:** "Harra, I believe we should give this one to Weese.” “If you think so, Amabel.” They gave her a shift of grey roughspun wool and a pair of ill-fitting shoes, and sent her off."

**Improved quote** (`locate_quality=both-named`): "Harra, I believe we should give this one to Weese.” “If you think so, Amabel.” They gave her a shift of grey roughspun wool and a pair of ill-fitting shoes, and sent her off. Weese was understeward fo"

### Example 9: old-nan → bran-stark

**Original quote:** ""Dragons... It be dragons, boy.""

**Improved quote** (`locate_quality=both-named`): "Bran got no princes from Nan, no more than he ever had."

### Example 10: mormont → jon-snow

**Original quote:** ""Find him. Fight him. Stop him.""

**Improved quote** (`locate_quality=both-named`): "“There’s a cold smell to that one, there is.” “Jon,” Lord Mormont commanded, “ride back along the column and spread the word."

## 4. Still Failing After Improvement

**24 rows** still fail the quote-relevance filter after the improved locator.

- **cersei-lannister → catelyn-stark** [coreference] `one-named`:
  "So here is Cersei’s nightmare: while her father and brother spend their power battling Starks and Tullys, Lord Stannis will land, proclaim himself king, and lop off her son’s curly blond head … and he"
- **robert-baratheon → kingsguard** [genuinely-not-co-located] `nearest-fallback`:
  "“His Grace was reeling in his saddle by the time we flushed the boar from his lair, yet he commanded us all to stand aside.” “I wonder, Ser Barristan,” asked Varys, so quietly, “who gave the king this"
- **cersei-lannister → hand-of-the-king** [coreference] `one-named`:
  "No one wants war again, least of all me.” Her hand touched his face, his hair."
- **catelyn-stark → dragonpit** [coreference] `one-named`:
  "She had certainly been the fastest of the ships available in White Harbor when Catelyn and Ser Rodrik Cassel had arrived after their headlong gallop downriver."
- **yoren → eddard-stark** [coreference] `one-named`:
  "Rode hard, I did, near killed my horse the way I drove her, but I left the others well behind.” “The others?” Yoren spat."
- **tyrion-lannister → marillion** [coreference] `one-named`:
  "When the song was over, Jaime rose from his place, commanded Tyrion to kneel, and touched him first on one shoulder and then on the other with his golden sword, and he rose up a knight."
- **quhuru-mo → kings-landing** [coreference] `one-named`:
  "Come to me in King’s Landing when I am on my father’s throne, and you shall have a great reward.” The Summer Islander promised he would do so, and kissed her lightly on the fingers as he took his leav"
- **tyrion-lannister → guildhall-of-the-alchemists** [stoplist-filtered] `one-named`:
  "If there are more, the Bold Wind will cleave to the Seaswift to protect her while the rest of the fleet does battle.” Tyrion nodded."
- **grenn → fist-of-the-first-men** [genuinely-not-co-located] `nearest-fallback`:
  "Giant, Dolorous Edd, Sweet Donnel Hill, Ulmer, Left Hand Lew, Garth Greyfeather."
- **donal-noye → cellador** [genuinely-not-co-located] `nearest-fallback`:
  "“Any man here stays his sword, I’ll chuck his puckered arse right off this Wall ."
- **tom-of-sevenstreams → lady-smallwood** [coreference] `one-named`:
  "Men will be calling you Tom Sevensons before much longer.” “As it happens,” said Tom, “I passed seven many years ago."
- **grenn → mormont** [coreference] `one-named`:
  "Grenn pulled Sam to his feet, checked Small Paul for a pulse and closed his eyes, then snatched up the dagger again."
- **oberyn-martell → starfall** [stoplist-filtered] `one-named`:
  "A quest that took us to Starfall, the Arbor, Oldtown, the Shield Islands, Crakehall, and finally Casterly Rock ."
- **joffrey-baratheon → tyrion-lannister** [coreference] `one-named`:
  "The men would carry her up to her wedding bed, undressing her on the way and making rude jokes about the fate that awaited her between the sheets, while the women did Tyrion the same honors."
- **tywin-lannister → hoster-tully** [coreference] `one-named`:
  "“Jeyne Westerling is her mother’s daughter,” said Lord Tywin, “and Robb Stark is his father’s son.” This Westerling betrayal did not seem to have enraged his father as much as Tyrion would have expect"
  *(... and 9 more)*

## 5. Honest Assessment

### What the window-expansion improvement reaches

The core mis-location class — where the locator chose a single sentence that named
only ONE endpoint — is now largely addressed.  The improved algorithm:

1. Tries EVERY sentence for both-named first (covers cases where a single sentence
   spans both names but scored lower than a one-name content-rich sentence).
2. If no single sentence names both, expands a window of up to
   3 consecutive sentences centred on the best
   sentence.  This catches the common pattern of 'Name A ... [sentence] ... Name B'
   appearing in adjacent sentences within the same prose beat.
3. Uses the alias-aware token index (build_slug_token_index from the relevance filter),
   so firstname aliases and alternate forms are recognised.

### Irreducible residual (coreference)

The hard limit that window expansion CANNOT fix is **coreference**: when the prose
refers to an entity only as 'she', 'he', 'my father', 'the girl', etc. within the
relevant passage.  These cases land as `one-named` or `nearest-fallback` regardless
of how large the window is, because no name token appears in the text.

This is not a locator failure — it is a fundamental property of the source text.
Resolution requires NLP coreference resolution (out of scope for this deterministic
pipeline), or manual review.

### Remaining gap

Even after improvement, some rows will still fail the quote-relevance filter.  The
bulk of remaining failures fall into three categories:

1. **Coreference** (pronouns in the selected passage)
2. **Genuinely not co-located** (the two entities are mentioned in different parts
   of the chapter, with no single prose beat spanning both)
3. **Rare stoplist cases** (one entity has a very short or generic name that is
   filtered by the stoplist)

The improvement is expected to recover a meaningful fraction of originally-failing
rows — the exact number is measured in §2 above.
