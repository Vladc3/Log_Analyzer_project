"""Find log lines that contain a severity level, using a regex."""

import re
from collections.abc import Iterable, Iterator

from results import Match

LEVELS = ("CRITICAL", "ERROR", "WARNING")


def build_pattern(levels: Iterable[str]) -> re.Pattern[str]:
    # \b = word boundary: "ERROR" and "[ERROR]" match, "ERRORS_TOTAL" doesn't.
    # Case-sensitive on purpose, so "no errors found" in a message isn't a hit.
    return re.compile(r"\b(" + "|".join(re.escape(lvl) for lvl in levels) + r")\b")


def find_matches(lines: Iterable[str], levels: Iterable[str]) -> Iterator[Match]:
    # LIMITATION: the level word can appear anywhere in the line, so a message like
    # "INFO retry after ERROR" counts as ERROR. Anchor to a real log format if that bites.
    pattern = build_pattern(levels)
    for number, line in enumerate(lines, start=1):
        found = pattern.search(line)
        if found:
            yield Match(number, found.group(1), line)
