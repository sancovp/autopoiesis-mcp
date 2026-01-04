#!/bin/bash

# Autopoiesis Setup Script
# Creates state file for promise-based work loop

set -euo pipefail

PROMPT_PARTS=()
MAX_ITERATIONS=0
COMPLETION_PROMISE="DONE"

while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      cat << 'HELP_EOF'
Autopoiesis - Self-maintaining promise-based work loop

USAGE:
  /autopoiesis:start [PROMPT...] [OPTIONS]

ARGUMENTS:
  PROMPT...    The promise/task you commit to completing

OPTIONS:
  --max-iterations <n>           Maximum iterations before auto-stop (default: unlimited)
  --completion-promise '<text>'  Custom completion phrase (default: DONE)
  -h, --help                     Show this help message

EXAMPLES:
  /autopoiesis:start Fix the authentication bug
  /autopoiesis:start Build the API --max-iterations 10
  /autopoiesis:start --completion-promise 'All tests pass' Refactor cache
HELP_EOF
      exit 0
      ;;
    --max-iterations)
      if [[ -z "${2:-}" ]] || ! [[ "$2" =~ ^[0-9]+$ ]]; then
        echo "Error: --max-iterations requires a positive integer" >&2
        exit 1
      fi
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    --completion-promise)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --completion-promise requires a text argument" >&2
        exit 1
      fi
      COMPLETION_PROMISE="$2"
      shift 2
      ;;
    *)
      PROMPT_PARTS+=("$1")
      shift
      ;;
  esac
done

PROMPT="${PROMPT_PARTS[*]}"

if [[ -z "$PROMPT" ]]; then
  echo "Error: No promise provided" >&2
  echo "Example: /autopoiesis:start Fix the auth bug" >&2
  exit 1
fi

cat > /tmp/active_promise.md <<EOF
---
created: $(date -u +%Y-%m-%dT%H:%M:%SZ)
status: active
iteration: 1
max_iterations: $MAX_ITERATIONS
completion_promise: "$COMPLETION_PROMISE"
---

$PROMPT
EOF

cat <<EOF
🔄 Ralph loop activated in this session!

Iteration: 1
Max iterations: $(if [[ $MAX_ITERATIONS -gt 0 ]]; then echo $MAX_ITERATIONS; else echo "unlimited"; fi)
Completion promise: $(if [[ "$COMPLETION_PROMISE" != "null" ]]; then echo "${COMPLETION_PROMISE//\"/} (ONLY output when TRUE - do not lie!)"; else echo "none (runs forever)"; fi)

The stop hook is now active. When you try to exit, the SAME PROMPT will be
fed back to you. You'll see your previous work in files, creating a
self-referential loop where you iteratively improve on the same task.

To monitor: cat /tmp/active_promise.md

⚠️  WARNING: This loop cannot be stopped manually! It will run infinitely
    unless you set --max-iterations or --completion-promise.

🔄
EOF

echo ""
echo "$PROMPT"
