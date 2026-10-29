"""Stream a log file line by line. Plain text and .gz are both supported."""

import gzip
from collections.abc import Iterator
from pathlib import Path


def read_lines(path: str | Path) -> Iterator[str]:
    """Yield lines one at a time without the trailing newline.

    Only one line is in memory at a time, so file size doesn't matter.
    Bytes that aren't valid UTF-8 are replaced instead of crashing the run.
    """
    path = Path(path)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            yield line.rstrip("\r\n")
