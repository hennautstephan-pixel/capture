from __future__ import annotations

import hashlib

from capture_recovery.binary.binary_graph import BinaryGraph
from capture_recovery.binary.binary_index import BinaryIndex
from capture_recovery.binary.decode_coverage import DecodeCoverage
from capture_recovery.explorer.binary_exploration_report import (
    BinaryExplorationReport,
)
from capture_recovery.explorer.binary_explorer import BinaryExplorer


def test_explore_returns_report(tmp_path) -> None:
    file_path = tmp_path / "demo.c2p"
    file_path.write_bytes(b"Capture Recovery")

    explorer = BinaryExplorer()

    report = explorer.explore(file_path)

    assert isinstance(report, BinaryExplorationReport)


def test_file_size_is_detected(tmp_path) -> None:
    data = b"1234567890"

    file_path = tmp_path / "demo.c2p"
    file_path.write_bytes(data)

    report = BinaryExplorer().explore(file_path)

    assert report.container.file_size == len(data)


def test_path_is_preserved(tmp_path) -> None:
    file_path = tmp_path / "demo.c2p"
    file_path.write_bytes(b"abc")

    report = BinaryExplorer().explore(file_path)

    assert report.container.path == str(file_path)


def test_sha256_is_computed(tmp_path) -> None:
    data = b"Capture Recovery"

    file_path = tmp_path / "demo.c2p"
    file_path.write_bytes(data)

    report = BinaryExplorer().explore(file_path)

    expected = hashlib.sha256(data).hexdigest()

    assert report.sha256 == expected


def test_index_is_empty(tmp_path) -> None:
    file_path = tmp_path / "demo.c2p"
    file_path.write_bytes(b"")

    report = BinaryExplorer().explore(file_path)

    assert isinstance(report.index, BinaryIndex)
    assert report.index.count() == 0


def test_graph_is_empty(tmp_path) -> None:
    file_path = tmp_path / "demo.c2p"
    file_path.write_bytes(b"")

    report = BinaryExplorer().explore(file_path)

    assert isinstance(report.graph, BinaryGraph)
    assert len(report.graph) == 0


def test_coverage_is_created(tmp_path) -> None:
    file_path = tmp_path / "demo.c2p"
    file_path.write_bytes(b"")

    report = BinaryExplorer().explore(file_path)

    assert isinstance(report.coverage, DecodeCoverage)


def test_sections_are_empty(tmp_path) -> None:
    file_path = tmp_path / "demo.c2p"
    file_path.write_bytes(b"")

    report = BinaryExplorer().explore(file_path)

    assert report.section_count == 0