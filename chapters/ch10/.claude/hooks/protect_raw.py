"""PreToolUse guard: nothing may write to data/raw/ (Luis's rule).

Claude Code sends the pending tool call as JSON on stdin. Exit 2 blocks the call and sends
stderr to Claude; exit 0 lets it go ahead. A best-effort net: it reads the command text,
not what the command will do.
"""

import json
import re
import sys

RAW = re.compile(r"(?<![\w-])data/raw(?![\w-])", re.IGNORECASE)
WRITE_VERB = re.compile(
    r"(?<![\w./-])(cp|mv|rm|rmdir|tee|touch|truncate|dd|ln|rsync|install|copy|move|del|erase|ren|rename"
    r"|out-file|set-content|add-content|clear-content|remove-item|copy-item|move-item|new-item|rename-item)(?![\w-])",
    re.IGNORECASE,
)
REDIRECT_INTO_RAW = re.compile(r">>?\s*['\"]?\S*data/raw", re.IGNORECASE)

call = json.load(sys.stdin)
args = call["tool_input"]
if call["tool_name"] in ("Write", "Edit"):
    text = args["file_path"].replace("\\", "/")  # Windows paths arrive with backslashes
    blocked = bool(RAW.search(text))
else:  # Bash or PowerShell
    text = args["command"].replace("\\", "/")
    blocked = bool(RAW.search(text)) and bool(WRITE_VERB.search(text) or REDIRECT_INTO_RAW.search(text))

if blocked:
    print("Blocked: this call names data/raw/ and writes (Luis's rule: nothing writes to data/raw/). "
          "Reading is fine. Write results to out/ or data/parquet/ instead.", file=sys.stderr)
    sys.exit(2)
