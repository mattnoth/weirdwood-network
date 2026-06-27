#!/usr/bin/env python3
"""
sift.py — The Sift: a two-stage corpus scanner for the Weirwood Network.

Stage 1 (this file): pure Python deterministic scan → pointer JSONL files.
Stage 2 (deferred): Haiku LLM interpretation of pointers → candidates.

Usage:
  python3 scripts/sift.py status
  python3 scripts/sift.py run --lens oaths [--book agot]
  python3 scripts/sift.py sample --lens oaths [--book agot] [-n 20]
  python3 scripts/sift.py interpret --lens oaths   # stub: deferred
  python3 scripts/sift.py backfill-aliases --lens oaths  # stub: deferred

Determinism: a `run` is a pure function of (lens spec, chapter files). Same input →
byte-identical `*.pointers.jsonl`. The corpus is small (~371 files / ~11 MB) and a
full scan is sub-second, so `run` always re-scans every file rather than skipping
unchanged ones — the sha256 manifest is an audit/idempotency record (input + output
hashes), NOT a skip cache. (Per-file skip would mean splicing pointer blocks inside
the aggregated per-book file for zero wall-clock gain; deliberately not built. The
documented escape hatch, if the corpus ever grows past ~2 s, is pyahocorasick.)
"""

import argparse
import bisect
import datetime
import hashlib
import json
import sys
from pathlib import Path
from typing import Optional

import re

PROJECT_ROOT = Path(__file__).parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "sources" / "chapters"
SIFT_WORK_DIR = PROJECT_ROOT / "working" / "sift"
LENSES_DIR = SIFT_WORK_DIR / "lenses"

BOOKS = ["agot", "acok", "asos", "affc", "adwd"]

# 1:1 curly-quote normalization — character offsets stay stable after this
_QUOTE_TABLE = str.maketrans({
    "‘": "'",   # LEFT SINGLE QUOTATION MARK  →  straight apostrophe
    "’": "'",   # RIGHT SINGLE QUOTATION MARK →  straight apostrophe
    "“": '"',   # LEFT DOUBLE QUOTATION MARK  →  straight double
    "”": '"',   # RIGHT DOUBLE QUOTATION MARK →  straight double
})


def normalize_quotes(text: str) -> str:
    """Normalize curly quotes to straight equivalents (1:1, offset-stable)."""
    return text.translate(_QUOTE_TABLE)


