#!/usr/bin/env python3
"""fire-and-blood-extraction.py — Fire & Blood enrichment unattended worker (SCAFFOLD — do NOT run yet).

Status (S198): DESIGN SCAFFOLD, mirrors working/dunk-egg-pass1/dunk-egg-pass1-extraction.py almost exactly.
Lives in working/fire-and-blood/ until Matt greenlights; then `git mv` to scripts/ and register as a READY
track in scripts/weirwood-run.sh (see "Wiring weirwood run start fire-and-blood" below — as of this build,
dunk-egg-pass1 ITSELF is not yet registered there either; see that section for why).
LAUNCHES NOTHING on import. The actual extraction launch is a separate explicit Matt go-ahead
(memory feedback_no_extraction_without_asking) — this includes SMOKE runs (they call claude -p too).

WHAT THIS IS
------------
A copy of working/dunk-egg-pass1/dunk-egg-pass1-extraction.py, adapted for the Fire & Blood node-first
enrichment pass (build-spec-s198.md "Script 3"):
  - queue built from sources/chapters/fab/*.md (39 units — whole sections + split parts);
  - run the subprocess with cwd=/tmp (~49% cheaper — skips CLAUDE.md; reference_llm_pass_via_claude_p),
    so ALL paths in the prompt are absolute;
  - send a VERSIONED prompt (working/fire-and-blood/prompts/fab-enrichment-<version>.md);
  - per-unit roster hint generated from the unit's candidate pack (names-only, capped ~1500 names);
  - write to extractions/fire-and-blood/<unit>.enrichment.md (never a graph/ or sources/ write —
    this worker produces enrichment PROPOSALS; fab-reconcile-candidates.py is the separate consumer);
  - honor the longrun.sh exit-code contract (0 / 2 / 10 / crash).

PROMPT VERSIONS + SMOKE TESTING
--------------------------------
  SMOKE (attended, one-or-more units, NO supervisor, NO manifest — outputs to a scratch dir so variants
         never touch the canonical tree or each other):
    python3 fire-and-blood-extraction.py --smoke --only fab-aegons-conquest-03 --prompt-version v1
    # then inspect: working/fire-and-blood/smoke/v1/fab-aegons-conquest-03.enrichment.md

  FULL (unattended, supervised, writes the canonical extractions; pin the WINNING version):
    weirwood run start fire-and-blood          # registry pins --prompt-version <winner>
    # = bash scripts/longrun.sh python3 working/fire-and-blood/fire-and-blood-extraction.py \\
    #       --resume --prompt-version v1

One-time setup before the first FULL launch:
    python3 working/fire-and-blood/fire-and-blood-extraction.py --build-queue

EXIT CODES (longrun.sh contract)
  0  — all units done           2  — POSITIVE rate-limit wall (exit 2 ONLY on a confirmed signal)
  10 — chunk done, more remain   other — crash (longrun retries)

DEBUG/INSPECTION (no claude -p call)
  --dry-render --only <unit> --prompt-version v1   # print the fully-substituted prompt, no subprocess
"""

import argparse
import json
import os
import re
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
TRACK = "fire-and-blood"                          # telemetry + weirwood track name
MODEL = "claude-opus-4-8"                         # node prose is the portfolio product — reasoning-depth carve-out
DEFAULT_PROMPT_VERSION = "v1"                     # overridden by --prompt-version
CHUNK_SIZE = 1                                    # 1 unit/iteration; long units, lose <=1 on crash
WORK_DIR = PROJECT_ROOT / "working" / "fire-and-blood"
PROMPTS_DIR = WORK_DIR / "prompts"                 # prompts/fab-enrichment-<version>.md
SOURCE_DIR = PROJECT_ROOT / "sources" / "chapters" / "fab"
OUT_DIR = PROJECT_ROOT / "extractions" / "fire-and-blood"
CANDIDATE_PACKS_DIR = WORK_DIR / "candidate-packs"
ROSTER_HINTS_DIR = WORK_DIR / "roster-hints"
QUEUE_FILE = WORK_DIR / "queue.jsonl"
LOG_DIR = WORK_DIR / "logs"
SMOKE_DIR = WORK_DIR / "smoke"                    # smoke/<version>/<unit>.enrichment.md (never canonical)
HARVEST_FILE = WORK_DIR / "harvest-fire-and-blood.jsonl"
TELEMETRY_DIR = PROJECT_ROOT / "working" / "telemetry"
SUBPROC_CWD = "/tmp"                              # skip project-context load

