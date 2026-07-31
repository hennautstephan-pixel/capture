from __future__ import annotations

from typing import Callable, Mapping

from capture_recovery.knowledge.knowledge_base import KnowledgeBase, KnowledgeSnapshot
from capture_recovery.knowledge.knowledge_inference_engine import Inference, InferenceReport, KnowledgeInferenceEngine
from capture_recovery.knowledge.knowledge_pipeline import KnowledgePipeline, KnowledgePipelineResult
from capture_recovery.knowledge.knowledge_query_engine import KnowledgeQueryEngine
from capture_recovery.experiments.corpus_experiment_runner import CorpusExperimentRunner, CorpusExperimentReport, ExperimentResult


class StubPipeline(KnowledgePipeline):
    def __init__(self, results: dict[bytes, KnowledgePipelineResult]) -> None:
        self._results = results
        self.calls: list[bytes] = []

    def build(self, corpus: list[bytes]) -> KnowledgePipelineResult:
        self.calls.extend(corpus)
        if not corpus:
            return KnowledgePipelineResult(snapshot=KnowledgeSnapshot(entries=(), statistics={}), files_processed=0, reports_processed=0, statistics={})
        first = corpus[0]
        return self._results[first]


class StubInferenceEngine(KnowledgeInferenceEngine):
    def __init__(self, report: InferenceReport) -> None:
        self._report = report

    def infer(self) -> InferenceReport:
        return self._report


class StubFactory:
    def __init__(self, reports: dict[str, InferenceReport]) -> None:
        self._reports = reports
        self.calls: list[KnowledgeSnapshot] = []

    def __call__(self, snapshot: KnowledgeSnapshot) -> KnowledgeInferenceEngine:
        self.calls.append(snapshot)
        key = snapshot.entries[0].key if snapshot.entries else ""
        return StubInferenceEngine(self._reports[key])


def _snapshot(key: str) -> KnowledgeSnapshot:
    return KnowledgeSnapshot(
        entries=(
            type("Entry", (), {"key": key, "observations": 1, "confidence": 0.5, "metadata": {}})(),
        ),
        statistics={"entry_count": 1},
    )


def _report(key: str) -> InferenceReport:
    return InferenceReport(
        inferences=(Inference(subject=key, hypothesis="test", confidence=0.5, evidence=(f"key={key}",)),),
        statistics={"inference_count": 1},
    )


def test_run_handles_empty_corpus() -> None:
    pipeline = StubPipeline({})
    runner = CorpusExperimentRunner(pipeline=pipeline, inference_engine_factory=StubFactory({}))

    report = runner.run({})

    assert report.experiments == ()
    assert report.statistics["project_count"] == 0
    assert report.statistics["total_inferences"] == 0
    assert report.statistics["total_knowledge_entries"] == 0


def test_run_processes_single_project() -> None:
    snapshot = _snapshot("alpha")
    pipeline_result = KnowledgePipelineResult(snapshot=snapshot, files_processed=1, reports_processed=1, statistics={"files_processed": 1})
    pipeline = StubPipeline({b"alpha": pipeline_result})
    factory = StubFactory({"alpha": _report("alpha")})
    runner = CorpusExperimentRunner(pipeline=pipeline, inference_engine_factory=factory)

    report = runner.run({"alpha": b"alpha"})

    assert len(report.experiments) == 1
    assert report.experiments[0].source == "alpha"
    assert report.experiments[0].snapshot == snapshot
    assert report.experiments[0].inference_report == _report("alpha")
    assert report.statistics["project_count"] == 1
    assert report.statistics["total_inferences"] == 1
    assert report.statistics["total_knowledge_entries"] == 1


def test_run_processes_multiple_projects_in_stable_order() -> None:
    first_snapshot = _snapshot("alpha")
    second_snapshot = _snapshot("beta")
    first_result = KnowledgePipelineResult(snapshot=first_snapshot, files_processed=1, reports_processed=1, statistics={})
    second_result = KnowledgePipelineResult(snapshot=second_snapshot, files_processed=1, reports_processed=1, statistics={})
    pipeline = StubPipeline({b"alpha": first_result, b"beta": second_result})
    factory = StubFactory({"alpha": _report("alpha"), "beta": _report("beta")})
    runner = CorpusExperimentRunner(pipeline=pipeline, inference_engine_factory=factory)

    report = runner.run({"alpha": b"alpha", "beta": b"beta"})

    assert [experiment.source for experiment in report.experiments] == ["alpha", "beta"]
    assert [factory.calls[i].entries[0].key for i in range(len(factory.calls))] == ["alpha", "beta"]
    assert report.statistics["project_count"] == 2
    assert report.statistics["total_inferences"] == 2
    assert report.statistics["total_knowledge_entries"] == 2


def test_run_does_not_mutate_dependencies() -> None:
    snapshot = _snapshot("alpha")
    pipeline_result = KnowledgePipelineResult(snapshot=snapshot, files_processed=1, reports_processed=1, statistics={})
    pipeline = StubPipeline({b"alpha": pipeline_result})
    factory = StubFactory({"alpha": _report("alpha")})
    runner = CorpusExperimentRunner(pipeline=pipeline, inference_engine_factory=factory)

    before_pipeline = pipeline.calls.copy()
    before_factory_calls = factory.calls.copy()

    runner.run({"alpha": b"alpha"})

    assert pipeline.calls == before_pipeline + [b"alpha"]
    assert factory.calls == before_factory_calls + [snapshot]
