from __future__ import annotations

from capture_recovery.research import (
    FieldCorrelator,
    CorrelationReport,
    FieldCorrelation,
    KnowledgeBase,
    KnowledgeEntry,
)


def create_entry(
    offset: int,
    length: int,
    *,
    confidence: float = 1.0,
    semantic_name: str | None = None,
):

    return KnowledgeEntry(
        offset=offset,
        length=length,
        type_candidates=("bytes",),
        confidence=confidence,
        evidence=("test",),
        semantic_name=semantic_name,
    )


def test_empty():

    correlator = FieldCorrelator()

    report = correlator.correlate(
        KnowledgeBase()
    )

    assert isinstance(
        report,
        CorrelationReport,
    )

    assert report.correlation_count == 0


def test_single():

    kb = KnowledgeBase()

    kb.add(
        create_entry(
            100,
            4,
        )
    )

    report = (
        FieldCorrelator()
        .correlate(kb)
    )

    assert report.correlation_count == 1

    assert isinstance(
        report.correlations[0],
        FieldCorrelation,
    )


def test_by_offset():

    kb = KnowledgeBase()

    kb.add(
        create_entry(
            300,
            4,
        )
    )

    kb.add(
        create_entry(
            100,
            4,
        )
    )

    report = (
        FieldCorrelator()
        .correlate(kb)
    )

    ordered = report.by_offset()

    assert ordered[0].offset == 100

    assert ordered[1].offset == 300


def test_by_confidence():

    kb = KnowledgeBase()

    kb.add(
        create_entry(
            100,
            4,
            confidence=0.2,
        )
    )

    kb.add(
        create_entry(
            200,
            4,
            confidence=0.9,
        )
    )

    report = (
        FieldCorrelator()
        .correlate(kb)
    )

    ordered = report.by_confidence()

    assert ordered[0].confidence == 0.9


def test_occurrence_count():

    kb = KnowledgeBase()

    kb.add(
        create_entry(
            100,
            4,
        )
    )

    kb.add(
        create_entry(
            100,
            4,
        )
    )

    report = (
        FieldCorrelator()
        .correlate(kb)
    )

    correlation = report.correlations[0]

    assert correlation.occurrence_count == 2

    assert correlation.is_unique is False


def test_end():

    kb = KnowledgeBase()

    kb.add(
        create_entry(
            100,
            8,
        )
    )

    report = (
        FieldCorrelator()
        .correlate(kb)
    )

    correlation = report.correlations[0]

    assert correlation.end == 108


def test_semantic_name():

    kb = KnowledgeBase()

    kb.add(
        create_entry(
            100,
            4,
            semantic_name="FixtureCount",
        )
    )

    report = (
        FieldCorrelator()
        .correlate(kb)
    )

    assert (
        report.correlations[0].semantic_name
        == "FixtureCount"
    )