# Chapter 5

`.claude/CLAUDE.md` is the team's file: the three conventions (snake_case, DuckDB, nothing
written to `data/raw/`), the commands, the money and week rules, and an import of
`../DATASET.md`. The import path starts with `../` because it is read from the folder that holds
the file, not from the project root. `CLAUDE.local.md` is one analyst's personal notes.

In your own project, `CLAUDE.local.md` stays out of git with one line added to the project's
`.gitignore`:

    CLAUDE.local.md

This folder has no `.gitignore` of its own on purpose: that line would hide the sample
`CLAUDE.local.md` here. Compare your copy of `.claude/CLAUDE.md` and `CLAUDE.local.md` with these two files
when your session does not seem to know the team's rules, and run `/context` to see which
files loaded.
