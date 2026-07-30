"""
Semantic recovery pipeline.

Transforms reverse findings into
semantic recovery objects.
"""

from __future__ import annotations

from capture_recovery.semantic.reverse_adapter import (
    ReverseSemanticAdapter,
)

from .results import (
    SemanticRecoveryResult,
)


class SemanticRecoveryPipeline:
    """
    Convert reverse analysis into
    semantic recovery data.
    """

    def __init__(
        self,
        builders: list | None = None,
        adapter: ReverseSemanticAdapter | None = None,
    ) -> None:

        self.builders: list = (
            builders
            or []
        )

        self.adapter: ReverseSemanticAdapter = (
            adapter
            or ReverseSemanticAdapter()
        )

    def build(
        self,
        detections: list,
    ) -> list:
        """
        Run additional builders.
        """

        objects = []

        for builder in self.builders:

            result = builder.build(
                detections,
            )

            objects.extend(
                result
            )

        return objects

    def run(
        self,
        analysis: dict,
    ) -> dict:
        """
        Execute semantic recovery.
        """

        detections = analysis.get(
            "detections",
            [],
        )

        reverse_result = analysis.get(
            "reverse",
        )

        result = SemanticRecoveryResult(
            detections=list(detections),
            reverse=reverse_result,
        )

        #
        # Reverse analysis
        #

        if reverse_result is not None:

            semantic = self.adapter.analyze(
                reverse_result,
            )

            result.objects.extend(
                semantic.get(
                    "objects",
                    [],
                )
            )

            result.evidence.update(
                semantic.get(
                    "evidence",
                    {},
                )
            )

        #
        # Legacy builders
        #

        result.objects.extend(
            self.build(
                detections,
            )
        )

        #
        # Temporary compatibility layer.
        #

        return {
            "detections": result.detections,
            "reverse": result.reverse,
            "objects": result.objects,
            "evidence": result.evidence,
            "result": result,
        }