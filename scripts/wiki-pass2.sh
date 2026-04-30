#!/usr/bin/env bash
# wiki-pass2.sh — Wiki Pass 2 launcher for the Weirwood Network project
#
# Orchestrates agentic wiki ingestion (Pass 2): wiki pages → graph/nodes/*.node.md
#
# Subcommands:
#   triage [--accept]                   Draft or commit per-bucket manifests
#   run <tier> [--wave N] [--bucket B]  Process buckets atomically via agent
#   launch <tier> [-t N -w N]           Open iTerm tabs for parallel processing
#   status [tier]                       ASCII table of bucket progress
#   check                               Cross-bucket coherence check
#   reset --version vN [--archive-dir PATH] [--dry-run]
#   unstick <bucket> [--force]          Clear orphaned in-progress bucket
#   questions [--unresolved|--bucket B|--type T]  Query question queue
#   stop                                Create soft-stop marker
#
# Mirrors extract.sh conventions: wave-based concurrency, soft-stop file,
# atomic tmp/ → graph/nodes/ promotion, CSV stats, worklog updates.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# ── Constants ──────────────────────────────────────────────────────────────────

STATS_DIR="working/extraction-stats"
WORKLOG_FILE="worklog.md"
WIKI_STATE_DIR="working/wiki-pass2"
TRIAGE_MANIFEST="working/wiki-parsed/triage-manifest.jsonl"
STOP_FILE="/tmp/wiki-pass2-stop"
WAVE_SIZE=4          # 3-5 buckets per wave (default 4)
VERSION="v1"
DEFAULT_ORPHAN_THRESHOLD=60  # minutes

# Status code values (referenced in documentation)
# pending | in-progress | ok | fail | skip-done | skip-rate-limit |
# validation-failed | partial | version-stale

# Graph node parent-type to directory mapping (from runbook §5.1)
declare -A TYPE_DIR_MAP=(
  ["character"]="characters"
  ["place"]="locations"
  ["organization.house"]="houses"
  ["organization.faction"]="factions"
  ["organization.religion"]="religions"
  ["organization"]="factions"
  ["concept"]="concepts"
  ["object"]="artifacts"
  ["event"]="events"
  ["species"]="species"
  ["title"]="titles"
  ["prophecy"]="prophecies"
  ["theory"]="theories"
  ["text"]="texts"
  ["battle"]="battles"
  ["war"]="wars"
)

# ── Helpers ────────────────────────────────────────────────────────────────────

format_duration() {
  local secs=$1
  local h=$(( secs / 3600 )) m=$(( (secs % 3600) / 60 )) s=$(( secs % 60 ))
  if (( h > 0 )); then printf "%dh %dm %ds" "$h" "$m" "$s"
  elif (( m > 0 )); then printf "%dm %ds" "$m" "$s"
  else printf "%ds" "$s"; fi
}

# Resolve the graph/nodes/ subdirectory for a given type string.
# Takes the type from node frontmatter (e.g. "character.human", "organization.house")
# Returns the directory path relative to REPO_ROOT.
resolve_node_dir() {
  local type_str="$1"
  # Try most-specific match first
  if [[ -n "${TYPE_DIR_MAP[$type_str]:-}" ]]; then
    echo "graph/nodes/${TYPE_DIR_MAP[$type_str]}"
    return
  fi
  # Try parent type (prefix before first dot)
  local parent="${type_str%%.*}"
  if [[ -n "${TYPE_DIR_MAP[$parent]:-}" ]]; then
    echo "graph/nodes/${TYPE_DIR_MAP[$parent]}"
    return
  fi
  # Fallback: uncategorized
  echo "graph/nodes/characters"
}

# Read a field from a manifest JSON file
manifest_get() {
  local manifest="$1" field="$2"
  python3 -c "
import json, sys
with open('$manifest') as f:
    d = json.load(f)
print(d.get('$field', ''))
" 2>/dev/null || echo ""
}

# Write a single field to a manifest JSON file (in-place)
manifest_set() {
  local manifest="$1" field="$2" value="$3"
  python3 -c "
import json
with open('$manifest') as f:
    d = json.load(f)
d['$field'] = '$value'
with open('$manifest', 'w') as f:
    json.dump(d, f, indent=2)
" 2>/dev/null
}

# List all bucket manifest paths, sorted by tier then bucket_id
list_manifests() {
  local tier_filter="${1:-}"
  if [[ -z "$tier_filter" ]]; then
    find "$WIKI_STATE_DIR" -name "manifest.json" 2>/dev/null | sort
  else
    find "$WIKI_STATE_DIR" -name "manifest.json" 2>/dev/null | while read -r m; do
      local t
      t=$(manifest_get "$m" "tier")
      [[ "$t" == "$tier_filter" ]] && echo "$m"
    done | sort
  fi
}

# Get the stats CSV path for a tier+version
stats_file_for() {
  local tier="$1"
  echo "${STATS_DIR}/wiki-pass2-stats-${tier}-${VERSION}.csv"
}

# Ensure a stats CSV exists with the correct header.
# First 13 columns are BYTE-IDENTICAL to extraction-stats-{book}-pass1-v3.csv.
# The column names are adapted: chapter→bucket, book→tier.
ensure_stats_csv() {
  local tier="$1"
  local sf
  sf=$(stats_file_for "$tier")
  mkdir -p "$STATS_DIR"
  if [[ ! -f "$sf" ]]; then
    echo "bucket,tier,wave,status,start_time,end_time,duration_s,input_tokens,cache_creation_tokens,cache_read_tokens,output_tokens,total_tokens,cost_usd,pages_in_bucket,nodes_emitted,validation_status,notes,questions_filed,conflicts_filed,pass1_contradictions_filed" > "$sf"
  fi
}

# Append a row to the stats CSV
append_stats_row() {
  local tier="$1"
  local bucket="$2" wave="$3" status="$4" start_time="$5" end_time="$6" \
        duration_s="$7" input_tokens="$8" cache_creation_tokens="$9" \
        cache_read_tokens="${10}" output_tokens="${11}" total_tokens="${12}" \
        cost_usd="${13}" pages_in_bucket="${14}" nodes_emitted="${15}" \
        validation_status="${16}" notes="${17}" \
        questions_filed="${18:-0}" conflicts_filed="${19:-0}" \
        pass1_contradictions_filed="${20:-0}"
  local sf
  sf=$(stats_file_for "$tier")
  echo "${bucket},${tier},${wave},${status},${start_time},${end_time},${duration_s},${input_tokens},${cache_creation_tokens},${cache_read_tokens},${output_tokens},${total_tokens},${cost_usd},${pages_in_bucket},${nodes_emitted},${validation_status},${notes},${questions_filed},${conflicts_filed},${pass1_contradictions_filed}" >> "$sf"
}

# Count lines in a JSONL file (returns 0 if file doesn't exist).
jsonl_linecount() {
  local f="$1"
  if [[ -f "$f" ]]; then
    wc -l < "$f" | tr -d ' '
  else
    echo 0
  fi
}

# Update worklog.md checklist lines for wiki pass 2 progress
update_worklog() {
  local tier="$1"

  local done=0 total=0
  while IFS= read -r mf; do
    [[ -z "$mf" ]] && continue
    total=$(( total + 1 ))
    local st
    st=$(manifest_get "$mf" "status")
    [[ "$st" == "complete" || "$st" == "ok" ]] && done=$(( done + 1 ))
  done < <(list_manifests "$tier")

  local new_line
  if (( total > 0 && done == total )); then
    new_line="- [x] Wiki Pass 2 ${VERSION} — ${tier} (${done}/${total} buckets)"
  else
    new_line="- [ ] Wiki Pass 2 ${VERSION} — ${tier} (${done}/${total} buckets)"
  fi

  local tier_pattern="Wiki Pass 2 ${VERSION} — ${tier}"
  if grep -q "$tier_pattern" "$WORKLOG_FILE" 2>/dev/null; then
    sed -i '' "s|^- \[.\] ${tier_pattern}.*|${new_line}|" "$WORKLOG_FILE"
    echo "Updated worklog: ${new_line}"
  else
    echo "Note: no worklog line found for '${tier_pattern}' — add it to worklog.md to enable tracking."
  fi
}

