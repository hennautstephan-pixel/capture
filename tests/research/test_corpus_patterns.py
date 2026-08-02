from __future__ import annotations

import zlib

from capture_recovery.research import (
    CorpusPatterns,
    CorpusPatternsAnalyzer,
)


def create_project(
    path,
    payload: bytes,
):

    path.write_bytes(
        b"HEADER"
        + zlib.compress(payload)
    )


def test_empty_directory(tmp_path):

    patterns = (
        CorpusPatternsAnalyzer()
        .analyze(tmp_path)
    )

    assert isinstance(
        patterns,
        CorpusPatterns,
    )

    assert patterns.pattern_count == 0

    assert patterns.largest_region() is None

    assert patterns.most_common_region() is None


def test_identical_projects(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"same",
    )

    create_project(
        tmp_path / "b.c2p",
        b"same",
    )

    patterns = (
        CorpusPatternsAnalyzer()
        .analyze(tmp_path)
    )

    assert patterns.pattern_count == 0


def test_different_projects(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"abc",
    )

    create_project(
        tmp_path / "b.c2p",
        b"xyz",
    )

    patterns = (
        CorpusPatternsAnalyzer()
        .analyze(tmp_path)
    )

    assert patterns.pattern_count > 0

    assert (
        patterns.largest_region()
        is not None
    )

    assert (
        patterns.most_common_region()
        is not None
    )


def test_three_projects(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"aaa",
    )

    create_project(
        tmp_path / "b.c2p",
        b"bbb",
    )

    create_project(
        tmp_path / "c.c2p",
        b"ccc",
    )

    patterns = (
        CorpusPatternsAnalyzer()
        .analyze(tmp_path)
    )

    assert patterns.pattern_count >= 1


def test_largest_region(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"abcdef",
    )

    create_project(
        tmp_path / "b.c2p",
        b"abcXYZ",
    )

    patterns = (
        CorpusPatternsAnalyzer()
        .analyze(tmp_path)
    )

    region = patterns.largest_region()

    assert region is not None

    assert region.length > 0


def test_most_common_region(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"111111",
    )

    create_project(
        tmp_path / "b.c2p",
        b"222222",
    )

    create_project(
        tmp_path / "c.c2p",
        b"333333",
    )

    patterns = (
        CorpusPatternsAnalyzer()
        .analyze(tmp_path)
    )

    region = patterns.most_common_region()

    assert region is not None

    assert region.occurrence_count > 0