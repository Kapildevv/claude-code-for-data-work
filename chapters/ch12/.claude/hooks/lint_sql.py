"""PostToolUse hook: lint a .sql file that Claude has just written or edited.

The tool has already run, so exit 2 cannot undo it. It sends the findings to Claude,
who fixes them in the next step.

The project's own .sqlfluff wins. A project that has none gets the kit's rules, which sit
at the root of the folder this script lives in (.claude/hooks/lint_sql.py -> that root).
"""

import json
import os
import sys
from pathlib import Path

import sqlfluff

call = json.load(sys.stdin)
path = Path(call["tool_input"]["file_path"])
if path.suffix != ".sql" or not path.exists():
    sys.exit(0)

project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or call.get("cwd") or ".")
config = project / ".sqlfluff"
if not config.exists():
    config = Path(__file__).resolve().parents[2] / ".sqlfluff"

found = sqlfluff.lint(path.read_text(encoding="utf-8"), config_path=str(config))
if found:
    print(f"sqlfluff reports {len(found)} violations in {path.name}:", file=sys.stderr)
    for v in found:
        print(f"  line {v['start_line_no']}: {v['code']} {v['description']}", file=sys.stderr)
    sys.exit(2)
