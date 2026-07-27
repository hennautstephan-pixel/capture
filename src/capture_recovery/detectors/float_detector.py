from __future__ import annotations

import math
import struct

from .base import Detector
from ..models import Detection


class FloatDetector(Detector):
    """Détecte un flottant IEEE754 32 bits au début d'un buffer."""

    @property
    def name(self) -> str:
        return "Float Detector"

    def detect(self, data: bytes) -> list[Detection]:

        if len(data) < 4:
            return []

        value = struct.unpack_from("<f", data, 0)[0]

        if not math.isfinite(value):
            return []

        return [
            Detection(
                datatype="float",
                offset=0,
                length=4,
                value=value,
                confidence=0.70,
            )
        ]