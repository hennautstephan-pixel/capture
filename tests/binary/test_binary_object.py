from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.binary.binary_object import BinaryObject


def test_binary_object_creation() -> None:
    obj = BinaryObject(
        identifier=42,
        offset=128,
        size=64,
        raw_data=b"\x01\x02\x03\x04",
    )

    assert obj.identifier == 42
    assert obj.offset == 128
    assert obj.size == 64
    assert obj.raw_data == b"\x01\x02\x03\x04"
    assert obj.type_hint is None
    assert obj.name is None


def test_end_offset_property() -> None:
    obj = BinaryObject(
        identifier=1,
        offset=100,
        size=25,
        raw_data=b"x" * 25,
    )

    assert obj.end_offset == 125


def test_end_offset_zero_size() -> None:
    obj = BinaryObject(
        identifier=2,
        offset=500,
        size=0,
        raw_data=b"",
    )

    assert obj.end_offset == 500


def test_optional_fields() -> None:
    obj = BinaryObject(
        identifier=10,
        offset=0,
        size=4,
        raw_data=b"abcd",
        type_hint=0x22,
        name="Fixture",
    )

    assert obj.type_hint == 0x22
    assert obj.name == "Fixture"


def test_equality() -> None:
    obj1 = BinaryObject(
        identifier=1,
        offset=10,
        size=8,
        raw_data=b"12345678",
    )

    obj2 = BinaryObject(
        identifier=1,
        offset=10,
        size=8,
        raw_data=b"12345678",
    )

    assert obj1 == obj2


def test_hashability() -> None:
    obj = BinaryObject(
        identifier=7,
        offset=50,
        size=5,
        raw_data=b"abcde",
    )

    mapping = {obj: "binary"}

    assert mapping[obj] == "binary"


def test_is_frozen() -> None:
    obj = BinaryObject(
        identifier=1,
        offset=0,
        size=1,
        raw_data=b"\x00",
    )

    with pytest.raises(FrozenInstanceError):
        obj.identifier = 99  # type: ignore[misc]


def test_slots() -> None:
    obj = BinaryObject(
        identifier=1,
        offset=0,
        size=1,
        raw_data=b"\x00",
    )

    with pytest.raises(AttributeError):
        obj.new_attribute = "forbidden"  # type: ignore[attr-defined]


def test_empty_raw_data() -> None:
    obj = BinaryObject(
        identifier=100,
        offset=2048,
        size=0,
        raw_data=b"",
    )

    assert obj.raw_data == b""
    assert obj.end_offset == 2048


def test_large_offset() -> None:
    obj = BinaryObject(
        identifier=999,
        offset=0x100000,
        size=512,
        raw_data=b"\x00" * 512,
    )

    assert obj.end_offset == 0x100200