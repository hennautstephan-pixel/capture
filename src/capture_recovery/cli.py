"""
Capture Recovery

Command Line Interface
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .structure_parser import StructureParser


# ----------------------------------------------------------------------

def inspect_file(filename: str) -> int:
    """
    Analyse un fichier Capture.
    """

    path = Path(filename)

    if not path.exists():

        print(f"Erreur : fichier introuvable : {path}")

        return 1

    parser = StructureParser(path)

    report = parser.run()

    print()
    print("=" * 60)
    print("Capture Recovery Report")
    print("=" * 60)
    print()

    print(f"Fichier   : {report.filename}")
    print(f"Taille    : {report.filesize:,} bytes")
    print()

    print("Statistiques")
    print("-" * 60)

    print(f"Findings            : {len(report.findings)}")
    print(f"Blocs               : {len(report.blocks)}")
    print(f"ASCII               : {report.statistics.ascii_strings}")
    print(f"UTF16               : {report.statistics.utf16_strings}")
    print(f"Pointeurs           : {report.statistics.pointers}")
    print(f"Signatures          : {report.statistics.signatures}")
    print(f"Blocs compressés    : {report.statistics.compressed_blocks}")

    print()

    #
    # Aperçu des Findings
    #

    if report.findings:

        print("Premiers Findings")
        print("-" * 60)

        for finding in report.findings[:20]:

            print(
                f"{finding.offset:08X}  "
                f"{finding.category.value:<12}  "
                f"{finding.value}"
            )

        if len(report.findings) > 20:

            print()

            print(
                f"... {len(report.findings)-20} findings supplémentaires ..."
            )

    print()

    return 0


# ----------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="capture-recovery",
        description="Capture 2024 Reverse Engineering Toolkit",
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    inspect = sub.add_parser(
        "inspect",
        help="Analyse un fichier .c2p",
    )

    inspect.add_argument(
        "file",
        help="Fichier Capture",
    )

    return parser


# ----------------------------------------------------------------------

def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    match args.command:

        case "inspect":

            sys.exit(
                inspect_file(args.file)
            )

        case _:

            parser.print_help()

            sys.exit(1)


# ----------------------------------------------------------------------

if __name__ == "__main__":

    main()