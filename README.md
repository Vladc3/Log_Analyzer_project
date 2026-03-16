# 🔍 Log File Analyzer

A Python CLI tool for searching and analyzing error messages in large log files.

Parses plain-text and gzipped logs line-by-line, matches entries by severity level (ERROR, WARNING, CRITICAL) using regex, and exports results as text, JSON, or HTML.

## Features
- Memory-efficient streaming parser for large files
- Configurable regex patterns and log level filters
- Timestamp-based filtering with `--since`
- Multiple output formats: plain text, JSON, HTML report
- Summary statistics (error counts by severity)

## Tech stack
`Python` · `argparse` · `re` · `dataclasses` · `gzip`

log_analyzer/
├── main.py            # CLI entry point and application logic
├── parser.py          # Log file reading and chunking utilities
├── matcher.py         # Regex pattern application and error detection
├── results.py         # Data storage and sorting for matches
├── reporter.py        # Output formatting and file writing
├── config.py          # CLI arguments and regex pattern definitions
└── tests/             # Unit and integration testing suite
    └── test_matcher.py
