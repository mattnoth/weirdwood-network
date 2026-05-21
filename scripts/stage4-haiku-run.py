#!/usr/bin/env python3
"""stage4-haiku-run.py — Haiku orchestrator for Stage 4 prose-edge classification.

All bookkeeping lives here. The Haiku model receives only a thin classify-only prompt
(stage4-haiku-classify.md) with an explicit (input → output) file list injected at
the %%FILE_PAIRS%% placeholder. No manifest access, no lock files, no state.jsonl,
no resume logic inside the agent — this script owns all of that.

Usage:
    # Re-classify specific Sonnet batches (by Sonnet batch ID):
    python3 scripts/stage4-haiku-run.py --batches batch-0020,batch-0021

    # Re-classify every Sonnet batch that has status: done:
    python3 scripts/stage4-haiku-run.py --all-done

    # Dry-run: print chunk plan + rendered prompt for first chunk, spend nothing:
    python3 scripts/stage4-haiku-run.py --batches batch-0020 --dry-run

    # Custom chunk size, retry count, and concurrency:
    python3 scripts/stage4-haiku-run.py --batches batch-0020 --chunk-size 5 --retries 3 --concurrency 4

    # Parallel across multiple batches:
    python3 scripts/stage4-haiku-run.py --all-done --concurrency 8

Output dirs:
    Haiku edges land in prose-edges-haiku/ beside the Sonnet prose-edges/ for easy diff.
    All mission state lives in working/missions/2026-05-19-stage4-haiku/ — never in
    the Sonnet mission dir.

Concurrency notes:
    --concurrency N runs up to N chunk-invocations in parallel using a thread pool.
    Each chunk is an independent claude -p subprocess writing its own log file and
    output files — no shared mutable state between threads. Rate-limit events are
    collected from futures and written sequentially by the main thread.
    --concurrency 1 (default) preserves exact sequential behavior.
"""

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ───────────────────────────────────────────────────────────────────

REPO = Path(__file__).resolve().parent.parent
SONNET_MISSION = REPO / "working/missions/2026-05-14-stage4-v1-bulk-sonnet"
SONNET_MANIFEST = SONNET_MISSION / "batch-manifest.jsonl"
HAIKU_MISSION = REPO / "working/missions/2026-05-19-stage4-haiku"
HAIKU_RESULTS = HAIKU_MISSION / "results"
HAIKU_RUN_LOGS = HAIKU_MISSION / "run-logs"
HAIKU_PROMPTS_USED = HAIKU_MISSION / "prompts-used"
HAIKU_SONNET_CONTROL = HAIKU_PROMPTS_USED / "sonnet-control"
CLASSIFY_TEMPLATE = REPO / ".claude/commands/stage4-haiku-classify.md"
CLASSIFIER_MANUAL = REPO / ".claude/agents/prose-edge-classifier.md"
LOCKED_VOCAB = HAIKU_MISSION / "locked-edge-vocab-159.md"
SONNET_WORKER = REPO / ".claude/commands/worker-stage4.md"
BUCKETS = REPO / "working/wiki/pass2-buckets"
RATE_LIMIT_LOG = HAIKU_MISSION / "rate-limit-events.jsonl"


# ── Output path computation ──────────────────────────────────────────────────

def candidate_to_haiku_output(candidate_path: str) -> Path:
    """Map a candidate file path to its Haiku output path.

    Mirrors worker-stage4.md's per-shape path table but replaces
    prose-edges/ with prose-edges-haiku/ so Haiku output sits beside
    Sonnet output for easy folder-vs-folder comparison.

    Path patterns:
        source_target:
            working/wiki/pass2-buckets/<bucket>/prose-edge-candidates/<slug>.candidates.jsonl
            → working/wiki/pass2-buckets/<bucket>/prose-edges-haiku/<slug>.edges.jsonl

        comention:
            working/wiki/pass2-buckets/meta-chapters-<book>/comention-candidates/<chapter>.candidates.jsonl
            → working/wiki/pass2-buckets/meta-chapters-<book>/prose-edges-haiku/<chapter>.comention-edges.jsonl

        pass1_relationship:
            working/wiki/pass2-buckets/extractions-pass1/<book>/<chapter>.candidates.jsonl
            → working/wiki/pass2-buckets/extractions-pass1/<book>/prose-edges-haiku/<chapter>.pass1-edges.jsonl

    We distinguish the three shapes by path structure:
        comention       — bucket starts with "meta-chapters-"
        pass1_rel       — bucket is "extractions-pass1"
        source_target   — everything else
    """
    parts = Path(candidate_path).parts
    # parts: ('working', 'wiki', 'pass2-buckets', <bucket>, <subdir>, <file>)
    if len(parts) < 6:
        raise ValueError(f"Unexpected candidate path structure: {candidate_path!r}")

    bucket = parts[3]
    slug = parts[5].removesuffix(".candidates.jsonl")

    if bucket.startswith("meta-chapters-"):
        # comention shape
        output_file = f"{slug}.comention-edges.jsonl"
        out_path = REPO / "working/wiki/pass2-buckets" / bucket / "prose-edges-haiku" / output_file
    elif bucket == "extractions-pass1":
        # pass1_relationship shape — parts[4] is the book dir
        book = parts[4]
        output_file = f"{slug}.pass1-edges.jsonl"
        out_path = REPO / "working/wiki/pass2-buckets" / bucket / book / "prose-edges-haiku" / output_file
    else:
        # source_target shape
        output_file = f"{slug}.edges.jsonl"
        out_path = REPO / "working/wiki/pass2-buckets" / bucket / "prose-edges-haiku" / output_file

    return out_path


# ── Manifest loading (read-only) ─────────────────────────────────────────────

