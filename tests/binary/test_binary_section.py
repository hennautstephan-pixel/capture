from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.binary.binary_section import BinarySection


def test_binary_section_creation() -> None:
    section = BinarySection(
        name="Objects",
        offset=1024,
        size=4096,
    )

    assert section.name == "Objects"
    assert section.offset == 1024
    assert section.size == 4096


def test_empty_name() -> None:
    section = BinarySection(
        name="",
        offset=0,
        size=0,
    )

    assert section.name == ""


def test_zero_size() -> None:
    section = BinarySection(
        name="Empty",
        offset=512,
        size=0,
    )

    assert section.size == 0


def test_equality() -> None:
    s1 = BinarySection(
        name="Header",
        offset=0,
        size=64,
    )

    s2 = BinarySection(
        name="Header",
        offset=0,
        size=64,
    )

    assert s1 == s2


def test_hashable() -> None:
    section = BinarySection(
        name="Metadata",
        offset=128,
        size=256,
    )

    mapping = {section: "ok"}

    assert mapping[section] == "ok"


def test_is_frozen() -> None:
    section = BinarySection(
        name="Header",
        offset=0,
        size=64,
    )

    with pytest.raises(FrozenInstanceError):
        section.name = "Modified"  # type: ignore[misc]


def test_slots() -> None:
    section = BinarySection(
        name="Header",
        offset=0,
        size=64,
    )

    with pytest.raises(AttributeError):
        section.extra = True  # type: ignore[attr-defined]


def test_large_values() -> None:
    section = BinarySection(
        name="Huge",
        offset=0x10000000,
        size=0x20000000,
    )

    assert section.offset == 0x10000000
    assert section.size == 0x20000000