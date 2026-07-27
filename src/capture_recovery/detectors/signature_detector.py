from __future__ import annotations

from .base import Detector
from ..models import Detection


class SignatureDetector(Detector):
    """Détecte les signatures binaires connues."""

    SIGNATURES = {
        "zip": b"PK\x03\x04",
        "zip_eocd": b"PK\x05\x06",
        "zip64": b"PK\x06\x06",
        "zlib": b"\x78\x9C",
        "zlib_fast": b"\x78\x01",
        "zlib_best": b"\x78\xDA",
        "png": b"\x89PNG",
        "jpeg": b"\xFF\xD8\xFF",
        "gif87a": b"GIF87a",
        "gif89a": b"GIF89a",
        "xml": b"<?xml",
        "utf8_bom": b"\xEF\xBB\xBF",
        "utf16_le": b"\xFF\xFE",
        "utf16_be": b"\xFE\xFF",
    }

    @property
    def name(self) -> str:
        return "Signature Detector"

    def detect(
        self,
        data: bytes,
    ) -> list[Detection]:

        detections: list[Detection] = []

        for datatype, signature in self.SIGNATURES.items():

            start = 0

            while True:

                offset = data.find(signature, start)

                if offset == -1:
                    break

                detections.append(
                    Detection(
                        datatype=datatype,
                        offset=offset,
                        length=len(signature),
                        value=None,
                        confidence=1.0,
                    )
                )

                start = offset + 1

        detections.sort(key=lambda d: d.offset)

        return detections