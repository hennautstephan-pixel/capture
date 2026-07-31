from __future__ import annotations

from capture_recovery.knowledge.knowledge_base import KnowledgeBase
from capture_recovery.knowledge.knowledge_inference_engine import KnowledgeInferenceEngine
from capture_recovery.knowledge.knowledge_query_engine import KnowledgeQueryEngine
from capture_recovery.reverse.semantic_pattern_analyzer import PatternObservation, PatternReport


def _make_base() -> KnowledgeBase:
    base = KnowledgeBase()
    reports = (
        PatternReport(
            observations=(
                PatternObservation(pattern_id="alpha", description="first", value_type="int", offsets=(1,), occurrences=2, confidence=0.9),
                PatternObservation(pattern_id="alpha", description="first", value_type="int", offsets=(1,), occurrences=2, confidence=0.2),
            ),
            statistics={},
        ),
        PatternReport(
            observations=(
                PatternObservation(pattern_id="alpha_beta", description="second", value_type="string", offsets=(2,), occurrences=2, confidence=0.8),
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


def test_infer_returns_empty_report_for_empty_base() -> None:
    engine = KnowledgeInferenceEngine(KnowledgeQueryEngine(KnowledgeBase()))

    report = engine.infer()

    assert report.inferences == ()
    assert report.statistics["inference_count"] == 0


def test_infer_creates_simple_inference_for_single_entry() -> None:
    base = KnowledgeBase()
    base.ingest(
        PatternReport(
            observations=(
                PatternObservation(pattern_id="single", description="one", value_type="int", offsets=(1,), occurrences=2, confidence=0.9),
            ),
            statistics={},
        )
    )
    engine = KnowledgeInferenceEngine(KnowledgeQueryEngine(base))

    report = engine.infer()

    assert len(report.inferences) == 1
    assert report.inferences[0].subject == "single"
    assert any("single" in evidence for evidence in report.inferences[0].evidence)
    assert report.statistics["inference_count"] == 1


def test_infer_creates_multiple_inferences_for_multiple_entries() -> None:
    engine = KnowledgeInferenceEngine(KnowledgeQueryEngine(_make_base()))

    report = engine.infer()

    assert len(report.inferences) >= 3
    assert report.statistics["inference_count"] == len(report.inferences)


def test_infer_is_stable_and_reproducible() -> None:
    engine = KnowledgeInferenceEngine(KnowledgeQueryEngine(_make_base()))

    first = engine.infer()
    second = KnowledgeInferenceEngine(KnowledgeQueryEngine(_make_base())).infer()

    assert first == second


def test_infer_does_not_mutate_the_knowledge_base() -> None:
    base = _make_base()
    before = base.snapshot()
    engine = KnowledgeInferenceEngine(KnowledgeQueryEngine(base))

    engine.infer()

    assert base.snapshot() == before
    assert base.snapshot().statistics == before.statistics
