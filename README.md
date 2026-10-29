# Log File Analyzer

[![CI](https://github.com/Vladc3/Log_Analyzer_project/actions/workflows/ci.yml/badge.svg)](https://github.com/Vladc3/Log_Analyzer_project/actions/workflows/ci.yml)

A small Python CLI that finds `ERROR`, `WARNING` and `CRITICAL` lines in a log file and prints them with a count per level. Standard library only, no runtime dependencies.

## What it does

- Reads plain-text and gzipped (`.gz`) logs line by line (streaming, the whole file is never loaded into memory)
- Matches severity levels with a regex: whole, uppercase words only (`[ERROR]` matches, `errors` and `ERRORS_TOTAL` don't)
- Lets you pick which levels to search with `--level` (repeatable)
- Prints results as plain text or JSON, with a summary count per level
- Exits with a clear message and code `1` if the file is missing, unreadable, or a broken `.gz`

## Limitations

- The level word can appear anywhere in the line, so `INFO retry after ERROR` counts as an ERROR
- Matching lines are kept in memory until the report is printed (the file itself is not)
- No date/time filtering, no custom patterns, no HTML output
- Exit code is `0` whether or not matches are found

## Requirements

Python 3.11 or newer. Nothing to install to run it.

## Usage

```console
$ python main.py tests/data/sample.log
2: 2026-10-01 12:00:05 WARNING Disk usage at 85% on /var
3: 2026-10-01 12:01:10 ERROR Database connection failed: timeout after 30s
5: 2026-10-01 12:01:15 ERROR Database connection failed: timeout after 30s
7: 2026-10-01 12:03:30 CRITICAL Out of memory, killing worker 4
9: 2026-10-01 12:05:00 WARNING Response time 2.4s exceeds threshold

Summary: CRITICAL=1 ERROR=2 WARNING=2 total=5
```

Only one level, as JSON:

```console
$ python main.py tests/data/sample.log --level ERROR --format json
{
  "summary": {
    "ERROR": 2
  },
  "total": 2,
  "matches": [
    {
      "line_number": 3,
      "level": "ERROR",
      "text": "2026-10-01 12:01:10 ERROR Database connection failed: timeout after 30s"
    },
    {
      "line_number": 5,
      "level": "ERROR",
      "text": "2026-10-01 12:01:15 ERROR Database connection failed: timeout after 30s"
    }
  ]
}
```

Several levels, gzipped file (level names are case-insensitive on the command line):

```console
$ python main.py /var/log/app.log.gz --level critical --level warning
```

JSON output pipes well into `jq`:

```console
$ python main.py app.log --format json | jq '.summary'
```

| Exit code | Meaning |
|-----------|---------|
| 0 | Ran successfully |
| 1 | File missing, unreadable, or not a valid `.gz` |
| 2 | Invalid command-line arguments |

## Development

```console
$ python -m venv .venv && source .venv/bin/activate
$ python -m pip install --upgrade pip      # --group needs pip >= 25.1
$ python -m pip install --group dev        # pytest + ruff from pyproject.toml
$ pytest
$ ruff check . && ruff format --check .
```

CI (GitHub Actions) runs the same ruff and pytest commands on Python 3.11 and 3.12 for every push and pull request.

## Project structure

```text
├── main.py          # entry point: wires the pieces together, handles file errors
├── config.py        # argparse options (--level, --format)
├── parser.py        # streams lines from .log / .gz files
├── matcher.py       # regex matching by level
├── results.py       # Match dataclass + per-level summary counts
├── reporter.py      # text and JSON output
├── tests/
│   ├── data/sample.log
│   ├── test_parser.py
│   ├── test_matcher.py
│   └── test_reporter.py
├── pyproject.toml   # project metadata, dev dependencies, pytest + ruff config
└── .github/workflows/ci.yml
```

## Built with Claude Code

I built this with [Claude Code] as a coding assistant. I wrote the spec, reviewed every change and ran the tests.

## What went wrong and how I fixed it

<!-- TODO: fill in -->
