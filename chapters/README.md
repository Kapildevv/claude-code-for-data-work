# Finished files, chapter by chapter

Each `chNN/` folder holds the `juniper-lane` project's files as they stand at the end of that
chapter: what Claude wrote, the `.claude/` folder so far, and the scripts the chapter adds.
Generated files (`data/`, `*.duckdb`, `out/`) are left out; `make_data.py` and the pipeline
rebuild them. Chapter 1 adds no files, so it has no folder.

Compare your copy with a chapter's folder when something behaves differently from the book.
Do not copy a whole folder into your project ahead of the chapter: the point of each chapter
is building its part yourself. The exception is a chapter that names files to copy. Chapter 8
does: its scripts and SQL models are too long to print, so copy the eleven files it names from
`ch08/` into your project at the same paths.
