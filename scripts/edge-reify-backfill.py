#!/usr/bin/env python3
"""edge-reify-backfill.py — Plate 3 reification pipeline for the Weirwood Network.

Mines Pass-1 extraction files for n-ary events matching Q1 trigger families,
resolves event hubs via the reuse lookup (Q2), and emits role edges
(AGENT_IN, VICTIM_IN, COMMANDS_IN, LOCATED_AT) to a staging JSONL.

Modes:
  --smoke / --event <slug>  Process ONE event (original smoke-test mode, kept for regression).
  --batch <config.json>     Process a curated list of events from a JSON config file.
                            This is the mini-batch / full-run entry point.
  --all                     Full corpus scan over all 344 chapter extractions.

Design decisions applied:
    D2=Replace  — no materialized agent→patient dyad; scattered binaries marked superseded_by.
    D7          — executor → AGENT_IN; orderer → COMMANDS_IN; never collapse instigator→victim.
    D8          — reify only n-ary events (multiple agents/victims OR instigator≠executor).
    Q1          — selective trigger families only (deaths, weddings, sieges, captures, guest-right violations).
    Q2          — reuse-before-mint via event-node-reuse-lookup.json.

Engineering rules (from Full-run engineering notes, continue-prompt 2026-06-05):
    1. Group/faction actors → house.* AGENT_IN (per cleanup-decisions-resolved.md §5).
    2. Cross-chapter dedup: gather roles from ALL chapters per event hub, dedup by (source_slug, role, event_slug).
    3. Programmatic supersede detection: query edges.jsonl for endpoints that are participants AND
       edge_type in reify trigger family → emit to supersede-candidates.jsonl.
       FIX (2026-06-07): edge's evidence_chapter MUST be in the event's chapter set to avoid
       false positives from major characters appearing in many events.
    4. Orderer-evidence confidence gate: indirect/inferred orders → confidence_tier 2.
    5. claude -p MUST use cwd=/tmp (avoids loading 32k CLAUDE.md project cache).
    6. LOCATED_AT direction: event → location (event LOCATED_AT place).
    7. Concurrency: claude -p calls run in a thread pool (cap=5).
    8. Borderline single-agent gate (FIX 2026-06-07): if LLM returns is_nary=True but the event
       has only 1 AGENT_IN, 0-1 VICTIM_IN, and 0 COMMANDS_IN (single agent both ordered AND
       executed), route to hub-review-queue.jsonl with reason="borderline-single-agent" instead
       of auto-reifying. Clearly n-ary events (distinct instigator, multiple agents/victims,
       multi-chapter set-piece) proceed normally.

Resilience / resume features (added 2026-06-07):
    9. Fail-fast rate-limit wall: a hard rate-limit or quota-exhausted error raises RateLimitError.
       The runner allows at most 1 short retry (for transient blips), then sets a process-wide
       _RATE_LIMIT_WALL Event, prints a clear message, and exits with code 2. Total wall-time
       before exit: never more than ~90s. Partial ledger + files remain intact.
   10. Incremental flush: after each event completes, role edges and supersede candidates are
       immediately appended to their files. A SIGKILL loses at most the single in-flight event.
   11. Processed-events ledger: working/edge-modeling/plate3-full/processed-events.jsonl, one
       line per completed event {event_key, hub_slug, outcome, n_role_edges}. Written incrementally.
   12. --resume flag: loads the ledger, skips already-processed event keys, deduplicates role
       edges by (source_slug, edge_type, target_slug, evidence_chapter). Resuming over the
       existing 37 minted nodes / 11 queued produces zero duplicates.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
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
_EDGES_JSONL = _REPO / "graph" / "edges" / "edges.jsonl"
_NODES_DIR = _REPO / "graph" / "nodes"
_REUSE_LOOKUP = _REPO / "working" / "edge-modeling" / "event-node-reuse-lookup.json"
_EXTRACTIONS_DIR = _REPO / "extractions" / "mechanical"
_SMOKE_OUTPUT_DIR = _REPO / "working" / "edge-modeling"

# ---------------------------------------------------------------------------
# Rate-limit / quota-wall handling
# ---------------------------------------------------------------------------

# Sentinel strings in claude -p stderr that indicate a HARD rate-limit wall
# (quota exhausted, not just a transient 529).
_RATE_LIMIT_STDERR_PATTERNS = [
    "rate limit",
    "rate_limit",
    "quota",
    "overloaded",
    "too many requests",
    "429",
    "529",
    "usage limit",
    "credit balance",
]

# Process-wide Event: when set, no new work starts and the runner exits cleanly.
_RATE_LIMIT_WALL = threading.Event()

# Lock for writing to the ledger and append files to avoid interleaved writes
_WRITE_LOCK = threading.Lock()


class RateLimitError(RuntimeError):
    """Raised when claude -p returns a hard rate-limit / quota-exhausted error."""


# ---------------------------------------------------------------------------
# Q1 Trigger families — keywords that flag a Pass-1 event as reify-eligible
# ---------------------------------------------------------------------------

_TRIGGER_KEYWORDS = frozenset({
    # death / killing family
    "kill", "kills", "killed", "murder", "slain", "slaughter", "massacre",
    "assassination", "assassinate", "executed", "execution", "stabbed", "stabs",
    "dies", "death", "throat cut", "slays", "slay",
    "beheaded", "beheading",
    # (REMOVED 2026-06-07: "falls", "fall" — too narrative; matches "Bran's fall"
    #  bold titles legitimately but also "Tyrion asks about Bran's fall" / "Catelyn falls",
    #  and matches the description text under non-event beats.)
    # (REMOVED 2026-06-07: "fires on", "fire on", "crossbow", "crossbows" — narrative
    #  micro-action words; the events that legitimately involve crossbows are caught by
    #  "kill"/"attack"/"betray" already.)
    # wedding / ceremony family
    "wedding", "wed", "bedding", "ceremony", "crowning", "coronation",
    # siege / battle / assault family
    "siege", "sack", "attack", "ambush", "assault", "battle", "conquest",
    # capture / imprisonment family
    "capture", "captures", "captured", "takes hostage", "hostage", "prisoner",
    "imprisoned", "arrested", "arrest",
    # guest-right / betrayal family
    "betrayal", "betrays", "betray", "betrayed", "guest right", "guest-right",
    # conspiracy / conspiracy family
    "conspiracy", "plot", "plots", "plotted",
    # sacrifice family
    "sacrifice", "sacrificed", "sacrifices",
    # poison family
    "poison", "poisoned", "poisoning",
})

# Gate E (added 2026-06-07): dialogue / recall / discussion verb deny-list.
# These bold-title patterns are recountings, revelations, reflections, or
# discussions ABOUT events — not events themselves. Reifying them produces
# duplicate-of-real-event hubs ("cersei-recalls-ned-stark-s-execution") or
# pure narrative-beat hubs that pollute the graph. Block at the slug-pattern
# layer BEFORE the LLM call (~21% of GATE-A surviving slugs, ~$10-20 saved).
#
# Patterns are matched against the kebab-case slug derived from the bold title.
# Word-boundary semantics ensure "demands" in "demands-to-know" matches but
# "aeron-demands-benfred-s-death" does NOT (the latter is a real ordering event).
_GATE_E_DIALOGUE_RECALL_PATTERNS = re.compile(
    r"(^|[-_])("
    # V1 patterns — speech, recall, cognition
    r"reflects?-on|reflects?|"
    r"recalls?|remembers?|"
    r"reveals?|"
    r"reports?|reported|"
    r"tells?|told|"
    r"cryptic-remark|"
    r"discuss(es|ed|ion)?|discussion-of|"
    r"debates?|"
    r"asks?-(about|who|if|that|why|how|whether)|"
    r"considers?|"
    r"studies|studied|"
    r"observes?|"
    r"questions?-(about|on)|"
    r"describes?|"
    r"mentions?|"
    r"speculates?|"
    r"deduces?|deduction-of|"
    r"speaks?-of|"
    r"warns?-(of|about|that)|"
    r"suggests?|"
    r"proposes?|"
    r"demands?-to-know|"
    r"claims?-(that|to)|"
    r"denies-(that|the)|"
    r"confirms?-(that|the|.*-was|.*-is|.*-killed|.*-died|.*-poisoned)|"
    r"memory-of|memories-of|"
    r"dream(s|ed)?-of|"
    r"vision-(of|that)|"
    r"flashback|flashbacks?-of|"
    r"discovery-of|"
    r"news-of|"
    r"reactions?-to|"
    r"recap-of|"
    r"learns?-(of|about|that|the)|"
    r"hears?-(of|about|that)|"
    r"acknowledges?|"
    r"identifies|"
    r"agonizes-over|"
    r"recites?-(her|his)|"
    r"delivers-news|"
    r"announcement-of|"
    r"announcing-the|"
    r"revelation-(of|that)|"
    r"raises-the-possibility-of|"
    r"voice-support-for|"
    r"voices?-(support|opposition)|"
    # V2 patterns (2026-06-07) — observed slipthroughs in calibration #2
    # whisper/mutter speech verbs
    r"whispers?|whispered|whispering|"
    r"mutters?|muttered|"
    r"muses?|mused|"
    r"wonders?-(if|why|how|what|whether)|"
    r"thinks?-(of|about|that)|"
    # aftermath / post-event recap beats
    r"aftermath-of|"
    # battle/attack sub-beats (begin, end, rage — not the event itself)
    r"^(battle|attack|siege)-(begins?|ends?|rages?|outcome|in-progress|assembly|dispositions|becomes|plan|preparations|details|aftermath|formations|outcome-explained|at-the-holdfast|in-the-market-square|in-the-plaza|in-the-street)|"
    # banquet / feast micro-beats (the actual wedding/coronation are still admitted)
    r"^(banquet|feast)-(in-progress|begins?|ends?)|"
    # static scene descriptors
    r"^bodies-(stored|brought|laid|found|discovered)|"
    # assignment/insistence/argument beats (not actions)
    r"is-assigned-to|assigned-to-(kill|spy|find)|"
    r"insists-(on|that)|"
    # passive descriptive beats
    r"rides?-as-prisoner|rides?-with-the|"
    r"visits?-prisoners?|visits?-the-prisoners?|visits?-dornish-prisoners?|"
    # plan/preparation beats (not the action)
    r"plans?-(to|the)|planning-(the|to)"
    r")([-_]|$)"
)


def is_dialogue_recall_slug(slug: str) -> bool:
    """Gate E: True if the slug matches a dialogue/recall/discussion verb pattern."""
    if not slug:
        return False
    return bool(_GATE_E_DIALOGUE_RECALL_PATTERNS.search(slug))


# Edge types in the reify trigger family (for supersede detection)
_TRIGGER_EDGE_TYPES = frozenset({
    "KILLS", "MURDERS", "EXECUTES", "ASSASSINATES", "POISONS",
    "BETRAYS", "ATTACKS", "ASSAULTS", "CAPTURES", "IMPRISONS",
    "COMMANDS_ATTACK", "SIEGE", "SACKS",
    "VIOLATES_GUEST_RIGHT", "MASSACRES",
    "CONSPIRES_WITH", "CONSPIRES_AGAINST",
})

# ---------------------------------------------------------------------------
# Role vocabulary enforced in the LLM prompt (D7)
# ---------------------------------------------------------------------------

_ROLE_VOCAB = ["AGENT_IN", "VICTIM_IN", "COMMANDS_IN", "WIELDED_IN", "LOCATED_AT"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_reuse_lookup(path: Path) -> dict[str, str]:
    """Load the normalized-title → slug reuse lookup."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("lookup", {})


