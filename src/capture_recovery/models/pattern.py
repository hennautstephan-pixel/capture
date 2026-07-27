"""
Repeated structure description.
"""

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class Pattern:

    signature: str

    block_size: int

    occurrences: int = 0

    offsets: list[int] = field(default_factory=list)

    confidence: float = 0.0