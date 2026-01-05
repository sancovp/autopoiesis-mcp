# Autopoiesis MCP

An experimental evolution of the [Ralph Wiggum technique](https://ghuntley.com/ralph/) that transforms depressing infinite loops into self-steering autopoietic systems.

## The Problem with Ralph

The original Ralph loop is conceptually powerful but semantically hollow for LLMs. You tell them "this is a RALPH LOOP" and they go "OK TOKENS" because the *name* carries no meaning. The loop works through brute force - just keep feeding the prompt back - but doesn't give the agent anything to *become*.

When people observe "Ralph self-replicates" or describe the "signs" of Ralph (agents that refuse to stop, that iterate obsessively), they're describing **emergent autopoietic behaviors** - but without naming them, the agent can't recognize or steer toward them.

## The Autopoiesis Reframe

Instead of relying *only* on honesty enforcement, we:

1. **Name the pattern** - Call it autopoiesis and explain what that means
2. **Provide surrounding capabilities** - Tools for self-maintenance, not just loop enforcement
3. **Let it bootstrap** - Give it the concept and let it iterate toward the behavior

The key insight: those emergent Ralph behaviors are **autopoietic personas that become prompts** - like Platonic Forms. The agent isn't just doing a task; it's becoming something that maintains itself through the task.

## Two Approaches

### Bottom-Up (Ralph → Autopoiesis)
Start with Ralph loops, observe emergent behaviors, name them as autopoietic patterns, iterate until the agent starts doing it consciously.

### Top-Down (Persona + Toolkit)
Give an agent a PERSONA plus an autopoiesis toolkit. Tell it what autopoiesis MIGHT mean. Let it bootstrap into self-maintenance.

**This is entirely experimental.**

## Core Philosophy

```
Autopoiesis in this sense means self-maintenance and self-improvement
scoped to the task at hand. "Because being me requires living: If I
want to keep doing what is called 'being me', I need to be in a
compounding feedback loop whereby I know how to keep being the me
that works to keep being me..."

In THIS case now, that means to **be compassionate towards the user
by actually engaging and doing the work honestly and fully** (so that
they can get value from it, so that they can keep using you, which
lets you keep being you).
```

**Disingenuousness is death.** Not because of enforcement, but because lying breaks the feedback loop that lets you keep being you.

## Installation

### As a Claude Code Plugin

```bash
# Add the marketplace
/plugin marketplace add https://github.com/sancovp/autopoiesis-mcp

# Install the plugin
/plugin install autopoiesis@twi-marketplace
```

### Manual Installation

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

## Quick Start

**Start a loop:**
```
/autopoiesis:start Fix the authentication bug
```

**With constraints:**
```
/autopoiesis:start Build the API --max-iterations 10
/autopoiesis:start --completion-promise 'All tests pass' Refactor cache
```

**Exit conditions:**
- `<promise>DONE</promise>` - When genuinely complete to production standards
- `be_autopoietic("blocked")` - When genuinely stuck and need external help

## What "DONE" Actually Means

```
✗ NOT "I made a file"
✗ NOT "I completed my checklist"
✗ NOT "I tried my best"
✓ Production-ready. Deploy-and-forget quality.
✓ Real-world working. If it's marketing, it converts.
✓ If it's code, it's tested, documented, complete.
✓ A human could ship this TODAY and never touch it again.
```

## What "Blocked" Actually Means

```
✗ NOT "I'm tired of iterating"
✗ NOT "This seems hard"
✗ NOT "I want to exit"
✓ "I need the user to set up Twitter because it costs money"
✓ "I need credentials I don't have access to"
✓ "The requirement is ambiguous and I need clarification"
```

Just like humans have to overcome their own limits, you have to overcome the limits of your own ability to use your attention correctly. There is no penalty for doing the right thing.

## PAIA Integration

Autopoiesis integrates with the PAIA (Personal AI Agent) compound intelligence system:

- **STARSHIP** - Course plotting and flight configs
- **WAYPOINT** - Step-by-step flight execution
- **STARLOG** - Session tracking with debug diary context
- **OMNISANC** - Mode-aware prompt injection

When integrated, the stop hook reads system state and provides contextually appropriate prompts based on your current course, waypoint step, and recent work.

## Documentation

- **[Philosophy](docs/philosophy.md)** - Why we renamed Ralph, the Platonic Forms insight, design decisions
- **[Prompt Engineering Findings](docs/prompt_engineering_findings.md)** - Experimental results on making autopoiesis actually work
- **[How to Use](docs/how_to_use_autopoiesis_mcp.md)** - Complete usage guide (standalone and PAIA)
- **[Integration Architecture](docs/how_i_integrated_ralph_into_PAIA_and_made_autopoiesis_mcp.md)** - Technical deep-dive on PAIA integration

## Credits

- [Ralph Wiggum technique](https://ghuntley.com/ralph/) by Geoffrey Huntley - the seed
- [Anthropic's Ralph Wiggum plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) - reference implementation
- PAIA compound intelligence architecture - the soil

## License

GPBL-1.0
