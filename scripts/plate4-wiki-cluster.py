#!/usr/bin/env python3
"""plate4-wiki-cluster.py — classify Plate-3 mints against wiki event-nodes.

For each Plate-3 mint (`working/edge-modeling/plate3-full/minted-event-nodes/`),
narrow to ~5-15 candidate wiki event-nodes via DETERMINISTIC signals, then
ask an LLM to classify the relationship.

Hybrid narrowing signals (all deterministic, $0):
  1. CHAPTER match — mint's source chapter ∈ wiki event's chapter_evidence (when present).
  2. WIKI-LINK tokens — wiki node body has `(wiki:X)` references that proxy participants;
     overlap with mint's role-edge characters scores match strength. (This is the
     load-bearing signal — red-wedding.node.md has ZERO person-edges but its body
     mentions Walder_Frey, Roose_Bolton, Robb_Stark, Catelyn_Stark as wiki-links.)
  3. BOOK proximity — mint's source book vs wiki node's evidence_book.
  4. TRIGGER-FAMILY match — mint's keyword family (kill/wedding/siege/capture)
     vs wiki node's type and title keywords.

LLM classification output per mint:
  best_match: <wiki_event_slug> | "none"
  suggested_action: "sub-beat-of" | "duplicate-of" | "distinct"
  equivalence_evidence_strength: "direct-textual" | "inference-only"
  rationale: <1-2 sentences>
  quoted_evidence: <verbatim quote from wiki body that supports the match, or "">

Two-tier model cascade:
  Pass A: claude-haiku-4-5-20251001 (cheap, fast). Auto-accept direct-textual matches.
  Pass B: claude-opus-4-7 (expensive, judgment) — run only on Pass A's
    `distinct` returns and `inference-only` returns. Separate process invocation
    (avoids the shared process-wide _RATE_LIMIT_WALL flag killing Pass B).

Inherits architecture from scripts/edge-reify-backfill.py:
  - Ledger (processed-mints.jsonl) for --resume
  - Incremental flush to wiki-cluster-assignments.jsonl
  - Fail-fast on rate-limit wall (empty-stderr exit-1 → wall, no silent loss)
  - cwd="/tmp" for claude -p calls (~49% cost savings, skips repo CLAUDE.md)
  - --max-events N for bounded chunks (the 20-mint PILOT)
  - Thread pool concurrency=3 by default (Haiku finishes faster than Sonnet →
    hits rate limit faster at same parallelism)
  - Errors NOT written to ledger (retryable on --resume)
  - Parse failures route to a separate file (Haiku JSON-failure rate higher than Sonnet)

Usage:
  # 20-mint pilot (Pass A, Haiku)
  python3 scripts/plate4-wiki-cluster.py --max-events 20

  # Full Pass A
  python3 scripts/plate4-wiki-cluster.py --resume

  # Pass B (Opus on Pass A's distinct + inference-only returns)
  python3 scripts/plate4-wiki-cluster.py --pass B \\
    --model claude-opus-4-7 \\
    --pass-a-results working/edge-modeling/plate4-wiki-cluster/wiki-cluster-assignments.jsonl \\
    --output-dir working/edge-modeling/plate4-wiki-cluster-passb/
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Repo layout
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parent.parent
_PLATE3_OUT = _REPO / "working" / "edge-modeling" / "plate3-full"
_PLATE3_MINTS = _PLATE3_OUT / "minted-event-nodes"
_PLATE3_LEDGER = _PLATE3_OUT / "processed-events.jsonl"
_PLATE3_ROLE_EDGES = _PLATE3_OUT / "role-edges-staging.jsonl"
_WIKI_EVENT_NODES = _REPO / "graph" / "nodes" / "events"

# Default output
_DEFAULT_OUT = _REPO / "working" / "edge-modeling" / "plate4-wiki-cluster"

# ---------------------------------------------------------------------------
# Rate-limit / quota-wall handling (preserved verbatim from edge-reify-backfill.py)
# ---------------------------------------------------------------------------

_RATE_LIMIT_STDERR_PATTERNS = [
    "rate limit", "rate_limit", "quota", "overloaded", "too many requests",
    "429", "529", "usage limit", "credit balance",
]

_RATE_LIMIT_WALL = threading.Event()
_WRITE_LOCK = threading.Lock()


class RateLimitError(RuntimeError):
    """Raised when claude -p returns a hard rate-limit / quota-exhausted error."""


def _is_rate_limit_error(returncode: int, stderr: str, stdout: str = "") -> bool:
    """Return True if the subprocess failure looks like a hard rate-limit wall.

    Includes the empty-stderr fix (load-bearing — without it, the 5-hour wall causes
    silent failures that get incorrectly marked done in the ledger).
    """
    if returncode not in (1, 2):
        return False
    combined = (stderr or "").lower() + " " + (stdout or "").lower()
    if any(pat in combined for pat in _RATE_LIMIT_STDERR_PATTERNS):
        return True
    if not (stderr or "").strip():
        return True
    return False


# ---------------------------------------------------------------------------
# Trigger families — for narrowing candidates by event type similarity
# ---------------------------------------------------------------------------

_TRIGGER_FAMILIES = {
    "kill": {"kill", "kills", "killed", "murder", "slain", "slay", "slays", "slaughter",
             "massacre", "stabbed", "stab", "throat-cut", "beheaded", "beheading", "died", "dies", "death"},
    "wedding": {"wedding", "weddings", "bedding", "ceremony", "ceremonies"},
    "execution": {"execution", "executed", "executes"},
    "assassination": {"assassination", "assassinate", "assassinated", "poison", "poisoned", "poisoning"},
    "siege": {"siege", "sieges", "sack", "sacks", "sacked", "sacking"},
    "battle": {"battle", "battles", "attack", "attacks", "ambush", "ambushes", "assault", "assaults",
               "conquest", "skirmish"},
    "capture": {"capture", "captures", "captured", "hostage", "prisoner", "imprisoned", "arrest", "arrested"},
    "betrayal": {"betrayal", "betrays", "betrayed", "betray", "guest-right"},
    "coronation": {"coronation", "crowning", "crowned"},
}


def trigger_family_of(text: str) -> set[str]:
    """Return the set of trigger family labels that appear in the text."""
    tokens = re.findall(r"[a-z]+", text.lower())
    families: set[str] = set()
    for fam, keywords in _TRIGGER_FAMILIES.items():
        if any(kw in text.lower() for kw in keywords) or any(t in keywords for t in tokens):
            families.add(fam)
    return families


# ---------------------------------------------------------------------------
# Parsers — Plate-3 mints, wiki event-nodes, role edges
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
_WIKI_LINK_RE = re.compile(r"\(wiki:([A-Za-z0-9_\-\(\)']+)\)")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body) from a markdown file with YAML frontmatter."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_raw = m.group(1)
    body = m.group(2)
    fm: dict[str, Any] = {}
    for line in fm_raw.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        # List continuation — check FIRST (these lines have no colon, e.g. "  - ASOS Catelyn VII")
        if line.startswith("  - "):
            last_key = list(fm.keys())[-1] if fm else None
            if last_key and isinstance(fm[last_key], list):
                fm[last_key].append(line[4:].strip().strip('"').strip("'"))
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            fm[k] = [s.strip().strip('"').strip("'") for s in inner.split(",")] if inner else []
        elif not v:
            fm[k] = []  # may become a list via continuation
        else:
            fm[k] = v.strip('"').strip("'")
    return fm, body


def chapter_label_to_id(label: str) -> str:
    """Convert 'ASOS Catelyn VII' → 'asos-catelyn-07'. Returns label lower-stripped if can't parse."""
    label = label.strip()
    m = re.match(r"^([A-Z]+)\s+([A-Za-z]+)\s+([IVXLC]+|\d+)$", label)
    if not m:
        return label.lower().replace(" ", "-")
    book = m.group(1).lower()
    pov = m.group(2).lower()
    chap = m.group(3)
    # Roman → int
    if not chap.isdigit():
        romans = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
        n = 0
        prev = 0
        for c in reversed(chap):
            v = romans.get(c, 0)
            if v < prev:
                n -= v
            else:
                n += v
            prev = v
        chap = f"{n:02d}"
    else:
        chap = f"{int(chap):02d}"
    return f"{book}-{pov}-{chap}"


