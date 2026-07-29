from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BinarySection:

    name: str

    offset: int

    size: int