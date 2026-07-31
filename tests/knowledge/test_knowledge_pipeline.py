from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.knowledge.knowledge_base import KnowledgeBase, KnowledgeSnapshot
from capture_recovery.knowledge.knowledge_pipeline import KnowledgePipeline, KnowledgePipelineResult
from capture_recovery.reverse.semantic_diff import SemanticDiff, SemanticDiffEngine, ValueDifference
from capture_recovery.reverse.semantic_pattern_analyzer import PatternReport, PatternObservation, SemanticPatternAnalyzer

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class StubInspector:
    def __init__(self, results: dict[bytes, list[RecoveredValue]]) -> None:
        self._results = results
        self.calls: list[bytes] = []

    def inspect(self, data: bytes) -> list[RecoveredValue]:
        self.calls.append(data)
        return list(self._results.get(data, []))


class StubDiffEngine:
    def __init__(self, diffs: dict[bytes, SemanticDiff]) -> None:
        self._diffs = diffs
        self.calls: list[tuple[list[RecoveredValue], list[RecoveredValue]]] = []

    def compare(self, before: list[RecoveredValue], after: list[RecoveredValue]) -> SemanticDiff:
        self.calls.append((list(before), list(after)))
        if after and hasattr(after[0], "source"):
            source = after[0].source
            if isinstance(source, str):
                return self._diffs.get(source.encode("utf-8"), SemanticDiff(added=(), removed=(), modified=(), unchanged=()))
            return self._diffs.get(source, SemanticDiff(added=(), removed=(), modified=(), unchanged=()))
        return SemanticDiff(added=(), removed=(), modified=(), unchanged=())


class StubPatternAnalyzer:
    def __init__(self, reports: dict[SemanticDiff, PatternReport]) -> None:
        self._reports = reports
        self.calls: list[SemanticDiff] = []

    def analyze(self, diffs: list[SemanticDiff]) -> PatternReport:
        self.calls.extend(diffs)
        if not diffs:
            return PatternReport(observations=(), statistics={})
        diff = diffs[0]
        for candidate, report in self._reports.items():
            if candidate == diff:
                return report
        return PatternReport(observations=(), statistics={})


class StubKnowledgeBase(KnowledgeBase):
    def __init__(self) -> None:
        super().__init__()
        self.ingested: list[PatternReport] = []

    def ingest(self, report: PatternReport) -> None:
        self.ingested.append(report)
        super().ingest(report)


def test_build_handles_empty_corpus() -> None:
    pipeline = KnowledgePipeline(
        inspector=StubInspector({}),
        diff_engine=StubDiffEngine({}),
        pattern_analyzer=StubPatternAnalyzer({}),
        knowledge_base=StubKnowledgeBase(),
    )

    result = pipeline.build([])

    assert result.files_processed == 0
    assert result.reports_processed == 0
    assert result.statistics["files_processed"] == 0
    assert result.statistics["semantic_diffs_generated"] == 0
    assert result.statistics["knowledge_entries"] == 0
    assert result.snapshot.entries == ()


def test_build_processes_single_file() -> None:
    diff = SemanticDiff(added=(), removed=(), modified=(), unchanged=())
    report = PatternReport(observations=(PatternObservation(pattern_id="alpha", description="desc", value_type="int", offsets=(1,), occurrences=1, confidence=0.5),), statistics={})
    inspector = StubInspector({b"a": [RecoveredValue(type="int", value=1, offset=1, size=4, source="a")]})
    diff_engine = StubDiffEngine({b"a": diff})
    pattern_analyzer = StubPatternAnalyzer({diff: report})
    knowledge_base = StubKnowledgeBase()
    pipeline = KnowledgePipeline(inspector=inspector, diff_engine=diff_engine, pattern_analyzer=pattern_analyzer, knowledge_base=knowledge_base)

    result = pipeline.build([b"a"])

    assert result.files_processed == 1
    assert result.reports_processed == 1
    assert result.statistics["reports_processed"] == 1
    assert result.snapshot.entries[0].key == "alpha"
    assert len(knowledge_base.ingested) == 1
    assert inspector.calls == [b"a"]
    assert len(pattern_analyzer.calls) == 1


def test_build_processes_multiple_files_and_propagates_reports() -> None:
    first_diff = SemanticDiff(added=(), removed=(), modified=(), unchanged=())
    second_diff = SemanticDiff(added=(), removed=(), modified=(), unchanged=())
    first_report = PatternReport(observations=(PatternObservation(pattern_id="first", description="desc", value_type="int", offsets=(1,), occurrences=1, confidence=0.2),), statistics={})
    second_report = PatternReport(observations=(PatternObservation(pattern_id="second", description="desc", value_type="string", offsets=(2,), occurrences=1, confidence=0.8),), statistics={})
    inspector = StubInspector({b"one": [RecoveredValue(type="int", value=1, offset=1, size=4, source="one")], b"two": [RecoveredValue(type="string", value="x", offset=2, size=4, source="two")]})
    diff_engine = StubDiffEngine({b"one": first_diff, b"two": second_diff})
    pattern_analyzer = StubPatternAnalyzer({first_diff: first_report, second_diff: second_report})
    knowledge_base = StubKnowledgeBase()
    pipeline = KnowledgePipeline(inspector=inspector, diff_engine=diff_engine, pattern_analyzer=pattern_analyzer, knowledge_base=knowledge_base)

    result = pipeline.build([b"one", b"two"])

    assert result.files_processed == 2
    assert result.reports_processed == 2
    assert result.statistics["semantic_diffs_generated"] == 2
    assert result.statistics["knowledge_entries"] == 1
    assert [entry.key for entry in result.snapshot.entries] == ["second"]
    assert [report.observations[0].pattern_id for report in knowledge_base.ingested] == ["second", "second"]


def test_build_generates_stable_snapshot() -> None:
    diff = SemanticDiff(added=(), removed=(), modified=(), unchanged=())
    report = PatternReport(observations=(PatternObservation(pattern_id="stable", description="desc", value_type="int", offsets=(3,), occurrences=1, confidence=0.4),), statistics={})
    inspector = StubInspector({b"x": [RecoveredValue(type="int", value=1, offset=3, size=4, source="x")]})
    diff_engine = StubDiffEngine({b"x": diff})
    pattern_analyzer = StubPatternAnalyzer({diff: report})
    pipeline = KnowledgePipeline(inspector=inspector, diff_engine=diff_engine, pattern_analyzer=pattern_analyzer, knowledge_base=StubKnowledgeBase())

    first = pipeline.build([b"x"])
    second = KnowledgePipeline(inspector=inspector, diff_engine=diff_engine, pattern_analyzer=pattern_analyzer, knowledge_base=StubKnowledgeBase()).build([b"x"])

    assert first.snapshot == second.snapshot
    assert first.statistics == second.statistics
