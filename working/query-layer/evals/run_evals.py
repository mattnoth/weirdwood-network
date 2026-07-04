#!/usr/bin/env python3
"""run_evals.py — deterministic eval runner for the query-layer Track (step 3).

Part of the query-layer Track (design: working/query-layer/design.md), session B.
Reads the FIXED question set (questions.md's Q1-Q20 table, hand-transcribed as
QUESTIONS below — see "Why the questions are inlined, not parsed" below) and scores
retrieval outcomes against the LIVE artifacts at run time:

  - full profile   -> graph/query/weirwood_query (imported directly; reads the live
                       graph/nodes/, graph/edges/edges.jsonl, and the alias tables at
                       working/wiki/data/*.json)
  - bounded profile -> web/data/{nodes,edges,alias-map}.json (the built chat bundle),
                       via a FAITHFUL PORT of web/src/lib/{resolve,normalize}.ts's
                       lookup semantics (see BoundedResolver below) -- not a re-derivation,
                       a direct line-for-line port, so it stays honest about what the
                       bounded profile actually does.

ZERO network / API calls. ZERO writes outside working/query-layer/evals/. This script
is read-only over graph/, web/data/, and working/wiki/data/.

Re-runnable: every number below is computed fresh from the live artifacts each run --
there are no baked-in "expected" values here. The FROZEN snapshot is the separate
baseline-2026-07-04.md report (produced by `--report`), not this script.

Usage:
    python3 working/query-layer/evals/run_evals.py            # print table to stdout
    python3 working/query-layer/evals/run_evals.py --report   # also write the dated
                                                                 baseline report file
    python3 working/query-layer/evals/run_evals.py --json     # machine-readable dump

Why the questions are inlined, not parsed from questions.md:
    questions.md is a hand-authored, narrative markdown table meant for human editing
    (with prose notes, provenance, and an appendix) -- round-tripping it through a
    markdown-table parser is more fragile than just keeping one small QUESTIONS list
    here that mirrors it. If questions.md's Q-rows change, update QUESTIONS to match
    (the ids are the join key; a mismatch is a bug in this file, not questions.md).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
QUERY_PKG = REPO_ROOT / "graph" / "query"
sys.path.insert(0, str(QUERY_PKG))

from weirwood_query import load as L  # noqa: E402
from weirwood_query import resolve as R  # noqa: E402
from weirwood_query import traverse as T  # noqa: E402

BUNDLE_DIR = REPO_ROOT / "web" / "data"
EVALS_DIR = REPO_ROOT / "working" / "query-layer" / "evals"

# ---------------------------------------------------------------------------
# The fixed question set (mirrors working/query-layer/evals/questions.md Q1-Q20).
# ---------------------------------------------------------------------------


@dataclass
class Question:
    id: str
    text: str
    archetype: str  # traversal | quote-hunter | thematic | researcher
    key_phrases: list[str]
    target_slugs: list[str]
    ops: list[str]  # expected-answerable-via, per operations.md op names
    notes: str = ""


QUESTIONS: list[Question] = [
    Question(
        "Q1", "Who killed Robb Stark?", "traversal",
        ["Robb Stark's death", "Robb Stark"],
        ["robb-is-killed", "roose-bolton", "walder-frey"],
        ["resolve", "neighbors", "chain"],
        "Mode-3 dip #1. Dip grade: correct (via fs-search workaround at dip time).",
    ),
    Question(
        "Q2", "Who ordered the Red Wedding?", "traversal",
        ["the Red Wedding"],
        ["red-wedding", "walder-frey", "roose-bolton", "tywin-lannister"],
        ["resolve", "participants", "neighbors"],
        "Mode-3 dip #2. Dip grade: partial. tywin-lannister included but NOT expected "
        "reachable via edges from red-wedding (accepted dark-historical gap).",
    ),
    Question(
        "Q3", "Who crowned Lyanna Queen of Love and Beauty?", "traversal",
        ["Lyanna crowned queen of love and beauty", "Lyanna Stark"],
        ["lyanna-stark", "rhaegar-targaryen"],
        ["resolve", "neighbors"],
        "Mode-3 dip #3. Dip grade: correct (via fs-search workaround at dip time).",
    ),
    Question(
        "Q4", "What weapon killed Robb Stark?", "quote-hunter",
        ["Robb Stark's death"],
        ["robb-is-killed"],
        ["resolve", "neighbors", "read"],
        "Mode-3 dip #4. Post-dip re-grade: not-applicable, not a graph defect "
        "(unnamed generic longsword; WIELDED_IN requires a named artifact).",
    ),
    Question(
        "Q5", "Who fought at the Tourney at Harrenhal?", "traversal",
        ["Tourney at Harrenhal"],
        ["tourney-at-harrenhal"],
        ["resolve", "neighbors", "theme"],
        "Mode-3 dip #5. Dip grade: failed, 0 edges on hub. Reframed post-dip as "
        "historical-hub-attachment (not this Track's fix).",
    ),
    Question(
        "Q6", "How are Tywin Lannister and Gregor Clegane connected?", "traversal",
        ["Tywin Lannister", "Gregor Clegane"],
        ["tywin-lannister", "gregor-clegane"],
        ["resolve", "path"],
        "Mode-3 dip #6. Dip grade: correct, best-in-class. path has no bounded-profile "
        "port yet (PLANNED step 6b) -- this row also measures that port gap.",
    ),
    Question(
        "Q7", "Who attended Ned Stark's execution?", "traversal",
        ["Ned Stark's execution", "Eddard Stark"],
        ["execution-of-eddard-stark", "eddard-stark"],
        ["resolve", "participants", "neighbors"],
        "Mode-3 dip #7. Dip grade: partial (perpetrators+weapon present; crowd absent).",
    ),
    Question(
        "Q8", "What is Jon Snow's relationship to Ned Stark, who is he sworn to, "
        "and where was he born?", "traversal",
        ["Jon Snow", "Eddard Stark"],
        ["jon-snow", "eddard-stark"],
        ["resolve", "neighbors", "family_tree"],
        "Mode-3 dip #8. Dip grade: correct (BORN_AT absence treated as restraint).",
    ),
    Question(
        "Q9", "What set the incident at the Trident (Joffrey/Mycah/Nymeria) in motion?",
        "traversal",
        ["incident at the Trident", "Mycah"],
        ["incident-at-the-trident", "mycah"],
        ["resolve", "chain"],
        "Mode-3 dip #9. Dip grade: failed (EXPECTED baseline -- hub not yet minted).",
    ),
    Question(
        "Q10", "What were the consequences of the Battle of the Trident?", "traversal",
        ["Battle of the Trident"],
        ["battle-of-the-trident"],
        ["resolve", "chain"],
        "Mode-3 dip #10. Dip grade: failed (no causal edges radiate from the hub).",
    ),
    Question(
        "Q11", "Describe some detailed meals in the books.", "thematic",
        [],  # deliberately no single entity phrase -- the S188 live-failure shape
        ["lemon-cake", "honeyed-ham", "bowl-of-brown", "fish-stew", "guest-right"],
        ["search", "list", "theme"],
        "THE S188 LIVE FAILURE. No content-first op exists yet in either profile "
        "(search/list/theme all PLANNED). Marked loop-bound by construction.",
    ),
    Question(
        "Q12", "Who is Aegon the Conqueror?", "quote-hunter",
        ["Aegon the Conqueror"],
        ["aegon-i-targaryen"],
        ["resolve", "read"],
        "S177 marquee resolve. Confirmed live: exact-miss -> character-name hit "
        "(full) / exact alias-map hit (bounded).",
    ),
    Question(
        "Q13", "Trace the Targaryen dynasty.", "traversal",
        ["Targaryen dynasty", "House Targaryen"],
        ["house-targaryen", "aegon-i-targaryen"],
        ["resolve", "family_tree"],
        "S177 marquee resolve. 'Targaryen dynasty' bare phrase is a MISS-to-fuzzy "
        "in both profiles as of 2026-07-04; 'House Targaryen' resolves cleanly.",
    ),
    Question(
        "Q14", "How did Robb Stark die?", "quote-hunter",
        ["Robb Stark's death"],
        ["robb-is-killed"],
        ["resolve", "read"],
        "Explicit required question. Same resolve mechanics as Q1/Q4 (G19).",
    ),
    Question(
        "Q15", "What are lemon cakes and who eats them?", "quote-hunter",
        ["lemon cakes"],
        ["lemon-cake"],
        ["resolve", "read", "search"],
        "Explicit required question -- G2's own worked example. Live node is "
        "singular 'lemon-cake' with 0 quotes.",
    ),
    Question(
        "Q16", "What does the graph say about hospitality customs (guest right, "
        "welcoming guests)?", "thematic",
        ["guest right", "hospitality"],
        ["guest-right", "catelyn-secures-guest-right"],
        ["resolve", "read", "theme"],
        "Required hospitality thematic question. 'guest right' resolves exactly "
        "today (control row: thematic archetype that already mostly works).",
    ),
    Question(
        "Q17", "Does the graph support the claim that Tywin Lannister orchestrated "
        "the Red Wedding?", "researcher",
        ["Tywin Lannister", "the Red Wedding"],
        ["tywin-lannister", "red-wedding"],
        ["resolve", "neighbors", "chain"],
        "Required researcher claim-check (negative control): both entities resolve "
        "fine, but no connecting edge exists -- correct answer requires reasoning "
        "about an ABSENCE.",
    ),
    Question(
        "Q18", "Is it true that Ned Stark was executed with a named ancestral sword, "
        "and if so which one?", "researcher",
        ["Ned Stark's execution"],
        ["execution-of-eddard-stark"],
        ["resolve", "neighbors"],
        "Researcher claim-check (positive control, pairs with Q7/Q4): WIELDED_IN -> "
        "ice IS present on this hub.",
    ),
    Question(
        "Q19", "What connects Jaime Lannister's confession about Tysha to later "
        "events?", "traversal",
        ["Jaime Lannister", "Tysha"],
        ["jaime-reveals-the-truth-of-tysha"],
        ["resolve", "chain"],
        "Positive-control causal-chain case (named fork-hub in operations.md's "
        "braid section: out=3, reach=11).",
    ),
    Question(
        "Q20", "Walk the Targaryen family tree from Aegon the Conqueror down to "
        "Daenerys.", "traversal",
        ["Aegon the Conqueror"],
        ["aegon-i-targaryen", "daenerys-targaryen"],
        ["resolve", "family_tree"],
        "Positive-control family_tree case (operations.md's own deep-main-line-"
        "spine verification anchor, 12 PARENT_OF hops).",
    ),
]

assert len(QUESTIONS) == 20, f"expected 20 questions, got {len(QUESTIONS)}"
assert len({q.id for q in QUESTIONS}) == 20, "duplicate question id"


# ---------------------------------------------------------------------------
# Bounded-profile resolver -- a FAITHFUL PORT of web/src/lib/{resolve,normalize}.ts.
#
# This is not a re-derivation of what the bundle "should" do -- it mirrors the TS
# lookup semantics line-for-line (normalize -> exact alias-map hit -> fuzzy
# token-overlap w/ slug bonus) reading the SAME on-disk bundle files the Netlify
# Edge function loads. Ported (not shelled-out-to-deno) because: (a) no `deno`
# dependency for a read-only eval script, (b) the logic is ~40 lines and small
# enough that a faithful port is low-risk, (c) it can be run in the same process
# as the full-profile Python resolver, so scoring both profiles per question is
# one pass. If this ever drifts from resolve.ts, the golden parity cases in
# graph/query/spec/cases/resolve.json are the authoritative drift alarm, not this
# script -- this script only needs to be CLOSE ENOUGH to report accurate HIT/MISS
# outcomes for the eval's purposes.
# ---------------------------------------------------------------------------

_LEADING_ARTICLE = re.compile(r"^(the|a|an)\s+")
_WHITESPACE = re.compile(r"\s+")
_WORD = re.compile(r"[^\W\d_]+|\d+", re.UNICODE)  # approximates \p{L}\p{N}_ combined runs

_STOP = {
    "of", "the", "a", "an", "at", "in", "on", "by", "to", "and", "for", "s",
    "who", "what", "where", "when", "how", "which", "whom",
    "did", "does", "do", "is", "was", "were", "are", "has", "have", "had",
}

MIN_FUZZY_SCORE = 0.5
MAX_FUZZY_CANDIDATES = 5
SLUG_BONUS = 0.05


def ts_normalize(phrase: str) -> str:
    p = phrase.lower().strip()
    p = _LEADING_ARTICLE.sub("", p)
    p = _WHITESPACE.sub(" ", p).strip()
    return p


def ts_tokenize(phrase: str) -> set[str]:
    tokens: set[str] = set()
    for m in re.finditer(r"[^\W\d_]+|\d+|[\w]+", phrase.lower(), re.UNICODE):
        t = m.group(0)
        if t and t not in _STOP:
            tokens.add(t)
    return tokens


@dataclass
class BoundedResolver:
    """Reads web/data/{alias-map,nodes,edges}.json once; resolves like resolve.ts."""

    alias_map: dict[str, list[dict]]
    nodes: dict[str, dict]
    edges: list[dict]

    @classmethod
    def load(cls, bundle_dir: Path = BUNDLE_DIR) -> "BoundedResolver":
        with open(bundle_dir / "alias-map.json", encoding="utf-8") as f:
            alias_map = json.load(f)
        with open(bundle_dir / "nodes.json", encoding="utf-8") as f:
            nodes = json.load(f)
        with open(bundle_dir / "edges.json", encoding="utf-8") as f:
            edges = json.load(f)
        return cls(alias_map=alias_map, nodes=nodes, edges=edges)

    def _prominence(self, slugs: set[str]) -> dict[str, int]:
        deg = {s: 0 for s in slugs}
        for e in self.edges:
            src, tgt = e.get("source"), e.get("target")
            if src in deg:
                deg[src] += 1
            if tgt in deg:
                deg[tgt] += 1
        return {
            s: deg[s] + 4 * len(self.nodes.get(s, {}).get("quotes", []))
            for s in deg
        }

    def resolve(self, phrase: str) -> list[dict]:
        if not phrase or not phrase.strip():
            return []
        norm = ts_normalize(phrase)

        exact = self.alias_map.get(norm)
        if exact:
            prom = self._prominence({c["slug"] for c in exact})
            out = [
                {
                    "slug": c["slug"],
                    "category": c["category"],
                    "score": 1.0,
                    "matchType": "exact",
                    "prominence": prom.get(c["slug"], 0),
                }
                for c in exact
            ]
            out.sort(key=lambda c: -c["prominence"])
            return out

        query_tokens = ts_tokenize(norm)
        if not query_tokens:
            return []

        best_score: dict[str, float] = {}
        category_of: dict[str, str] = {}
        for phrase_key, candidates in self.alias_map.items():
            cand_tokens = ts_tokenize(phrase_key)
            if not cand_tokens:
                continue
            overlap = len(query_tokens & cand_tokens)
            base = overlap / len(query_tokens)
            if base < MIN_FUZZY_SCORE:
                continue
            for cand in candidates:
                slug = cand["slug"]
                slug_tokens = ts_tokenize(slug.replace("-", " "))
                slug_overlap = len(query_tokens & slug_tokens)
                score = base
                if slug_overlap > 0:
                    score = min(1.0, score + SLUG_BONUS * slug_overlap)
                if score > best_score.get(slug, 0.0):
                    best_score[slug] = score
                if slug not in category_of:
                    category_of[slug] = cand["category"]

        if not best_score:
            return []

        prom = self._prominence(set(best_score.keys()))
        ranked = sorted(
            best_score.items(),
            key=lambda kv: (-kv[1], -prom.get(kv[0], 0)),
        )[:MAX_FUZZY_CANDIDATES]
        return [
            {
                "slug": slug,
                "category": category_of.get(slug, ""),
                "score": round(score, 3),
                "matchType": "fuzzy",
                "prominence": prom.get(slug, 0),
            }
            for slug, score in ranked
        ]


# ---------------------------------------------------------------------------
# Full-profile resolver wrapper (thin -- weirwood_query.resolve already IS the
# full-profile engine; this just loads its tables once for reuse across
# questions).
# ---------------------------------------------------------------------------


@dataclass
class FullResolver:
    lookup: dict[str, str]
    all_node_index: dict[str, list[dict]]
    collisions: dict[str, list[dict]]

    @classmethod
    def load(cls) -> "FullResolver":
        return cls(
            lookup=R.load_alias_lookup(),
            all_node_index=L.load_all_node_index(),
            collisions=R.load_alias_collisions(),
        )

    def resolve(self, phrase: str) -> tuple[str | None, str, list[dict]]:
        return R.resolve(
            phrase, self.lookup, self.all_node_index, collisions=self.collisions
        )


# ---------------------------------------------------------------------------
# Resolve-outcome classification -- shared vocabulary for both profiles.
# ---------------------------------------------------------------------------

# HIT | HIT-CHARACTER | AMBIGUOUS | FUZZY(top, correct?) | MISS
RESOLVE_OUTCOMES = ("HIT", "HIT-CHARACTER", "AMBIGUOUS", "FUZZY", "MISS")


def classify_full(status: str, slug: str | None, candidates: list[dict],
                   target_slugs: list[str]) -> dict[str, Any]:
    if status == "hit":
        return {"outcome": "HIT", "top": slug, "correct": slug in target_slugs}
    if status == "hit-character":
        return {"outcome": "HIT-CHARACTER", "top": slug, "correct": slug in target_slugs}
    if status == "ambiguous":
        return {"outcome": "AMBIGUOUS", "top": None, "correct": False}
    if status == "candidates":
        top = candidates[0]["slug"] if candidates else None
        return {
            "outcome": "FUZZY",
            "top": top,
            "correct": top in target_slugs if top else False,
            "candidates": [c["slug"] for c in candidates],
        }
    return {"outcome": "MISS", "top": None, "correct": False}


def classify_bounded(candidates: list[dict], target_slugs: list[str]) -> dict[str, Any]:
    if not candidates:
        return {"outcome": "MISS", "top": None, "correct": False}
    top = candidates[0]
    outcome = "HIT" if top["matchType"] == "exact" else "FUZZY"
    return {
        "outcome": outcome,
        "top": top["slug"],
        "correct": top["slug"] in target_slugs,
        "candidates": [c["slug"] for c in candidates],
    }


# ---------------------------------------------------------------------------
# Content-reachable check: do target slugs exist, and do they carry quotes?
# ---------------------------------------------------------------------------


def content_reachable(target_slugs: list[str], bundle_nodes: dict[str, dict]) -> dict[str, Any]:
    per_slug = {}
    for slug in target_slugs:
        node = bundle_nodes.get(slug)
        per_slug[slug] = {
            "exists": node is not None,
            "quote_count": len(node.get("quotes", [])) if node else 0,
        }
    existing = [s for s in target_slugs if per_slug[s]["exists"]]
    with_quotes = [s for s in target_slugs if per_slug[s]["quote_count"] > 0]
    return {
        "per_slug": per_slug,
        "all_exist": len(existing) == len(target_slugs),
        "any_exist": len(existing) > 0,
        "any_with_quotes": len(with_quotes) > 0,
    }


# ---------------------------------------------------------------------------
# Estimated minimum tool calls under the bounded profile's CURRENT toolset
# (resolve / read_node / walk_chain / neighbors / family_tree -- no search).
#
# Heuristic (documented, mechanical, not vibes):
#   1. If a question's `ops` list requires an op NOT in the current bounded
#      toolset at all (search, list, theme, participants, path, container,
#      expand-beats) AND no fallback via resolve+read/neighbors/chain/family_tree
#      can plausibly answer it (per the question's own target-slug content
#      reachability), the question is LOOP-BOUND (∞) -- the toolset structurally
#      cannot reach the answer, regardless of how many calls are spent.
#   2. Otherwise: 1 resolve call per DISTINCT key phrase that is needed (a
#      question needing 2 entities needs 2 resolves), plus 1 read/neighbors/
#      chain/family_tree call per resolved entity that must be inspected.
#      - traversal questions needing a relationship between 2 resolved entities:
#        resolves(len(key_phrases)) + 1 relational call (neighbors/chain/family_tree)
#        = len(key_phrases) + 1
#      - single-entity quote-hunter / researcher-single-hub questions:
#        resolves(len(key_phrases)) + 1 read/neighbors call
#        = len(key_phrases) + 1  (same shape, different op)
#      - if a key phrase currently MISSES in the bounded profile (both stages),
#        that resolve alone doesn't ground anything -- but the model would need
#        at least one more attempt (a retry / alternate phrasing) before it can
#        proceed, or the question degrades to loop-bound if no phrase resolves
#        at all. This adds +1 per missed phrase (a documented, mechanical retry
#        cost) rather than silently assuming a free pass.
#   3. A question with 0 key_phrases (Q11 -- the meals question, by design) is
#      always loop-bound today -- there is no phrase to resolve at all.
#   4. `family_tree`-shaped questions collapse to 1 relational call regardless
#      of how many downstream members are named (family_tree returns the whole
#      tree in one call, per the design doc's own MANDATORY-tool framing).
#
# This heuristic is intentionally conservative and mechanical so it can be
# re-run identically after every step; it is NOT a live-model measurement (that
# column stays GATED below).
# ---------------------------------------------------------------------------

# Ops available in the bounded profile's CURRENT chat toolset (5 tools, no search).
BOUNDED_TOOLSET_OPS = {"resolve", "read", "neighbors", "chain", "family_tree"}


def estimate_min_tool_calls(
    q: Question,
    bounded_resolve_by_phrase: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    # Rule 3: no key phrase at all -> structurally loop-bound.
    if not q.key_phrases:
        return {"estimate": None, "loop_bound": True, "reason": "no key phrase to resolve"}

    # Rule 1: does this question fundamentally need an op outside the current
    # bounded toolset, with no reachable fallback?
    needs_unavailable_op = any(op not in BOUNDED_TOOLSET_OPS for op in q.ops)
    # "path" specifically has no bounded port (G-table); "participants",
    # "theme", "search", "list", "container", "expand-beats" likewise absent.
    # A fallback via neighbors/chain/family_tree is only plausible if the
    # question's archetype is traversal/researcher AND at least one phrase hits.
    any_phrase_resolves = any(
        bounded_resolve_by_phrase[p]["outcome"] != "MISS" for p in q.key_phrases
    )
    if needs_unavailable_op and q.archetype == "thematic" and not any_phrase_resolves:
        # thematic questions with an unavailable op (search/theme/list) AND no
        # phrase that resolves at all have no fallback whatsoever -- content-first
        # ops ARE the only possible answer path. (A thematic question where SOME
        # phrase resolves today, e.g. Q16's "guest right", is scored under the
        # normal resolve+read fallback below instead -- it is not loop-bound, it
        # is just narrower/shallower than the eventual theme/search op would give.)
        return {
            "estimate": None,
            "loop_bound": True,
            "reason": "requires search/list/theme (not in bounded toolset); "
                      "no key phrase resolves at all, so no resolve-shaped fallback "
                      "either",
        }

    # Count resolve calls: 1 per key phrase, +1 retry cost per phrase that misses.
    resolve_calls = 0
    for p in q.key_phrases:
        resolve_calls += 1
        if bounded_resolve_by_phrase[p]["outcome"] == "MISS":
            resolve_calls += 1  # documented retry cost

    if not any_phrase_resolves:
        return {
            "estimate": None,
            "loop_bound": True,
            "reason": "every key phrase misses in the bounded profile; no entity "
                      "to read/walk/neighbor from",
            "resolve_calls_spent": resolve_calls,
        }

    # Rule 2/4: +1 relational/read call once at least one entity resolved.
    relational_calls = 1
    total = resolve_calls + relational_calls
    return {"estimate": total, "loop_bound": False, "reason": "resolve(s) + one relational call"}


# ---------------------------------------------------------------------------
# Scoring a single question.
# ---------------------------------------------------------------------------


def score_question(
    q: Question,
    full: FullResolver,
    bounded: BoundedResolver,
) -> dict[str, Any]:
    full_resolve_by_phrase = {}
    for phrase in q.key_phrases:
        slug, status, candidates = full.resolve(phrase)
        full_resolve_by_phrase[phrase] = classify_full(status, slug, candidates, q.target_slugs)

    bounded_resolve_by_phrase = {}
    for phrase in q.key_phrases:
        candidates = bounded.resolve(phrase)
        bounded_resolve_by_phrase[phrase] = classify_bounded(candidates, q.target_slugs)

    content = content_reachable(q.target_slugs, bounded.nodes)
    tool_estimate = estimate_min_tool_calls(q, bounded_resolve_by_phrase)

    return {
        "id": q.id,
        "question": q.text,
        "archetype": q.archetype,
        "key_phrases": q.key_phrases,
        "target_slugs": q.target_slugs,
        "ops": q.ops,
        "notes": q.notes,
        "resolve_full": full_resolve_by_phrase,
        "resolve_bounded": bounded_resolve_by_phrase,
        "content_reachable": content,
        "tool_estimate": tool_estimate,
        # Live-model columns -- GATED on Matt. Present, empty, documented.
        "live_model": {
            "answered": None,
            "grounded": None,
            "actual_tool_calls": None,
            "note": "GATED on Matt -- requires API spend or a local weirwood-live run; "
                    "not populated by this deterministic runner.",
        },
    }


# ---------------------------------------------------------------------------
# Report rendering.
# ---------------------------------------------------------------------------


def render_table(results: list[dict[str, Any]]) -> str:
    lines = []
    header = (
        "| id | archetype | resolve (full) | resolve (bounded) | content reachable | "
        "min tool calls (bounded) | live-model (GATED) |"
    )
    sep = "|---|---|---|---|---|---|---|"
    lines.append(header)
    lines.append(sep)
    for r in results:
        full_summary = "; ".join(
            f"{p!r}:{v['outcome']}" + (f"->{v['top']}" if v.get("top") else "")
            for p, v in r["resolve_full"].items()
        ) or "(none)"
        bounded_summary = "; ".join(
            f"{p!r}:{v['outcome']}" + (f"->{v['top']}" if v.get("top") else "")
            for p, v in r["resolve_bounded"].items()
        ) or "(none)"
        cr = r["content_reachable"]
        cr_summary = (
            f"exist={sum(1 for s in cr['per_slug'].values() if s['exists'])}/"
            f"{len(cr['per_slug'])}, quotes={'yes' if cr['any_with_quotes'] else 'no'}"
        )
        te = r["tool_estimate"]
        te_summary = "∞ (loop-bound)" if te["loop_bound"] else str(te["estimate"])
        lines.append(
            f"| {r['id']} | {r['archetype']} | {full_summary} | {bounded_summary} | "
            f"{cr_summary} | {te_summary} | (empty, gated) |"
        )
    return "\n".join(lines)


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(results)
    fully_resolve_bounded = sum(
        1 for r in results
        if r["key_phrases"] and all(
            v["outcome"] in ("HIT",) for v in r["resolve_bounded"].values()
        )
    )
    any_hit_bounded = sum(
        1 for r in results
        if any(v["outcome"] == "HIT" for v in r["resolve_bounded"].values())
    )
    any_fuzzy_bounded = sum(
        1 for r in results
        if any(v["outcome"] == "FUZZY" for v in r["resolve_bounded"].values())
    )
    all_miss_bounded = sum(
        1 for r in results
        if r["key_phrases"] and all(v["outcome"] == "MISS" for v in r["resolve_bounded"].values())
    )
    loop_bound = [r["id"] for r in results if r["tool_estimate"]["loop_bound"]]
    no_key_phrase = [r["id"] for r in results if not r["key_phrases"]]

    return {
        "total_questions": n,
        "fully_exact_resolve_bounded": fully_resolve_bounded,
        "any_hit_bounded": any_hit_bounded,
        "any_fuzzy_bounded": any_fuzzy_bounded,
        "all_miss_bounded": all_miss_bounded,
        "loop_bound_questions": loop_bound,
        "loop_bound_count": len(loop_bound),
        "questions_with_no_key_phrase": no_key_phrase,
    }


def render_report(results: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    today = date.today().isoformat()
    parts = []
    parts.append(f"# Query-Layer Eval Baseline — {today}\n")
    parts.append(
        "> Produced by `python3 working/query-layer/evals/run_evals.py --report`. "
        "Zero API spend, zero network calls — every number below is computed from "
        "the live graph/query engine + web/data/ bundle at run time. This is the "
        "FROZEN snapshot; re-run the script after any retrieval-touching step to "
        "compare (the script itself has no baked-in expected values).\n"
    )
    parts.append("## Summary\n")
    parts.append(f"- **Total questions:** {summary['total_questions']}")
    parts.append(
        f"- **Fully exact-resolve (bounded profile, ALL key phrases HIT):** "
        f"{summary['fully_exact_resolve_bounded']}/{summary['total_questions']}"
    )
    parts.append(
        f"- **At least one key phrase HITs (bounded):** "
        f"{summary['any_hit_bounded']}/{summary['total_questions']}"
    )
    parts.append(
        f"- **At least one key phrase falls to FUZZY (bounded):** "
        f"{summary['any_fuzzy_bounded']}"
    )
    parts.append(
        f"- **All key phrases MISS (bounded):** {summary['all_miss_bounded']}"
    )
    parts.append(
        f"- **Loop-bound under the current bounded toolset (∞ tool calls):** "
        f"{summary['loop_bound_count']}/{summary['total_questions']} "
        f"({', '.join(summary['loop_bound_questions'])})"
    )
    if summary["questions_with_no_key_phrase"]:
        parts.append(
            f"- **Questions with no single key phrase to resolve (thematic-only):** "
            f"{', '.join(summary['questions_with_no_key_phrase'])}"
        )
    parts.append("")
    parts.append(
        "## Known-bad marquee cases\n\n"
        "- **G19** — `Robb Stark's death` (Q1/Q4/Q14): falls to FUZZY, not HIT, in the "
        "bounded profile (victim-phrase alias source not yet merged into the bundle's "
        "alias-map.json — fix is step 4a).\n"
        "- **G2** — `lemon cakes` (Q15): MISS on the intended food node in both profiles "
        "for the plural phrasing; the live node is singular `lemon-cake` with 0 quotes "
        "(fix is step 4b variant-expansion + step 5 content search).\n"
        "- **G10** — bare `Tywin` / short single-token phrases can rank a different "
        "character above the intended one (no candidate-length penalty; fix is step 4c). "
        "Not directly one of Q1–Q20's key phrases (all use fuller phrasings), but the "
        "same mechanism affects Q13's fuzzy fallback (`Targaryen dynasty`).\n"
        "- **Q11 (the meals question)** — loop-bound by construction: zero key phrases, "
        "no content-first op (search/list/theme) exists in either profile yet. This is "
        "the metric step 5 must flip.\n"
    )
    parts.append("## Per-question detail\n")
    parts.append(render_table(results))
    parts.append("")
    parts.append(
        "## Live-model columns\n\n"
        "GATED on Matt's explicit OK — not populated in this baseline. When approved, "
        "a live run (local `weirwood-live` only, never prod) would fill: answered? "
        "(bool), grounded? (bool, per the cite-verification gate in "
        "`web/netlify/edge-functions/lib/agent.ts`), actual tool calls used (int).\n"
    )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", action="store_true",
                     help="also write the dated baseline-<date>.md report file")
    ap.add_argument("--json", action="store_true", help="dump raw JSON instead of a table")
    args = ap.parse_args()

    full = FullResolver.load()
    bounded = BoundedResolver.load()

    results = [score_question(q, full, bounded) for q in QUESTIONS]
    summary = summarize(results)

    if args.json:
        print(json.dumps({"summary": summary, "results": results}, indent=2, default=str))
        return

    print(render_table(results))
    print()
    print(json.dumps(summary, indent=2))

    if args.report:
        report_text = render_report(results, summary)
        out_path = EVALS_DIR / f"baseline-{date.today().isoformat()}.md"
        out_path.write_text(report_text, encoding="utf-8")
        print(f"\nWrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
