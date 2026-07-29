"""
Tests for capture_recovery.reverse.detection_strategy.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.detection_strategy import (
    DetectionStrategy,
)


# ----------------------------------------------------------------------
# Enum values
# ----------------------------------------------------------------------


def test_scan_value() -> None:

    assert DetectionStrategy.SCAN.value == "scan"


def test_aligned_value() -> None:

    assert DetectionStrategy.ALIGNED.value == "aligned"


def test_custom_value() -> None:

    assert DetectionStrategy.CUSTOM.value == "custom"


# ----------------------------------------------------------------------
# String conversion
# ----------------------------------------------------------------------


def test_scan_string() -> None:

    assert str(DetectionStrategy.SCAN) == "scan"


def test_aligned_string() -> None:

    assert str(DetectionStrategy.ALIGNED) == "aligned"


def test_custom_string() -> None:

    assert str(DetectionStrategy.CUSTOM) == "custom"


# ----------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------


def test_scan_requires_alignment() -> None:

    assert DetectionStrategy.SCAN.requires_alignment is False


def test_aligned_requires_alignment() -> None:

    assert DetectionStrategy.ALIGNED.requires_alignment is True


def test_custom_requires_alignment() -> None:

    assert DetectionStrategy.CUSTOM.requires_alignment is False


def test_scan_requires_custom_offsets() -> None:

    assert DetectionStrategy.SCAN.requires_custom_offsets is False


def test_aligned_requires_custom_offsets() -> None:

    assert DetectionStrategy.ALIGNED.requires_custom_offsets is False


def test_custom_requires_custom_offsets() -> None:

    assert DetectionStrategy.CUSTOM.requires_custom_offsets is True


def test_scan_scans_every_offset() -> None:

    assert DetectionStrategy.SCAN.scans_every_offset is True


def test_aligned_scans_every_offset() -> None:

    assert DetectionStrategy.ALIGNED.scans_every_offset is False


def test_custom_scans_every_offset() -> None:

    assert DetectionStrategy.CUSTOM.scans_every_offset is False


# ----------------------------------------------------------------------
# Enum iteration
# ----------------------------------------------------------------------


def test_iteration_order() -> None:

    assert list(DetectionStrategy) == [
        DetectionStrategy.SCAN,
        DetectionStrategy.ALIGNED,
        DetectionStrategy.CUSTOM,
    ]


def test_enum_length() -> None:

    assert len(DetectionStrategy) == 3


def test_unique_values() -> None:

    values = [member.value for member in DetectionStrategy]

    assert len(values) == len(set(values))


# ----------------------------------------------------------------------
# Lookup
# ----------------------------------------------------------------------


def test_lookup_scan() -> None:

    assert DetectionStrategy("scan") is DetectionStrategy.SCAN


def test_lookup_aligned() -> None:

    assert DetectionStrategy("aligned") is DetectionStrategy.ALIGNED


def test_lookup_custom() -> None:

    assert DetectionStrategy("custom") is DetectionStrategy.CUSTOM


def test_lookup_invalid() -> None:

    with pytest.raises(ValueError):
        DetectionStrategy("invalid")


# ----------------------------------------------------------------------
# Members
# ----------------------------------------------------------------------


def test_members() -> None:

    assert DetectionStrategy.__members__ == {
        "SCAN": DetectionStrategy.SCAN,
        "ALIGNED": DetectionStrategy.ALIGNED,
        "CUSTOM": DetectionStrategy.CUSTOM,
    }


# ----------------------------------------------------------------------
# Equality
# ----------------------------------------------------------------------


def test_equality() -> None:

    assert DetectionStrategy.SCAN == DetectionStrategy.SCAN


def test_inequality() -> None:

    assert DetectionStrategy.SCAN != DetectionStrategy.ALIGNED


def test_identity() -> None:

    strategy = DetectionStrategy.CUSTOM

    assert strategy is DetectionStrategy.CUSTOM


# ----------------------------------------------------------------------
# Hashability
# ----------------------------------------------------------------------


def test_hashable() -> None:

    mapping = {
        DetectionStrategy.SCAN: 1,
        DetectionStrategy.ALIGNED: 2,
        DetectionStrategy.CUSTOM: 3,
    }

    assert mapping[DetectionStrategy.SCAN] == 1
    assert mapping[DetectionStrategy.ALIGNED] == 2
    assert mapping[DetectionStrategy.CUSTOM] == 3


# ----------------------------------------------------------------------
# Names
# ----------------------------------------------------------------------


def test_names() -> None:

    assert [member.name for member in DetectionStrategy] == [
        "SCAN",
        "ALIGNED",
        "CUSTOM",
    ]