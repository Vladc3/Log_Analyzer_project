import gzip
import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest

from parser import read_lines

SAMPLE = Path(__file__).parent / "data" / "sample.log"


def test_reads_every_line_without_newlines():
    lines = list(read_lines(SAMPLE))
    assert len(lines) == 10
    assert lines[0] == "2026-10-01 12:00:00 INFO Service started on port 8080"
    assert not any(line.endswith("\n") for line in lines)


def test_is_lazy_iterator():
    # Streaming: nothing is read until we iterate, so big files don't fill memory.
    assert isinstance(read_lines(SAMPLE), Iterator)


def test_gz_gives_same_lines_as_plain(tmp_path):
    gz_path = tmp_path / "sample.log.gz"
    with open(SAMPLE, "rb") as src, gzip.open(gz_path, "wb") as dst:
        shutil.copyfileobj(src, dst)
    assert list(read_lines(gz_path)) == list(read_lines(SAMPLE))


def test_strips_windows_line_endings(tmp_path):
    path = tmp_path / "crlf.log"
    path.write_bytes(b"ERROR one\r\nINFO two\r\n")
    assert list(read_lines(path)) == ["ERROR one", "INFO two"]


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        list(read_lines("does-not-exist.log"))
