"""What a match looks like, and how matches are counted."""

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Match:
    line_number: int  # 1-based, like `grep -n` and editors
    level: str
    text: str


def summarize(matches: Iterable[Match], levels: Iterable[str]) -> dict[str, int]:
    """Count matches per level. Every requested level appears, even with 0."""
    counts = Counter(m.level for m in matches)
    return {level: counts[level] for level in levels}
