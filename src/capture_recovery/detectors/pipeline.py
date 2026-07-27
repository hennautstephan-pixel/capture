from __future__ import annotations

from collections.abc import Iterable

from .base import Detector
from ..models import Detection


class DetectorPipeline:

    def __init__(
        self,
        detectors: Iterable[Detector],
    ):
        self.detectors = list(detectors)

    def detect(
        self,
        data: bytes,
    ) -> list[Detection]:

        detections: list[Detection] = []

        for detector in self.detectors:
            detections.extend(detector.detect(data))

        return detections