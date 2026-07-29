from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.binary.binary_container import BinaryContainer
from capture_recovery.binary.binary_section import BinarySection


def test_binary_container_creation() -> None:
    section = BinarySection(
        name="Header",
        offset=0,
        size=128,
    )

    container = BinaryContainer(
        path="project.c2p",
        file_size=4096,
        sections=(section,),
    )

    assert container.path == "project.c2p"
    assert container.file_size == 4096
    assert len(container.sections) == 1
    assert container.sections[0] == section


def test_empty_container() -> None:
    container = BinaryContainer(
        path="empty.c2p",
        file_size=0,
        sections=(),
    )

    assert container.file_size == 0
    assert container.sections == ()


def test_multiple_sections() -> None:
    sections = (
        BinarySection("Header", 0, 64),
        BinarySection("Objects", 64, 1024),
        BinarySection("Strings", 1088, 256),
    )

    container = BinaryContainer(
        path="capture.c2p",
        file_size=1344,
        sections=sections,
    )

    assert len(container.sections) == 3
    assert container.sections[1].name == "Objects"


def test_equality() -> None:
    section = BinarySection("Header", 0, 64)

    c1 = BinaryContainer(
        path="test.c2p",
        file_size=64,
        sections=(section,),
    )

    c2 = BinaryContainer(
        path="test.c2p",
        file_size=64,
        sections=(section,),
    )

    assert c1 == c2


def test_hashable() -> None:
    section = BinarySection("Header", 0, 64)

    container = BinaryContainer(
        path="test.c2p",
        file_size=64,
        sections=(section,),
    )

    mapping = {container: "ok"}

    assert mapping[container] == "ok"


def test_is_frozen() -> None:
    container = BinaryContainer(
        path="test.c2p",
        file_size=10,
        sections=(),
    )

    with pytest.raises(FrozenInstanceError):
        container.path = "other.c2p"  # type: ignore[misc]


def test_slots() -> None:
    container = BinaryContainer(
        path="test.c2p",
        file_size=10,
        sections=(),
    )

    with pytest.raises(AttributeError):
        container.extra = True  # type: ignore[attr-defined]


def test_tuple_is_preserved() -> None:
    section = BinarySection("Header", 0, 32)

    container = BinaryContainer(
        path="demo.c2p",
        file_size=32,
        sections=(section,),
    )

    assert isinstance(container.sections, tuple)


def test_large_file_size() -> None:
    container = BinaryContainer(
        path="huge.c2p",
        file_size=2**32,
        sections=(),
    )

    assert container.file_size == 2**32