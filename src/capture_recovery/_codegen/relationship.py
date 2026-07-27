from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Relationship:
    name: str
    target: str
    many: bool = False