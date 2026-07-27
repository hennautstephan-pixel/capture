"""
Field description inferred from binary data.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Field:

    offset: int

    size: int

    datatype: str

    confidence: float

    name: str = ""