"""
Full recovery pipeline.

Coordinates binary analysis,
semantic recovery and project reconstruction.
"""

from __future__ import annotations


from capture_recovery.pipeline.binary_recovery_pipeline import (
    BinaryRecoveryPipeline,
)

from capture_recovery.pipeline.semantic_recovery_pipeline import (
    SemanticRecoveryPipeline,
)


class FullRecoveryPipeline:
    """
    Complete Capture recovery workflow.
    """


    def __init__(
        self,
        binary_pipeline=None,
        semantic_pipeline=None,
        reconstructor=None,
    ) -> None:

        self.binary_pipeline = (

            binary_pipeline

            or BinaryRecoveryPipeline()

        )


        self.semantic_pipeline = (

            semantic_pipeline

            or SemanticRecoveryPipeline()

        )


        self.reconstructor = reconstructor



    def analyze(
        self,
        path,
    ) -> dict:
        """
        Run binary analysis.
        """

        return self.binary_pipeline.run(
            path,
        )



    def recover(
        self,
        path,
    ) -> dict:
        """
        Execute complete recovery.
        """

        binary_result = self.analyze(
            path,
        )


        analysis = binary_result["analysis"]


        semantic_result = (
            self.semantic_pipeline.run(
                analysis,
            )
        )


        project = None


        if self.reconstructor:

            project = self.reconstructor.reconstruct(
                semantic_result["objects"],
            )


        return {

            "binary": binary_result,

            "semantic": semantic_result,

            "project": project,

        }