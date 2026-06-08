"""
plate3-alias-retro-match.py

For each of the 219 Plate-3 minted event-node slugs, check whether the slug
appears as a key OR an alias value in the event-node-aliases.json produced by
wiki-event-alias-harvester.py.

Output: working/edge-modeling/plate3-full/alias-retro-matches.csv

Columns: mint_slug, matched_wiki_event, match_via (alias|name|none)

Usage:
  python scripts/plate3-alias-retro-match.py
"""

import csv
import json
import sys
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parent.parent

    alias_path = repo_root / "working" / "wiki" / "data" / "event-node-aliases.json"
    minted_dir = repo_root / "working" / "edge-modeling" / "plate3-full" / "minted-event-nodes"
    output_csv = repo_root / "working" / "edge-modeling" / "plate3-full" / "alias-retro-matches.csv"

    if not alias_path.exists():
        print(f"ERROR: {alias_path} not found. Run wiki-event-alias-harvester.py first.", file=sys.stderr)
        sys.exit(1)

    if not minted_dir.exists():
        print(f"ERROR: {minted_dir} not found.", file=sys.stderr)
        sys.exit(1)

    # Load aliases JSON
    with open(alias_path) as f:
        aliases: dict = json.load(f)

    # Build flat lookup: normalized_string → (canonical_slug, match_via)
    # Priority: canonical slug match first, then alias match
    lookup: dict[str, tuple[str, str]] = {}

    for canonical, data in aliases.items():
        # The canonical slug itself
        if canonical not in lookup:
            lookup[canonical] = (canonical, "name")
        # Each alias
        for a in data["aliases"]:
            if a not in lookup:
                lookup[a] = (canonical, "alias")

    print(f"Alias lookup entries: {len(lookup)}")

    # Load mint slugs
    mint_files = sorted(minted_dir.glob("*.node.md"))
    mint_slugs = [f.stem.replace(".node", "") for f in mint_files]
    print(f"Plate-3 mint slugs: {len(mint_slugs)}")

    # Match
    rows = []
    match_count = 0
    for slug in mint_slugs:
        if slug in lookup:
            matched_wiki, via = lookup[slug]
            rows.append((slug, matched_wiki, via))
            match_count += 1
        else:
            rows.append((slug, "", "none"))

    # Write CSV
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mint_slug", "matched_wiki_event", "match_via"])
        writer.writerows(rows)

    print(f"\nWrote {output_csv}")
    print(f"\n--- Results ---")
    print(f"Total mint slugs:   {len(mint_slugs)}")
    print(f"Matched:            {match_count}")
    print(f"Unmatched:          {len(mint_slugs) - match_count}")

    matched_rows = [(s, w, v) for s, w, v in rows if v != "none"]
    by_alias = [r for r in matched_rows if r[2] == "alias"]
    by_name = [r for r in matched_rows if r[2] == "name"]
    print(f"  via name:  {len(by_name)}")
    print(f"  via alias: {len(by_alias)}")

    if matched_rows:
        print("\nMatched entries:")
        for slug, wiki, via in matched_rows:
            print(f"  {slug:55s} → {wiki} ({via})")


if __name__ == "__main__":
    main()
