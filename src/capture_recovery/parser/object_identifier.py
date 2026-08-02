from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .object_parser import (
    ObjectCollection,
    ParsedObject,
)


class CandidateKind(Enum):
    """
    Classification of a candidate object.

    The values are intentionally generic. They
    will be refined as the Capture format becomes
    better understood.
    """

    UNKNOWN = auto()

    EMPTY = auto()

    BINARY = auto()

    TEXT = auto()

    MIXED = auto()


@dataclass(slots=True, frozen=True)
class IdentifiedObject:
    """
    One analysed object candidate.
    """

    offset: int

    size: int

    kind: CandidateKind

    printable_ratio: float

    zero_ratio: float

    raw: bytes

    @property
    def is_empty(self) -> bool:
        return self.size == 0


@dataclass(slots=True, frozen=True)
class IdentificationReport:
    """
    Result of an object identification pass.
    """

    objects: tuple[IdentifiedObject, ...]

    @property
    def count(self) -> int:
        return len(self.objects)

    @property
    def empty_count(self) -> int:
        return sum(
            obj.kind is CandidateKind.EMPTY
            for obj in self.objects
        )


class ObjectIdentifier:
    """
    Characterise parsed objects.

    This class does not try to identify Capture
    entities yet. It only extracts simple metrics
    useful for reverse engineering.
    """

    def identify(
        self,
        collection: ObjectCollection,
    ) -> IdentificationReport:

        objects: list[IdentifiedObject] = []

        for candidate in collection.objects:

            objects.append(
                self._identify(
                    candidate,
                )
            )

        return IdentificationReport(
            objects=tuple(objects),
        )

    def _identify(
        self,
        candidate: ParsedObject,
    ) -> IdentifiedObject:

        data = candidate.raw

        size = len(data)

        if size == 0:

            return IdentifiedObject(
                offset=candidate.offset,
                size=0,
                kind=CandidateKind.EMPTY,
                printable_ratio=0.0,
                zero_ratio=1.0,
                raw=data,
            )

        printable = sum(
            32 <= byte <= 126
            for byte in data
        )

        zeros = data.count(0)

        printable_ratio = printable / size

        zero_ratio = zeros / size

        if printable_ratio > 0.90:

            kind = CandidateKind.TEXT

        elif printable_ratio > 0.20:

            kind = CandidateKind.MIXED

        else:

            kind = CandidateKind.BINARY

        return IdentifiedObject(
            offset=candidate.offset,
            size=size,
            kind=kind,
            printable_ratio=printable_ratio,
            zero_ratio=zero_ratio,
            raw=data,
        )