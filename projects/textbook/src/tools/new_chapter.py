#!/usr/bin/env python3
"""
Utility script to scaffold a new chapter file and update the LaTeX driver.

Usage:
  python tools/new_chapter.py "Chapter Title"

Optional flags:
  --number  Explicit chapter number to use (otherwise auto-increments)
  --slug    Override the slug used in labels (defaults to a cleaned title)
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

RE_CHAPTER_FILE = re.compile(r"chapter_(\d+)\.tex$")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "chapter"


def find_next_chapter_number(chapter_dir: Path) -> int:
    numbers = []
    for path in chapter_dir.glob("chapter_*.tex"):
        match = RE_CHAPTER_FILE.match(path.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers) + 1 if numbers else 1


def create_chapter_file(path: Path, number: int, title: str, slug: str) -> None:
    content = f"""\\ChapterHeading{{{number}}}{{{title}}}
\\label{{ch:{slug}}}

\\SectionBar{{{number}.1}}{{Overview}}
\\label{{sec:{slug}-overview}}

% Add your content here. Use additional \\SectionBar commands as needed.
"""
    path.write_text(content, encoding="utf8")


def update_main_tex(main_path: Path, chapter_filename: str) -> None:
    lines = main_path.read_text(encoding="utf8").splitlines()
    insertion_index = None
    for idx, line in enumerate(lines):
        if line.strip().startswith(r"\input{appendices/"):
            insertion_index = idx
            break
        if line.strip().startswith(r"\backmatter"):
            insertion_index = idx
            break
    if insertion_index is None:
        raise RuntimeError("Could not find insertion point for new chapter in main.tex")
    new_line = f"\\input{{chapters/{chapter_filename}}}"
    if new_line not in lines:
        lines.insert(insertion_index, new_line)
        main_path.write_text("\n".join(lines) + "\n", encoding="utf8")


def update_table_of_contents(toc_path: Path, number: int, title: str, slug: str) -> None:
    block = [
        "",
        f"\\SectionBar{{{number}}}{{\\hyperref[ch:{slug}]{{{title}}}}}",
        "\\begin{itemize}[leftmargin=1.5em,label={},itemsep=0.15em,topsep=0.3em]",
        "  % Add \\hyperref items for sections inside this chapter.",
        "\\end{itemize}",
    ]

    lines = toc_path.read_text(encoding="utf8").splitlines()
    for existing in lines:
        if f"\\hyperref[ch:{slug}]" in existing:
            return  # Already present
    insert_at = None
    for idx, line in enumerate(lines):
        if line.startswith(r"\SectionBar{A}"):
            insert_at = idx
            break
    if insert_at is None:
        insert_at = len(lines)
    lines[insert_at:insert_at] = block
    toc_path.write_text("\n".join(lines) + "\n", encoding="utf8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    chapters_dir = root / "chapters"
    main_tex = root / "main.tex"
    toc_tex = chapters_dir / "table-of-contents.tex"

    parser = argparse.ArgumentParser(description="Create a new chapter skeleton")
    parser.add_argument("title", help="Displayed chapter title")
    parser.add_argument(
        "--number",
        type=int,
        help="Numeric chapter identifier (default: next available)",
    )
    parser.add_argument("--slug", help="Optional slug for labels")
    args = parser.parse_args()

    chapter_number = args.number or find_next_chapter_number(chapters_dir)
    chapter_slug = args.slug or slugify(args.title)
    chapter_filename = f"chapter_{chapter_number}.tex"
    chapter_path = chapters_dir / chapter_filename

    if chapter_path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {chapter_path}")

    create_chapter_file(chapter_path, chapter_number, args.title, chapter_slug)
    update_main_tex(main_tex, chapter_filename.replace(".tex", ""))
    update_table_of_contents(toc_tex, chapter_number, args.title, chapter_slug)
    print(f"Created {chapter_path.relative_to(root)} and updated main.tex / table-of-contents.")


if __name__ == "__main__":
    main()