def book_from_chapter_id(chapter_id: str) -> str:
    """asos-catelyn-07 → asos."""
    parts = chapter_id.split("-")
    return parts[0] if parts else ""


def parse_plate3_mint(node_path: Path) -> dict:
    """Return {slug, title, source_chapter_id, source_book, evidence_chapter_labels}."""
    text = node_path.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)
    chapter_labels = fm.get("evidence_chapters", []) or []
    chapter_ids = [chapter_label_to_id(c) for c in chapter_labels] if chapter_labels else []
    book = book_from_chapter_id(chapter_ids[0]) if chapter_ids else ""
    return {
        "slug": fm.get("slug", node_path.stem.replace(".node", "")),
        "title": fm.get("title", ""),
        "source_chapter_ids": chapter_ids,
        "source_chapter_labels": chapter_labels,
        "source_book": book,
        "type": fm.get("type", ""),
    }


def parse_wiki_event_node(node_path: Path) -> dict:
    """Return {slug, type, aliases, body_summary, wiki_link_tokens, evidence_book, ...}."""
    text = node_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    slug = fm.get("slug") or node_path.stem.replace(".node", "")
    # Extract wiki-link tokens — the real participant proxy
    raw_tokens = set(_WIKI_LINK_RE.findall(body))
    # Normalize: lowercase, replace _ with -, drop trailing ()/.cite suffixes
    wiki_link_slugs: set[str] = set()
    for tok in raw_tokens:
        clean = tok.split(".")[0]  # drop .cite_ref-... suffixes
        clean = clean.split("(")[0].strip("_-")  # drop disambiguation suffix
        if not clean:
            continue
        slug_form = clean.lower().replace("_", "-")
        if len(slug_form) > 2 and not slug_form.startswith(slug.lower()):  # skip self-refs
            wiki_link_slugs.add(slug_form)
    # First ~300 chars of body for description (skip ## Identity boilerplate)
    body_clean = re.sub(r"^\s*##\s*Identity\s*\n.*?(?=\n##|\Z)", "", body, flags=re.DOTALL)
    body_clean = re.sub(r"\(wiki:[^)]+\)", "", body_clean)  # strip wiki-link parens
    body_clean = re.sub(r"\[([^\]]+)\]", r"\1", body_clean)  # unwrap [text] markdown
    body_clean = re.sub(r"\s+", " ", body_clean).strip()
    body_summary = body_clean[:400] if body_clean else ""
    return {
        "slug": slug,
        "type": fm.get("type", ""),
        "name": fm.get("name", slug),
        "aliases": fm.get("aliases", []) or [],
        "body_summary": body_summary,
        "wiki_link_slugs": wiki_link_slugs,
        "evidence_book": fm.get("evidence_book", ""),
    }


