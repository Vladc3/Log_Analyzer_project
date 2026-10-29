"""Command-line options."""

import argparse

from matcher import LEVELS
from reporter import FORMATTERS


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find ERROR / WARNING / CRITICAL lines in a log file (.gz supported).",
    )
    parser.add_argument("logfile", help="path to a .log or .log.gz file")
    parser.add_argument(
        "--level",
        action="append",
        type=str.upper,  # so --level error works too
        choices=LEVELS,
        help="level to search for; repeat for several (default: all levels)",
    )
    parser.add_argument("--format", choices=FORMATTERS, default="text", help="output format")
    args = parser.parse_args(argv)
    # Default set here, not in add_argument: "append" would add to the default list.
    args.level = args.level or list(LEVELS)
    return args
