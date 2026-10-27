# Chapter 9

A read-only reviewer sub-agent and its seeded notes:

- `.claude/agents/dq-reviewer.md` is the agent. It reads `out/dq_profile.txt` (chapter 8's
  `dq_profile.py` saves it) and the raw files, and replies in a fixed four-line shape. Its fields:
  `tools: Read, Grep, Glob` (no Bash, so it cannot run the profile script or write through a shell),
  `model: haiku`, `memory: project`, and no `skills` (every skill in this project runs a script, and a
  script needs Bash). The description has no colon-and-space and the file uses Unix line endings:
  with an unquoted `: ` in the description and Windows line endings the agent is not loaded at all,
  with no message at run time (`claude plugin validate .claude/agents` reports it).
- `.claude/agent-memory/dq-reviewer/MEMORY.md` is the agent's project-scope memory, seeded with
  Luis's ticket JL-117 ("store S10's till re-sends its batch"), which is in none of the six CSV
  files. Because `memory: project` keeps it inside the repository, commit it: the agent's own later
  edits then show up in `git status`.

Run `uv run python .claude/skills/profile-data/scripts/dq_profile.py` first, so that
`out/dq_profile.txt` is current, then ask: `Use the dq-reviewer sub-agent to review tonight's drop.`

**One change outside this folder.** Agent memory is part of auto memory, and chapter 6 set
`"autoMemoryEnabled": false` in `.claude/settings.json`. With that key false the `memory` field has no
effect: the agent had no write tool and could not update its notes (the seeded file can still be read
by an agent that goes looking for it). Change the key to `true` for the agent to read, curate and
write `MEMORY.md`. The same key turns Claude's own auto memory back on for the main session. This
folder does not carry a `settings.json`, because chapter 6 owns that file.
