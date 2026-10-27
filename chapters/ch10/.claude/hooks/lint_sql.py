"""PostToolUse hook: lint a .sql file that Claude has just written or edited.

The tool has already run, so exit 2 cannot undo it. It sends the findings to Claude,
who fixes them in the next step.
"""

import json
import sys
from pathlib import Path

import sqlfluff

ROOT = Path(__file__).resolve().parents[2]  # .claude/hooks/lint_sql.py -> the project root

call = json.load(sys.stdin)
path = Path(call["tool_input"]["file_path"])
if path.suffix != ".sql" or not path.exists():
    sys.exit(0)

found = sqlfluff.lint(path.read_text(encoding="utf-8"), config_path=str(ROOT / ".sqlfluff"))
if found:
    print(f"sqlfluff reports {len(found)} violations in {path.name}:", file=sys.stderr)
    for v in found:
        print(f"  line {v['start_line_no']}: {v['code']} {v['description']}", file=sys.stderr)
    sys.exit(2)
