from __future__ import annotations

from capture_recovery.formats.capture import (
    CaptureStream,
)


def make_stream() -> CaptureStream:
    return CaptureStream(
        offset=100,
        compressed_size=32,
        raw=b"\x78\x9c" + b"\x00" * 30,
    )


def test_fields():

    stream = make_stream()

    assert stream.offset == 100
    assert stream.compressed_size == 32
    assert len(stream.raw) == 32


def test_len():

    assert len(make_stream()) == 32


def test_end_offset():

    assert make_stream().end_offset == 132


def test_contains():

    stream = make_stream()

    assert stream.contains(100)
    assert stream.contains(120)
    assert stream.contains(131)

    assert not stream.contains(99)
    assert not stream.contains(132)


def test_empty():

    stream = CaptureStream(
        offset=0,
        compressed_size=0,
    )

    assert stream.is_empty


def test_not_empty():

    assert not make_stream().is_empty


def test_hashable():

    assert hash(make_stream())


def test_repr():

    text = repr(make_stream())

    assert "CaptureStream" in text
    assert "offset=100" in text