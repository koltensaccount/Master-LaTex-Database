# Quick Start

This document mirrors Chapter 3 of the typeset guide but in plain text so you can
skim the workflow while working in a terminal.

## Prerequisites

- XeLaTeX (TeX Live 2022+ or MikTeX with XeLaTeX enabled)
- Optional: `latexmk` for incremental builds

## Build the Documentation Book

```sh
cd projects/textbook/src
latexmk -xelatex -interaction=nonstopmode -outdir=../output main.tex
```

Why these flags:

- `-xelatex` selects XeLaTeX so the custom fonts and Unicode characters render
  consistently.
- `-outdir=../output` mirrors the repository layout—artefacts stay out of the
  source directory, and `.gitignore` already blankets the `output/` folder.
- `-interaction=nonstopmode` prevents LaTeX from stalling on warnings during
  automated builds.

Avoid the `-pdf` flag; it switches latexmk back to pdfLaTeX, which cannot load
`fontspec`.

## Build a Standalone Homework Packet

```sh
cd projects/homework
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error homework_template.tex
```

Each homework/discussion/lecture/report file starts by `\input`ing one of the
wrappers in `tex/system/`. When latexmk runs from a project directory, it
creates a sibling folder named after the `.tex` file and stores the PDF plus all
intermediates there—e.g., `projects/homework/homework_template/`. Run latexmk
(or XeLaTeX twice) any time you edit headers, counters, or cross-references.

The discussion, lecture, and lab-report examples follow the same pattern via
`\input{../../tex/system/document-notes.tex}` and
`\input{../../tex/system/document-report.tex}` respectively.

## Clean Up

To clean up, delete the per-file output directory (for example,
`rm -rf projects/homework/homework_template`). If you used
`-outdir=../output` for the textbook build, clear `projects/textbook/output/`
as well.
