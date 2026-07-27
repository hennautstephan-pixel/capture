from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class SemanticObject:
    """
    High-level semantic object inferred from reconstructed structures.
    """

    object_type: str

    identifier: str | int

    properties: dict[str, Any] = field(default_factory=dict)

    confidence: float = 1.0

    def get(self, name: str, default: Any = None) -> Any:
        return self.properties.get(name, default)

    def has(self, name: str) -> bool:
        return name in self.properties