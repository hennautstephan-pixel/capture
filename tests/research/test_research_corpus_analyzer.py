from pathlib import Path

from capture_recovery.research import (
    CorpusAnalyzer,
)


def test_analyze_vide():

    analyzer = CorpusAnalyzer()

    analysis = analyzer.analyze(
        Path("samples") / "Vide.c2p"
    )

    assert analysis.header_size == 62

    assert analysis.stream.offset == 62

    assert analysis.stream.trailing_bytes == 8

    assert analysis.stream.compressed_size > 1000

    assert analysis.stream.decompressed_size > 10000