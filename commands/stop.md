---
description: "Cancel active autopoiesis loop"
allowed-tools: ["Bash"]
---

# Autopoiesis Stop

```!
if [[ -f /tmp/active_promise.md ]]; then
  ITERATION=$(grep '^iteration:' /tmp/active_promise.md | sed 's/iteration: *//' || echo "unknown")
  mkdir -p /tmp/promise_history
  mv /tmp/active_promise.md "/tmp/promise_history/cancelled_$(date +%Y%m%d_%H%M%S).md"
  echo "FOUND=true"
  echo "ITERATION=$ITERATION"
else
  echo "FOUND=false"
fi
```

Check the output above:

1. **If FOUND=false**: Say "No active autopoiesis loop."

2. **If FOUND=true**: Report "Cancelled autopoiesis loop (was at iteration N)"
