"""PostToolUse hook: append one JSON line per finished tool call to .claude/logs/tools.jsonl."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG = Path(__file__).resolve().parents[1] / "logs" / "tools.jsonl"

call = json.load(sys.stdin)
args = call.get("tool_input", {})
entry = {
    "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "tool": call["tool_name"],
    "target": str(args.get("file_path") or args.get("command") or "")[:120],
}
LOG.parent.mkdir(exist_ok=True)
with LOG.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps(entry) + "\n")
