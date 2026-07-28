import zlib

from capture_recovery.parser.binary_inspector import BinaryInspector
from capture_recovery.parser.segment import Segment


def test_empty_buffer():
    segments = BinaryInspector.inspect(b"")

    assert segments == []


def test_returns_segment_instances():
    segments = BinaryInspector.inspect(b"Hello")

    assert len(segments) == 1
    assert isinstance(segments[0], Segment)


def test_ascii_buffer():
    segments = BinaryInspector.inspect(b"Hello Capture!")

    assert len(segments) == 1
    assert segments[0].kind == "ascii"


def test_zero_buffer():
    segments = BinaryInspector.inspect(bytes(64))

    assert len(segments) == 1
    assert segments[0].kind == "zero"


def test_unknown_buffer():
    segments = BinaryInspector.inspect(bytes([1, 2, 3, 4, 5]))

    assert len(segments) == 1
    assert segments[0].kind == "unknown"


def test_zlib_buffer():
    compressed = zlib.compress(b"Capture Recovery " * 20)

    segments = BinaryInspector.inspect(compressed)

    kinds = {segment.kind for segment in segments}

    assert "zlib" in kinds


def test_binary_buffer():
    data = bytes(range(256))

    segments = BinaryInspector.inspect(data)

    kinds = {segment.kind for segment in segments}

    assert "binary" in kinds


def test_segments_are_sorted():
    segments = BinaryInspector.inspect(b"Hello")

    assert segments == sorted(
        segments,
        key=lambda s: (s.offset, s.length, s.kind),
    )


def test_offsets_are_non_negative():
    segments = BinaryInspector.inspect(b"Hello")

    assert all(segment.offset >= 0 for segment in segments)


def test_lengths_are_positive():
    segments = BinaryInspector.inspect(b"Hello")

    assert all(segment.length > 0 for segment in segments)