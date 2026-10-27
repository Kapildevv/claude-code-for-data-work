# Chapter 12

The project becomes a plugin. Lay these files over your project (chapters 2 to 11 in place) and commit them.

- `.claude-plugin/plugin.json` is the plugin manifest. `name` is `juniper-data-kit`, and every path starts `./` and
  stays inside the repository: `skills` is `./.claude/skills/`, `agents` lists `./.claude/agents/dq-reviewer.md`, and
  `hooks` is `./.claude/hooks/hooks.json`. The plugin's root is the repository root, so the manifest points into `.claude/`.
- `.claude-plugin/marketplace.json` is a one-plugin marketplace named `juniper-team`. The plugin's `source` is `./`, the
  folder that holds the marketplace. A teammate installs `juniper-data-kit@juniper-team`.
- `.claude/hooks/hooks.json` is chapter 10's hooks block as a plugin ships it: each command reaches its script through
  `${CLAUDE_PLUGIN_ROOT}` (the folder the plugin is installed in) and runs under `uv run --no-project`, so the hook does not
  depend on, or wait for, the host project's environment. The lint hook adds `--with sqlfluff==4.4.0` because the host
  project may not have sqlfluff. Your own `.claude/settings.json` keeps chapter 10's block, which uses
  `${CLAUDE_PROJECT_DIR}`: the repository that owns the files never needs the plugin.
- `.claude/hooks/log_tools.py` takes the project from `CLAUDE_PROJECT_DIR` (the hook JSON's `cwd` is the fallback), so the
  log lands in `.claude/logs/tools.jsonl` of the project being worked in, not inside the plugin's folder.
- `.claude/hooks/lint_sql.py` uses the project's own `.sqlfluff` when there is one and the kit's (at the plugin root)
  when there is not. `protect_raw.py` is chapter 10's file and does not change: it reads only the JSON on stdin.
- `.claude/skills/<name>/SKILL.md` for `profile-data`, `to-parquet`, `build-marts` and `kpi-report` are chapter 8's files with
  one change: each script is reached through `${CLAUDE_SKILL_DIR}/scripts/...` in the body and in the `Bash(...)` and
  `PowerShell(...)` rules of `allowed-tools`, instead of `.claude/skills/<name>/scripts/...` from the project root.

Check the files with `claude plugin validate .` (it reads structure only: it never reads a hook's command or a skill's body).

Do not register the marketplace from your working folder. Installing from a local folder copies everything in it into the
Claude Code configuration folder, `.env` and every gitignored file included. Make a clean clone and use that:

```text
git clone . ..\juniper-kit
cd ..\juniper-lane-imani
claude plugin install juniper-data-kit --marketplace ..\juniper-kit --scope project
```

That is the one-command install into a second repository (here named `juniper-lane-imani`, a copy of the starter with no
`.claude/` of its own). It declares the marketplace in your user settings and writes `enabledPlugins` to the second
repository's `.claude/settings.json`. In your own repository, where the same skills and hooks already load from `.claude/`,
leave the plugin off (or set `"enabledPlugins": {"juniper-data-kit@juniper-team": false}` in its project settings): enabled
there too, every skill, agent and hook registers twice and each tool call is logged twice.

Chapter 11's `.mcp.json` sits at the plugin root, a default MCP location, so its two servers travel with the plugin as
`plugin:juniper-data-kit:warehouse` and `plugin:juniper-data-kit:context7`. The plugin does not carry `CLAUDE.md`, `rules/`,
`settings.json` permissions, the `weekly-report` command, the agent's memory notes, the SQL in `models/` or the packages a
script imports: those belong to the project that uses the kit.
