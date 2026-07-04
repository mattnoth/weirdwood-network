# weirwood — run Weirwood Network extractions
#
# Install:
#   source this file in your .zshrc, or copy it to your shell functions directory.
#   Example: echo 'source ~/source/asoiaf-chat/scripts/weirwood.zsh' >> ~/.zshrc
#
# Commands:
#   weirwood                         Overview: help + status across all books
#   weirwood <book>                  Detailed status for one book (wave table)
#   weirwood <book> <terms> <waves>  Launch extraction across iTerm tabs
#   weirwood <book> <t> <w> <model>  Launch with a specific Claude model
#   weirwood stop                    Soft stop — halt after current wave finishes
#   weirwood wiki <subcommand>       Wiki Pass 2 — see 'weirwood wiki --help'
#   weirwood stage4 <subcommand>     Stage 4 prose-edge classifier
#
# Race protection:
#   Multiple terminals on the same book are safe — each chapter is claimed
#   atomically before extraction starts. A second terminal skips chapters
#   already claimed or completed by another.
#
# Examples:
#   weirwood                         # show help + all-books overview
#   weirwood acok                    # what's left in ACOK?
#   weirwood acok 2 3                # 2 terminals, 3 waves each
#   weirwood acok 2 3 claude-sonnet-4-6  # use sonnet instead of opus
#   weirwood stop                    # stop between waves (see below)
#
# How it works:
#   Each book's chapters are grouped into waves of 5. When you launch,
#   the script finds incomplete waves and distributes them across iTerm
#   tabs. Each tab runs its assigned waves one at a time. When you run
#   it again later, it picks up from where it left off.
#
# Soft stop:
#   'weirwood stop' creates a file ($HOME/source/claude-cwd/tmp/extraction-stop) that terminals
#   check between waves. It never interrupts a wave mid-chapter — the
#   current wave finishes normally, then the terminal sees the stop file
#   and exits instead of starting the next wave.
#
#   Run 'weirwood stop' from ANY terminal — a third tab, Claude Code
#   (! weirwood stop), wherever. It doesn't talk to the running terminals
#   directly; they discover the file on their own.
#
#   The stop file is automatically cleared when you launch a new run.

