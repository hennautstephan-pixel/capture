from __future__ import annotations


import argparse
import json

from pathlib import Path


from capture_recovery.recovery.file_recovery_engine import (
    FileRecoveryEngine,
)


from capture_recovery.reconstruction import (
    RecoveryOrchestrator,
    ObjectLibrary,
    ReconstructionStrategy,
)



class RecoveryReport:
    """
    CLI recovery report.
    """

    def __init__(
        self,
        result,
    ) -> None:

        self.success = result.success

        self.input_file = str(
            result.input_file
        )

        self.reference_file = str(
            result.reference_file
        )

        self.output_file = str(
            result.output_file
        )

        self.input_size = (
            result.input_size
        )

        self.output_size = (
            result.output_size
        )

        self.repaired_regions = (
            result.repaired_regions
        )


    def to_dict(
        self,
    ) -> dict:
        """
        Convert report to JSON data.

        Keeps compatibility with previous CLI reports.
        """

        return {
            "success": self.success,

            "input_file": self.input_file,

            "reference_file": self.reference_file,

            "output_file": self.output_file,

            "input_size": self.input_size,

            "output_size": self.output_size,

            "repaired_regions": self.repaired_regions,

            # Backward compatibility
            "objects_restored": self.repaired_regions,
        }



def build_engine(
    corpus: Path | None = None,
) -> FileRecoveryEngine:
    """
    Build recovery engine.
    """

    library = ObjectLibrary()


    strategy = ReconstructionStrategy(
        library,
    )


    orchestrator = RecoveryOrchestrator(
        strategy=strategy,
    )


    return FileRecoveryEngine(
        orchestrator,
    )



def _recover_file(
    source: Path,
    reference: Path,
    corpus: Path,
    output: Path,
):
    """
    Internal recovery implementation.
    """

    engine = build_engine(
        corpus,
    )


    return engine.recover_file(
        source,
        reference,
        output,
        object_type="fixture",
    )



def recover_file(
    source: Path,
    reference: Path,
    corpus: Path,
    output: Path,
    report_path: Path | None = None,
):
    """
    CLI compatible recovery function.

    Returns:
        0 success
        1 failure
    """

    result = _recover_file(
        source,
        reference,
        corpus,
        output,
    )


    if report_path is not None:

        report = RecoveryReport(
            result,
        )


        report_path.write_text(
            json.dumps(
                report.to_dict(),
                indent=2,
            ),
            encoding="utf-8",
        )


    return (
        0
        if result.success
        else 1
    )



def build_parser():
    """
    Build command line parser.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Recover a corrupted Capture project"
        )
    )


    parser.add_argument(
        "source",
        type=Path,
        help="Corrupted Capture file",
    )


    parser.add_argument(
        "--reference",
        required=True,
        type=Path,
        help="Reference Capture file",
    )


    parser.add_argument(
        "--corpus",
        required=True,
        type=Path,
        help="Reference corpus directory",
    )


    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Recovered output file",
    )


    parser.add_argument(
        "--report",
        dest="report_path",
        type=Path,
        default=None,
        help="Write recovery report JSON",
    )


    return parser



def main(
    argv=None,
):
    """
    CLI entry point.
    """

    parser = build_parser()


    args = parser.parse_args(
        argv,
    )


    return recover_file(
        source=args.source,

        reference=args.reference,

        corpus=args.corpus,

        output=args.output,

        report_path=args.report_path,
    )