"""
Command line interface for Capture Recovery.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from capture_recovery import recover


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recover corrupted Capture projects."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input Capture project file",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output recovered project file",
    )

    args = parser.parse_args()


    result = recover(
        args.input,
    )


    project = result["project"]


    if project is None:
        print(
            "Recovery failed: no project reconstructed."
        )
        return 1


    # Export temporaire :
    # sera remplacé par CaptureProjectWriter
    args.output.write_text(
        str(project),
        encoding="utf-8",
    )


    print(
        f"Recovery completed: {args.output}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )