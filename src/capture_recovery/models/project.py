"""
Recovered Capture project.
"""

from dataclasses import dataclass
from dataclasses import field

from .structure import Structure


@dataclass(slots=True)
class Project:

    version: str = ""

    structures: list[Structure] = field(default_factory=list)