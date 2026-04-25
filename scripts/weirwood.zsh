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
#   'weirwood stop' creates a file (/tmp/extraction-stop) that terminals
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
      touch /tmp/extraction-stop
      echo "Stop file created — terminals will halt after their current wave."
      ;;
    ""|--help|-h)
      echo "weirwood — run Weirwood Network extractions"
      echo ""
      echo "Commands:"
      echo "  weirwood                          This help + all-books overview"
      echo "  weirwood check                    Verify source files & prerequisites"
      echo "  weirwood <book>                   Detailed status (wave table, costs)"
      echo "  weirwood <book> <terms> <waves>   Launch iTerm tabs to extract"
      echo "  weirwood <book> <t> <w> <model>   Launch with a specific model"
      echo "  weirwood stop                     Soft stop (see below)"
      echo ""
      echo "Examples:"
      echo "  weirwood acok                     What's left in ACOK?"
      echo "  weirwood acok 2 3                 2 terminals, 3 waves each"
      echo "  weirwood acok 2 3 claude-sonnet-4-6"
      echo "  weirwood stop"
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
        local waves="${3:?Usage: weirwood <book> <terminals> <waves>}"
        local model="${4:-}"
        local model_args=()
        [[ -n "$model" ]] && model_args=(--model "$model")
        "$script" launch "$book" -t "$terminals" -w "$waves" "${model_args[@]}"
      fi
      ;;
  esac
}
