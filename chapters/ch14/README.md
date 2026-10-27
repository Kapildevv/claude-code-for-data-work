# Chapter 14

The capstone. These files are laid over `capstone/juniper-inventory/`, a second repository (dbt on DuckDB) and not the
sales project, so the sales project ends at chapter 13. Copy the supplied repository, lay these files over it at the same
relative paths, and commit.

- `.claude/CLAUDE.md` is the repository's memory: the commands, the dbt pin, the rule that `seeds/` is never edited
  (`make_seeds.py` included), the two warnings that are expected, and which MCP server to ask. The README is pointed at, not
  imported, because its "Known issues" section goes stale once the fix lands.
- `.claude/settings.json` allows the dbt commands (both shells), denies `Edit(./seeds/**)`, keeps `plansDirectory` and
  `autoMemoryEnabled: false`, registers `protect_seeds.py` under `PreToolUse`, and carries the `enabledPlugins` block last, where
  `claude plugin install juniper-data-kit --marketplace <clean clone> --scope project` writes it. The chapter's copy lines take
  the block out first (a kit installed in chapter 12 would otherwise load before the plugin section), so the install writes it
  back and the file ends up as it is here.
- `.claude/settings.local.json` is the personal sample, gitignored: `Bash(uv run *)` and `enabledMcpjsonServers`. Append
  `CLAUDE.local.md` and `.claude/settings.local.json` to the repository's `.gitignore`.
- `.claude/rules/dbt.md` applies to `models/marts/**/*.sql` only.
- `.claude/skills/reorder-list/` is the skill (`SKILL.md`) and its script `reorder_summary.py`: `dbt build`, then the size of
  the reorder list and the counts that need a recount.
- `.claude/agents/stock-reviewer.md` is the read-only reviewer (`Read, Grep, Glob`, `memory: project`), and
  `.claude/agent-memory/stock-reviewer/MEMORY.md` is its seeded notes.
- `.claude/hooks/protect_seeds.py` is the guard on `seeds/`.
- `.mcp.json` is the read-only DuckDB server, `inventory`, on `inventory.duckdb`. Approve it in the local settings file.
- `.sqlfluff` is the repository's lint style. The team plugin's lint hook uses it instead of the kit's.
- `models/marts/mart_reorder_list.sql` is the fixed mart: rows whose latest count is negative leave the reorder list
  (197 rows, 1,927 units; 199 and 2,011 before).

The team plugin itself is not in this folder. Install it from a clean clone of the sales project, never from its working
folder (chapter 12 says why).