weirwood() {
  # Resolve project dir relative to this script, or fall back to default
  local project_dir="${WEIRWOOD_PROJECT_DIR:-$HOME/source/asoiaf-chat}"
  local script="$project_dir/scripts/extract.sh"
  local wiki_script="$project_dir/scripts/wiki-pass2.sh"
  local stage4_script="$project_dir/scripts/stage4.sh"

  if [[ ! -f "$script" ]]; then
    echo "ERROR: extract.sh not found at $script"
    echo "Set WEIRWOOD_PROJECT_DIR to the repo root, or clone to ~/source/asoiaf-chat"
    return 1
  fi

  case "${1:-}" in
    check)
      "$script" check
      ;;
    stop)
      touch $HOME/source/claude-cwd/tmp/extraction-stop
      echo "Stop file created — terminals will halt after their current wave."
      ;;

    # ── Wiki Pass 2 subcommand ──────────────────────────────────────────────
    wiki)
      if [[ ! -f "$wiki_script" ]]; then
        echo "ERROR: wiki-pass2.sh not found at $wiki_script"
        return 1
      fi
      local wiki_sub="${2:-}"
      case "$wiki_sub" in
        ""|status)
          # weirwood wiki              → status (all tiers)
          # weirwood wiki status       → status (all tiers)
          "$wiki_script" status "${3:-}"
          ;;
        triage|run|check|reset|unstick|questions|stop|launch)
          # Pass remaining args verbatim
          shift 2
          "$wiki_script" "$wiki_sub" "$@"
          ;;
        core|secondary)
          # weirwood wiki core          → status for core tier
          # weirwood wiki core 2 3      → launch: 2 terminals, 3 waves each
          local tier="$wiki_sub"
          local terminals="${3:-}"
          local waves="${4:-}"
          if [[ -z "$terminals" ]]; then
            # Status mode for this tier
            "$wiki_script" status "$tier"
          else
            if [[ -z "$waves" ]]; then
              echo "Usage: weirwood wiki $tier <terminals> <waves>"
              return 1
            fi
            "$wiki_script" launch "$tier" -t "$terminals" -w "$waves"
          fi
          ;;
        --help|-h)
          echo "weirwood wiki — Wiki Pass 2 (wiki → graph/nodes/)"
          echo ""
          echo "Commands:"
          echo "  weirwood wiki                           Status (all tiers)"
          echo "  weirwood wiki status [tier]             Status table"
          echo "  weirwood wiki triage [--accept]         Draft or commit bucket manifests"
          echo "  weirwood wiki core                      Status for core tier"
          echo "  weirwood wiki core <terms> <waves>      Launch iTerm tabs (core tier)"
          echo "  weirwood wiki secondary                 Status for secondary tier"
          echo "  weirwood wiki secondary <terms> <waves> Launch iTerm tabs (secondary)"
          echo "  weirwood wiki run <tier> [--wave N]     Run a single wave"
          echo "  weirwood wiki check                     Cross-bucket coherence check"
          echo "  weirwood wiki reset --version vN        Archive prior-version output"
          echo "  weirwood wiki unstick <bucket>          Clear orphaned in-progress bucket"
          echo "  weirwood wiki questions [--unresolved]  View question queue"
          echo "  weirwood wiki stop                      Soft stop (wiki tabs only)"
          echo ""
          echo "Examples:"
          echo "  weirwood wiki triage --accept           Commit triage bucket manifests"
          echo "  weirwood wiki core 2 3                  2 terminals, 3 waves each (core)"
          echo "  weirwood wiki status core               Core tier progress table"
          echo "  weirwood wiki stop                      Halt wiki tabs after current bucket"
          echo "  weirwood wiki check                     Check graph/nodes/ coherence"
          echo "  weirwood wiki reset --version v1        Archive v1 output before re-run"
          ;;
        *)
          echo "Unknown wiki subcommand: $wiki_sub"
          echo "Run 'weirwood wiki --help' for usage."
          return 1
          ;;
      esac
      ;;

    # ── Long-run track registry ────────────────────────────────────────────────
    run)
      local run_script="$project_dir/scripts/weirwood-run.sh"
      if [[ ! -f "$run_script" ]]; then
        echo "ERROR: weirwood-run.sh not found at $run_script"
        return 1
      fi
      shift
      bash "$run_script" "$@"
      ;;

    # ── Standing tools (class C/D) ───────────────────────────────────────────────
    query)
      # NEW front door — the consolidated query engine (graph/query/weirwood_query).
      #   weirwood query <slug> | --neighbors <slug> | --path <a> <b> | --health
      #   weirwood query --causal-chain <slug> | --container <name> | --family-tree <slug>
      shift
      PYTHONPATH="$project_dir/graph/query${PYTHONPATH:+:$PYTHONPATH}" \
        python3 -m weirwood_query.cli "$@"
      ;;
    graph)
      # LEGACY alias — thin pass-through to the graph-query.py compat shim.
      # Prefer 'weirwood query'. (Shim output is identical; shim points at graph/query/.)
      shift
      python3 "$project_dir/scripts/graph-query.py" "$@"
      ;;
    resolve)
      # LEGACY alias — thin pass-through to the event_alias_resolver.py compat shim.
      # Prefer 'weirwood query' for lookups; rebuilds run via 'weirwood refresh'.
      shift
      python3 "$project_dir/scripts/event_alias_resolver.py" "$@"
      ;;
    refresh)
      # Rebuild ALL derived artifacts (class C/D) — the standard post-node-mutation step.
      #   weirwood refresh            Rebuild entity+character indexes + alias resolver
      #   weirwood refresh --check    WARN if artifacts are stale vs graph/nodes/
      local refresh_script="$project_dir/scripts/weirwood-refresh.sh"
      if [[ ! -f "$refresh_script" ]]; then
        echo "ERROR: weirwood-refresh.sh not found at $refresh_script"
        return 1
      fi
      shift
      bash "$refresh_script" "$@"
      ;;

    # ── Stage 4 subcommand ─────────────────────────────────────────────────────
    stage4)
      if [[ ! -f "$stage4_script" ]]; then
        echo "ERROR: stage4.sh not found at $stage4_script"
        return 1
      fi
      local s4_sub="${2:-}"
      case "$s4_sub" in
        ""|status)
          bash "$stage4_script" status
          ;;
        stop)
          touch $HOME/source/claude-cwd/tmp/stage4-stop
          echo "Stop file created — workers will halt after their current batch."
          ;;
        unstick)
          local batch_id="${3:-}"
          if [[ -z "$batch_id" ]]; then
            echo "Usage: weirwood stage4 unstick <batch_id>"
            return 1
          fi
          bash "$stage4_script" unstick "$batch_id"
          ;;
        --help|-h)
          echo "weirwood stage4 — Stage 4 prose-edge classifier"
          echo ""
          echo "Commands:"
          echo "  weirwood stage4                 Status: progress, tokens, cost, stuck batches"
          echo "  weirwood stage4 <N>             Launch N concurrent worker tabs"
          echo "  weirwood stage4 stop            Soft stop after current batch"
          echo "  weirwood stage4 unstick <id>    Release orphaned batch lock + requeue"
          echo ""
          echo "Examples:"
          echo "  weirwood stage4                 Check progress"
          echo "  weirwood stage4 5               Launch 5 concurrent workers"
          echo "  weirwood stage4 stop"
          echo "  weirwood stage4 unstick batch-0003"
          ;;
        *)
          # If numeric, treat as terminal count
          if [[ "$s4_sub" =~ ^[0-9]+$ ]]; then
            bash "$stage4_script" launch -t "$s4_sub"
          else
            echo "Unknown stage4 subcommand: $s4_sub"
            echo "Run 'weirwood stage4 --help' for usage."
            return 1
          fi
          ;;
      esac
      ;;

    # ── Sift corpus scanner ────────────────────────────────────────────────────
    sift)
      shift
      python3 "$project_dir/scripts/sift.py" "$@"
      ;;

    ""|--help|-h)
      echo "weirwood — run Weirwood Network extractions"
      echo ""
      echo "Commands:"
      echo "  weirwood                          This help + all-books overview"
      echo "  weirwood check                    Verify source files & prerequisites"
      echo "  weirwood <book>                   Detailed status (wave table, costs)"
      echo "  weirwood <book> <t> <w>           Launch iTerm tabs to extract"
      echo "  weirwood <book> <t> <w> <model>   With a specific model"
      echo "  weirwood stop                     Soft stop (see below)"
      echo "  weirwood wiki <subcommand>        Wiki Pass 2 — see 'weirwood wiki --help'"
      echo "  weirwood stage4 <subcommand>      Stage 4 prose-edge classifier"
      echo "  weirwood sift <subcommand>        Sift corpus scanner (status/run/sample/interpret)"
      echo "  weirwood run <subcommand>         Long-run track registry — see 'weirwood run --help'"
      echo "  weirwood query <args>             Query engine (graph/query/) — the NEW front door"
      echo "  weirwood graph <args>             LEGACY alias for query (graph-query.py shim)"
      echo "  weirwood resolve <args>           LEGACY alias (event_alias_resolver.py shim)"
      echo "  weirwood refresh [--check]        Rebuild all derived artifacts (post-node-mutation)"
      echo ""
      echo "Examples:"
      echo "  weirwood acok                     What's left in ACOK?"
      echo "  weirwood acok 2 1                 2 terminals, 1 wave each"
      echo "  weirwood acok 2 3 claude-opus-4-7"
      echo "  weirwood stop"
      echo "  weirwood wiki triage --accept     Commit wiki triage manifests"
      echo "  weirwood wiki core 2 3            Launch wiki core tier (2 tabs, 3 waves)"
      echo "  weirwood stage4 5                 Launch 5 Stage 4 worker tabs"
      echo "  weirwood run list                 List long-run tracks"
      echo "  weirwood query --neighbors ned-stark   Inspect a node's edges"
      echo "  weirwood query --path arya-stark jaqen-hghar"
      echo "  weirwood resolve --lookup \"Ned Stark's execution\""
      echo "  weirwood refresh                  Rebuild indexes + alias resolver after a node add/rename"
      echo "  weirwood refresh --check          Warn if derived artifacts are stale"
      echo ""
      echo "Run ANY long job under longrun supervision (no new wrapper needed):"
      echo "  weirwood run start custom -- python3 scripts/<your-worker>.py --resume"
      echo "  (worker emits exit 0=done / 2=wall / 10=more-work; see scripts/worker-template.py)"
      echo ""
      echo "Books: agot acok asos affc adwd"
      echo ""
      echo "How it works:"
      echo "  1. Run 'weirwood <book>' to see which waves are incomplete"
      echo "  2. Run 'weirwood <book> <terminals> <waves>' to launch"
      echo "     - Automatically picks the next incomplete waves"
      echo "     - Each terminal runs its waves sequentially"
      echo "  3. When the session ends, run it again — picks up where it left off"
      echo ""
      echo "Soft stop:"
      echo "  'weirwood stop' creates a file that terminals check between waves."
      echo "  It never interrupts mid-chapter — the current wave finishes, then"
      echo "  the terminal exits instead of starting the next wave."
      echo "  Run it from any terminal, a third tab, or Claude Code (! weirwood stop)."
      echo "  The stop file is cleared automatically on the next launch."
      echo "  Note: 'weirwood wiki stop' and 'weirwood stage4 stop' each use SEPARATE"
      echo "        stop files ($HOME/source/claude-cwd/tmp/wiki-pass2-stop, $HOME/source/claude-cwd/tmp/stage4-stop)."
      echo ""
      echo "Overview:"
      # Quick status across all books
      for b in agot acok asos affc adwd; do
        local chdir="$project_dir/sources/chapters/$b"
        local exdir="$project_dir/extractions/mechanical/$b"
        if [[ ! -d "$chdir" ]]; then
          printf "  %-5s  (no chapters)\n" "${b:u}"
          continue
        fi
        local total=0 done=0
        for f in "$chdir"/*.md(N); do
          total=$((total + 1))
          local stem="${f:t:r}"
          if [[ -f "$exdir/${stem}.extraction.md" ]]; then
            done=$((done + 1))
          fi
        done
        if (( total == 0 )); then
          printf "  %-5s  (no chapters)\n" "${b:u}"
        elif (( done == total )); then
          printf "  %-5s  %d/%d  done\n" "${b:u}" "$done" "$total"
        else
          printf "  %-5s  %d/%d  (%d remaining)\n" "${b:u}" "$done" "$total" "$((total - done))"
        fi
      done
      ;;
    *)
      local book="$1"
      if [[ -z "${2:-}" ]]; then
        # Status mode
        "$script" status "$book"
      else
        local terminals="$2"
        local waves="${3:?Usage: weirwood <book> <terminals> <waves> [model]}"
        shift 3
        local model=""
        local extra_args=()
        # Pass through remaining args (model, unknown flags)
        while [[ $# -gt 0 ]]; do
          case "$1" in
            --chain|--delay) echo "ERROR: --chain and --delay were removed. Launch separate runs instead." >&2; return 1 ;;
            --model|-m) model="$2"; shift 2 ;;
            -*)         extra_args+=("$1"); shift ;;
            *)          # Positional model arg (legacy: weirwood <book> <t> <w> <model>)
                        [[ -z "$model" ]] && model="$1"
                        shift ;;
          esac
        done
        local model_args=()
        [[ -n "$model" ]] && model_args=(--model "$model")
        "$script" launch "$book" -t "$terminals" -w "$waves" "${model_args[@]}" "${extra_args[@]}"
      fi
      ;;
  esac
}
