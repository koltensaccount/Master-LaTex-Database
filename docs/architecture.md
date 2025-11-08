# Architecture Notes

The LaTeX projects in this repository are intentionally modular. This note
summarises the rationale behind each directory so contributors can map code to
behaviour without compiling the full documentation book.

## Directory Map

```
tex/
  core/       # Shared packages, macros, and colour palette
  styles/     # Visual identity (textbook, homework, lab reports)
  modules/    # Optional shims, e.g. homework embedding
  system/     # Standalone wrappers (document-*.tex) + bootstrap helpers
projects/
  textbook/
    src/      # Documentation sources (chapters, figures, main.tex)
  homework/
    homeworkXX.tex  # Dual-use sources (include tex/system/document-homework.tex)
  discussion/
    discussion-example.tex  # Intake demo (document-notes wrapper)
  lecture/
    lecture-example.tex     # Intake demo (document-notes wrapper)
  reports/
    Master_Lab_Report_Template.tex  # Uses tex/system/document-report.tex
docs/        # Markdown mirrors of the typeset documentation
```

## tex/core

- `colors.tex`: Defines semantic palette names (`Primary`, `Accent`, `Highlight`,
  etc.) with override-friendly storage. Downstream documents can redefine a
  colour before loading the file to experiment locally.
- `base.tex`: Loads AMS packages, graphics tooling (`tikz`, `pgfplots`), and
  helper macros (`\vect`, `\solutionbox`, `\textbookproblem`, and custom theorem
  environments). Any new macro intended for both the textbook and homework PDFs
  should live here, alongside an inline comment describing its purpose.

## tex/styles

- `notes.tex`: Configures the textbook layout—wide left margin, custom chapter
  headings, font selection, and fancy headers. The `\ChapterHeading` and
  `\SectionBar` macros encapsulate all TikZ drawing logic so chapter sources stay
  readable.
- `homework.tex`: Tailors the article class for assignments. Highlights include
  the metadata banner (`\HomeworkSetup` + `\HomeworkHeader`), solution boxes, an
  optional print layout toggle, and an embedding-aware `\HomeworkIncludeInNotes`
  helper that restores the colour palette automatically.
- `report/lab-report-template.sty`: Modernises the lab-report look (cover page,
  palette helpers, headers) while staying agnostic to the parent repository.

## tex/system

- `bootstrap.tex`: Path helpers used by `projects/textbook/src/main.tex` to
  locate the shared library and project roots.
- `document-homework.tex`: Standalone wrapper for assignments. It defines
  `\HomeworkDocumentBegin` / `\HomeworkDocumentEnd`, loads the homework style in
  standalone mode, and becomes a no-op when the same source is embedded in the
  book.
- `document-notes.tex`: Similar wrapper for lecture/discussion capture. It
  handles the article class, typography, and header defaults so intake files
  focus solely on content.
- `document-report.tex`: Shared entry point for lab reports. Standalone builds
  load the lab-report style from `tex/styles/report/`; embedded builds let the
  appendix module supply those resources.

## tex/modules

- `homework-embed.tex`: Sets `\ifMathHomeworkEmbedded` to `true` and loads the
  homework style without its standalone geometry. The module expects a macro
  named `\TexInput`; when the textbook imports it, that macro resolves paths
  relative to the repository root (see `projects/textbook/src/main.tex`).

## projects/textbook

- `src/main.tex`: Entry point for the documentation. It detects the repository
  layout, defines `\TexInput`, loads the shared library, and imports the chapter
  files. The appendix block switches temporarily to the homework geometry so
  embedded assignments look identical to their standalone counterparts.
- `src/chapters/*.tex`: Typeset documentation. Chapters 1–3 cover layout,
  library structure, and daily workflows. Update these files whenever the code
  changes; the project aims to be fully self-documenting.

## projects/homework

- `homeworkXX.tex`: Dual-use sources that simply set metadata, input
  `tex/system/document-homework.tex`, and then call
  `\HomeworkDocumentBegin` / `\HomeworkDocumentEnd`. The wrapper detects whether
  the file is embedded in the textbook and loads the homework style only when
  necessary.

## docs/

- `quickstart.md`: Command-centric build instructions (mirrors Chapter 3).
- `architecture.md`: This file—structural overview.
- `maintenance.md`: Release checklist and hygiene reminders.

Keep these Markdown summaries in sync with the typeset guide so contributors have
both a terminal-friendly reference and a polished PDF to share with new authors.