def normalize_title(title: str) -> str:
    """Produce a normalized lookup key:
    lower-case, strip punctuation, collapse whitespace.
    """
    t = title.lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def resolve_event_slug(
    title: str,
    lookup: dict[str, str],
    threshold: float = 0.5,
) -> tuple[str | None, str, float]:
    """Try to resolve a Pass-1 event title to an existing event-node slug.

    Returns (slug_or_None, match_type, score).
    match_type in {"exact", "slug", "token_sorted", "fuzzy_medium", "no_match"}.
    """
    norm = normalize_title(title)

    # 1. Normalized space form
    if norm in lookup:
        return lookup[norm], "exact", 1.0

    # 2. Slug form
    slug_form = norm.replace(" ", "-")
    if slug_form in lookup:
        return lookup[slug_form], "slug", 1.0

    # 3. Token-sorted form
    token_sorted = " ".join(sorted(norm.split()))
    if token_sorted in lookup:
        return lookup[token_sorted], "token_sorted", 1.0

    # 4. Fuzzy: count token overlap
    norm_tokens = set(norm.split())
    best_slug: str | None = None
    best_score = 0.0
    for key, slug in lookup.items():
        key_tokens = set(key.split())
        if not key_tokens or not norm_tokens:
            continue
        overlap = len(norm_tokens & key_tokens)
        score = overlap / max(len(norm_tokens), len(key_tokens))
        if score > best_score:
            best_score = score
            best_slug = slug

    if best_score >= threshold:
        return best_slug, "fuzzy_medium", best_score

    return None, "no_match", 0.0


def build_slug_category_index(nodes_dir: Path) -> dict[str, str]:
    """Return slug → subdirectory-name mapping for all node files."""
    index: dict[str, str] = {}
    if not nodes_dir.is_dir():
        return index
    for cat_dir in nodes_dir.iterdir():
        if not cat_dir.is_dir() or cat_dir.name.startswith("_"):
            continue
        for node_file in cat_dir.glob("*.node.md"):
            slug = node_file.stem.replace(".node", "")
            index[slug] = cat_dir.name
    return index


def load_edges_jsonl(path: Path) -> list[dict]:
    """Load the graph edges.jsonl into a list of dicts."""
    edges: list[dict] = []
    if not path.exists():
        return edges
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                edges.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return edges


# ---------------------------------------------------------------------------
# Pass-1 extraction parser
# ---------------------------------------------------------------------------

def parse_extraction_sections(md_path: Path) -> dict[str, Any]:
    """Extract Events & Actions and Relationships Observed from a .extraction.md file.

    Each event entry is parsed into:
        {"bold_title": "<just the **bold** part>", "full_text": "<title + description>"}

    Bold title is what Pass-1 extractor put in `**...**` for that numbered entry
    (e.g. "Departure at daybreak", "The execution", "Red Wedding"). It is the
    canonical event name, separate from the narrative description text that
    follows the em-dash. Plate 3 uses bold_title for trigger-keyword matching
    and slug generation (full_text would contain promiscuous words like
    "executed" / "killed" / "slain" in the description and over-admit micro-beats).
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    chapter_id = md_path.stem.replace(".extraction", "")

    for line in lines[:20]:
        if "pov_chapter_number:" in line:
            pov_ch = line.split("pov_chapter_number:", 1)[1].strip().lstrip("*").strip()
            book = md_path.stem.split("-")[0].upper()
            chapter_id = f"{book} {pov_ch}"
            break

    events: list[dict[str, str]] = []
    relationships: list[str] = []

    in_events = False
    in_relationships = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## Events & Actions"):
            in_events = True
            in_relationships = False
            continue
        if stripped.startswith("## Relationships Observed"):
            in_relationships = True
            in_events = False
            continue
        if stripped.startswith("## ") and in_events:
            in_events = False
            continue
        if stripped.startswith("## ") and in_relationships:
            in_relationships = False
            continue

        if in_events and stripped:
            no_num = re.sub(r"^\d+\.\s*", "", stripped)
            # Extract bold title from the FIRST **...** block at the start.
            bold_match = re.match(r"\*\*([^*]+)\*\*", no_num)
            bold_title = bold_match.group(1).strip() if bold_match else ""
            # Full clean text = description + title with bold markers stripped.
            clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", no_num)
            if clean and not clean.startswith("|") and not clean.startswith("-"):
                events.append({"bold_title": bold_title, "full_text": clean})

        if in_relationships and stripped.startswith("|"):
            if "Character A" in stripped or "---" in stripped:
                continue
            relationships.append(stripped)

    return {
        "events": events,
        "relationships": relationships,
        "chapter": chapter_id,
        "source_file": str(md_path.relative_to(_REPO)),
    }


def filter_trigger_events(events: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return only events whose BOLD TITLE matches a Q1 trigger keyword.

    Matching on bold_title (not full_text) is the key gate fix (2026-06-07):
    Pass-1 description text routinely contains words like "executed", "killed",
    "slain" in non-event narrative beats — "Bran rides out to see a man executed"
    is a journey, not an execution event. The bold title is the extractor's
    declared event name, so it is the right matching surface.

    Falls back to full_text matching if bold_title is empty (extractor didn't
    use bold formatting), so we don't lose events that lack the bold convention.
    """
    result: list[dict[str, str]] = []
    for e in events:
        surface = (e.get("bold_title") or e.get("full_text") or "").lower()
        if any(kw in surface for kw in _TRIGGER_KEYWORDS):
            result.append(e)
    return result


# ---------------------------------------------------------------------------
# LLM role assignment via claude -p (D5, D7)
# ---------------------------------------------------------------------------

ROLE_ASSIGNMENT_PROMPT_TEMPLATE = """You are processing a single event from A Song of Ice and Fire for the Weirwood Network knowledge graph.

Your task: extract participant roles for the event "{event_title}" (event node slug: {event_slug}).

ROLE VOCABULARY — assign each named participant exactly ONE role:
  AGENT_IN    — the person(s)/house(s) who physically executed or performed the action
  VICTIM_IN   — the person(s)/house(s) who received the action (killed, betrayed, captured, etc.)
  COMMANDS_IN — the person(s)/house(s) who ordered/instigated but did NOT personally execute
  WIELDED_IN  — a named artifact used to perform the action (not a person)
  LOCATED_AT  — the location where the event took place (not a person)

CRITICAL RULES:
1. D7: NEVER assign COMMANDS_IN to a victim. Instigator (orderer) → COMMANDS_IN; direct executor → AGENT_IN.
   These are different roles on the SAME event node. Do NOT collapse instigator→victim into a single edge.
2. D8 n-ary gate: if this event is actually a clean single-agent/single-victim dyad with NO instigator
   or ordering third party, set is_nary=false and return an empty participants list. DO NOT reify clean dyads.
3. Confidence: explicit textual evidence → confidence=1; strong inference → confidence=2; uncertain → confidence=3.
   Indirect "countenanced"/"gave his blessing" orders → confidence=2 (not 1).
4. Group actors: if the executor is a group (e.g. "Frey crossbowmen", "Bolton men-at-arms"), emit
   the house slug (e.g. "house-frey", "house-bolton") as AGENT_IN.
5. LOCATED_AT direction: event → location. The event is located at the place, NOT the reverse.
6. Slugs must be kebab-case matching graph/nodes/characters/<slug>.node.md naming.

SOURCE MATERIAL — Events & Actions entries from the chapter extraction:
{events_text}

SOURCE MATERIAL — Relationships Observed entries:
{relationships_text}

ADDITIONAL CONTEXT:
{additional_context}

PARTICIPANTS to assign roles for:
{participants_list}

D8 CHECK: Is this event genuinely n-ary?
- N-ary = multiple agents, OR instigator≠executor, OR multiple victims, OR it is a named set-piece that other edges reference.
- Clean dyad = exactly one agent + one victim, no ordering third party, not a named set-piece.
- If clean dyad: set is_nary=false and return empty participants list. No hub should be created.

OUTPUT FORMAT — return ONLY valid JSON, no markdown, no explanation:
{{
  "event_slug": "{event_slug}",
  "event_title": "{event_title}",
  "is_nary": true,
  "nary_reason": "<why n-ary: multiple killers, multiple victims, instigator≠executor, named set-piece>",
  "participants": [
    {{
      "slug": "<character-or-location-or-house-slug>",
      "name": "<display name>",
      "role": "<AGENT_IN|VICTIM_IN|COMMANDS_IN|WIELDED_IN|LOCATED_AT>",
      "confidence": <1-3>,
      "rationale": "<one sentence>",
      "evidence_quote": "<direct quote or paraphrase from source>"
    }}
  ]
}}

Return ONLY the JSON object. No preamble, no explanation, no markdown fences.
"""


def _is_rate_limit_error(returncode: int, stderr: str, stdout: str = "") -> bool:
    """Return True if the subprocess failure looks like a hard rate-limit wall.

    Detection (any of):
    1. Known rate-limit / quota strings in stderr (or stdout — claude -p sometimes
       writes the error envelope to stdout instead of stderr).
    2. **Empty stderr + nonzero exit** (added 2026-06-07): claude -p frequently
       exits 1 with NO stderr output when the 5-hour usage wall is in effect.
       That silent-failure mode caused 324 events in a prior run to be misclassified
       as generic errors and (worse) written to the ledger as "done", causing
       resume to skip them. Treating silent exit-1 as a wall is the correct safety:
       worst case it sleeps WALL_SLEEP on a real bug, but never silently loses work.
    """
    if returncode not in (1, 2):
        return False
    combined = (stderr or "").lower() + " " + (stdout or "").lower()
    if any(pat in combined for pat in _RATE_LIMIT_STDERR_PATTERNS):
        return True
    # Silent failure → assume wall (safe default; never silently mark events done)
    if not (stderr or "").strip():
        return True
    return False


