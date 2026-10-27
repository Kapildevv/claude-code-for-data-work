# Chapter 7

`.claude/skills/profile-data/SKILL.md` is the first skill: the procedure for profiling any file in
`data/raw/`, so two analysts' profiles have the same shape. The folder name and `name` are equal
(`profile-data`). The description starts with the use case and stays under 200 characters, so the
skill also fits the Claude app's limit. It calls the `profile.py` of chapter 2; chapter 8 moves the
counting into the skill's own `scripts/` folder.

`allowed-tools` lists the one script call in both shapes, `Bash(...)` and `PowerShell(...)`, and
applies for the turn that runs the skill. `argument-hint` is the text the `/` menu shows after the
name.

If you retype the description, keep a colon followed by a space out of it, or wrap the whole value
in double quotes. That text is not valid YAML, and on the book's machine a file saved with Windows
line endings lost its metadata without an error on screen: the skill still ran by name but was no
longer offered to Claude. Check a new skill with `claude -p "/context"` (the Skills table lists it
at about 60 tokens) or `claude plugin validate .claude/skills`. If you created `.claude/skills/`
while a session was open, run `/reload-skills`.

`.claude/commands/weekly-report.md` is the older form: one Markdown file whose text is the prompt
for `/weekly-report`. It runs the query in `models/weekly_sales.sql` (chapter 6) and writes Dana two
sentences; the last row for the report week gives net sales of 41404.95. A skill and a command with
the same name make the same slash command, and the skill wins.

To reuse the skill in the Claude app, copy it without the Claude Code-only fields (`argument-hint`
and `allowed-tools` here) and zip the folder so that `profile-data/SKILL.md` sits at the root of the
zip. The chapter prints the commands. Windows PowerShell 5.1's `Compress-Archive` writes backslashes
in the entry names, so the book uses `tar -a -cf`.