ROSTER_HINT_MAX_NAMES = 1500                      # ~2K-token cap; truncate by anchor_count, note it


# Per-version state so a full run of v1 and a later full run of v1b never cross-mark each other.
def manifest_file(version: str) -> Path:
    return WORK_DIR / f"manifest-{version}.json"


def lock_dir_for(version: str) -> Path:
    return WORK_DIR / f"locks-{version}"


def prompt_file_for(version: str) -> Path:
    return PROMPTS_DIR / f"fab-enrichment-{version}.md"


ANCHOR_HEADERS = ["## Entity Roster", "## Relationships Observed"]


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
# Frontmatter parsing (tiny hand-roller — avoids a yaml dependency for 5 scalar fields)
# ---------------------------------------------------------------------------
def _parse_frontmatter(text: str) -> dict:
    """Pull simple `key: value` scalars out of a leading `---\\n...\\n---` YAML block.
    Good enough for the flat string/int fields fab chapter files use; does not handle
    nested/list YAML (none of the fields we read are nested)."""
    meta: dict = {}
    if not text.startswith("---"):
        return meta
    end = text.find("\n---", 3)
    if end == -1:
        return meta
    block = text[3:end]
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith('"') and val.endswith('"') and len(val) >= 2:
            val = val[1:-1]
        elif val.startswith("'") and val.endswith("'") and len(val) >= 2:
            val = val[1:-1]
        meta[key] = val
    return meta


# ---------------------------------------------------------------------------
# Unit-id -> slug (for candidate-pack lookup)
# ---------------------------------------------------------------------------
_UNIT_RE = re.compile(r"^fab-(?P<slug>.+?)-\d{2}(?:-p\d+)?$")


def _slug_from_unit_id(unit_id: str) -> str | None:
    """fab-aegons-conquest-03 -> aegons-conquest; fab-heirs-of-the-dragon-15-p01 -> heirs-of-the-dragon."""
    m = _UNIT_RE.match(unit_id)
    return m.group("slug") if m else None


def _pack_path_for_slug(slug: str) -> Path | None:
    """Candidate packs are fab-<slug>-NNN.json (3-digit nn); glob since nn isn't derivable from the
    chapter's 2-digit section_number without a leading-zero mismatch."""
    matches = sorted(CANDIDATE_PACKS_DIR.glob(f"fab-{slug}-*.json"))
    matches = [m for m in matches if m.name not in ("_index.md", "_unmapped-sections.md")]
    return matches[0] if matches else None


# ---------------------------------------------------------------------------
# Roster hint generation (--build-queue time; names-only, capped)
# ---------------------------------------------------------------------------
def _build_roster_hint(unit_id: str) -> Path:
    """Write working/fire-and-blood/roster-hints/<unit>.roster-hint.txt — one name per line
    (with top aliases), capped at ROSTER_HINT_MAX_NAMES, ranked by anchor_count when truncating.
    Empty file (still written) if no candidate pack matches this unit's slug."""
    ROSTER_HINTS_DIR.mkdir(parents=True, exist_ok=True)
    hint_path = ROSTER_HINTS_DIR / f"{unit_id}.roster-hint.txt"

    slug = _slug_from_unit_id(unit_id)
    pack_path = _pack_path_for_slug(slug) if slug else None
    if pack_path is None:
        hint_path.write_text("")
        return hint_path

    pack = _load_json(pack_path, {})
    per_slug = pack.get("per_slug", {}) or {}
    rows = list(per_slug.values())
    rows.sort(key=lambda r: r.get("anchor_count", 0), reverse=True)

    truncated = len(rows) > ROSTER_HINT_MAX_NAMES
    if truncated:
        rows = rows[:ROSTER_HINT_MAX_NAMES]

    lines = []
    if truncated:
        lines.append(
            f"# truncated to top {ROSTER_HINT_MAX_NAMES} of {len(per_slug)} names by anchor_count"
        )
    for r in rows:
        name = r.get("name", "").strip()
        if not name:
            continue
        aliases = r.get("aliases") or []
        top_aliases = [a for a in aliases[:2] if a]
        if top_aliases:
            lines.append(f"{name} (aka {', '.join(top_aliases)})")
        else:
            lines.append(name)

    hint_path.write_text("\n".join(lines) + ("\n" if lines else ""))
    return hint_path


