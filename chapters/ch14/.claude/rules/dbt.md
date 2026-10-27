---
paths:
  - "models/marts/**/*.sql"
---

# Mart models

- Write SQL keywords in lowercase, with each clause on its own line.
- Start the file with a comment that says what one row is.
- A mart is a table. Do not turn it into a view or an incremental model without asking.
- Refer to other models with `ref()`. A new rule on a mart's rows gets a test beside it in
  `models/marts/_marts.yml`.
- A negative `on_hand` is a keying error at the store. Never order against it: leave the row
  out of the reorder list and let `reorder-list` print it for a recount.
- After an edit run `uv run dbt build --select <model>+` and read the last line.
