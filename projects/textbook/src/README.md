# Textbook Source Quick Start

This folder contains the sources for the textbook-style notes. You rarely need
to touch anything outside it when writing new content. The two most common
tasks—creating a chapter and adding an appendix—now have helper scripts so you
never wonder which files to edit.

## Directory Map

```
chapters/      # One file per chapter + table-of-contents helper
appendices/    # Appendix files (homework, discussion, lecture, …)
figures/       # Shared artwork
tools/         # Helper scripts for new content
main.tex       # Driver that stitches everything together
```

## Creating a Chapter

Use the helper to scaffold a chapter file, register it with `main.tex`, and add
an entry to the table of contents in one go:

```sh
cd projects/textbook/src
python tools/new_chapter.py "Linear Algebra Refresher"
```

What you get:

- `chapters/chapter_4.tex` (number auto-increments) with a labelled
  `\ChapterHeading` and starter `\SectionBar`.
- `main.tex` updated with `\input{chapters/chapter_4}` in reading order.
- `chapters/table-of-contents.tex` extended with a placeholder block for the
  new chapter; replace the comment with real bullet items when you outline it.

Need a specific number or slug? Supply `--number` and `--slug`:

```sh
python tools/new_chapter.py "Applications" --number 7 --slug applications
```

## Creating an Appendix

Appendices (Homework, Discussion, Lecture, …) live under `appendices/`. The
helper script creates a new file, wires it into `main.tex`, and appends a table
of contents entry:

```sh
cd projects/textbook/src
python tools/new_appendix.py "Reference Tables"
```

The script chooses the next unused appendix letter (D if A–C exist) and creates
`appendices/appD-reference-tables.tex`. To force a letter, pass `--letter B`.

## Editing the Table of Contents

`chapters/table-of-contents.tex` mirrors the on-page summary. After running one
of the helpers, fill in the `%` placeholders with real `\hyperref` items so the
PDF remains navigable.

## Intake Macros at a Glance

- `\newlecture{Title}{YYYY-MM-DD}` → Appendix lecture entry
- `\newdiscussion{Week}{Sheet}{YYYY-MM-DD}` → Discussion intake
- `\newhwprob{Section}{Number}[Title]` → Homework problem stub
- `\newdiscprob{Pack}{Id}[Topic]` → Discussion problem stub
- `\probref{prob:hw-…}` / `\Probref{…}` → Cross-reference helper

These macros are only available inside the appendices so chapters stay curated.
Capture class notes in the appendices first, then cite them from polished
chapters with `\probref`/`\Probref`.

## Building

```sh
latexmk -xelatex -interaction=nonstopmode -outdir=../output main.tex
```

This keeps the main book’s artefacts in `../output/` (relative to `src/`). Every
standalone project that uses latexmk creates a sibling directory named after the
`.tex` file (for example, `projects/homework/homework_template/`). Clean with
`latexmk -CA` when you need a fresh build, then remove the per-file folders if
you want to clear standalone caches as well.
