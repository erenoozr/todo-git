# todo-git

Scans code for `TODO`, `FIXME`, `HACK`, `XXX` and `shortcut:` notes and produces a single-page HTML report.
The report follows light/dark mode and shows a per-tag summary.

## Usage

Python 3.8+, no dependencies.

```
python todo_git.py C:\Dev\myproject
python todo_git.py C:\Dev\myproject -o report.html
```

The default output is `todo-report.html` in the current directory.

## What it matches

- `TODO`, `FIXME`, `HACK`, `XXX` in uppercase as whole words. Words like `todos` or `XXXL` don't match.
- Lowercase notes in the form `shortcut:`.

## What it skips

- `.git`, `node_modules`, `venv`, `.venv`, `dist`, `build`, `__pycache__` folders. It never descends into them.
- Files larger than 1 MB and binary files.
- The report itself, even when it is written inside the scanned folder.

Non-UTF-8 text files are still scanned; undecodable characters show up as `?`.

## Limits

It matches line by line with a regex and does not check whether the line is a comment. For example, a `TODO` inside a string is also matched.

## Development

```
pip install pytest
python -m pytest tests
```

License: MIT