def load_sonnet_manifest() -> list[dict]:
    """Load the Sonnet batch manifest as a list of dicts. READ-ONLY."""
    if not SONNET_MANIFEST.exists():
        sys.exit(f"ERROR: Sonnet manifest not found: {SONNET_MANIFEST}")
    rows = []
    for line in SONNET_MANIFEST.read_text().splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


# ── Provenance snapshot ───────────────────────────────────────────────────────

def git_hash(path: Path) -> str:
    """Return the current git blob hash for a file, or 'untracked' if not committed."""
    result = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "--error-unmatch", str(path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return "untracked"
    result2 = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", f"HEAD:{path.relative_to(REPO)}"],
        capture_output=True, text=True
    )
    return result2.stdout.strip() or "unknown"


def git_log_window(path: Path, after: str, before: str) -> list[dict]:
    """Return git commits touching `path` between `after` and `before` dates."""
    result = subprocess.run(
        [
            "git", "-C", str(REPO), "log",
            f"--after={after}", f"--before={before}",
            "--format=%H %ai %s",
            "--", str(path.relative_to(REPO)),
        ],
        capture_output=True, text=True
    )
    commits = []
    for line in result.stdout.strip().splitlines():
        if line.strip():
            parts = line.split(" ", 3)
            commits.append({"hash": parts[0], "date": parts[1], "subject": parts[3] if len(parts) > 3 else ""})
    return commits


def git_show_file(commit_hash: str, repo_relative_path: Path, dest: Path) -> bool:
    """Extract a file at a specific commit and write it to dest. Returns True on success."""
    result = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{commit_hash}:{repo_relative_path}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(result.stdout)
    return True


def record_provenance(model: str, dry_run: bool) -> dict:
    """Snapshot prompt provenance for this run. Writes files to prompts-used/."""
    HAIKU_PROMPTS_USED.mkdir(parents=True, exist_ok=True)
    HAIKU_SONNET_CONTROL.mkdir(parents=True, exist_ok=True)

    now_iso = datetime.now(timezone.utc).isoformat()

    # ── Current prompts (what Haiku will actually use) ────────────────────────
    classifier_hash = git_hash(CLASSIFIER_MANUAL)
    classify_cmd_hash = git_hash(CLASSIFY_TEMPLATE)

    # Copy current versions
    if not dry_run:
        (HAIKU_PROMPTS_USED / CLASSIFIER_MANUAL.name).write_text(CLASSIFIER_MANUAL.read_text())
        (HAIKU_PROMPTS_USED / CLASSIFY_TEMPLATE.name).write_text(CLASSIFY_TEMPLATE.read_text())

    # ── Sonnet-era prompts (from before Sonnet run, 2026-05-14) ───────────────
    # The Sonnet run window was 2026-05-14 to 2026-05-16. The most recent commit
    # touching each file before that window is the "Sonnet control" version.
    # We recover it with git log --before=2026-05-14 and git show.
    sonnet_classifier_commits = []
    sonnet_worker_commits = []

    for path, commits_list in [
        (CLASSIFIER_MANUAL, sonnet_classifier_commits),
        (SONNET_WORKER, sonnet_worker_commits),
    ]:
        result = subprocess.run(
            [
                "git", "-C", str(REPO), "log",
                "--before=2026-05-14",
                "--format=%H %ai %s",
                "-1",  # most recent commit before the Sonnet run
                "--", str(path.relative_to(REPO)),
            ],
            capture_output=True, text=True
        )
        for line in result.stdout.strip().splitlines():
            if line.strip():
                parts = line.split(" ", 3)
                commits_list.append({
                    "hash": parts[0],
                    "date": parts[1] if len(parts) > 1 else "",
                    "subject": parts[3] if len(parts) > 3 else "",
                })

    # Extract Sonnet-era versions into prompts-used/sonnet-control/
    sonnet_classifier_hash = "none"
    sonnet_worker_hash = "none"

    if sonnet_classifier_commits and not dry_run:
        commit = sonnet_classifier_commits[0]["hash"]
        dest = HAIKU_SONNET_CONTROL / CLASSIFIER_MANUAL.name
        success = git_show_file(commit, CLASSIFIER_MANUAL.relative_to(REPO), dest)
        sonnet_classifier_hash = commit if success else "extraction-failed"
    elif sonnet_classifier_commits:
        sonnet_classifier_hash = sonnet_classifier_commits[0]["hash"]

    if sonnet_worker_commits and not dry_run:
        commit = sonnet_worker_commits[0]["hash"]
        dest = HAIKU_SONNET_CONTROL / SONNET_WORKER.name
        success = git_show_file(commit, SONNET_WORKER.relative_to(REPO), dest)
        sonnet_worker_hash = commit if success else "extraction-failed"
    elif sonnet_worker_commits:
        sonnet_worker_hash = sonnet_worker_commits[0]["hash"]

    provenance = {
        "recorded_at": now_iso,
        "dry_run": dry_run,
        "haiku_model": model,
        "haiku_prompts": {
            "classifier_manual": str(CLASSIFIER_MANUAL.relative_to(REPO)),
            "classifier_manual_git_hash": classifier_hash,
            "classify_command": str(CLASSIFY_TEMPLATE.relative_to(REPO)),
            "classify_command_git_hash": classify_cmd_hash,
        },
        "sonnet_control_prompts": {
            "classifier_manual": str(CLASSIFIER_MANUAL.relative_to(REPO)),
            "classifier_manual_git_hash": sonnet_classifier_hash,
            "worker_command": str(SONNET_WORKER.relative_to(REPO)),
            "worker_command_git_hash": sonnet_worker_hash,
            "note": "Versions in effect at the start of the 2026-05-14 Sonnet run "
                    "(last commit before 2026-05-14 per git log --before=2026-05-14)",
        },
    }

    if not dry_run:
        prov_path = HAIKU_PROMPTS_USED / "provenance.json"
        prov_path.write_text(json.dumps(provenance, indent=2) + "\n")
        print(f"  Provenance written: {prov_path.relative_to(REPO)}")
        if sonnet_classifier_hash not in ("none", "extraction-failed"):
            print(f"  Sonnet-era classifier: commit {sonnet_classifier_hash[:8]}")
        if sonnet_worker_hash not in ("none", "extraction-failed"):
            print(f"  Sonnet-era worker: commit {sonnet_worker_hash[:8]}")
    else:
        print(f"  [dry-run] Would write provenance.json")
        print(f"  Current classifier git hash: {classifier_hash}")
        print(f"  Current classify-cmd git hash: {classify_cmd_hash}")
        if sonnet_classifier_commits:
            print(f"  Sonnet-era classifier commit: {sonnet_classifier_commits[0]['hash'][:8]} "
                  f"({sonnet_classifier_commits[0].get('date', '')})")
        else:
            print(f"  Sonnet-era classifier: no git history before 2026-05-14")
        if sonnet_worker_commits:
            print(f"  Sonnet-era worker commit: {sonnet_worker_commits[0]['hash'][:8]} "
                  f"({sonnet_worker_commits[0].get('date', '')})")
        else:
            print(f"  Sonnet-era worker: no git history before 2026-05-14")

    return provenance


