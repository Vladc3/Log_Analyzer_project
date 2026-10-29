import json

from reporter import to_json, to_text
from results import Match

MATCHES = [
    Match(3, "ERROR", "12:01 ERROR db down"),
    Match(7, "CRITICAL", "12:03 CRITICAL out of memory"),
]
SUMMARY = {"CRITICAL": 1, "ERROR": 1, "WARNING": 0}


def test_text_lists_matches_with_line_numbers_then_summary():
    assert to_text(MATCHES, SUMMARY) == (
        "3: 12:01 ERROR db down\n"
        "7: 12:03 CRITICAL out of memory\n"
        "\n"
        "Summary: CRITICAL=1 ERROR=1 WARNING=0 total=2"
    )


def test_text_with_no_matches_is_just_the_summary():
    assert to_text([], {"ERROR": 0}) == "Summary: ERROR=0 total=0"


def test_json_is_valid_and_has_summary_total_and_matches():
    data = json.loads(to_json(MATCHES, SUMMARY))
    assert data == {
        "summary": SUMMARY,
        "total": 2,
        "matches": [
            {"line_number": 3, "level": "ERROR", "text": "12:01 ERROR db down"},
            {"line_number": 7, "level": "CRITICAL", "text": "12:03 CRITICAL out of memory"},
        ],
    }