# ── Reconciliation pass ────────────────────────────────────────────────────────
# Per runbook §5.1.1: walk every complete manifest, verify expected_nodes on disk.
# Filesystem is canonical. Downgrades manifests that diverge from disk state.

run_reconciliation() {
  local downgraded=0 version_stale=0 skipped=0

  while IFS= read -r mf; do
    [[ -z "$mf" ]] && continue
    local status
    status=$(manifest_get "$mf" "status")
    [[ "$status" != "complete" ]] && continue

    # Check fingerprint match (prompt_version)
    local mf_prompt_ver
    mf_prompt_ver=$(manifest_get "$mf" "prompt_version")

    # Get expected_nodes list
    local missing_count=0
    while IFS= read -r node_file; do
      [[ -z "$node_file" ]] && continue
      # expected_nodes contains bare filenames; find them under graph/nodes/
      local found=false
      while IFS= read -r candidate; do
        [[ "$candidate" == *"/$node_file" ]] && { found=true; break; }
      done < <(find "graph/nodes" -name "$node_file" 2>/dev/null)
      [[ "$found" == false ]] && missing_count=$(( missing_count + 1 ))
    done < <(python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
for n in d.get('expected_nodes', []):
    print(n)
" 2>/dev/null)

    if (( missing_count > 0 )); then
      manifest_set "$mf" "status" "partial"
      echo "  Reconciliation: $(basename "$(dirname "$mf")") → partial (${missing_count} missing nodes)"
      downgraded=$(( downgraded + 1 ))
    fi
  done < <(list_manifests)

  if (( downgraded > 0 || version_stale > 0 )); then
    echo "Reconciliation: ${downgraded} downgraded to partial, ${version_stale} version-stale, ${skipped} ok"
  fi
}

# ── Orphan recovery ────────────────────────────────────────────────────────────
# Per runbook §5.4: in-progress manifests older than threshold → reset to pending.

run_orphan_recovery() {
  local threshold_min="${1:-$DEFAULT_ORPHAN_THRESHOLD}"
  local now
  now=$(date +%s)
  local recovered=0

  while IFS= read -r mf; do
    [[ -z "$mf" ]] && continue
    local status
    status=$(manifest_get "$mf" "status")
    [[ "$status" != "in-progress" ]] && continue

    local started_at
    started_at=$(manifest_get "$mf" "started_at")
    [[ -z "$started_at" || "$started_at" == "null" ]] && {
      # No start time — reset it
      manifest_set "$mf" "status" "pending"
      recovered=$(( recovered + 1 ))
      continue
    }

    local started_epoch
    started_epoch=$(python3 -c "
from datetime import datetime
try:
    dt = datetime.fromisoformat('$started_at')
    import calendar, time
    print(int(dt.timestamp()))
except:
    print(0)
" 2>/dev/null || echo 0)

    local age_min=$(( (now - started_epoch) / 60 ))
    if (( age_min > threshold_min )); then
      local bucket_dir
      bucket_dir="$(dirname "$mf")"
      # Wipe tmp/
      rm -rf "${bucket_dir}/tmp"
      mkdir -p "${bucket_dir}/tmp"
      manifest_set "$mf" "status" "pending"
      echo "  Orphan recovery: $(basename "$bucket_dir") (age=${age_min}min > threshold=${threshold_min}min) → pending"
      recovered=$(( recovered + 1 ))
    else
      echo "  Skipping in-progress $(basename "$(dirname "$mf")") (age=${age_min}min < threshold=${threshold_min}min — another tab may own it)"
    fi
  done < <(list_manifests)

  # Use if-block (not `&&` chain) so the function always returns 0 under set -e.
  # `(( recovered > 0 )) && echo ...` returns 1 when recovered==0, killing cmd_run.
  if (( recovered > 0 )); then
    echo "Orphan recovery: ${recovered} bucket(s) reset to pending"
  fi
}

# ── Compose bucket_input.json ──────────────────────────────────────────────────
# Per runbook §2.1.1. Combines triage data, Track B rows, page-index rows,
# and Pass 1 mentions for each page in the bucket.

compose_bucket_input() {
  local bucket_dir="$1"
  local manifest="${bucket_dir}/manifest.json"
  local output="${bucket_dir}/bucket_input.json"

  python3 - "$manifest" "$output" <<'PYEOF'
import json, sys, os, re

manifest_path = sys.argv[1]
output_path = sys.argv[2]
repo_root = os.getcwd()

with open(manifest_path) as f:
    manifest = json.load(f)

bucket_id = manifest.get("bucket_id", "")
tier = manifest.get("tier", "")
tier_default = manifest.get("tier_default", "tier-2")
prompt_version = manifest.get("prompt_version", "v1")
chunk_strategy = manifest.get("chunk_strategy", "single-pass")
input_pages = manifest.get("input_pages", [])

# Load Track B data if available
infobox_data = {}
infobox_path = os.path.join(repo_root, "working/wiki-parsed/infobox-data.jsonl")
if os.path.exists(infobox_path):
    with open(infobox_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                page = row.get("page", "")
                if page:
                    infobox_data[page] = row
            except Exception:
                pass

# Load page-index data if available
page_index = {}
page_index_path = os.path.join(repo_root, "working/wiki-parsed/page-index.jsonl")
if os.path.exists(page_index_path):
    with open(page_index_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                page = row.get("page", "")
                if page:
                    page_index[page] = row
            except Exception:
                pass

# Find Pass 1 mentions for pages in this bucket (cheap grep over extractions/)
pass1_mentions_map = {}
extractions_dir = os.path.join(repo_root, "extractions/mechanical")
if os.path.exists(extractions_dir):
    for book_dir in os.listdir(extractions_dir):
        book_path = os.path.join(extractions_dir, book_dir)
        if not os.path.isdir(book_path):
            continue
        for ext_file in os.listdir(book_path):
            if not ext_file.endswith(".extraction.md"):
                continue
            ch_name = ext_file.replace(".extraction.md", "")
            ext_path = os.path.join(book_path, ext_file)
            try:
                with open(ext_path) as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    for page in input_pages:
                        # Normalize page name for matching (Eddard_Stark → Eddard Stark)
                        page_norm = page.replace("_", " ")
                        if page_norm in line or page in line:
                            if page not in pass1_mentions_map:
                                pass1_mentions_map[page] = []
                            context_start = max(0, i - 1)
                            context_end = min(len(lines), i + 2)
                            context = "".join(lines[context_start:context_end]).strip()
                            pass1_mentions_map[page].append({
                                "chapter": ch_name,
                                "line": i + 1,
                                "context": context[:200]
                            })
            except Exception:
                pass

# Build page entries
pages = []
for page in input_pages:
    # Wiki cache filenames use underscores (Grey_Wind.json), but page names
    # are space-form (Grey Wind). Normalize before path lookup. (B1 fix)
    page_filename = page.replace(" ", "_")
    raw_html_path = f"sources/wiki/_raw/{page_filename}.json"
    if not os.path.exists(os.path.join(repo_root, raw_html_path)):
        # Try _uncategorized
        raw_html_path = f"sources/wiki/_uncategorized/{page_filename}.json"
        if not os.path.exists(os.path.join(repo_root, raw_html_path)):
            raw_html_path = None

    entry = {
        "page": page,
        "raw_html_path": raw_html_path,
        "track_b_row": infobox_data.get(page, {}),
        "page_index_row": page_index.get(page, {}),
        "pass1_mentions": pass1_mentions_map.get(page, [])
    }
    pages.append(entry)

bundle = {
    "bucket_id": bucket_id,
    "tier": tier,
    "tier_default": tier_default,
    "prompt_version": prompt_version,
    "chunk_strategy": chunk_strategy,
    "pages": pages
}

with open(output_path, "w") as f:
    json.dump(bundle, f, indent=2)

print(f"  Composed bucket_input.json: {len(pages)} pages")
PYEOF
}

# ── CMD: triage ───────────────────────────────────────────────────────────────

cmd_triage() {
  local accept=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --accept) accept=true; shift ;;
      --help|-h) echo "Usage: wiki-pass2.sh triage [--accept]"; return 0 ;;
      *) echo "Unknown option: $1" >&2; return 1 ;;
    esac
  done

  if [[ ! -f "scripts/wiki-pass2-triage.py" ]]; then
    echo "ERROR: scripts/wiki-pass2-triage.py not found." >&2
    echo "  The triage script must be built before running triage." >&2
    return 1
  fi

  if $accept; then
    echo "Running triage with --accept (will commit per-bucket manifests)..."
    python3 scripts/wiki-pass2-triage.py --accept
  else
    echo "Running triage (draft only — use --accept to commit manifests)..."
    python3 scripts/wiki-pass2-triage.py
  fi
}

# ── CMD: run ──────────────────────────────────────────────────────────────────

cmd_run() {
  local tier="" wave="" bucket_filter="" orphan_threshold="$DEFAULT_ORPHAN_THRESHOLD"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --wave|-w)               wave="$2";              shift 2 ;;
      --bucket|-b)             bucket_filter="$2";     shift 2 ;;
      --orphan-threshold-min)  orphan_threshold="$2";  shift 2 ;;
      --help|-h)
        echo "Usage: wiki-pass2.sh run <tier> [--wave N] [--bucket <id>] [--orphan-threshold-min N]"
        return 0
        ;;
      -*)  echo "Unknown option: $1" >&2; return 1 ;;
      *)   tier="$1"; shift ;;
    esac
  done

  if [[ -z "$tier" ]]; then
    echo "ERROR: tier is required (core|secondary)" >&2
    return 1
  fi

  # Check that triage manifests exist
  if [[ ! -d "$WIKI_STATE_DIR" ]] || [[ -z "$(find "$WIKI_STATE_DIR" -name "manifest.json" -maxdepth 2 -print -quit 2>/dev/null)" ]]; then
    echo "No triage manifest found — run \`weirwood wiki triage\` first"
    return 0
  fi

  # Reconciliation and orphan recovery
  echo "--- Reconciliation pass ---"
  run_reconciliation
  echo "--- Orphan recovery (threshold=${orphan_threshold}min) ---"
  run_orphan_recovery "$orphan_threshold"

  # Clear stop file
  rm -f "$STOP_FILE"

  ensure_stats_csv "$tier"

  # Collect pending/partial buckets for this tier
  local -a pending_manifests=()
  while IFS= read -r mf; do
    [[ -z "$mf" ]] && continue
    local status
    status=$(manifest_get "$mf" "status")
    case "$status" in
      pending|partial|fail|validation-failed|version-stale) ;;
      *) continue ;;
    esac
    # If bucket filter specified, only run that bucket
    if [[ -n "$bucket_filter" ]]; then
      local bid
      bid=$(manifest_get "$mf" "bucket_id")
      [[ "$bid" != "$bucket_filter" ]] && continue
    fi
    pending_manifests+=("$mf")
  done < <(list_manifests "$tier")

  if (( ${#pending_manifests[@]} == 0 )); then
    echo "No pending buckets found for tier '${tier}'. All done or use --bucket to target one specifically."
    return 0
  fi

  # Determine wave slice
  local start=0 end=${#pending_manifests[@]}
  if [[ -n "$wave" ]]; then
    start=$(( (wave - 1) * WAVE_SIZE ))
    end=$(( start + WAVE_SIZE ))
    (( end > ${#pending_manifests[@]} )) && end=${#pending_manifests[@]}
    if (( start >= ${#pending_manifests[@]} )); then
      echo "Wave $wave is out of range for tier ${tier}"
      return 1
    fi
    echo "=== Wiki Pass 2 — ${tier^^} Wave ${wave}: buckets $((start+1))-${end} of ${#pending_manifests[@]} pending ==="
  else
    echo "=== Wiki Pass 2 — ${tier^^}: processing all ${#pending_manifests[@]} pending buckets ==="
  fi

  local -a wave_manifests=("${pending_manifests[@]:$start:$((end - start))}")

  local wave_start successes=0 failures=0
  local total_q_filed=0 total_c_filed=0 total_p_filed=0
  local buckets_with_questions=0
  local q_file="${WIKI_STATE_DIR}/questions-for-matt.jsonl"
  local c_file="${WIKI_STATE_DIR}/conflicts.jsonl"
  local p_file="${WIKI_STATE_DIR}/pass1-contradictions.jsonl"
  wave_start=$(date +%s)

  for mf in "${wave_manifests[@]}"; do
    # Soft-stop check
    if [[ -f "$STOP_FILE" ]]; then
      echo ""
      echo "Stop file detected — halting before next bucket. Remaining buckets will run on next launch."
      break
    fi

    local bucket_dir
    bucket_dir="$(dirname "$mf")"
    local bucket_id
    bucket_id=$(manifest_get "$mf" "bucket_id")
    local pages_count
    pages_count=$(python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
print(len(d.get('input_pages', [])))
" 2>/dev/null || echo 0)

    echo ""
    echo "--- Processing bucket: ${bucket_id} (${pages_count} pages) ---"

    # Snapshot structured-channel sizes before this bucket runs.
    # Delta after the agent completes = entries this bucket contributed.
    # (questions / conflicts carry bucket_id in their schema; pass1-contradictions
    # is keyed by node slug, so we use total-line delta as a coarse signal.)
    local q_before c_before p_before
    q_before=$(jsonl_linecount "$q_file")
    c_before=$(jsonl_linecount "$c_file")
    p_before=$(jsonl_linecount "$p_file")

    # Read prior status BEFORE flipping to in-progress; used to decide
    # whether to wipe stale tmp/ contents from a previous failed run.
    local prior_status
    prior_status=$(manifest_get "$mf" "status")

    # Mark in-progress
    local started_at
    started_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
d['status'] = 'in-progress'
d['started_at'] = '$started_at'
with open('$mf', 'w') as f:
    json.dump(d, f, indent=2)
"

    # Prepare tmp/ directory. Wipe stale contents when retrying a previously
    # failed bucket so the agent starts on a blank canvas (otherwise leftover
    # node files from the prior run can pollute validation).
    if [[ "$prior_status" == "fail" || "$prior_status" == "validation-failed" ]]; then
      if [[ -d "${bucket_dir}/tmp" ]]; then
        echo "  Wiping stale tmp/ from prior ${prior_status} run..."
        rm -rf "${bucket_dir}/tmp"
      fi
    fi
    mkdir -p "${bucket_dir}/tmp"

    # Compose bucket_input.json
    echo "  Composing bucket_input.json..."
    if ! compose_bucket_input "$bucket_dir"; then
      echo "  ERROR: failed to compose bucket_input.json" >&2
      manifest_set "$mf" "status" "fail"
      failures=$(( failures + 1 ))
      append_stats_row "$tier" "$bucket_id" "${wave:-1}" "fail" "$started_at" \
        "$(date '+%Y-%m-%d %H:%M:%S')" "0" "0" "0" "0" "0" "0" "0" \
        "$pages_count" "0" "fail" "bucket_input composition failed" \
        "0" "0" "0"
      continue
    fi

    # Invoke agent (wiki-ingester)
    local logfile="/tmp/wiki-pass2-${bucket_id}.log"
    local jsonfile="/tmp/wiki-pass2-${bucket_id}.json"
    local ch_start ch_start_fmt
    ch_start=$(date +%s)
    ch_start_fmt=$(date '+%Y-%m-%d %H:%M:%S')

    local agent_prompt="You are the wiki-ingester agent for the Weirwood Network project.

Read .claude/agents/wiki-ingester.md for your full schema and rules.
Read the bucket input file: ${bucket_dir}/bucket_input.json

Process each page in the bucket and write *.node.md files to: ${bucket_dir}/tmp/

Follow the schema exactly. Do not modify any files outside ${bucket_dir}/tmp/."

    local agent_status
    if claude -p --dangerously-skip-permissions --model claude-opus-4-6 --verbose \
         --output-format stream-json "$agent_prompt" > "$jsonfile" 2>&1; then
      agent_status="ok"
    else
      agent_status="fail"
    fi

    local ch_end ch_end_fmt elapsed
    ch_end=$(date +%s)
    ch_end_fmt=$(date '+%Y-%m-%d %H:%M:%S')
    elapsed=$(( ch_end - ch_start ))

    # Parse token usage
    local INPUT_TOKENS=0 CACHE_CREATION=0 CACHE_READ=0 OUTPUT_TOKENS=0 COST_USD=0
    eval "$(python3 -c "
import json
found = False
for line in open('$jsonfile'):
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if obj.get('type') == 'result' and not found:
            found = True
            u = obj.get('usage', {})
            print(f'INPUT_TOKENS={u.get(\"input_tokens\", 0)}')
            print(f'CACHE_CREATION={u.get(\"cache_creation_input_tokens\", 0)}')
            print(f'CACHE_READ={u.get(\"cache_read_input_tokens\", 0)}')
            print(f'OUTPUT_TOKENS={u.get(\"output_tokens\", 0)}')
            print(f'COST_USD={obj.get(\"total_cost_usd\", 0)}')
    except: pass
if not found:
    print('INPUT_TOKENS=0'); print('CACHE_CREATION=0'); print('CACHE_READ=0')
    print('OUTPUT_TOKENS=0'); print('COST_USD=0')
" 2>/dev/null)"
    local total_tokens=$(( INPUT_TOKENS + CACHE_CREATION + CACHE_READ + OUTPUT_TOKENS ))

    # Extract readable log
    python3 -c "
import json
for line in open('$jsonfile'):
    line = line.strip()
    if not line: continue
    try:
        obj = json.loads(line)
        if obj.get('type') == 'assistant' and 'message' in obj:
            for block in obj['message'].get('content', []):
                if block.get('type') == 'text': print(block['text'])
    except: pass
" > "$logfile" 2>/dev/null || true

    # Check for rate limit
    local rate_limited=false
    if grep -q '"status":"rejected"' "$jsonfile" 2>/dev/null && \
       grep -q '"rateLimitType"' "$jsonfile" 2>/dev/null; then
      rate_limited=true
    fi

    if [[ "$agent_status" != "ok" ]]; then
      echo "  ERROR: agent failed for bucket ${bucket_id} (${elapsed}s)"
      manifest_set "$mf" "status" "fail"
      failures=$(( failures + 1 ))

      # Save failure log
      mkdir -p "${WIKI_STATE_DIR}/failures"
      local ts_safe
      ts_safe=$(date '+%Y-%m-%dT%H-%M-%S')
      cp "$logfile" "${WIKI_STATE_DIR}/failures/${bucket_id}-${ts_safe}.log" 2>/dev/null || true

      # Compute structured-channel deltas (agent may have filed entries even on failure).
      local q_filed c_filed p_filed
      q_filed=$(( $(jsonl_linecount "$q_file") - q_before ))
      c_filed=$(( $(jsonl_linecount "$c_file") - c_before ))
      p_filed=$(( $(jsonl_linecount "$p_file") - p_before ))
      total_q_filed=$(( total_q_filed + q_filed ))
      total_c_filed=$(( total_c_filed + c_filed ))
      total_p_filed=$(( total_p_filed + p_filed ))
      (( q_filed > 0 )) && buckets_with_questions=$(( buckets_with_questions + 1 ))

      if [[ "$rate_limited" == true ]]; then
        echo ""
        echo "  RATE LIMIT hit — halting wave."
        append_stats_row "$tier" "$bucket_id" "${wave:-1}" "skip-rate-limit" \
          "$ch_start_fmt" "$ch_end_fmt" "$elapsed" \
          "$INPUT_TOKENS" "$CACHE_CREATION" "$CACHE_READ" "$OUTPUT_TOKENS" "$total_tokens" "$COST_USD" \
          "$pages_count" "0" "fail" "rate-limit" \
          "$q_filed" "$c_filed" "$p_filed"
        break
      fi

      append_stats_row "$tier" "$bucket_id" "${wave:-1}" "fail" \
        "$ch_start_fmt" "$ch_end_fmt" "$elapsed" \
        "$INPUT_TOKENS" "$CACHE_CREATION" "$CACHE_READ" "$OUTPUT_TOKENS" "$total_tokens" "$COST_USD" \
        "$pages_count" "0" "fail" "agent error" \
        "$q_filed" "$c_filed" "$p_filed"
      continue
    fi

    # Count emitted nodes in tmp/
    local nodes_emitted
    nodes_emitted=$(find "${bucket_dir}/tmp" -name "*.node.md" 2>/dev/null | wc -l | tr -d ' ')

    # Run validator
    local validation_ok=false
    local validator_notes="no validator script"
    if [[ -f "scripts/wiki-pass2-validator.py" ]]; then
      local validator_output="${bucket_dir}/validator-report.json"
      if python3 scripts/wiki-pass2-validator.py \
           --bucket-dir "${bucket_dir}" \
           --output "$validator_output" 2>/dev/null; then
        validation_ok=true
        validator_notes="pass"
        manifest_set "$mf" "validation_report" "$validator_output"
      else
        validator_notes="validation-failed"
        echo "  Validator FAILED for bucket ${bucket_id} — output held in tmp/"
        manifest_set "$mf" "validation_report" "$validator_output"
        manifest_set "$mf" "status" "validation-failed"
        mkdir -p "${WIKI_STATE_DIR}/failures"
        local ts_safe
        ts_safe=$(date '+%Y-%m-%dT%H-%M-%S')
        cp "$logfile" "${WIKI_STATE_DIR}/failures/${bucket_id}-${ts_safe}.log" 2>/dev/null || true
        local q_filed c_filed p_filed
        q_filed=$(( $(jsonl_linecount "$q_file") - q_before ))
        c_filed=$(( $(jsonl_linecount "$c_file") - c_before ))
        p_filed=$(( $(jsonl_linecount "$p_file") - p_before ))
        total_q_filed=$(( total_q_filed + q_filed ))
        total_c_filed=$(( total_c_filed + c_filed ))
        total_p_filed=$(( total_p_filed + p_filed ))
        (( q_filed > 0 )) && buckets_with_questions=$(( buckets_with_questions + 1 ))
        append_stats_row "$tier" "$bucket_id" "${wave:-1}" "validation-failed" \
          "$ch_start_fmt" "$ch_end_fmt" "$elapsed" \
          "$INPUT_TOKENS" "$CACHE_CREATION" "$CACHE_READ" "$OUTPUT_TOKENS" "$total_tokens" "$COST_USD" \
          "$pages_count" "$nodes_emitted" "fail" "validator rejected output" \
          "$q_filed" "$c_filed" "$p_filed"
        failures=$(( failures + 1 ))
        continue
      fi
    else
      # No validator yet — allow promotion but note it
      validation_ok=true
      validator_notes="no-validator"
      echo "  WARNING: scripts/wiki-pass2-validator.py not found — skipping validation"
    fi

    # Atomic promotion: tmp/*.node.md → graph/nodes/<type>/
    # Per §6.5: no overwrite unless fingerprint+byte-equivalent match
    local promoted=0 conflicted=0
    while IFS= read -r node_file; do
      [[ -z "$node_file" ]] && continue
      local node_name
      node_name=$(basename "$node_file")

      # Read type from frontmatter
      local node_type
      node_type=$(python3 -c "
import re, sys
with open('$node_file') as f:
    content = f.read()
m = re.search(r'^type:\s*(.+)$', content, re.MULTILINE)
print(m.group(1).strip() if m else 'character')
" 2>/dev/null || echo "character")

      local dest_dir
      dest_dir=$(resolve_node_dir "$node_type")
      mkdir -p "$dest_dir"
      local dest_path="${dest_dir}/${node_name}"

      if [[ ! -f "$dest_path" ]]; then
        # Normal promotion
        mv "$node_file" "$dest_path"
        promoted=$(( promoted + 1 ))
      else
        # Destination exists — check byte-equivalence
        if cmp -s "$node_file" "$dest_path"; then
          # Byte-identical: skip silently
          rm "$node_file"
        else
          # Conflict: write to _conflicts/, log it
          mkdir -p "graph/nodes/_conflicts"
          local ts_safe
          ts_safe=$(date '+%Y-%m-%dT%H-%M-%S')
          local conflict_name="${node_name%.node.md}-${bucket_id}-${ts_safe}.node.md"
          local conflict_path="graph/nodes/_conflicts/${conflict_name}"
          mv "$node_file" "$conflict_path"
          conflicted=$(( conflicted + 1 ))

          # Log to conflicts.jsonl
          python3 -c "
import json
from datetime import datetime
row = {
    'page': '${node_name%.node.md}',
    'bucket_id': '$bucket_id',
    'conflict_path': '$conflict_path',
    'existing_node_path': '$dest_path',
    'detected_at': datetime.utcnow().isoformat() + 'Z'
}
with open('${WIKI_STATE_DIR}/conflicts.jsonl', 'a') as f:
    f.write(json.dumps(row) + '\n')
" 2>/dev/null || true
          echo "  CONFLICT: ${node_name} already exists — written to _conflicts/"
        fi
      fi
    done < <(find "${bucket_dir}/tmp" -name "*.node.md" 2>/dev/null)

    echo "  Promoted: ${promoted} nodes | Conflicts: ${conflicted}"

    # Update manifest
    local completed_at
    completed_at=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
d['status'] = 'complete'
d['completed_at'] = '$completed_at'
d['nodes_promoted'] = $promoted
with open('$mf', 'w') as f:
    json.dump(d, f, indent=2)
"

    successes=$(( successes + 1 ))

    # Compute structured-channel deltas for this bucket.
    local q_filed c_filed p_filed
    q_filed=$(( $(jsonl_linecount "$q_file") - q_before ))
    c_filed=$(( $(jsonl_linecount "$c_file") - c_before ))
    p_filed=$(( $(jsonl_linecount "$p_file") - p_before ))
    total_q_filed=$(( total_q_filed + q_filed ))
    total_c_filed=$(( total_c_filed + c_filed ))
    total_p_filed=$(( total_p_filed + p_filed ))
    (( q_filed > 0 )) && buckets_with_questions=$(( buckets_with_questions + 1 ))

    local channel_summary=""
    if (( q_filed > 0 || c_filed > 0 || p_filed > 0 )); then
      channel_summary=" | filed: q=${q_filed} c=${c_filed} p1c=${p_filed}"
    fi
    echo "  OK: ${bucket_id} (${elapsed}s | in:${INPUT_TOKENS} cache_create:${CACHE_CREATION} cache_read:${CACHE_READ} out:${OUTPUT_TOKENS} | \$${COST_USD})${channel_summary}"

    append_stats_row "$tier" "$bucket_id" "${wave:-1}" "ok" \
      "$ch_start_fmt" "$ch_end_fmt" "$elapsed" \
      "$INPUT_TOKENS" "$CACHE_CREATION" "$CACHE_READ" "$OUTPUT_TOKENS" "$total_tokens" "$COST_USD" \
      "$pages_count" "$promoted" "$validator_notes" "" \
      "$q_filed" "$c_filed" "$p_filed"
  done

  local wave_elapsed
  wave_elapsed=$(( $(date +%s) - wave_start ))

  echo ""
  echo "=== Wiki Pass 2 — ${tier^^} wave complete ==="
  echo "Succeeded: ${successes} / ${#wave_manifests[@]}"
  echo "Failed: ${failures}"
  echo "Wall time: $(format_duration "$wave_elapsed")"
  if (( total_q_filed > 0 )); then
    echo "  Questions filed: ${total_q_filed} (across ${buckets_with_questions} bucket(s))  →  ${q_file}"
  else
    echo "  Questions filed: 0"
  fi
  echo "  Conflicts filed: ${total_c_filed}"
  echo "  Pass-1 contradictions: ${total_p_filed}"

  update_worklog "$tier"
}

# ── CMD: launch ───────────────────────────────────────────────────────────────

cmd_launch() {
  local tier="" terminals="" waves_per="" orphan_threshold="$DEFAULT_ORPHAN_THRESHOLD"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --terminals|-t) terminals="$2"; shift 2 ;;
      --waves|-w)     waves_per="$2";  shift 2 ;;
      --orphan-threshold-min) orphan_threshold="$2"; shift 2 ;;
      --help|-h)
        echo "Usage: wiki-pass2.sh launch <tier> [-t N -w N] [--orphan-threshold-min N]"
        return 0
        ;;
      -*) echo "Unknown option: $1" >&2; return 1 ;;
      *)  tier="$1"; shift ;;
    esac
  done

  if [[ -z "$tier" || -z "$terminals" || -z "$waves_per" ]]; then
    echo "ERROR: tier, -t (terminals), and -w (waves) are required" >&2
    echo "Usage: wiki-pass2.sh launch <tier> -t <N> -w <N>" >&2
    return 1
  fi

  # Check triage manifests exist
  if [[ ! -d "$WIKI_STATE_DIR" ]] || [[ -z "$(find "$WIKI_STATE_DIR" -name "manifest.json" -maxdepth 2 -print -quit 2>/dev/null)" ]]; then
    echo "No triage manifest found — run \`weirwood wiki triage\` first"
    return 0
  fi

  # Reconciliation and orphan recovery
  echo "--- Pre-launch reconciliation ---"
  run_reconciliation
  run_orphan_recovery "$orphan_threshold"

  # Count pending buckets
  local -a pending_manifests=()
  while IFS= read -r mf; do
    [[ -z "$mf" ]] && continue
    local status
    status=$(manifest_get "$mf" "status")
    case "$status" in
      pending|partial|fail|validation-failed|version-stale) pending_manifests+=("$mf") ;;
    esac
  done < <(list_manifests "$tier")

  local available=${#pending_manifests[@]}
  if (( available == 0 )); then
    echo "${tier^^}: All buckets complete! Nothing to launch."
    return 0
  fi

  # Clear stop file
  rm -f "$STOP_FILE"

  local total_needed=$(( terminals * waves_per ))
  if (( total_needed > available )); then
    echo "Note: only $available pending buckets remain (requested $total_needed)"
    if (( available <= terminals )); then
      terminals=$available
      waves_per=1
    else
      waves_per=$(( (available + terminals - 1) / terminals ))
    fi
  fi

  echo "${tier^^}: ${available} pending buckets"
  echo "Launching ${terminals} terminals, ${waves_per} waves each"
  echo ""

  local project_dir="$REPO_ROOT"
  local idx=0
  local total_waves=$(( (available + WAVE_SIZE - 1) / WAVE_SIZE ))

  for (( t=0; t<terminals; t++ )); do
    local -a term_waves=()
    for (( j=0; j<waves_per; j++ )); do
      local wave_num=$(( idx * waves_per / waves_per + j + t * waves_per + 1 ))
      # Simpler: just assign sequential wave numbers
      local tw=$(( t * waves_per + j + 1 ))
      (( tw <= total_waves )) && term_waves+=("$tw")
    done
    idx=$(( idx + ${#term_waves[@]} ))

    if (( ${#term_waves[@]} == 0 )); then
      continue
    fi

    local wave_display
    wave_display=$(IFS=', '; echo "${term_waves[*]}")
    echo "Terminal $((t+1)): waves [${wave_display}]"

    local cmd=""
    if (( ${#term_waves[@]} == 1 )); then
      cmd="./scripts/wiki-pass2.sh run ${tier} --wave ${term_waves[0]}"
    else
      cmd="for w in ${term_waves[*]}; do "
      cmd+="if [[ -f ${STOP_FILE} ]]; then echo 'Stop file detected — halting before wave '\$w; break; fi; "
      cmd+="./scripts/wiki-pass2.sh run ${tier} --wave \$w; "
      cmd+="done"
    fi

    osascript <<EOF
tell application "iTerm2"
  activate
  tell current window
    create tab with default profile
    tell current session of current tab
      write text "cd ${project_dir} && ${cmd}"
    end tell
  end tell
end tell
EOF
  done

  echo ""
  echo "Launched ${terminals} iTerm2 tabs."
  (( waves_per > 1 )) && echo "To stop after current bucket: weirwood wiki stop"
}

# ── CMD: status ───────────────────────────────────────────────────────────────

cmd_status() {
  local tier_filter="${1:-}"

  # No manifests at all
  if [[ ! -d "$WIKI_STATE_DIR" ]] || [[ -z "$(find "$WIKI_STATE_DIR" -name "manifest.json" -maxdepth 2 -print -quit 2>/dev/null)" ]]; then
    echo "no triage manifest found — run \`weirwood wiki triage\` first"
    return 0
  fi

  # Declare per-tier counters
  declare -A tier_ok tier_fail tier_pending tier_total
  for t in core secondary; do
    tier_ok[$t]=0 tier_fail[$t]=0 tier_pending[$t]=0 tier_total[$t]=0
  done
  local total_cost=0

  # Print table header
  printf "\n"
  printf "%-28s  %-10s  %-5s  %-20s  %-6s  %s\n" \
    "bucket" "tier" "wave" "status" "nodes" "last_run"
  printf "%s\n" "$(printf '%.0s-' {1..95})"

  while IFS= read -r mf; do
    [[ -z "$mf" ]] && continue
    local bucket_id tier status nodes last_run wave_num
    bucket_id=$(manifest_get "$mf" "bucket_id")
    tier=$(manifest_get "$mf" "tier")
    status=$(manifest_get "$mf" "status")
    wave_num=$(manifest_get "$mf" "wave" 2>/dev/null || echo "—")
    [[ -z "$wave_num" || "$wave_num" == "null" ]] && wave_num="—"

    # Count promoted nodes
    nodes=$(python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
print(d.get('nodes_promoted', '—'))
" 2>/dev/null || echo "—")

    # Last run time
    last_run=$(python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
ct = d.get('completed_at', d.get('started_at', ''))
print(ct[:19].replace('T', ' ') if ct else '—')
" 2>/dev/null || echo "—")

    # Apply tier filter
    if [[ -n "$tier_filter" && "$tier" != "$tier_filter" ]]; then
      continue
    fi

    printf "%-28s  %-10s  %-5s  %-20s  %-6s  %s\n" \
      "${bucket_id:0:28}" "$tier" "$wave_num" "$status" "$nodes" "$last_run"

    # Count into tier buckets
    if [[ -n "${tier_ok[$tier]+_}" ]]; then
      tier_total[$tier]=$(( tier_total[$tier] + 1 ))
      case "$status" in
        complete|ok) tier_ok[$tier]=$(( tier_ok[$tier] + 1 )) ;;
        fail|validation-failed) tier_fail[$tier]=$(( tier_fail[$tier] + 1 )) ;;
        *) tier_pending[$tier]=$(( tier_pending[$tier] + 1 )) ;;
      esac
    fi
  done < <(list_manifests "$tier_filter")

  # Roll-up footer
  printf "\n"
  for t in core secondary; do
    (( tier_total[$t] == 0 )) && continue
    printf "%-12s %d/%d buckets ok, %d failed, %d pending\n" \
      "${t}:" "${tier_ok[$t]}" "${tier_total[$t]}" \
      "${tier_fail[$t]}" "${tier_pending[$t]}"
  done

  # Cost from stats CSVs
  total_cost=$(python3 -c "
import csv, glob, os
total = 0.0
for f in glob.glob('${STATS_DIR}/wiki-pass2-stats-*-${VERSION}.csv'):
    try:
        with open(f) as fh:
            for row in csv.DictReader(fh):
                try: total += float(row.get('cost_usd', 0))
                except: pass
    except: pass
print(f'{total:.2f}')
" 2>/dev/null || echo "0.00")

  # Count special files
  local conflicts=0 contradictions=0 questions=0
  [[ -f "${WIKI_STATE_DIR}/conflicts.jsonl" ]] && \
    conflicts=$(wc -l < "${WIKI_STATE_DIR}/conflicts.jsonl" | tr -d ' ')
  [[ -f "${WIKI_STATE_DIR}/pass1-contradictions.jsonl" ]] && \
    contradictions=$(wc -l < "${WIKI_STATE_DIR}/pass1-contradictions.jsonl" | tr -d ' ')
  [[ -f "${WIKI_STATE_DIR}/questions-for-matt.jsonl" ]] && \
    questions=$(python3 -c "
import json
count = 0
with open('${WIKI_STATE_DIR}/questions-for-matt.jsonl') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            obj = json.loads(line)
            if not obj.get('resolved_at'): count += 1
        except: pass
print(count)
" 2>/dev/null || echo 0)

  printf "total cost so far:     \$%s\n" "$total_cost"
  printf "conflicts:             %d   (%s/conflicts.jsonl)\n" "$conflicts" "$WIKI_STATE_DIR"
  printf "contradictions:        %d   (%s/pass1-contradictions.jsonl)\n" "$contradictions" "$WIKI_STATE_DIR"
  printf "unresolved questions:  %d   (%s/questions-for-matt.jsonl)\n" "$questions" "$WIKI_STATE_DIR"
  printf "\n"
}

# ── CMD: check ────────────────────────────────────────────────────────────────

cmd_check() {
  if [[ ! -f "scripts/wiki-pass2-coherence.py" ]]; then
    echo "ERROR: scripts/wiki-pass2-coherence.py not found." >&2
    return 1
  fi
  echo "Running cross-bucket coherence check..."
  python3 scripts/wiki-pass2-coherence.py "$@"
}

# ── CMD: reset ────────────────────────────────────────────────────────────────

cmd_reset() {
  local version="" bucket_filter="" archive_dir="" dry_run=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --version)     version="$2";        shift 2 ;;
      --bucket|-b)   bucket_filter="$2";  shift 2 ;;
      --archive-dir) archive_dir="$2";    shift 2 ;;
      --dry-run)     dry_run=true;        shift   ;;
      --help|-h)
        echo "Usage: wiki-pass2.sh reset --version vN [--archive-dir PATH] [--dry-run]"
        echo "       wiki-pass2.sh reset --bucket <id> [--archive-dir PATH] [--dry-run]"
        return 0
        ;;
      -*) echo "Unknown option: $1" >&2; return 1 ;;
      *)  echo "Unknown argument: $1" >&2; return 1 ;;
    esac
  done

  if [[ -n "$bucket_filter" ]]; then
    cmd_reset_bucket "$bucket_filter" "$archive_dir" "$dry_run"
    return $?
  fi

  if [[ -z "$version" ]]; then
    echo "ERROR: --version or --bucket is required" >&2
    return 1
  fi

  # Default archive dir
  local ts
  ts=$(date '+%Y-%m-%dT%H-%M-%S')
  if [[ -z "$archive_dir" ]]; then
    archive_dir="graph/archives/wiki-pass2-${version}-${ts}"
  fi

  # Refuse if archive dir already exists
  if [[ -d "$archive_dir" ]]; then
    echo "ERROR: archive directory already exists: $archive_dir" >&2
    echo "  Rename or move it first to avoid silent merging." >&2
    return 1
  fi

  echo "=== Wiki Pass 2 Reset — version ${version} ==="
  echo "Archive destination: ${archive_dir}"
  $dry_run && echo "(DRY RUN — no files will be moved)"
  echo ""

  # Find nodes matching prompt_version in frontmatter
  local -a node_files=()
  while IFS= read -r nf; do
    [[ -z "$nf" ]] && continue
    local pv
    pv=$(python3 -c "
import re
with open('$nf') as f:
    content = f.read()
m = re.search(r'^prompt_version:\s*(.+)$', content, re.MULTILINE)
print(m.group(1).strip() if m else '')
" 2>/dev/null || echo "")
    [[ "$pv" == "$version" ]] && node_files+=("$nf")
  done < <(find "graph/nodes" -name "*.node.md" -not -path "*/_conflicts/*" 2>/dev/null)

  echo "Node files to archive: ${#node_files[@]}"

  # Find bucket manifests matching prompt_version
  local -a bucket_dirs=()
  while IFS= read -r mf; do
    [[ -z "$mf" ]] && continue
    local pv
    pv=$(manifest_get "$mf" "prompt_version")
    [[ "$pv" == "$version" ]] && bucket_dirs+=("$(dirname "$mf")")
  done < <(list_manifests)

  echo "Bucket state directories to archive: ${#bucket_dirs[@]}"

  # List preserved files
  local preserved_files=(
    "${WIKI_STATE_DIR}/conflicts.jsonl"
    "${WIKI_STATE_DIR}/pass1-contradictions.jsonl"
    "${WIKI_STATE_DIR}/questions-for-matt.jsonl"
    "${WIKI_STATE_DIR}/failures"
    "graph/nodes/_conflicts"
  )
  echo ""
  echo "Preserved (not moved):"
  for pf in "${preserved_files[@]}"; do
    [[ -e "$pf" ]] && echo "  $pf"
  done
  echo ""

  if $dry_run; then
    echo "DRY RUN complete — no files moved."
    return 0
  fi

  # Execute moves
  mkdir -p "$archive_dir"

  # Move node files (preserving parent-type structure)
  local nodes_moved=0
  for nf in "${node_files[@]}"; do
    local rel_path="${nf#graph/nodes/}"
    local dest="${archive_dir}/nodes/${rel_path}"
    mkdir -p "$(dirname "$dest")"
    mv "$nf" "$dest"
    nodes_moved=$(( nodes_moved + 1 ))
  done

  # Move bucket state directories
  local buckets_moved=0
  for bd in "${bucket_dirs[@]}"; do
    local bucket_name
    bucket_name=$(basename "$bd")
    local dest="${archive_dir}/wiki-pass2-state/${bucket_name}"
    mkdir -p "$(dirname "$dest")"
    mv "$bd" "$dest"
    buckets_moved=$(( buckets_moved + 1 ))
  done

  echo "=== Reset complete ==="
  echo "Nodes moved:   ${nodes_moved}"
  echo "Buckets moved: ${buckets_moved}"
  echo "Archive path:  ${archive_dir}"
  echo ""
  echo "Preserved:"
  for pf in "${preserved_files[@]}"; do
    [[ -e "$pf" ]] && echo "  $pf"
  done
}

# Reset a single bucket for re-emit: archive its promoted nodes, wipe tmp/,
# flip manifest status to pending so cmd_run picks it up. Preserves the
# manifest itself (input_pages, fingerprint, expected_nodes) so the next
# triage --accept doesn't have to recompute from scratch.
cmd_reset_bucket() {
  local bucket_id="$1" archive_dir="$2" dry_run="$3"

  local bucket_dir="${WIKI_STATE_DIR}/${bucket_id}"
  local mf="${bucket_dir}/manifest.json"
  if [[ ! -f "$mf" ]]; then
    echo "ERROR: no manifest found for bucket '${bucket_id}' at ${mf}" >&2
    return 1
  fi

  local ts
  ts=$(date '+%Y-%m-%dT%H-%M-%S')
  if [[ -z "$archive_dir" ]]; then
    archive_dir="graph/archives/wiki-pass2-${bucket_id}-${ts}"
  fi
  if [[ -e "$archive_dir" ]]; then
    echo "ERROR: archive directory already exists: $archive_dir" >&2
    return 1
  fi

  echo "=== Wiki Pass 2 Bucket Reset — ${bucket_id} ==="
  echo "Archive destination: ${archive_dir}"
  $dry_run && echo "(DRY RUN — no files will be moved)"

  # Find existing promoted nodes by reading expected_nodes from the manifest
  # AND any current node files in graph/nodes/<type>/ that match the bucket's
  # bucket_id frontmatter (catches slug-renamed nodes after a fingerprint change).
  local -a node_files=()
  while IFS= read -r expected; do
    [[ -z "$expected" ]] && continue
    while IFS= read -r found; do
      [[ -n "$found" ]] && node_files+=("$found")
    done < <(find "graph/nodes" -name "$expected" -not -path "*/_conflicts/*" 2>/dev/null)
  done < <(python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
for n in d.get('expected_nodes', []):
    print(n)
" 2>/dev/null)

  # Also catch any node with bucket_id frontmatter pointing at this bucket
  # (covers nodes whose slug differs from expected — e.g., nymeria-direwolf
  # when expected was nymeria).
  while IFS= read -r nf; do
    [[ -z "$nf" ]] && continue
    local node_bucket
    node_bucket=$(python3 -c "
import re
with open('$nf') as f:
    content = f.read()
m = re.search(r'^bucket_id:\s*(.+)$', content, re.MULTILINE)
print(m.group(1).strip() if m else '')
" 2>/dev/null || echo "")
    if [[ "$node_bucket" == "$bucket_id" ]]; then
      # Skip if already in the list
      local already=false
      for existing in "${node_files[@]}"; do
        [[ "$existing" == "$nf" ]] && { already=true; break; }
      done
      $already || node_files+=("$nf")
    fi
  done < <(find "graph/nodes" -name "*.node.md" -not -path "*/_conflicts/*" 2>/dev/null)

  echo "Node files to archive: ${#node_files[@]}"
  for nf in "${node_files[@]}"; do
    echo "  $nf"
  done

  if $dry_run; then
    echo "DRY RUN complete — no files moved."
    return 0
  fi

  mkdir -p "$archive_dir"

  local nodes_moved=0
  for nf in "${node_files[@]}"; do
    local rel_path="${nf#graph/nodes/}"
    local dest="${archive_dir}/nodes/${rel_path}"
    mkdir -p "$(dirname "$dest")"
    mv "$nf" "$dest"
    nodes_moved=$(( nodes_moved + 1 ))
  done

  # Wipe tmp/ and reset manifest status
  rm -rf "${bucket_dir}/tmp"
  mkdir -p "${bucket_dir}/tmp"

  python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
d['status'] = 'pending'
d['started_at'] = None
d['completed_at'] = None
d['nodes_promoted'] = 0
d['validation_report'] = None
with open('$mf', 'w') as f:
    json.dump(d, f, indent=2)
"

  echo ""
  echo "=== Bucket reset complete ==="
  echo "Bucket:        ${bucket_id}"
  echo "Nodes moved:   ${nodes_moved}"
  echo "Archive path:  ${archive_dir}"
  echo "Manifest:      ${mf} (status → pending)"
  echo ""
  local tier
  tier=$(manifest_get "$mf" "tier")
  echo "Next: weirwood wiki run ${tier:-<tier>} --bucket ${bucket_id}"
}

# ── CMD: unstick ──────────────────────────────────────────────────────────────

cmd_unstick() {
  local bucket_id="" force=false

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --force) force=true; shift ;;
      --help|-h) echo "Usage: wiki-pass2.sh unstick <bucket> [--force]"; return 0 ;;
      -*) echo "Unknown option: $1" >&2; return 1 ;;
      *)  bucket_id="$1"; shift ;;
    esac
  done

  if [[ -z "$bucket_id" ]]; then
    echo "ERROR: bucket id is required" >&2
    echo "Usage: wiki-pass2.sh unstick <bucket> [--force]" >&2
    return 1
  fi

  local bucket_dir="${WIKI_STATE_DIR}/${bucket_id}"
  local mf="${bucket_dir}/manifest.json"

  if [[ ! -f "$mf" ]]; then
    echo "ERROR: no manifest found for bucket '${bucket_id}'" >&2
    echo "  Available buckets:"
    find "$WIKI_STATE_DIR" -name "manifest.json" -maxdepth 2 2>/dev/null | while read -r m; do
      echo "    $(basename "$(dirname "$m")")"
    done
    return 1
  fi

  local status
  status=$(manifest_get "$mf" "status")
  if [[ "$status" != "in-progress" ]]; then
    echo "Bucket '${bucket_id}' is not in-progress (status: ${status}). Nothing to unstick."
    return 0
  fi

  # Check for recent tmp/ files vs started_at
  if [[ "$force" == false ]]; then
    local started_at
    started_at=$(manifest_get "$mf" "started_at")
    if [[ -n "$started_at" && "$started_at" != "null" ]]; then
      local started_epoch
      started_epoch=$(python3 -c "
from datetime import datetime
try:
    dt = datetime.fromisoformat('$started_at')
    print(int(dt.timestamp()))
except:
    print(0)
" 2>/dev/null || echo 0)
      # Check if any tmp/ files are newer than started_at
      local newer_files=0
      if [[ -d "${bucket_dir}/tmp" ]]; then
        while IFS= read -r tf; do
          [[ -z "$tf" ]] && continue
          local mtime
          mtime=$(python3 -c "import os; print(int(os.path.getmtime('$tf')))" 2>/dev/null || echo 0)
          (( mtime > started_epoch )) && newer_files=$(( newer_files + 1 ))
        done < <(find "${bucket_dir}/tmp" -name "*.node.md" 2>/dev/null)
      fi
      if (( newer_files > 0 )); then
        echo "ERROR: ${newer_files} node file(s) in tmp/ are newer than started_at=${started_at}" >&2
        echo "  This suggests in-flight work may still be active." >&2
        echo "  Use --force to override and wipe tmp/ anyway." >&2
        return 1
      fi
    fi
  fi

  echo "Clearing bucket '${bucket_id}' (wiping tmp/, resetting to pending)..."
  rm -rf "${bucket_dir}/tmp"
  mkdir -p "${bucket_dir}/tmp"
  manifest_set "$mf" "status" "pending"
  python3 -c "
import json
with open('$mf') as f:
    d = json.load(f)
d['started_at'] = None
with open('$mf', 'w') as f:
    json.dump(d, f, indent=2)
" 2>/dev/null || true
  echo "Done. Bucket '${bucket_id}' reset to pending."
}

# ── CMD: questions ────────────────────────────────────────────────────────────

cmd_questions() {
  local filter_unresolved=false filter_bucket="" filter_type=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --unresolved)  filter_unresolved=true; shift ;;
      --bucket)      filter_bucket="$2"; shift 2 ;;
      --type)        filter_type="$2"; shift 2 ;;
      --help|-h)
        echo "Usage: wiki-pass2.sh questions [--unresolved|--bucket <id>|--type <type>]"
        echo "Types: disambiguation | tier | promotion | other"
        return 0
        ;;
      -*) echo "Unknown option: $1" >&2; return 1 ;;
      *)  echo "Unknown argument: $1" >&2; return 1 ;;
    esac
  done

  local qfile="${WIKI_STATE_DIR}/questions-for-matt.jsonl"
  if [[ ! -f "$qfile" ]]; then
    echo "No questions file found at ${qfile}"
    echo "(Questions are appended here when buckets surface disambiguation or tier issues.)"
    return 0
  fi

  python3 - "$qfile" "$filter_unresolved" "$filter_bucket" "$filter_type" <<'PYEOF'
import json, sys

qfile = sys.argv[1]
filter_unresolved = sys.argv[2] == "true"
filter_bucket = sys.argv[3]
filter_type = sys.argv[4]

count = 0
with open(qfile) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            q = json.loads(line)
        except Exception:
            continue

        # Apply filters
        if filter_unresolved and q.get("resolved_at"):
            continue
        if filter_bucket and q.get("bucket_id") != filter_bucket:
            continue
        if filter_type and q.get("type") != filter_type:
            continue

        count += 1
        resolved = "[RESOLVED]" if q.get("resolved_at") else "[OPEN]"
        print(f"\n{resolved} {q.get('question_id', '?')} — {q.get('type', '?')}")
        print(f"  bucket: {q.get('bucket_id', '?')} | page: {q.get('page', '?')}")
        print(f"  asked:  {q.get('asked_at', '?')[:19]}")
        if q.get("resolved_at"):
            print(f"  resolved: {q.get('resolved_at', '')[:19]}")
        print(f"  Q: {q.get('text', '')}")
        if q.get("resolution"):
            print(f"  A: {q.get('resolution', '')}")

if count == 0:
    print("No questions match the given filters.")
else:
    print(f"\n--- {count} question(s) shown ---")
PYEOF
}

# ── CMD: stop ─────────────────────────────────────────────────────────────────

cmd_stop() {
  touch "$STOP_FILE"
  echo "Wiki Pass 2 stop file created at ${STOP_FILE}"
  echo "Tabs will halt after their current bucket. Does not affect Pass 1 extraction."
}

# ── Usage ─────────────────────────────────────────────────────────────────────

usage() {
  cat <<'EOF'
wiki-pass2.sh — Wiki Pass 2 launcher for the Weirwood Network

Subcommands:
  triage [--accept]
      Draft bucket assignments from triage manifest.
      --accept writes per-bucket manifests to working/wiki-pass2/<bucket>/manifest.json

  run <tier> [--wave N] [--bucket <id>] [--orphan-threshold-min N]
      Process pending buckets in a tier. Atomic: validates before promoting
      output from tmp/ to graph/nodes/.

  launch <tier> [-t N -w N] [--orphan-threshold-min N]
      Open iTerm tabs for parallel bucket processing (mirrors extract.sh launch).

  status [tier]
      ASCII table of bucket progress + roll-up footer.
      Without any manifest on disk, prints "no triage manifest found" and exits 0.

  check [--tier core|secondary|all] [-v]
      Run cross-bucket coherence check (scripts/wiki-pass2-coherence.py).

  reset --version vN [--archive-dir PATH] [--dry-run]
      Archive all nodes + manifests from a prompt version. Preserves audit files.
      Refuses if archive dir already exists.

  reset --bucket <id> [--archive-dir PATH] [--dry-run]
      Archive a single bucket's promoted nodes, wipe tmp/, flip manifest to
      pending. Use to re-emit a bucket from a clean bundle after a triage fix.

  unstick <bucket> [--force]
      Clear orphaned in-progress bucket (wipes tmp/, resets to pending).
      Refuses if tmp/ has files newer than started_at unless --force.

  questions [--unresolved|--bucket <id>|--type <type>]
      Query working/wiki-pass2/questions-for-matt.jsonl.
      Types: disambiguation | tier | promotion | other

  stop
      Create /tmp/wiki-pass2-stop (DISTINCT from /tmp/extraction-stop).
      Tabs check between buckets; current bucket finishes normally.

Use via: weirwood wiki <subcommand>
EOF
}

# ── Dispatch ──────────────────────────────────────────────────────────────────

case "${1:-}" in
  triage)    shift; cmd_triage "$@" ;;
  run)       shift; cmd_run "$@" ;;
  launch)    shift; cmd_launch "$@" ;;
  status)    shift; cmd_status "$@" ;;
  check)     shift; cmd_check "$@" ;;
  reset)     shift; cmd_reset "$@" ;;
  unstick)   shift; cmd_unstick "$@" ;;
  questions) shift; cmd_questions "$@" ;;
  stop)      shift; cmd_stop "$@" ;;
  --help|-h) usage ;;
  *)         usage ;;
esac
