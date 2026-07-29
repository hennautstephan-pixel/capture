from dataclasses import dataclass

from .binary_section import BinarySection


@dataclass(slots=True, frozen=True)
class BinaryContainer:

    path: str

    file_size: int

    sections: tuple[BinarySection, ...]