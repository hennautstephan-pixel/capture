from capture_recovery.knowledge import (
    DecoderRegistry,
    RegistryBuilder,
    build_default_registry,
)


def test_registry_builder():

    builder = RegistryBuilder()

    registry = (
        builder
        .register_builtin()
        .build()
    )

    assert isinstance(
        registry,
        DecoderRegistry,
    )


def test_default_registry():

    registry = build_default_registry()

    assert isinstance(
        registry,
        DecoderRegistry,
    )