class Sift:
    """
    Generic corpus scanner driven by a lens JSON spec.

    Public entry point: run(book=None)
    """

    def __init__(self, lens_path: Path):
        with open(lens_path, encoding="utf-8") as fh:
            self.lens = json.load(fh)

        self.lens_name: str = self.lens["name"]
        self.lens_version = self.lens.get("version", "?")
        snippet_cfg = self.lens.get("snippet", {})
        self.lines_before: int = snippet_cfg.get("lines_before", 2)
        self.lines_after: int = snippet_cfg.get("lines_after", 2)

        # Two hits cluster together when their snippet windows overlap, i.e. they sit
        # within `cluster_gap` lines of each other. Stage 2 reads one cluster as one
        # event (the Night's Watch vow fires 8 triggers on a single line — that is ONE
        # oath, not eight). cluster_id is the correct dedup key; cand_id (which keys on
        # trigger) is not, since co-located hits have *different* triggers.
        self.cluster_gap: int = self.lines_before + self.lines_after

        # Sort triggers longest-first: Python re alternation is first-alternative-wins,
        # so "apple tart" must appear before "apple" in the alternation.
        raw_surfaces = [t["surface"] for t in self.lens["triggers"]]
        self._triggers_sorted = sorted(raw_surfaces, key=lambda s: -len(normalize_quotes(s)))

        # Normalized-lowercase → canonical trigger surface form (for output + coverage report)
        self._norm_to_canonical: dict = {}
        for t in self._triggers_sorted:
            key = normalize_quotes(t).lower()
            if key not in self._norm_to_canonical:
                self._norm_to_canonical[key] = t

        # Build the compiled matcher.
        # Boundaries via lookarounds, NOT blanket \b — \b breaks on multi-word / punctuated triggers.
        alternation = "|".join(re.escape(normalize_quotes(t)) for t in self._triggers_sorted)
        self._matcher = re.compile(
            r"(?<!\w)(?:" + alternation + r")(?!\w)",
            re.IGNORECASE | re.UNICODE,
        )

        # Exclusion patterns (empty until smoke-test-proven noise is identified)
        self._exclusions = [
            re.compile(ex, re.IGNORECASE | re.UNICODE)
            for ex in self.lens.get("exclusions", [])
        ]

        self._out_dir = SIFT_WORK_DIR / self.lens_name
        self._out_dir.mkdir(parents=True, exist_ok=True)
        self._manifest_path = self._out_dir / ".manifest.json"

    # ── internal helpers ──────────────────────────────────────────────────────

    def _load_manifest(self) -> dict:
        if self._manifest_path.exists():
            with open(self._manifest_path, encoding="utf-8") as fh:
                return json.load(fh)
        return {}

    def _save_manifest(self, manifest: dict) -> None:
        with open(self._manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, sort_keys=True)

    @staticmethod
    def _sha256(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    def _book_files(self, book: str) -> list:
        d = CHAPTERS_DIR / book
        if not d.exists():
            return []
        return sorted(d.glob("*.md"))

    def _scan_file(self, path: Path) -> list:
        """Scan one chapter file; return unsorted pointer dicts."""
        text_raw = path.read_text(encoding="utf-8", errors="replace")
        text_norm = normalize_quotes(text_raw)

        # Build cumulative char-offset line-start array (over text_raw; same char lengths).
        # We read the whole file including frontmatter — line numbers are file-absolute.
        lines = text_raw.splitlines(keepends=True)
        line_starts: list = []
        pos = 0
        for line in lines:
            line_starts.append(pos)
            pos += len(line)

        # Parse book name from YAML frontmatter (fallback: parent dir name uppercased)
        book_name = path.parent.name.upper()
        if text_raw.startswith("---"):
            end = text_raw.find("---", 3)
            if end != -1:
                for fm_line in text_raw[3:end].splitlines():
                    stripped = fm_line.strip()
                    if stripped.startswith("book:"):
                        book_name = stripped.split(":", 1)[1].strip()
                        break

        pointers = []
        for m in self._matcher.finditer(text_norm):
            start = m.start()
            matched = m.group()  # substring of text_norm (already quote-normalized)

            # Exclusion check: test a ±200-char context window against exclusion patterns
            if self._exclusions:
                ctx_lo = max(0, start - 200)
                ctx_hi = min(len(text_norm), start + len(matched) + 200)
                ctx = text_norm[ctx_lo:ctx_hi]
                if any(ex.search(ctx) for ex in self._exclusions):
                    continue

            # 1-based line number via bisect into cumulative line_starts
            line_idx = bisect.bisect_right(line_starts, start) - 1
            line_num = line_idx + 1

            # Snippet: ±N lines, clamped at file ends
            snip_lo = max(0, line_idx - self.lines_before)
            snip_hi = min(len(lines), line_idx + self.lines_after + 1)
            snippet = "".join(lines[snip_lo:snip_hi]).rstrip("\n")

            # Map matched text back to canonical trigger (original casing from lens)
            trigger_key = matched.lower()
            canonical = self._norm_to_canonical.get(trigger_key, matched)

            # Stable per-pointer id — match_start makes it unique even for the same
            # trigger twice on one line. Stage 2 may compute its own cand_id on top.
            norm_trigger = normalize_quotes(canonical).lower()
            ptr_id = hashlib.sha1(
                f"{book_name}|{path.name}|{line_num}|{start}|{norm_trigger}".encode("utf-8")
            ).hexdigest()[:12]

            pointers.append({
                "ptr_id": ptr_id,
                "lens": self.lens_name,
                "book": book_name,
                "chapter_file": path.name,
                "line": line_num,
                "match_start": start,
                "trigger": canonical,
                "snippet": snippet,
            })

        return pointers

    def _assign_clusters(self, pointers: list) -> None:
        """Stamp cluster_id / cluster_size onto pointers (already sorted in-place).

        Co-located hits (same chapter, snippet windows overlapping) form one cluster.
        cluster_id = '<chapter_file>:<first_line_of_cluster>' — deterministic + readable.
        """
        prev_file = None
        prev_line = None
        current: list = []
        clusters: list = []
        for p in pointers:
            same_cluster = (
                prev_file == p["chapter_file"]
                and (p["line"] - prev_line) <= self.cluster_gap
            )
            if not same_cluster and current:
                clusters.append(current)
                current = []
            current.append(p)
            prev_file = p["chapter_file"]
            prev_line = p["line"]
        if current:
            clusters.append(current)

        for members in clusters:
            cid = f"{members[0]['chapter_file']}:{members[0]['line']}"
            size = len(members)
            for p in members:
                p["cluster_id"] = cid
                p["cluster_size"] = size

    def _write_coverage(self, book: str, book_label: str, pointers: list) -> Path:
        """Write a machine-readable trigger-coverage report for one book."""
        counts = {t: 0 for t in self._triggers_sorted}
        for p in pointers:
            if p["trigger"] in counts:
                counts[p["trigger"]] += 1
        ordered = sorted(self._triggers_sorted, key=lambda t: (-counts[t], t))
        triggers = [{"surface": t, "hits": counts[t]} for t in ordered if counts[t] > 0]
        zero_hit = [t for t in ordered if counts[t] == 0]
        n_clusters = len({p["cluster_id"] for p in pointers}) if pointers else 0
        cov = {
            "lens": self.lens_name,
            "lens_version": self.lens_version,
            "book": book,
            "book_label": book_label,
            "total_pointers": len(pointers),
            "n_clusters": n_clusters,
            "n_triggers": len(self._triggers_sorted),
            "n_triggered": len(triggers),
            "n_zero_hit": len(zero_hit),
            "triggers": triggers,
            "zero_hit": zero_hit,
        }
        cov_path = self._out_dir / f"{book}.coverage.json"
        with open(cov_path, "w", encoding="utf-8") as fh:
            json.dump(cov, fh, ensure_ascii=False, indent=2)
        return cov_path

    # ── public interface ──────────────────────────────────────────────────────

    def run(self, book: Optional[str] = None) -> None:
        """Stage 1: deterministic Python scan → per-book pointer JSONL files."""
        books = [book] if book else BOOKS
        manifest = self._load_manifest()

        hit_counts: dict = {t: 0 for t in self._triggers_sorted}
        grand_total = 0
        grand_clusters = 0

        for b in books:
            files = self._book_files(b)
            if not files:
                print(f"  {b.upper():5s}  (no chapters found at {CHAPTERS_DIR / b})")
                continue

            book_pointers: list = []
            book_label = b.upper()
            for path in files:
                manifest[str(path.relative_to(PROJECT_ROOT))] = self._sha256(path)
                scanned = self._scan_file(path)
                if scanned:
                    book_label = scanned[0]["book"]
                book_pointers.extend(scanned)

            # Deterministic output sort
            book_pointers.sort(key=lambda p: (
                p["chapter_file"], p["line"], p["match_start"], p["trigger"]
            ))

            # Co-located-hit clustering (post-sort, in place)
            self._assign_clusters(book_pointers)
            n_clusters = len({p["cluster_id"] for p in book_pointers})

            # Tally hits per canonical trigger (grand total, for the stdout report)
            for ptr in book_pointers:
                t = ptr["trigger"]
                if t in hit_counts:
                    hit_counts[t] += 1

            grand_total += len(book_pointers)
            grand_clusters += n_clusters

            # Write JSONL — first line is a mandatory header comment
            out_path = self._out_dir / f"{b}.pointers.jsonl"
            header = (
                f"# SIFT OUTPUT — lens={self.lens_name} — "
                f"NOT the harvest queue. See working/sift/sift-design.md\n"
            )
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(header)
                for ptr in book_pointers:
                    fh.write(json.dumps(ptr, ensure_ascii=False) + "\n")

            # Audit record: hash of the output we just produced
            manifest[str(out_path.relative_to(PROJECT_ROOT))] = self._sha256(out_path)

            # Machine-readable coverage report alongside the pointers
            self._write_coverage(b, book_label, book_pointers)

            print(
                f"  {b.upper():5s}  {len(book_pointers):4d} pointers / "
                f"{n_clusters:3d} clusters → {out_path.relative_to(PROJECT_ROOT)}"
            )

        self._save_manifest(manifest)
        print(f"\nTotal: {grand_total} pointer(s) in {grand_clusters} cluster(s)")

        # Trigger coverage report (hits descending, zero-hits grouped at bottom)
        by_hits = sorted(self._triggers_sorted, key=lambda t: (-hit_counts[t], t))
        zero = [t for t in by_hits if hit_counts[t] == 0]
        nonzero = [t for t in by_hits if hit_counts[t] > 0]

        print(f"\nTrigger coverage ({len(self._triggers_sorted)} triggers):")
        for t in nonzero:
            print(f"  {hit_counts[t]:4d}  {t!r}")
        if zero:
            print(f"\n  Zero-hit triggers ({len(zero)}):")
            for t in zero:
                print(f"    {t!r}")

    def interpret(self, book: Optional[str] = None) -> None:
        """Stage 2 (deferred): Haiku LLM over pointers → candidates."""
        print("Stage 2 (Haiku) is deferred — not implemented")
        sys.exit(0)

    def backfill_aliases(self) -> None:
        """Alias backfill (deferred): write surface forms into node aliases:."""
        print("deferred")
        sys.exit(0)


# ── sample (read pointers → stratified preview, no lens compile) ────────────────

def _load_pointers(lens_name: str, book: Optional[str]) -> list:
    out_dir = SIFT_WORK_DIR / lens_name
    books = [book] if book else BOOKS
    rows = []
    for b in books:
        p = out_dir / f"{b}.pointers.jsonl"
        if not p.exists():
            continue
        with open(p, encoding="utf-8") as fh:
            for ln in fh:
                ln = ln.strip()
                if not ln or ln.startswith("#"):
                    continue
                rows.append(json.loads(ln))
    return rows


def _sample(lens_name: str, book: Optional[str], n: int) -> None:
    """Print a deterministic, trigger-stratified preview of existing pointers.

    Round-robins across distinct triggers so the sample spans the lexicon rather than
    over-representing the loudest trigger. Reproducible: same pointers → same sample.
    """
    rows = _load_pointers(lens_name, book)
    if not rows:
        scope = f" --book {book}" if book else ""
        print(f"No pointers found for lens '{lens_name}'{scope}. Run 'sift run' first.")
        return

    # Bucket by trigger, preserving deterministic order within each bucket
    rows.sort(key=lambda r: (r["trigger"], r["chapter_file"], r["line"], r["match_start"]))
    buckets: dict = {}
    for r in rows:
        buckets.setdefault(r["trigger"], []).append(r)

    # Round-robin: one row per distinct trigger per pass, until we have n
    order = sorted(buckets.keys())
    picked = []
    idx = 0
    while len(picked) < n and any(buckets[t] for t in order):
        t = order[idx % len(order)]
        if buckets[t]:
            picked.append(buckets[t].pop(0))
        idx += 1
        if idx > len(order) * (n + 1):  # safety against infinite loop
            break

    scope = book.upper() if book else "ALL"
    print(f"Sample — lens={lens_name} book={scope}  ({len(picked)} of {len(rows)} pointers)\n")
    for r in picked:
        snippet = " ".join(r["snippet"].split())
        excerpt = snippet[:140] + ("…" if len(snippet) > 140 else "")
        loc = f"{r['chapter_file']}:{r['line']}"
        csz = r.get("cluster_size", 1)
        cflag = f"  [cluster×{csz}]" if csz > 1 else ""
        print(f"• {r['trigger']!r:42s} {loc}{cflag}")
        print(f"    {excerpt}")


# ── status (no lens required) ─────────────────────────────────────────────────

def _status() -> None:
    """Print lenses present, last run timestamp, pointer counts per lens/book."""
    print("Sift status")
    print(f"  Lenses dir: {LENSES_DIR.relative_to(PROJECT_ROOT)}")
    lens_files = sorted(LENSES_DIR.glob("*.lens.json"))
    if not lens_files:
        print("  No lenses found.")
        return

    for lf in lens_files:
        with open(lf, encoding="utf-8") as fh:
            lens_data = json.load(fh)
        name = lens_data["name"]
        n_triggers = len(lens_data.get("triggers", []))
        n_excl = len(lens_data.get("exclusions", []))
        print(f"\n  Lens: {name}  (v{lens_data.get('version', '?')})")
        print(f"    Triggers:   {n_triggers}")
        print(f"    Exclusions: {n_excl}")
        out_dir = SIFT_WORK_DIR / name
        for b in BOOKS:
            out_path = out_dir / f"{b}.pointers.jsonl"
            if out_path.exists():
                with open(out_path, encoding="utf-8") as fh:
                    rows = [json.loads(ln) for ln in fh if ln.strip() and not ln.startswith("#")]
                count = len(rows)
                n_clusters = len({r.get("cluster_id", r["ptr_id"]) for r in rows}) if rows else 0
                mtime = out_path.stat().st_mtime
                dt = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                print(f"    {b.upper():5s}  {count:4d} pointers / {n_clusters:3d} clusters  (last run: {dt})")
            else:
                print(f"    {b.upper():5s}  not run")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sift.py",
        description="The Sift — Weirwood Network corpus scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    # status
    sub.add_parser("status", help="Lenses present, last run, pointer counts")

    # run
    run_p = sub.add_parser("run", help="Stage 1: Python scan → pointers JSONL (safe, additive)")
    run_p.add_argument("--lens", required=True, help="Lens name (e.g. oaths)")
    run_p.add_argument("--book", help="Book code (agot/acok/asos/affc/adwd); omit for all books")

    # sample
    smp_p = sub.add_parser("sample", help="Print a stratified preview of existing pointers")
    smp_p.add_argument("--lens", required=True, help="Lens name (e.g. oaths)")
    smp_p.add_argument("--book", help="Book filter; omit for all books")
    smp_p.add_argument("-n", "--num", type=int, default=20, help="Number of rows (default 20)")

    # interpret (stub)
    int_p = sub.add_parser("interpret", help="Stage 2: Haiku → candidates (deferred)")
    int_p.add_argument("--lens", required=True)
    int_p.add_argument("--book", help="Book filter")

    # backfill-aliases (stub)
    ba_p = sub.add_parser("backfill-aliases", help="Write surface forms into node aliases (deferred)")
    ba_p.add_argument("--lens", required=True)

    args = parser.parse_args()

    if args.command in (None, "status"):
        _status()
        return

    if args.command == "sample":
        book = args.book.lower() if args.book else None
        _sample(args.lens, book, args.num)
        return

    # All other commands need a lens file
    lens_path = LENSES_DIR / f"{args.lens}.lens.json"
    if not lens_path.exists():
        print(f"ERROR: lens file not found: {lens_path}", file=sys.stderr)
        sys.exit(1)

    sift = Sift(lens_path)

    if args.command == "run":
        book = args.book.lower() if args.book else None
        sift.run(book=book)

    elif args.command == "interpret":
        book = args.book.lower() if getattr(args, "book", None) else None
        sift.interpret(book=book)

    elif args.command == "backfill-aliases":
        sift.backfill_aliases()


if __name__ == "__main__":
    main()
