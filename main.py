"""Entry point: python main.py app.log --level ERROR --format json"""

import sys

from config import parse_args
from matcher import find_matches
from parser import read_lines
from reporter import FORMATTERS
from results import summarize


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        # The file is streamed; only the matching lines are kept in memory.
        matches = list(find_matches(read_lines(args.logfile), args.level))
    except (OSError, EOFError) as e:  # missing file, no permission, corrupt or truncated .gz
        print(f"error: {args.logfile}: {e}", file=sys.stderr)
        return 1
    print(FORMATTERS[args.format](matches, summarize(matches, args.level)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
