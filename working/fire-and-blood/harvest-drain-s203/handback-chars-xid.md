# Handback — harvest-drain-s203 packet-chars-xid

Rows that don't home to a node inside characters/, species/, or houses/ (my owned
dirs), or that I couldn't confidently place, land here for the next attacher /
Matt triage. Format: `row | unit:line | reason`.

No true handbacks this packet — all 52 rows (42 cross-identity + 10
character-homed handback rows from the events attacher) homed to nodes under
`graph/nodes/characters/`. Two audit notes, not handbacks:

- row 120 (Mysaria "the White Worm ... The other harlots called her Misery.",
  fab-the-blacks-and-the-greens-16-p02:277) — SKIPPED. The exact quote text
  "The other harlots called her Misery." was already present verbatim in
  `mysaria.node.md`'s existing `## Quotes` section (a wiki-cite plain line,
  not a blockquote). Alias "Misery, the White Worm" was also already present.
  No new content added.
- row 277 (Mushroom's account of Aegon III protesting the dismissal of Massey
  and Darklyn) — packet unit/line (`fab-voyage-of-alyn-oakenfist-23:217`)
  did not contain this passage. Located the actual text at
  `sources/chapters/fab/fab-war-and-peace-and-cattle-shows-22-p01.md:31` and
  cited that instead (verified clean by scripts/verify_node_quotes.py). Packet
  metadata for this row looks mislocated — flagging in case the packet
  generator needs a fix.

