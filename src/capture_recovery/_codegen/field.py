from __future__ import annotations

from dataclasses import dataclass
from capture_recovery.structures.datatype import DataType


@dataclass(slots=True, frozen=True)
class Field:
    name: str
    datatype: DataType
    required: bool = False
    description: str = ""