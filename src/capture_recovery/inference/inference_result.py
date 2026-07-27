from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class InferenceResult:
    """
    Result produced by an inference rule.
    """

    matched: bool

    structure_name: str | None = None

    confidence: float = 0.0

    reason: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)