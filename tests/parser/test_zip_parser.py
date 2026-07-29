from __future__ import annotations

from io import BytesIO
from zipfile import ZipFile

import pytest

from capture_recovery.parser.container_extractor import (
    ExtractedContainer,
)
from capture_recovery.parser.zip_parser import (
    ZipEntry,
    ZipParser,
)


def make_zip() -> bytes:

    buffer = BytesIO()

    with ZipFile(buffer, "w") as archive:
        archive.writestr("project.xml", b"<project/>")
        archive.writestr("fixtures.xml", b"<fixtures/>")

    return buffer.getvalue()


def test_parse_zip() -> None:

    container = ExtractedContainer(
        kind="zip",
        data=make_zip(),
    )

    entries = ZipParser.parse(container)

    assert len(entries) == 2


def test_entry_names() -> None:

    container = ExtractedContainer(
        kind="zip",
        data=make_zip(),
    )

    entries = ZipParser.parse(container)

    names = {e.name for e in entries}

    assert "project.xml" in names
    assert "fixtures.xml" in names


def test_entry_contents() -> None:

    container = ExtractedContainer(
        kind="zip",
        data=make_zip(),
    )

    entries = ZipParser.parse(container)

    project = next(
        e
        for e in entries
        if e.name == "project.xml"
    )

    assert project.data == b"<project/>"


def test_sizes_are_positive() -> None:

    container = ExtractedContainer(
        kind="zip",
        data=make_zip(),
    )

    entries = ZipParser.parse(container)

    assert all(e.size > 0 for e in entries)
    assert all(e.compressed_size > 0 for e in entries)


def test_crc_is_integer() -> None:

    container = ExtractedContainer(
        kind="zip",
        data=make_zip(),
    )

    entries = ZipParser.parse(container)

    assert all(isinstance(e.crc, int) for e in entries)


def test_returns_zipentry_objects() -> None:

    container = ExtractedContainer(
        kind="zip",
        data=make_zip(),
    )

    entries = ZipParser.parse(container)

    assert all(isinstance(e, ZipEntry) for e in entries)


def test_non_zip_container() -> None:

    container = ExtractedContainer(
        kind="binary",
        data=b"abcdef",
    )

    with pytest.raises(ValueError):
        ZipParser.parse(container)


def test_empty_zip() -> None:

    buffer = BytesIO()

    with ZipFile(buffer, "w"):
        pass

    container = ExtractedContainer(
        kind="zip",
        data=buffer.getvalue(),
    )

    entries = ZipParser.parse(container)

    assert entries == []