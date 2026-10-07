# Textbook Source

This folder is the source for the textbook-style example.

```
main.tex      driver file
chapters/     chapter files
appendices/   embedded homework, lecture, discussion, and report examples
bib/          bibliography
figures/      shared figures
tools/        small scaffolding scripts
```

## Build

```sh
latexmk -xelatex -outdir=../output main.tex
```

## Add a chapter

```sh
python tools/new_chapter.py "Linear Algebra Refresher"
```

## Add an appendix

```sh
python tools/new_appendix.py "Reference Tables"
```

After adding content, edit `chapters/table-of-contents.tex` if you want the PDF overview page to mention it.