def call_claude_for_roles(
    event_slug: str,
    event_title: str,
    events_lines: list[str],
    relationships_lines: list[str],
    participants: list[dict],
    additional_context: str = "",
    model: str = "claude-sonnet-4-6",
    max_transient_retries: int = 1,
) -> tuple[dict, dict]:
    """Make ONE claude -p call (cwd=/tmp) to assign participant roles.

    Returns (parsed_json_response, usage_info).

    Raises RateLimitError on a hard quota wall (after at most 1 transient retry).
    Raises RuntimeError on other subprocess failures.
    The caller should check _RATE_LIMIT_WALL.is_set() before calling this function.
    """
    events_text = "\n".join(f"- {e}" for e in events_lines) or "(none)"
    relationships_text = "\n".join(f"- {r}" for r in relationships_lines) or "(none)"
    participants_list = (
        "\n".join(f"  - {p['name']} (slug: {p['slug']})" for p in participants)
        if participants else "(no pre-identified participants — infer from source material)"
    )

    prompt = ROLE_ASSIGNMENT_PROMPT_TEMPLATE.format(
        event_title=event_title,
        event_slug=event_slug,
        events_text=events_text,
        relationships_text=relationships_text,
        additional_context=additional_context,
        participants_list=participants_list,
    )

    cmd = [
        "claude",
        "--model", model,
        "--output-format", "json",
        "-p", prompt,
    ]

    last_exc: Exception | None = None
    rate_limit_count = 0

    for attempt in range(max_transient_retries + 1):
        # Abort immediately if the wall was set by another thread
        if _RATE_LIMIT_WALL.is_set():
            raise RateLimitError("Rate-limit wall set by another thread; aborting.")

        start = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/tmp",  # MUST be /tmp per reference_llm_pass_via_claude_p memory
                timeout=180,
            )
        except subprocess.TimeoutExpired as e:
            last_exc = e
            if attempt < max_transient_retries:
                time.sleep(5)
                continue
            raise RuntimeError(f"claude -p timed out after 180s for event {event_slug!r}") from e

        elapsed = time.time() - start

        if result.returncode != 0:
            stderr_snippet = (result.stderr or "")[:600]
            stdout_snippet = (result.stdout or "")[:300]
            if _is_rate_limit_error(result.returncode, result.stderr, result.stdout):
                rate_limit_count += 1
                if attempt < max_transient_retries:
                    # One short wait in case it's a brief blip (not a full wall)
                    wait_secs = 30
                    print(
                        f"  [{event_slug}] TRANSIENT rate-limit (attempt {attempt+1}), "
                        f"waiting {wait_secs}s before retry...",
                        file=sys.stderr,
                    )
                    time.sleep(wait_secs)
                    continue
                # Second rate-limit hit → hard wall; do NOT retry further
                raise RateLimitError(
                    f"Hard rate-limit wall on event {event_slug!r} "
                    f"(returncode={result.returncode}); stderr={stderr_snippet!r} stdout={stdout_snippet!r}"
                )
            last_exc = RuntimeError(
                f"claude -p exited {result.returncode} for {event_slug!r}.\n"
                f"stderr: {stderr_snippet}\nstdout: {stdout_snippet}"
            )
            if attempt < max_transient_retries:
                time.sleep(5)
                continue
            raise last_exc  # type: ignore[misc]

        raw_output = result.stdout.strip()

        try:
            envelope = json.loads(raw_output)
        except json.JSONDecodeError:
            # Sometimes the output is raw text, not the JSON envelope
            envelope = {"result": raw_output, "usage": {}}

        usage = envelope.get("usage", {})
        input_tokens = usage.get("input_tokens", 0)
        cache_create_tokens = usage.get("cache_creation_input_tokens", 0)
        cache_read_tokens = usage.get("cache_read_input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        # Sonnet 4.x pricing (2026): $3 input / $15 output / $3.75 cache-create / $0.30 cache-read
        cost_usd = (
            (input_tokens * 3.0)
            + (cache_create_tokens * 3.75)
            + (cache_read_tokens * 0.30)
            + (output_tokens * 15.0)
        ) / 1_000_000

        content = envelope.get("result", "")
        if not content:
            content = raw_output

        content_clean = re.sub(r"^```(?:json)?\s*", "", content.strip())
        content_clean = re.sub(r"\s*```$", "", content_clean.strip())

        parsed = json.loads(content_clean)

        usage_info = {
            "input_tokens": input_tokens,
            "cache_creation_input_tokens": cache_create_tokens,
            "cache_read_input_tokens": cache_read_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost_usd,
            "elapsed_seconds": round(elapsed, 1),
            "model": model,
        }

        return parsed, usage_info

    raise RuntimeError(f"Exhausted retries for event {event_slug!r}: {last_exc}")


# ---------------------------------------------------------------------------
# Role-edge emitter
# ---------------------------------------------------------------------------

def emit_role_edges(
    parsed_response: dict,
    source_chapter: str,
    source_file: str,
    run_label: str = "plate3-minibatch",
) -> list[dict]:
    """Convert LLM role-assignment response into JSONL-ready edge dicts."""
    event_slug = parsed_response.get("event_slug", "")
    edges: list[dict] = []

    for p in parsed_response.get("participants", []):
        role = p.get("role", "")
        slug = p.get("slug", "")
        name = p.get("name", "")
        evidence_quote = p.get("evidence_quote", "")
        confidence = p.get("confidence", 2)
        rationale = p.get("rationale", "")

        if not role or not slug or not event_slug:
            continue

        if role in ("AGENT_IN", "VICTIM_IN", "COMMANDS_IN"):
            source_slug = slug
            target_slug = event_slug
        elif role == "LOCATED_AT":
            # event → location (per architecture: LOCATED_AT = Entity → Location)
            source_slug = event_slug
            target_slug = slug
        elif role == "WIELDED_IN":
            source_slug = slug
            target_slug = event_slug
        else:
            print(f"[warn] Unknown role {role!r} for {slug!r}, skipping", file=sys.stderr)
            continue

        edge = {
            "edge_type": role,
            "source_slug": source_slug,
            "target_slug": target_slug,
            "confidence_tier": confidence,
            "evidence_book": source_chapter.split()[0].lower() if source_chapter else "",
            "evidence_chapter": source_chapter,
            "evidence_kind": "book-pass1-reified",
            "evidence_source_file": source_file,
            "evidence_quote": evidence_quote,
            "rationale": rationale,
            "participant_name": name,
            "plate": run_label,
            "produced_at": datetime.now(timezone.utc).isoformat(),
            "schema_version": "plate3-v1",
        }
        edges.append(edge)

    return edges


# ---------------------------------------------------------------------------
# Contract 10 validator
# ---------------------------------------------------------------------------

def validate_role_edges(
    edges: list[dict],
    slug_category_index: dict[str, str],
    minted_slugs: set[str] | None = None,
) -> dict:
    """Validate AGENT_IN / VICTIM_IN edges against Contract 10.

    Contract 10: AGENT_IN/VICTIM_IN target MUST be event.*
      KEEP — target resolves to 'events' or is in minted_slugs (newly minted, not yet on disk)
      FLAG — target has no node (alias/unminted)
      DROP — target resolves to a known non-event category
    """
    minted_slugs = minted_slugs or set()
    results: dict[str, list] = {"keep": [], "flag": [], "drop": []}

    for edge in edges:
        et = edge.get("edge_type", "")
        tgt = edge.get("target_slug", "")

        if et not in ("AGENT_IN", "VICTIM_IN"):
            results["keep"].append({"edge": edge, "reason": "not AGENT_IN/VICTIM_IN — no Contract 10 check"})
            continue

        if tgt in minted_slugs:
            results["keep"].append({"edge": edge, "reason": "PASS: target is freshly minted event node"})
            continue

        tgt_cat = slug_category_index.get(tgt)

        if tgt_cat == "events":
            results["keep"].append({"edge": edge, "reason": "PASS: target is event.*"})
        elif tgt_cat is None:
            results["flag"].append({
                "edge": edge,
                "reason": f"CONTRACT_WARNING: {et} target {tgt!r} has no node (unminted or alias)",
            })
        else:
            results["drop"].append({
                "edge": edge,
                "reason": f"CONTRACT_VIOLATED: {et} target {tgt!r} is category {tgt_cat!r}, expected events",
            })

    return results


# ---------------------------------------------------------------------------
# Supersede detection (D2 = Replace)
# ---------------------------------------------------------------------------

def find_supersede_candidates(
    all_edges: list[dict],
    participant_slugs: set[str],
    hub_slug: str,
    event_chapter_ids: set[str],
) -> list[dict]:
    """Find edges in the graph whose BOTH endpoints are event participants,
    whose edge_type is in the reify trigger family, AND whose evidence_chapter
    is in the event's chapter set.

    The chapter-overlap filter is the critical fix that prevents false positives:
    major characters (Tyrion, Cersei, Jorah) appear across many events, so without
    the chapter filter, edges from completely different events get falsely tagged.

    Example: tyrion-lannister KILLS tywin-lannister has evidence_chapter=asos-tyrion-11,
    which is NOT in battle-of-the-blackwater's chapter set (acok-tyrion-13, acok-sansa-06),
    so it is correctly NOT flagged.

    True positive: roose-bolton BETRAYS robb-stark has evidence_chapter=asos-catelyn-07,
    which IS in red-wedding's chapter set, so it IS correctly flagged.

    Returns list of edges with added superseded_by field.
    """
    candidates = []
    for edge in all_edges:
        src = edge.get("source_slug", "")
        tgt = edge.get("target_slug", "")
        et = edge.get("edge_type", "")
        evidence_chapter = edge.get("evidence_chapter", "")

        if et not in _TRIGGER_EDGE_TYPES:
            continue
        if src not in participant_slugs or tgt not in participant_slugs:
            continue

        # FIX: require evidence_chapter to be within the event's chapter set.
        # This is the blocker fix: without it, major characters in many events
        # produce cascading false positives.
        if event_chapter_ids and evidence_chapter not in event_chapter_ids:
            continue

        cand = dict(edge)
        cand["superseded_by"] = hub_slug
        cand["supersede_note"] = (
            f"Both endpoints ({src}, {tgt}) are participants in {hub_slug}; "
            f"edge_type {et} is in reify trigger family; "
            f"evidence_chapter {evidence_chapter!r} is in event chapter set. "
            f"Mark for deprecation at Plate 5."
        )
        candidates.append(cand)
    return candidates


# ---------------------------------------------------------------------------
# Node minting
# ---------------------------------------------------------------------------

def mint_event_node(
    event_title: str,
    event_slug: str,
    event_type: str,
    description: str,
    evidence_chapters: list[str],
    minted_dir: Path,
) -> Path:
    """Write a minimal event node markdown file to the minted staging dir.

    Returns the path written.
    """
    minted_dir.mkdir(parents=True, exist_ok=True)
    node_path = minted_dir / f"{event_slug}.node.md"

    content = f"""---
slug: {event_slug}
type: {event_type}
title: "{event_title}"
status: minted-plate3
minted_at: {datetime.now(timezone.utc).isoformat()}
evidence_chapters:
{chr(10).join(f'  - {c}' for c in evidence_chapters)}
---

# {event_title}

{description}

## Edges
(populated by Plate 3 role-edge staging; merge at Plate 5)

## Notes
Node minted by `edge-reify-backfill.py --batch` during Plate 3 mini-batch run.
Staging only — do NOT promote to graph/nodes/events/ until Plate 5 gated merge.
"""
    node_path.write_text(content, encoding="utf-8")
    return node_path


# ---------------------------------------------------------------------------
# Single-event batch processor
# ---------------------------------------------------------------------------

def process_event(
    event_cfg: dict,
    lookup: dict[str, str],
    all_graph_edges: list[dict],
    slug_category_index: dict[str, str],
    output_dir: Path,
    model: str,
    dry_run: bool = False,
    ledger_path: Path | None = None,
    existing_role_edge_keys: set[tuple] | None = None,
) -> dict:
    """Process one event from the batch config.

    Returns a result dict with:
      event_slug, hub_slug, hub_resolution (reuse/mint/queue_review/skip),
      is_nary, role_edges, supersede_candidates, validation, usage, warning_messages.

    Flushes role edges and supersede candidates incrementally to disk as soon as
    the LLM call succeeds, so a SIGKILL loses at most the single in-flight event.
    Writes a ledger entry on completion.
    Raises RateLimitError if the claude -p wall is hit (caller must handle).
    """
    event_slug = event_cfg["event_slug"]
    event_title = event_cfg["event_title"]
    chapter_files_rel = event_cfg.get("chapter_files", [])
    participants_override = event_cfg.get("participants", [])
    additional_context = event_cfg.get("additional_context", "")
    nary_known = event_cfg.get("nary_known", None)  # True/False/None (None = let LLM decide)
    skip_reason = event_cfg.get("skip_reason", None)  # pre-declared clean dyad skip

    # Output paths for incremental flush
    role_edges_path = output_dir / "role-edges-staging.jsonl"
    supersede_path = output_dir / "supersede-candidates.jsonl"
    hub_review_path = output_dir / "hub-review-queue.jsonl"

    result: dict[str, Any] = {
        "event_slug": event_slug,
        "event_title": event_title,
        "hub_slug": None,
        "hub_resolution": None,
        "is_nary": None,
        "nary_reason": None,
        "role_edges": [],
        "supersede_candidates": [],
        "validation": None,
        "usage": None,
        "warnings": [],
        "error": None,
    }

    # Abort immediately if the rate-limit wall was tripped by another thread
    if _RATE_LIMIT_WALL.is_set():
        result["error"] = "rate-limit-wall"
        result["hub_resolution"] = "aborted-rate-limit-wall"
        return result

    # --- Pre-declared skip (clean dyad) ---
    if skip_reason:
        result["hub_resolution"] = "skip-clean-dyad"
        result["is_nary"] = False
        result["nary_reason"] = skip_reason
        print(f"  [{event_slug}] SKIP (pre-declared clean dyad): {skip_reason}")
        return result

    # --- Resolve chapter files ---
    chapter_files: list[Path] = []
    for rel in chapter_files_rel:
        p = _REPO / rel
        if p.exists():
            chapter_files.append(p)
        else:
            result["warnings"].append(f"Chapter file not found: {rel}")
            print(f"  [{event_slug}] WARN: chapter file not found: {rel}", file=sys.stderr)

    if not chapter_files:
        result["error"] = "No chapter files found; skipping"
        result["hub_resolution"] = "error-no-chapters"
        print(f"  [{event_slug}] ERROR: no chapter files; skipping", file=sys.stderr)
        return result

    # --- Q2: Hub resolution ---
    # Priority 1: try event_slug directly in the lookup (slug and space forms).
    # This is the canonical first-look: if the config's event_slug maps exactly,
    # that is a high-confidence reuse (the slug is already the node slug).
    direct_slug = (
        lookup.get(event_slug)
        or lookup.get(event_slug.replace("-", " "))
    )
    if direct_slug:
        resolved_slug, match_type, score = direct_slug, "slug", 1.0
    else:
        # Fuzzy threshold raised to 0.80 to avoid false-positive cross-event matches
        # (e.g. "execution-of-eddard-stark" fuzzy-matching "arrest-of-eddard-stark" at 0.75)
        resolved_slug, match_type, score = resolve_event_slug(event_title, lookup, threshold=0.80)

    if match_type in ("exact", "slug", "token_sorted"):
        hub_slug = resolved_slug
        result["hub_resolution"] = "reuse"
        print(f"  [{event_slug}] REUSE: '{event_title}' → '{hub_slug}' (match: {match_type})")
    elif match_type == "fuzzy_medium":
        # Queue for human review; use event_slug as provisional hub
        hub_slug = event_slug
        result["hub_resolution"] = "queue_review"
        result["warnings"].append(
            f"Fuzzy-only match for '{event_title}' → '{resolved_slug}' (score={score:.2f}). "
            f"Queued for review; using event_slug as provisional hub."
        )
        print(f"  [{event_slug}] QUEUE_REVIEW: fuzzy hit '{resolved_slug}' score={score:.2f}")
        # Write to hub-review-queue.jsonl
        review_entry = {
            "event_slug": event_slug,
            "event_title": event_title,
            "fuzzy_match": resolved_slug,
            "fuzzy_score": round(score, 3),
            "action": "review_before_mint",
        }
        _append_jsonl_locked(hub_review_path, review_entry)
    else:
        # Mint a new node
        hub_slug = event_slug
        result["hub_resolution"] = "mint"
        print(f"  [{event_slug}] MINT: no match in reuse lookup, minting new hub '{hub_slug}'")

    result["hub_slug"] = hub_slug

    # Verify hub node exists on disk (for reuse; for mint it won't yet)
    hub_node_path = _NODES_DIR / "events" / f"{hub_slug}.node.md"
    if result["hub_resolution"] == "reuse" and not hub_node_path.exists():
        result["warnings"].append(f"Hub resolution=reuse but node not found on disk: {hub_slug}")

    # --- Parse extraction files ---
    all_events: list[dict[str, str]] = []
    all_relationships: list[str] = []
    chapter_labels: list[str] = []
    source_files: list[str] = []

    for cf in chapter_files:
        parsed = parse_extraction_sections(cf)
        all_events.extend(parsed["events"])
        all_relationships.extend(parsed["relationships"])
        chapter_labels.append(parsed["chapter"])
        source_files.append(parsed["source_file"])

    # Filter to trigger-family events only (bold-title-based; see filter_trigger_events).
    relevant_events_dicts = filter_trigger_events(all_events)
    if not relevant_events_dicts:
        relevant_events_dicts = all_events[:30]
        result["warnings"].append("No Q1 trigger events found; using first 30 events as fallback")
    # Flatten to strings for the LLM prompt (it wants narrative context — full_text).
    relevant_events = [e.get("full_text", "") for e in relevant_events_dicts]

    # --- LLM role assignment ---
    chapter_label = chapter_labels[0] if chapter_labels else ""
    source_file_label = source_files[0] if source_files else ""

    if dry_run:
        print(f"  [{event_slug}] DRY RUN: skipping claude -p call")
        # Deterministic fake response: two agents, one victim, one location.
        # Slug names are prefixed "dry-run-" so they never collide with real graph nodes.
        parsed_response = {
            "event_slug": hub_slug,
            "event_title": event_title,
            "is_nary": True,
            "nary_reason": "dry-run: multiple agents for test purposes",
            "participants": [
                {
                    "slug": f"dry-run-agent-a-{event_slug[:20]}",
                    "name": "Dry Run Agent A",
                    "role": "AGENT_IN",
                    "confidence": 1,
                    "rationale": "dry-run deterministic stub",
                    "evidence_quote": "(dry-run)",
                },
                {
                    "slug": f"dry-run-agent-b-{event_slug[:20]}",
                    "name": "Dry Run Agent B",
                    "role": "COMMANDS_IN",
                    "confidence": 1,
                    "rationale": "dry-run deterministic stub",
                    "evidence_quote": "(dry-run)",
                },
                {
                    "slug": f"dry-run-victim-{event_slug[:20]}",
                    "name": "Dry Run Victim",
                    "role": "VICTIM_IN",
                    "confidence": 1,
                    "rationale": "dry-run deterministic stub",
                    "evidence_quote": "(dry-run)",
                },
                {
                    "slug": f"dry-run-location-{event_slug[:20]}",
                    "name": "Dry Run Location",
                    "role": "LOCATED_AT",
                    "confidence": 1,
                    "rationale": "dry-run deterministic stub",
                    "evidence_quote": "(dry-run)",
                },
            ],
        }
        usage_info = {"cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0, "elapsed_seconds": 0.0, "dry_run": True}
    else:
        try:
            parsed_response, usage_info = call_claude_for_roles(
                event_slug=hub_slug,
                event_title=event_title,
                events_lines=relevant_events,
                relationships_lines=all_relationships[:50],  # cap relationship rows
                participants=participants_override,
                additional_context=additional_context,
                model=model,
            )
        except RateLimitError:
            # Hard wall — propagate up so the run_full_corpus / run_batch loop can handle it
            raise
        except Exception as exc:
            result["error"] = str(exc)
            result["hub_resolution"] = f"error-llm-{result['hub_resolution']}"
            print(f"  [{event_slug}] ERROR calling claude -p: {exc}", file=sys.stderr)
            # FIX 2026-06-07: do NOT write the ledger on transient LLM errors.
            # Writing here would cause --resume to SKIP the failed event forever.
            # Errors are retryable — leave the event uncommitted so the next run picks it up.
            return result

    result["usage"] = usage_info
    is_nary = parsed_response.get("is_nary", True)
    nary_reason = parsed_response.get("nary_reason", "")

    # D8 gate: if LLM says clean dyad, skip
    if not is_nary:
        result["is_nary"] = False
        result["nary_reason"] = nary_reason
        result["hub_resolution"] = "skip-clean-dyad"
        print(f"  [{event_slug}] D8 GATE: LLM returned is_nary=false → SKIP. Reason: {nary_reason}")
        if ledger_path:
            write_ledger_entry(ledger_path, event_slug, result.get("hub_slug") or event_slug, "skip-clean-dyad", 0)
        return result

    result["is_nary"] = True
    result["nary_reason"] = nary_reason

    # --- FIX 2: Borderline single-agent gate ---
    # If LLM says n-ary, double-check: if there is exactly 1 AGENT_IN, 0-1 VICTIM_IN,
    # and 0 COMMANDS_IN (meaning the single agent both ordered AND executed), this is
    # effectively a clean dyad. Route to hub-review-queue.jsonl rather than auto-reifying.
    # Clearly n-ary events (distinct instigator, multiple agents/victims, multi-chapter
    # set-pieces) are NOT affected.
    participants_from_llm = parsed_response.get("participants", [])
    agent_count = sum(1 for p in participants_from_llm if p.get("role") == "AGENT_IN")
    victim_count = sum(1 for p in participants_from_llm if p.get("role") == "VICTIM_IN")
    commands_count = sum(1 for p in participants_from_llm if p.get("role") == "COMMANDS_IN")
    is_borderline_single_agent = (
        agent_count == 1
        and victim_count <= 1
        and commands_count == 0
        and len(chapter_files) <= 1  # multi-chapter events are always n-ary set-pieces
    )
    if is_borderline_single_agent:
        borderline_reason = (
            f"Single AGENT_IN ({agent_count}), {victim_count} VICTIM_IN, "
            f"{commands_count} COMMANDS_IN — effectively a clean dyad. "
            f"nary_reason from LLM: {nary_reason!r}"
        )
        result["hub_resolution"] = "borderline-single-agent"
        result["is_nary"] = False
        result["nary_reason"] = borderline_reason
        review_entry = {
            "event_slug": event_slug,
            "event_title": event_title,
            "reason": "borderline-single-agent",
            "detail": borderline_reason,
            "llm_nary_reason": nary_reason,
            "participants": participants_from_llm,
            "produced_at": datetime.now(timezone.utc).isoformat(),
        }
        _append_jsonl_locked(hub_review_path, review_entry)
        if ledger_path:
            write_ledger_entry(ledger_path, event_slug, result.get("hub_slug") or event_slug, "borderline-single-agent", 0)
        print(
            f"  [{event_slug}] BORDERLINE: single-agent gate → review queue "
            f"(agents={agent_count}, victims={victim_count}, commands={commands_count})"
        )
        return result

    # --- FIX 3: Pure-agent (non-harming-multi-agent) guard (added 2026-06-07) ---
    # If LLM says n-ary but there are NO VICTIMs and NO COMMANDS (just multiple agents
    # acting without harm — typical of journeys, councils, observations, discussions),
    # this is almost certainly a narrative micro-beat that slipped past the keyword filter.
    # Route to hub-review-queue for human triage. Genuine n-ary events without victims
    # (e.g. coronations) are rare and worth eyeballing.
    is_pure_agent_no_harm = (
        victim_count == 0
        and commands_count == 0
        and agent_count >= 2
    )
    if is_pure_agent_no_harm:
        pure_agent_reason = (
            f"{agent_count} AGENT_IN, 0 VICTIM_IN, 0 COMMANDS_IN — "
            f"non-harming multi-agent event (likely journey/council/observation). "
            f"nary_reason from LLM: {nary_reason!r}"
        )
        result["hub_resolution"] = "non-harming-multi-agent"
        result["is_nary"] = False
        result["nary_reason"] = pure_agent_reason
        review_entry = {
            "event_slug": event_slug,
            "event_title": event_title,
            "reason": "non-harming-multi-agent",
            "detail": pure_agent_reason,
            "llm_nary_reason": nary_reason,
            "participants": participants_from_llm,
            "produced_at": datetime.now(timezone.utc).isoformat(),
        }
        _append_jsonl_locked(hub_review_path, review_entry)
        if ledger_path:
            write_ledger_entry(ledger_path, event_slug, result.get("hub_slug") or event_slug, "non-harming-multi-agent", 0)
        print(
            f"  [{event_slug}] NON-HARMING: pure-agent gate → review queue "
            f"(agents={agent_count}, victims=0, commands=0)"
        )
        return result

    # --- Mint node if needed ---
    if result["hub_resolution"] == "mint":
        minted_dir = output_dir / "minted-event-nodes"
        minted_path = minted_dir / f"{hub_slug}.node.md"
        if not minted_path.exists():
            # Determine event type (default to event.battle for battles, event.war for wars, etc.)
            event_type = event_cfg.get("event_type", "event.battle")
            description = event_cfg.get("description", f"Event node minted by Plate 3 for: {event_title}")
            mint_event_node(
                event_title=event_title,
                event_slug=hub_slug,
                event_type=event_type,
                description=description,
                evidence_chapters=chapter_labels,
                minted_dir=minted_dir,
            )
            print(f"  [{event_slug}] MINTED: {minted_path.name}")
        else:
            print(f"  [{event_slug}] MINT: node already minted this run, skipping duplicate write")

    # --- Emit role edges ---
    raw_edges = emit_role_edges(parsed_response, chapter_label, source_file_label)
    result["role_edges"] = raw_edges

    # --- Cross-chapter dedup (within this event) + cross-run dedup (against existing file) ---
    # Dedup key: (source_slug, edge_type, target_slug, evidence_chapter)
    # The evidence_chapter dimension is the extra field that makes cross-run dedup safe:
    # two events with overlapping participants but different chapters won't collide.
    seen_within_event: set[tuple] = set()
    deduped_edges: list[dict] = []
    cross_run_skipped = 0
    for edge in raw_edges:
        key = (
            edge.get("source_slug"),
            edge.get("edge_type"),
            edge.get("target_slug"),
            edge.get("evidence_chapter", ""),
        )
        if key in seen_within_event:
            result["warnings"].append(f"Within-event dedup removed duplicate: {key}")
            continue
        seen_within_event.add(key)
        # Cross-run dedup: skip edges already written in a prior run
        if existing_role_edge_keys and key in existing_role_edge_keys:
            cross_run_skipped += 1
            continue
        deduped_edges.append(edge)

    if cross_run_skipped:
        result["warnings"].append(
            f"Cross-run dedup skipped {cross_run_skipped} edges already in role-edges-staging.jsonl"
        )

    result["role_edges"] = deduped_edges

    # --- INCREMENTAL FLUSH: role edges to disk immediately ---
    for edge in deduped_edges:
        _append_jsonl_locked(role_edges_path, edge)

    # --- Supersede detection (D2) ---
    participant_slugs: set[str] = set()
    for p in parsed_response.get("participants", []):
        participant_slugs.add(p.get("slug", ""))
    # Also add participants from config if override provided
    for p in participants_override:
        participant_slugs.add(p.get("slug", ""))
    participant_slugs.discard("")

    # Build the chapter ID set for this event (used by the chapter-overlap filter in FIX 1).
    # chapter_labels are like "ASOS 7" (from the parser), but evidence_chapter in edges.jsonl
    # is the file-stem format (e.g. "asos-catelyn-07"). Derive both from the chapter file paths.
    event_chapter_ids: set[str] = set()
    for cf in chapter_files:
        # cf is a Path like .../asos-catelyn-07.extraction.md
        stem = cf.stem.replace(".extraction", "")  # → asos-catelyn-07
        event_chapter_ids.add(stem)

    supersede_candidates = find_supersede_candidates(
        all_graph_edges, participant_slugs, hub_slug, event_chapter_ids
    )
    result["supersede_candidates"] = supersede_candidates

    # --- INCREMENTAL FLUSH: supersede candidates to disk immediately ---
    for cand in supersede_candidates:
        _append_jsonl_locked(supersede_path, cand)

    # --- Contract 10 validation ---
    minted_slugs: set[str] = set()
    if result["hub_resolution"] == "mint":
        minted_slugs.add(hub_slug)
    # Also scan queue_review provisional hubs
    if result["hub_resolution"] == "queue_review":
        minted_slugs.add(hub_slug)

    validation = validate_role_edges(deduped_edges, slug_category_index, minted_slugs)
    result["validation"] = {
        "keep": len(validation["keep"]),
        "flag": len(validation["flag"]),
        "drop": len(validation["drop"]),
        "passed": len(validation["drop"]) == 0,
        "drop_details": [d["reason"] for d in validation["drop"]],
    }

    # --- LEDGER: record this event as processed ---
    if ledger_path:
        write_ledger_entry(
            ledger_path,
            event_key=event_slug,
            hub_slug=hub_slug,
            outcome=result["hub_resolution"],
            n_role_edges=len(deduped_edges),
        )

    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _append_jsonl_locked(path: Path, obj: dict) -> None:
    """Thread-safe version of _append_jsonl."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with _WRITE_LOCK:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Ledger: processed-events tracking for --resume
# ---------------------------------------------------------------------------

def load_ledger(ledger_path: Path) -> dict[str, dict]:
    """Load processed-events.jsonl → {event_key: ledger_row}.

    event_key is event_slug for --all mode (one event_cfg per hub_slug).
    """
    ledger: dict[str, dict] = {}
    if not ledger_path.exists():
        return ledger
    with open(ledger_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                key = row.get("event_key", "")
                if key:
                    ledger[key] = row
            except json.JSONDecodeError:
                pass
    return ledger


def write_ledger_entry(ledger_path: Path, event_key: str, hub_slug: str, outcome: str, n_role_edges: int) -> None:
    """Append one entry to the processed-events ledger (thread-safe)."""
    entry = {
        "event_key": event_key,
        "hub_slug": hub_slug,
        "outcome": outcome,
        "n_role_edges": n_role_edges,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    _append_jsonl_locked(ledger_path, entry)


def load_existing_role_edges(role_edges_path: Path) -> set[tuple]:
    """Return a set of dedup keys (source_slug, edge_type, target_slug, evidence_chapter)
    from an existing role-edges-staging.jsonl, for cross-run dedup on --resume.
    """
    seen: set[tuple] = set()
    if not role_edges_path.exists():
        return seen
    with open(role_edges_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                edge = json.loads(line)
                key = (
                    edge.get("source_slug", ""),
                    edge.get("edge_type", ""),
                    edge.get("target_slug", ""),
                    edge.get("evidence_chapter", ""),
                )
                seen.add(key)
            except json.JSONDecodeError:
                pass
    return seen


# ---------------------------------------------------------------------------
# Batch runner
# ---------------------------------------------------------------------------

def run_batch(
    config_path: Path,
    output_dir: Path,
    model: str,
    dry_run: bool = False,
    concurrency: int = 5,
) -> None:
    """Process all events in the batch config JSON file.

    Config JSON format:
    {
      "events": [
        {
          "event_slug": "red-wedding",
          "event_title": "The Red Wedding",
          "chapter_files": ["extractions/mechanical/asos/asos-catelyn-07.extraction.md", ...],
          "participants": [...],      // optional pre-identified participants
          "additional_context": "",   // optional extra context for LLM
          "skip_reason": null,        // if set, pre-declare as clean dyad skip
          "event_type": "event.battle",  // for minted nodes
          "description": "..."        // for minted nodes
        }
      ]
    }
    """
    with open(config_path, encoding="utf-8") as fh:
        config = json.load(fh)

    events = config.get("events", [])
    if not events:
        print(f"[warn] No events found in config {config_path}", file=sys.stderr)
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    role_edges_path = output_dir / "role-edges-staging.jsonl"
    skipped_dyads_path = output_dir / "skipped-clean-dyads.jsonl"
    hub_review_queue_path = output_dir / "hub-review-queue.jsonl"
    supersede_candidates_path = output_dir / "supersede-candidates.jsonl"

    # Clear output files for idempotent re-run
    for p in [role_edges_path, skipped_dyads_path, supersede_candidates_path]:
        if p.exists():
            p.unlink()

    print(f"\n=== Plate 3 Batch Run ===")
    print(f"Config: {config_path}")
    print(f"Events: {len(events)}")
    print(f"Output: {output_dir}")
    print(f"Model:  {model}")
    print(f"DryRun: {dry_run}")
    print(f"Concurrency: {concurrency}")
    print()

    # Load shared state
    lookup = load_reuse_lookup(_REUSE_LOOKUP)
    all_graph_edges = load_edges_jsonl(_EDGES_JSONL)
    slug_category_index = build_slug_category_index(_NODES_DIR)

    print(f"Loaded {len(lookup)} reuse lookup keys")
    print(f"Loaded {len(all_graph_edges)} graph edges for supersede detection")
    print(f"Loaded {len(slug_category_index)} node slugs for validation")
    print()

    all_results: list[dict] = []

    # Run events with concurrency cap
    # Note: events with skip_reason are handled synchronously (no LLM call)
    # Others go through the thread pool
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(
                process_event,
                event_cfg=ev,
                lookup=lookup,
                all_graph_edges=all_graph_edges,
                slug_category_index=slug_category_index,
                output_dir=output_dir,
                model=model,
                dry_run=dry_run,
            ): ev["event_slug"]
            for ev in events
        }

        for future in as_completed(futures):
            event_slug = futures[future]
            try:
                result = future.result()
                all_results.append(result)
            except Exception as exc:
                print(f"  [{event_slug}] FATAL ERROR: {exc}", file=sys.stderr)
                all_results.append({
                    "event_slug": event_slug,
                    "error": str(exc),
                    "hub_resolution": "error-fatal",
                    "role_edges": [],
                    "supersede_candidates": [],
                    "warnings": [],
                })

    # Sort results back to config order
    slug_order = {ev["event_slug"]: i for i, ev in enumerate(events)}
    all_results.sort(key=lambda r: slug_order.get(r.get("event_slug", ""), 9999))

    # --- Write outputs ---
    total_role_edges = 0
    total_supersede = 0
    total_skipped = 0
    total_borderline = 0
    total_reified = 0
    total_minted = 0
    total_reused = 0
    total_queued = 0
    total_errors = 0
    total_cost = 0.0
    role_edge_type_counts: dict[str, int] = {}
    validation_failures: list[str] = []

    for result in all_results:
        resolution = result.get("hub_resolution", "")

        # FIX 2: borderline-single-agent routes to hub-review-queue.jsonl (already written
        # inside process_event). Count it separately from clean dyad skips.
        if resolution == "borderline-single-agent":
            total_borderline += 1
            usage = result.get("usage") or {}
            total_cost += usage.get("cost_usd", 0.0)
            continue

        if resolution in ("skip-clean-dyad",):
            total_skipped += 1
            skip_entry = {
                "event_slug": result["event_slug"],
                "event_title": next(
                    (e["event_title"] for e in events if e["event_slug"] == result["event_slug"]),
                    result["event_slug"],
                ),
                "reason": result.get("nary_reason", "pre-declared skip"),
                "produced_at": datetime.now(timezone.utc).isoformat(),
            }
            _append_jsonl(skipped_dyads_path, skip_entry)
            continue

        if "error" in result and result.get("error"):
            total_errors += 1
            continue

        # Role edges
        for edge in result.get("role_edges", []):
            _append_jsonl(role_edges_path, edge)
            et = edge.get("edge_type", "UNKNOWN")
            role_edge_type_counts[et] = role_edge_type_counts.get(et, 0) + 1
            total_role_edges += 1

        # Supersede candidates
        for cand in result.get("supersede_candidates", []):
            _append_jsonl(supersede_candidates_path, cand)
            total_supersede += 1

        # Validation failures
        val = result.get("validation") or {}
        if val.get("drop"):
            for detail in val.get("drop_details", []):
                validation_failures.append(f"{result['event_slug']}: {detail}")

        # Counters
        if resolution == "reuse":
            total_reused += 1
        elif resolution == "mint":
            total_minted += 1
        elif resolution == "queue_review":
            total_queued += 1

        is_nary = result.get("is_nary", False)
        if is_nary and resolution not in ("skip-clean-dyad", "error-no-chapters", "borderline-single-agent"):
            total_reified += 1

        usage = result.get("usage") or {}
        total_cost += usage.get("cost_usd", 0.0)

    # --- Per-event summary table ---
    print("\n=== BATCH RESULTS ===")
    print(f"{'Event':<45} {'Hub':<35} {'Resolution':<18} {'N-ary':<7} {'Edges':<6} {'Supersede':<10} {'Valid'}")
    print(f"{'-'*45} {'-'*35} {'-'*18} {'-'*7} {'-'*6} {'-'*10} {'-'*6}")
    for result in all_results:
        slug = result.get("event_slug", "")[:44]
        hub = (result.get("hub_slug") or "—")[:34]
        res = result.get("hub_resolution", "—")[:17]
        n_ary = "YES" if result.get("is_nary") else ("SKIP" if result.get("hub_resolution", "").startswith("skip") else "NO")
        n_edges = len(result.get("role_edges", []))
        n_super = len(result.get("supersede_candidates", []))
        val = result.get("validation") or {}
        valid = "PASS" if val.get("passed", True) else f"FAIL({val.get('drop', 0)})"
        if result.get("error"):
            valid = f"ERROR"
        print(f"{slug:<45} {hub:<35} {res:<18} {n_ary:<7} {n_edges:<6} {n_super:<10} {valid}")

    # --- Totals ---
    print(f"\n=== TOTALS ===")
    print(f"  Events processed:        {len(events)}")
    print(f"  Reified (n-ary):         {total_reified}")
    print(f"  Skipped (clean dyad):    {total_skipped}")
    print(f"  Borderline (queued):     {total_borderline}  ← routed to hub-review-queue.jsonl")
    print(f"  Errors:                  {total_errors}")
    print()
    print(f"  Hubs reused:             {total_reused}")
    print(f"  Hubs minted:             {total_minted}")
    print(f"  Hubs queued for review:  {total_queued}")
    print()
    print(f"  Role edges staged:     {total_role_edges}")
    print(f"  By type:")
    for et, count in sorted(role_edge_type_counts.items()):
        print(f"    {et:<20} {count}")
    print()
    print(f"  Supersede candidates:  {total_supersede}")
    print()
    if validation_failures:
        print(f"  Contract 10 FAILURES ({len(validation_failures)}):")
        for vf in validation_failures:
            print(f"    {vf}")
    else:
        print(f"  Contract 10: ALL PASSED")
    print()
    print(f"  Total LLM cost:        ${total_cost:.4f}")
    print()
    print(f"  Output files:")
    print(f"    {role_edges_path}")
    print(f"    {skipped_dyads_path}")
    print(f"    {hub_review_queue_path}")
    print(f"    {supersede_candidates_path}")
    print(f"    {output_dir / 'minted-event-nodes/'}")

    # --- Write summary JSON ---
    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "config": str(config_path),
        "model": model,
        "dry_run": dry_run,
        "events_processed": len(events),
        "total_reified": total_reified,
        "total_skipped": total_skipped,
        "total_errors": total_errors,
        "hubs_reused": total_reused,
        "hubs_minted": total_minted,
        "hubs_queued_review": total_queued,
        "total_borderline_queued": total_borderline,
        "total_role_edges": total_role_edges,
        "role_edge_type_counts": role_edge_type_counts,
        "total_supersede_candidates": total_supersede,
        "contract10_passed": len(validation_failures) == 0,
        "contract10_failures": validation_failures,
        "total_cost_usd": round(total_cost, 6),
        "per_event_results": [
            {
                "event_slug": r.get("event_slug"),
                "hub_slug": r.get("hub_slug"),
                "hub_resolution": r.get("hub_resolution"),
                "is_nary": r.get("is_nary"),
                "nary_reason": r.get("nary_reason"),
                "role_edges_count": len(r.get("role_edges", [])),
                "supersede_candidates_count": len(r.get("supersede_candidates", [])),
                "validation": r.get("validation"),
                "warnings": r.get("warnings", []),
                "error": r.get("error"),
                "cost_usd": (r.get("usage") or {}).get("cost_usd", 0.0),
            }
            for r in all_results
        ],
    }
    summary_path = output_dir / "plate3-minibatch-summary.json"
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
    print(f"    {summary_path}")
    print()


# ---------------------------------------------------------------------------
# Smoke test: Red Wedding (kept for regression / original de-risk test)
# ---------------------------------------------------------------------------

_RED_WEDDING_SUPERSEDE_CANDIDATES = [
    {"edge_type": "BETRAYS",              "source_slug": "roose-bolton",  "target_slug": "robb-stark"},
    {"edge_type": "BETRAYS",              "source_slug": "walder-frey",   "target_slug": "robb-stark"},
    {"edge_type": "KILLS",                "source_slug": "raymund-frey",  "target_slug": "catelyn-stark"},
    {"edge_type": "KILLS",                "source_slug": "ryman-frey",    "target_slug": "dacey-mormont"},
    {"edge_type": "KILLS",                "source_slug": "hosteen-frey",  "target_slug": "lucas-blackwood"},
    {"edge_type": "VIOLATES_GUEST_RIGHT", "source_slug": "walder-frey",   "target_slug": "robb-stark"},
    {"edge_type": "VIOLATES_GUEST_RIGHT", "source_slug": "walder-frey",   "target_slug": "catelyn-stark"},
    {"edge_type": "VIOLATES_GUEST_RIGHT", "source_slug": "house-frey",    "target_slug": "robb-stark"},
    {"edge_type": "VIOLATES_GUEST_RIGHT", "source_slug": "house-frey",    "target_slug": "catelyn-stark"},
]


def smoke_test_red_wedding(
    chapter_files: list[Path],
    event_slug: str,
    model: str,
    dry_run: bool = False,
) -> None:
    """Original smoke-test mode — kept for regression testing."""
    print(f"\n=== Plate 3 Smoke Test: {event_slug} ===\n")

    lookup = load_reuse_lookup(_REUSE_LOOKUP)
    resolved_slug = lookup.get(event_slug) or lookup.get(event_slug.replace("-", " "))
    if not resolved_slug:
        resolved_slug, match_type, _ = resolve_event_slug(event_slug.replace("-", " "), lookup)

    if resolved_slug:
        print(f"  REUSE: '{event_slug}' → existing hub '{resolved_slug}'")
        hub_slug = resolved_slug
    else:
        print(f"  [warn] No match in reuse lookup for '{event_slug}'. Would MINT.")
        hub_slug = event_slug

    hub_node_path = _NODES_DIR / "events" / f"{hub_slug}.node.md"
    if hub_node_path.exists():
        print(f"  Hub node confirmed: graph/nodes/events/{hub_slug}.node.md")
    else:
        print(f"  [warn] Hub node NOT found at {hub_node_path}")

    print(f"\nStep 2: Parsing {len(chapter_files)} extraction file(s)...")
    all_events: list[dict[str, str]] = []
    all_relationships: list[str] = []
    all_chapters: list[str] = []
    all_source_files: list[str] = []

    for cf in chapter_files:
        if not cf.exists():
            print(f"  [warn] File not found: {cf}", file=sys.stderr)
            continue
        parsed = parse_extraction_sections(cf)
        all_events.extend(parsed["events"])
        all_relationships.extend(parsed["relationships"])
        all_chapters.append(parsed["chapter"])
        all_source_files.append(parsed["source_file"])
        print(f"  {cf.name}: {len(parsed['events'])} events, {len(parsed['relationships'])} relationships")

    catelyn_07_file = next((cf for cf in chapter_files if "catelyn-07" in cf.name), None)
    if catelyn_07_file:
        catelyn_07_parsed = parse_extraction_sections(catelyn_07_file)
        relevant_events_dicts = catelyn_07_parsed["events"]
        all_relationships_for_event = catelyn_07_parsed["relationships"]
    else:
        relevant_events_dicts = filter_trigger_events(all_events)
        all_relationships_for_event = all_relationships
    # Flatten to strings for the LLM prompt (uses full_text — bold_title + description).
    relevant_events = [e.get("full_text", "") for e in relevant_events_dicts]

    participants = [
        {"slug": "walder-frey",       "name": "Walder Frey (Lord of the Crossing)"},
        {"slug": "tywin-lannister",   "name": "Tywin Lannister"},
        {"slug": "lothar-frey",       "name": "Lame Lothar Frey"},
        {"slug": "roose-bolton",      "name": "Roose Bolton"},
        {"slug": "ryman-frey",        "name": "Ser Ryman Frey"},
        {"slug": "hosteen-frey",      "name": "Ser Hosteen Frey"},
        {"slug": "raymund-frey",      "name": "Raymund Frey"},
        {"slug": "black-walder-frey", "name": "Black Walder Frey"},
        {"slug": "robb-stark",        "name": "Robb Stark"},
        {"slug": "catelyn-stark",     "name": "Catelyn Stark"},
        {"slug": "dacey-mormont",     "name": "Dacey Mormont"},
        {"slug": "twins",             "name": "The Twins"},
    ]

    additional_context = (
        "From the ASOS Epilogue (Merrett Frey POV): "
        "Lame Lothar plotted the Red Wedding with Roose Bolton, arranging the musicians with crossbows. "
        "Lord Walder ordered the slaughter. Raymund Frey cut Catelyn's throat. "
        "Roose Bolton killed Robb Stark directly ('Jaime Lannister sends his regards'). "
        "Tywin Lannister countenanced Walder's actions and had corresponded with Walder beforehand."
    )

    print(f"\nStep 4: Calling claude -p (model: {model}, cwd=/tmp)...")

    if dry_run:
        parsed_response = {
            "event_slug": hub_slug,
            "event_title": "Red Wedding",
            "is_nary": True,
            "nary_reason": "Multiple killers/victims + instigator≠executor (dry-run)",
            "participants": [
                {"slug": "walder-frey",     "name": "Walder Frey",    "role": "COMMANDS_IN", "confidence": 1, "rationale": "Ordered the slaughter", "evidence_quote": "Lord Walder ordered the slaughter"},
                {"slug": "tywin-lannister", "name": "Tywin Lannister","role": "COMMANDS_IN", "confidence": 2, "rationale": "Countenanced the massacre", "evidence_quote": "Tywin countenanced Walder's actions"},
                {"slug": "lothar-frey",     "name": "Lame Lothar",    "role": "COMMANDS_IN", "confidence": 1, "rationale": "Planned logistics with Roose Bolton", "evidence_quote": "Lame Lothar who had plotted it out with Roose Bolton"},
                {"slug": "roose-bolton",    "name": "Roose Bolton",   "role": "AGENT_IN",    "confidence": 1, "rationale": "Personally killed Robb Stark", "evidence_quote": "Jaime Lannister sends his regards"},
                {"slug": "ryman-frey",      "name": "Ser Ryman Frey", "role": "AGENT_IN",    "confidence": 1, "rationale": "Killed Dacey Mormont", "evidence_quote": "He buries his axe head in her stomach"},
                {"slug": "hosteen-frey",    "name": "Ser Hosteen Frey","role": "AGENT_IN",   "confidence": 1, "rationale": "Cut down Lucas Blackwood", "evidence_quote": "Lucas Blackwood is cut down"},
                {"slug": "raymund-frey",    "name": "Raymund Frey",   "role": "AGENT_IN",    "confidence": 1, "rationale": "Cut Catelyn's throat", "evidence_quote": "Raymund opened her throat from ear to ear"},
                {"slug": "black-walder-frey","name": "Black Walder",  "role": "AGENT_IN",    "confidence": 1, "rationale": "Led attack on camps", "evidence_quote": "Black Walder led the attack on the camps"},
                {"slug": "robb-stark",      "name": "Robb Stark",     "role": "VICTIM_IN",   "confidence": 1, "rationale": "Killed by Roose Bolton", "evidence_quote": "He thrusts his longsword through Robb's heart"},
                {"slug": "catelyn-stark",   "name": "Catelyn Stark",  "role": "VICTIM_IN",   "confidence": 1, "rationale": "Throat cut by Raymund Frey", "evidence_quote": "Someone grabs her scalp and cuts her throat"},
                {"slug": "dacey-mormont",   "name": "Dacey Mormont",  "role": "VICTIM_IN",   "confidence": 1, "rationale": "Killed by Ryman Frey", "evidence_quote": "He buries his axe head in her stomach"},
                {"slug": "twins",           "name": "The Twins",      "role": "LOCATED_AT",  "confidence": 1, "rationale": "Location of the Red Wedding", "evidence_quote": "The wedding feast takes place at the Twins"},
            ],
        }
        usage_info = {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "elapsed_seconds": 0.0, "dry_run": True}
    else:
        parsed_response, usage_info = call_claude_for_roles(
            event_slug=hub_slug,
            event_title="Red Wedding",
            events_lines=relevant_events,
            relationships_lines=all_relationships_for_event,
            participants=participants,
            additional_context=additional_context,
            model=model,
        )

    print(f"  Token usage:")
    print(f"    Input:         {usage_info['input_tokens']:,}")
    print(f"    Cache create:  {usage_info.get('cache_creation_input_tokens', 0):,}")
    print(f"    Cache read:    {usage_info.get('cache_read_input_tokens', 0):,}")
    print(f"    Output:        {usage_info['output_tokens']:,}")
    print(f"    Cost:          ${usage_info['cost_usd']:.4f}")

    role_edges = emit_role_edges(parsed_response, all_chapters[0] if all_chapters else "", all_source_files[0] if all_source_files else "", run_label="plate3-smoke")

    slug_category_index = build_slug_category_index(_NODES_DIR)
    validation = validate_role_edges(role_edges, slug_category_index)
    keep_count = len(validation["keep"])
    flag_count = len(validation["flag"])
    drop_count = len(validation["drop"])

    print(f"\nContract 10: KEEP={keep_count} FLAG={flag_count} DROP={drop_count}")
    if drop_count == 0:
        print(f"  PASSED")
    else:
        print(f"  FAILED")

    output_path = _SMOKE_OUTPUT_DIR / f"plate3-smoke-{event_slug}.jsonl"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as fh:
        for edge in role_edges:
            fh.write(json.dumps(edge, ensure_ascii=False) + "\n")

    all_graph_edges = load_edges_jsonl(_EDGES_JSONL)
    found = []
    not_found = []
    for c in _RED_WEDDING_SUPERSEDE_CANDIDATES:
        matched = any(
            e.get("edge_type") == c["edge_type"]
            and e.get("source_slug") == c["source_slug"]
            and e.get("target_slug") == c["target_slug"]
            for e in all_graph_edges
        )
        (found if matched else not_found).append(c)

    print(f"\nSuperseded binaries: {len(found)} found in graph, {len(not_found)} not found")
    print(f"\nSmoke output: {output_path}")

    meta_path = _SMOKE_OUTPUT_DIR / f"plate3-smoke-{event_slug}-meta.json"
    meta = {
        "event_slug": hub_slug,
        "hub_node_exists": hub_node_path.exists(),
        "chapters_processed": [str(cf) for cf in chapter_files],
        "role_edges_emitted": len(role_edges),
        "validation": {"keep": keep_count, "flag": flag_count, "drop": drop_count, "passed": drop_count == 0},
        "superseded_candidates": {"found_in_graph": len(found), "not_found": len(not_found), "candidates": _RED_WEDDING_SUPERSEDE_CANDIDATES},
        "llm_usage": usage_info,
        "produced_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
    }
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
    print(f"Metadata: {meta_path}")


# ---------------------------------------------------------------------------
# Full corpus scan (--all mode)
# ---------------------------------------------------------------------------

def _title_to_slug_candidate(title: str) -> str:
    """Convert a Pass-1 event title to a candidate slug for minting.

    Removes common leading phrases that make poor slug roots.
    """
    t = title.lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    # slug-ify: spaces to hyphens, collapse runs
    slug = re.sub(r"\s+", "-", t)
    slug = re.sub(r"-+", "-", slug)
    # Truncate long slugs
    if len(slug) > 80:
        slug = slug[:80].rstrip("-")
    return slug


def run_full_corpus(
    output_dir: Path,
    model: str,
    dry_run: bool = False,
    concurrency: int = 5,
    resume: bool = False,
    max_events: int | None = None,
) -> None:
    """Full corpus scan: process all 344 chapter extractions in parallel.

    This implements the --all mode:
    1. Scan all extraction files, parse events, apply Q1 trigger filter.
    2. For each trigger event, try Q2 reuse lookup → assign to an existing hub or mint a slug.
    3. Cross-chapter dedup: group all chapters that share the same hub slug.
    4. For each hub group, run process_event via the thread pool.
    5. Apply chapter-overlap supersede detection (FIX 1) and borderline gate (FIX 2).
    6. Validate Contract 10, produce summary.

    Output: working/edge-modeling/plate3-full/
      role-edges-staging.jsonl      (append-only; incremental flush)
      skipped-clean-dyads.jsonl     (append-only; incremental flush)
      hub-review-queue.jsonl        (append-only; incremental flush)
      supersede-candidates.jsonl    (append-only; incremental flush)
      processed-events.jsonl        (ledger; append-only; one line per completed event)
      minted-event-nodes/
      plate3-full-summary.md        (written at end of run)

    With --resume: loads processed-events.jsonl ledger, skips completed events,
    deduplicates role edges against existing role-edges-staging.jsonl.

    Rate-limit safety: raises SystemExit(2) on a hard rate-limit wall, leaving
    all partial state intact for --resume.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    role_edges_path = output_dir / "role-edges-staging.jsonl"
    skipped_dyads_path = output_dir / "skipped-clean-dyads.jsonl"
    hub_review_queue_path = output_dir / "hub-review-queue.jsonl"
    supersede_candidates_path = output_dir / "supersede-candidates.jsonl"
    ledger_path = output_dir / "processed-events.jsonl"

    # --- Resume vs. fresh start ---
    if resume:
        ledger = load_ledger(ledger_path)
        existing_role_edge_keys = load_existing_role_edges(role_edges_path)
        print(f"\n=== Plate 3 Full Corpus Scan (RESUMING) ===")
        print(f"  Ledger: {len(ledger)} events already processed")
        print(f"  Existing role edges: {len(existing_role_edge_keys)} dedup keys loaded")
    else:
        ledger = {}
        existing_role_edge_keys = set()
        # Fresh run: clear output files for idempotent re-run
        # (Note: hub-review-queue.jsonl is NOT cleared so manual reviews survive)
        for p in [role_edges_path, skipped_dyads_path, supersede_candidates_path, ledger_path]:
            if p.exists():
                p.unlink()
        print(f"\n=== Plate 3 Full Corpus Scan ===")

    print(f"Output: {output_dir}")
    print(f"Model:  {model}")
    print(f"DryRun: {dry_run}")
    print(f"Concurrency: {concurrency}")
    print(f"Resume: {resume}")
    print()

    # Load shared state
    lookup = load_reuse_lookup(_REUSE_LOOKUP)
    all_graph_edges = load_edges_jsonl(_EDGES_JSONL)
    slug_category_index = build_slug_category_index(_NODES_DIR)

    print(f"Loaded {len(lookup)} reuse lookup keys")
    print(f"Loaded {len(all_graph_edges)} graph edges for supersede detection")
    print(f"Loaded {len(slug_category_index)} node slugs for validation")

    # Collect all extraction files
    all_extraction_files: list[Path] = []
    for book in ["agot", "acok", "asos", "affc", "adwd"]:
        book_dir = _EXTRACTIONS_DIR / book
        if book_dir.is_dir():
            all_extraction_files.extend(sorted(book_dir.glob("*.extraction.md")))

    print(f"Found {len(all_extraction_files)} extraction files")
    print()

    # Step 1: Parse all files, collect trigger events, group by hub slug
    # hub_slug → {chapter_files, event_title, event_slug}
    hub_to_chapters: dict[str, dict] = {}  # hub_slug → {title, chapters: [Path], event_slug}

    chapters_scanned = 0
    trigger_events_found = 0
    gate_e_skipped = 0
    gate_e_skip_path = output_dir / "gate-e-dialogue-recall-skipped.jsonl"

    for cf in all_extraction_files:
        chapters_scanned += 1
        parsed = parse_extraction_sections(cf)
        trigger_evts = filter_trigger_events(parsed["events"])

        for evt in trigger_evts:
            trigger_events_found += 1

            # Use BOLD TITLE as the canonical event title (clean, declarative event name
            # like "Red Wedding" / "Bran's fall" / "The execution"). Fall back to full_text
            # if bold is missing. This is the slug-quality fix (2026-06-07): slugifying the
            # 80-char description text produced micro-beat slugs like
            # "departure-at-daybreak-bran-rides-out-with-his-lord-father-...".
            event_title = (evt.get("bold_title") or "").strip()
            if not event_title:
                event_title = evt.get("full_text", "")[:100].strip()

            # Gate E (added 2026-06-07): dialogue/recall/discussion verb deny-list,
            # applied BEFORE the LLM call. Catches the 1A+1V+1C hole that fools
            # gates B/C/D (e.g. "Cersei reveals Joffrey ordered Eddard's execution").
            candidate_slug_for_gate = _title_to_slug_candidate(event_title)
            if is_dialogue_recall_slug(candidate_slug_for_gate):
                gate_e_skipped += 1
                _append_jsonl(gate_e_skip_path, {
                    "event_slug": candidate_slug_for_gate,
                    "event_title": event_title,
                    "source_chapter": str(cf.relative_to(_REPO)),
                    "reason": "gate-e-dialogue-recall-verb",
                    "produced_at": datetime.now(timezone.utc).isoformat(),
                })
                continue

            resolved_slug, match_type, score = resolve_event_slug(event_title, lookup, threshold=0.80)

            if match_type in ("exact", "slug", "token_sorted"):
                hub_slug = resolved_slug
                resolution_type = "reuse"
            elif match_type == "fuzzy_medium":
                hub_slug = _title_to_slug_candidate(event_title)
                resolution_type = "queue_review"
            else:
                hub_slug = _title_to_slug_candidate(event_title)
                resolution_type = "mint"

            # Group this chapter under the hub
            if hub_slug not in hub_to_chapters:
                hub_to_chapters[hub_slug] = {
                    "event_slug": hub_slug,
                    "event_title": event_title,
                    "hub_slug": hub_slug,
                    "resolution_type": resolution_type,
                    "chapter_files": [],
                    "seen_chapter_paths": set(),
                }
            group = hub_to_chapters[hub_slug]
            # Cross-chapter dedup: add chapter file if not already included
            cf_str = str(cf)
            if cf_str not in group["seen_chapter_paths"]:
                group["seen_chapter_paths"].add(cf_str)
                group["chapter_files"].append(cf)
            # Keep the longest/most descriptive title (still bold-title; rare ties broken on length)
            if len(event_title) > len(group["event_title"]):
                group["event_title"] = event_title

    print(f"Chapters scanned: {chapters_scanned}")
    print(f"Trigger events found (GATE A): {trigger_events_found}")
    print(f"Gate E (dialogue/recall) skipped: {gate_e_skipped} → {gate_e_skip_path.name}")
    print(f"Unique hub groups (post-GATE-A+E): {len(hub_to_chapters)}")
    print()

    # Build event_cfg dicts from the hub groups
    events_to_process: list[dict] = []
    skipped_by_ledger = 0
    for hub_slug, group in hub_to_chapters.items():
        # --resume: skip events already in the ledger
        if resume and hub_slug in ledger:
            skipped_by_ledger += 1
            continue
        chapter_files_rel = [
            str(cf.relative_to(_REPO)) for cf in group["chapter_files"]
        ]
        events_to_process.append({
            "event_slug": group["event_slug"],
            "event_title": group["event_title"],
            "chapter_files": chapter_files_rel,
            "participants": [],
            "additional_context": "",
            "skip_reason": None,
            "event_type": _infer_event_type(group["event_title"]),
            "description": f"Event node minted by Plate 3 full-corpus scan for: {group['event_title']}",
        })

    if resume:
        print(f"Skipped by ledger (--resume): {skipped_by_ledger}")
    print(f"Events available to process: {len(events_to_process)}")

    # --max-events: cap this invocation for calibration / cost-bounded chunks.
    # Selection is deterministic (sorted by hub_slug) so successive --resume runs
    # under --max-events still make forward progress (ledger excludes done ones).
    if max_events is not None and len(events_to_process) > max_events:
        events_to_process.sort(key=lambda e: e["event_slug"])
        events_to_process = events_to_process[:max_events]
        print(f"--max-events cap: trimming to first {max_events} (deterministic by event_slug)")

    print(f"Events to process this run:  {len(events_to_process)}")
    print()

    if not events_to_process:
        print("All events already processed. Nothing to do.")
        return

    # Step 2: Process via thread pool — incremental flush inside process_event
    all_results: list[dict] = []
    rate_limit_hit = False
    total_events = len(events_to_process)

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit all futures up front (the wall check inside each process_event
        # means new work stops immediately when _RATE_LIMIT_WALL is set)
        futures = {
            executor.submit(
                process_event,
                event_cfg=ev,
                lookup=lookup,
                all_graph_edges=all_graph_edges,
                slug_category_index=slug_category_index,
                output_dir=output_dir,
                model=model,
                dry_run=dry_run,
                ledger_path=ledger_path,
                existing_role_edge_keys=existing_role_edge_keys,
            ): ev["event_slug"]
            for ev in events_to_process
        }

        done_count = 0
        running_cost = 0.0

        for future in as_completed(futures):
            event_slug = futures[future]
            done_count += 1
            try:
                result = future.result()
                all_results.append(result)
                running_cost += (result.get("usage") or {}).get("cost_usd", 0.0)

                # Progress report every 10 events or at the end
                if done_count % 10 == 0 or done_count == total_events:
                    print(
                        f"  Progress: {done_count}/{total_events} events done | "
                        f"cost so far: ${running_cost:.4f}"
                    )

            except RateLimitError as exc:
                # Hard wall — set the process-wide flag, cancel pending work,
                # then exit cleanly. All flushed data survives.
                _RATE_LIMIT_WALL.set()
                rate_limit_hit = True
                print(
                    f"\n[RATE LIMIT WALL] Hard quota/rate-limit hit on event {event_slug!r}.\n"
                    f"  Detail: {exc}\n"
                    f"  Stopping immediately. Partial state is intact.\n"
                    f"  Resume with: python3 scripts/edge-reify-backfill.py --all --resume\n",
                    file=sys.stderr,
                )
                # Cancel remaining futures (they'll check _RATE_LIMIT_WALL and return early)
                for f in futures:
                    f.cancel()
                # Don't break — let remaining in-flight futures drain (they check the wall flag)

            except Exception as exc:
                if _RATE_LIMIT_WALL.is_set():
                    # Already shutting down; ignore
                    continue
                print(f"  [{event_slug}] FATAL ERROR: {exc}", file=sys.stderr)
                all_results.append({
                    "event_slug": event_slug,
                    "error": str(exc),
                    "hub_resolution": "error-fatal",
                    "role_edges": [],
                    "supersede_candidates": [],
                    "warnings": [],
                })

    # Step 3: Tally results — NOTE: role edges and supersede candidates are already on disk.
    # The aggregation loop here only computes summary counters and flushes the skip file
    # (which is cheap to re-emit since process_event records it in the ledger).
    total_role_edges = 0
    total_supersede = 0
    total_skipped = 0
    total_borderline = 0
    total_reified = 0
    total_minted = 0
    total_reused = 0
    total_queued = 0
    total_errors = 0
    total_cost = 0.0
    role_edge_type_counts: dict[str, int] = {}
    validation_failures: list[str] = []

    for result in all_results:
        resolution = result.get("hub_resolution", "")

        if resolution == "aborted-rate-limit-wall":
            continue  # Not counted — not processed

        if resolution == "borderline-single-agent":
            total_borderline += 1
            usage = result.get("usage") or {}
            total_cost += usage.get("cost_usd", 0.0)
            continue

        if resolution in ("skip-clean-dyad",):
            total_skipped += 1
            skip_entry = {
                "event_slug": result["event_slug"],
                "event_title": result.get("event_title", result["event_slug"]),
                "reason": result.get("nary_reason", "pre-declared skip"),
                "produced_at": datetime.now(timezone.utc).isoformat(),
            }
            _append_jsonl_locked(skipped_dyads_path, skip_entry)
            continue

        if "error" in result and result.get("error"):
            total_errors += 1
            continue

        # Role edges and supersede candidates already flushed by process_event;
        # here we just count them for the summary.
        for edge in result.get("role_edges", []):
            et = edge.get("edge_type", "UNKNOWN")
            role_edge_type_counts[et] = role_edge_type_counts.get(et, 0) + 1
            total_role_edges += 1

        total_supersede += len(result.get("supersede_candidates", []))

        val = result.get("validation") or {}
        if val.get("drop"):
            for detail in val.get("drop_details", []):
                validation_failures.append(f"{result['event_slug']}: {detail}")

        if resolution == "reuse":
            total_reused += 1
        elif resolution == "mint":
            total_minted += 1
        elif resolution == "queue_review":
            total_queued += 1

        is_nary = result.get("is_nary", False)
        if is_nary and resolution not in ("skip-clean-dyad", "error-no-chapters", "borderline-single-agent"):
            total_reified += 1

        usage = result.get("usage") or {}
        total_cost += usage.get("cost_usd", 0.0)

    # Print summary
    print(f"\n=== FULL CORPUS RESULTS (this run) ===")
    print(f"  Chapters scanned:        {chapters_scanned}")
    print(f"  Trigger events found:    {trigger_events_found}")
    print(f"  Unique hub groups:       {len(hub_to_chapters)}")
    if resume:
        print(f"  Skipped by ledger:       {skipped_by_ledger}")
    print(f"  Events attempted:        {total_events}")
    print(f"  Reified (n-ary):         {total_reified}")
    print(f"  Skipped (clean dyad):    {total_skipped}")
    print(f"  Borderline (queued):     {total_borderline}  ← hub-review-queue.jsonl")
    print(f"  Errors:                  {total_errors}")
    print()
    print(f"  Hubs reused:             {total_reused}")
    print(f"  Hubs minted:             {total_minted}")
    print(f"  Hubs queued for review:  {total_queued}")
    print()
    print(f"  Role edges staged:       {total_role_edges}")
    print(f"  By type:")
    for et, count in sorted(role_edge_type_counts.items()):
        print(f"    {et:<20} {count}")
    print()
    print(f"  Supersede candidates:    {total_supersede}")
    print()
    if validation_failures:
        print(f"  Contract 10 FAILURES ({len(validation_failures)}):")
        for vf in validation_failures[:20]:
            print(f"    {vf}")
        if len(validation_failures) > 20:
            print(f"    ... and {len(validation_failures) - 20} more")
    else:
        print(f"  Contract 10: ALL PASSED")
    print()
    print(f"  Total LLM cost:          ${total_cost:.4f}")
    print()
    print(f"  Output directory: {output_dir}")
    print(f"  Ledger: {ledger_path}")

    if rate_limit_hit:
        print(
            f"\n[STOPPED EARLY — rate limit wall]\n"
            f"  Resume command:\n"
            f"    python3 scripts/edge-reify-backfill.py --all --resume\n"
        )

    # Write summary JSON (append run info; not clobbered on resume)
    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "mode": "full-corpus",
        "model": model,
        "dry_run": dry_run,
        "resume": resume,
        "rate_limit_hit": rate_limit_hit,
        "chapters_scanned": chapters_scanned,
        "trigger_events_found": trigger_events_found,
        "gate_e_dialogue_recall_skipped": gate_e_skipped,
        "unique_hub_groups": len(hub_to_chapters),
        "events_attempted_this_run": total_events,
        "skipped_by_ledger": skipped_by_ledger if resume else 0,
        "total_reified": total_reified,
        "total_skipped": total_skipped,
        "total_borderline_queued": total_borderline,
        "total_errors": total_errors,
        "hubs_reused": total_reused,
        "hubs_minted": total_minted,
        "hubs_queued_review": total_queued,
        "total_role_edges": total_role_edges,
        "role_edge_type_counts": role_edge_type_counts,
        "total_supersede_candidates": total_supersede,
        "contract10_passed": len(validation_failures) == 0,
        "contract10_failures": validation_failures[:50],  # cap for JSON size
        "total_cost_usd": round(total_cost, 6),
    }
    summary_json_path = output_dir / "plate3-full-summary.json"
    with open(summary_json_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)

    # Write human-readable summary
    summary_md_path = output_dir / "plate3-full-summary.md"
    with open(summary_md_path, "w", encoding="utf-8") as fh:
        fh.write(f"# Plate 3 Full Corpus — Summary\n\n")
        fh.write(f"**Run date:** {datetime.now().strftime('%Y-%m-%d')}\n")
        fh.write(f"**Script:** `scripts/edge-reify-backfill.py --all`\n")
        fh.write(f"**Model:** {model}\n")
        fh.write(f"**DryRun:** {dry_run}\n")
        fh.write(f"**Resume:** {resume}\n")
        if rate_limit_hit:
            fh.write(f"**STOPPED EARLY — rate limit wall hit.**\n\n")
            fh.write(f"Resume: `python3 scripts/edge-reify-backfill.py --all --resume`\n")
        fh.write(f"\n---\n\n")
        fh.write(f"## Coverage\n\n")
        fh.write(f"| Item | Count |\n|------|-------|\n")
        fh.write(f"| Chapters scanned | {chapters_scanned} |\n")
        fh.write(f"| Trigger events found | {trigger_events_found} |\n")
        fh.write(f"| Unique hub groups | {len(hub_to_chapters)} |\n")
        fh.write(f"| Skipped by ledger (--resume) | {skipped_by_ledger if resume else 0} |\n")
        fh.write(f"| Events attempted this run | {total_events} |\n\n")
        fh.write(f"## Disposition\n\n")
        fh.write(f"| Item | Count |\n|------|-------|\n")
        fh.write(f"| Reified (n-ary) | {total_reified} |\n")
        fh.write(f"| Skipped (clean dyad) | {total_skipped} |\n")
        fh.write(f"| Borderline → review queue | {total_borderline} |\n")
        fh.write(f"| Errors | {total_errors} |\n\n")
        fh.write(f"## Hub Resolution\n\n")
        fh.write(f"| Item | Count |\n|------|-------|\n")
        fh.write(f"| Hubs reused | {total_reused} |\n")
        fh.write(f"| Hubs minted | {total_minted} |\n")
        fh.write(f"| Hubs queued for review | {total_queued} |\n\n")
        fh.write(f"## Role Edges\n\n")
        fh.write(f"| Edge Type | Count |\n|-----------|-------|\n")
        for et, count in sorted(role_edge_type_counts.items()):
            fh.write(f"| {et} | {count} |\n")
        fh.write(f"| **Total** | **{total_role_edges}** |\n\n")
        fh.write(f"## Contract 10\n\n")
        if validation_failures:
            fh.write(f"**FAILED** — {len(validation_failures)} violations.\n\n")
            for vf in validation_failures[:20]:
                fh.write(f"- {vf}\n")
        else:
            fh.write(f"**ALL PASSED** — all AGENT_IN/VICTIM_IN targets resolve to event.*\n\n")
        fh.write(f"## Cost\n\n")
        fh.write(f"| Item | Value |\n|------|-------|\n")
        fh.write(f"| Total LLM cost | ${total_cost:.4f} |\n")
        fh.write(f"| Events reified | {total_reified} |\n")
        if total_reified > 0:
            fh.write(f"| Avg cost/event | ${total_cost/total_reified:.4f} |\n")
        fh.write(f"\n## Output Files\n\n")
        fh.write(f"- `{role_edges_path}`\n")
        fh.write(f"- `{skipped_dyads_path}`\n")
        fh.write(f"- `{hub_review_queue_path}`\n")
        fh.write(f"- `{supersede_candidates_path}`\n")
        fh.write(f"- `{ledger_path}`\n")
        fh.write(f"- `{output_dir / 'minted-event-nodes/'}`\n")

    print(f"  Summary: {summary_md_path}")
    print()

    if rate_limit_hit:
        sys.exit(2)


def _infer_event_type(event_title: str) -> str:
    """Heuristically infer the event node type from the event title text."""
    t = event_title.lower()
    if any(w in t for w in ("wedding", "ceremony", "coronation", "crowning", "betrothal")):
        return "event.ceremony"
    if any(w in t for w in ("battle", "siege", "sack", "assault")):
        return "event.battle"
    if any(w in t for w in ("assassination", "murder", "poison")):
        return "event.assassination"
    if any(w in t for w in ("execution", "beheading")):
        return "event.execution"
    if any(w in t for w in ("death", "dies", "killed", "kill", "slain")):
        return "event.death"
    if any(w in t for w in ("arrest", "capture", "prisoner", "hostage", "imprisoned")):
        return "event.capture"
    if any(w in t for w in ("betray", "betrayal", "conspiracy", "plot")):
        return "event.conspiracy"
    return "event.incident"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Plate 3 reification pipeline — mine Pass-1 events → role edges on event hubs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--smoke", action="store_true", help="Smoke-test mode: ONE event (Red Wedding default)")
    mode.add_argument("--batch", metavar="CONFIG_JSON", help="Batch mode: process events from JSON config file")
    mode.add_argument("--all", action="store_true", help="Full corpus mode: scan all 344 extractions")

    parser.add_argument("--event", default="red-wedding", help="Event slug for smoke mode")
    parser.add_argument("--chapters", nargs="+", help="Chapter files for smoke mode")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: working/edge-modeling/plate3-minibatch/)")
    parser.add_argument("--model", default="claude-sonnet-4-6", help="Model for claude -p calls")
    parser.add_argument("--dry-run", action="store_true", help="Skip actual claude -p calls (use deterministic stubs)")
    parser.add_argument("--concurrency", type=int, default=5, help="Max concurrent claude -p calls (default: 5)")
    parser.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Resume a previously interrupted --all run. Loads processed-events.jsonl ledger, "
            "skips completed events, deduplicates role edges against existing staging file. "
            "Safe to run after a rate-limit wall exit (exit code 2) or SIGKILL."
        ),
    )
    parser.add_argument(
        "--max-events",
        type=int,
        default=None,
        help=(
            "Cap the number of events processed in this invocation (calibration / cost-bounded "
            "chunks). Selection is deterministic (sorted by event_slug) so multiple chunked "
            "--resume runs keep making forward progress. Default: process all eligible."
        ),
    )

    args = parser.parse_args(argv)

    if args.all:
        output_dir = (
            Path(args.output_dir) if args.output_dir
            else _REPO / "working" / "edge-modeling" / "plate3-full"
        )
        run_full_corpus(
            output_dir=output_dir,
            model=args.model,
            dry_run=args.dry_run,
            concurrency=args.concurrency,
            resume=args.resume,
            max_events=args.max_events,
        )
        return

    if args.smoke:
        if args.chapters:
            chapter_files = [Path(c) if Path(c).is_absolute() else _REPO / c for c in args.chapters]
        else:
            chapter_files = [
                _REPO / "extractions/mechanical/asos/asos-catelyn-07.extraction.md",
                _REPO / "extractions/mechanical/asos/asos-epilogue.extraction.md",
            ]
        smoke_test_red_wedding(chapter_files, args.event, args.model, args.dry_run)
        return

    if args.batch:
        config_path = Path(args.batch)
        if not config_path.is_absolute():
            config_path = _REPO / args.batch
        if not config_path.exists():
            print(f"ERROR: config file not found: {config_path}", file=sys.stderr)
            sys.exit(1)

        output_dir = (
            Path(args.output_dir) if args.output_dir
            else _REPO / "working" / "edge-modeling" / "plate3-minibatch"
        )
        run_batch(
            config_path=config_path,
            output_dir=output_dir,
            model=args.model,
            dry_run=args.dry_run,
            concurrency=args.concurrency,
        )
        return


if __name__ == "__main__":
    main()
