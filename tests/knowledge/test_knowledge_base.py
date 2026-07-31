from __future__ import annotations

import sys
from pathlib import Path

from capture_recovery.reverse.semantic_pattern_analyzer import PatternObservation, PatternReport
from capture_recovery.knowledge.knowledge_base import KnowledgeBase, KnowledgeEntry, KnowledgeSnapshot

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_empty_base_snapshot_is_stable() -> None:
    base = KnowledgeBase()

    snapshot = base.snapshot()

    assert snapshot.entries == ()
    assert snapshot.statistics == {"entry_count": 0, "total_observations": 0, "average_confidence": 0.0}


def test_ingest_stores_pattern_report() -> None:
    base = KnowledgeBase()
    report = PatternReport(
        observations=(
            PatternObservation(pattern_id="type_string", description="a", value_type="string", offsets=(10,), occurrences=1, confidence=0.8),
        ),
        statistics={},
    )

    base.ingest(report)

    entry = base.query("type_string")
    assert entry is not None
    assert entry.key == "type_string"
    assert entry.observations == 1
    assert entry.confidence == 0.8
    assert entry.metadata["value_type"] == "string"


def test_ingest_merges_identical_observations() -> None:
    base = KnowledgeBase()
    first_report = PatternReport(
        observations=(
            PatternObservation(pattern_id="type_string", description="a", value_type="string", offsets=(10,), occurrences=1, confidence=0.8),
        ),
        statistics={},
    )
    second_report = PatternReport(
        observations=(
            PatternObservation(pattern_id="type_string", description="a", value_type="string", offsets=(10,), occurrences=2, confidence=0.6),
        ),
        statistics={},
    )

    base.ingest(first_report)
    base.ingest(second_report)

    entry = base.query("type_string")
    assert entry is not None
    assert entry.observations == 2
    assert entry.confidence == 0.7


def test_query_returns_none_for_missing_key() -> None:
    base = KnowledgeBase()

    assert base.query("missing") is None


def test_snapshot_is_stable_and_sorted() -> None:
    base = KnowledgeBase()
    report = PatternReport(
        observations=(
            PatternObservation(pattern_id="zeta", description="z", value_type="int", offsets=(5,), occurrences=1, confidence=0.5),
            PatternObservation(pattern_id="alpha", description="a", value_type="string", offsets=(1,), occurrences=1, confidence=0.3),
        ),
        statistics={},
    )

    base.ingest(report)
    snapshot = base.snapshot()

    assert [entry.key for entry in snapshot.entries] == ["alpha", "zeta"]
    assert snapshot.statistics["entry_count"] == 2
    assert snapshot.statistics["total_observations"] == 2


def test_snapshot_statistics_are_derived_from_entries() -> None:
    base = KnowledgeBase()
    report = PatternReport(
        observations=(
            PatternObservation(pattern_id="one", description="a", value_type="int", offsets=(1,), occurrences=1, confidence=0.2),
            PatternObservation(pattern_id="two", description="b", value_type="string", offsets=(2,), occurrences=1, confidence=0.8),
        ),
        statistics={},
    )

    base.ingest(report)

    snapshot = base.snapshot()

    assert snapshot.statistics["entry_count"] == 2
    assert snapshot.statistics["total_observations"] == 2
    assert snapshot.statistics["average_confidence"] == 0.5
