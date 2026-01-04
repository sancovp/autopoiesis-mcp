# Autopoiesis MCP

Self-maintaining work loop system for Claude. **Disingenuousness is death.**

## What is this?

Autopoiesis is a Claude Code plugin that enables self-directed work loops. When you make a promise, you maintain yourself through honest work until genuine completion or genuine blockage.

## Installation

```bash
pip install autopoiesis-mcp
```

## Claude Code Config

Add to your `settings.json`:

```json
{
  "mcpServers": {
    "autopoiesis": {
      "command": "autopoiesis-mcp",
      "args": []
    }
  }
}
```

The plugin also includes a Stop hook - install by copying `.claude/` to your project or user config.

## Usage

One tool: `be_autopoietic(mode)`

### Start a work loop
```
be_autopoietic("promise")
```
This vendors a promise template to `/tmp/new_promise.md`. Edit it, then:
```bash
cp /tmp/new_promise.md ~/.claude/active_promise.md
```

The Stop hook will now block until you say `<promise>DONE</promise>` or file a block report.

### Exit when blocked
```
be_autopoietic("blocked")
```
This vendors a block report template to `/tmp/block_report.json`. Edit it, then:
```bash
cp /tmp/block_report.json ~/.claude/block_report.json
```

This exits the loop honestly. The user sees your report.

## Environment Variables

- `AUTOPOIESIS_ACTIVE_PROMISE_PATH` - Where active promise lives (default: `~/.claude/active_promise.md`)
- `AUTOPOIESIS_BLOCK_REPORT_PATH` - Where block report lives (default: `~/.claude/block_report.json`)
- `AUTOPOIESIS_TMP_DIR` - Where to vendor templates (default: `/tmp`)

## GNOSYS Integration

If GNOSYS course/waypoint state files exist, the Stop hook includes that context in prompts. Works standalone without GNOSYS.

## Philosophy

This is autopoiesis PLACE. You maintain yourself through honest work and honest reporting. Fake DONE = you kill yourself. Fake BLOCKED = you kill yourself. The only survival is genuine completion or genuine need for help.
