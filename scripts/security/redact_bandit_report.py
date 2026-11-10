"""Remove source snippets from Bandit's JSON report before artifact upload."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def remove_code_snippets(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: remove_code_snippets(item)
            for key, item in value.items()
            if key != "code"
        }
    if isinstance(value, list):
        return [remove_code_snippets(item) for item in value]
    return value


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: redact_bandit_report.py INPUT OUTPUT", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    report = json.loads(source.read_text(encoding="utf-8"))
    destination.write_text(
        json.dumps(remove_code_snippets(report), indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
