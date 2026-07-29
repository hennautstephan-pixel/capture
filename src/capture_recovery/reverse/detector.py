"""
capture_recovery.reverse.detector

Generic reverse detector protocol.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .detection_options import DetectionOptions



@runtime_checkable
class ReverseDetector(Protocol):
    """
    Common interface for all reverse detectors.
    """


    @property
    def name(self) -> str:
        """
        Detector public name.
        """
        ...


    def detect(
        self,
        data: bytes,
        options: DetectionOptions | None = None,
    ) -> list[object]:
        """
        Analyze binary data.
        """
        ...