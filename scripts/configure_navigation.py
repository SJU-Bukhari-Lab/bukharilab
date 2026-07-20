#!/usr/bin/env python3
"""Configure the public navigation while preserving hidden archive pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def split_front_matter(text: str) -> tuple[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, flags=re.DOTALL)
    if not match:
        raise ValueError("Missing YAML front matter")
    return match.group(1), text[match.end():]


def remove_key_block(front: str, key: str) -> str:
    lines = front.splitlines()
    result: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if re.match(rf"^{re.escape(key)}\s*:", line):
            index += 1
            while index < len(lines) and (lines[index].startswith(" ") or not lines[index].strip()):
                index += 1
            continue
        result.append(line)
        index += 1
    return "\n".join(result).strip()


def set_scalar(front: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}\s*:.*$", flags=re.MULTILINE)
    replacement = f"{key}: {value}"
    if pattern.search(front):
        return pattern.sub(replacement, front, count=1)
    return f"{replacement}\n{front}".strip()


def update_page(path: Path, *, title: str | None, nav_order: int | None, tooltip: str | None) -> None:
    if not path.exists():
        print(f"Skipping missing page: {path}")
        return

    text = path.read_text(encoding="utf-8")
    front, body = split_front_matter(text)
    front = remove_key_block(front, "nav")

    if title is not None:
        front = set_scalar(front, "title", title)

    if nav_order is not None:
        nav = f"nav:\n  order: {nav_order}\n  tooltip: {tooltip or title or 'Page'}"
        front = f"{front.rstrip()}\n{nav}".strip()

    path.write_text(f"---\n{front}\n---\n\n{body.lstrip()}", encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: configure_navigation.py /path/to/site", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    updates = [
        ("index.md", "Home", 0, "Home"),
        ("research/index.md", "Research", 1, "Research areas and initiatives"),
        ("papers/index.md", "Papers", 2, "Publications and benchmarking research"),
        ("software/index.md", "Software", 3, "Research software, standards, and tools"),
        ("team/index.md", "Team", 4, "Meet our team"),
        ("blog/index.md", "News", 5, "Lab news"),
        ("contact/index.md", "Join Us", 6, "Join or contact the lab"),
        # Keep these routes available without placing them in the main navigation.
        ("projects/index.md", "Projects", None, None),
        ("about/index.md", None, None, None),
    ]

    for relative, title, order, tooltip in updates:
        update_page(root / relative, title=title, nav_order=order, tooltip=tooltip)

    print("Navigation updated: Home, Research, Papers, Software, Team, News, Join Us")
    print("Projects and About remain accessible but are not displayed in the main navigation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