# ---------------------------------------------------------------------------
# Queue construction (--build-queue) — also makes the canonical output dir + roster hints
# ---------------------------------------------------------------------------
def build_queue() -> int:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not SOURCE_DIR.exists():
        print(f"ERROR: source dir missing: {SOURCE_DIR}", file=sys.stderr)
        return 1

    src_files = sorted(SOURCE_DIR.glob("*.md"))
    if not src_files:
        print(f"ERROR: no *.md files found under {SOURCE_DIR}", file=sys.stderr)
        return 1

    rows = []
    hints_written = 0
    no_pack_units = []
    for src in src_files:
        unit_id = src.stem  # e.g. fab-aegons-conquest-03, fab-heirs-of-the-dragon-15-p01
        hint_path = _build_roster_hint(unit_id)
        hints_written += 1
        if hint_path.stat().st_size == 0:
            no_pack_units.append(unit_id)
        rows.append({
            "unit_id": unit_id,
            "source": str(src),
            "out": str(OUT_DIR / f"{unit_id}.enrichment.md"),
            "roster_hint": str(hint_path),
        })

    with open(QUEUE_FILE, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")

    print(f"Wrote {len(rows)} units -> {QUEUE_FILE}")
    print(f"Created output dir: {OUT_DIR}")
    print(f"Wrote {hints_written} roster-hint files -> {ROSTER_HINTS_DIR}")
    if no_pack_units:
        print(f"WARNING: {len(no_pack_units)} unit(s) had no matching candidate pack "
              f"(empty hint written): {', '.join(no_pack_units)}")
    return 0


def _load_queue(queue_path: Path | None = None) -> list[dict]:
    path = queue_path or QUEUE_FILE
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


# ---------------------------------------------------------------------------
# Prompt assembly — pull the versioned prompt body, substitute placeholders
# ---------------------------------------------------------------------------
def _build_prompt(prompt_path: Path, unit: dict, out_path: str) -> str:
    """Extract the THE-PROMPT body (between the heavy rules) from the chosen version file and
    substitute the placeholders. cwd=/tmp => all paths must be absolute."""
    text = prompt_path.read_text()
    rule = "═" * 79
    parts = text.split(rule)
    body = parts[1].strip() if len(parts) >= 3 else text

    source_path = unit["source"]
    frontmatter = _parse_frontmatter(Path(source_path).read_text())
    section_title = frontmatter.get("section_title", "")
    era = frontmatter.get("era", "")
    first_available = frontmatter.get("first_available", "")

    return (
        body.replace("{SOURCE_PATH}", source_path)
            .replace("{OUT_PATH}", out_path)
            .replace("{HARVEST_PATH}", str(HARVEST_FILE))
            .replace("{ROSTER_HINT_PATH}", unit.get("roster_hint", ""))
            .replace("{SECTION_TITLE}", section_title)
            .replace("{ERA}", era)
            .replace("{FIRST_AVAILABLE}", first_available)
    )


# ---------------------------------------------------------------------------
# The real work — proven claude -p call, ported from the D&E worker
# ---------------------------------------------------------------------------
def _do_real_work(unit: dict, out_path: str, version: str) -> dict:
    """Run claude -p for one unit to out_path using the version's prompt.
    status in {ok, invalid, wall, crash}."""
    prompt = _build_prompt(prompt_file_for(version), unit, out_path)
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
    if not _validate_output(Path(out_path)):
        return {"status": "invalid", "usage": usage}
    return {"status": "ok", "usage": usage}


def _validate_output(out_path: Path) -> bool:
    """Minimally valid: both anchor headers present (per build-spec-s198.md Script 3)."""
    if not out_path.exists():
        return False
    text = out_path.read_text()
    if not all(h in text for h in ANCHOR_HEADERS):
        return False
    return True


def _emit(version: str, mode: str, run_id: str, worker_id: str, uid: str,
          started: str, elapsed: float, result: dict) -> None:
    usage = result.get("usage", {}) or {}
    emit_telemetry_row(TRACK, {
        "run_id": run_id, "track": TRACK, "worker_id": worker_id,
        "unit": uid, "unit_type": "fab-section", "started_at": started, "elapsed_s": elapsed,
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
# DRY-RENDER mode — print the fully-substituted prompt, no subprocess call at all.
# ---------------------------------------------------------------------------
def run_dry_render(args: argparse.Namespace) -> int:
    version = args.prompt_version
    if not prompt_file_for(version).exists():
        print(f"ERROR: prompt not found: {prompt_file_for(version)}", file=sys.stderr)
        return 1
    if not args.only:
        print("ERROR: --dry-render requires --only <unit_id>.", file=sys.stderr)
        return 1

    queue_path = Path(args.queue).resolve() if args.queue else None
    units = _load_queue(queue_path)
    if not units:
        print("Queue empty. Run --build-queue first.", file=sys.stderr)
        return 1
    matches = [u for u in units if u["unit_id"] == args.only]
    if not matches:
        print(f"ERROR: --only {args.only} matched no unit.", file=sys.stderr)
        return 1
    unit = matches[0]

    out_path = unit["out"]
    prompt = _build_prompt(prompt_file_for(version), unit, out_path)

    remaining_placeholders = re.findall(r"\{[A-Z_]+\}", prompt)
    print(prompt)
    print("\n" + "=" * 79)
    if remaining_placeholders:
        print(f"WARNING: unsubstituted placeholders remain: {sorted(set(remaining_placeholders))}")
    else:
        print("OK: no unsubstituted {PLACEHOLDER} tokens remain.")
    return 0


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

        out_path = unit["out"]   # canonical extractions/fire-and-blood/...
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        t0 = time.monotonic()
        result = _do_real_work(unit, out_path, version)
        elapsed = round(time.monotonic() - t0, 1)
        _emit(version, "full", run_id, worker_id, uid, started, elapsed, result)

        if result["status"] == "wall":
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

    print(f"Queue drained ({len(units)} units, {version}). exit(0).")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fire-and-blood-extraction.py",
                                description="Fire & Blood enrichment worker (SCAFFOLD). Versioned + smoke-aware.")
    p.add_argument("--resume", action="store_true", help="FULL unattended run (manifest-resumable).")
    p.add_argument("--smoke", action="store_true",
                   help="SMOKE: attended, output to smoke/<version>/, no manifest, no canonical writes.")
    p.add_argument("--dry-render", action="store_true",
                   help="Print the fully-substituted prompt for --only <unit>. No claude -p call.")
    p.add_argument("--only", metavar="UNIT", help="Restrict to one unit_id. Smoke/dry-render mainly.")
    p.add_argument("--prompt-version", default=DEFAULT_PROMPT_VERSION, metavar="VER",
                   help=f"Which prompts/fab-enrichment-<VER>.md to use (default {DEFAULT_PROMPT_VERSION}).")
    p.add_argument("--build-queue", action="store_true",
                   help="One-time: create output dir + roster hints + write queue.jsonl, then exit.")
    p.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)
    p.add_argument(
        "--queue",
        metavar="PATH",
        default=None,
        help=(
            "Path to an alternate queue JSONL. Defaults to working/fire-and-blood/queue.jsonl. "
            "Rows must have the same shape (unit_id, source, out, roster_hint)."
        ),
    )
    return p


if __name__ == "__main__":
    # SAFETY: real claude -p loops fire only on --smoke or --resume. Per
    # feedback_no_extraction_without_asking, do not invoke either until Matt has signed off.
    args = _build_parser().parse_args()
    if args.build_queue:
        sys.exit(build_queue())
    if args.dry_render:
        sys.exit(run_dry_render(args))
    if args.smoke:
        sys.exit(run_smoke(args))
    if args.resume:
        sys.exit(run_worker(args))
    print("Nothing to do. Use --build-queue (setup), --dry-render --only <unit> (inspect a prompt),")
    print("--smoke (test a version), or --resume (full run).")
    print("This is a SCAFFOLD — do not --smoke/--resume until Matt greenlights the Fire & Blood run.")
    sys.exit(0)
