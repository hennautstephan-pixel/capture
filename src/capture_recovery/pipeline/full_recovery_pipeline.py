"""
Full recovery pipeline.

Coordinates:

Capture binary analysis
        |
        v
Reverse analysis
        |
        v
Semantic recovery
        |
        v
Project reconstruction
"""

from __future__ import annotations

from time import perf_counter

from capture_recovery.analysis import AnalysisResult

from capture_recovery.pipeline.binary_recovery_pipeline import (
    BinaryRecoveryPipeline,
)

from capture_recovery.pipeline.semantic_recovery_pipeline import (
    SemanticRecoveryPipeline,
)

from capture_recovery.reconstruction.project_reconstructor import (
    ProjectReconstructor,
)

from .results import (
    FullRecoveryResult,
)

from .types import (
    BinaryPipelineDict,
    FullPipelineDict,
)


class FullRecoveryPipeline:
    """
    Complete Capture recovery workflow.
    """

    def __init__(
        self,
        binary_pipeline: BinaryRecoveryPipeline | None = None,
        semantic_pipeline: SemanticRecoveryPipeline | None = None,
        reconstructor: ProjectReconstructor | None = None,
    ) -> None:

        self.binary_pipeline: BinaryRecoveryPipeline = (
            binary_pipeline
            or BinaryRecoveryPipeline()
        )

        self.semantic_pipeline: SemanticRecoveryPipeline = (
            semantic_pipeline
            or SemanticRecoveryPipeline()
        )

        self.reconstructor: ProjectReconstructor = (
            reconstructor
            or ProjectReconstructor()
        )

    def analyze(
        self,
        path: str,
    ) -> BinaryPipelineDict:
        """
        Execute binary analysis.
        """

        return self.binary_pipeline.run(
            path,
        )

    def recover(
        self,
        path: str,
    ) -> FullPipelineDict:
        """
        Execute complete recovery.
        """

        binary_result = self.analyze(
            path,
        )

        analysis = binary_result.get(
            "analysis",
            {},
        )

        semantic_result = self.semantic_pipeline.run(
            analysis,
        )

        project = self.reconstructor.reconstruct(
            semantic_result.get(
                "objects",
                [],
            ),
        )

        result = FullRecoveryResult()

        if "result" in binary_result:
            result.binary = binary_result["result"]

        if "result" in semantic_result:
            result.semantic = semantic_result["result"]

        result.project.project = project
        result.project.valid = project is not None

        #
        # Temporary compatibility layer.
        #

        return {
            "binary": binary_result,
            "semantic": semantic_result,
            "project": project,
            "result": result,
        }

    def analyse(
        self,
        path: str,
    ) -> AnalysisResult:
        """
        Analyse a Capture project and return a normalized AnalysisResult.
        """

        #
        # Measure the complete pipeline.
        #

        start = perf_counter()

        recovered = self.recover(path)

        duration_seconds = perf_counter() - start

        binary = recovered.get("binary", {})
        semantic = recovered.get("semantic", {})
        result = recovered.get("result")

        file_size = 0

        data = binary.get("data")

        if isinstance(
            data,
            (
                bytes,
                bytearray,
            ),
        ):
            file_size = len(data)

        object_count = 0

        objects = semantic.get(
            "objects",
        )

        if isinstance(
            objects,
            list,
        ):
            object_count = len(objects)

        property_count = 0
        candidate_count = 0

        average_confidence = 0.0
        minimum_confidence = 0.0
        maximum_confidence = 0.0

        unknown_objects = 0
        unknown_signatures = 0

        conflict_count = 0

        if result is not None:

            binary_result = getattr(
                result,
                "binary",
                None,
            )

            semantic_result = getattr(
                result,
                "semantic",
                None,
            )

            if binary_result is not None:

                unknown_signatures = getattr(
                    binary_result,
                    "unknown_signature_count",
                    0,
                )

            if semantic_result is not None:

                property_count = getattr(
                    semantic_result,
                    "property_count",
                    0,
                )

                candidate_count = getattr(
                    semantic_result,
                    "candidate_count",
                    0,
                )

                average_confidence = getattr(
                    semantic_result,
                    "average_confidence",
                    0.0,
                )

                minimum_confidence = getattr(
                    semantic_result,
                    "minimum_confidence",
                    0.0,
                )

                maximum_confidence = getattr(
                    semantic_result,
                    "maximum_confidence",
                    0.0,
                )

                conflict_count = getattr(
                    semantic_result,
                    "conflict_count",
                    0,
                )

        return AnalysisResult(
            filename=str(path),
            file_size=file_size,
            object_count=object_count,
            property_count=property_count,
            candidate_count=candidate_count,
            average_confidence=average_confidence,
            minimum_confidence=minimum_confidence,
            maximum_confidence=maximum_confidence,
            unknown_objects=unknown_objects,
            unknown_signatures=unknown_signatures,
            conflict_count=conflict_count,
            duration_seconds=duration_seconds,
        )