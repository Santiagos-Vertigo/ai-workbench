#!/usr/bin/env python3
"""Workbench Console — read-only status reporter.

Implements exactly the v0.8 MVP defined by docs/console-specification.md: a single,
dependency-free, stdlib-only, stateless command that reports Workbench and repository
state to stdout/stderr. It never modifies anything, never launches anything, never
selects a workflow, and never grants scope or authorization.
"""

import sys

sys.dont_write_bytecode = True

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")
del _stream

import os
import re
import subprocess
from pathlib import Path

PROGRAM = "workbench.py"

INSTRUCTION_FILENAMES = ["README.md", "CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md"]
STATE_FILE_DISCOVERY_ORDER = ["WORKBENCH_STATE.md", "PROJECT_STATE.md"]

# Git Subprocess Safeguards — docs/console-specification.md, "Git Subprocess Safeguards".
GIT_ENV_OVERRIDES = {
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
    "GIT_NO_LAZY_FETCH": "1",
}
GIT_SUBPROCESS_TIMEOUT_SECONDS = 10


def usage() -> str:
    return f"usage: python {PROGRAM} status <repository-path>"


def run_git(repo_path: Path, args: list[str]) -> tuple[bool, str]:
    """Run a single read-only git subprocess against repo_path.

    No fetch, no push, no authentication, no terminal prompts, no optional locking or
    index refresh, no lazy remote fetching, stdin unavailable, no shell construction —
    per the specification's Git Subprocess Safeguards. Returns (ok, stripped stdout).
    """
    env = dict(os.environ)
    env.update(GIT_ENV_OVERRIDES)
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), *args],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            timeout=GIT_SUBPROCESS_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return False, ""
    if result.returncode != 0:
        return False, ""
    return True, result.stdout.strip()


def git_is_repository(repo_path: Path) -> bool:
    ok, _ = run_git(repo_path, ["rev-parse", "--git-dir"])
    return ok


def git_branch(repo_path: Path) -> str:
    ok, out = run_git(repo_path, ["branch", "--show-current"])
    if not ok:
        return "unavailable"
    return out if out else "detached HEAD"


def git_head_commit(repo_path: Path) -> str:
    ok, out = run_git(repo_path, ["log", "-1", "--format=%h %s"])
    if not ok:
        return "no commits yet"
    return out


def git_working_tree(repo_path: Path) -> str:
    ok, out = run_git(repo_path, ["status", "--porcelain"])
    if not ok:
        return "unavailable"
    if not out:
        return "clean"
    changed = len(out.splitlines())
    return f"dirty ({changed} changed path{'s' if changed != 1 else ''})"


def git_ahead_behind(repo_path: Path) -> str:
    has_upstream, _ = run_git(
        repo_path, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]
    )
    if not has_upstream:
        return "no upstream configured"
    ok, out = run_git(repo_path, ["rev-list", "--left-right", "--count", "@{u}...HEAD"])
    parts = out.split() if ok else []
    if len(parts) != 2:
        return "unavailable"
    behind, ahead = parts
    return f"{ahead} ahead, {behind} behind"


def find_instruction_files(repo_path: Path) -> list[str]:
    return [
        name
        for name in INSTRUCTION_FILENAMES + STATE_FILE_DISCOVERY_ORDER
        if (repo_path / name).is_file()
    ]


def parse_markdown_sections(text: str) -> dict[str, str]:
    """Split on '## ' headings only; content is never displayed raw, only excerpted."""
    sections: dict[str, str] = {}
    current = None
    buffer: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line[3:].strip()
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def read_state_file(repo_path: Path):
    """Return (filename_used_or_None, sections_or_None, problem_or_None).

    Discovery order is fixed: WORKBENCH_STATE.md, then PROJECT_STATE.md. The first
    existing file wins. If it cannot be read or parsed, this never falls back to the
    secondary file — a broken higher-priority file must be surfaced, not concealed.
    """
    for name in STATE_FILE_DISCOVERY_ORDER:
        candidate = repo_path / name
        if candidate.is_file():
            try:
                text = candidate.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                return name, None, f"{name} found but could not be read ({exc})"
            return name, parse_markdown_sections(text), None
    return None, None, None


def first_paragraph_or_item(text: str) -> str:
    """Extract the first complete paragraph (or first list item) beneath a heading.

    Joins Markdown-wrapped physical lines with normalized single spaces. Stops at a
    blank line, or — for a bulleted block — at the start of the next list item, so a
    single wrapped sentence is never cut off merely because the source text wrapped.
    Never reproduces an entire long section.
    """
    lines = text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return ""

    is_bullet = lines[i].lstrip().startswith(("- ", "* "))
    collected = [lines[i]]
    i += 1
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            break  # blank line ends the paragraph
        stripped = line.lstrip()
        if is_bullet and stripped.startswith(("- ", "* ")):
            break  # next list item is a new structural block
        if not is_bullet and stripped.startswith(("- ", "* ", "#")):
            break  # a list or heading starting mid-paragraph is a new structural block
        collected.append(line)
        i += 1

    joined = " ".join(part.strip() for part in collected if part.strip())
    return re.sub(r"^[-*]\s+", "", joined).strip()


def truncate_at_word_boundary(text: str, max_len: int = 200) -> str:
    if len(text) <= max_len:
        return text
    truncated = text[:max_len]
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return truncated.rstrip() + "…"


def declared_field(sections: dict[str, str] | None, key: str) -> str | None:
    if not sections or key not in sections or not sections[key].strip():
        return None
    paragraph = first_paragraph_or_item(sections[key])
    if not paragraph:
        return None
    return truncate_at_word_boundary(paragraph)


