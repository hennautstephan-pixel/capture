from __future__ import annotations

from capture_recovery.formats.capture import (
    CaptureStreamRegion,
)


def make_region():

    return CaptureStreamRegion(
        start=10,
        end=50,
        signature=b"\x78\x9C",
    )


def test_fields():

    region = make_region()

    assert region.start == 10
    assert region.end == 50
    assert region.signature == b"\x78\x9C"


def test_size():

    assert make_region().size == 40


def test_len():

    assert len(make_region()) == 40


def test_contains():

    region = make_region()

    assert region.contains(10)
    assert region.contains(25)
    assert region.contains(49)

    assert not region.contains(50)
    assert not region.contains(9)


def test_empty():

    region = CaptureStreamRegion(
        start=0,
        end=0,
        signature=b"",
    )

    assert region.is_empty


def test_hashable():

    assert hash(make_region())


def test_repr():

    text = repr(make_region())

    assert "CaptureStreamRegion" in text