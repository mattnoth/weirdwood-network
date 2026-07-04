"""themes.py — `theme` op (query-layer Track, step 8a; design.md D-E/G4).

Reads the deterministic theme->members table `build/build_theme_index.py`
writes (`working/wiki/data/theme-index.json`, full profile). No ranking, no
LLM — this is a lookup over a pre-built table, same "read what the builder
wrote, never re-derive" discipline as `search.py` reading `search-index.json`.

`list_themes()` with no argument (or the CLI's bare `weirwood query theme`)
returns every theme name + member count — the discovery surface ("what
themes exist") a caller needs before naming one.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .load import REPO_ROOT

WORKING_INDEX_FILE = REPO_ROOT / "working" / "wiki" / "data" / "theme-index.json"
BUNDLE_INDEX_FILE = REPO_ROOT / "web" / "data" / "theme-index.json"


def load_index(path: Path = WORKING_INDEX_FILE) -> dict[str, Any] | None:
    """Load a theme-index.json (either the full or bundle format — both share
    the same `{"themes": {name: {member_count, members}}}` shape, the bundle
    format's members just drop `matched_via`). Returns None if the file
    doesn't exist (caller decides whether that's fatal)."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_themes(index: dict[str, Any] | None = None, *, index_path: Path = WORKING_INDEX_FILE) -> list[dict[str, Any]]:
    """Return every theme name + member_count, sorted by name — the
    discovery surface for `weirwood query theme` (no argument)."""
    if index is None:
        index = load_index(index_path)
    if index is None:
        return []
    themes = index.get("themes", {})
    return [
        {"name": name, "member_count": obj.get("member_count", len(obj.get("members", [])))}
        for name, obj in sorted(themes.items())
    ]


def theme(
    name: str,
    index: dict[str, Any] | None = None,
    *,
    index_path: Path = WORKING_INDEX_FILE,
    category: str | None = None,
) -> dict[str, Any]:
    """Return `{theme, member_count, members}` for one theme name (exact,
    case-insensitive match against the theme's canonical name — themes are a
    small, fixed, named set, not a free-text search). `category` optionally
    filters members to one `graph/nodes/` type-directory name (e.g. "foods"),
    same vocabulary as `search`'s `--type`/`list`'s `--type`.

    An unknown theme name returns `{theme: name, member_count: 0, members: [],
    error: "unknown theme", known_themes: [...]}` — not an exception; mirrors
    `list_nodes`'s "unknown category -> empty result, not an error" convention,
    but ALSO surfaces the known-theme list since (unlike a node category) a
    typo here has no discovery path other than this error message.
    """
    if index is None:
        index = load_index(index_path)
    if index is None:
        return {"theme": name, "member_count": 0, "members": [], "error": "theme index not built"}

    themes = index.get("themes", {})
    target = name.strip().lower()
    matched_name = next((n for n in themes if n.lower() == target), None)

    if matched_name is None:
        return {
            "theme": name,
            "member_count": 0,
            "members": [],
            "error": "unknown theme",
            "known_themes": sorted(themes.keys()),
        }

    members = themes[matched_name].get("members", [])
    if category is not None:
        members = [m for m in members if m.get("category") == category]

    return {
        "theme": matched_name,
        "member_count": len(members),
        "members": members,
    }
