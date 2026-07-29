"""
capture_recovery.reverse.detection_strategy

Detection strategies shared by every binary detector.

The strategy defines how offsets are visited inside a binary buffer.
It is intentionally independent from any specific detector
(numeric, string, GUID, entropy, ...).
"""

from __future__ import annotations

from enum import Enum


class DetectionStrategy(str, Enum):
    """
    Strategy used to iterate over a binary buffer.

    SCAN
        Visit every possible byte offset.

        Example
        -------
        0, 1, 2, 3, 4, ...

    ALIGNED
        Visit only aligned offsets.

        The alignment value is supplied by DetectionOptions.

        Example (alignment=4)
        ---------------------
        0, 4, 8, 12, ...

    CUSTOM
        Visit only offsets supplied by the caller.

        Example
        -------
        [12, 48, 96, 128]
    """

    SCAN = "scan"

    ALIGNED = "aligned"

    CUSTOM = "custom"

    @property
    def requires_alignment(self) -> bool:
        """
        Return True if the strategy requires
        an alignment value.
        """

        return self is DetectionStrategy.ALIGNED

    @property
    def requires_custom_offsets(self) -> bool:
        """
        Return True if the strategy requires
        an explicit iterable of offsets.
        """

        return self is DetectionStrategy.CUSTOM

    @property
    def scans_every_offset(self) -> bool:
        """
        Return True if every byte offset
        must be visited.
        """

        return self is DetectionStrategy.SCAN

    def __str__(self) -> str:
        """
        Human-readable representation.
        """

        return self.value