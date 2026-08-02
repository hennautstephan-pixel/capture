import pytest

from capture_recovery.reconstruction import (
    HeaderScanner,
    HeaderSignature,
)


def test_empty_scanner():

    scanner = HeaderScanner()

    assert len(scanner) == 0


def test_register_signature():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="TEST",
            pattern=b"\xAA\xBB",
        )
    )

    assert len(scanner) == 1


def test_duplicate_registration():

    scanner = HeaderScanner()

    signature = HeaderSignature(
        name="TEST",
        pattern=b"\xAA\xBB",
    )

    scanner.register(signature)
    scanner.register(signature)

    assert len(scanner) == 1


def test_scan_single_signature():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="HDR",
            pattern=b"\xAA\xBB\xCC",
        )
    )

    data = b"\x00\x11\xAA\xBB\xCC\x44"

    results = scanner.scan(data)

    assert len(results) == 1
    assert results[0].offset == 2
    assert results[0].signature.name == "HDR"


def test_scan_multiple_occurrences():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="HDR",
            pattern=b"\xAA",
        )
    )

    results = scanner.scan(
        b"\xAA\x00\xAA\x00\xAA"
    )

    assert len(results) == 3
    assert [r.offset for r in results] == [0, 2, 4]


def test_first():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="HDR",
            pattern=b"\x55",
        )
    )

    result = scanner.first(
        b"\x00\x55\x55"
    )

    assert result is not None
    assert result.offset == 1


def test_nearest():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="HDR",
            pattern=b"\xAA",
        )
    )

    result = scanner.nearest(
        b"\xAA\x00\x00\xAA",
        offset=3,
    )

    assert result is not None
    assert result.offset == 3


def test_between():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="HDR",
            pattern=b"\xAA",
        )
    )

    results = scanner.between(
        b"\xAA\x00\xAA\x00\xAA",
        1,
        3,
    )

    assert len(results) == 1
    assert results[0].offset == 2


def test_has_header():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="HDR",
            pattern=b"\xAA",
        )
    )

    assert scanner.has_header(b"\x00\xAA")
    assert not scanner.has_header(b"\x00\x11")


def test_count():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="HDR",
            pattern=b"\xAA",
        )
    )

    assert scanner.count(
        b"\xAA\xAA\x00\xAA"
    ) == 3