"""
Unit tests for capture_recovery.diff.models
"""

from __future__ import annotations

from datetime import datetime

from capture_recovery.diff.models import (
    BinaryChange,
    ChangeType,
    DiffMetadata,
    DiffReport,
    DiffStatistics,
    RegionChange,
    SemanticChange,
    StructureChange,
)


# ---------------------------------------------------------------------------
# BinaryChange
# ---------------------------------------------------------------------------


def test_binary_change_before_length():
    change = BinaryChange(
        offset=10,
        before=b"\x01\x02",
        after=b"\x01\x03",
    )

    assert change.before_length == 2


def test_binary_change_after_length():
    change = BinaryChange(
        offset=0,
        before=b"\x01",
        after=b"\x01\x02\x03",
    )

    assert change.after_length == 3


def test_binary_change_delta_positive():
    change = BinaryChange(
        offset=0,
        before=b"\x00",
        after=b"\x00\x01\x02",
    )

    assert change.delta == 2


def test_binary_change_delta_negative():
    change = BinaryChange(
        offset=0,
        before=b"\x00\x01\x02",
        after=b"\x00",
    )

    assert change.delta == -2


def test_binary_change_default_type():
    change = BinaryChange(offset=0)

    assert change.change_type is ChangeType.MODIFY


def test_binary_change_insert():
    change = BinaryChange(
        offset=100,
        before=b"",
        after=b"\xAA",
        change_type=ChangeType.INSERT,
    )

    assert change.change_type is ChangeType.INSERT


# ---------------------------------------------------------------------------
# RegionChange
# ---------------------------------------------------------------------------


def test_region_change_defaults():
    region = object()

    change = RegionChange(
        offset=128,
        region=region,
    )

    assert change.region is region
    assert change.binary_changes == ()


def test_region_change_contains_binary_changes():
    binary = BinaryChange(offset=0)

    region = RegionChange(
        offset=0,
        region="Header",
        binary_changes=(binary,),
    )

    assert len(region.binary_changes) == 1
    assert region.binary_changes[0] is binary


# ---------------------------------------------------------------------------
# StructureChange
# ---------------------------------------------------------------------------


def test_structure_change_defaults():
    change = StructureChange(offset=0)

    assert change.structure_before is None
    assert change.structure_after is None
    assert change.changed_fields == ()


def test_structure_change_fields():
    change = StructureChange(
        offset=0,
        structure_before="A",
        structure_after="B",
        changed_fields=("position", "rotation"),
    )

    assert len(change.changed_fields) == 2
    assert "position" in change.changed_fields
    assert "rotation" in change.changed_fields


# ---------------------------------------------------------------------------
# SemanticChange
# ---------------------------------------------------------------------------


def test_semantic_change_defaults():
    change = SemanticChange(offset=0)

    assert change.object_type == ""
    assert change.property_name == ""
    assert change.before is None
    assert change.after is None


def test_semantic_change_values():
    change = SemanticChange(
        offset=12,
        object_type="Fixture",
        object_identifier="Fixture_001",
        property_name="color",
        before=(255, 255, 255),
        after=(255, 0, 0),
    )

    assert change.object_type == "Fixture"
    assert change.object_identifier == "Fixture_001"
    assert change.property_name == "color"
    assert change.after == (255, 0, 0)


# ---------------------------------------------------------------------------
# DiffStatistics
# ---------------------------------------------------------------------------


def test_statistics_empty():
    stats = DiffStatistics()

    assert stats.total_changes == 0


def test_statistics_total():
    stats = DiffStatistics(
        binary_changes=2,
        region_changes=3,
        structure_changes=4,
        semantic_changes=5,
    )

    assert stats.total_changes == 14


# ---------------------------------------------------------------------------
# DiffMetadata
# ---------------------------------------------------------------------------


def test_metadata_creation():
    metadata = DiffMetadata(
        project_before="before.c2p",
        project_after="after.c2p",
    )

    assert metadata.project_before == "before.c2p"
    assert metadata.project_after == "after.c2p"
    assert isinstance(metadata.created, datetime)


# ---------------------------------------------------------------------------
# DiffReport
# ---------------------------------------------------------------------------


def test_empty_report():
    metadata = DiffMetadata(
        project_before="A",
        project_after="B",
    )

    stats = DiffStatistics()

    report = DiffReport(
        metadata=metadata,
        statistics=stats,
    )

    assert report.is_empty()


def test_non_empty_report():
    metadata = DiffMetadata(
        project_before="A",
        project_after="B",
    )

    stats = DiffStatistics(binary_changes=1)

    report = DiffReport(
        metadata=metadata,
        statistics=stats,
    )

    assert not report.is_empty()


def test_report_summary():
    metadata = DiffMetadata(
        project_before="A",
        project_after="B",
    )

    stats = DiffStatistics(
        binary_changes=1,
        region_changes=2,
        structure_changes=3,
        semantic_changes=4,
    )

    report = DiffReport(
        metadata=metadata,
        statistics=stats,
    )

    assert (
        report.summary()
        == "1 binary changes, 2 region changes, "
        "3 structure changes, 4 semantic changes"
    )


def test_report_to_dict():
    metadata = DiffMetadata(
        project_before="before",
        project_after="after",
    )

    stats = DiffStatistics()

    report = DiffReport(
        metadata=metadata,
        statistics=stats,
    )

    data = report.to_dict()

    assert isinstance(data, dict)
    assert "metadata" in data
    assert "statistics" in data
    assert "binary_changes" in data
    assert "region_changes" in data
    assert "structure_changes" in data
    assert "semantic_changes" in data


# ---------------------------------------------------------------------------
# Immutability
# ---------------------------------------------------------------------------


def test_models_are_hashable():
    metadata = DiffMetadata(
        project_before="A",
        project_after="B",
    )

    stats = DiffStatistics()

    report = DiffReport(
        metadata=metadata,
        statistics=stats,
    )

    assert hash(report)


def test_binary_change_hashable():
    change = BinaryChange(offset=0)

    assert hash(change)