"""
Finding model.
"""

from dataclasses import dataclass

from .enums import FindingType
from .enums import Severity


@dataclass(slots=True)
class Finding:
    """
    Single piece of information discovered during analysis.
    """

    offset: int

    length: int

    category: FindingType

    value: str

    description: str

    severity: Severity = Severity.INFO

    analyzer: str = ""

    confidence: float = 1.0