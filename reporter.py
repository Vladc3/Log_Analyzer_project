"""Turn matches + summary into the text or JSON the user sees."""

import json
from dataclasses import asdict

from results import Match


def to_text(matches: list[Match], summary: dict[str, int]) -> str:
    lines = [f"{m.line_number}: {m.text}" for m in matches]
    if lines:
        lines.append("")  # blank line between matches and summary
    counts = " ".join(f"{level}={n}" for level, n in summary.items())
    lines.append(f"Summary: {counts} total={sum(summary.values())}")
    return "\n".join(lines)


def to_json(matches: list[Match], summary: dict[str, int]) -> str:
    return json.dumps(
        {
            "summary": summary,
            "total": sum(summary.values()),
            "matches": [asdict(m) for m in matches],
        },
        indent=2,
    )


FORMATTERS = {"text": to_text, "json": to_json}
