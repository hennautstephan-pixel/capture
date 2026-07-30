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

        self.binary_pipeline = (
            binary_pipeline
            or BinaryRecoveryPipeline()
        )

        self.semantic_pipeline = (
            semantic_pipeline
            or SemanticRecoveryPipeline()
        )

        self.reconstructor = (
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

        project = None

        if self.reconstructor:

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