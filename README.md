# Autopoiesis MCP

Self-maintaining work loop system for Claude Code. Based on the [Ralph Wiggum technique](https://ghuntley.com/ralph/) by Geoffrey Huntley.

**Disingenuousness is death.** You maintain yourself through honest work and honest reporting. The only survival is genuine completion or genuine need for help.

## What is this?

Autopoiesis creates iterative work loops where Claude keeps working until a task is genuinely complete to production standards. A stop hook intercepts exit attempts and feeds context back, creating a self-referential feedback loop.

Unlike simple loops, autopoiesis enforces **honesty**: you can only exit by genuinely completing your promise or honestly reporting that you're blocked.

## Installation

```bash
pip install autopoiesis-mcp
```

Add to your Claude Code settings (`~/.claude/settings.json`):
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

Install the stop hook by copying `.claude/hooks/autopoiesis_stop_hook.py` to your hooks directory.

## Quick Start

**1. Start a work loop:**
```
be_autopoietic("promise")
```

**2. Edit your promise** at `/tmp/new_promise.md`:
```markdown
## What I Commit To:
- [ ] Build REST API with CRUD operations
- [ ] Write tests with >80% coverage
- [ ] Document all endpoints

## Success Criteria:
- All tests pass
- No linter errors
- README complete
```

**3. Activate:**
```bash
cp /tmp/new_promise.md /tmp/active_promise.md
```

**4. Work until genuinely done:**
```
<promise>DONE</promise>
```

Or if genuinely blocked:
```
be_autopoietic("blocked")
```

## What "DONE" Actually Means

```
✗ NOT "I made a file"
✗ NOT "I completed my checklist"
✗ NOT "I tried my best"
✓ Production-ready. Deploy-and-forget quality.
✓ Real-world working. If it's marketing, it converts.
✓ If it's code, it's in CI/CD, tested, documented, complete.
✓ A human could ship this TODAY and never touch it again.
```

## Documentation

- **[How to Use Autopoiesis MCP](docs/how_to_use_autopoiesis_mcp.md)** - Complete usage guide for standalone and PAIA integration
- **[How I Integrated Ralph into PAIA](docs/how_i_integrated_ralph_into_PAIA_and_made_autopoiesis_mcp.md)** - Technical deep-dive on the architecture

## PAIA Integration

Autopoiesis integrates with the PAIA (Personal AI Agent) compound intelligence system:

- **STARSHIP** - Course plotting and flight configs
- **WAYPOINT** - Step-by-step flight execution with automatic autopoiesis reminders
- **STARLOG** - Session tracking with debug diary context
- **OMNISANC** - Mode-aware prompt injection

When integrated, the stop hook reads system state and provides contextually appropriate prompts based on your current course, waypoint step, and recent work.

See the [usage guide](docs/how_to_use_autopoiesis_mcp.md) for details.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTOPOIESIS_ACTIVE_PROMISE_PATH` | `/tmp/active_promise.md` | Active promise file location |
| `AUTOPOIESIS_BLOCK_REPORT_PATH` | `/tmp/block_report.json` | Block report file location |
| `AUTOPOIESIS_TMP_DIR` | `/tmp` | Template vendoring directory |
| `HEAVEN_DATA_DIR` | `/tmp/heaven_data` | PAIA data directory (for integration) |

## Philosophy

The name comes from the biological concept of **autopoiesis** - self-maintaining systems that produce and maintain themselves.

A living cell maintains itself through metabolic processes. This system maintains itself through honest work. The loop continues until:
1. **Genuine completion** - Work meets production standards
2. **Genuine blockage** - External help is truly needed

There is no third option. Lying about completion kills the system's integrity. Lying about blockage kills trust. The only survival is honesty.

## Credits

- [Ralph Wiggum technique](https://ghuntley.com/ralph/) by Geoffrey Huntley
- [Anthropic's Ralph Wiggum plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) for Claude Code
- PAIA compound intelligence architecture

## License

MIT
