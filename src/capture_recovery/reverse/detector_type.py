"""
capture_recovery.reverse.detector_type

Common detector type definitions.

This module defines the detector families used
by the reverse engineering framework.
"""

from __future__ import annotations

from enum import Enum


class DetectorType(str, Enum):
    """
    Supported detector families.

    Each detector implementation belongs to
    one detector type.
    """

    NUMERIC = "numeric"

    STRING = "string"

    GUID = "guid"

    PATTERN = "pattern"

    ENTROPY = "entropy"

    STRUCTURE = "structure"

    @property
    def is_binary_detector(self) -> bool:
        """
        Return True for detectors operating
        directly on binary structures.
        """

        return self in {
            DetectorType.NUMERIC,
            DetectorType.GUID,
            DetectorType.PATTERN,
            DetectorType.STRUCTURE,
        }

    @property
    def is_text_detector(self) -> bool:
        """
        Return True for detectors focused
        on textual content.
        """

        return self is DetectorType.STRING

    @property
    def is_analysis_detector(self) -> bool:
        """
        Return True for analytical detectors.
        """

        return self is DetectorType.ENTROPY

    def __str__(self) -> str:
        """
        Return the serialized value.
        """

        return self.value