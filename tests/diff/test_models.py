from __future__ import annotations

from datetime import datetime

from capture_recovery.diff.models import (
    BinaryChange,
    ChangeType,
    DiffMetadata,
    DiffReport,
    DiffStatistics,
    FieldChange,
    RegionChange,
    SemanticChange,
    StructureChange,
)
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field


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
    assert change.confidence == 1.0


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
# FieldChange
# ---------------------------------------------------------------------------


def test_field_change_defaults():
    change = FieldChange(offset=0)

    assert change.offset == 0
    assert change.field_before is None
    assert change.field_after is None
    assert change.changed_properties == ()
    assert change.confidence == 1.0


def test_field_change_properties():
    before = Field(
        name="Intensity",
        offset=0,
        length=4,
        datatype=DataType.FLOAT32,
        value=100.0,
    )

    after = Field(
        name="Intensity",
        offset=0,
        length=4,
        datatype=DataType.FLOAT32,
        value=75.0,
    )

    change = FieldChange(
        offset=0,
        field_before=before,
        field_after=after,
        changed_properties=("value",),
        confidence=0.95,
    )

    assert change.field_before is before
    assert change.field_after is after
    assert change.changed_properties == ("value",)
    assert change.confidence == 0.95


def test_field_change_multiple_properties():
    before = Field(
        name="Color",
        offset=12,
        length=4,
        datatype=DataType.UINT32,
    )

    after = Field(
        name="Colour",
        offset=12,
        length=8,
        datatype=DataType.UINT64,
    )

    change = FieldChange(
        offset=12,
        field_before=before,
        field_after=after,
        changed_properties=(
            "name",
            "datatype",
            "length",
        ),
    )

    assert len(change.changed_properties) == 3
    assert "name" in change.changed_properties
    assert "datatype" in change.changed_properties
    assert "length" in change.changed_properties

# ---------------------------------------------------------------------------
# StructureChange
# ---------------------------------------------------------------------------


def test_structure_change_defaults():
    change = StructureChange(offset=0)

    assert change.offset == 0
    assert change.structure_before is None
    assert change.structure_after is None
    assert change.changed_fields == ()
    assert change.confidence == 1.0


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


def test_structure_change_confidence():
    change = StructureChange(
        offset=64,
        confidence=0.85,
    )

    assert change.confidence == 0.85


# ---------------------------------------------------------------------------
# SemanticChange
# ---------------------------------------------------------------------------


def test_semantic_change_defaults():
    change = SemanticChange(offset=0)

    assert change.offset == 0
    assert change.object_type == ""
    assert change.object_identifier is None
    assert change.property_name == ""
    assert change.before is None
    assert change.after is None
    assert change.confidence == 1.0


def test_semantic_change_values():
    change = SemanticChange(
        offset=12,
        object_type="Fixture",
        object_identifier="Fixture_001",
        property_name="color",
        before=(255, 255, 255),
        after=(255, 0, 0),
        confidence=0.92,
    )

    assert change.object_type == "Fixture"
    assert change.object_identifier == "Fixture_001"
    assert change.property_name == "color"
    assert change.before == (255, 255, 255)
    assert change.after == (255, 0, 0)
    assert change.confidence == 0.92


# ---------------------------------------------------------------------------
# DiffStatistics
# ---------------------------------------------------------------------------


def test_statistics_empty():
    stats = DiffStatistics()

    assert stats.bytes_added == 0
    assert stats.bytes_removed == 0
    assert stats.bytes_modified == 0
    assert stats.binary_changes == 0
    assert stats.region_changes == 0
    assert stats.field_changes == 0
    assert stats.structure_changes == 0
    assert stats.semantic_changes == 0
    assert stats.total_changes == 0


def test_statistics_total():
    stats = DiffStatistics(
        binary_changes=2,
        region_changes=3,
        field_changes=4,
        structure_changes=5,
        semantic_changes=6,
    )

    assert stats.total_changes == 20


def test_statistics_bytes():
    stats = DiffStatistics(
        bytes_added=10,
        bytes_removed=5,
        bytes_modified=7,
    )

    assert stats.bytes_added == 10
    assert stats.bytes_removed == 5
    assert stats.bytes_modified == 7

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


