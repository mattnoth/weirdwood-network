#!/usr/bin/env python3
"""Stratified ~50-row cross-model drift audit of the Events Haiku bulk emits.

THROWAWAY single-purpose script (chain step 01-drift-audit). Do NOT generalize
into a reusable framework — future drift audits will have different prompts,
vocabs, and samplers and want their own scripts.

Method (Option B, decided in chain README):
  - Load 1,617 Haiku emits from `_events-haiku-bulk/{book}/*.edges.jsonl`.
  - Stratified sample of 50 rows (seed=531): proportional by book, ≥3 of each
    of TRAVELS_WITH / COMMANDS / TRAVELS_TO / LOCATED_AT / SERVES / REVEALS_TO.
  - Re-classify each batch via `claude -p` with cwd=~/source/claude-cwd and
    Sonnet 4.6, using the *exact* same prompt the Haiku bulk run used. Parity
    (not cost) is the reason for cwd-outside-repo + subprocess vs an Agent
    subagent — an Agent inherits
    ~28k tokens of CLAUDE.md plus tools Haiku never had, contaminating the audit.
  - Compute triple-level / pair-level / per-type agreement; surface ≥5-sample
    types under 50%.

Gates (publish in cross-model-audit.md, not enforced here):
  - Go: triple ≥70% AND pair ≥85% AND no edge type with >5 samples <50%.
  - Below those → escalate to Matt; do NOT proceed to step 2.

Cost-gate convention: `--dry-run` is the default; `--apply` is required to
actually invoke `claude -p`. Per feedback_no_extraction_without_asking.md,
get Matt's explicit go before --apply.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EMITS_DIR = REPO / "working/wiki/pass2-buckets/pass1-derived/_events-haiku-bulk"
AUDIT_DIR = REPO / "working/audits/events-haiku-bulk-2026-05-29"
BOOKS = ("agot", "acok", "asos", "affc", "adwd")
NAMED_TYPES = ("TRAVELS_WITH", "COMMANDS", "TRAVELS_TO",
               "LOCATED_AT", "SERVES", "REVEALS_TO")
MIN_PER_NAMED = 3
SAMPLE_N = 50
SAMPLE_SEED = 531
EXPECTED_PROMPT_SHA = "d31ca56c4768"
JUDGE_MODEL = "claude-sonnet-4-6"
CHAIN_STEP = "01-drift-audit"


def _load_tail_classifier():
    """Import scripts/stage4-tail-classifier.py (hyphenated filename) for
    canonical prompt-rendering and `claude -p` invocation. Using the same
    module the bulk run used guarantees prompt + invocation parity."""
    path = REPO / "scripts" / "stage4-tail-classifier.py"
    spec = importlib.util.spec_from_file_location("tail_classifier", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TC = _load_tail_classifier()


def script_sha() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:12]


def load_all_emits() -> list[dict]:
    rows: list[dict] = []
    for book in BOOKS:
        path = EMITS_DIR / book / f"{book}-tail.edges.jsonl"
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                row["_book"] = book
                rows.append(row)
    return rows


def stratified_audit_sample(rows: list[dict]) -> list[dict]:
    """Reserve MIN_PER_NAMED rows of each named type, then fill the remainder
    proportional by book. Seed=SAMPLE_SEED so the draw is reproducible.

    Different shape from stage4-tail-classifier.stratified_sample() (which
    stratifies by book+candidate_kind proportionally) — audit needs a
    min-coverage floor on specific edge types, not pure proportional stratify."""
    rng = random.Random(SAMPLE_SEED)
    by_type: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_type[r["edge_type"]].append(r)

    reserved: list[dict] = []
    reserved_ids: set[int] = set()
    for t in NAMED_TYPES:
        pool = list(by_type[t])
        rng.shuffle(pool)
        picked = pool[:MIN_PER_NAMED]
        if len(picked) < MIN_PER_NAMED:
            print(f"WARN: only {len(picked)} rows of {t} (wanted {MIN_PER_NAMED})", file=sys.stderr)
        for r in picked:
            reserved.append(r)
            reserved_ids.add(id(r))

    remainder_needed = SAMPLE_N - len(reserved)
    unreserved = [r for r in rows if id(r) not in reserved_ids]
    by_book: dict[str, list[dict]] = defaultdict(list)
    for r in unreserved:
        by_book[r["_book"]].append(r)

    total = len(unreserved)
    quotas: dict[str, int] = {}
    fracs: list[tuple[float, str]] = []
    allocated = 0
    for book in BOOKS:
        exact = remainder_needed * len(by_book[book]) / total if total else 0
        floor_val = int(exact)
        quotas[book] = floor_val
        allocated += floor_val
        fracs.append((exact - floor_val, book))
    fracs.sort(key=lambda x: -x[0])
    for i in range(remainder_needed - allocated):
        quotas[fracs[i % len(fracs)][1]] += 1

    picked: list[dict] = []
    for book in BOOKS:
        pool = list(by_book[book])
        rng.shuffle(pool)
        picked.extend(pool[: quotas[book]])

    sample = reserved + picked
    rng.shuffle(sample)
    return sample


def build_metadata(judged_count: int, judged_cost: float) -> dict:
    return {
        "_metadata": True,
        "chain_step": CHAIN_STEP,
        "script_path": "scripts/events-drift-audit.py",
        "script_sha": script_sha(),
        "judge_model": JUDGE_MODEL,
        "judge_cwd": "/Users/mnoth/source/claude-cwd",
        "expected_prompt_sha": EXPECTED_PROMPT_SHA,
        "sample_seed": SAMPLE_SEED,
        "sample_n": SAMPLE_N,
        "named_types": list(NAMED_TYPES),
        "min_per_named": MIN_PER_NAMED,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "judged_count": judged_count,
        "judged_cost_usd": round(judged_cost, 6),
    }


def chunked(rows: list[dict], size: int):
    for i in range(0, len(rows), size):
        yield rows[i : i + size]


def compute_agreement(sample: list[dict], judged: dict[int, dict]) -> dict:
    triple = pair = disagree_shape = 0
    per_type: dict[str, list[int]] = defaultdict(lambda: [0, 0])  # [agree, total]
    judged_count = 0
    for row in sample:
        idx = row["_judge_idx"]
        jd = judged.get(idx)
        if jd is None:
            continue
        judged_count += 1
        haiku_t = row["edge_type"]
        judge_t = jd.get("edge_type", "")
        per_type[haiku_t][1] += 1
        if judge_t == "REJECT":
            disagree_shape += 1
            continue
        pair += 1  # same source/target by construction (judge sees same row)
        if judge_t == haiku_t:
            triple += 1
            per_type[haiku_t][0] += 1
    return {
        "triple_agree": triple,
        "pair_agree": pair,
        "disagree_shape": disagree_shape,
        "judged": judged_count,
        "per_type": {k: tuple(v) for k, v in per_type.items()},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="Actually invoke `claude -p` (incurs cost). Default is dry-run.")
    ap.add_argument("--chunk-size", type=int, default=10,
                    help="Rows per claude -p batch (default 10).")
    args = ap.parse_args()

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading emits from {EMITS_DIR}")
    all_emits = load_all_emits()
    print(f"  Loaded {len(all_emits)} emits across {len(BOOKS)} books")

    print("Loading locked vocab (canonical via stage4-tail-classifier)…")
    locked_vocab = TC.load_locked_vocab(TC.ARCH_MD)
    gated_types = TC.DEFAULT_GATED_TYPES
    actual_sha = TC.compute_prompt_sha(locked_vocab, gated_types=gated_types)
    print(f"  Locked vocab: {len(locked_vocab)} edge types")
    print(f"  Prompt SHA: {actual_sha} (expected {EXPECTED_PROMPT_SHA})")
    if actual_sha != EXPECTED_PROMPT_SHA:
        print(f"FATAL: prompt SHA drift. Bulk run used {EXPECTED_PROMPT_SHA}; "
              f"current canonical prompt computes {actual_sha}. "
              f"STOP and ask Matt — the audit cannot run with a mismatched judge.",
              file=sys.stderr)
        return 2

    print(f"Stratified sampling (seed={SAMPLE_SEED}, n={SAMPLE_N})…")
    sample = stratified_audit_sample(all_emits)
    for i, r in enumerate(sample):
        r["_judge_idx"] = i
    book_counts = Counter(r["_book"] for r in sample)
    type_counts = Counter(r["edge_type"] for r in sample)
    print(f"  Sample size: {len(sample)}")
    print(f"  Book distribution: {dict(book_counts)}")
    named_cov = {t: type_counts[t] for t in NAMED_TYPES}
    print(f"  Named-type coverage: {named_cov}")
    long_tail = sum(c for t, c in type_counts.items() if t not in NAMED_TYPES)
    print(f"  Long-tail rows: {long_tail} across "
          f"{sum(1 for t in type_counts if t not in NAMED_TYPES)} other types")

    sample_path = AUDIT_DIR / "audit-sample-50.jsonl"
    with sample_path.open("w") as f:
        f.write(json.dumps(build_metadata(0, 0.0)) + "\n")
        for r in sample:
            f.write(json.dumps(r) + "\n")
    print(f"  Wrote {sample_path}")

    if not args.apply:
        print()
        print("DRY-RUN — did NOT invoke `claude -p`. Sample file written for review.")
        print(f"To actually judge: re-run with --apply after Matt's go.")
        print(f"Estimated spend: 50 rows × Sonnet 4.6 ≈ pennies (not the cost-gate reason).")
        return 0

    print()
    print("=" * 70)
    print(f"APPLY: invoking `claude -p` model={JUDGE_MODEL} cwd={TC.CLAUDE_P_CWD}")
    print(f"Chunk size: {args.chunk_size}; total batches: "
          f"{(len(sample) + args.chunk_size - 1) // args.chunk_size}")
    print("=" * 70)

    judged_all: dict[int, dict] = {}
    total_cost = 0.0
    for batch_idx, batch in enumerate(chunked(sample, args.chunk_size)):
        prompt = TC.render_classify_prompt(batch, locked_vocab, gated_types=gated_types)
        t0 = time.monotonic()
        print(f"  Batch {batch_idx + 1}: {len(batch)} rows…", end=" ", flush=True)
        result = TC.invoke_claude(prompt, JUDGE_MODEL)
        dt = time.monotonic() - t0
        cost = result.get("total_cost_usd", 0.0)
        total_cost += cost
        print(f"${cost:.4f}  {dt:.1f}s")
        if result["returncode"] != 0:
            print(f"    ERROR rc={result['returncode']} stderr={result.get('error_message')}",
                  file=sys.stderr)
            continue
        parsed, perr = TC.parse_batch_response(result["raw_output"], len(batch))
        if perr:
            print(f"    parse error: {perr}", file=sys.stderr)
        aligned = TC.align_batch_output(parsed, [{}] * len(batch))
        for local_idx, obj in aligned.items():
            global_idx = batch[local_idx]["_judge_idx"]
            judged_all[global_idx] = obj

    judged_path = AUDIT_DIR / "audit-sample-50-judged.jsonl"
    with judged_path.open("w") as f:
        f.write(json.dumps(build_metadata(len(judged_all), total_cost)) + "\n")
        for r in sample:
            jd = judged_all.get(r["_judge_idx"], {})
            f.write(json.dumps({
                "judge_idx": r["_judge_idx"],
                "book": r["_book"],
                "source_slug": r["source_slug"],
                "target_slug": r["target_slug"],
                "evidence_chapter": r.get("evidence_chapter"),
                "evidence_quote": r.get("evidence_quote"),
                "hint_raw": r.get("hint_raw"),
                "haiku_edge_type": r["edge_type"],
                "haiku_qualifier": r.get("qualifier"),
                "haiku_tier": r.get("confidence_tier"),
                "judge_edge_type": jd.get("edge_type"),
                "judge_qualifier": jd.get("qualifier"),
                "judge_tier": jd.get("confidence_tier"),
            }) + "\n")
    print(f"\nWrote {judged_path}")

    agree = compute_agreement(sample, judged_all)
    judged_n = max(agree["judged"], 1)
    print()
    print("AGREEMENT")
    print(f"  Judged:           {agree['judged']}/{len(sample)}")
    print(f"  Triple-level:     {agree['triple_agree']}/{agree['judged']} "
          f"= {100 * agree['triple_agree'] / judged_n:.1f}%")
    print(f"  Pair-level:       {agree['pair_agree']}/{agree['judged']} "
          f"= {100 * agree['pair_agree'] / judged_n:.1f}%")
    print(f"  Judge-rejected:   {agree['disagree_shape']} "
          f"(Haiku emitted, judge REJECT)")
    print()
    print("  Per-edge-type triple agreement:")
    for t, (a, n) in sorted(agree["per_type"].items(), key=lambda kv: -kv[1][1]):
        marker = "  <-- BELOW 50% FLOOR" if n > 5 and a / n < 0.5 else ""
        print(f"    {t:24s} {a}/{n} = {100 * a / n:.0f}%{marker}")
    print()
    print(f"Total cost: ${total_cost:.4f}")
    print()
    print("Next: write working/audits/events-haiku-bulk-2026-05-29/cross-model-audit.md")
    print("      with the table above + 5 manual-inspection rows + Go/No-Go.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