def project_phase(sections: dict[str, str] | None) -> str | None:
    """Explicit project-phase field only — never derived from a milestone/version status.

    "In progress" / "complete" are milestone statuses, not project phases; this must not
    read them out of a Current Version heading. Only an explicit "Project Phase" or
    "Current Phase" heading counts.
    """
    if not sections:
        return None
    for key in ("Project Phase", "Current Phase"):
        if key in sections and sections[key].strip():
            return declared_field(sections, key)
    return None


def readme_heading(repo_path: Path) -> str | None:
    readme = repo_path / "README.md"
    if not readme.is_file():
        return None
    try:
        text = readme.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped.lstrip("#").strip()
    return None


def field(name: str, value: str, tag: str) -> str:
    return f"{name}: {value} [{tag}]"


def declared_or_unknown_line(name: str, value: str | None) -> str:
    if value:
        return f"{name}: {value} [Declared]"
    return f"{name}: [Unknown]"


def declared_or_unknown_literal(name: str, value: str | None) -> str:
    """Like declared_or_unknown_line, but shows the literal word 'Unknown' as the value —
    used for fields the console has no basis to leave silently blank about: Project Phase
    and the three external-session fields (assistant, workflow, Profile)."""
    if value:
        return f"{name}: {value} [Declared]"
    return f"{name}: Unknown [Unknown]"


def cmd_status(repo_arg: str) -> int:
    raw_path = Path(repo_arg)

    if not raw_path.exists():
        print(f"Path does not exist: {repo_arg}", file=sys.stderr)
        return 1

    if not raw_path.is_dir():
        print(f"Path is not a directory: {repo_arg}", file=sys.stderr)
        return 1

    resolved = raw_path.resolve()
    lines: list[str] = ["Workbench Console — Status Report", ""]

    lines.append(field("Repository Identity", resolved.name, "Verified"))
    heading = readme_heading(resolved)
    if heading:
        lines.append(
            f'  README heading (source excerpt): "{heading}" [Verified] '
            "— not a verified or inferred purpose"
        )
    lines.append(field("Resolved Repository Path", str(resolved), "Verified"))
    lines.append("")

    if not git_is_repository(resolved):
        lines.append("Not a Git repository — Git fields unavailable")
        print("\n".join(lines))
        return 1

    lines.append(field("Git Branch", git_branch(resolved), "Verified"))
    lines.append(field("HEAD Commit", git_head_commit(resolved), "Verified"))
    lines.append(field("Working-Tree Condition", git_working_tree(resolved), "Verified"))
    lines.append(field("Ahead/Behind Upstream", git_ahead_behind(resolved), "Stale Possible"))
    lines.append(
        "Remote Freshness: No fetch was performed. Ahead/behind reflects local "
        "remote-tracking refs only."
    )
    lines.append("")

    state_file, sections, problem = read_state_file(resolved)

    lines.append(declared_or_unknown_literal("Project Phase", project_phase(sections)))
    if problem:
        lines.append(f"State Source Problem: {problem}")
        for name in [
            "Current Milestone/Version",
            "Current Objective",
            "Completed Work (excerpt)",
            "Next Objective",
            "Known Blockers/Unresolved Questions",
        ]:
            lines.append(f"{name}: [Unknown]")
    else:
        lines.append(
            declared_or_unknown_line(
                "Current Milestone/Version", declared_field(sections, "Current Version")
            )
        )
        lines.append(
            declared_or_unknown_line(
                "Current Objective", declared_field(sections, "Current Status")
            )
        )
        lines.append(
            declared_or_unknown_line(
                "Completed Work (excerpt)", declared_field(sections, "Completed")
            )
        )
        lines.append(
            declared_or_unknown_line(
                "Next Objective", declared_field(sections, "Next Objective")
            )
        )
        lines.append(
            declared_or_unknown_line(
                "Known Blockers/Unresolved Questions",
                declared_field(sections, "Open Questions"),
            )
        )
    lines.append("")

    found = find_instruction_files(resolved)
    lines.append(
        field(
            "Repository-Local Instruction Files Found",
            ", ".join(found) if found else "none",
            "Verified",
        )
    )
    if state_file:
        lines.append(field("Project-State File Used", state_file, "Verified"))
    else:
        lines.append('Project-State File Used: "None found" [Unknown]')
    lines.append("")

    # A stateless, independent invocation cannot know whether an assistant, workflow, or
    # Profile is active in the surrounding session — it can only report what a recognized
    # state file explicitly declares, never infer or assume "none" from silence.
    assistant_value = declared_field(sections, "Active Assistant") if not problem else None
    workflow_value = declared_field(sections, "Active Workflow") if not problem else None
    profile_value = declared_field(sections, "Active Profile") if not problem else None
    lines.append(declared_or_unknown_literal("Active Assistant", assistant_value))
    lines.append(declared_or_unknown_literal("Active Workflow", workflow_value))
    lines.append(declared_or_unknown_literal("Active Profile", profile_value))
    lines.append("")

    lines.append(
        "Authorization State: Report-only console operation; this command did not modify "
        "files, launch an assistant, select a workflow, or activate a Profile. [Verified]"
    )
    lines.append(
        "Stop Condition: Command complete; no process remains running. [Verified]"
    )

    print("\n".join(lines))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 1:
        print(usage(), file=sys.stderr)
        return 2

    command = argv[0]
    if command != "status":
        print(f"Unknown command: {command}", file=sys.stderr)
        print(usage(), file=sys.stderr)
        return 2

    if len(argv) < 2:
        print(usage(), file=sys.stderr)
        return 2

    if len(argv) > 2:
        print(f"Unexpected extra arguments: {' '.join(argv[2:])}", file=sys.stderr)
        print(usage(), file=sys.stderr)
        return 2

    return cmd_status(argv[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
