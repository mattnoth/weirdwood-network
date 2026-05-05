
# POV Character Lookup Table

> **Purpose:** Canonical mapping of chapter heading text → normalized character name for the chapter splitter script. Used by the script-builder agent when constructing `scripts/chapter-splitter.py`.

```python
POV_CHARACTERS = {
    # AGOT
    "BRAN": "bran",
    "CATELYN": "catelyn",
    "DAENERYS": "daenerys",
    "EDDARD": "eddard",
    "JON": "jon",
    "ARYA": "arya",
    "TYRION": "tyrion",
    "SANSA": "sansa",

    # ACOK additions
    "THEON": "theon",
    "DAVOS": "davos",

    # ASOS additions
    "JAIME": "jaime",
    "SAMWELL": "samwell",

    # AFFC descriptive titles
    "THE PROPHET": "the-prophet",
    "THE DROWNED MAN": "the-drowned-man",
    "THE IRON CAPTAIN": "the-iron-captain",
    "THE KRAKEN'S DAUGHTER": "the-krakens-daughter",
    "THE CAPTAIN OF GUARDS": "the-captain-of-guards",
    "THE SOILED KNIGHT": "the-soiled-knight",
    "THE QUEENMAKER": "the-queenmaker",
    "THE PRINCESS IN THE TOWER": "the-princess-in-the-tower",
    "ALAYNE": "alayne",
    "CAT OF THE CANALS": "cat-of-the-canals",
    "BRIENNE": "brienne",
    "CERSEI": "cersei",

    # AFFC descriptive title (missing from original list)
    "THE REAVER": "the-reaver",

    # ADWD descriptive titles
    "REEK": "reek",
    "THE MERCHANT'S MAN": "the-merchants-man",
    "THE TURNCLOAK": "the-turncloak",
    "THE PRINCE OF WINTERFELL": "the-prince-of-winterfell",
    "THE LOST LORD": "the-lost-lord",
    "THE WINDBLOWN": "the-windblown",
    "THE WAYWARD BRIDE": "the-wayward-bride",
    "THE WATCHER": "the-watcher",
    "THE KING'S PRIZE": "the-kings-prize",
    "THE DRAGONTAMER": "the-dragontamer",
    "THE GRIFFIN REBORN": "the-griffin-reborn",
    "THE SACRIFICE": "the-sacrifice",
    "THE UGLY LITTLE GIRL": "the-ugly-little-girl",
    "THE DISCARDED KNIGHT": "the-discarded-knight",
    "THE SPURNED SUITOR": "the-spurned-suitor",
    "THE QUEENSGUARD": "the-queensguard",
    "THE BLIND GIRL": "the-blind-girl",
    "A GHOST IN WINTERFELL": "a-ghost-in-winterfell",
    "THE IRON SUITOR": "the-iron-suitor",
    "THE KINGBREAKER": "the-kingbreaker",
    "THE QUEEN'S HAND": "the-queens-hand",
    "MELISANDRE": "melisandre",
    "BARRISTAN": "barristan",
    "VICTARION": "victarion",
    "QUENTYN": "quentyn",
    "JON CONNINGTON": "jon-connington",
}
```

## Expected Chapter Counts

| Book | Total | Breakdown |
|------|-------|-----------|
| AGOT | 73 | Prologue + 72 chapters (8 POV + prologue POV) |
| ACOK | 70 | Prologue + 69 chapters (10 POV + prologue POV) |
| ASOS | 82 | Prologue + 80 chapters + Epilogue (10 POV + prologue/epilogue POV) |
| AFFC | 46 | Prologue + 45 chapters (12 POV + prologue POV) |
| ADWD | 73 | 72 chapters + Epilogue (18 POV + epilogue POV) |

### Tales of Dunk and Egg

| Novella | Code | Chapters | POV | Words |
|---------|------|----------|-----|-------|
| The Hedge Knight | `thk` | 1 | Duncan the Tall | ~31,600 |
| The Sworn Sword | `tss` | 1 | Duncan the Tall | ~36,600 |
| The Mystery Knight | `tmk` | 1 | Duncan the Tall | ~36,800 |

Duncan the Tall (Dunk) is the sole POV character across all three novellas. Each novella is one continuous chapter with no internal divisions. Set pre-AGOT in the Targaryen era (~90 years before the main series).
