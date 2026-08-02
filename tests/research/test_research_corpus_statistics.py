from __future__ import annotations

import zlib

from capture_recovery.research.corpus_statistics import (
    CorpusStatistics,
    CorpusStatisticsAnalyzer,
)


def create_sample(path):

    payload = b"Hello Capture"

    compressed = zlib.compress(payload)

    path.write_bytes(
        b"HEADER" + compressed
    )


def test_analyze(tmp_path):

    file = tmp_path / "sample.c2p"

    create_sample(file)

    analyzer = CorpusStatisticsAnalyzer()

    stats = analyzer.analyze(file)

    assert isinstance(
        stats,
        CorpusStatistics,
    )

    assert stats.file_size == file.stat().st_size

    assert stats.header_size == 6

    assert stats.compressed_size > 0

    assert stats.decompressed_size == len(
        b"Hello Capture"
    )

    assert stats.compression_ratio > 0

    assert stats.trailing_bytes == 0


def test_analyze_directory(tmp_path):

    create_sample(tmp_path / "a.c2p")

    create_sample(tmp_path / "b.c2p")

    analyzer = CorpusStatisticsAnalyzer()

    stats = analyzer.analyze_directory(
        tmp_path
    )

    assert len(stats) == 2


def test_average_ratio(tmp_path):

    create_sample(tmp_path / "a.c2p")

    analyzer = CorpusStatisticsAnalyzer()

    stats = analyzer.analyze_directory(
        tmp_path
    )

    assert (
        analyzer.average_compression_ratio(
            stats
        )
        > 0
    )


def test_total_sizes(tmp_path):

    create_sample(tmp_path / "a.c2p")

    create_sample(tmp_path / "b.c2p")

    analyzer = CorpusStatisticsAnalyzer()

    stats = analyzer.analyze_directory(
        tmp_path
    )

    assert (
        analyzer.total_compressed_size(
            stats
        )
        > 0
    )

    assert (
        analyzer.total_decompressed_size(
            stats
        )
        > 0
    )


def test_largest_project(tmp_path):

    #
    # Petit projet
    #
    small_payload = b"Hello Capture"

    (tmp_path / "small.c2p").write_bytes(
        b"HEADER"
        + zlib.compress(small_payload)
    )

    #
    # Grand projet
    #
    large_payload = bytes(range(256)) * 4

    (tmp_path / "large.c2p").write_bytes(
        b"HEADER"
        + zlib.compress(large_payload)
    )

    analyzer = CorpusStatisticsAnalyzer()

    stats = analyzer.analyze_directory(
        tmp_path
    )

    largest = analyzer.largest_project(
        stats
    )

    assert largest is not None
    assert largest.path.name == "large.c2p"