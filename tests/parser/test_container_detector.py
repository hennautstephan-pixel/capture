from __future__ import annotations

import zlib

from capture_recovery.parser.container_detector import (
    Container,
    ContainerDetector,
)


def test_empty_buffer() -> None:
    assert ContainerDetector.detect(b"") == []


def test_detect_zip_container() -> None:
    data = b"PK\x03\x04" + b"\x00" * 32

    containers = ContainerDetector.detect(data)

    assert len(containers) == 1

    c = containers[0]

    assert c.kind == "zip"
    assert c.offset == 0
    assert c.length == len(data)
    assert c.confidence == 1.0


def test_detect_gzip_container() -> None:
    data = b"\x1f\x8b\x08\x00" + b"\x00" * 32

    containers = ContainerDetector.detect(data)

    assert len(containers) == 1
    assert containers[0].kind == "gzip"


def test_detect_png_container() -> None:
    data = (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00" * 32
    )

    containers = ContainerDetector.detect(data)

    assert len(containers) == 1
    assert containers[0].kind == "png"


def test_detect_zlib_container() -> None:
    data = zlib.compress(b"Capture Recovery")

    containers = ContainerDetector.detect(data)

    assert len(containers) == 1
    assert containers[0].kind == "zlib"


def test_unknown_buffer_returns_empty() -> None:
    data = b"\x10\x20\x30\x40"

    containers = ContainerDetector.detect(data)

    assert containers == []


def test_container_end_property() -> None:
    container = Container(
        offset=12,
        length=25,
        kind="zip",
    )

    assert container.end == 37


def test_metadata_is_copied() -> None:
    data = b"PK\x03\x04" + b"\x00" * 32

    containers = ContainerDetector.detect(data)

    assert containers

    metadata = containers[0].metadata

    assert isinstance(metadata, dict)


def test_detect_returns_list() -> None:
    result = ContainerDetector.detect(b"")

    assert isinstance(result, list)


def test_offsets_are_positive() -> None:
    data = b"PK\x03\x04" + b"\x00" * 16

    containers = ContainerDetector.detect(data)

    assert all(c.offset >= 0 for c in containers)


def test_lengths_are_positive() -> None:
    data = b"PK\x03\x04" + b"\x00" * 16

    containers = ContainerDetector.detect(data)

    assert all(c.length > 0 for c in containers)


def test_confidence_range() -> None:
    data = b"PK\x03\x04" + b"\x00" * 16

    containers = ContainerDetector.detect(data)

    assert all(0.0 <= c.confidence <= 1.0 for c in containers)