# ── Prompt rendering ──────────────────────────────────────────────────────────

def load_locked_vocab() -> str:
    """Return the 164-edge-type vocabulary body for inlining into the classify prompt.

    Source of truth is locked-edge-vocab-159.md (itself regenerated from
    architecture.md via `stage4-haiku-normalize-edge-types.py --dump-vocab`).
    Injecting it at render time keeps a single source — the prompt never holds
    a hand-maintained copy that can drift. We strip the file's admin header
    (everything up to and including the first horizontal rule) so only the
    entry list + footer land in the prompt.
    """
    if not LOCKED_VOCAB.exists():
        sys.exit(
            f"ERROR: locked vocab file not found: {LOCKED_VOCAB}\n"
            "Regenerate it: python3 scripts/stage4-haiku-normalize-edge-types.py "
            f"--dump-vocab {LOCKED_VOCAB}"
        )
    text = LOCKED_VOCAB.read_text()
    # Drop the auto-generated admin header — keep entries onward.
    body = text.split("\n---\n", 1)[-1].strip()
    return body


def render_prompt(chunk_pairs: list[tuple[str, Path]]) -> str:
    """Render the classify prompt template with the chunk's file pairs and the
    locked 164-edge-type vocabulary injected at their placeholders."""
    template = CLASSIFY_TEMPLATE.read_text()
    pairs_block = "\n".join(
        f"{cand_path} -> {str(out_path.relative_to(REPO))}"
        for cand_path, out_path in chunk_pairs
    )
    if "%%FILE_PAIRS%%" not in template:
        sys.exit("ERROR: classify template missing %%FILE_PAIRS%% placeholder")
    if "%%LOCKED_VOCAB%%" not in template:
        sys.exit("ERROR: classify template missing %%LOCKED_VOCAB%% placeholder")
    template = template.replace("%%LOCKED_VOCAB%%", load_locked_vocab())
    return template.replace("%%FILE_PAIRS%%", pairs_block)


# ── Output verification ───────────────────────────────────────────────────────

def verify_outputs(chunk_pairs: list[tuple[str, Path]]) -> tuple[list[Path], list[Path]]:
    """Return (ok_paths, missing_or_empty_paths) after a claude invocation."""
    ok, bad = [], []
    for _, out_path in chunk_pairs:
        if not out_path.exists() or out_path.stat().st_size == 0:
            bad.append(out_path)
            continue
        # Check valid JSONL
        try:
            for line in out_path.read_text().strip().splitlines():
                if line.strip():
                    json.loads(line)
            ok.append(out_path)
        except json.JSONDecodeError:
            bad.append(out_path)
    return ok, bad


# ── Rate-limit detection ──────────────────────────────────────────────────────

def detect_rate_limit(log_path: Path) -> dict | None:
    """Scan a stream-json log file for a rate-limit rejection event.

    Mirrors the detection logic in stage4.sh (lines 401-428): looks for
    type=rate_limit_event with rate_limit_info.status == "rejected".

    Returns a dict with keys {rate_limit_type, resets_at_ts, reset_info}
    if a rate-limit event is found, otherwise None.
    """
    if not log_path.exists():
        return None

    try:
        for raw_line in log_path.read_text().splitlines():
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            if event.get("type") != "rate_limit_event":
                continue

            info = event.get("rate_limit_info", {})
            if info.get("status") != "rejected":
                continue

            resets_at_ts = info.get("resetsAt", 0)
            rate_limit_type = info.get("rateLimitType", "unknown")

            reset_info = f"{rate_limit_type} limit hit"
            if resets_at_ts and resets_at_ts > 0:
                try:
                    reset_dt = datetime.fromtimestamp(resets_at_ts, tz=timezone.utc)
                    reset_info = (
                        f"{rate_limit_type} limit — resets at "
                        f"{reset_dt.strftime('%Y-%m-%d %H:%M UTC')}"
                    )
                except (OSError, ValueError, OverflowError):
                    pass

            return {
                "rate_limit_type": rate_limit_type,
                "resets_at_ts": resets_at_ts,
                "reset_info": reset_info,
            }
    except OSError:
        pass

    return None


# ── Claude invocation ─────────────────────────────────────────────────────────

