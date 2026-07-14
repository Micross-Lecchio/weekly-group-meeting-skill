#!/usr/bin/env python3
"""Safely initialize the current or specified ISO-week workspace.

This script only creates missing directories and files inside the chosen
project root. It never overwrites existing files and never moves user data.
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys


ISO_WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
LABEL_RE = re.compile(r"^\[[^\[\]\r\n]+\]$")
WINDOWS_PATH_FORBIDDEN_RE = re.compile(r'[<>:"/\\|?*\r\n]')


def iso_week_for_date(day: dt.date) -> str:
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


def find_project_root(start: Path) -> Path:
    """Find the nearest ancestor containing AGENTS.md; otherwise use start."""
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file():
            return candidate
    return current


def read_template(skill_dir: Path, name: str) -> str:
    path = skill_dir / "templates" / name
    if not path.is_file():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def relative_posix(path: Path, project_root: Path) -> str:
    return path.relative_to(project_root).as_posix()


def validate_task_identity(label: str, task_name: str) -> None:
    if not LABEL_RE.fullmatch(label):
        raise ValueError("Task label must use square brackets, for example [paper].")
    if not task_name.strip():
        raise ValueError("Task name must not be empty.")
    if WINDOWS_PATH_FORBIDDEN_RE.search(task_name):
        raise ValueError("Task name contains characters that are unsafe in file paths.")


def initialize(project_root: Path, iso_week: str) -> list[str]:
    if not ISO_WEEK_RE.fullmatch(iso_week):
        raise ValueError("ISO week must use YYYY-Www format, for example 2026-W29.")

    skill_dir = project_root / ".agents" / "skills" / "managing-weekly-group-meetings"
    weekly_template = read_template(skill_dir, "weekly-readme.md")
    dashboard_template = read_template(skill_dir, "task-dashboard.md")

    created: list[str] = []

    for directory in [
        project_root / "weekly",
        project_root / "completed-projects",
        project_root / "weekly" / iso_week / "tasks",
        project_root / "weekly" / iso_week / "deliverables",
        project_root / "weekly" / iso_week / "non-task",
    ]:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(relative_posix(directory, project_root))

    readme = project_root / "weekly" / iso_week / "README.md"
    if write_if_missing(readme, weekly_template.replace("{{ISO_WEEK}}", iso_week)):
        created.append(relative_posix(readme, project_root))

    dashboard = project_root / "TASKS.md"
    if write_if_missing(dashboard, dashboard_template):
        created.append(relative_posix(dashboard, project_root))

    return created


def initialize_task_workspace(
    project_root: Path,
    iso_week: str,
    label: str,
    task_name: str,
    *,
    day: dt.date | None = None,
) -> list[str]:
    if not ISO_WEEK_RE.fullmatch(iso_week):
        raise ValueError("ISO week must use YYYY-Www format, for example 2026-W29.")
    validate_task_identity(label, task_name)

    skill_dir = project_root / ".agents" / "skills" / "managing-weekly-group-meetings"
    task_template = read_template(skill_dir, "task-record.md")
    created = initialize(project_root, iso_week)

    task_dir = project_root / "weekly" / iso_week / "tasks" / f"{label}{task_name}"
    for directory in [
        task_dir,
        task_dir / "temporary",
        task_dir / "deliverables",
        task_dir / "working",
    ]:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(relative_posix(directory, project_root))

    record = task_dir / f"{label}任务记录.md"
    record_content = (
        task_template.replace("{{LABEL}}", label)
        .replace("{{TASK_NAME}}", task_name)
        .replace("{{ISO_WEEK}}", iso_week)
        .replace("{{DATE}}", (day or dt.date.today()).isoformat())
        .replace("{{TASK_WORKSPACE}}", relative_posix(task_dir, project_root))
    )
    if write_if_missing(record, record_content):
        created.append(relative_posix(record, project_root))

    return created


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Project root or a path inside it. Defaults to the current directory.",
    )
    parser.add_argument(
        "--week",
        default=iso_week_for_date(dt.date.today()),
        help="ISO week in YYYY-Www format. Defaults to the current ISO week.",
    )
    parser.add_argument(
        "--label",
        help="Optional task label in square brackets, for example [paper].",
    )
    parser.add_argument(
        "--task-name",
        help="Optional task name. Requires --label and creates an isolated task workspace.",
    )
    args = parser.parse_args()

    try:
        root = find_project_root(args.root)
        if bool(args.label) != bool(args.task_name):
            raise ValueError("--label and --task-name must be provided together.")
        if args.label and args.task_name:
            created = initialize_task_workspace(root, args.week, args.label, args.task_name)
        else:
            created = initialize(root, args.week)
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(f"Initialization failed: {exc}", file=sys.stderr)
        return 1

    print(f"Project root: {root}")
    print(f"ISO week: {args.week}")
    if created:
        print("Created:")
        for item in created:
            print(f"  - {item}")
    else:
        print("Nothing created; all required paths already exist.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
