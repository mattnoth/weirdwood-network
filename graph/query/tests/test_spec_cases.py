"""test_spec_cases.py — the pytest half of the drift alarm (query-layer
Track, S191 D-G checkpoint #3/final session).

graph/query/spec/run_cases.py is the existing standalone verification runner
for every "full"/"both"-profile golden case in graph/query/spec/cases/*.json.
This module does NOT reimplement case interpretation — it imports run_cases.py
directly (sys.path trick, mirroring conftest.py's own import pattern) and
wraps its per-case Engine + RUNNERS dispatch in one pytest test per case id,
so a case's PASS/FAIL/SKIP verdict becomes a pytest pass/fail/skip instead of
a line in a script's stdout.

Marked `corpus` — these cases run against the REAL graph/bundle
(graph/edges/edges.jsonl, web/data/{nodes,edges}.json), not the mini fixture.
Skipped whole-module when the graph/bundle inputs aren't present at all (the
per-case runner already skips gracefully case-by-case when an input or
callable is missing — this module-level skip only guards the pathological
case of running in an environment with no graph checked out whatsoever).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
QUERY_DIR = TESTS_DIR.parent  # graph/query
SPEC_DIR = QUERY_DIR / "spec"
REPO_ROOT = QUERY_DIR.parent.parent  # graph/query -> graph -> repo root

if str(QUERY_DIR) not in sys.path:
    sys.path.insert(0, str(QUERY_DIR))

# Import run_cases.py by path (it lives in spec/, not a package with an
# __init__.py) — importlib rather than a bare `import run_cases` so this
# works regardless of the caller's sys.path/cwd.
_RUN_CASES_PATH = SPEC_DIR / "run_cases.py"
_spec = importlib.util.spec_from_file_location("weirwood_run_cases", _RUN_CASES_PATH)
run_cases = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(run_cases)

pytestmark = pytest.mark.corpus

EDGES_FILE = REPO_ROOT / "graph" / "edges" / "edges.jsonl"
WEB_DATA_DIR = REPO_ROOT / "web" / "data"

# Bundle-staleness guard (S210 board finding). The `family.json` corpus goldens
# read web/data/{edges,nodes}.json — a GITIGNORED build artifact rebuilt only by
# `netlify deploy --build` / build_chat_bundle.py, NOT on every graph mutation.
# Between deploys the bundle lags the live graph, so those goldens would validate
# STALE data and pass misleadingly (this is why S205-S209 reported "green" while
# actually checking week-old data). A fresh bundle exactly equals the live counts,
# so any real lag is hundreds of edges — well past this tolerance. When the two
# diverge we SKIP the bundle-reading goldens with a loud reason instead of
# reporting a false green.
_STALENESS_TOLERANCE = 25


def _bundle_staleness_reason() -> str | None:
    """Skip-reason string if web/data lags the live graph, else None."""
    import json
    edges_json = WEB_DATA_DIR / "edges.json"
    if not edges_json.exists():
        return "web/data/edges.json not built (run build_chat_bundle.py or `netlify deploy --build`)"
    try:
        bundle_n = len(json.loads(edges_json.read_text(encoding="utf-8")))
        live_n = sum(1 for _ in EDGES_FILE.open(encoding="utf-8"))
    except Exception as e:  # pragma: no cover - defensive
        return f"could not compare bundle vs live edge counts: {type(e).__name__}: {e}"
    if abs(live_n - bundle_n) > _STALENESS_TOLERANCE:
        return (
            f"BUNDLE STALE — web/data/edges.json has {bundle_n} edges vs {live_n} live "
            f"(graph/edges/edges.jsonl). The bundle only rebuilds on deploy/build, so these "
            f"goldens would validate stale data. Rebuild web/data (build_chat_bundle.py) first."
        )
    return None


_BUNDLE_STALE_REASON = _bundle_staleness_reason()

_ENGINE = run_cases.Engine()


def _collect_pytest_cases() -> list[tuple[str, dict]]:
    """Mirror run_cases.main()'s case-selection loop: for each case file,
    include every case that runs_under_full() (or is family.json, which
    always runs per run_cases.py's FAMILY_ALWAYS_RUNS special-case). Returns
    (case_file, case_dict) tuples so each becomes one parametrized test."""
    collected: list[tuple[str, dict]] = []
    for filename in run_cases.CASE_FILES:
        cases = run_cases.load_cases(filename)
        for case in cases:
            if filename != run_cases.FAMILY_ALWAYS_RUNS and not run_cases.runs_under_full(case):
                continue
            collected.append((filename, case))
    return collected


_CASES = _collect_pytest_cases()
_IDS = [f"{filename}:{case['id']}" for filename, case in _CASES]


@pytest.mark.skipif(
    not EDGES_FILE.exists(),
    reason="graph/edges/edges.jsonl not present — the real graph isn't checked out/built here",
)
@pytest.mark.parametrize("filename, case", _CASES, ids=_IDS)
def test_golden_case(filename, case):
    if not _ENGINE.ok:
        pytest.skip(f"weirwood_query not importable: {_ENGINE.error}")

    # family.json cases read the built bundle (web/data via run_cases.load_bundle);
    # skip them loudly rather than validate a stale bundle (see _bundle_staleness_reason).
    if filename == run_cases.FAMILY_ALWAYS_RUNS and _BUNDLE_STALE_REASON:
        pytest.skip(_BUNDLE_STALE_REASON)

    runner = run_cases.RUNNERS.get(case["op"])
    if runner is None:
        pytest.skip(f"no runner registered for op {case['op']!r}")

    status, detail = runner(_ENGINE, case)

    if status == "skip":
        pytest.skip(detail)
    elif status == "fail":
        assert False, f"{filename}:{case['id']} — {detail}"
    else:
        assert status == "pass"
