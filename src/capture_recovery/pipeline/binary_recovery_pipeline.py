"""
Binary recovery pipeline.

Connects Capture binary files
with binary analysis.
"""

from __future__ import annotations


from capture_recovery.io import (
    CaptureBinaryReader,
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
    ) -> None:

        self.reader = (

            reader

            or CaptureBinaryReader()

        )


        self.analyzer = (

            analyzer

            or BinaryAnalyzer()

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


        return {

            "size": summary["size"],

            # compatibility with previous API
            "signature": data[:16],

            "count": summary["count"],

            "detections": summary["detections"],

            "detection_index": summary,

        }



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

            "data": data,

            "analysis": analysis,

        }