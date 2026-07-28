import zlib

from capture_recovery.parser.segment_detector import SegmentDetector


def test_empty_buffer():
    segments = SegmentDetector.detect(b"")

    assert segments == []


def test_zero_buffer():
    segments = SegmentDetector.detect(bytes(128))

    assert len(segments) == 1

    segment = segments[0]

    assert segment.kind == "zero"
    assert segment.offset == 0
    assert segment.length == 128
    assert segment.confidence == 1.0


def test_ascii_buffer():
    data = b"Hello Capture Recovery!"

    segments = SegmentDetector.detect(data)

    assert len(segments) == 1

    segment = segments[0]

    assert segment.kind == "ascii"
    assert segment.offset == 0
    assert segment.length == len(data)
    assert segment.confidence >= 0.95


def test_unknown_buffer():
    data = bytes([1, 2, 3, 4, 5])

    segments = SegmentDetector.detect(data)

    assert len(segments) == 1
    assert segments[0].kind == "unknown"


def test_valid_zlib_buffer():
    raw = b"Capture Recovery " * 20

    compressed = zlib.compress(raw)

    segments = SegmentDetector.detect(compressed)

    kinds = {segment.kind for segment in segments}

    assert "zlib" in kinds


def test_high_entropy_buffer():
    data = bytes(range(256))

    segments = SegmentDetector.detect(data)

    kinds = {segment.kind for segment in segments}

    assert "binary" in kinds


def test_segment_length():
    data = b"ABCDEFG"

    segments = SegmentDetector.detect(data)

    assert segments[0].length == len(data)


def test_segment_offset():
    data = b"ABCDEFG"

    segments = SegmentDetector.detect(data)

    assert segments[0].offset == 0


def test_binary_segment_contains_entropy():
    data = bytes(range(256))

    segments = SegmentDetector.detect(data)

    binary = next(s for s in segments if s.kind == "binary")

    assert "entropy" in binary.metadata
    assert binary.metadata["entropy"] >= 7.5


def test_invalid_zlib_is_not_detected():
    data = b"\x78\x9cTHIS IS NOT A VALID ZLIB STREAM"

    segments = SegmentDetector.detect(data)

    kinds = {segment.kind for segment in segments}

    assert "zlib" not in kinds