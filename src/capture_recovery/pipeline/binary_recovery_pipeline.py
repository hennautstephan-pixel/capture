"""
Binary recovery pipeline.

Connects Capture binary files
with binary analysis and reverse engineering.
"""

from __future__ import annotations


from capture_recovery.io import (
    CaptureBinaryReader,
)

from capture_recovery.reverse.reverse_engine import (
    ReverseEngine,
)


from .binary_analyzer import (
    BinaryAnalyzer,
)



class BinaryRecoveryPipeline:
    """
    Recover information from
    binary Capture files.

    Pipeline:

        .c2p
          |
          v
        BinaryReader
          |
          v
        BinaryAnalyzer
          |
          v
        ReverseEngine
          |
          v
        Analysis result

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

        Runs:
        - classic binary analysis
        - reverse binary analysis
        """

        summary = self.analyzer.summary(
            data,
        )


        try:

            reverse_result = (
                self.reverse_engine.analyze(
                    data,
                )
            )


        except Exception as exc:

            # Reverse analysis must not
            # stop the recovery pipeline

            reverse_result = {

                "error": str(exc)

            }



        return {

            "size": summary["size"],


            # compatibility with previous API

            "signature": data[:16],


            "count": summary["count"],


            "detections": summary["detections"],


            "detection_index": summary,


            # new reverse analysis

            "reverse": reverse_result,

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