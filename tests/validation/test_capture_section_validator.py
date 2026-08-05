from capture_recovery.validation import (
    CaptureSectionValidator,
)

from capture_recovery.formats.capture.section import (
    CaptureSection,
)


def test_section_validator_accepts_valid_section():

    validator = CaptureSectionValidator()

    section = CaptureSection(
        offset=100,
        size=5,
        raw=b"ABCDE",
    )

    result = validator.validate(
        section,
    )

    assert result.valid is True

    assert result.offset_valid is True

    assert result.size_valid is True

    assert result.content_valid is True

    assert result.issues == ()



def test_section_validator_detects_invalid_offset():

    validator = CaptureSectionValidator()

    section = CaptureSection(
        offset=-1,
        size=4,
        raw=b"TEST",
    )

    result = validator.validate(
        section,
    )

    assert result.valid is False

    assert result.offset_valid is False

    assert (
        "invalid section offset"
        in result.issues
    )



def test_section_validator_detects_size_mismatch():

    validator = CaptureSectionValidator()

    section = CaptureSection(
        offset=0,
        size=10,
        raw=b"DATA",
    )

    result = validator.validate(
        section,
    )

    assert result.valid is False

    assert result.size_valid is False

    assert (
        "section size mismatch"
        in result.issues
    )



def test_section_validator_detects_empty_section():

    validator = CaptureSectionValidator()

    section = CaptureSection(
        offset=0,
        size=0,
        raw=b"",
    )

    result = validator.validate(
        section,
    )

    assert result.valid is True

    assert result.size_valid is True

    assert result.content_valid is True