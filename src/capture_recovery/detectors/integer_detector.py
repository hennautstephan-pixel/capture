from __future__ import annotations

import struct

from .base import Detector
from ..models import Detection


class IntegerDetector(Detector):
    """Détecte les entiers 32 bits signés et non signés."""

    MIN_VALUE = 1
    MAX_VALUE = 1_000_000

    def __init__(self, scan_unaligned: bool = False) -> None:
        """
        Parameters
        ----------
        scan_unaligned:
            False -> ne teste que les offsets multiples de 4 (mode normal).
            True  -> teste tous les offsets (mode reverse engineering).
        """
        self.scan_unaligned = scan_unaligned

    @property
    def name(self) -> str:
        return "Integer Detector"

    def detect(
        self,
        data: bytes,
    ) -> list[Detection]:

        detections: list[Detection] = []

        if len(data) < 4:
            return detections

        if self.scan_unaligned:
            offsets = range(len(data) - 3)
        else:
            offsets = range(0, len(data) - 3, 4)

        for offset in offsets:

            signed = struct.unpack_from("<i", data, offset)[0]
            unsigned = struct.unpack_from("<I", data, offset)[0]

            aligned = (offset % 4) == 0
            confidence = 0.85 if aligned else 0.60

            if self.MIN_VALUE <= signed <= self.MAX_VALUE:

                detections.append(
                    Detection(
                        datatype="int32",
                        offset=offset,
                        length=4,
                        value=signed,
                        confidence=confidence,
                    )
                )

            if (
                unsigned != signed
                and self.MIN_VALUE <= unsigned <= self.MAX_VALUE
            ):

                detections.append(
                    Detection(
                        datatype="uint32",
                        offset=offset,
                        length=4,
                        value=unsigned,
                        confidence=confidence,
                    )
                )

        return detections