def test_metadata_aliases():
    metadata = DiffMetadata(
        project_before="before.c2p",
        project_after="after.c2p",
    )

    assert metadata.project_name_before == "before.c2p"
    assert metadata.project_name_after == "after.c2p"


# ---------------------------------------------------------------------------
# DiffReport
# ---------------------------------------------------------------------------


def test_empty_report():
    metadata = DiffMetadata(
        project_before="A",
        project_after="B",
    )

    report = DiffReport(
        metadata=metadata,
        statistics=DiffStatistics(),
    )

    assert report.is_empty()
    assert len(report) == 0
    assert not report


def test_non_empty_report():
    metadata = DiffMetadata(
        project_before="A",
        project_after="B",
    )

    report = DiffReport(
        metadata=metadata,
        statistics=DiffStatistics(binary_changes=1),
    )

    assert not report.is_empty()
    assert len(report) == 1
    assert report


def test_report_summary():
    metadata = DiffMetadata(
        project_before="A",
        project_after="B",
    )

    stats = DiffStatistics(
        binary_changes=1,
        region_changes=2,
        field_changes=0,
        structure_changes=3,
        semantic_changes=4,
    )

    report = DiffReport(
        metadata=metadata,
        statistics=stats,
    )

    assert (
        report.summary()
        == "1 binary changes, "
        "2 region changes, "
        "0 field changes, "
        "3 structure changes, "
        "4 semantic changes"
    )


def test_binary_at():
    change = BinaryChange(offset=64)

    report = DiffReport(
        metadata=DiffMetadata(
            project_before="A",
            project_after="B",
        ),
        statistics=DiffStatistics(binary_changes=1),
        binary_changes=(change,),
    )

    assert report.binary_at(64) is change
    assert report.binary_at(100) is None


def test_semantic_of_type():
    fixture = SemanticChange(
        offset=0,
        object_type="Fixture",
    )

    cue = SemanticChange(
        offset=10,
        object_type="Cue",
    )

    report = DiffReport(
        metadata=DiffMetadata(
            project_before="A",
            project_after="B",
        ),
        statistics=DiffStatistics(semantic_changes=2),
        semantic_changes=(fixture, cue),
    )

    result = report.semantic_of_type("Fixture")

    assert result == (fixture,)


def test_filter_confidence():
    low = BinaryChange(
        offset=0,
        confidence=0.20,
    )

    high = BinaryChange(
        offset=1,
        confidence=0.90,
    )

    report = DiffReport(
        metadata=DiffMetadata(
            project_before="A",
            project_after="B",
        ),
        statistics=DiffStatistics(binary_changes=2),
        binary_changes=(low, high),
    )

    filtered = report.filter_confidence(0.5)

    assert filtered.binary_changes == (high,)


def test_iter():
    binary = BinaryChange(offset=0)

    report = DiffReport(
        metadata=DiffMetadata(
            project_before="A",
            project_after="B",
        ),
        statistics=DiffStatistics(binary_changes=1),
        binary_changes=(binary,),
    )

    assert tuple(report) == (binary,)


def test_report_to_dict():
    metadata = DiffMetadata(
        project_before="before",
        project_after="after",
    )

    report = DiffReport(
        metadata=metadata,
        statistics=DiffStatistics(),
    )

    data = report.to_dict()

    assert isinstance(data, dict)

    assert "metadata" in data
    assert "statistics" in data

    assert "binary_changes" in data
    assert "region_changes" in data
    assert "field_changes" in data
    assert "structure_changes" in data
    assert "semantic_changes" in data


# ---------------------------------------------------------------------------
# Immutability / Hashability
# ---------------------------------------------------------------------------


def test_models_are_hashable():
    report = DiffReport(
        metadata=DiffMetadata(
            project_before="A",
            project_after="B",
        ),
        statistics=DiffStatistics(),
    )

    assert hash(report)


def test_binary_change_hashable():
    assert hash(BinaryChange(offset=0))


def test_region_change_hashable():
    assert hash(
        RegionChange(
            offset=0,
            region="Header",
        )
    )


def test_field_change_hashable():
    assert hash(FieldChange(offset=0))


def test_structure_change_hashable():
    assert hash(StructureChange(offset=0))


def test_semantic_change_hashable():
    assert hash(SemanticChange(offset=0))