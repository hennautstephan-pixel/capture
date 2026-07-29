"""
Tests for capture_recovery.reverse.string_detector.
"""

from __future__ import annotations


from capture_recovery.reverse.detection_options import (
    DetectionOptions,
)

from capture_recovery.reverse.detector_type import (
    DetectorType,
)

from capture_recovery.reverse.string_detector import (
    StringDetector,
)

from capture_recovery.reverse.string_type import (
    ASCII,
    UTF16_LE,
)



# ----------------------------------------------------------------------
# Basic detection
# ----------------------------------------------------------------------


def test_detect_ascii() -> None:

    detector = StringDetector(
        string_types=(
            ASCII,
        )
    )


    result = detector.detect(
        b"Hello\x00",
    )


    values = [
        item.value
        for item in result
    ]


    assert "Hello" in values



def test_detect_with_offset() -> None:

    detector = StringDetector(
        string_types=(
            ASCII,
        )
    )


    result = detector.detect(
        b"\xff\xffTest\x00",
    )


    assert any(
        item.value == "Test"
        for item in result
    )



# ----------------------------------------------------------------------
# UTF16
# ----------------------------------------------------------------------


def test_detect_utf16_le() -> None:

    detector = StringDetector(
        string_types=(
            UTF16_LE,
        )
    )


    data = (
        "Hello"
        .encode("utf-16-le")
        +
        b"\x00\x00"
    )


    result = detector.detect(
        data,
    )


    assert any(
        item.value == "Hello"
        for item in result
    )



# ----------------------------------------------------------------------
# Filters
# ----------------------------------------------------------------------


def test_min_length_filter() -> None:

    detector = StringDetector(
        string_types=(
            ASCII,
        )
    )


    result = detector.detect(
        b"A\x00AB\x00",
        min_length=3,
    )


    assert all(
        len(item.value) >= 3
        for item in result
    )



def test_disabled_string_detector() -> None:

    detector = StringDetector(
        string_types=(
            ASCII,
        )
    )


    options = DetectionOptions(
        enabled_types={
            DetectorType.NUMERIC,
        }
    )


    result = detector.detect(
        b"Hello\x00",
        options,
    )


    assert result == []



# ----------------------------------------------------------------------
# API
# ----------------------------------------------------------------------


def test_string_types_property() -> None:

    detector = StringDetector(
        string_types=(
            ASCII,
        )
    )


    assert detector.string_types == (
        ASCII,
    )