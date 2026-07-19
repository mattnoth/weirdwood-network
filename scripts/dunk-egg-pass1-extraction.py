#!/usr/bin/env python3
"""dunk-egg-pass1-extraction.py — Dunk & Egg Pass-1 unattended worker (SCAFFOLD — do NOT run yet).

Status (S131/132): DESIGN SCAFFOLD. Lives in working/dunk-egg-pass1/ until Matt greenlights;
then `git mv` to scripts/ and register as a READY track in scripts/weirwood-run.sh (see run-plan).
LAUNCHES NOTHING on import. The actual extraction launch is a separate explicit Matt go-ahead
(memory feedback_no_extraction_without_asking) — this includes SMOKE runs (they call claude -p too).

WHAT THIS IS
------------
A copy of scripts/worker-template.py with the fake `_do_real_work()` replaced by the PROVEN
`claude -p` extraction call from scripts/extract.sh (lines ~494-578), adapted to:
  - run the subprocess with cwd=/tmp  (~49% cheaper — skips CLAUDE.md; reference_llm_pass_via_claude_p),
    so ALL paths in the prompt are absolute;
  - send a VERSIONED hardened prompt (working/dunk-egg-pass1/prompts/pass1-prompt-<version>.md);
  - write to extractions/mechanical/{thk,tss,tmk}/  (NEVER an archive folder —
    feedback_extraction_archive_rules). thk/tss/tmk are CANONICAL book codes, not abbreviations;
  - honor the longrun.sh exit-code contract (0 / 2 / 10 / crash).

PROMPT VERSIONS + SMOKE TESTING (the reason this worker takes --prompt-version / --smoke)
----------------------------------------------------------------------------------------
We will smoke-test a few prompt variants before committing to the full batch.
  prompts/pass1-prompt-v4.md, pass1-prompt-v4b.md, …   (the version id IS the filename suffix)

  SMOKE (attended, one unit, NO supervisor, NO manifest — outputs to a scratch dir so variants
         never touch the canonical tree or each other):
    python3 dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4
    python3 dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4b
    # then diff:  working/dunk-egg-pass1/smoke/v4/thk-dunk-01.extraction.md
    #        vs:  working/dunk-egg-pass1/smoke/v4b/thk-dunk-01.extraction.md

  FULL (unattended, supervised, writes the canonical extractions; pin the WINNING version):
    weirwood run start dunk-egg-pass1          # registry pins --prompt-version <winner>
    # = bash scripts/longrun.sh python3 scripts/dunk-egg-pass1-extraction.py --resume --prompt-version <winner>

One-time setup before the first FULL launch:
    python3 scripts/dunk-egg-pass1-extraction.py --build-queue

EXIT CODES (longrun.sh contract)
  0  — all units done           2  — POSITIVE rate-limit wall (exit 2 ONLY on a confirmed signal)
  10 — chunk done, more remain   other — crash (longrun retries)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = next(
    (p for p in [SCRIPT_DIR.parent, SCRIPT_DIR.parent.parent] if (p / "CLAUDE.md").exists()),
    SCRIPT_DIR.parent,
)

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import importlib.util as _ilu


def _load_pace():
    spec = _ilu.spec_from_file_location("pace", PROJECT_ROOT / "scripts" / "pace.py")
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


emit_telemetry_row = _load_pace().emit_telemetry_row

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TRACK = "dunk-egg-pass1"                          # telemetry + weirwood track name (no abbreviations)
MODEL = "claude-opus-4-8"                         # all Pass 1 is Opus (project_pass1_all_opus)
DEFAULT_PROMPT_VERSION = "v4"                     # overridden by --prompt-version
CHUNK_SIZE = 1                                    # 1 novella/iteration; long units, lose <=1 on crash
WORK_DIR = PROJECT_ROOT / "working" / "dunk-egg-pass1"
PROMPTS_DIR = WORK_DIR / "prompts"               # prompts/pass1-prompt-<version>.md
QUEUE_FILE = WORK_DIR / "queue.jsonl"          # whole-novella default; override with --queue
LOG_DIR = WORK_DIR / "logs"
SMOKE_DIR = WORK_DIR / "smoke"                    # smoke/<version>/<stem>.extraction.md (never canonical)
HARVEST_FILE = WORK_DIR / "harvest-dunk-egg.jsonl"
ARCH_PATH = PROJECT_ROOT / "reference" / "architecture.md"
TELEMETRY_DIR = PROJECT_ROOT / "working" / "telemetry"
SUBPROC_CWD = "/tmp"                              # skip project-context load

# Per-version state so a full run of v4 and a later full run of v4b never cross-mark each other.
def manifest_file(version: str) -> Path:
    return WORK_DIR / f"manifest-{version}.json"

def lock_dir_for(version: str) -> Path:
    return WORK_DIR / f"locks-{version}"

def prompt_file_for(version: str) -> Path:
    return PROMPTS_DIR / f"pass1-prompt-{version}.md"


# Whole-novella units. The split option (run-plan section 4) swaps this for per-part rows.
NOVELLAS = [
    {"unit_id": "thk", "book": "THK", "stem": "thk-dunk-01"},   # The Hedge Knight
    {"unit_id": "tss", "book": "TSS", "stem": "tss-dunk-01"},   # The Sworn Sword
    {"unit_id": "tmk", "book": "TMK", "stem": "tmk-dunk-01"},   # The Mystery Knight
]

ANCHOR_HEADERS = ["## Characters", "## Events", "## Locations", "## Relationships"]
RAW_LIST_CATEGORIES = [
    "### Characters", "### Locations", "### Houses", "### Factions & Organizations",
    "### Religions & Faiths", "### Cultures & Peoples", "### Artifacts & Objects",
    "### In-world Texts & Songs", "### Magic & Phenomena", "### Wars & Conflicts",
    "### Titles & Offices", "### Other",
]


# ---------------------------------------------------------------------------
# Atomic state
# ---------------------------------------------------------------------------
def _atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    os.replace(tmp, path)


def _load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return default


# ---------------------------------------------------------------------------
# Queue construction (--build-queue) — also makes the canonical output dirs
# ---------------------------------------------------------------------------
def build_queue() -> int:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for n in NOVELLAS:
        book_dir = n["unit_id"]
        src = PROJECT_ROOT / "sources" / "chapters" / book_dir / f"{n['stem']}.md"
        out_dir = PROJECT_ROOT / "extractions" / "mechanical" / book_dir   # NEVER archives/
        out_dir.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            print(f"ERROR: source missing: {src}", file=sys.stderr)
            return 1
        rows.append({
            "unit_id": n["unit_id"], "book": n["book"], "stem": n["stem"],
            "source": str(src),
            "out": str(out_dir / f"{n['stem']}.extraction.md"),
        })
    with open(QUEUE_FILE, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"Wrote {len(rows)} units -> {QUEUE_FILE}")
    print("Created output dirs under extractions/mechanical/{thk,tss,tmk}/")
    return 0


def _load_queue(queue_path: Path | None = None) -> list[dict]:
    path = queue_path or QUEUE_FILE
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


# ---------------------------------------------------------------------------
# Prompt assembly — pull the versioned prompt body, substitute absolute paths
# ---------------------------------------------------------------------------
def _build_prompt(prompt_path: Path, source: str, out_path: str) -> str:
    """Extract the THE-PROMPT body (between the heavy rules) from the chosen version file and
    substitute the four path placeholders. cwd=/tmp => all paths must be absolute."""
    text = prompt_path.read_text()
    rule = "═" * 79
    parts = text.split(rule)
    body = parts[1].strip() if len(parts) >= 3 else text
    return (
        body.replace("{ARCH_PATH}", str(ARCH_PATH))
            .replace("{SOURCE_PATH}", source)
            .replace("{OUT_PATH}", out_path)
            .replace("{HARVEST_PATH}", str(HARVEST_FILE))
    )


# ---------------------------------------------------------------------------
# The real work — proven claude -p call (ported from extract.sh:494-578)
# ---------------------------------------------------------------------------
def _do_real_work(unit: dict, out_path: str, version: str) -> dict:
    """Run claude -p for one unit to out_path using the version's prompt.
    status in {ok, invalid, wall, crash}."""
    prompt = _build_prompt(prompt_file_for(version), unit["source"], out_path)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    json_log = LOG_DIR / f"{version}-{unit['unit_id']}.json"

    cmd = [
        "claude", "-p", "--dangerously-skip-permissions",
        "--model", MODEL, "--verbose", "--output-format", "stream-json", prompt,
    ]
    with open(json_log, "w") as logfh:
        proc = subprocess.run(cmd, cwd=SUBPROC_CWD, stdout=logfh,
                              stderr=subprocess.STDOUT, text=True)

    raw = json_log.read_text()

    if '"status":"rejected"' in raw and '"rateLimitType"' in raw:   # POSITIVE wall only
        return {"status": "wall"}

    usage = {"input_tokens": None, "cache_creation": None, "cache_read": None,
             "output_tokens": None, "cost_usd": None}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "result":
            u = obj.get("usage", {})
            usage = {"input_tokens": u.get("input_tokens"),
                     "cache_creation": u.get("cache_creation_input_tokens"),
                     "cache_read": u.get("cache_read_input_tokens"),
                     "output_tokens": u.get("output_tokens"),
                     "cost_usd": obj.get("total_cost_usd")}
            break

    if proc.returncode != 0:
        return {"status": "crash", "usage": usage}
    if not _validate_output(Path(out_path), unit):
        return {"status": "invalid", "usage": usage}
    return {"status": "ok", "usage": usage}


def _validate_output(out_path: Path, unit: dict | None = None) -> bool:
    # Line floor scales with unit shape: 250 was calibrated on whole novellas
    # (THK smoke = 817 lines), but a scene-split part is ~1/7-1/9 of that
    # (TSS avg ≈ 89 lines/part) — the structural check for parts is the header
    # set below; the floor only catches truncation/garbage.
    whole = (unit or {}).get("unit_part", "whole") == "whole"
    min_lines = 250 if whole else 60
    if not out_path.exists():
        return False
    text = out_path.read_text()
    if len(text.splitlines()) < min_lines:
        return False
    if not all(h in text for h in ANCHOR_HEADERS):
        return False
    if not all(c in text for c in RAW_LIST_CATEGORIES):
        return False
    return True


def _emit(version: str, mode: str, run_id: str, worker_id: str, uid: str,
          started: str, elapsed: float, result: dict) -> None:
    usage = result.get("usage", {}) or {}
    emit_telemetry_row(TRACK, {
        "run_id": run_id, "track": TRACK, "worker_id": worker_id,
        "unit": uid, "unit_type": "novella", "started_at": started, "elapsed_s": elapsed,
        "input_tokens": usage.get("input_tokens"), "cache_creation": usage.get("cache_creation"),
        "cache_read": usage.get("cache_read"), "output_tokens": usage.get("output_tokens"),
        "cost_usd": usage.get("cost_usd"), "exit_reason": result["status"],
        "rate_limited": result["status"] == "wall", "sleep_taken_s": None,
        "model": MODEL, "prompt_version": version, "mode": mode,   # <- version/mode provenance
    }, telemetry_dir=TELEMETRY_DIR)


def _write_next_eligible() -> None:
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    (TELEMETRY_DIR / f"{TRACK}.next-eligible").write_text(str(int(time.time()) + 3600) + "\n")


def _claim(unit_id: str, lock_dir: Path) -> bool:
    lock_dir.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(lock_dir / f"{unit_id}.lock"), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return True
    except FileExistsError:
        return False


# ---------------------------------------------------------------------------
# SMOKE mode — attended, one-or-more units, no supervisor, no manifest,
# output to smoke/<version>/ so variants never touch the canonical tree.
# ---------------------------------------------------------------------------
def run_smoke(args: argparse.Namespace) -> int:
    version = args.prompt_version
    if not prompt_file_for(version).exists():
        print(f"ERROR: prompt not found: {prompt_file_for(version)}", file=sys.stderr)
        return 1
    queue_path = Path(args.queue).resolve() if args.queue else None
    units = _load_queue(queue_path)
    if not units:
        print("Queue empty. Run --build-queue first.", file=sys.stderr)
        return 1
    if args.only:
        units = [u for u in units if u["unit_id"] == args.only]
        if not units:
            print(f"ERROR: --only {args.only} matched no unit.", file=sys.stderr)
            return 1

    out_base = SMOKE_DIR / version
    out_base.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    worker_id = f"smoke-{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"
    print(f"SMOKE {version}: {len(units)} unit(s) -> {out_base}/")

    for unit in units:
        out_path = str(out_base / Path(unit["out"]).name)
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        t0 = time.monotonic()
        result = _do_real_work(unit, out_path, version)
        elapsed = round(time.monotonic() - t0, 1)
        _emit(version, "smoke", run_id, worker_id, unit["unit_id"], started, elapsed, result)
        print(f"  {unit['unit_id']}: {result['status']} in {elapsed}s -> {out_path}")
    print("Smoke done. Diff the version dirs under smoke/ to compare.")
    return 0


# ---------------------------------------------------------------------------
# FULL mode — unattended, supervised, canonical outputs (longrun.sh contract).
# ---------------------------------------------------------------------------
def run_worker(args: argparse.Namespace) -> int:
    version = args.prompt_version
    if not prompt_file_for(version).exists():
        print(f"ERROR: prompt not found: {prompt_file_for(version)}", file=sys.stderr)
        return 1
    queue_path = Path(args.queue).resolve() if args.queue else None
    units = _load_queue(queue_path)
    if not units:
        print("Queue empty. Run --build-queue first.", file=sys.stderr)
        return 1

    mf = manifest_file(version)
    manifest = _load_json(mf, {"done": [], "run_id": str(uuid.uuid4()), "prompt_version": version})
    run_id = manifest.get("run_id", str(uuid.uuid4()))
    lock_dir = lock_dir_for(version)
    worker_id = f"worker-{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}"

    pending = [u for u in units if u["unit_id"] not in manifest.get("done", [])]
    if not pending:
        print(f"All {len(units)} units done for {version}. Drained.")
        return 0
    print(f"{worker_id} [{version}]: {len(pending)} pending / {len(units)} total")
    done_this_chunk = 0

    for unit in pending:
        uid = unit["unit_id"]
        if uid in manifest.get("done", []):
            continue
        if not _claim(uid, lock_dir):
            print(f"  {uid}: claimed elsewhere, skip.")
            continue

        out_path = unit["out"]   # canonical extractions/mechanical/...
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        t0 = time.monotonic()
        result = _do_real_work(unit, out_path, version)
        elapsed = round(time.monotonic() - t0, 1)
        _emit(version, "full", run_id, worker_id, uid, started, elapsed, result)

        if result["status"] == "wall":
            # Release the claim — a walled unit is NOT done and must be
            # re-claimable after the supervisor's wall sleep (DE-4 fix: a held
            # lock made resume skip the unit forever and exit 0 "drained").
            (lock_dir / f"{uid}.lock").unlink(missing_ok=True)
            print(f"  {uid}: rate-limit wall. exit(2).")
            _write_next_eligible()
            return 2
        if result["status"] in ("crash", "invalid"):
            print(f"  {uid}: {result['status']} in {elapsed}s. exit(crash).")
            (lock_dir / f"{uid}.lock").unlink(missing_ok=True)
            return 1

        manifest["done"] = manifest.get("done", []) + [uid]
        _atomic_write_json(mf, manifest)
        print(f"  {uid}: done in {elapsed}s.")
        done_this_chunk += 1
        if done_this_chunk >= args.chunk_size:
            print(f"Chunk done ({done_this_chunk}). ~{len(pending) - done_this_chunk} remain. exit(10).")
            return 10

    # Only report drained if the manifest agrees — units skipped on a failed
    # claim (stale lock) must NOT produce a false exit-0 (DE-4 fix).
    still_pending = [u["unit_id"] for u in units if u["unit_id"] not in manifest.get("done", [])]
    if still_pending:
        print(f"WARNING: {len(still_pending)} unit(s) pending but unclaimable "
              f"(stale lock?): {still_pending}. exit(10) — supervisor will retry; "
              f"clear locks-{version}/<unit>.lock if this repeats.")
        return 10
    print(f"Queue drained ({len(units)} units, {version}). exit(0).")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="dunk-egg-pass1-extraction.py",
                                description="Dunk & Egg Pass-1 worker (SCAFFOLD). Versioned + smoke-aware.")
    p.add_argument("--resume", action="store_true", help="FULL unattended run (manifest-resumable).")
    p.add_argument("--smoke", action="store_true",
                   help="SMOKE: attended, output to smoke/<version>/, no manifest, no canonical writes.")
    p.add_argument("--only", metavar="UNIT", help="Restrict to one unit_id (thk|tss|tmk). Smoke mainly.")
    p.add_argument("--prompt-version", default=DEFAULT_PROMPT_VERSION, metavar="VER",
                   help=f"Which prompts/pass1-prompt-<VER>.md to use (default {DEFAULT_PROMPT_VERSION}).")
    p.add_argument("--build-queue", action="store_true",
                   help="One-time: create output dirs + write queue.jsonl, then exit.")
    p.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)
    p.add_argument(
        "--queue",
        metavar="PATH",
        default=None,
        help=(
            "Path to an alternate queue JSONL (e.g. queue-parts.jsonl for scene-split runs). "
            "Defaults to working/dunk-egg-pass1/queue.jsonl (whole novellas). "
            "Rows must have the same shape (unit_id, book, stem, source, out)."
        ),
    )
    return p


if __name__ == "__main__":
    # SAFETY: real claude -p loops fire only on --smoke or --resume. Per
    # feedback_no_extraction_without_asking, do not invoke either until Matt has signed off.
    args = _build_parser().parse_args()
    if args.build_queue:
        sys.exit(build_queue())
    if args.smoke:
        sys.exit(run_smoke(args))
    if args.resume:
        sys.exit(run_worker(args))
    print("Nothing to do. Use --build-queue (setup), --smoke (test a version), or --resume (full run).")
    print("This is a SCAFFOLD — do not --smoke/--resume until Matt greenlights the Dunk & Egg run.")
    sys.exit(0)
