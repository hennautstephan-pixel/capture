from __future__ import annotations

import argparse
from pathlib import Path

from capture_recovery.analyzers.structure_analyzer import StructureAnalyzer
from capture_recovery.models import report
from src.capture_recovery.detectors import (
    AsciiDetector,
    DetectorPipeline,
    FloatDetector,
    IntegerDetector,
    SignatureDetector,
)
from src.capture_recovery.exporters import JsonExporter
from src.capture_recovery.models import Report


def build_pipeline() -> DetectorPipeline:
    """
    Construit la chaîne de détection utilisée pour analyser un fichier.
    """
    return DetectorPipeline(
        [
            SignatureDetector(),
            AsciiDetector(),
            IntegerDetector(),
            FloatDetector(),
        ]
    )


def scan(filename: Path) -> Report:
    """
    Analyse un fichier Capture (.c2p) et retourne un rapport.
    """

    filename = filename.expanduser().resolve()

    if not filename.exists():
        raise FileNotFoundError(
            f"Le fichier n'existe pas :\n{filename}"
        )

    if not filename.is_file():
        raise IsADirectoryError(
            f"Le chemin n'est pas un fichier :\n{filename}"
        )

    try:
        data = filename.read_bytes()
    except OSError as exc:
        raise RuntimeError(
            f"Impossible de lire le fichier :\n{filename}"
        ) from exc

    report = Report(
        filename=filename.name,
        filesize=len(data),
    )

    pipeline = build_pipeline()

    detections = pipeline.detect(data)

    for detection in detections:
        report.add_detection(detection)

    report.update_statistics()

    from src.capture_recovery.analyzers import StructureAnalyzer

    StructureAnalyzer().analyze(report)

    from src.capture_recovery.analyzers import SummaryAnalyzer

    SummaryAnalyzer().analyze(report)

    return report


def main() -> None:

    parser = argparse.ArgumentParser(
        description="Analyse un projet Capture (.c2p)."
    )

    parser.add_argument(
        "file",
        help="Projet Capture (*.c2p)",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Exporter un rapport JSON.",
    )

    args = parser.parse_args()

    filename = Path(args.file)

    try:
        report = scan(filename)
    except Exception as exc:
        print()
        print(f"Erreur : {exc}")
        raise SystemExit(1)

    print()
    print("Capture Recovery")
    print("================")
    print()

    print(f"Fichier     : {report.filename}")
    print(f"Taille      : {report.filesize:,} octets")
    print(f"Détections  : {report.detection_count}")
    print()

    for datatype, count in sorted(report.statistics.by_type.items()):
        print(f"{datatype:12} {count}")
    print(f"Blocs       : {report.block_count}")
    print(f"Résultats   : {report.finding_count}")

    if args.json:
        output = filename.with_suffix(".report.json")

        JsonExporter().export(
            report,
            output,
        )

        print()
        print(f"Rapport JSON écrit dans :")
        print(output)

    print()


if __name__ == "__main__":
    main()

print()
print("Blocks")
print("------")

for block in report.blocks:

    print(
        f"{block.offset:08X}  "
        f"{block.name:<12} "
        f"{block.length:8d} B"
    )