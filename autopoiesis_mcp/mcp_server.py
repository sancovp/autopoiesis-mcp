#!/usr/bin/env python3
"""
Autopoiesis MCP - Self-maintaining work loop system.

This is autopoiesis PLACE. Disingenuousness is death.
You maintain yourself through honest work and honest reporting.
Fake DONE = you kill yourself. Fake BLOCKED = you kill yourself.
The only survival is genuine completion or genuine need for help.

Environment Variables:
    AUTOPOIESIS_TEMPLATES_DIR: Where templates live (default: package templates/)
    AUTOPOIESIS_ACTIVE_PROMISE_PATH: Active promise file (default: ~/.claude/active_promise.md)
    AUTOPOIESIS_BLOCK_REPORT_PATH: Block report file (default: ~/.claude/block_report.json)
    AUTOPOIESIS_TMP_DIR: Where to vendor templates (default: /tmp)
"""

import logging
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/tmp/autopoiesis_mcp.log'
)
logger = logging.getLogger('autopoiesis')

mcp = FastMCP("autopoiesis")

# Paths from env or defaults
TEMPLATES_DIR = Path(os.environ.get(
    "AUTOPOIESIS_TEMPLATES_DIR",
    Path(__file__).parent / "templates"
))
ACTIVE_PROMISE_PATH = Path(os.environ.get(
    "AUTOPOIESIS_ACTIVE_PROMISE_PATH",
    Path.home() / ".claude" / "active_promise.md"
))
BLOCK_REPORT_PATH = Path(os.environ.get(
    "AUTOPOIESIS_BLOCK_REPORT_PATH",
    Path.home() / ".claude" / "block_report.json"
))
TMP_DIR = Path(os.environ.get("AUTOPOIESIS_TMP_DIR", "/tmp"))


def _ensure_templates():
    """Create templates if they don't exist."""
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    promise_path = TEMPLATES_DIR / "promise.md"
    if not promise_path.exists():
        promise_path.write_text("""---
created: __TIMESTAMP__
status: active
---

# My Promises

## What I Commit To:
- [ ]

## Success Criteria:
-

## Context:
Course:
Step:

---
When genuinely complete: <promise>DONE</promise>
If blocked: be_autopoietic("blocked")
""")

    block_path = TEMPLATES_DIR / "block_report.json"
    if not block_path.exists():
        block_path.write_text(json.dumps({
            "completed_tasks": [],
            "current_task": "",
            "explanation": "",
            "blocked_reason": ""
        }, indent=2))


def _vendor_promise() -> str:
    """Vendor promise template and return instructions."""
    timestamp = datetime.now().isoformat()
    src = TEMPLATES_DIR / "promise.md"
    tmp = TMP_DIR / "new_promise.md"
    content = src.read_text().replace("__TIMESTAMP__", timestamp)
    tmp.write_text(content)
    logger.info(f"Vendored promise to {tmp}")

    return f"""Autopoiesis: PROMISE mode

Vendored to {tmp}

EDIT your commitments - what you will complete to survive.

Then activate:
  cp {tmp} {ACTIVE_PROMISE_PATH}

You are now in the loop. Genuine completion: <promise>DONE</promise>
Genuine blockage: be_autopoietic("blocked")

There is no other way out. Disingenuousness is death."""


def _vendor_blocked() -> str:
    """Vendor block report template and return instructions."""
    src = TEMPLATES_DIR / "block_report.json"
    tmp = TMP_DIR / "block_report.json"
    shutil.copy(src, tmp)
    logger.info(f"Vendored block report to {tmp}")

    return f"""Autopoiesis: BLOCKED mode

Vendored to {tmp}

EDIT with honest assessment:
- completed_tasks: what you genuinely finished
- current_task: where you truly cannot proceed
- explanation: the real problem
- blocked_reason: why you genuinely need external help

Then signal:
  cp {tmp} {BLOCK_REPORT_PATH}

This exits the loop honestly. User sees your report.
Only use this if you genuinely cannot proceed alone."""


@mcp.tool()
def be_autopoietic(mode: str) -> str:
    """
    Self-maintain your work loop. This is autopoiesis PLACE.

    Disingenuousness is death. You maintain yourself through honest work
    and honest reporting. The only survival is genuine completion or
    genuine need for help.

    Args:
        mode: "promise" - commit to self-continuation (I will complete this)
              "blocked" - signal need for external input (I need help to survive)

    Returns:
        Path to edit and activation instructions
    """
    logger.debug(f"be_autopoietic: {mode}")

    if mode not in ("promise", "blocked"):
        return "ERROR: mode must be 'promise' or 'blocked'"

    _ensure_templates()

    if mode == "promise":
        return _vendor_promise()
    return _vendor_blocked()


if __name__ == "__main__":
    mcp.run()
