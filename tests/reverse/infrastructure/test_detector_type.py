"""
Tests for capture_recovery.reverse.detector_type.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.detector_type import (
    DetectorType,
)


# ----------------------------------------------------------------------
# Values
# ----------------------------------------------------------------------


def test_numeric_value() -> None:

    assert DetectorType.NUMERIC.value == "numeric"


def test_string_value() -> None:

    assert DetectorType.STRING.value == "string"


def test_guid_value() -> None:

    assert DetectorType.GUID.value == "guid"


def test_pattern_value() -> None:

    assert DetectorType.PATTERN.value == "pattern"


def test_entropy_value() -> None:

    assert DetectorType.ENTROPY.value == "entropy"


def test_structure_value() -> None:

    assert DetectorType.STRUCTURE.value == "structure"


# ----------------------------------------------------------------------
# String conversion
# ----------------------------------------------------------------------


def test_string_conversion() -> None:

    assert str(DetectorType.NUMERIC) == "numeric"


def test_string_detector_conversion() -> None:

    assert str(DetectorType.STRING) == "string"


# ----------------------------------------------------------------------
# Binary detectors
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "detector",
    [
        DetectorType.NUMERIC,
        DetectorType.GUID,
        DetectorType.PATTERN,
        DetectorType.STRUCTURE,
    ],
)
def test_binary_detectors(
    detector: DetectorType,
) -> None:

    assert detector.is_binary_detector is True


@pytest.mark.parametrize(
    "detector",
    [
        DetectorType.STRING,
        DetectorType.ENTROPY,
    ],
)
def test_non_binary_detectors(
    detector: DetectorType,
) -> None:

    assert detector.is_binary_detector is False


# ----------------------------------------------------------------------
# Text detectors
# ----------------------------------------------------------------------


def test_string_is_text_detector() -> None:

    assert DetectorType.STRING.is_text_detector is True


@pytest.mark.parametrize(
    "detector",
    [
        DetectorType.NUMERIC,
        DetectorType.GUID,
        DetectorType.PATTERN,
        DetectorType.ENTROPY,
    ],
)
def test_non_string_detectors(
    detector: DetectorType,
) -> None:

    assert detector.is_text_detector is False


# ----------------------------------------------------------------------
# Analysis detectors
# ----------------------------------------------------------------------


def test_entropy_is_analysis_detector() -> None:

    assert DetectorType.ENTROPY.is_analysis_detector is True


@pytest.mark.parametrize(
    "detector",
    [
        DetectorType.NUMERIC,
        DetectorType.STRING,
        DetectorType.GUID,
        DetectorType.PATTERN,
        DetectorType.STRUCTURE,
    ],
)
def test_non_analysis_detectors(
    detector: DetectorType,
) -> None:

    assert detector.is_analysis_detector is False


# ----------------------------------------------------------------------
# Enum behaviour
# ----------------------------------------------------------------------


def test_enum_length() -> None:

    assert len(DetectorType) == 6


def test_enum_values_unique() -> None:

    values = [
        detector.value
        for detector in DetectorType
    ]

    assert len(values) == len(set(values))


def test_lookup_numeric() -> None:

    assert (
        DetectorType("numeric")
        is DetectorType.NUMERIC
    )


def test_invalid_lookup() -> None:

    with pytest.raises(ValueError):
        DetectorType("unknown")


def test_members() -> None:

    assert "NUMERIC" in DetectorType.__members__
    assert "STRING" in DetectorType.__members__