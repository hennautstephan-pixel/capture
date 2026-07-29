from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.binary.binary_container import BinaryContainer
from capture_recovery.binary.binary_graph import BinaryGraph
from capture_recovery.binary.binary_index import BinaryIndex
from capture_recovery.binary.binary_object import BinaryObject
from capture_recovery.binary.binary_section import BinarySection
from capture_recovery.binary.decode_coverage import DecodeCoverage
from capture_recovery.explorer.binary_exploration_report import (
    BinaryExplorationReport,
)


def make_report() -> BinaryExplorationReport:
    section = BinarySection(
        name="Header",
        offset=0,
        size=64,
    )

    container = BinaryContainer(
        path="demo.c2p",
        file_size=1024,
        sections=(section,),
    )

    obj = BinaryObject(
        identifier=1,
        offset=64,
        size=32,
        raw_data=b"\x00" * 32,
    )

    index = BinaryIndex(
        objects={
            obj.identifier: obj,
        }
    )

    graph = BinaryGraph()

    coverage = DecodeCoverage(
        total_objects=1,
        decoded_objects=1,
        unknown_objects=0,
        decoded_bytes=32,
        total_bytes=32,
    )

    return BinaryExplorationReport(
        container=container,
        index=index,
        graph=graph,
        coverage=coverage,
        sha256="0" * 64,
    )


def test_creation() -> None:
    report = make_report()

    assert report.container.file_size == 1024
    assert report.index.count() == 1
    assert len(report.graph) == 0
    assert report.sha256 == "0" * 64


def test_object_count() -> None:
    report = make_report()

    assert report.object_count == 1


def test_reference_count() -> None:
    report = make_report()

    assert report.reference_count == 0


def test_section_count() -> None:
    report = make_report()

    assert report.section_count == 1


def test_frozen() -> None:
    report = make_report()

    with pytest.raises(FrozenInstanceError):
        report.container = None  # type: ignore[misc]


def test_contains_expected_components() -> None:
    report = make_report()

    assert report.container is not None
    assert report.index is not None
    assert report.graph is not None
    assert report.coverage is not None
    assert report.sha256 == "0" * 64


def test_counts_are_consistent() -> None:
    report = make_report()

    assert report.object_count == report.index.count()
    assert report.reference_count == len(report.graph)
    assert report.section_count == len(report.container.sections)


def test_sha256_property() -> None:
    report = make_report()

    assert isinstance(report.sha256, str)
    assert len(report.sha256) == 64
    assert report.sha256 == "0" * 64