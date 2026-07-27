"""
Logical structure signature.
"""

from dataclasses import dataclass
from dataclasses import field


@dataclass(slots=True)
class Signature:

    offset: int

    block_size: int

    tokens: list[str] = field(default_factory=list)

    @property
    def key(self) -> str:
        return "-".join(self.tokens)