from __future__ import annotations

from .base import Detector
from ..models import Detection


class AsciiDetector(Detector):
    """Détecte les chaînes ASCII imprimables."""

    MIN_LENGTH = 4

    @property
    def name(self) -> str:
        return "ASCII Detector"

    def detect(
        self,
        data: bytes,
    ) -> list[Detection]:

        detections: list[Detection] = []

        start: int | None = None

        for index, byte in enumerate(data):

            if 32 <= byte <= 126:

                if start is None:
                    start = index

            else:

                if start is not None:

                    length = index - start

                    if length >= self.MIN_LENGTH:

                        text = data[start:index].decode(
                            "ascii",
                            errors="strict",
                        )

                        detections.append(
                            Detection(
                                datatype="ascii",
                                offset=start,
                                length=length,
                                value=text,
                                confidence=1.0,
                            )
                        )

                    start = None

        #
        # Gère une chaîne qui se termine à la fin du fichier.
        #
        if start is not None:

            length = len(data) - start

            if length >= self.MIN_LENGTH:

                text = data[start:].decode(
                    "ascii",
                    errors="strict",
                )

                detections.append(
                    Detection(
                        datatype="ascii",
                        offset=start,
                        length=length,
                        value=text,
                        confidence=1.0,
                    )
                )

        return detections