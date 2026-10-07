# Master LaTeX Database

A small LaTeX starter kit for notes, homework, lecture/discussion handouts, and lab reports.

The repo is meant to hold source files only. PDFs, logs, aux files, and latexmk output folders are ignored so Git stays readable.

## What is inside

```
tex/
  core/       shared packages, colors, macros, and TikZ helpers
  styles/     document styles for notes, homework, and reports
  system/     wrappers that make project files compile on their own
  modules/    adapters for embedding project files in the textbook

projects/
  homework/     homework template
  lecture/      lecture notes example
  discussion/   discussion notes example
  reports/      lab report template
  textbook/src/ longer notes/textbook example
```

## Build

Install a TeX distribution with XeLaTeX and latexmk. Then compile the file you are working on.

```sh
cd projects/homework
latexmk -xelatex homework_template.tex
```

```sh
cd projects/lecture
latexmk -xelatex lecture-example.tex
```

```sh
cd projects/discussion
latexmk -xelatex discussion-example.tex
```

```sh
cd projects/reports
latexmk -xelatex Master_Lab_Report_Template.tex
```

Textbook build:

```sh
cd projects/textbook/src
latexmk -xelatex -outdir=../output main.tex
```

## Clean

Most generated files are ignored by `.gitignore`. To clean a working directory:

```sh
latexmk -C
```

If latexmk created a per-file output folder, remove that folder too. Example:

```sh
rm -rf projects/homework/homework_template
```

## Editing the shared style

- Colors: `tex/core/colors.tex`
- Shared macros: `tex/core/base.tex`
- Notes/textbook layout: `tex/styles/notes.tex`
- Homework layout: `tex/styles/homework.tex`
- Lab report layout: `tex/styles/report/lab-report-template.sty`

Keep new reusable commands in `tex/core/` or `tex/styles/`. Keep class-specific content in `projects/`.

More build details are in `docs/quickstart.md`.
