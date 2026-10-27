# Chapter 11

`.mcp.json` sits at the project root, not inside `.claude/`. It is the file `claude mcp add --scope project`
writes for the two commands in the chapter, and it is committed:

- `warehouse` is a stdio server: `uvx --python 3.14 mcp-server-motherduck@1.1.0 --db-path warehouse.duckdb`.
  It opens `warehouse.duckdb` (chapter 8's database) read-only, because the server's default for a local
  file is read-only and the line has no `--read-write`. Run the command once with `--help` first so the
  package is downloaded before Claude Code starts the server.
- `context7` is an HTTP server at `https://mcp.context7.com/mcp`. Its `Authorization` header is
  `Bearer ${CONTEXT7_API_KEY:-}`: the key, if you have one, lives in an environment variable on your
  machine, and the empty default makes an unset variable send an empty value. Never write the key into the
  file or into the URL. Context7 answers without a key, with lower rate limits.

`.claude/settings.local.json` is chapter 6's personal sample (the `uv run *` allow rule) plus the line the
approval dialog writes when you approve project servers: `enabledMcpjsonServers`. It stays out of git.
Claude Code reads it only in a folder you have trusted (run `claude` in the folder once and accept the
trust dialog); until then `claude mcp list` shows both servers as Pending approval.

Lay these two files over your project, run chapter 8's pipeline so that `warehouse.duckdb` exists, and ask
Claude: "Dana asks: what are net sales for Boulder since 2026-07-06? Answer it from the warehouse server."
The answer to compare is $72,711.65 (store S01, Juniper Lane Boulder).
