# Chapter 13

Three files and one ignore rule take the project off your keyboard. Lay the files over your project (chapters 2 to 12 in
place) and commit them.

- `scripts/weekly_report.ps1` runs Dana's weekly report with nobody at the keyboard. It moves to the project root, calls
  `claude -p "/weekly-report"` with `--permission-mode dontAsk`, `--allowedTools "Skill"` (the one tool the three skills
  need, because each skill's `allowed-tools` covers its own script), `--output-format json`, `--max-turns 15` and
  `--strict-mcp-config`, saves the JSON to `out/weekly_report.json`, and exits 0 only when the call exited 0, `is_error` is
  false, `permission_denials` is empty and a `reports/kpi-*.md` file newer than the start holds a `Net sales` row. The net
  sales figure for the week of 2026-09-21 is $41,404.95 and comes from the report file that `kpi_report.py` wrote.
- `scripts/weekly_report.sh` is the same script for macOS, Linux and Git Bash. It exports `MSYS_NO_PATHCONV=1` so Git Bash
  does not rewrite the `/weekly-report` argument into a Windows path, and its three `grep` and `-nt` checks mirror the
  PowerShell ones. It was not run for the book (`bash -n` accepts it).
- `.claude/workflows/weekly-run.js` is a saved workflow (`export const meta` first, then `agent()` and `phase()` calls). It
  runs as `/weekly-run`: it profiles the drop, asks `dq-reviewer` to review it, then runs `to-parquet`, `build-marts` and
  `kpi-report` one after the other and stops at the first failure. It starts five sub-agents, which spend usage, so the
  book shows the file and checks that Claude Code lists it, and does not run it.
- `.gitignore` gets one line, `.claude/worktrees/`, where `claude --worktree <name>` keeps its folders. Without it,
  `git add .` stages a worktree as an embedded repository:

  ```powershell
  Add-Content .gitignore ".claude/worktrees/"
  ```

Register the script with the operating system's scheduler. On Windows:

```powershell
$action   = New-ScheduledTaskAction -Execute "powershell.exe" -Argument '-NoProfile -ExecutionPolicy Bypass -File "C:\work\juniper-lane\scripts\weekly_report.ps1"'
$trigger  = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 6:30am
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun
Register-ScheduledTask -TaskName "Juniper weekly report" -Action $action -Trigger $trigger -Settings $settings
```

The chapter's own run added `-Disable` to the settings so that nothing could start `claude` by itself, read the task back,
and unregistered it. On macOS and Linux the cron line `30 6 * * 1 /home/you/work/juniper-lane/scripts/weekly_report.sh`
does the same job (not run), with full paths to `claude` and `uv` because cron starts with a minimal `PATH`.

Worktrees need no file: `claude --worktree a` and `claude --worktree b` make two folders under `.claude/worktrees/`. Take
one down with `git worktree unlock`, `git worktree remove` (add `--force` if it holds untracked files) and `git branch -d`.