def invoke_haiku(prompt: str, model: str, log_path: Path) -> dict:
    """Call claude with the rendered prompt. Stream output to log_path.

    Returns a dict with keys: returncode, total_cost_usd, error_message,
    duration_s, rate_limit_info (None or dict from detect_rate_limit).
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "claude",
        "-p",
        "--dangerously-skip-permissions",
        "--model", model,
        "--verbose",
        "--output-format", "stream-json",
        prompt,
    ]

    total_cost_usd = 0.0
    error_message = None
    t_start = time.monotonic()

    with open(log_path, "w") as log_fh:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for line in proc.stdout:
            log_fh.write(line)
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("type") == "result":
                    total_cost_usd = event.get("total_cost_usd", 0.0)
            except json.JSONDecodeError:
                pass

        _stderr = proc.stderr.read()
        proc.wait()

        if proc.returncode != 0:
            error_message = _stderr.strip()[:500] if _stderr.strip() else f"exit code {proc.returncode}"

    duration_s = time.monotonic() - t_start

    # Detect rate-limit in the log we just wrote
    rate_limit_info = detect_rate_limit(log_path)

    return {
        "returncode": proc.returncode,
        "total_cost_usd": total_cost_usd,
        "error_message": error_message,
        "duration_s": round(duration_s, 2),
        "rate_limit_info": rate_limit_info,
    }


# ── Decision counting ─────────────────────────────────────────────────────────

def count_decisions(out_paths: list[Path]) -> dict:
    """Count decision types across a list of output JSONL files."""
    totals: dict[str, int] = {}
    for p in out_paths:
        if not p.exists():
            continue
        for line in p.read_text().strip().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                decision = row.get("decision", "unknown")
                totals[decision] = totals.get(decision, 0) + 1
            except json.JSONDecodeError:
                pass
    return totals


# ── Chunk runner (called from thread pool or directly) ───────────────────────

def run_chunk(
    chunk_id: str,
    batch_id: str,
    chunk: list[tuple[str, Path]],
    chunk_idx: int,
    total_chunks: int,
    model: str,
    retries: int,
) -> dict:
    """Process a single chunk: invoke Haiku, retry on missing outputs.

    Safe to call from multiple threads — writes only to its own log path
    and the output files determined by candidate_to_haiku_output (each
    file is unique to its chunk).

    Returns a dict with:
        chunk_id, batch_id, chunk_idx, files_done (list[str]),
        files_failed (list[str]), ok_paths (list[Path]),
        total_cost_usd, duration_s, rate_limit_event (None or dict).
    """
    prompt = render_prompt(chunk)
    log_path = HAIKU_RUN_LOGS / f"{batch_id}-chunk-{chunk_idx:02d}.jsonl"

    files_done: list[str] = []
    all_ok_paths: list[Path] = []
    total_cost = 0.0
    total_duration = 0.0
    rate_limit_event: dict | None = None

    attempt = 0
    remaining = chunk[:]

    while attempt <= retries and remaining:
        if attempt > 0:
            print(f"  [{chunk_id}] Retry {attempt}/{retries} for {len(remaining)} missing files...")

        if attempt > 0:
            # Re-render with only missing pairs
            prompt = render_prompt(remaining)
            log_path = HAIKU_RUN_LOGS / f"{batch_id}-chunk-{chunk_idx:02d}-retry{attempt}.jsonl"

        result = invoke_haiku(prompt, model, log_path)
        total_cost += result.get("total_cost_usd", 0.0)
        total_duration += result.get("duration_s", 0.0)

        # Capture rate-limit event from this attempt (first one wins)
        if rate_limit_event is None and result.get("rate_limit_info"):
            rate_limit_event = result["rate_limit_info"]

        if result["returncode"] != 0:
            print(f"  [{chunk_id}] WARNING: claude exited non-zero: {result['error_message']}")

        # If rate-limited, stop retrying this chunk immediately
        if rate_limit_event is not None:
            print(f"  [{chunk_id}] RATE LIMIT detected — {rate_limit_event['reset_info']} — stopping retries")
            break

        # Verify outputs
        ok, bad = verify_outputs(remaining)
        all_ok_paths.extend(ok)
        files_done.extend(str(p) for p in ok)

        if not bad:
            break

        remaining = [(c, p) for c, p in remaining if p in bad]
        attempt += 1

    # If rate-limited, none of the remaining files are done
    if rate_limit_event is not None:
        files_failed = [str(p) for _, p in remaining]
    else:
        files_failed = [str(p) for _, p in remaining
                        if p not in all_ok_paths]

    return {
        "chunk_id": chunk_id,
        "batch_id": batch_id,
        "chunk_idx": chunk_idx,
        "files_done": files_done,
        "files_failed": files_failed,
        "ok_paths": all_ok_paths,
        "total_cost_usd": round(total_cost, 6),
        "duration_s": round(total_duration, 2),
        "rate_limit_event": rate_limit_event,
    }


# ── Batch planning ────────────────────────────────────────────────────────────

def plan_batch_chunks(
    batch_row: dict,
    chunk_size: int,
    skip_if_output_exists: bool = False,
) -> tuple[list[list[tuple[str, Path]]], list[str]]:
    """Compute (chunks, warning_messages) for a batch without running anything.

    When skip_if_output_exists=True, files whose output .edges.jsonl already
    exists (non-empty) are filtered out — used by the loop's rate-limit
    re-run path to avoid re-processing files already done in an earlier
    partial attempt of the same batch.
    """
    files = batch_row["files"]
    all_pairs: list[tuple[str, Path]] = []
    warnings: list[str] = []

    skipped_count = 0
    for f in files:
        try:
            out = candidate_to_haiku_output(f)
        except ValueError as e:
            warnings.append(f"WARNING: skipping unroutable path: {e}")
            continue
        if skip_if_output_exists and out.exists() and out.stat().st_size > 0:
            skipped_count += 1
            continue
        all_pairs.append((f, out))

    if skipped_count > 0:
        warnings.append(
            f"INFO: skipped {skipped_count} file(s) whose output already exists"
        )

    chunks: list[list[tuple[str, Path]]] = []
    for i in range(0, len(all_pairs), chunk_size):
        chunks.append(all_pairs[i : i + chunk_size])

    return chunks, warnings


# ── Batch runner ──────────────────────────────────────────────────────────────

def run_batch(
    batch_row: dict,
    chunk_size: int,
    retries: int,
    model: str,
    dry_run: bool,
    concurrency: int = 1,
    skip_if_output_exists: bool = False,
) -> dict:
    """Process one batch: chunk its files, invoke Haiku per chunk, verify outputs.

    When concurrency > 1, chunks within this batch are submitted to the caller's
    thread pool. For sequential use (called directly), chunks run one by one.

    Returns a results dict suitable for writing to results/<batch_id>.json.
    Callers using a thread pool should use run_batch_sequential or submit chunks
    directly via submit_batch_chunks.
    """
    batch_id = batch_row["batch_id"]
    shape = batch_row.get("shape", "unknown")

    print(f"\n=== Batch {batch_id} ({len(batch_row['files'])} files, shape={shape}) ===")

    chunks, warnings = plan_batch_chunks(batch_row, chunk_size, skip_if_output_exists)
    for w in warnings:
        print(f"  {w}")

    total_pairs = sum(len(c) for c in chunks)
    print(f"  {total_pairs} pairs -> {len(chunks)} chunks of <=>{chunk_size}")

    if dry_run:
        print(f"\n  [dry-run] Chunk plan:")
        for i, chunk in enumerate(chunks):
            print(f"    Chunk {i:02d} ({len(chunk)} files):")
            for cand, out in chunk:
                print(f"      {Path(cand).name}")
                print(f"        -> {out.relative_to(REPO)}")
        if chunks:
            print(f"\n  [dry-run] Rendered prompt for chunk 0:")
            print("  " + "-" * 70)
            rendered = render_prompt(chunks[0])
            for line in rendered.splitlines():
                print(f"  {line}")
            print("  " + "-" * 70)
        return {
            "batch_id": batch_id,
            "dry_run": True,
            "files_planned": total_pairs,
            "chunks_planned": len(chunks),
            "chunk_size": chunk_size,
        }

    # Live run — sequential (used when the caller doesn't manage a pool)
    started_at = datetime.now(timezone.utc).isoformat()
    files_done: list[str] = []
    files_failed: list[str] = []
    total_cost = 0.0
    all_ok_paths: list[Path] = []
    chunk_timings: list[dict] = []
    rate_limit_events: list[dict] = []
    classifier_hash = git_hash(CLASSIFIER_MANUAL)

    for chunk_idx, chunk in enumerate(chunks):
        chunk_id = f"{batch_id}-chunk-{chunk_idx:02d}"
        print(f"  Chunk {chunk_idx:02d}/{len(chunks)-1} ({len(chunk)} files)...")

        chunk_result = run_chunk(
            chunk_id=chunk_id,
            batch_id=batch_id,
            chunk=chunk,
            chunk_idx=chunk_idx,
            total_chunks=len(chunks),
            model=model,
            retries=retries,
        )

        total_cost += chunk_result["total_cost_usd"]
        all_ok_paths.extend(chunk_result["ok_paths"])
        files_done.extend(chunk_result["files_done"])
        files_failed.extend(chunk_result["files_failed"])
        chunk_timings.append({
            "chunk_id": chunk_id,
            "chunk_idx": chunk_idx,
            "duration_s": chunk_result["duration_s"],
            "cost_usd": chunk_result["total_cost_usd"],
            "files_done": len(chunk_result["files_done"]),
            "files_failed": len(chunk_result["files_failed"]),
            "rate_limited": chunk_result["rate_limit_event"] is not None,
        })

        if chunk_result["rate_limit_event"]:
            rate_limit_events.append({
                "chunk_id": chunk_id,
                "batch_id": batch_id,
                **chunk_result["rate_limit_event"],
            })

    return _assemble_batch_result(
        batch_id=batch_id,
        shape=shape,
        started_at=started_at,
        all_pairs_count=total_pairs,
        files_done=files_done,
        files_failed=files_failed,
        all_ok_paths=all_ok_paths,
        total_cost=total_cost,
        chunk_timings=chunk_timings,
        rate_limit_events=rate_limit_events,
        classifier_hash=classifier_hash,
        chunks_run=len(chunks),
    )


def _assemble_batch_result(
    batch_id: str,
    shape: str,
    started_at: str,
    all_pairs_count: int,
    files_done: list[str],
    files_failed: list[str],
    all_ok_paths: list[Path],
    total_cost: float,
    chunk_timings: list[dict],
    rate_limit_events: list[dict],
    classifier_hash: str,
    chunks_run: int,
) -> dict:
    """Assemble and write a per-batch result file."""
    decision_totals = count_decisions(all_ok_paths)
    completed_at = datetime.now(timezone.utc).isoformat()

    batch_result = {
        "batch_id": batch_id,
        "shape": shape,
        "started_at": started_at,
        "completed_at": completed_at,
        "files_attempted": all_pairs_count,
        "files_done": len(files_done),
        "files_failed": len(files_failed),
        "failed_outputs": files_failed,
        "decision_totals": decision_totals,
        "total_cost_usd": round(total_cost, 6),
        "classifier_prompt_git_hash": classifier_hash,
        "chunks_run": chunks_run,
        "chunk_timings": chunk_timings,
        "rate_limit_events_count": len(rate_limit_events),
    }

    HAIKU_RESULTS.mkdir(parents=True, exist_ok=True)
    result_path = HAIKU_RESULTS / f"{batch_id}.json"
    result_path.write_text(json.dumps(batch_result, indent=2) + "\n")
    print(f"  Results written: {result_path.relative_to(REPO)}")
    print(f"  Done: {len(files_done)}/{all_pairs_count} files | "
          f"Decisions: {decision_totals} | Cost: ${total_cost:.4f}")

    return batch_result


# ── Parallel chunk dispatcher ─────────────────────────────────────────────────

def run_all_parallel(
    target_rows: list[dict],
    chunk_size: int,
    retries: int,
    model: str,
    concurrency: int,
    skip_if_output_exists: bool = False,
) -> tuple[list[dict], list[dict]]:
    """Run all chunks from all batches in a shared thread pool.

    Returns (batch_results, all_rate_limit_events).

    Concurrency is across chunks globally — chunks from different batches
    fill the same pool, keeping N workers busy at once.

    Each chunk writes its own log file and output files; no shared state
    is mutated by worker threads. Rate-limit events are collected from
    futures by the main thread after each future completes.
    """
    classifier_hash = git_hash(CLASSIFIER_MANUAL)

    # Build a flat list of all chunk work items with batch metadata
    work_items: list[dict] = []  # {batch_id, shape, chunk_idx, chunk, batch_pairs_total}
    batch_meta: dict[str, dict] = {}  # batch_id -> {shape, pairs_total, started_at, chunks}

    for batch_row in target_rows:
        batch_id = batch_row["batch_id"]
        shape = batch_row.get("shape", "unknown")
        chunks, warnings = plan_batch_chunks(batch_row, chunk_size, skip_if_output_exists)

        for w in warnings:
            print(f"  [{batch_id}] {w}")

        total_pairs = sum(len(c) for c in chunks)
        print(f"\n=== Batch {batch_id} ({len(batch_row['files'])} files, shape={shape}) ===")
        print(f"  {total_pairs} pairs -> {len(chunks)} chunks of <={chunk_size}")

        batch_meta[batch_id] = {
            "shape": shape,
            "pairs_total": total_pairs,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "chunks": chunks,
        }

        for chunk_idx, chunk in enumerate(chunks):
            work_items.append({
                "batch_id": batch_id,
                "chunk_idx": chunk_idx,
                "total_chunks": len(chunks),
                "chunk": chunk,
            })

    total_chunks = len(work_items)
    print(f"\nDispatching {total_chunks} chunks across {concurrency} workers...")

    # Accumulate results per batch
    batch_accum: dict[str, dict] = {
        batch_id: {
            "files_done": [],
            "files_failed": [],
            "ok_paths": [],
            "total_cost": 0.0,
            "chunk_timings": [],
            "rate_limit_events": [],
        }
        for batch_id in batch_meta
    }

    all_rate_limit_events: list[dict] = []
    completed_count = 0

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        future_to_item = {
            pool.submit(
                run_chunk,
                chunk_id=f"{item['batch_id']}-chunk-{item['chunk_idx']:02d}",
                batch_id=item["batch_id"],
                chunk=item["chunk"],
                chunk_idx=item["chunk_idx"],
                total_chunks=item["total_chunks"],
                model=model,
                retries=retries,
            ): item
            for item in work_items
        }

        for future in as_completed(future_to_item):
            item = future_to_item[future]
            batch_id = item["batch_id"]
            chunk_idx = item["chunk_idx"]
            completed_count += 1

            try:
                chunk_result = future.result()
            except Exception as exc:
                chunk_id = f"{batch_id}-chunk-{chunk_idx:02d}"
                print(f"  [{chunk_id}] EXCEPTION: {exc}")
                # Mark all files in this chunk as failed
                chunk = item["chunk"]
                batch_accum[batch_id]["files_failed"].extend(str(p) for _, p in chunk)
                batch_accum[batch_id]["chunk_timings"].append({
                    "chunk_id": chunk_id,
                    "chunk_idx": chunk_idx,
                    "duration_s": 0.0,
                    "cost_usd": 0.0,
                    "files_done": 0,
                    "files_failed": len(chunk),
                    "rate_limited": False,
                    "exception": str(exc),
                })
                continue

            chunk_id = chunk_result["chunk_id"]
            accum = batch_accum[batch_id]
            accum["total_cost"] += chunk_result["total_cost_usd"]
            accum["ok_paths"].extend(chunk_result["ok_paths"])
            accum["files_done"].extend(chunk_result["files_done"])
            accum["files_failed"].extend(chunk_result["files_failed"])
            accum["chunk_timings"].append({
                "chunk_id": chunk_id,
                "chunk_idx": chunk_idx,
                "duration_s": chunk_result["duration_s"],
                "cost_usd": chunk_result["total_cost_usd"],
                "files_done": len(chunk_result["files_done"]),
                "files_failed": len(chunk_result["files_failed"]),
                "rate_limited": chunk_result["rate_limit_event"] is not None,
            })

            if chunk_result["rate_limit_event"]:
                rl = chunk_result["rate_limit_event"]
                rl_entry = {
                    "chunk_id": chunk_id,
                    "batch_id": batch_id,
                    "detected_at": datetime.now(timezone.utc).isoformat(),
                    **rl,
                }
                accum["rate_limit_events"].append(rl_entry)
                all_rate_limit_events.append(rl_entry)
                print(f"  [{chunk_id}] RATE LIMIT: {rl['reset_info']}")

            print(f"  [{chunk_id}] complete ({completed_count}/{total_chunks}) "
                  f"| cost ${chunk_result['total_cost_usd']:.4f} "
                  f"| {len(chunk_result['files_done'])} ok "
                  f"| {chunk_result['duration_s']:.1f}s")

    # Write rate-limit events log (sequentially, from main thread)
    if all_rate_limit_events:
        HAIKU_MISSION.mkdir(parents=True, exist_ok=True)
        with open(RATE_LIMIT_LOG, "a") as fh:
            for entry in all_rate_limit_events:
                fh.write(json.dumps(entry) + "\n")
        print(f"\nRate-limit events written: {RATE_LIMIT_LOG.relative_to(REPO)} "
              f"({len(all_rate_limit_events)} events)")

    # Assemble per-batch result files
    batch_results: list[dict] = []
    for batch_id, meta in batch_meta.items():
        accum = batch_accum[batch_id]
        result = _assemble_batch_result(
            batch_id=batch_id,
            shape=meta["shape"],
            started_at=meta["started_at"],
            all_pairs_count=meta["pairs_total"],
            files_done=accum["files_done"],
            files_failed=accum["files_failed"],
            all_ok_paths=accum["ok_paths"],
            total_cost=accum["total_cost"],
            chunk_timings=sorted(accum["chunk_timings"], key=lambda x: x["chunk_idx"]),
            rate_limit_events=accum["rate_limit_events"],
            classifier_hash=classifier_hash,
            chunks_run=len(meta["chunks"]),
        )
        batch_results.append(result)

    return batch_results, all_rate_limit_events


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Haiku orchestrator for Stage 4 prose-edge classification.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--batches",
        metavar="BATCH_IDS",
        help="Comma-separated Sonnet batch IDs to re-classify (e.g. batch-0020,batch-0021)",
    )
    group.add_argument(
        "--all-done",
        action="store_true",
        help="Re-classify every batch in the Sonnet manifest with status: done",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=3,
        metavar="N",
        help="Files per Haiku invocation (default: 3)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        metavar="N",
        help="Retry attempts for missing outputs after each chunk (default: 2)",
    )
    parser.add_argument(
        "--model",
        default="claude-haiku-4-5",
        metavar="MODEL",
        help="Model to invoke (default: claude-haiku-4-5)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        metavar="N",
        help=(
            "Number of chunk-invocations to run in parallel (default: 1 = sequential). "
            "When N>1, a ThreadPoolExecutor drives independent claude -p subprocesses. "
            "Each chunk writes its own log and output files — no shared state."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print chunk plan + rendered prompt for first chunk; invoke nothing",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help=(
            "Filter out files whose output .edges.jsonl already exists (non-empty) "
            "before chunking. Used by the loop's rate-limit re-run path to avoid "
            "re-processing files already done in an earlier partial attempt of "
            "the same batch."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.concurrency < 1:
        sys.exit("ERROR: --concurrency must be >= 1")

    # ── Setup mission dir ─────────────────────────────────────────────────────
    for d in [HAIKU_MISSION, HAIKU_RESULTS, HAIKU_RUN_LOGS, HAIKU_PROMPTS_USED, HAIKU_SONNET_CONTROL]:
        d.mkdir(parents=True, exist_ok=True)

    print(f"Weirwood Network — Stage 4 Haiku Orchestrator")
    print(f"  Model: {args.model}")
    print(f"  Chunk size: {args.chunk_size}")
    print(f"  Concurrency: {args.concurrency} ({'sequential' if args.concurrency == 1 else 'parallel'})")
    print(f"  Retries: {args.retries}")
    print(f"  Dry-run: {args.dry_run}")
    print(f"  Sonnet manifest: {SONNET_MANIFEST.relative_to(REPO)}")
    print(f"  Haiku mission dir: {HAIKU_MISSION.relative_to(REPO)}")
    print()

    # ── Provenance snapshot (once per run) ───────────────────────────────────
    print("Recording provenance...")
    record_provenance(model=args.model, dry_run=args.dry_run)
    print()

    # ── Load Sonnet manifest (read-only) ─────────────────────────────────────
    manifest_rows = load_sonnet_manifest()
    manifest_by_id = {r["batch_id"]: r for r in manifest_rows}
    print(f"Sonnet manifest: {len(manifest_rows)} rows, "
          f"{sum(1 for r in manifest_rows if r.get('status') == 'done')} done")

    # ── Determine target batches ──────────────────────────────────────────────
    if args.all_done:
        target_rows = [r for r in manifest_rows if r.get("status") == "done"]
        print(f"Mode: --all-done -> {len(target_rows)} batches selected")
    else:
        requested_ids = [b.strip() for b in args.batches.split(",") if b.strip()]
        target_rows = []
        for bid in requested_ids:
            row = manifest_by_id.get(bid)
            if row is None:
                print(f"  WARNING: batch {bid!r} not found in manifest — skipping")
            else:
                target_rows.append(row)
        print(f"Mode: --batches {args.batches} -> {len(target_rows)} batches selected")

    if not target_rows:
        print("No target batches found. Nothing to do.")
        return 1

    print()

    # ── Verify classify template ──────────────────────────────────────────────
    if not CLASSIFY_TEMPLATE.exists():
        sys.exit(f"ERROR: classify template not found: {CLASSIFY_TEMPLATE}")
    _template_text = CLASSIFY_TEMPLATE.read_text()
    if "%%FILE_PAIRS%%" not in _template_text:
        sys.exit("ERROR: classify template missing %%FILE_PAIRS%% placeholder")
    if "%%LOCKED_VOCAB%%" not in _template_text:
        sys.exit("ERROR: classify template missing %%LOCKED_VOCAB%% placeholder")
    if not LOCKED_VOCAB.exists():
        sys.exit(f"ERROR: locked vocab file not found: {LOCKED_VOCAB}")

    # ── Process batches ───────────────────────────────────────────────────────
    run_started = time.time()
    all_results: list[dict] = []
    total_cost = 0.0
    total_files_done = 0
    total_files_attempted = 0
    all_rate_limit_events: list[dict] = []

    if args.dry_run:
        # Dry-run: show chunk plan for each batch, no API calls
        for batch_row in target_rows:
            result = run_batch(
                batch_row=batch_row,
                chunk_size=args.chunk_size,
                retries=args.retries,
                model=args.model,
                dry_run=True,
                concurrency=args.concurrency,
                skip_if_output_exists=args.skip_existing,
            )
            all_results.append(result)

    elif args.concurrency == 1:
        # Sequential: one chunk at a time, preserves exact prior behavior
        for batch_row in target_rows:
            result = run_batch(
                batch_row=batch_row,
                chunk_size=args.chunk_size,
                retries=args.retries,
                model=args.model,
                dry_run=False,
                concurrency=1,
                skip_if_output_exists=args.skip_existing,
            )
            all_results.append(result)
            total_cost += result.get("total_cost_usd", 0.0)
            total_files_done += result.get("files_done", 0)
            total_files_attempted += result.get("files_attempted", 0)

            # Write rate-limit events as we go (sequential — no race)
            batch_rl = result.get("rate_limit_events_count", 0)
            if batch_rl:
                # Re-read from chunk_timings to reconstruct events for the log
                # (run_batch sequential writes them inline via run_chunk return)
                pass  # rate-limit events from sequential are handled below

        # Collect rate-limit events from sequential batch results
        # (they are embedded in chunk_timings.rate_limited but not separately returned)
        # Sequential run_batch does NOT separately persist them — gather now
        # from the chunk_timings in each result and write once.
        sequential_rl_entries: list[dict] = []
        for result in all_results:
            for ct in result.get("chunk_timings", []):
                if ct.get("rate_limited"):
                    sequential_rl_entries.append({
                        "chunk_id": ct["chunk_id"],
                        "batch_id": result["batch_id"],
                        "detected_at": datetime.now(timezone.utc).isoformat(),
                        "note": "sequential run — see run-log for details",
                    })
        if sequential_rl_entries:
            with open(RATE_LIMIT_LOG, "a") as fh:
                for entry in sequential_rl_entries:
                    fh.write(json.dumps(entry) + "\n")
            all_rate_limit_events = sequential_rl_entries
            print(f"\nRate-limit events written: {RATE_LIMIT_LOG.relative_to(REPO)} "
                  f"({len(sequential_rl_entries)} events)")

    else:
        # Parallel: shared thread pool across all batches
        all_results, all_rate_limit_events = run_all_parallel(
            target_rows=target_rows,
            chunk_size=args.chunk_size,
            retries=args.retries,
            model=args.model,
            concurrency=args.concurrency,
            skip_if_output_exists=args.skip_existing,
        )
        for result in all_results:
            total_cost += result.get("total_cost_usd", 0.0)
            total_files_done += result.get("files_done", 0)
            total_files_attempted += result.get("files_attempted", 0)

    # ── Final summary ─────────────────────────────────────────────────────────
    elapsed = time.time() - run_started
    print()
    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"  Batches processed: {len(all_results)}")
    print(f"  Concurrency: {args.concurrency}")
    print(f"  Chunk size: {args.chunk_size}")

    if not args.dry_run:
        print(f"  Files attempted: {total_files_attempted}")
        print(f"  Files done: {total_files_done}")
        print(f"  Files failed: {total_files_attempted - total_files_done}")
        print(f"  Rate-limit events: {len(all_rate_limit_events)}")
        print(f"  Total cost: ${total_cost:.4f}")
        print(f"  Elapsed: {elapsed:.1f}s")
        print(f"  Output dir: {HAIKU_MISSION.relative_to(REPO)}/results/")

        # Per-chunk duration table
        all_chunk_timings: list[dict] = []
        for r in all_results:
            all_chunk_timings.extend(r.get("chunk_timings", []))
        if all_chunk_timings:
            print(f"\n  Per-chunk durations ({len(all_chunk_timings)} chunks):")
            for ct in sorted(all_chunk_timings, key=lambda x: x.get("chunk_id", "")):
                rl_flag = " [RATE-LIMITED]" if ct.get("rate_limited") else ""
                print(f"    {ct['chunk_id']}: {ct.get('duration_s', 0):.1f}s "
                      f"| ${ct.get('cost_usd', 0):.4f} "
                      f"| {ct.get('files_done', 0)} ok / {ct.get('files_failed', 0)} failed"
                      f"{rl_flag}")

        # Write run-summary.json
        run_summary = {
            "run_completed_at": datetime.now(timezone.utc).isoformat(),
            "model": args.model,
            "concurrency": args.concurrency,
            "chunk_size": args.chunk_size,
            "retries": args.retries,
            "wall_clock_s": round(elapsed, 2),
            "total_cost_usd": round(total_cost, 6),
            "batches_processed": len(all_results),
            "files_attempted": total_files_attempted,
            "files_done": total_files_done,
            "files_failed": total_files_attempted - total_files_done,
            "rate_limit_events_count": len(all_rate_limit_events),
            "rate_limit_events": all_rate_limit_events,
            "chunk_timings": all_chunk_timings,
        }
        summary_path = HAIKU_MISSION / "run-summary.json"
        summary_path.write_text(json.dumps(run_summary, indent=2) + "\n")
        print(f"\n  Run summary written: {summary_path.relative_to(REPO)}")

    else:
        print(f"  [dry-run] No files written, no API calls made")
        print(f"  Chunk plan printed for {len(target_rows)} batch(es)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
