from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BinaryObject:
    """
    Objet binaire brut extrait du fichier C2P.

    Aucun décodage métier n'est effectué ici.
    """

    identifier: int

    offset: int

    size: int

    raw_data: bytes

    type_hint: int | None = None

    name: str | None = None

    @property
    def end_offset(self) -> int:
        return self.offset + self.size