def load_plate3_role_edges(role_edges_path: Path) -> dict[str, list[dict]]:
    """Group role edges by event hub. AGENT_IN/VICTIM_IN/COMMANDS_IN/WIELDED_IN target=hub;
    LOCATED_AT source=hub."""
    by_hub: dict[str, list[dict]] = {}
    if not role_edges_path.exists():
        return by_hub
    with open(role_edges_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                edge = json.loads(line)
            except json.JSONDecodeError:
                continue
            et = edge.get("edge_type", "")
            if et == "LOCATED_AT":
                hub = edge.get("source_slug", "")
            else:
                hub = edge.get("target_slug", "")
            if hub:
                by_hub.setdefault(hub, []).append(edge)
    return by_hub


# ---------------------------------------------------------------------------
# Candidate narrowing
# ---------------------------------------------------------------------------

def participant_slugs_for_mint(mint_slug: str, role_edges_by_hub: dict[str, list[dict]]) -> set[str]:
    """Extract the set of participant character/house slugs from a mint's role edges."""
    edges = role_edges_by_hub.get(mint_slug, [])
    participants: set[str] = set()
    for e in edges:
        et = e.get("edge_type", "")
        if et in ("AGENT_IN", "VICTIM_IN", "COMMANDS_IN", "WIELDED_IN"):
            s = e.get("source_slug", "")
            if s:
                participants.add(s.lower())
        elif et == "LOCATED_AT":
            t = e.get("target_slug", "")
            if t:
                participants.add(t.lower())
    return participants


def narrow_candidates(
    mint: dict,
    mint_participants: set[str],
    wiki_events: list[dict],
    top_k: int = 12,
) -> list[tuple[dict, float, dict]]:
    """Score each wiki event vs the mint; return top_k (event, score, signal_breakdown).

    Signals (additive; tuned for recall over precision since LLM will judge):
      +3.0 if mint book == wiki book (rare; mostly absent)
      +1.0 per overlap between mint_participants and wiki.wiki_link_slugs (cap 5)
      +2.0 per shared trigger family
      +0.5 if mint type == wiki type
    """
    mint_title = mint.get("title", "")
    mint_slug = mint.get("slug", "")
    mint_book = mint.get("source_book", "")
    mint_families = trigger_family_of(mint_title + " " + mint_slug)
    mint_type = mint.get("type", "")

    scored: list[tuple[dict, float, dict]] = []
    for wiki in wiki_events:
        breakdown: dict[str, Any] = {}
        score = 0.0

        # Book proximity
        if mint_book and wiki.get("evidence_book") == mint_book:
            score += 3.0
            breakdown["book_match"] = 3.0

        # Participant overlap (capped 5 — beyond that it's noise)
        wiki_slugs = wiki.get("wiki_link_slugs", set())
        overlap = mint_participants & wiki_slugs
        if overlap:
            o_score = min(len(overlap), 5) * 1.0
            score += o_score
            breakdown["participant_overlap"] = {"score": o_score, "overlapping": sorted(overlap)[:8]}

        # Trigger family match
        wiki_text = (wiki.get("name", "") + " " + wiki.get("body_summary", "")[:100] + " " + wiki.get("slug", ""))
        wiki_families = trigger_family_of(wiki_text)
        family_overlap = mint_families & wiki_families
        if family_overlap:
            f_score = len(family_overlap) * 2.0
            score += f_score
            breakdown["trigger_family"] = {"score": f_score, "shared": sorted(family_overlap)}

        # Type match (event.battle / event.incident / etc.)
        if mint_type and wiki.get("type") == mint_type:
            score += 0.5
            breakdown["type_match"] = 0.5

        if score > 0:
            scored.append((wiki, score, breakdown))

    scored.sort(key=lambda x: -x[1])
    return scored[:top_k]


# ---------------------------------------------------------------------------
# LLM classifier prompt + call
# ---------------------------------------------------------------------------

CLASSIFIER_PROMPT_TEMPLATE = """You are classifying a Plate-3 minted "event hub" against a candidate set of existing wiki event-nodes for the Weirwood Network (an ASOIAF knowledge graph).

MINTED HUB (the thing to classify):
  Slug:        {mint_slug}
  Title:       {mint_title}
  Source chapter: {mint_chapter}
  Source book:    {mint_book}
  Type:        {mint_type}
  Participants from role edges ({n_participants}):
{mint_participants_block}

CANDIDATE WIKI EVENTS ({n_candidates}; narrowed by chapter / participant overlap / trigger family):
{candidates_block}

TASK: Decide whether the minted hub corresponds to one of the candidates. Output ONE of:
  - "sub-beat-of": the mint is a fine-grained beat within the wiki event (e.g. "Lord Walder calls for the bedding" is part of "Red Wedding")
  - "duplicate-of": the mint is the SAME event under different naming
  - "distinct": the mint is genuinely NOT captured by any candidate

CRITICAL RULES:
- Default to "distinct" if uncertain. False positives pollute the graph more than false negatives.
- "direct-textual" = a candidate's body description EXPLICITLY mentions the mint's title or participants. You must quote the matching passage in `quoted_evidence`.
- "inference-only" = match is plausible from context but not directly stated. Use sparingly. Auto-pipeline will route inference-only matches to human review.
- If best_match is "none", suggested_action MUST be "distinct" and quoted_evidence MUST be "".

OUTPUT — exactly this JSON shape, no preamble, no markdown fences:
{{
  "best_match": "<candidate slug>" | "none",
  "suggested_action": "sub-beat-of" | "duplicate-of" | "distinct",
  "equivalence_evidence_strength": "direct-textual" | "inference-only",
  "rationale": "<one or two sentences explaining the decision>",
  "quoted_evidence": "<verbatim quote from the matched candidate's body description that supports the match, or empty string>"
}}
"""


def format_candidates_block(candidates: list[tuple[dict, float, dict]]) -> str:
    lines = []
    for i, (wiki, score, breakdown) in enumerate(candidates, 1):
        lines.append(f"  {i}. {wiki['slug']} (type: {wiki['type']}, narrow_score: {score:.1f})")
        if wiki.get("name") and wiki["name"] != wiki["slug"]:
            lines.append(f"     name: {wiki['name']}")
        summary = wiki.get("body_summary", "")[:300]
        if summary:
            lines.append(f"     body: {summary}")
        wikiparts = sorted(wiki.get("wiki_link_slugs", set()))[:12]
        if wikiparts:
            lines.append(f"     participants (wiki-link): {', '.join(wikiparts)}")
        lines.append("")
    return "\n".join(lines) or "  (no candidates passed narrowing — answer 'none' / 'distinct')"


def format_mint_participants(participants: set[str]) -> str:
    if not participants:
        return "  (none — mint has no role-edge participants)"
    return "\n".join(f"  - {p}" for p in sorted(participants))


def call_claude_for_classification(
    mint: dict,
    mint_participants: set[str],
    candidates: list[tuple[dict, float, dict]],
    model: str,
    max_transient_retries: int = 1,
) -> tuple[dict, dict]:
    """One claude -p call. Returns (parsed_response, usage_info).
    Raises RateLimitError on hard wall.
    """
    prompt = CLASSIFIER_PROMPT_TEMPLATE.format(
        mint_slug=mint["slug"],
        mint_title=mint.get("title", ""),
        mint_chapter=", ".join(mint.get("source_chapter_labels", [])) or mint.get("source_book", ""),
        mint_book=mint.get("source_book", ""),
        mint_type=mint.get("type", ""),
        n_participants=len(mint_participants),
        mint_participants_block=format_mint_participants(mint_participants),
        n_candidates=len(candidates),
        candidates_block=format_candidates_block(candidates),
    )

    cmd = ["claude", "--model", model, "--output-format", "json", "-p", prompt]

    for attempt in range(max_transient_retries + 1):
        if _RATE_LIMIT_WALL.is_set():
            raise RateLimitError("Rate-limit wall set by another thread; aborting.")

        start = time.time()
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                cwd="/tmp",  # non-negotiable per reference_llm_pass_via_claude_p memory
                timeout=180,
            )
        except subprocess.TimeoutExpired as e:
            if attempt < max_transient_retries:
                time.sleep(5)
                continue
            raise RuntimeError(f"claude -p timed out after 180s for mint {mint['slug']!r}") from e

        elapsed = time.time() - start

        if result.returncode != 0:
            stderr_snippet = (result.stderr or "")[:600]
            stdout_snippet = (result.stdout or "")[:300]
            if _is_rate_limit_error(result.returncode, result.stderr, result.stdout):
                if attempt < max_transient_retries:
                    time.sleep(30)
                    continue
                raise RateLimitError(
                    f"Hard rate-limit wall on mint {mint['slug']!r}; stderr={stderr_snippet!r}"
                )
            if attempt < max_transient_retries:
                time.sleep(5)
                continue
            raise RuntimeError(
                f"claude -p exited {result.returncode} for {mint['slug']!r}: "
                f"stderr={stderr_snippet!r} stdout={stdout_snippet!r}"
            )

        # Parse claude -p JSON envelope
        try:
            envelope = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            envelope = {"result": result.stdout.strip(), "usage": {}}

        usage = envelope.get("usage", {})
        in_t = usage.get("input_tokens", 0)
        cc_t = usage.get("cache_creation_input_tokens", 0)
        cr_t = usage.get("cache_read_input_tokens", 0)
        out_t = usage.get("output_tokens", 0)

        # Model pricing (per MTok)
        if "haiku" in model.lower():
            in_p, cc_p, cr_p, out_p = 1.0, 1.25, 0.10, 5.0
        elif "opus" in model.lower():
            in_p, cc_p, cr_p, out_p = 15.0, 18.75, 1.50, 75.0
        else:  # sonnet default
            in_p, cc_p, cr_p, out_p = 3.0, 3.75, 0.30, 15.0
        cost_usd = (in_t * in_p + cc_t * cc_p + cr_t * cr_p + out_t * out_p) / 1_000_000

        content = envelope.get("result", "") or result.stdout.strip()
        content_clean = re.sub(r"^```(?:json)?\s*", "", content.strip())
        content_clean = re.sub(r"\s*```$", "", content_clean.strip())

        try:
            parsed = json.loads(content_clean)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"LLM returned non-JSON for {mint['slug']!r}: {content_clean[:400]!r} (parse error: {e})"
            )

        usage_info = {
            "input_tokens": in_t, "cache_creation_input_tokens": cc_t,
            "cache_read_input_tokens": cr_t, "output_tokens": out_t,
            "cost_usd": cost_usd, "elapsed_seconds": round(elapsed, 1), "model": model,
        }
        return parsed, usage_info

    raise RuntimeError(f"Exhausted retries for mint {mint['slug']!r}")


