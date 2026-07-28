"""
Semantic recovery pipeline.

Transforms binary detections into
semantic recovery objects.
"""

from __future__ import annotations


class SemanticRecoveryPipeline:
    """
    Convert detection results into
    semantic objects.
    """


    def __init__(
        self,
        builders=None,
    ) -> None:

        self.builders = (

            builders

            or []

        )


    def build(
        self,
        detections,
    ) -> list:
        """
        Build semantic objects
        from detections.
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


        objects = self.build(
            detections,
        )


        return {

            "detections": detections,

            "objects": objects,

        }