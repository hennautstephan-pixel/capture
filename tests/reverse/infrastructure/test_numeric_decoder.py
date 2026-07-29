"""
Tests for capture_recovery.reverse.numeric_detector.
"""

from __future__ import annotations

from capture_recovery.reverse.detection_options import (
    DetectionOptions,
)

from capture_recovery.reverse.detection_strategy import (
    DetectionStrategy,
)

from capture_recovery.reverse.detector_type import (
    DetectorType,
)

from capture_recovery.reverse.numeric_detector import (
    NumericDetector,
)

from capture_recovery.reverse.numeric_type import (
    INT16,
    INT32,
)


# ----------------------------------------------------------------------
# Basic detection
# ----------------------------------------------------------------------


def test_detect_int32() -> None:

    detector = NumericDetector(
        numeric_types=(
            INT32,
        )
    )

    data = b"\x78\x56\x34\x12"

    result = detector.detect(
        data,
    )

    assert len(result) == 1

    assert result[0].value == 0x12345678


def test_detect_int16_multiple() -> None:

    detector = NumericDetector(
        numeric_types=(
            INT16,
        )
    )

    data = (
        b"\x01\x00"
        b"\x02\x00"
    )

    result = detector.detect(
        data,
    )

    values = [
        item.value
        for item in result
    ]

    assert values == [
        1,
        2,
    ]


# ----------------------------------------------------------------------
# Strategies
# ----------------------------------------------------------------------


def test_aligned_detection() -> None:

    detector = NumericDetector(
        numeric_types=(
            INT16,
        )
    )

    options = DetectionOptions(
        strategy=DetectionStrategy.ALIGNED,
        alignment=2,
    )

    result = detector.detect(
        b"\x01\x00\x02\x00",
        options,
    )

    assert [
        item.offset
        for item in result
    ] == [
        0,
        2,
    ]


def test_custom_offsets_detection() -> None:

    detector = NumericDetector(
        numeric_types=(
            INT16,
        )
    )

    options = DetectionOptions(
        strategy=DetectionStrategy.CUSTOM,
        offsets=(2,),
    )

    result = detector.detect(
        b"\x00\x00\x05\x00",
        options,
    )

    assert result[0].offset == 2
    assert result[0].value == 5


# ----------------------------------------------------------------------
# Endianness
# ----------------------------------------------------------------------


def test_big_endian_detection() -> None:

    detector = NumericDetector(
        numeric_types=(
            INT32,
        )
    )

    result = detector.detect(
        b"\x12\x34\x56\x78",
        endianness="big",
    )

    assert result[0].value == 0x12345678


# ----------------------------------------------------------------------
# Filtering
# ----------------------------------------------------------------------


def test_disabled_detector_type() -> None:

    detector = NumericDetector()

    options = DetectionOptions(
        enabled_types={
            DetectorType.STRING,
        }
    )

    result = detector.detect(
        b"\x01\x00\x00\x00",
        options,
    )

    assert result == []


# ----------------------------------------------------------------------
# API
# ----------------------------------------------------------------------


def test_numeric_types_property() -> None:

    detector = NumericDetector(
        numeric_types=(
            INT32,
        )
    )

    assert detector.numeric_types == (
        INT32,
    )