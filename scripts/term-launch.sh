#!/usr/bin/env bash
# term-launch.sh — open a real terminal window (Terminal.app by default) and run a
# command there, from inside a Claude Code session.
#
# Why this exists (DE-1/DE-3 findings, 2026-06-23 / 2026-07-18):
#   - A nested `claude -p` spawned directly inside a Claude Code session 401s — the
#     host-managed OAuth is not inherited by a child process.
#   - Worse, `open -a Terminal` from a Claude Code session PROPAGATES the session's
#     env (CLAUDECODE, CLAUDE_CODE_*, ANTHROPIC_BASE_URL, …) into the launched app,
#     so even a "real terminal" window can be contaminated. The snippet therefore
#     scrubs the environment with `env -i` and rebuilds it via a fresh zsh LOGIN
#     shell — the payload runs exactly as if Matt typed it in a new terminal.
#
# Usage:
#   bash scripts/term-launch.sh <command string...>
#   bash scripts/term-launch.sh --iterm <command string...>   # iTerm2 tab instead
# Examples:
#   bash scripts/term-launch.sh 'python3 working/dunk-egg-pass1/dunk-egg-pass1-extraction.py --smoke --only thk --prompt-version v4b'
#   bash scripts/term-launch.sh 'bash scripts/weirwood-run.sh start dunk-egg-pass1'
#
# Mechanisms:
#   default — `open -a Terminal <snippet>`: needs NO automation permission; proven.
#   --iterm — AppleScript tab in iTerm2: nicer, but requires the one-time macOS
#             automation consent (TCC) for the calling app to control iTerm2. If
#             that consent is not granted the Apple Event times out (~2 min hang);
#             this flag is opt-in for that reason.
#
# Every launch writes a timestamped snippet to working/logs/term-launch/ (audit
# trail + sidesteps AppleScript quoting). The snippet cd's to the repo root, then
# execs the payload under `env -i … zsh -lc`.
#
# Policy: nothing that fires an extraction goes through here without Matt's
# explicit go (feedback_no_extraction_without_asking).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

USE_ITERM=0
if [[ "${1:-}" == "--iterm" ]]; then
    USE_ITERM=1
    shift
fi

if [[ $# -lt 1 ]]; then
    echo "usage: bash scripts/term-launch.sh [--iterm] <command string...>" >&2
    exit 1
fi

LAUNCH_DIR="$REPO_ROOT/working/logs/term-launch"
mkdir -p "$LAUNCH_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
SNIP="$LAUNCH_DIR/$STAMP.sh"
PAYLOAD="$LAUNCH_DIR/$STAMP-payload.sh"

# Payload: what actually runs, in a clean login-shell environment.
{
    echo "#!/usr/bin/env zsh"
    echo "# term-launch payload — $STAMP"
    echo "cd \"$REPO_ROOT\""
    printf '%s\n' "$*"
} > "$PAYLOAD"
chmod +x "$PAYLOAD"

# Snippet: the file the terminal opens. Scrubs env, then runs the payload via a
# fresh zsh login shell (zprofile/path_helper rebuild the real PATH; `claude`
# authenticates from Matt's own credentials, not the Claude Code session's).
{
    echo "#!/usr/bin/env bash"
    echo "# term-launch snippet — $STAMP (env-scrubbed; payload: $PAYLOAD)"
    echo "exec env -i HOME=\"\$HOME\" USER=\"\$USER\" LOGNAME=\"\$USER\" SHELL=/bin/zsh TERM=\"\${TERM:-xterm-256color}\" LANG=\"\${LANG:-en_US.UTF-8}\" /bin/zsh -lc '\"$PAYLOAD\"'"
} > "$SNIP"
chmod +x "$SNIP"

if [[ "$USE_ITERM" -eq 1 ]]; then
    osascript <<EOF
with timeout of 15 seconds
    tell application "iTerm"
        activate
        if (count of windows) = 0 then
            create window with default profile
        else
            tell current window
                create tab with default profile
            end tell
        end if
        tell current session of current window
            write text "bash ${SNIP}"
        end tell
    end tell
end timeout
EOF
    echo "Launched in iTerm2 tab. Snippet: $SNIP"
else
    open -a Terminal "$SNIP"
    echo "Launched in Terminal.app window. Snippet: $SNIP"
fi
