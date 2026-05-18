#!/usr/bin/env python3
"""
Stage 4 vocab-gap analysis — normalize questions-for-matt.jsonl across the 16
distinct schemas observed and emit a per-proposed-type rollup.

Input:  working/wiki/pass2-buckets/questions-for-matt.jsonl
Output: working/agent-fleet-specs/stage4-vocab-gaps-normalized.jsonl
        working/agent-fleet-specs/stage4-vocab-gaps-rollup.md

Run from repo root.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
QUESTIONS = REPO / "working/wiki/pass2-buckets/questions-for-matt.jsonl"
NORM_OUT = REPO / "working/agent-fleet-specs/stage4-vocab-gaps-normalized.jsonl"
ROLLUP_OUT = REPO / "working/agent-fleet-specs/stage4-vocab-gaps-rollup.md"
ARCH = REPO / "reference/architecture.md"

# Field-name aliases — each row's value collapses to the first non-empty hit.
ALIAS_PROPOSED_TYPE = ("proposed_edge_type", "proposed_type")
ALIAS_PROPOSED_TYPES_LIST = ("proposed_types",)
ALIAS_QUESTION_TYPE = ("type", "kind", "question_type")
ALIAS_EVIDENCE = ("evidence_snippet", "example_snippet", "snippet", "example", "candidate_text")
ALIAS_DESCRIPTION = ("text", "description", "question", "rationale", "note")
ALIAS_BATCH = ("batch_id", "batch", "source_batch")
ALIAS_BUCKET = ("bucket_id",)
ALIAS_SECTION = ("evidence_section",)
ALIAS_SOURCE = ("source_slug",)
ALIAS_TARGET = ("target_slug",)
ALIAS_PATTERN = ("pattern",)


def pick(row: dict, keys: tuple[str, ...]) -> str | None:
    for k in keys:
        v = row.get(k)
        if v not in (None, "", []):
            return v
    return None


def normalize_proposed_type(row: dict) -> str | None:
    v = pick(row, ALIAS_PROPOSED_TYPE)
    if v:
        return v
    pl = row.get("proposed_types")
    if isinstance(pl, list) and pl:
        return "|".join(str(x) for x in pl)
    # pattern field sometimes holds the proposed type as a free-text phrase —
    # extract uppercase tokens that look like edge_type names.
    pat = pick(row, ALIAS_PATTERN)
    if pat:
        # Capture all SNAKE_CASE_UPPER tokens; join if multiple.
        tokens = re.findall(r"\b([A-Z][A-Z0-9_]{2,})\b", str(pat))
        if tokens:
            return "|".join(tokens)
        return f"_freetext:{pat}"
    # context.proposed_type fallback
    ctx = row.get("context")
    if isinstance(ctx, dict):
        v = pick(ctx, ALIAS_PROPOSED_TYPE)
        if v:
            return v
    return None


def normalize_question_type(row: dict) -> str:
    v = pick(row, ALIAS_QUESTION_TYPE)
    if v:
        return str(v)
    if pick(row, ALIAS_PATTERN) or pick(row, ALIAS_PROPOSED_TYPE):
        return "vocabulary-gap"
    return "unknown"


def normalize_evidence(row: dict) -> str | None:
    v = pick(row, ALIAS_EVIDENCE)
    if v:
        return v
    ctx = row.get("context")
    if isinstance(ctx, dict):
        return pick(ctx, ALIAS_EVIDENCE + ("snippet",))
    return None


def normalize_description(row: dict) -> str | None:
    return pick(row, ALIAS_DESCRIPTION)


def normalize_slugs(row: dict) -> tuple[str | None, str | None]:
    src = pick(row, ALIAS_SOURCE)
    tgt = pick(row, ALIAS_TARGET)
    if src and tgt:
        return src, tgt
    ctx = row.get("context")
    if isinstance(ctx, dict):
        src = src or pick(ctx, ALIAS_SOURCE) or ctx.get("source")
        tgt = tgt or pick(ctx, ALIAS_TARGET) or ctx.get("target")
    return src, tgt


def load_canonical_types() -> set[str]:
    """Mirror the validator's vocab-loader: pick out every uppercase edge_type
    that appears as a leading `| `TYPE`` cell in any `## Edge Types` subsection."""
    text = ARCH.read_text()
    # Sections are delimited by H2 ("## ") — capture the master block.
    types: set[str] = set()
    in_master = False
    for line in text.splitlines():
        if line.startswith("## Edge Types"):
            in_master = True
            continue
        if line.startswith("## ") and in_master:
            # Next ## ends the master block.
            break
        # Within Edge Types, ### sub-headings are still under master.
        if in_master:
            m = re.match(r"^\|\s*`([A-Z][A-Z0-9_]+)`", line)
            if m:
                types.add(m.group(1))
    return types


def main() -> None:
    canonical = load_canonical_types()
    rows = []
    with QUESTIONS.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows.append(row)

    # Normalize
    norm = []
    for i, row in enumerate(rows):
        qtype = normalize_question_type(row)
        ptype = normalize_proposed_type(row)
        src, tgt = normalize_slugs(row)
        # A proposed_type may be a compound like "UNCLE_OF|NEPHEW_OF" (when
        # workers proposed forward+reverse together) or "KNIGHTED_BY / BESTOWS_KNIGHTHOOD_ON"
        # — split on |, /, " or " and check if ALL parts are canonical.
        if ptype:
            parts = re.split(r"\s*[|/]\s*|\s+or\s+", ptype)
            parts = [p.strip() for p in parts if p.strip()]
            all_canonical = bool(parts) and all(p in canonical for p in parts)
        else:
            all_canonical = False
        n = {
            "row_index": i,
            "question_id": row.get("question_id"),
            "question_type": qtype,
            "proposed_type": ptype,
            "proposed_type_in_canonical": all_canonical,
            "source_slug": src,
            "target_slug": tgt,
            "evidence": normalize_evidence(row),
            "evidence_section": pick(row, ALIAS_SECTION),
            "description": normalize_description(row),
            "batch_id": pick(row, ALIAS_BATCH),
            "bucket_id": pick(row, ALIAS_BUCKET),
            "raw_keys": sorted(row.keys()),
        }
        norm.append(n)

    NORM_OUT.parent.mkdir(parents=True, exist_ok=True)
    with NORM_OUT.open("w") as f:
        for n in norm:
            f.write(json.dumps(n) + "\n")

    # Group by proposed_type
    by_type: dict[str, list[dict]] = defaultdict(list)
    untyped = []
    for n in norm:
        if n["question_type"] == "vocabulary-gap" or n["proposed_type"]:
            if n["proposed_type"]:
                by_type[n["proposed_type"]].append(n)
            else:
                untyped.append(n)

    # Rollup markdown
    lines = []
    lines.append("# Stage 4 — Vocab-Gap Rollup (2026-05-18)")
    lines.append("")
    lines.append(f"Source: `{QUESTIONS.relative_to(REPO)}` ({len(rows)} total rows)")
    lines.append("")
    lines.append(f"Normalized: `{NORM_OUT.relative_to(REPO)}`")
    lines.append("")
    lines.append("**Canonical vocab loaded from architecture.md:** "
                 f"{len(canonical)} edge types.")
    lines.append("")
    lines.append("## Distribution by question_type (normalized)")
    qt_counts: dict[str, int] = defaultdict(int)
    for n in norm:
        qt_counts[n["question_type"]] += 1
    for qt, c in sorted(qt_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- `{qt}`: {c}")
    lines.append("")

    # Already-resolved (proposed type is now in canonical vocab)
    resolved = [t for t, rs in by_type.items() if rs and rs[0]["proposed_type_in_canonical"]]
    open_gaps = [t for t in by_type.keys() if t not in resolved]

    lines.append("## Already resolved")
    lines.append("")
    lines.append("These proposed types are NOW in the canonical vocab "
                 "(architecture.md). The gap rows are stale — they were filed "
                 "before the type was added.")
    lines.append("")
    if resolved:
        for t in sorted(resolved):
            count = len(by_type[t])
            lines.append(f"- **{t}** — {count} row(s) filed before adoption")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("## Open gaps — to be decided this session")
    lines.append("")
    lines.append("Each gap below lists every example evidence we have.")
    lines.append("")
    for t in sorted(open_gaps):
        rs = by_type[t]
        lines.append(f"### `{t}` — {len(rs)} occurrence(s)")
        lines.append("")
        for r in rs:
            ev = (r.get("evidence") or "").strip().replace("\n", " ")
            if len(ev) > 240:
                ev = ev[:240] + "…"
            src = r.get("source_slug") or "?"
            tgt = r.get("target_slug") or "?"
            sec = r.get("evidence_section") or ""
            sec_note = f" [section={sec}]" if sec else ""
            batch = r.get("batch_id") or ""
            batch_note = f" [batch={batch}]" if batch else ""
            lines.append(f"- `{src}` → `{tgt}`{sec_note}{batch_note}")
            if ev:
                lines.append(f"  > {ev}")
            desc = (r.get("description") or "").strip().replace("\n", " ")
            if desc and (len(desc) < 400 and desc not in ev):
                lines.append(f"  - _description:_ {desc[:300]}")
        lines.append("")

    lines.append("## Untyped vocab-gap rows (no extractable proposed_type)")
    lines.append("")
    lines.append(f"{len(untyped)} row(s) had question_type=vocabulary-gap but no "
                 "extractable proposed_type field. These need manual inspection or "
                 "must be re-filed in canonical schema.")
    lines.append("")
    for r in untyped[:50]:
        ev = (r.get("evidence") or "").strip().replace("\n", " ")
        if len(ev) > 200:
            ev = ev[:200] + "…"
        desc = (r.get("description") or "").strip().replace("\n", " ")
        if len(desc) > 200:
            desc = desc[:200] + "…"
        src = r.get("source_slug") or "?"
        tgt = r.get("target_slug") or "?"
        lines.append(f"- row#{r['row_index']+1} `{src}` → `{tgt}`")
        if desc:
            lines.append(f"  - {desc}")
        elif ev:
            lines.append(f"  > {ev}")
    lines.append("")

    ROLLUP_OUT.parent.mkdir(parents=True, exist_ok=True)
    ROLLUP_OUT.write_text("\n".join(lines))
    print(f"Wrote {NORM_OUT.relative_to(REPO)}")
    print(f"Wrote {ROLLUP_OUT.relative_to(REPO)}")
    print(f"  {len(rows)} rows total | {len(by_type)} distinct proposed_types | "
          f"{len(resolved)} already-resolved | {len(open_gaps)} open gaps | "
          f"{len(untyped)} untyped")


if __name__ == "__main__":
    main()
