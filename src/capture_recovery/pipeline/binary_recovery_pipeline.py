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



class BinaryRecoveryPipeline:
    """
    Recover information from
    binary Capture files.
    """



    def __init__(
        self,
        reader=None,
        analyzer=None,
        reverse_engine=None,
    ) -> None:


        self.reader = (

            reader

            or CaptureBinaryReader()

        )


        self.analyzer = (

            analyzer

            or BinaryAnalyzer()

        )


        self.reverse_engine = (

            reverse_engine

            or ReverseEngine()

        )



    def read(
        self,
        path,
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
    ) -> dict:
        """
        Analyze binary data.
        """

        summary = self.analyzer.summary(
            data,
        )


        analysis = {

            "size":
                summary["size"],


            "signature":
                data[:16],


            "count":
                summary["count"],


            "detections":
                summary["detections"],


            "detection_index":
                summary,

        }



        #
        # Reverse analysis
        #
        # Kept here for backward compatibility
        # and single execution point.
        #

        analysis["reverse"] = (

            self.reverse_engine.analyze(
                data,
            )

        )


        return analysis



    def run(
        self,
        path,
    ) -> dict:
        """
        Execute binary recovery.
        """


        data = self.read(
            path,
        )


        analysis = self.analyze(
            data,
        )


        return {

            "data":
                data,


            "analysis":
                analysis,

        }