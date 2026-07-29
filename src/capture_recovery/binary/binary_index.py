from __future__ import annotations

from dataclasses import dataclass

from .binary_object import BinaryObject


@dataclass(slots=True)
class BinaryIndex:

    objects: dict[int, BinaryObject]

    def get(self, identifier: int) -> BinaryObject | None:
        return self.objects.get(identifier)

    def all(self):

        return self.objects.values()

    def count(self):

        return len(self.objects)