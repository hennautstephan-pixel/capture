from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BinaryReference:
    """
    Relation binaire entre deux objets.
    """

    source: int

    target: int

    offset: int

    kind: str = "pointer"