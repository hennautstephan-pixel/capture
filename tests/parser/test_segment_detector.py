from __future__ import annotations

from capture_recovery.parser.segment_detector import SegmentDetector


def test_detect_empty() -> None:
    assert SegmentDetector.detect(b"") == []


def test_detect_zero_buffer() -> None:
    segments = SegmentDetector.detect(bytes(128))

    assert len(segments) == 1
    assert segments[0].kind == "zero"


def test_detect_ascii() -> None:
    segments = SegmentDetector.detect(
        b"The quick brown fox jumps over the lazy dog"
    )

    assert any(s.kind == "ascii" for s in segments)


def test_detect_unknown() -> None:
    data = bytes([1, 2, 3, 4, 5, 6, 7])

    segments = SegmentDetector.detect(data)

    assert len(segments) == 1
    assert segments[0].kind == "unknown"


def test_detect_zip_signature() -> None:
    data = b"PK\x03\x04" + b"\x00" * 64

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "zip" for s in segments)

    zip_segment = next(s for s in segments if s.kind == "zip")

    assert zip_segment.metadata["signature"] == "ZIP"


def test_detect_png_signature() -> None:
    data = (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00" * 32
    )

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "png" for s in segments)


def test_detect_pdf_signature() -> None:
    data = b"%PDF-1.7\n"

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "pdf" for s in segments)


def test_detect_xml_signature() -> None:
    data = b"<?xml version=\"1.0\"?>"

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "xml" for s in segments)


def test_detect_gzip_signature() -> None:
    data = b"\x1f\x8b\x08\x00"

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "gzip" for s in segments)


def test_detect_pe_signature() -> None:
    data = b"MZ" + b"\x00" * 64

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "pe" for s in segments)


def test_detect_binary_entropy() -> None:
    data = bytes(range(256)) * 8

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "binary" for s in segments)


def test_memoryview_input() -> None:
    data = memoryview(b"PK\x03\x04abcd")

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "zip" for s in segments)


def test_bytearray_input() -> None:
    data = bytearray(b"%PDF-1.7")

    segments = SegmentDetector.detect(data)

    assert any(s.kind == "pdf" for s in segments)


def test_signature_metadata() -> None:
    segments = SegmentDetector.detect(b"PK\x03\x04abcd")

    segment = next(s for s in segments if s.kind == "zip")

    assert "signature" in segment.metadata
    assert "description" in segment.metadata


def test_ascii_and_signature_can_coexist() -> None:
    data = b"<?xml version=\"1.0\"?>"

    segments = SegmentDetector.detect(data)

    kinds = {s.kind for s in segments}

    assert "xml" in kinds
    assert "ascii" in kinds