# ---------------------------------------------------------------------------
# Per-mint processor
# ---------------------------------------------------------------------------

def _append_jsonl_locked(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _WRITE_LOCK:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def write_ledger_entry(ledger_path: Path, mint_slug: str, outcome: str, best_match: str) -> None:
    entry = {
        "mint_slug": mint_slug,
        "outcome": outcome,
        "best_match": best_match,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    _append_jsonl_locked(ledger_path, entry)


def load_ledger(ledger_path: Path) -> set[str]:
    """Return set of mint_slugs already processed."""
    done: set[str] = set()
    if not ledger_path.exists():
        return done
    with open(ledger_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                slug = row.get("mint_slug", "")
                if slug:
                    done.add(slug)
            except json.JSONDecodeError:
                pass
    return done


def process_mint(
    mint: dict,
    mint_participants: set[str],
    wiki_events: list[dict],
    output_dir: Path,
    model: str,
    ledger_path: Path,
    dry_run: bool = False,
) -> dict:
    """Process one mint. Returns result dict. Flushes assignment to disk on success.

    Errors are LOGGED but NOT written to the ledger (per the lesson from
    edge-reify-backfill.py — error-llm in ledger → resume skips → silent loss).
    """
    assignments_path = output_dir / "wiki-cluster-assignments.jsonl"
    parse_fail_path = output_dir / "parse-failures.jsonl"

    result: dict[str, Any] = {
        "mint_slug": mint["slug"],
        "mint_title": mint.get("title", ""),
        "outcome": None,
        "best_match": "none",
        "suggested_action": None,
        "equivalence_evidence_strength": None,
        "rationale": None,
        "quoted_evidence": "",
        "narrow_candidate_count": 0,
        "usage": None,
        "error": None,
    }

    if _RATE_LIMIT_WALL.is_set():
        result["outcome"] = "aborted-rate-limit-wall"
        return result

    # Narrow candidates
    candidates = narrow_candidates(mint, mint_participants, wiki_events, top_k=12)
    result["narrow_candidate_count"] = len(candidates)
    result["narrow_candidate_slugs"] = [w["slug"] for w, _, _ in candidates]

    if not candidates:
        # No deterministic candidates — auto-classify as distinct, no LLM call
        result["outcome"] = "distinct-no-candidates"
        result["suggested_action"] = "distinct"
        result["equivalence_evidence_strength"] = "direct-textual"
        result["rationale"] = "No wiki event-node passed deterministic narrowing signals."
        assignment = {
            "mint_slug": mint["slug"],
            "mint_title": mint.get("title", ""),
            "source_chapter_labels": mint.get("source_chapter_labels", []),
            "source_book": mint.get("source_book", ""),
            "best_match": "none",
            "suggested_action": "distinct",
            "equivalence_evidence_strength": "direct-textual",
            "rationale": result["rationale"],
            "quoted_evidence": "",
            "narrow_candidate_slugs": [],
            "model": "deterministic",
            "produced_at": datetime.now(timezone.utc).isoformat(),
        }
        _append_jsonl_locked(assignments_path, assignment)
        write_ledger_entry(ledger_path, mint["slug"], "distinct-no-candidates", "none")
        return result

    # Dry run — fake response, no LLM call
    if dry_run:
        parsed = {
            "best_match": candidates[0][0]["slug"] if candidates else "none",
            "suggested_action": "distinct",
            "equivalence_evidence_strength": "inference-only",
            "rationale": "DRY RUN stub response",
            "quoted_evidence": "",
        }
        usage_info = {"cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0,
                      "elapsed_seconds": 0.0, "dry_run": True, "model": model}
    else:
        try:
            parsed, usage_info = call_claude_for_classification(
                mint, mint_participants, candidates, model=model,
            )
        except RateLimitError:
            raise
        except Exception as exc:
            err_msg = str(exc)
            result["error"] = err_msg
            result["outcome"] = "error-llm"
            print(f"  [{mint['slug']}] ERROR: {err_msg}", file=sys.stderr)
            # Route parse failures separately for human review
            if "non-JSON" in err_msg or "parse error" in err_msg:
                _append_jsonl_locked(parse_fail_path, {
                    "mint_slug": mint["slug"], "error": err_msg,
                    "produced_at": datetime.now(timezone.utc).isoformat(),
                })
            # DO NOT write to ledger — error is retryable on --resume
            return result

    result["usage"] = usage_info
    result["best_match"] = parsed.get("best_match", "none")
    result["suggested_action"] = parsed.get("suggested_action", "distinct")
    result["equivalence_evidence_strength"] = parsed.get("equivalence_evidence_strength", "inference-only")
    result["rationale"] = parsed.get("rationale", "")
    result["quoted_evidence"] = parsed.get("quoted_evidence", "")
    result["outcome"] = "classified"

    # Sanity: if best_match is "none", suggested_action must be "distinct"
    if result["best_match"] in ("none", "", None) and result["suggested_action"] != "distinct":
        result["suggested_action"] = "distinct"

    # Flush assignment
    assignment = {
        "mint_slug": mint["slug"],
        "mint_title": mint.get("title", ""),
        "source_chapter_labels": mint.get("source_chapter_labels", []),
        "source_book": mint.get("source_book", ""),
        "best_match": result["best_match"],
        "suggested_action": result["suggested_action"],
        "equivalence_evidence_strength": result["equivalence_evidence_strength"],
        "rationale": result["rationale"],
        "quoted_evidence": result["quoted_evidence"],
        "narrow_candidate_slugs": result["narrow_candidate_slugs"],
        "narrow_candidate_count": result["narrow_candidate_count"],
        "model": model,
        "cost_usd": (usage_info or {}).get("cost_usd", 0.0),
        "produced_at": datetime.now(timezone.utc).isoformat(),
    }
    _append_jsonl_locked(assignments_path, assignment)
    write_ledger_entry(ledger_path, mint["slug"], "classified", result["best_match"])

    return result


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run(
    output_dir: Path,
    model: str,
    concurrency: int,
    resume: bool,
    max_events: int | None,
    dry_run: bool,
    pass_b_filter: set[str] | None = None,
) -> None:
    """Run the classifier over all Plate-3 mints (or filtered subset for Pass B)."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = output_dir / "processed-mints.jsonl"

    print(f"\n=== Plate 4 Wiki-Cluster Classifier ===")
    print(f"Output dir:     {output_dir}")
    print(f"Model:          {model}")
    print(f"Concurrency:    {concurrency}")
    print(f"Resume:         {resume}")
    print(f"Max events:     {max_events if max_events is not None else 'unbounded'}")
    print(f"Dry run:        {dry_run}")
    if pass_b_filter is not None:
        print(f"Pass B filter:  {len(pass_b_filter)} mints")
    print()

    # Load shared state
    print("Loading Plate-3 mints...")
    mint_files = sorted(_PLATE3_MINTS.glob("*.node.md"))
    mints = [parse_plate3_mint(p) for p in mint_files]
    print(f"  Loaded {len(mints)} Plate-3 mints from {_PLATE3_MINTS}")

    print("Loading wiki event-nodes...")
    wiki_files = sorted(_WIKI_EVENT_NODES.glob("*.node.md"))
    wiki_events = [parse_wiki_event_node(p) for p in wiki_files]
    print(f"  Loaded {len(wiki_events)} wiki event-nodes from {_WIKI_EVENT_NODES}")

    print("Loading Plate-3 role edges (for participant lookup)...")
    role_edges_by_hub = load_plate3_role_edges(_PLATE3_ROLE_EDGES)
    print(f"  Loaded role edges for {len(role_edges_by_hub)} hubs")

    if resume:
        done = load_ledger(ledger_path)
        print(f"  Ledger: {len(done)} mints already processed (will skip)")
    else:
        done = set()
        # Fresh: clear assignments + parse-failures (NOT ledger if user is appending)
        for f in [output_dir / "wiki-cluster-assignments.jsonl",
                  output_dir / "parse-failures.jsonl"]:
            if f.exists():
                f.unlink()

    # Build work list
    to_process: list[dict] = []
    for mint in mints:
        slug = mint["slug"]
        if slug in done:
            continue
        if pass_b_filter is not None and slug not in pass_b_filter:
            continue
        to_process.append(mint)

    # --max-events cap
    if max_events is not None and len(to_process) > max_events:
        to_process.sort(key=lambda m: m["slug"])
        to_process = to_process[:max_events]
        print(f"  --max-events cap: trimming to first {max_events}")

    print(f"  To process this run: {len(to_process)}")
    print()
    if not to_process:
        print("Nothing to do.")
        return

    # Precompute participants per mint
    mint_to_participants = {
        m["slug"]: participant_slugs_for_mint(m["slug"], role_edges_by_hub)
        for m in to_process
    }

    # Process in parallel
    total_events = len(to_process)
    rate_limit_hit = False
    done_count = 0
    running_cost = 0.0
    outcome_counts: dict[str, int] = {}
    action_counts: dict[str, int] = {}

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(
                process_mint,
                mint=m,
                mint_participants=mint_to_participants[m["slug"]],
                wiki_events=wiki_events,
                output_dir=output_dir,
                model=model,
                ledger_path=ledger_path,
                dry_run=dry_run,
            ): m["slug"]
            for m in to_process
        }
        for future in as_completed(futures):
            slug = futures[future]
            done_count += 1
            try:
                result = future.result()
                running_cost += (result.get("usage") or {}).get("cost_usd", 0.0)
                outcome = result.get("outcome") or "unknown"
                action = result.get("suggested_action") or "n/a"
                outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
                action_counts[action] = action_counts.get(action, 0) + 1
                if done_count % 10 == 0 or done_count == total_events:
                    print(f"  Progress: {done_count}/{total_events} | cost ${running_cost:.4f}")
            except RateLimitError as exc:
                _RATE_LIMIT_WALL.set()
                rate_limit_hit = True
                print(
                    f"\n[RATE LIMIT WALL] {slug!r}: {exc}\n"
                    f"Stopping. Partial state intact.\n"
                    f"Resume: rerun the same command with --resume",
                    file=sys.stderr,
                )
                for f in futures:
                    f.cancel()
            except Exception as exc:
                if _RATE_LIMIT_WALL.is_set():
                    continue
                print(f"  [{slug}] FATAL: {exc}", file=sys.stderr)

    # Summary
    print(f"\n=== RESULTS ===")
    print(f"  Processed this run:  {done_count}")
    print(f"  Outcome distribution:")
    for k, v in sorted(outcome_counts.items(), key=lambda x: -x[1]):
        print(f"    {k:<32} {v}")
    print(f"  Suggested-action distribution:")
    for k, v in sorted(action_counts.items(), key=lambda x: -x[1]):
        print(f"    {k:<32} {v}")
    print(f"  Total cost this run: ${running_cost:.4f}")
    print(f"  Output: {output_dir}")

    if rate_limit_hit:
        sys.exit(2)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Plate 4 wiki-cluster classifier.")
    parser.add_argument("--output-dir", default=str(_DEFAULT_OUT))
    parser.add_argument("--model", default="claude-haiku-4-5-20251001")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-events", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--pass", dest="pass_label", choices=["A", "B"], default="A")
    parser.add_argument(
        "--pass-a-results", default=None,
        help="Pass B mode: path to Pass A's wiki-cluster-assignments.jsonl.",
    )
    parser.add_argument(
        "--pass-b-filter",
        choices=["inference-only", "distinct", "distinct-or-inference-only"],
        default="inference-only",
        help="Which Pass A rows to re-judge in Pass B (default: inference-only).",
    )
    args = parser.parse_args(argv)

    pass_b_filter: set[str] | None = None
    if args.pass_label == "B":
        if not args.pass_a_results:
            print("ERROR: --pass B requires --pass-a-results", file=sys.stderr)
            sys.exit(1)
        pa_path = Path(args.pass_a_results)
        if not pa_path.exists():
            print(f"ERROR: Pass A results not found: {pa_path}", file=sys.stderr)
            sys.exit(1)
        # Filter: per --pass-b-filter flag.
        filt = args.pass_b_filter
        pass_b_filter = set()
        with open(pa_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                action = row.get("suggested_action", "")
                strength = row.get("equivalence_evidence_strength", "")
                include = False
                if filt == "inference-only" and strength == "inference-only":
                    include = True
                elif filt == "distinct" and action == "distinct":
                    include = True
                elif filt == "distinct-or-inference-only" and (
                    action == "distinct" or strength == "inference-only"
                ):
                    include = True
                if include:
                    pass_b_filter.add(row.get("mint_slug", ""))
        pass_b_filter.discard("")
        print(f"Pass B filter built: {len(pass_b_filter)} mints from Pass A (filter='{filt}')")

    run(
        output_dir=Path(args.output_dir),
        model=args.model,
        concurrency=args.concurrency,
        resume=args.resume,
        max_events=args.max_events,
        dry_run=args.dry_run,
        pass_b_filter=pass_b_filter,
    )


if __name__ == "__main__":
    main()
