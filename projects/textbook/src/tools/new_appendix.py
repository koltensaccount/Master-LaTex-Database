#!/usr/bin/env python3
"""
Utility script to scaffold a new appendix file and update the LaTeX driver.

Usage:
  python tools/new_appendix.py "Appendix Title"

Optional flags:
  --letter  Override the appendix letter (A, B, C, ...)
  --slug    Override the slug used in labels (defaults to a cleaned title)
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

RE_APPENDIX_FILE = re.compile(r"app([A-Z])[-_]?.*\.tex$")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "appendix"


def next_letter(existing_letters: list[str]) -> str:
    if not existing_letters:
        return "A"
    highest = max(existing_letters)
    return chr(ord(highest) + 1)


def discover_letters(appendix_dir: Path) -> list[str]:
    letters = []
    for path in appendix_dir.glob("app*.tex"):
        match = RE_APPENDIX_FILE.match(path.name)
        if match:
            letters.append(match.group(1))
    return letters


def create_appendix_file(path: Path, title: str, slug: str) -> None:
    content = f"""\\clearpage
\\chapter{{{title}}}
\\label{{app:{slug}}}
\\addcontentsline{{toc}}{{chapter}}{{{title}}}

% Capture incoming notes here. Use \\newlecture, \\newdiscussion, or custom sections as needed.
"""
    path.write_text(content, encoding="utf8")


def update_main_tex(main_path: Path, filename: str) -> None:
    lines = main_path.read_text(encoding="utf8").splitlines()
    insert_before = None
    for idx, line in enumerate(lines):
        if line.strip().startswith(r"\backmatter"):
            insert_before = idx
            break
    if insert_before is None:
        raise RuntimeError("Could not find \\backmatter in main.tex")
    new_line = f"\\input{{appendices/{filename}}}"
    if new_line not in lines:
        lines.insert(insert_before, new_line)
        main_path.write_text("\n".join(lines) + "\n", encoding="utf8")


def update_table_of_contents(toc_path: Path, letter: str, title: str, slug: str) -> None:
    block = [
        "",
        f"\\SectionBar{{{letter}}}{{\\hyperref[app:{slug}]{{{title}}}}}",
        "\\begin{itemize}[leftmargin=1.5em,label={},itemsep=0.15em,topsep=0.3em]",
        "  % Add \\hyperref items for sections inside this appendix.",
        "\\end{itemize}",
    ]
    lines = toc_path.read_text(encoding="utf8").splitlines()
    for existing in lines:
        if f"\\hyperref[app:{slug}]" in existing:
            return
    lines.extend(block)
    toc_path.write_text("\n".join(lines) + "\n", encoding="utf8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    appendix_dir = root / "appendices"
    main_tex = root / "main.tex"
    toc_tex = root / "chapters" / "table-of-contents.tex"

    parser = argparse.ArgumentParser(description="Create a new appendix skeleton")
    parser.add_argument("title", help="Displayed appendix title")
    parser.add_argument("--letter", help="Appendix letter (default: next available)")
    parser.add_argument("--slug", help="Optional slug for labels")
    args = parser.parse_args()

    existing_letters = discover_letters(appendix_dir)
    letter = args.letter.upper() if args.letter else next_letter(existing_letters)
    if letter in existing_letters and not args.letter:
        raise SystemExit(f"Appendix letter {letter} already exists. Use --letter to override.")

    filename = f"app{letter}-{slugify(args.title)}.tex"
    appendix_path = appendix_dir / filename
    if appendix_path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {appendix_path}")

    slug = args.slug or slugify(args.title)
    create_appendix_file(appendix_path, args.title, slug)
    update_main_tex(main_tex, filename.replace(".tex", ""))
    update_table_of_contents(toc_tex, letter, args.title, slug)
    print(f"Created {appendix_path.relative_to(root)} and updated main.tex / table-of-contents.")


if __name__ == "__main__":
    main()
