#!/usr/bin/env python3
"""
Super-Ralph Stop Hook - Mode-aware continuity enforcement for GNOSYS

Unlike original Ralph (same prompt forever), Super-Ralph reads system state
and injects contextually appropriate prompts based on omnisanc mode.

Modes:
- HOME: No course plotted, suggest plotting one
- STARPORT: Course plotted, no waypoint journey started
- SESSION: Active waypoint journey, inject step context
- LANDING: Session ended, needs review
- MISSION: Multi-session mission active
"""

import json
import logging
import os
import sys
import traceback
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='/tmp/super_ralph_hook.log'
)
logger = logging.getLogger('super_ralph')

# State file locations
COURSE_STATE_FILE = "/tmp/heaven_data/omnisanc_core/.course_state"
LOOP_PROMPT_FILE = ".claude/super-ralph-loop.md"
HEAVEN_DATA_DIR = os.environ.get("HEAVEN_DATA_DIR", "/tmp/heaven_data")

# Ralph promise/blocked paths
ACTIVE_PROMISE_PATH = Path.home() / ".claude" / "active_promise.md"
BLOCK_REPORT_PATH = Path.home() / ".claude" / "block_report.json"


def get_course_state() -> dict:
    """Read omnisanc course state."""
    try:
        if os.path.exists(COURSE_STATE_FILE):
            with open(COURSE_STATE_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def get_waypoint_state(project_path: str) -> dict:
    """Read waypoint state for a project."""
    try:
        project_name = os.path.basename(project_path.rstrip('/'))
        waypoint_file = f"/tmp/waypoint_state_{project_name}.json"
        if os.path.exists(waypoint_file):
            with open(waypoint_file, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def get_recent_debug_diary(project_path: str, n: int = 3) -> list:
    """Get last N debug diary entries."""
    try:
        project_name = os.path.basename(project_path.rstrip('/'))
        registry_path = f"{HEAVEN_DATA_DIR}/registry/{project_name}_debug_diary_registry.json"

        if not os.path.exists(registry_path):
            return []

        with open(registry_path, 'r') as f:
            registry = json.load(f)

        # Get entries sorted by timestamp (newest first)
        entries = []
        for entry_id, entry in registry.items():
            if isinstance(entry, dict) and 'content' in entry:
                entries.append(entry)

        entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

        # Return last N entries (content only)
        return [e.get('content', '')[:200] for e in entries[:n]]

    except Exception:
        pass
    return []


def get_loop_prompt() -> tuple:
    """Read user's loop prompt file if exists. Returns (active, prompt_text)."""
    try:
        if os.path.exists(LOOP_PROMPT_FILE):
            with open(LOOP_PROMPT_FILE, 'r') as f:
                content = f.read()

            # Parse YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    prompt_text = parts[2].strip()

                    # Check if active
                    if 'active: false' in frontmatter:
                        return False, ""

                    return True, prompt_text
    except Exception:
        pass
    return False, ""


def get_active_promise() -> tuple:
    """Read active promise file. Returns (active, promise_content)."""
    try:
        if ACTIVE_PROMISE_PATH.exists():
            content = ACTIVE_PROMISE_PATH.read_text()
            logger.debug("Active promise found")
            return True, content
    except Exception as e:
        logger.error(f"Error reading promise: {e}\n{traceback.format_exc()}")
    return False, ""


def check_block_report() -> tuple:
    """Check if block report exists. Adds timestamp if missing. Returns (blocked, report_content)."""
    try:
        if BLOCK_REPORT_PATH.exists():
            content = BLOCK_REPORT_PATH.read_text()
            report = json.loads(content)

            # Add timestamp if missing (distributed logic - MCP vendors, hook timestamps)
            if "timestamp" not in report:
                report["timestamp"] = datetime.now().isoformat()
                BLOCK_REPORT_PATH.write_text(json.dumps(report, indent=2))
                logger.debug("Added timestamp to block report")

            logger.debug("Block report found")
            return True, json.dumps(report, indent=2)
    except Exception as e:
        logger.error(f"Error reading block report: {e}\n{traceback.format_exc()}")
    return False, ""


def check_done_in_transcript(transcript_path: str) -> bool:
    """Check if last assistant message contains <promise>DONE</promise>."""
    try:
        if not transcript_path or not os.path.exists(transcript_path):
            return False

        with open(transcript_path, 'r') as f:
            lines = f.readlines()

        # Read last few lines looking for assistant message with DONE
        for line in reversed(lines[-20:]):
            try:
                entry = json.loads(line.strip())
                if entry.get("type") == "assistant":
                    message = entry.get("message", {})
                    content = message.get("content", [])
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            if "<promise>DONE</promise>" in block.get("text", ""):
                                logger.debug("Found <promise>DONE</promise> in transcript")
                                return True
            except json.JSONDecodeError:
                continue
    except Exception as e:
        logger.error(f"Error checking transcript for DONE: {e}\n{traceback.format_exc()}")
    return False


def clear_promise_file() -> None:
    """Clear the active promise file after DONE detected."""
    try:
        if ACTIVE_PROMISE_PATH.exists():
            # Archive it
            archive_dir = Path.home() / ".claude" / "promise_history"
            archive_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = archive_dir / f"completed_{timestamp}.md"
            ACTIVE_PROMISE_PATH.rename(archive_path)
            logger.info(f"Promise archived to {archive_path}")
    except Exception as e:
        logger.error(f"Error clearing promise: {e}\n{traceback.format_exc()}")


def determine_mode(course: dict, waypoint: dict) -> str:
    """Determine current mode from state."""
    if not course.get("course_plotted"):
        return "HOME"

    if course.get("needs_review"):
        return "LANDING"

    # Check waypoint state FIRST - SESSION takes priority over MISSION
    # (mission is the container, session is active work within it)
    if waypoint.get("status") == "IN_PROGRESS":
        return "SESSION"

    if waypoint.get("status") == "END":
        return "LANDING"

    # Mission active but no waypoint journey started yet
    if course.get("mission_active"):
        return "MISSION"

    # Course plotted but no waypoint journey
    return "STARPORT"


def format_home_prompt() -> str:
    """Format prompt for HOME mode."""
    return """You're at HOME.

Available actions:
- starship.plot_course() to start a journey
- Review missions with STARSYSTEM tools

What would you like to work on?"""


def format_starport_prompt(course: dict) -> str:
    """Format prompt for STARPORT mode."""
    project = course.get("projects", ["unknown"])[0] if course.get("projects") else "unknown"
    description = course.get("description", "")

    return f"""Course plotted to: {project}
Description: {description}

You've set a course. Now select a flight config and start:
- Use starship.fly() to browse available flight configs
- Use waypoint.start_waypoint_journey(config_path, starlog_path) to begin

Continue."""


def _build_course_lines(course: dict) -> list:
    """Build course info lines."""
    project = course.get("projects", ["unknown"])[0] if course.get("projects") else "unknown"
    domain_str = course.get("domain", "")
    if course.get("subdomain"):
        domain_str += f"/{course['subdomain']}"
    description = course.get("description", "")
    return [
        f"Course: {project}",
        f"   Domain: {domain_str}",
        f"   Description: {description}",
    ]


def _build_waypoint_lines(waypoint: dict) -> list:
    """Build waypoint info lines."""
    config_name = waypoint.get("config_filename", "unknown")
    current_step = waypoint.get("completed_count", 0)
    total_steps = waypoint.get("total_waypoints", 0)
    step_file = waypoint.get("last_served_file", "")
    return [
        "",
        f"Flight: {config_name} (step {current_step}/{total_steps})",
        f"Step: {step_file}",
        "   -> Call get_current_step_content() for full instructions if needed",
    ]


def _build_diary_lines(diary_entries: list) -> list:
    """Build debug diary lines."""
    if not diary_entries:
        return []
    lines = ["", "Recent Debug Diary:"]
    for entry in diary_entries:
        clean_entry = entry.replace('\n', ' ')[:150]
        lines.append(f"  - {clean_entry}")
    return lines


def _build_navigation_lines() -> list:
    """Build navigation instruction lines."""
    return [
        "",
        "---",
        "If step complete -> call waypoint.navigate_to_next_waypoint()",
        "If flight complete -> review ALL steps, only <promise>DONE</promise> when verified",
        "If issues found -> call waypoint.reset_waypoint_journey() and run through again",
        "",
        "Continue."
    ]


def format_session_prompt(course: dict, waypoint: dict, diary_entries: list, loop_prompt: str) -> str:
    """Format prompt for SESSION mode (active waypoint journey)."""
    lines = _build_course_lines(course)
    lines.extend(_build_waypoint_lines(waypoint))
    lines.extend(_build_diary_lines(diary_entries))

    # Add user's loop prompt
    lines.append("")
    if loop_prompt:
        lines.append("Your Task:")
        lines.append(loop_prompt)
    else:
        lines.append("Continue working on the current step.")

    lines.extend(_build_navigation_lines())
    return "\n".join(lines)


def format_landing_prompt(course: dict) -> str:
    """Format prompt for LANDING mode."""
    return """LANDING SEQUENCE REQUIRED

Session has ended. Complete the 3-step landing sequence:
1. -> starship.landing_routine()
2. starship.session_review()
3. giint.respond()

You are on step 1. Begin landing sequence.

Continue."""


def format_mission_prompt(course: dict) -> str:
    """Format prompt for MISSION mode."""
    mission_id = course.get("mission_id", "unknown")
    mission_step = course.get("mission_step", 0)

    return f"""Mission: {mission_id} (step {mission_step})

Multi-session mission active. Options:
- Start next session with waypoint.start_waypoint_journey()
- Complete mission with STARSYSTEM.complete_mission()

What would you like to do?

Continue."""


def _output_approve():
    """Output approve decision and exit."""
    print(json.dumps({"decision": "approve"}))
    sys.exit(0)


def _output_block(prompt: str, mode: str):
    """Output block decision with prompt and exit."""
    result = {
        "decision": "block",
        "reason": prompt,
        "systemMessage": f"Super-Ralph: {mode} mode | To exit: <promise>DONE</promise> when genuinely complete"
    }
    print(json.dumps(result))
    sys.exit(0)


def _get_prompt_for_mode(mode: str, course: dict, waypoint: dict, project_path: str, loop_prompt: str) -> str:
    """Get the appropriate prompt for the current mode."""
    if mode == "HOME":
        return format_home_prompt()
    elif mode == "STARPORT":
        return format_starport_prompt(course)
    elif mode == "SESSION":
        diary_entries = get_recent_debug_diary(project_path) if project_path else []
        return format_session_prompt(course, waypoint, diary_entries, loop_prompt)
    elif mode == "LANDING":
        return format_landing_prompt(course)
    elif mode == "MISSION":
        return format_mission_prompt(course)
    return ""


def _build_promise_prompt(promise_content: str, course: dict, waypoint: dict) -> str:
    """Build prompt when promise is active."""
    lines = ["ACTIVE PROMISE:", ""]
    lines.append(promise_content[:500])  # Truncate if too long
    lines.append("")
    lines.append("---")

    # Add course context if available
    if course.get("course_plotted"):
        lines.extend(_build_course_lines(course))

    # Add waypoint context if available
    if waypoint.get("status") == "IN_PROGRESS":
        lines.extend(_build_waypoint_lines(waypoint))

    lines.append("")
    lines.append("Is this genuinely complete? <promise>DONE</promise> to confirm.")
    lines.append("Blocked? Use vendor_template('blocked') to exit honestly.")

    return "\n".join(lines)


def _get_system_state() -> tuple:
    """Get course, project_path, waypoint, and mode."""
    course = get_course_state()
    project_path = course["projects"][0] if course.get("projects") else ""
    waypoint = get_waypoint_state(project_path) if project_path else {}
    mode = determine_mode(course, waypoint)
    return course, project_path, waypoint, mode


def _handle_promise_check(course: dict, waypoint: dict) -> None:
    """Check for active promise and block if found."""
    promise_active, promise_content = get_active_promise()
    if promise_active:
        prompt = _build_promise_prompt(promise_content, course, waypoint)
        logger.debug("Blocking with active promise")
        _output_block(prompt, "PROMISE")


def _handle_mode_check(mode: str, course: dict, waypoint: dict, project_path: str) -> None:
    """Handle mode-based blocking logic."""
    loop_active, loop_prompt = get_loop_prompt()

    if not loop_active and mode not in ["SESSION"]:
        logger.debug("No loop active and not SESSION, approving stop")
        _output_approve()

    prompt = _get_prompt_for_mode(mode, course, waypoint, project_path, loop_prompt)
    if not prompt:
        logger.debug(f"No prompt for mode {mode}, approving stop")
        _output_approve()

    logger.debug(f"Blocking stop with {mode} prompt")
    _output_block(prompt, mode)


def main():
    try:
        hook_input = json.load(sys.stdin)
        logger.debug(f"Hook input received: {hook_input}")

        transcript_path = hook_input.get("transcript_path", "")

        # Check for <promise>DONE</promise> in transcript - if found, clear promise and approve
        if check_done_in_transcript(transcript_path):
            logger.debug("DONE found in transcript, clearing promise and approving")
            clear_promise_file()
            _output_approve()

        # Check for block report - if exists, allow exit
        blocked, _ = check_block_report()
        if blocked:
            logger.debug("Block report found, approving stop")
            _output_approve()

        course, project_path, waypoint, mode = _get_system_state()
        logger.debug(f"Determined mode: {mode}")

        _handle_promise_check(course, waypoint)
        _handle_mode_check(mode, course, waypoint, project_path)

    except Exception as e:
        logger.error(f"Super-Ralph hook error: {e}\n{traceback.format_exc()}")
        _output_approve()


if __name__ == "__main__":
    main()
