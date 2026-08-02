from __future__ import annotations

from capture_recovery.pipeline.results import (
    BinaryAnalysisResult,
    FullRecoveryResult,
    ProjectRecoveryResult,
    SemanticRecoveryResult,
)

from capture_recovery.knowledge import KnowledgeResult


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

def test_binary_analysis_contains_knowledge():

    result = BinaryAnalysisResult()

    assert isinstance(
        result.knowledge,
        KnowledgeResult,
    )

    assert result.known_signature_count == 0
    assert result.unknown_signature_count == 0
    assert result.decoded_object_count == 0
    assert result.coverage == 0.0