"""PreToolUse guard: nothing may write to seeds/ (the warehouse feed owns those files).

Claude Code sends the pending tool call as JSON on stdin. Exit 2 blocks the call and sends
stderr to Claude; exit 0 lets it go ahead. A best-effort net: it reads the command text,
not what the command will do. Reading seeds/ is fine, and `dbt build` only reads it.
"""

import json
import re
import sys

SEEDS = re.compile(r"(?<![\w.-])seeds/", re.IGNORECASE)
WRITE_VERB = re.compile(
    r"(?<![\w./-])(cp|mv|rm|rmdir|tee|touch|truncate|dd|ln|rsync|install|sed|copy|move|del|erase|ren|rename"
    r"|out-file|set-content|add-content|clear-content|remove-item|copy-item|move-item|new-item|rename-item)(?![\w-])",
    re.IGNORECASE,
)
REDIRECT_INTO_SEEDS = re.compile(r">>?\s*['\"]?\S*seeds/", re.IGNORECASE)

call = json.load(sys.stdin)
args = call["tool_input"]
if call["tool_name"] in ("Write", "Edit"):
    text = args["file_path"].replace("\\", "/")  # Windows paths arrive with backslashes
    blocked = bool(SEEDS.search(text))
else:  # Bash or PowerShell
    text = args["command"].replace("\\", "/")
    blocked = bool(SEEDS.search(text)) and bool(WRITE_VERB.search(text) or REDIRECT_INTO_SEEDS.search(text))

if blocked:
    print("Blocked: this call names seeds/ and writes (the warehouse feed owns those files). "
          "Reading is fine. Fix a data problem in a model, and report it.", file=sys.stderr)
    sys.exit(2)
