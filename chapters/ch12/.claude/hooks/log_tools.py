"""PostToolUse hook: append one JSON line per finished tool call to .claude/logs/tools.jsonl.

The log belongs to the project the session runs in, not to the folder this script lives in. Claude Code
sets CLAUDE_PROJECT_DIR for a hook, and the call's JSON carries the working directory as a fallback.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

call = json.load(sys.stdin)
project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or call.get("cwd") or ".")
LOG = project / ".claude" / "logs" / "tools.jsonl"

args = call.get("tool_input", {})
entry = {
    "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "tool": call["tool_name"],
    "target": str(args.get("file_path") or args.get("command") or "")[:120],
}
LOG.parent.mkdir(parents=True, exist_ok=True)
with LOG.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps(entry) + "\n")
