from __future__ import annotations

from capture_recovery.knowledge.knowledge_base import KnowledgeBase
from capture_recovery.knowledge.knowledge_query_engine import KnowledgeQueryEngine
from capture_recovery.reverse.semantic_pattern_analyzer import PatternObservation, PatternReport


def _make_base() -> KnowledgeBase:
    base = KnowledgeBase()
    reports = (
        PatternReport(
            observations=(
                PatternObservation(pattern_id="alpha", description="first", value_type="int", offsets=(1,), occurrences=1, confidence=0.9),
                PatternObservation(pattern_id="alpha", description="first", value_type="int", offsets=(1,), occurrences=1, confidence=0.2),
            ),
            statistics={},
        ),
        PatternReport(
            observations=(
                PatternObservation(pattern_id="alpha_beta", description="second", value_type="string", offsets=(2,), occurrences=2, confidence=0.4),
            ),
            statistics={},
        ),
        PatternReport(
            observations=(
                PatternObservation(pattern_id="gamma", description="third", value_type="float", offsets=(3,), occurrences=1, confidence=0.6),
            ),
            statistics={},
        ),
    )
    for report in reports:
        base.ingest(report)
    return base


def test_engine_handles_empty_base() -> None:
    engine = KnowledgeQueryEngine(KnowledgeBase())

    result = engine.statistics()

    assert result["entry_count"] == 0
    assert result["total_observations"] == 0
    assert result["average_confidence"] == 0.0


def test_by_key_returns_exact_match() -> None:
    engine = KnowledgeQueryEngine(_make_base())

    result = engine.by_key("alpha")

    assert result.query == "alpha"
    assert [entry.key for entry in result.matches] == ["alpha"]
    assert result.statistics["match_count"] == 1


def test_by_key_returns_empty_for_missing_key() -> None:
    engine = KnowledgeQueryEngine(_make_base())

    result = engine.by_key("missing")

    assert result.query == "missing"
    assert result.matches == ()
    assert result.statistics["match_count"] == 0


def test_by_prefix_returns_matching_entries_in_stable_order() -> None:
    engine = KnowledgeQueryEngine(_make_base())

    result = engine.by_prefix("alpha")

    assert [entry.key for entry in result.matches] == ["alpha", "alpha_beta"]
    assert result.statistics["match_count"] == 2


def test_by_confidence_filters_by_minimum_threshold() -> None:
    engine = KnowledgeQueryEngine(_make_base())

    result = engine.by_confidence(0.6)

    assert [entry.key for entry in result.matches] == ["gamma"]
    assert result.statistics["match_count"] == 1


def test_top_returns_limited_results_sorted_by_observations() -> None:
    engine = KnowledgeQueryEngine(_make_base())

    result = engine.top(2)

    assert [entry.key for entry in result.matches] == ["alpha", "alpha_beta"]
    assert result.statistics["returned_count"] == 2


def test_statistics_returns_snapshot_summary() -> None:
    engine = KnowledgeQueryEngine(_make_base())

    stats = engine.statistics()

    assert stats["entry_count"] == 3
    assert stats["total_observations"] == 4
    assert stats["average_confidence"] == 0.5166666666666667


def test_queries_are_stable_and_read_only() -> None:
    base = _make_base()
    engine = KnowledgeQueryEngine(base)
    before = base.snapshot()

    first = engine.by_key("alpha")
    second = engine.by_key("alpha")
    third = engine.top(2)

    assert first.matches == second.matches
    assert third.matches == engine.top(2).matches
    assert base.snapshot() == before
    assert base.snapshot().statistics == before.statistics
