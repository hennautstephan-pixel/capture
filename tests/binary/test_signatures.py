from __future__ import annotations

from capture_recovery.binary.signatures import (
    BinarySignature,
    SignatureRegistry,
)


def test_registry_contains_defaults() -> None:
    registry = SignatureRegistry()

    assert len(registry) >= 17


def test_identify_zip() -> None:
    registry = SignatureRegistry()

    assert registry.identify(b"PK\x03\x04xxxx") == "ZIP"


def test_identify_png() -> None:
    registry = SignatureRegistry()

    data = b"\x89PNG\r\n\x1a\nrest"

    assert registry.identify(data) == "PNG"


def test_identify_jpeg() -> None:
    registry = SignatureRegistry()

    assert registry.identify(b"\xff\xd8\xff\xe0") == "JPEG"


def test_identify_pdf() -> None:
    registry = SignatureRegistry()

    assert registry.identify(b"%PDF-1.7") == "PDF"


def test_identify_gzip() -> None:
    registry = SignatureRegistry()

    assert registry.identify(b"\x1f\x8b\x08") == "GZIP"


def test_identify_unknown() -> None:
    registry = SignatureRegistry()

    assert registry.identify(b"abcdef") is None


def test_match_returns_signature() -> None:
    registry = SignatureRegistry()

    sig = registry.match(b"PK\x03\x04abcd")

    assert sig is not None
    assert sig.name == "ZIP"
    assert sig.pattern == b"PK\x03\x04"


def test_match_returns_none() -> None:
    registry = SignatureRegistry()

    assert registry.match(b"abcd") is None


def test_matches_returns_list() -> None:
    registry = SignatureRegistry()

    matches = registry.matches(b"PK\x03\x04abcd")

    assert isinstance(matches, list)
    assert len(matches) == 1
    assert matches[0].name == "ZIP"


def test_register_custom_signature() -> None:
    registry = SignatureRegistry()

    registry.register(
        BinarySignature(
            name="TEST",
            pattern=b"TEST",
        )
    )

    assert registry.identify(b"TEST123") == "TEST"


def test_clear_registry() -> None:
    registry = SignatureRegistry()

    registry.clear()

    assert len(registry) == 0
    assert registry.identify(b"PK\x03\x04") is None


def test_iter_registry() -> None:
    registry = SignatureRegistry()

    names = [signature.name for signature in registry]

    assert "ZIP" in names
    assert "PNG" in names
    assert "PDF" in names


def test_signature_dataclass() -> None:
    signature = BinarySignature(
        name="ABC",
        pattern=b"ABC",
        offset=5,
        description="Example",
    )

    assert signature.name == "ABC"
    assert signature.pattern == b"ABC"
    assert signature.offset == 5
    assert signature.description == "Example"


def test_signature_with_offset() -> None:
    registry = SignatureRegistry()

    registry.clear()

    registry.register(
        BinarySignature(
            name="OFFSET",
            pattern=b"DATA",
            offset=8,
        )
    )

    data = b"12345678DATA"

    assert registry.identify(data) == "OFFSET"


def test_match_short_buffer() -> None:
    registry = SignatureRegistry()

    assert registry.match(b"P") is None


def test_matches_empty_buffer() -> None:
    registry = SignatureRegistry()

    assert registry.matches(b"") == []


def test_register_multiple_custom_signatures() -> None:
    registry = SignatureRegistry()

    registry.clear()

    registry.register(BinarySignature("A", b"A"))
    registry.register(BinarySignature("B", b"B"))
    registry.register(BinarySignature("C", b"C"))

    assert registry.identify(b"A123") == "A"
    assert registry.identify(b"B123") == "B"
    assert registry.identify(b"C123") == "C"


def test_matches_multiple_signatures() -> None:
    registry = SignatureRegistry()

    registry.clear()

    registry.register(BinarySignature("ONE", b"ABC"))
    registry.register(BinarySignature("TWO", b"ABC"))

    matches = registry.matches(b"ABCDEF")

    assert len(matches) == 2
    assert matches[0].name == "ONE"
    assert matches[1].name == "TWO"


def test_registry_len_after_register() -> None:
    registry = SignatureRegistry()

    initial = len(registry)

    registry.register(BinarySignature("X", b"XYZ"))

    assert len(registry) == initial + 1