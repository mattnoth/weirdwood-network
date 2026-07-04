// theme(name) / listThemes() — the `theme` op (query-layer Track, step 8a;
// design.md D-E/G4, "the trigger table's routing half").
//
// Reads the build-time theme->members table shipped in the bundle
// (`web/data/theme-index.json`, built by
// `graph/query/build/build_theme_index.py` — see that module's docstring for
// the exact membership rules per theme: a fixed seed set, wholesale-by-node-
// type + whole-word/whole-phrase keyword matching, deterministic and
// re-runnable). Ports `graph/query/weirwood_query/themes.py`'s semantics —
// same lookup-only behavior, no ranking, no LLM.
//
// Themes are a SEPARATE axis from the settled 5-container bag-retrieval axis
// (`containers:` frontmatter, event-only) — not shipped to this bounded
// profile at all yet (design.md step 6a). `theme` covers descriptive/
// thematic content (food, hospitality, dress, healing, songs) the container
// axis was never meant to hold.
//
// No LLM in the loop, ever — pure data.

import type { GraphData, ThemeResult, ThemeSummary } from "./types.ts";

/** List every theme name + member count, sorted by name — the discovery
 * surface for a caller that doesn't yet know which theme names exist. */
export function listThemes(data: GraphData): ThemeSummary[] {
  const index = data.themeIndex;
  if (!index) return [];
  return Object.entries(index.themes)
    .map(([name, obj]) => ({ name, memberCount: obj.member_count }))
    .sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));
}

/**
 * Return `{theme, memberCount, members}` for one theme name (exact,
 * case-insensitive match against the theme's canonical name — themes are a
 * small, fixed, named set, not a free-text search). `opts.category`
 * optionally filters members to one `graph/nodes/` type-directory name
 * (e.g. "foods"), the same vocabulary `searchQuotes`'s `type` / `listNodes`'s
 * `type` use.
 *
 * An unknown theme name returns `{theme: name, memberCount: 0, members: [],
 * error: "unknown theme", knownThemes: [...]}` — not a thrown error; mirrors
 * `listNodes()`'s "unknown category -> empty result, not an error"
 * convention, but also surfaces the known-theme list since a typo has no
 * other discovery path here.
 */
export function theme(
  name: string,
  data: GraphData,
  opts?: { category?: string },
): ThemeResult {
  const index = data.themeIndex;
  if (!index) {
    return { theme: name, memberCount: 0, members: [] };
  }

  const target = name.trim().toLowerCase();
  const matchedName = Object.keys(index.themes).find((n) => n.toLowerCase() === target);

  if (matchedName === undefined) {
    return {
      theme: name,
      memberCount: 0,
      members: [],
      error: "unknown theme",
      knownThemes: Object.keys(index.themes).sort(),
    };
  }

  let members = index.themes[matchedName].members;
  if (opts?.category !== undefined) {
    members = members.filter((m) => m.category === opts.category);
  }

  return { theme: matchedName, memberCount: members.length, members };
}
