from __future__ import annotations

from typing import TypedDict
from capture_recovery.models.detection import Detection
from capture_recovery.reverse import ReverseResult

from capture_recovery.pipeline.results import (
    BinaryAnalysisResult,
    SemanticRecoveryResult,
    FullRecoveryResult,
)


class BinarySummaryDict(TypedDict):
    size: int
    count: int
    detections: list[Detection][Detection]
    index: list[Detection]


class BinaryAnalysisDict(TypedDict):
    size: int
    signature: bytes
    count: int
    detections: list
    detection_index: BinarySummaryDict
    reverse: ReverseResult


class BinaryPipelineDict(TypedDict):
    data: bytes
    analysis: BinaryAnalysisDict
    result: BinaryAnalysisResult


class SemanticPipelineDict(TypedDict):
    detections: list[Detection]
    reverse: ReverseResult
    objects: list
    evidence: dict
    result: SemanticRecoveryResult


class FullPipelineDict(TypedDict):
    binary: BinaryPipelineDict
    semantic: SemanticPipelineDict
    project: object
    result: FullRecoveryResult