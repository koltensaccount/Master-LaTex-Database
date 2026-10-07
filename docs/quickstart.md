# Quick Start

Use XeLaTeX. These templates rely on packages and fonts that are safest with `latexmk -xelatex`.

## Build one template

Run latexmk from the folder that contains the `.tex` file:

```sh
cd projects/homework
latexmk -xelatex homework_template.tex
```

Swap in the file you need:

```sh
cd projects/lecture && latexmk -xelatex lecture-example.tex
cd projects/discussion && latexmk -xelatex discussion-example.tex
cd projects/reports && latexmk -xelatex Master_Lab_Report_Template.tex
```

## Build the textbook example

```sh
cd projects/textbook/src
latexmk -xelatex -outdir=../output main.tex
```

The `-outdir=../output` flag keeps textbook build files out of `src/`.

## Clean generated files

```sh
latexmk -C
```

If a build made a folder named after the source file, delete that folder when you want a fully clean tree. Those folders are ignored by Git.

## Add textbook content

```sh
cd projects/textbook/src
python tools/new_chapter.py "New Topic"
python tools/new_appendix.py "Reference Tables"
```

The scripts create the file and update `main.tex` for you.
