# Chapter 6

`.claude/settings.json` extends chapter 3's file (`plansDirectory`) with `autoMemoryEnabled: false`
and the permission rules: allow for the commands run all day (each in a `Bash(...)` and a
`PowerShell(...)` form), ask before `git push`, and deny for `.env` and everything under
`data/raw/`. The deny rule for writes is written `Edit(...)`, not `Write(...)`: `Edit` rules cover
every tool that changes a file.

`.claude/settings.local.json` is one analyst's personal file. The sample holds the rule that the
"don't ask again" answer of chapter 2 would leave for `uv run python clean_sales.py`. In your own
project it stays out of git: add `.claude/settings.local.json` to `.gitignore` (Claude Code adds it
to your global git excludes only when it creates the file itself). This folder has no `.gitignore`
of its own on purpose, and the companion repository's root `.gitignore` makes an exception for
the chapter samples.

`.claude/rules/sql.md` is a path-scoped rule: its `paths:` frontmatter makes it load only when
Claude reads or edits a file under `models/`. `models/weekly_sales.sql` is the first model; run
against the drop it gives 41404.95 net sales for the week of 2026-09-21, the check value of
chapter 4.

`.env` is not in this folder. Create it yourself (`JUNIPER_DB_PASSWORD=not-a-real-secret` as a
stand-in; Luis supplies the real value) and keep it out of git: the project's `.gitignore`
already lists it. The starter's `.env.example` shows the variable name with no value.
