from __future__ import annotations

import argparse
from pathlib import Path

from capture_recovery.tools.sample_analyzer import (
    SampleAnalyzer,
)


def main() -> int:
    """
    Command-line entry point for sample analysis.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Analyze a directory containing "
            "Capture sample files."
        ),
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default="samples",
        type=Path,
        help=(
            "Directory containing Capture files "
            "(default: samples)."
        ),
    )

    args = parser.parse_args()

    analyzer = SampleAnalyzer()

    report = analyzer.analyze(
        args.directory,
    )

    statistics = report.statistics

    print()
    print("=" * 60)
    print(" Capture Recovery - Sample Analysis")
    print("=" * 60)
    print(
        f"Directory          : "
        f"{args.directory.resolve()}"
    )
    print(
        f"Files analysed     : "
        f"{statistics.file_count}"
    )
    print(
        f"Comparisons        : "
        f"{statistics.comparison_count}"
    )
    print(
        f"Identical pairs    : "
        f"{statistics.identical_pairs}"
    )
    print(
        f"Different pairs    : "
        f"{statistics.different_pairs}"
    )
    print("=" * 60)
    print()

    if report.comparisons:

        print("Comparisons")
        print("-" * 60)

        for comparison in report.comparisons:

            print(
                f"{comparison.left.name}"
                " <-> "
                f"{comparison.right.name}"
            )

            print(
                "    Differences : "
                f"{comparison.diff.difference_count}"
            )

            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())