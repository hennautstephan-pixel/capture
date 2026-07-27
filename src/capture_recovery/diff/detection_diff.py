from pathlib import Path

from capture_scan import scan

from src.capture_recovery.diff import DiffEngine


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("file_a")

    parser.add_argument("file_b")

    args = parser.parse_args()

    report_a = scan(Path(args.file_a))

    report_b = scan(Path(args.file_b))

    diff = DiffEngine().compare(
        report_a,
        report_b,
    )

    print()
    print("Capture Diff")
    print("=" * 60)
    print()

    print(diff.filename_a)
    print("↓")
    print(diff.filename_b)
    print()

    for name, values in diff.statistics.items():

        a, b = values

        delta = b - a

        print(
            f"{name:<20}"
            f"{a:>6}"
            f" -> "
            f"{b:<6}"
            f" ({delta:+})"
        )