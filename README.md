# MATH 2243 Combined Notes and Homework

This repository is a LaTeX toolkit for producing a textbook-style set of notes
and matching homework assignments. Both deliverables share the same colour
palette, typography, and header layout, and every file is documented inside the
companion guide so contributors understand the rationale behind each line.

The documentation lives in `projects/textbook/src/`. Compile it to read a
typeset walkthrough, or open the Markdown summaries under `docs/` for a quick
reference.

## Repository Layout

```
.
├── README.md                  # High-level overview (this file)
├── .gitignore                 # LaTeX artefact hygiene rules
├── docs/                      # Plain-text quick start + architecture notes
├── tex/                       # Shared TeX library used by every project
│   ├── core/                  # Packages, macros, and colour palette
│   ├── styles/                # Layout implementations (notes, homework, reports)
│   ├── modules/               # Small shims, e.g. homework embedding
│   └── system/                # Standalone wrappers (document-*.tex, bootstrap)
└── projects/
    ├── textbook/              # Documentation-as-book project
    │   └── src/               # LaTeX sources (chapters, main.tex, figures)
    ├── homework/              # Single-source homework files (input tex/system/document-homework.tex)
    ├── discussion/            # Discussion intake examples (document-notes wrapper)
    ├── lecture/               # Lecture intake examples (document-notes wrapper)
    └── reports/               # Lab report template using document-report.tex
```

## Quick Start

Documentation build (from the repository root):

```sh
cd projects/textbook/src
latexmk -xelatex -interaction=nonstopmode -outdir=../output main.tex
```

Standalone homework build (swap the filename as needed):

```sh
cd projects/homework
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error homework_template.tex
```

latexmk creates an output folder named after the `.tex` file inside the same
directory (for example, compiling `projects/homework/homework_template.tex`
produces `projects/homework/homework_template/homework_template.pdf`). The root
`.gitignore` already blankets those per-file directories, plus the usual `.log`,
`.aux`, `.pdf`, and `.synctex.gz` artefacts, so repository history stays focused
on source changes. Running bare `xelatex` is still possible, but the artefacts
will accumulate next to the `.tex` file unless you clean them up manually.

### Day-to-day authoring

For step-by-step guidance on creating chapters, appendices, and using the intake
macros, see `projects/textbook/src/README.md`. Helper scripts in
`projects/textbook/src/tools/` scaffold new files and update the driver for you:

```sh
python tools/new_chapter.py "New Topic"
python tools/new_appendix.py "Extra Reference"
```

Discussion, lecture, and lab report capture follow the same pattern as homework:
each standalone file defines a few metadata macros (title, date, etc.) and then
`\input`s the matching wrapper from `tex/system/document-*.tex`. Compile them
directly or let the textbook appendices `\input` the exact same sources.

## Customising the System

1. Update the global palette in `tex/core/colors.tex`. The semantic colour names
   (`Primary`, `Accent`, `Highlight`, etc.) propagate automatically to the book,
   appendix, and homework PDFs.
2. Adjust typography and geometry in `tex/styles/notes.tex` (textbook) or
   `tex/styles/homework.tex` (assignments). Each block carries inline comments
   describing the effect of the parameters.
3. For document-specific tweaks, redefine colours or wrap layout changes in
   `\newgeometry ... \restoregeometry` blocks, mirroring the appendix pattern in
   `projects/textbook/src/main.tex`.

## Working With Homework Content

- Author problems under `projects/homework/`. These files contain only
  content—no packages or document classes.
- To embed an assignment in the book, append a line like
  `\HomeworkIncludeInNotes{Homework 9}{\HomeworkPath{homework09.tex}}`
  inside `projects/textbook/src/main.tex`.
- To keep a printable version, point the standalone wrapper at the same source
  (e.g., `latexmk -xelatex projects/homework/homework09.tex`). The command drops
  all artefacts inside `projects/homework/homework09/homework09.*`, matching the
  textbook appendix output.

## Further Reading

- Build and directory rationale: Chapter 1 of the documentation (`main.tex`).
- TeX library deep dive: Chapter 2, plus inline comments throughout `tex/`.
- Authoring workflow checklist: Chapter 3 and `docs/maintenance.md`.

Compile `projects/textbook/src/main.tex`, or open the Markdown in `docs/`, for a
complete explanation of every macro, folder, and build step.
