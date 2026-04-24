# Scratch Notes

Observations worth keeping but not yet triaged. Tag with source/date.

---

### POV Reference Table Gaps (Session 2, chapter-splitter)

The original `reference/pov-characters.md` was missing 6 chapter headings. All have been added:
- AFFC: THE REAVER (Victarion Greyjoy)
- ADWD: THE BLIND GIRL (Arya), A GHOST IN WINTERFELL (Theon), THE IRON SUITOR (Victarion), THE KINGBREAKER (Barristan), THE QUEEN'S HAND (Barristan)

### Smart Quotes in Source Files (Session 2, chapter-splitter)

Source .txt files use Unicode curly/smart quotes (U+2019 right single quote mark instead of U+0027 straight apostrophe). The chapter splitter normalizes these before heading matching. The wiki scraper may also need to be aware of this if cross-referencing chapter text.
