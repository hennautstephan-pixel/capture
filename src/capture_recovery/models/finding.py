"""
Finding model.

Unified model for binary analysis,
reverse analysis and recovery.
"""

from __future__ import annotations

from dataclasses import dataclass

from .enums import (
    FindingType,
    Severity,
)



@dataclass(slots=True)
class Finding:
    """
    Generic analysis finding.

    Compatible with:
    - binary analyzers
    - UTF16 analyzer
    - reverse recovery
    - JSON export
    """


    #
    # Legacy analysis fields
    #

    offset: int | None = None

    length: int | None = None

    category: FindingType | str | None = None

    description: str | None = None

    value: str | None = None

    severity: Severity | str | None = None



    #
    # Reverse recovery fields
    #

    type: str | None = None

    source: str | None = None

    confidence: float = 0.0



    def to_dict(self) -> dict:
        """
        JSON compatible representation.
        """


        category = self.category


        if hasattr(
            category,
            "value",
        ):

            category = category.value



        severity = self.severity


        if hasattr(
            severity,
            "value",
        ):

            severity = severity.value



        return {

            "type":
                self.type
                or category
                or "unknown",


            "category":
                category,


            "description":
                self.description,


            "offset":
                self.offset,


            "length":
                self.length,


            "value":
                self.value,


            "severity":
                severity,


            "source":
                self.source,


            "confidence":
                self.confidence,

        }