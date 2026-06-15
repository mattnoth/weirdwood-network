"""End-to-end tests for scripts/longrun.sh — the generic long-run supervisor.

Exercises the exit-code contract (0=done, 2=wall, 10=more-work, other=crash) with
tiny sleeps so the whole suite runs in a few seconds. A fake runner script
increments a persistent counter file each invocation and exits with a scripted
sequence of codes — proving the supervisor relaunches the SAME argv (resume),
sleeps on the right signals, and stops on the right ones.
"""
import os
import subprocess
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LONGRUN = REPO_ROOT / "scripts" / "longrun.sh"

# Tiny sleeps so tests run fast; all paths still execute the real sleep calls.
FAST_ENV = {
    "LONGRUN_SLEEP_BETWEEN": "1",
    "LONGRUN_WALL_SLEEP": "1",
    "LONGRUN_CRASH_SLEEP": "1",
    "LONGRUN_MAX_CRASHES": "3",
}


def _write_runner(tmp_path: Path, codes) -> Path:
    """A runner that exits codes[0], codes[1], ... on successive calls, by
    counting its own invocations in a sidecar file. Last code repeats forever."""
    counter = tmp_path / "count"
    counter.write_text("0")
    seq = " ".join(str(c) for c in codes)
    runner = tmp_path / "fake_runner.sh"
    runner.write_text(textwrap.dedent(f"""\
        #!/usr/bin/env bash
        codes=({seq})
        n=$(cat "{counter}")
        echo "$((n + 1))" > "{counter}"
        idx=$n
        if (( idx >= ${{#codes[@]}} )); then idx=$((${{#codes[@]}} - 1)); fi
        echo "runner invocation $((n + 1)) exiting ${{codes[$idx]}}"
        exit "${{codes[$idx]}}"
    """))
    runner.chmod(0o755)
    return counter


def _run(tmp_path, codes, extra_env=None, timeout=60):
    counter = _write_runner(tmp_path, codes)
    env = {**os.environ, **FAST_ENV, **(extra_env or {})}
    proc = subprocess.run(
        ["bash", str(LONGRUN), "bash", str(tmp_path / "fake_runner.sh")],
        capture_output=True, text=True, env=env, timeout=timeout,
    )
    invocations = int(counter.read_text())
    return proc, invocations


def test_exit0_completes_immediately(tmp_path):
    proc, n = _run(tmp_path, [0])
    assert proc.returncode == 0
    assert n == 1
    assert "work complete" in proc.stdout


def test_exit10_then_exit0_loops_then_stops(tmp_path):
    # iter1: exit 10 (more work, sleep), iter2: exit 0 (done)
    proc, n = _run(tmp_path, [10, 0])
    assert proc.returncode == 0
    assert n == 2, "supervisor must relaunch the same argv after exit 10"
    assert "more work remains" in proc.stdout
    assert "work complete" in proc.stdout


def test_exit2_wall_then_resume_then_done(tmp_path):
    # iter1: exit 10, iter2: exit 2 (rate-limit wall), iter3: exit 0
    proc, n = _run(tmp_path, [10, 2, 0])
    assert proc.returncode == 0
    assert n == 3, "supervisor must resume the same argv across a rate-limit wall"
    assert "rate-limit wall" in proc.stdout
    assert "work complete" in proc.stdout


def test_crash_gives_up_after_max_crashes(tmp_path):
    # always crash (exit 1); MAX_CRASHES=3 → exactly 3 invocations then give up
    proc, n = _run(tmp_path, [1])
    assert proc.returncode == 1
    assert n == 3, "supervisor must give up after LONGRUN_MAX_CRASHES crashes"
    assert "giving up" in proc.stdout


def test_crash_streak_resets_on_progress(tmp_path):
    # crash, crash, then exit 10 (resets streak), crash, crash, then exit 0.
    # With MAX_CRASHES=3 a naive counter would give up; streak-reset must let it finish.
    proc, n = _run(tmp_path, [1, 1, 10, 1, 1, 0])
    assert proc.returncode == 0
    assert n == 6
    assert "work complete" in proc.stdout


def test_max_iter_cap(tmp_path):
    # runner always says "more work" (exit 10); LONGRUN_MAX_ITER caps it.
    proc, n = _run(tmp_path, [10], extra_env={"LONGRUN_MAX_ITER": "3"})
    assert proc.returncode == 0
    assert n == 3, "MAX_ITER must cap the number of iterations"
    assert "MAX_ITER" in proc.stdout
