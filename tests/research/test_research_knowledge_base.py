from __future__ import annotations

from capture_recovery.research import (
    FieldCandidate,
    FieldMap,
    KnowledgeBase,
    KnowledgeBaseBuilder,
    KnowledgeEntry,
)


def create_field(
    offset: int,
    length: int,
    *,
    confidence: float = 1.0,
    name: str | None = None,
):

    return FieldCandidate(
        offset=offset,
        length=length,
        confidence=confidence,
        evidence=("test",),
        type_candidates=("bytes",),
        name=name,
    )


def test_empty():

    builder = KnowledgeBaseBuilder()

    kb = builder.build(
        FieldMap([])
    )

    assert isinstance(
        kb,
        KnowledgeBase,
    )

    assert kb.entry_count == 0


def test_single():

    builder = KnowledgeBaseBuilder()

    kb = builder.build(
        FieldMap(
            [
                create_field(
                    100,
                    4,
                )
            ]
        )
    )

    assert kb.entry_count == 1

    assert isinstance(
        kb.entries[0],
        KnowledgeEntry,
    )


def test_find():

    builder = KnowledgeBaseBuilder()

    kb = builder.build(
        FieldMap(
            [
                create_field(
                    123,
                    8,
                )
            ]
        )
    )

    entry = kb.find(123)

    assert entry is not None

    assert entry.offset == 123


def test_find_missing():

    kb = KnowledgeBase()

    assert kb.find(999) is None


def test_by_offset():

    builder = KnowledgeBaseBuilder()

    kb = builder.build(
        FieldMap(
            [
                create_field(
                    300,
                    4,
                ),
                create_field(
                    100,
                    4,
                ),
            ]
        )
    )

    ordered = kb.by_offset()

    assert ordered[0].offset == 100

    assert ordered[1].offset == 300


def test_highest_confidence():

    builder = KnowledgeBaseBuilder()

    kb = builder.build(
        FieldMap(
            [
                create_field(
                    100,
                    4,
                    confidence=0.4,
                ),
                create_field(
                    200,
                    4,
                    confidence=0.9,
                ),
            ]
        )
    )

    assert (
        kb.highest_confidence().offset
        == 200
    )


def test_find_semantic_name():

    builder = KnowledgeBaseBuilder()

    kb = builder.build(
        FieldMap(
            [
                create_field(
                    100,
                    4,
                    name="FixtureCount",
                )
            ]
        )
    )

    entry = kb.find_name(
        "FixtureCount"
    )

    assert entry is not None

    assert (
        entry.semantic_name
        == "FixtureCount"
    )


def test_find_candidate_type():

    builder = KnowledgeBaseBuilder()

    kb = builder.build(
        FieldMap(
            [
                create_field(
                    100,
                    4,
                )
            ]
        )
    )

    result = kb.find_type(
        "bytes"
    )

    assert len(result) == 1