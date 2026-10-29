from pathlib import Path

from matcher import LEVELS, find_matches
from parser import read_lines
from results import Match, summarize

SAMPLE = Path(__file__).parent / "data" / "sample.log"


def test_finds_all_levels_in_sample_with_line_numbers():
    matches = list(find_matches(read_lines(SAMPLE), LEVELS))
    assert [(m.line_number, m.level) for m in matches] == [
        (2, "WARNING"),
        (3, "ERROR"),
        (5, "ERROR"),
        (7, "CRITICAL"),
        (9, "WARNING"),
    ]
    assert matches[1].text.endswith("ERROR Database connection failed: timeout after 30s")


def test_filters_by_requested_level():
    matches = list(find_matches(read_lines(SAMPLE), ["ERROR"]))
    assert {m.level for m in matches} == {"ERROR"}
    assert len(matches) == 2


def test_matches_whole_uppercase_words_only():
    lines = [
        "INFO no errors found",  # lowercase: a message, not a level
        "INFO exported ERRORS_TOTAL metric",  # part of a bigger word
        "[ERROR] bracketed level still counts",
    ]
    matches = list(find_matches(lines, ["ERROR"]))
    assert [m.line_number for m in matches] == [3]


def test_summary_counts_every_requested_level_even_when_zero():
    matches = [Match(1, "ERROR", "x"), Match(2, "ERROR", "y"), Match(3, "WARNING", "z")]
    assert summarize(matches, ["CRITICAL", "ERROR", "WARNING"]) == {
        "CRITICAL": 0,
        "ERROR": 2,
        "WARNING": 1,
    }
