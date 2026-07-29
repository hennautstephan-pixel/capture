"""
Semantic recovery pipeline.

Transforms reverse findings into
semantic recovery objects.
"""

from __future__ import annotations


from capture_recovery.semantic.reverse_adapter import (
    ReverseSemanticAdapter,
)



class SemanticRecoveryPipeline:
    """
    Convert reverse analysis into
    semantic recovery data.
    """



    def __init__(
        self,
        builders=None,
        adapter=None,
    ) -> None:


        self.builders = (
            builders
            or []
        )


        self.adapter = (
            adapter
            or ReverseSemanticAdapter()
        )



    def build(
        self,
        detections,
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
        analysis,
    ) -> dict:
        """
        Execute semantic recovery.
        """

        detections = analysis.get(
            "detections",
            [],
        )


        objects = []

        evidence = {}



        #
        # Reverse analysis
        #

        reverse_result = analysis.get(
            "reverse",
        )


        if reverse_result is not None:


            semantic = self.adapter.analyze(
                reverse_result,
            )


            objects.extend(
                semantic.get(
                    "objects",
                    [],
                )
            )


            evidence = semantic.get(
                "evidence",
                {},
            )



        #
        # Legacy builders
        #

        objects.extend(

            self.build(
                detections,
            )

        )



        return {

            "detections":
                detections,


            "reverse":
                reverse_result,


            "objects":
                objects,


            "evidence":
                evidence,

        }