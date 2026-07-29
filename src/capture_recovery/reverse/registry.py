"""
capture_recovery.reverse.registry

Detector registry system.
"""

from __future__ import annotations

from collections.abc import Iterable


class ReverseRegistry:
    """
    Registry of reverse detectors.
    """



    def __init__(
        self,
        detectors: Iterable[object] = (),
    ) -> None:

        self._detectors: list[object] = []

        for detector in detectors:
            self.register(
                detector
            )



    def register(
        self,
        detector: object,
    ) -> None:
        """
        Register a detector.
        """

        if detector in self._detectors:
            return


        self._detectors.append(
            detector
        )



    def unregister(
        self,
        detector: object,
    ) -> None:
        """
        Remove detector.
        """

        if detector in self._detectors:

            self._detectors.remove(
                detector
            )



    def get(
        self,
        detector_type: type,
    ) -> object | None:
        """
        Find detector by class.
        """

        for detector in self._detectors:

            if isinstance(
                detector,
                detector_type,
            ):
                return detector


        return None



    def all(
        self,
    ) -> tuple[object, ...]:
        """
        Return registered detectors.
        """

        return tuple(
            self._detectors
        )



    def clear(
        self,
    ) -> None:
        """
        Remove all detectors.
        """

        self._detectors.clear()



    def __len__(
        self,
    ) -> int:

        return len(
            self._detectors
        )