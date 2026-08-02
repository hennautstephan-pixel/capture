from capture_recovery.knowledge import (
    KnowledgeEngine,
    create_default_engine,
)


def test_create_default_engine():

    engine = create_default_engine()

    assert isinstance(
        engine,
        KnowledgeEngine,
    )


def test_engine_contains_decoders():

    engine = create_default_engine()

    assert len(
        engine.registry
    ) > 0