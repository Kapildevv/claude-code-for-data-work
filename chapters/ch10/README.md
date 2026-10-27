# Chapter 10

Three hook scripts run beside Claude's tool calls, and a `hooks` block in `.claude/settings.json` registers them:

- `.claude/hooks/protect_raw.py` is a `PreToolUse` guard on `Write|Edit|Bash|PowerShell`. It reads the pending
  call as JSON on stdin and exits 2 with a message when a file write targets `data/raw/` or a shell command
  names `data/raw/` together with a write verb (`cp`, `mv`, `rm`, `tee`, `Out-File`, `Set-Content`...) or a
  redirection into it. Reads pass. It is a best-effort net: it reads the text of a command, not what the command
  will do.
- `.claude/hooks/lint_sql.py` is a `PostToolUse` hook on `Write|Edit`. It lints a `.sql` file with sqlfluff and
  exits 2 with the findings, which go to Claude.
- `.claude/hooks/log_tools.py` is a `PostToolUse` hook on every tool. It appends one JSON line per finished call
  to `.claude/logs/tools.jsonl`.
- `.claude/settings.json` is chapter 8's file plus the `hooks` block and nothing else. Every command is
  `uv run python "${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>"`: `uv run` so the hook uses the project's
  interpreter, and the braced variable so the line means the same under Git Bash and under PowerShell.
- `.sqlfluff` holds the project's SQL rules from `.claude/rules/sql.md` in the form sqlfluff reads: the `duckdb`
  dialect and the rules `CP01`, `CP03`, `LT02`, `LT09` and `LT14`.
- `pyproject.toml` and `uv.lock` gain `sqlfluff==4.4.0` in the `dev` dependency group (`uv add --dev sqlfluff==4.4.0`).

Add `.claude/logs/` to your project's `.gitignore` (the chapter does this with `Add-Content`). The log is created by
the first logged call and can hold whatever is typed into a command, so it stays out of git.

Test a guard by making it block: pipe a sample call into it and read the exit code.

```text
'{"tool_name": "Bash", "tool_input": {"command": "cp x.csv data/raw/"}}' | uv run python .claude/hooks/protect_raw.py
$LASTEXITCODE
```

The first line of output is the block message and the second is `2`. On macOS and Linux:
`echo '{...}' | uv run python .claude/hooks/protect_raw.py; echo $?`.

The hooks need the project's environment, so run `uv sync` first (it installs sqlfluff from `uv.lock`).
