from __future__ import annotations

from capture_recovery.pipeline.results import (
    BinaryAnalysisResult,
    FullRecoveryResult,
    ProjectRecoveryResult,
    SemanticRecoveryResult,
)


def test_binary_analysis_defaults():
    result = BinaryAnalysisResult()

    assert result.data == b""
    assert result.size == 0
    assert result.signature == b""
    assert result.detections == []
    assert result.reverse is None
    assert result.metadata == {}
    assert result.count == 0
    assert len(result) == 0


def test_binary_analysis_add_detection():
    result = BinaryAnalysisResult()

    result.add_detection("fixture")
    result.add_detection("scene")

    assert result.count == 2
    assert len(result) == 2
    assert result.detections == [
        "fixture",
        "scene",
    ]


def test_semantic_result_defaults():
    result = SemanticRecoveryResult()

    assert result.detections == []
    assert result.objects == []
    assert result.reverse is None
    assert result.evidence == {}
    assert result.metadata == {}
    assert result.count == 0
    assert len(result) == 0


def test_semantic_result_add_object():
    result = SemanticRecoveryResult()

    fixture = object()

    result.add_object(fixture)

    assert result.count == 1
    assert len(result) == 1
    assert result.objects == [fixture]


def test_project_result_defaults():
    result = ProjectRecoveryResult()

    assert result.project is None
    assert result.valid is False
    assert result.errors == []
    assert result.metadata == {}
    assert result.success is False


def test_project_result_success():
    result = ProjectRecoveryResult(
        project=object(),
        valid=True,
    )

    assert result.success is True


def test_project_result_failure():
    result = ProjectRecoveryResult(
        project=None,
        valid=True,
    )

    assert result.success is False


def test_full_result_success():
    binary = BinaryAnalysisResult()

    semantic = SemanticRecoveryResult()

    project = ProjectRecoveryResult(
        project=object(),
        valid=True,
    )

    result = FullRecoveryResult(
        binary=binary,
        semantic=semantic,
        project=project,
    )

    assert result.success is True


def test_full_result_failure():
    binary = BinaryAnalysisResult()

    semantic = SemanticRecoveryResult()

    project = ProjectRecoveryResult()

    result = FullRecoveryResult(
        binary=binary,
        semantic=semantic,
        project=project,
    )

    assert result.success is False