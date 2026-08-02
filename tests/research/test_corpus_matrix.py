from __future__ import annotations

import zlib

from capture_recovery.research import (
    CorpusMatrix,
    CorpusMatrixAnalyzer,
)
from extract_known_instances import matrix


def create_project(
    path,
    payload: bytes,
):

    path.write_bytes(
        b"HEADER"
        + zlib.compress(payload)
    )


def test_empty_directory(tmp_path):

    matrix = CorpusMatrixAnalyzer().analyze(
        tmp_path
    )

    assert isinstance(
        matrix,
        CorpusMatrix,
    )

    assert matrix.project_count == 0

    assert matrix.entries == []


def test_single_project(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"hello",
    )

    matrix = CorpusMatrixAnalyzer().analyze(
        tmp_path
    )

    assert matrix.project_count == 1
    assert len(matrix.entries) == 0


def test_two_projects(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"abc",
    )

    create_project(
        tmp_path / "b.c2p",
        b"xyz",
    )

    matrix = CorpusMatrixAnalyzer().analyze(
        tmp_path
    )

    assert matrix.project_count == 2
    assert len(matrix.entries) == 1


def test_get_is_symmetric(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"a",
    )

    create_project(
        tmp_path / "b.c2p",
        b"b",
    )

    matrix = CorpusMatrixAnalyzer().analyze(
        tmp_path
    )

    a = tmp_path / "a.c2p"
    b = tmp_path / "b.c2p"

    assert matrix.get(
        a,
        b,
    ) is matrix.get(
        b,
        a,
    )


def test_identical_pairs(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"same",
    )

    create_project(
        tmp_path / "b.c2p",
        b"same",
    )

    matrix = CorpusMatrixAnalyzer().analyze(
        tmp_path
    )

    assert len(
        matrix.identical_pairs()
    ) >= 1


def test_different_pairs(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"aaa",
    )

    create_project(
        tmp_path / "b.c2p",
        b"bbb",
    )

    matrix = CorpusMatrixAnalyzer().analyze(
        tmp_path
    )

    assert len(
        matrix.different_pairs()
    ) >= 1