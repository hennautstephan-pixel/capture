from __future__ import annotations


class DetectorRegistry:
    """
    Registry of detectors used by BinaryInspector.

    The registry only requires each detector to implement:

        detect(data: bytes)

    New detectors can simply be registered here.
    """

    def __init__(self) -> None:
        self._detectors = []

    def register(self, detector) -> None:
        self._detectors.append(detector)

    def detectors(self):
        return tuple(self._detectors)

    def __iter__(self):
        return iter(self._detectors)

    def __len__(self) -> int:
        return len(self._detectors)