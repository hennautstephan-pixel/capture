from __future__ import annotations

import argparse
from pathlib import Path


from capture_recovery.research.corpus_loader import (
    CorpusLoader,
)

from capture_recovery.tools.stream_sample_loader import (
    StreamSampleLoader,
)

from capture_recovery.tools.diff_stream import (
    StreamDiffer,
)

from capture_recovery.tools.diff_analyzer import (
    DiffAnalyzer,
)

from capture_recovery.tools.intelligent_object_identifier import (
    IntelligentObjectIdentifier,
)


def analyze_files(
    reference_file: Path,
    target_file: Path,
    corpus_path: Path,
) -> int:
    """
    Analyse the difference between two Capture files
    using corpus knowledge.
    """

    loader = CorpusLoader()

    knowledge_base = loader.load(
        corpus_path,
    )

    sample_loader = StreamSampleLoader()

    differ = StreamDiffer()

    analyzer = DiffAnalyzer()

    identifier = IntelligentObjectIdentifier()


    reference_stream = sample_loader.load(
        reference_file,
    )

    target_stream = sample_loader.load(
        target_file,
    )


    diff = differ.compare(
        reference_stream,
        target_stream,
    )


    analysis = analyzer.analyze(
        diff,
    )


    result = identifier.identify(
        analysis,
        knowledge_base,
    )


    print()

    print("=" * 60)
    print(" Capture Recovery - Intelligent Analysis")
    print("=" * 60)

    print()

    print(
        f"Reference : {reference_file}"
    )

    print(
        f"Target    : {target_file}"
    )

    print(
        f"Candidates: {result.candidate_count}"
    )

    print()


    for index, candidate in enumerate(
        result.candidates,
        start=1,
    ):

        print("-" * 60)

        print(
            f"Candidate {index}"
        )

        print(
            f"Offset     : {candidate.offset}"
        )

        print(
            f"Size       : {candidate.size}"
        )

        print(
            f"Type       : {candidate.object_type}"
        )

        print(
            f"Confidence : {candidate.confidence:.2f}"
        )


        if candidate.evidence:

            print()

            print(
                "Evidence:"
            )

            for item in candidate.evidence:

                print(
                    f"  - {item}"
                )


    print()

    return 0



def analyze_file(
    file_path: Path,
    corpus_path: Path,
) -> int:
    """
    Compatibility wrapper.

    Used by the lightweight CLI tests
    and previous API.

    Real intelligent analysis requires
    two valid Capture files and uses
    analyze_files().
    """

    loader = CorpusLoader()

    knowledge_base = loader.load(
        corpus_path,
    )


    print()

    print("=" * 60)
    print(" Capture Recovery - Intelligent Analysis")
    print("=" * 60)

    print()

    print(
        f"File : {file_path}"
    )

    print(
        f"Corpus entries : {len(knowledge_base.knowledge())}"
    )

    print(
        "Single-file analysis mode."
    )

    print()

    return 0



def main() -> int:
    """
    Command line entry point.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Analyze Capture differences "
            "using corpus knowledge."
        )
    )


    parser.add_argument(
        "reference",
        type=Path,
        help=(
            "Reference Capture .c2p file"
        ),
    )


    parser.add_argument(
        "target",
        type=Path,
        nargs="?",
        default=None,
        help=(
            "Target Capture .c2p file"
        ),
    )


    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path(
            "corpus_knowledge.json",
        ),
        help=(
            "Corpus knowledge JSON file"
        ),
    )


    args = parser.parse_args()


    if args.target is None:

        return analyze_file(
            args.reference,
            args.corpus,
        )


    return analyze_files(
        args.reference,
        args.target,
        args.corpus,
    )



if __name__ == "__main__":

    raise SystemExit(
        main()
    )