from pathlib import Path

from capture_recovery.corpus import (
    AnalysisReport,
    CorpusDiff,
    CorpusEntry,
    DiffAnalyzer,
    Difference,
)


def entry():

    return CorpusEntry(
        path=Path("sample.c2p"),
        format="capture_binary",
        size=100,
        sha256="abc",
        compressed_size=50,
        decompressed_size=120,
        stream_offset=62,
    )


def test_empty():

    report = DiffAnalyzer().analyze(
        CorpusDiff(
            left=entry(),
            right=entry(),
            differences=(),
        )
    )

    assert isinstance(
        report,
        AnalysisReport,
    )

    assert report.region_count == 0


def test_regions():

    diff = CorpusDiff(
        left=entry(),
        right=entry(),
        differences=(
            Difference("size", 10, 20),
            Difference("sha256", "a", "b"),
        ),
    )

    report = DiffAnalyzer().analyze(
        diff,
    )

    assert report.region_count == 1

    assert report.difference_count == 2