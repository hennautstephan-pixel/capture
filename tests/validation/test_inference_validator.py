from __future__ import annotations

from capture_recovery.experiments.corpus_experiment_runner import CorpusExperimentReport, ExperimentResult
from capture_recovery.knowledge.knowledge_base import KnowledgeSnapshot
from capture_recovery.knowledge.knowledge_inference_engine import Inference, InferenceReport
from capture_recovery.validation.inference_validator import InferenceValidator, ValidationReport, ValidatedInference


def _snapshot() -> KnowledgeSnapshot:
    return KnowledgeSnapshot(entries=(), statistics={})


def _inference(subject: str, hypothesis: str = "test") -> Inference:
    return Inference(subject=subject, hypothesis=hypothesis, confidence=0.8, evidence=(f"key={subject}",))


def _report(*inferences: Inference) -> InferenceReport:
    return InferenceReport(inferences=inferences, statistics={"inference_count": len(inferences)})


def test_validate_handles_empty_report() -> None:
    validator = InferenceValidator()

    report = validator.validate(CorpusExperimentReport(experiments=(), statistics={}))

    assert report.validated == ()
    assert report.statistics["validated_count"] == 0


def test_validate_handles_single_inference() -> None:
    validator = InferenceValidator()
    report = validator.validate(
        CorpusExperimentReport(
            experiments=(
                ExperimentResult(source="one", snapshot=_snapshot(), inference_report=_report(_inference("alpha"))),
            ),
            statistics={"project_count": 1},
        )
    )

    assert len(report.validated) == 1
    assert report.validated[0].inference.subject == "alpha"
    assert report.validated[0].confirmations == 1
    assert report.validated[0].contradictions == 0
    assert report.validated[0].coverage == 1
    assert report.validated[0].robustness == 1.0


def test_validate_groups_equivalent_inferences_across_experiments() -> None:
    validator = InferenceValidator()
    report = validator.validate(
        CorpusExperimentReport(
            experiments=(
                ExperimentResult(source="one", snapshot=_snapshot(), inference_report=_report(_inference("alpha"))),
                ExperimentResult(source="two", snapshot=_snapshot(), inference_report=_report(_inference("alpha"))),
                ExperimentResult(source="three", snapshot=_snapshot(), inference_report=_report(_inference("beta"))),
            ),
            statistics={"project_count": 3},
        )
    )

    validated = report.validated
    assert [entry.inference.subject for entry in validated] == ["alpha", "beta"]
    assert validated[0].confirmations == 2
    assert validated[0].contradictions == 0
    assert validated[0].coverage == 2
    assert validated[1].confirmations == 1
    assert validated[1].contradictions == 0
    assert validated[1].coverage == 1


def test_validate_calculates_robustness_and_is_stable() -> None:
    validator = InferenceValidator()
    first = validator.validate(
        CorpusExperimentReport(
            experiments=(
                ExperimentResult(source="one", snapshot=_snapshot(), inference_report=_report(_inference("alpha"))),
                ExperimentResult(source="two", snapshot=_snapshot(), inference_report=_report(_inference("alpha"))),
            ),
            statistics={"project_count": 2},
        )
    )
    second = validator.validate(
        CorpusExperimentReport(
            experiments=(
                ExperimentResult(source="one", snapshot=_snapshot(), inference_report=_report(_inference("alpha"))),
                ExperimentResult(source="two", snapshot=_snapshot(), inference_report=_report(_inference("alpha"))),
            ),
            statistics={"project_count": 2},
        )
    )

    assert first == second
    assert first.validated[0].robustness == 1.0


def test_validate_does_not_mutate_input_report() -> None:
    report = CorpusExperimentReport(
        experiments=(
            ExperimentResult(source="one", snapshot=_snapshot(), inference_report=_report(_inference("alpha"))),
        ),
        statistics={"project_count": 1},
    )
    validator = InferenceValidator()

    before = report
    validator.validate(report)

    assert report == before
