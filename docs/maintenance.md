# Maintenance Checklist

Run through this list before merging changes or tagging a release. It mirrors
Section 3.5 of the documentation and adds a few shell-friendly reminders.

## 1. Clean Builds

```sh
cd projects/textbook/src
latexmk -C      # optional: clear previous artefacts
latexmk -xelatex -interaction=nonstopmode -outdir=../output main.tex
```

Recompile every homework set touched by the change:

```sh
for file in projects/homework/*.tex; do
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error "$file"
done
```

## 2. Audit Logs

- Scan the latest `.log` files inside every per-file output directory (and
  `../output` if you direct the textbook there).
- Resolve overfull/underfull boxes, missing references, and font warnings.

## 3. Sync Documentation

- Update `projects/textbook/src/chapters/table-of-contents.tex` if you added a
  new chapter or section.
- Reflect the changes in `docs/architecture.md` or `docs/quickstart.md` when
  applicable.

## 4. Clear Stray Artefacts

Remove the subfolders latexmk generated next to each source (e.g.,
`rm -rf projects/homework/homework_template projects/discussion/discussion-example`)
and clear `projects/textbook/output/` if you ran the textbook build with
`-outdir=../output`. Ensure the root remains free of build debris so reviewers
only see source changes in a diff.

## 5. Cross-Project Parity

Any edit to the shared library (`tex/core/*`, `tex/styles/*`, `tex/modules/*`)
should be verified in both the documentation book and at least one standalone
homework. Feature parity is a design requirement—divergent layouts or colours
signal a regression.

## 6. Git Hygiene

- Review the staged diff to confirm only intentional files changed.
- Keep commit messages descriptive; mention the sections or modules you touched.

Staying disciplined with this checklist preserves the self-documenting promise
of the project and keeps onboarding friction low for new contributors.
