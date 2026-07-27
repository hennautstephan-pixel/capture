from capture_recovery.knowledge.signature import Signature
from capture_recovery.knowledge.signature_registry import SignatureRegistry


def create_signature(name="Fixture"):
    return Signature(
        name=name,
        required=(),
        optional=(),
    )


def test_empty_registry():
    registry = SignatureRegistry()

    assert len(registry) == 0
    assert registry.names == ()


def test_register_signature():
    registry = SignatureRegistry()

    signature = create_signature()

    registry.register(
        "Fixture",
        signature,
    )

    assert len(registry) == 1
    assert "Fixture" in registry


def test_signature_for():
    registry = SignatureRegistry()

    signature = create_signature()

    registry.register(
        "Fixture",
        signature,
    )

    assert registry.signature_for("Fixture") is signature


def test_missing_signature():
    registry = SignatureRegistry()

    try:
        registry.signature_for("Unknown")
    except KeyError:
        assert True
    else:
        assert False


def test_names_sorted():
    registry = SignatureRegistry()

    registry.register(
        "ZObject",
        create_signature("ZObject"),
    )

    registry.register(
        "AObject",
        create_signature("AObject"),
    )

    assert registry.names == (
        "AObject",
        "ZObject",
    )