"""
capture_recovery.reverse.alignment_detector

Detect binary alignment patterns.
"""

from __future__ import annotations

from collections.abc import Iterable

from .alignment_value import AlignmentValue
from .detection_options import DetectionOptions
from .detector_type import DetectorType



class AlignmentDetector:
    """
    Detect memory alignment patterns.
    """


    def __init__(
        self,
        alignments: Iterable[int] = (
            2,
            4,
            8,
        ),
    ) -> None:

        self._alignments = tuple(
            alignments
        )


    @property
    def name(self) -> str:
        """
        Detector public name.
        """

        return "alignment"



    def detect(
        self,
        data: bytes | bytearray | memoryview,
        options: DetectionOptions | None = None,
        minimum_score: float = 0.5,
    ) -> list[AlignmentValue]:
        """
        Detect alignment patterns.
        """


        if options is not None:

            enabled_types = getattr(
                options,
                "enabled_types",
                None,
            )

            if (
                enabled_types
                and DetectorType.ALIGNMENT
                not in enabled_types
            ):
                return []



        length = len(data)

        results: list[AlignmentValue] = []



        for alignment in self._alignments:

            score = self._calculate_score(
                length,
                alignment,
            )


            if score < minimum_score:
                continue


            results.append(
                AlignmentValue(
                    offset=0,
                    alignment=alignment,
                    score=score,
                    length=length,
                )
            )


        return results



    @staticmethod
    def _calculate_score(
        length: int,
        alignment: int,
    ) -> float:
        """
        Calculate structural alignment score.
        """


        if length <= 0:
            return 0.0


        score = 0.0


        score += 0.4


        if length % alignment == 0:

            score += 0.5


        if length >= alignment * 2:

            score += 0.1


        return min(
            score,
            1.0,
        )



    @property
    def alignments(
        self,
    ) -> tuple[int, ...]:
        """
        Supported alignments.
        """

        return self._alignments