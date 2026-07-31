"""
Binary recovery pipeline.

Connects Capture binary files
with binary and reverse analysis.
"""

from __future__ import annotations

from capture_recovery.io import (
    CaptureBinaryReader,
)
from capture_recovery.reverse import (
    ReverseEngine,
)

from .binary_analyzer import (
    BinaryAnalyzer,
)
from .results import (
    BinaryAnalysisResult,
)
from .types import BinaryPipelineDict


class BinaryRecoveryPipeline:
    """
    Recover information from
    binary Capture files.
    """

    def __init__(
        self,
        reader: CaptureBinaryReader | None = None,
        analyzer: BinaryAnalyzer | None = None,
        reverse_engine: ReverseEngine | None = None,
    ) -> None:
        self.reader: CaptureBinaryReader = (
            reader
            or CaptureBinaryReader()
        )

        self.analyzer: BinaryAnalyzer = (
            analyzer
            or BinaryAnalyzer()
        )

        self.reverse_engine: ReverseEngine = (
            reverse_engine
            or ReverseEngine()
        )

    def read(
        self,
        path: str,
    ) -> bytes:
        """
        Read binary Capture file.
        """

        return self.reader.read(
            path,
        )

    def analyze(
        self,
        data: bytes,
    ) -> BinaryAnalysisResult:
        """
        Analyze binary data.
        """

        summary = self.analyzer.summary(
            data,
        )

        analysis = BinaryAnalysisResult(
            data=data,
            size=summary["size"],
            signature=data[:16],
            detections=list(summary["detections"]),
            metadata={
                "detection_index": summary,
            },
        )

        analysis.reverse = self.reverse_engine.analyze(
            data,
        )

        return analysis

    def run(
        self,
        path: str,
    ) -> BinaryPipelineDict:
        """
        Execute binary recovery.
        """

        data = self.read(
            path,
        )

        analysis = self.analyze(
            data,
        )

        #
        # Temporary compatibility layer.
        # Keeps the historical API while the
        # remaining pipelines are migrated.
        #

        return {
            "data": data,
            "analysis": {
                "size": analysis.size,
                "signature": analysis.signature,
                "count": analysis.count,
                "detections": analysis.detections,
                "detection_index": analysis.metadata["detection_index"],
                "reverse": analysis.reverse,
            },
            "result": analysis,
        }