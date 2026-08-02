"""
Tests for capture_recovery.reverse.guid_detector.
"""

from __future__ import annotations


from capture_recovery.reverse.detection_options import (
    DetectionOptions,
)

from capture_recovery.reverse.detector_type import (
    DetectorType,
)

from capture_recovery.reverse.guid_detector import (
    GuidDetector,
)

from capture_recovery.reverse.guid_type import (
    WINDOWS_GUID,
    RFC4122_UUID,
)




WINDOWS_BYTES = bytes.fromhex(
    "78563412"
    "3412"
    "cdab"
    "ef0123456789abcd"
)



# ----------------------------------------------------------------------
# Detection
# ----------------------------------------------------------------------


def test_detect_windows_guid() -> None:

    detector = GuidDetector(
        guid_types=(
            WINDOWS_GUID,
        )
    )


    result = detector.detect(
        WINDOWS_BYTES
    )


    assert len(result) == 1

    assert (
        result[0].value
        ==
        "12345678-1234-abcd-ef01-23456789abcd"
    )



def test_detect_with_offset() -> None:

    data = (
        b"\xff\xff"
        +
        WINDOWS_BYTES
    )


    detector = GuidDetector(
        guid_types=(
            WINDOWS_GUID,
        )
    )


    result = detector.detect(
        data
    )


    assert any(
        item.offset == 2
        for item in result
    )



# ----------------------------------------------------------------------
# RFC UUID
# ----------------------------------------------------------------------


def test_detect_rfc_uuid() -> None:

    data = bytes.fromhex(
        "00112233445566778899aabbccddeeff"
    )


    detector = GuidDetector(
        guid_types=(
            RFC4122_UUID,
        )
    )


    result = detector.detect(
        data
    )


    assert result[0].value == (
        "00112233-4455-6677-8899-aabbccddeeff"
    )



# ----------------------------------------------------------------------
# Filters
# ----------------------------------------------------------------------


def test_disabled_guid_detector() -> None:

    detector = GuidDetector()


    options = DetectionOptions(
        enabled_types={
            DetectorType.STRING,
        }
    )


    result = detector.detect(
        WINDOWS_BYTES,
        options,
    )


    assert result == []



# ----------------------------------------------------------------------
# API
# ----------------------------------------------------------------------


def test_guid_types_property() -> None:

    detector = GuidDetector(
        guid_types=(
            WINDOWS_GUID,
        )
    )


    assert detector.guid_types == (
        WINDOWS_GUID,
    )