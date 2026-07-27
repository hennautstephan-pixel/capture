from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capture_recovery.models import DataType


@dataclass(slots=True)
class Field:
    """
    Field belonging to a reconstructed structure.
    """

    name: str

    offset: int

    length: int

    datatype: DataType

    value: Any = None

    confidence: float = 1.0

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def end(self) -> int:
        return self.offset + self.length

    def contains(self, offset: int) -> bool:
        return self.offset <= offset < self.end

    def __len__(self) -> int:
        return self.length