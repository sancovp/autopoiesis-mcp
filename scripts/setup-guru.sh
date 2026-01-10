#!/bin/bash
# Setup guru loop - creates /tmp/guru_loop.md with task content
# Usage: setup-guru.sh "task description"

TASK="$*"

if [ -z "$TASK" ]; then
    echo "ERROR: No task provided"
    echo "Usage: setup-guru.sh \"task description\""
    exit 1
fi

# Create guru loop file
cat > /tmp/guru_loop.md << EOF
---
created: $(date -Iseconds)
status: active
---

# Guru Loop Task

$TASK
EOF

echo "Guru loop activated at /tmp/guru_loop.md"
echo "Task: $TASK"
echo ""
echo "The stop hook will now enforce the bodhisattva vow."
echo "You must complete the task AND build an emanation."
echo "Exit with <vow>ABSOLVED</vow> when ready for samaya gate."
