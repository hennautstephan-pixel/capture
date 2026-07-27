"""
Recovered binary structure.
"""

from dataclasses import dataclass
from dataclasses import field

from .field import Field


@dataclass(slots=True)
class Structure:

    name: str

    size: int

    confidence: float

    occurrences: int

    fields: list[Field] = field(default_factory=list)

    def add_field(self, field: Field):

        self.fields.append(field)