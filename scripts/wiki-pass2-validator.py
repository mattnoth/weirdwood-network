#!/usr/bin/env python3
"""
wiki-pass2-validator.py — Gate validator for Wiki Pass 2 bucket output.

Validates every *.node.md file in <bucket_dir>/tmp/ before the launcher
performs the atomic rename from tmp/ into graph/nodes/.

Invocation (by wiki-pass2.sh::cmd_run):
    python3 scripts/wiki-pass2-validator.py \
        --bucket-dir working/wiki/pass2-buckets/<bucket_id> \
        --output working/wiki/pass2-buckets/<bucket_id>/validator-report.json

    Optional overrides (defer to bucket-dir layout if omitted):
        --bundle   working/wiki/pass2-buckets/<bucket_id>/bucket_input.json
        --manifest working/wiki/pass2-buckets/<bucket_id>/manifest.json

Exit codes:
    0 — all checks passed; launcher may promote tmp/ → graph/nodes/
    1 — one or more checks failed; launcher leaves tmp/ in place
    2 — internal error (unreadable bundle, bad args); logged to stderr

Stdout:
    Human-readable summary line per node, then final verdict.
    On failure, after the summary, prints the marker line
        ---VALIDATION-REPORT-JSON---
    followed by the JSON report (so the launcher can capture it from stdout
    in addition to reading the --output file).

OUT OF SCOPE for v1 (do not add without design review):
    - Body content checks (section density, citation coverage)
    - Edge labels validated against architecture.md controlled vocabulary
    - Whether claims are properly cited in the body prose
    - first_available format/parse validation (spoiler gating deferred)
    - Node body word-count threshold (see runbook open question #5)
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Architecture.md type-prefix extraction
# ---------------------------------------------------------------------------

def load_valid_type_prefixes(repo_root: Path) -> list[str]:
    """
    Read reference/architecture.md once and extract the valid entity-type
    prefixes from the Type Reference Table.

    Looks for table rows whose first column matches a known type pattern
    (e.g. `character.human`, `place.location`, `species`, `title`).
    Returns a list of exact type strings from the table — these are the only
    values the `type` frontmatter field may take.
    """
    arch_path = repo_root / "reference" / "architecture.md"
    if not arch_path.exists():
        raise FileNotFoundError(f"architecture.md not found at {arch_path}")

    text = arch_path.read_text(encoding="utf-8")

    # Match rows in the Type Reference Table:
    #   | `character.human` | ... |
    # The type token is the first backtick-quoted value in each pipe-delimited row.
    prefixes = re.findall(r"^\|\s*`([a-z][a-z0-9_.]*)`\s*\|", text, re.MULTILINE)
    if not prefixes:
        raise ValueError("Could not extract type prefixes from architecture.md — "
                         "table format may have changed")
    return prefixes


# ---------------------------------------------------------------------------
# YAML frontmatter parser
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> tuple[dict | None, str]:
    """
    Extract YAML frontmatter from a markdown file.

    Returns (parsed_dict, error_message). On success, error_message is "".
    On failure, parsed_dict is None and error_message describes the problem.
    """
    try:
        import yaml
    except ImportError:
        return None, "PyYAML not installed — run: pip3 install pyyaml"

    # Frontmatter must begin with '---' on the very first line.
    if not content.startswith("---"):
        return None, "file does not start with '---' (no frontmatter)"

    # Find the closing '---'
    end = content.find("\n---", 3)
    if end == -1:
        return None, "frontmatter block is not closed (missing second '---')"

    yaml_block = content[3:end].strip()
    try:
        data = yaml.safe_load(yaml_block)
    except Exception as exc:  # noqa: BLE001
        return None, f"YAML parse error: {exc}"

    if not isinstance(data, dict):
        return None, "frontmatter parsed to a non-dict value"

    return data, ""


# ---------------------------------------------------------------------------
# Per-node checks
# ---------------------------------------------------------------------------

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
CONFIDENCE_RE = re.compile(r"^tier-[1-4]$")


def check_node(
    node_path: Path,
    expected_bucket_id: str,
    expected_prompt_version: str,
    valid_types: list[str],
) -> list[dict]:
    """
    Run all v1 checks against a single *.node.md file.

    Returns a list of failure dicts:
        {"node": filename, "check": check_name, "field": field, "detail": detail}
    An empty list means the node passed.
    """
    filename = node_path.name
    failures = []

    def fail(check: str, field: str, detail: str) -> None:
        failures.append({"node": filename, "check": check, "field": field, "detail": detail})

    # ── Check 1: file parses as YAML frontmatter ────────────────────────────
    try:
        content = node_path.read_text(encoding="utf-8")
    except OSError as exc:
        fail("file-readable", "file", str(exc))
        return failures  # Cannot proceed without content

    fm, err = parse_frontmatter(content)
    if fm is None:
        fail("frontmatter-parse", "frontmatter", err)
        return failures  # All subsequent checks need the parsed frontmatter

    # ── Check 2: required fields present and non-empty ──────────────────────
    required_string_fields = ["name", "type", "slug", "confidence", "wiki_source",
                               "bucket_id", "prompt_version", "pass_origin"]
    for field in required_string_fields:
        value = fm.get(field)
        if value is None:
            fail("required-field", field, "missing")
        elif not isinstance(value, str) or not value.strip():
            fail("required-field", field, "empty or wrong type (expected non-empty string)")

    # node_version must be integer 1
    nv = fm.get("node_version")
    if nv is None:
        fail("required-field", "node_version", "missing")
    elif nv != 1:
        fail("required-field", "node_version", f"expected integer 1, got {nv!r}")

    # ── Check 3: first_available — optional in v1, accept any non-empty string
    # No check performed. If present, any non-empty string is valid.

    # ── Check 4 (part of required-field): type is in architecture.md taxonomy
    node_type = fm.get("type", "")
    if isinstance(node_type, str) and node_type.strip():
        if node_type.strip() not in valid_types:
            fail("type-prefix", "type",
                 f"'{node_type}' not found in architecture.md type table")

    # ── Check 5 (part of required-field): slug format ───────────────────────
    slug = fm.get("slug", "")
    if isinstance(slug, str) and slug.strip():
        if not SLUG_RE.match(slug.strip()):
            fail("slug-format", "slug",
                 f"'{slug}' is not lowercase kebab-case ([a-z0-9-]+)")

    # ── Check 6 (part of required-field): confidence format ─────────────────
    confidence = fm.get("confidence", "")
    if isinstance(confidence, str) and confidence.strip():
        if not CONFIDENCE_RE.match(confidence.strip()):
            fail("confidence-format", "confidence",
                 f"'{confidence}' does not match tier-[1-4]")

    # ── Check 7 (part of required-field): bucket_id matches bundle ──────────
    node_bucket = fm.get("bucket_id", "")
    if isinstance(node_bucket, str) and node_bucket.strip():
        if node_bucket.strip() != expected_bucket_id:
            fail("bucket-id-mismatch", "bucket_id",
                 f"node has '{node_bucket}', bundle expects '{expected_bucket_id}'")

    # ── Check 8 (part of required-field): prompt_version matches bundle ─────
    node_pv = fm.get("prompt_version", "")
    if isinstance(node_pv, str) and node_pv.strip():
        if node_pv.strip() != expected_prompt_version:
            fail("prompt-version-mismatch", "prompt_version",
                 f"node has '{node_pv}', bundle expects '{expected_prompt_version}'")

    # ── Check 9 (part of required-field): pass_origin ───────────────────────
    po = fm.get("pass_origin", "")
    if isinstance(po, str) and po.strip():
        if po.strip() != "pass2-wiki":
            fail("pass-origin", "pass_origin",
                 f"expected 'pass2-wiki', got '{po}'")

    # ── Check 10: slug matches filename ─────────────────────────────────────
    slug_value = fm.get("slug", "")
    expected_slug = filename.removesuffix(".node.md")
    if isinstance(slug_value, str) and slug_value.strip():
        if slug_value.strip() != expected_slug:
            fail("slug-filename-mismatch", "slug",
                 f"slug field '{slug_value}' does not match filename stem '{expected_slug}'")

    # ── Check 11 (optional field type-checks) ───────────────────────────────
    same_as = fm.get("same_as")
    if same_as is not None and not isinstance(same_as, str):
        fail("optional-field-type", "same_as",
             f"expected string, got {type(same_as).__name__}")

    disputed = fm.get("disputed")
    if disputed is not None and disputed is not True:
        fail("optional-field-type", "disputed",
             f"expected boolean true, got {disputed!r}")

    return failures


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Wiki Pass 2 bucket tmp/ output before promotion to graph/nodes/."
    )
    parser.add_argument("--bucket-dir", required=True,
                        help="Path to the bucket directory (e.g. working/wiki/pass2-buckets/direwolves)")
    parser.add_argument("--output", required=False,
                        help="Path to write the JSON validation report (overwritten each run). "
                             "Optional — if omitted, report is only written to stdout on failure.")
    parser.add_argument("--bundle", required=False,
                        help="Path to bucket_input.json. Defaults to <bucket-dir>/bucket_input.json.")
    parser.add_argument("--manifest", required=False,
                        help="Path to manifest.json. Defaults to <bucket-dir>/manifest.json.")
    args = parser.parse_args()

    # Resolve repo root (script lives in scripts/, repo root is one level up)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    bucket_dir = Path(args.bucket_dir)
    if not bucket_dir.is_absolute():
        bucket_dir = repo_root / bucket_dir
    bucket_dir = bucket_dir.resolve()

    bundle_path = Path(args.bundle) if args.bundle else bucket_dir / "bucket_input.json"
    if not bundle_path.is_absolute():
        bundle_path = repo_root / bundle_path

    manifest_path = Path(args.manifest) if args.manifest else bucket_dir / "manifest.json"
    if not manifest_path.is_absolute():
        manifest_path = repo_root / manifest_path

    # ── Load architecture.md type prefixes ──────────────────────────────────
    try:
        valid_types = load_valid_type_prefixes(repo_root)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: could not load valid types from architecture.md: {exc}", file=sys.stderr)
        return 2

    # ── Load bundle ─────────────────────────────────────────────────────────
    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: bundle not found: {bundle_path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: bundle is not valid JSON: {exc}", file=sys.stderr)
        return 2

    bucket_id = bundle.get("bucket_id", "")
    prompt_version = bundle.get("prompt_version", "")
    pages = bundle.get("pages", [])
    node_count_expected = len(pages)

    if not bucket_id:
        print("ERROR: bundle missing 'bucket_id'", file=sys.stderr)
        return 2
    if not prompt_version:
        print("ERROR: bundle missing 'prompt_version'", file=sys.stderr)
        return 2

    # ── Enumerate tmp/ ───────────────────────────────────────────────────────
    tmp_dir = bucket_dir / "tmp"
    if not tmp_dir.is_dir():
        print(f"ERROR: tmp/ directory not found at {tmp_dir}", file=sys.stderr)
        return 2

    node_files = sorted(tmp_dir.glob("*.node.md"))
    node_count_actual = len(node_files)

    # ── Run per-node checks ──────────────────────────────────────────────────
    all_failures: list[dict] = []
    checked_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"Validating bucket '{bucket_id}' — {node_count_actual} nodes found, "
          f"{node_count_expected} expected")
    print(f"  Type taxonomy: {len(valid_types)} valid types loaded from architecture.md")
    print()

    for node_path in node_files:
        node_failures = check_node(
            node_path,
            expected_bucket_id=bucket_id,
            expected_prompt_version=prompt_version,
            valid_types=valid_types,
        )
        if node_failures:
            status = "FAIL"
        else:
            status = "OK"
        print(f"  [{status}] {node_path.name}")
        for f in node_failures:
            print(f"        {f['check']} / {f['field']}: {f['detail']}")
        all_failures.extend(node_failures)

    # ── File count check ─────────────────────────────────────────────────────
    count_ok = (node_count_actual == node_count_expected)
    if not count_ok:
        direction = "missing" if node_count_actual < node_count_expected else "extra (contract violation)"
        all_failures.append({
            "node": "(bucket)",
            "check": "node-count",
            "field": "pages",
            "detail": (
                f"{direction}: expected {node_count_expected}, got {node_count_actual}"
            ),
        })

    # ── Final verdict ────────────────────────────────────────────────────────
    passed = len(all_failures) == 0

    print()
    if passed:
        print(f"PASS — bucket '{bucket_id}' validated ({node_count_actual} nodes)")
    else:
        print(f"FAIL — bucket '{bucket_id}': {len(all_failures)} failure(s) across "
              f"{node_count_actual} nodes")

    # ── Build JSON report ────────────────────────────────────────────────────
    report = {
        "bucket_id": bucket_id,
        "passed": passed,
        "checked_at": checked_at,
        "node_count_expected": node_count_expected,
        "node_count_actual": node_count_actual,
        "failures": all_failures,
    }

    # Write to --output file if specified (launcher captures this path)
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = repo_root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # On failure: also emit JSON to stdout after the human summary
    # (marker lets the caller grep/split the two sections)
    if not passed:
        print()
        print("---VALIDATION-REPORT-JSON---")
        print(json.dumps(report, indent=2))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
