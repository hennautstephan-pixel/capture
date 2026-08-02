from __future__ import annotations

from dataclasses import dataclass

from .field_correlator import (
    CorrelationReport,
    FieldCorrelation,
)


@dataclass(slots=True, frozen=True)
class CandidateObject:
    """
    Candidate binary object composed of several
    correlated fields.

    This object has no confirmed semantic meaning.
    """

    offset: int

    length: int

    confidence: float

    fields: tuple[
        FieldCorrelation,
        ...
    ]

    data: bytes = b""

    semantic_name: str | None = None

    @property
    def end(self) -> int:
        return self.offset + self.length

    @property
    def field_count(self) -> int:
        return len(self.fields)

    @property
    def has_data(self) -> bool:
        """
        Return True if binary data are available.
        """
        return bool(self.data)

    def encode(self) -> bytes:
        """
        Return the binary representation of this object.

        Future versions may rebuild the bytes from the
        decoded fields instead of returning the original
        binary payload.
        """
        return self.data


@dataclass(slots=True, frozen=True)
class ObjectMap:
    """
    Collection of candidate binary objects.
    """

    objects: list[CandidateObject]

    @property
    def object_count(self) -> int:
        return len(self.objects)

    def by_offset(self) -> list[CandidateObject]:

        return sorted(
            self.objects,
            key=lambda obj: (
                obj.offset,
                obj.length,
            ),
        )

    def by_confidence(self) -> list[CandidateObject]:

        return sorted(
            self.objects,
            key=lambda obj: (
                -obj.confidence,
                obj.offset,
            ),
        )

    def with_data(self) -> list[CandidateObject]:
        """
        Return only objects carrying binary data.
        """

        return [
            obj
            for obj in self.objects
            if obj.has_data
        ]


class ObjectMapper:
    """
    Group correlated fields into candidate objects.

    Fields are grouped when they overlap or are
    separated by at most ``max_gap`` bytes.
    """

    def map(
        self,
        report: CorrelationReport,
        *,
        max_gap: int = 0,
    ) -> ObjectMap:

        ordered = report.by_offset()

        if not ordered:
            return ObjectMap([])

        objects: list[CandidateObject] = []

        current: list[FieldCorrelation] = [
            ordered[0]
        ]

        start = ordered[0].offset
        end = ordered[0].end

        for field in ordered[1:]:

            if field.offset <= end + max_gap:

                current.append(field)

                end = max(
                    end,
                    field.end,
                )

                continue

            objects.append(
                self._build_object(
                    current,
                    start,
                    end,
                )
            )

            current = [field]
            start = field.offset
            end = field.end

        objects.append(
            self._build_object(
                current,
                start,
                end,
            )
        )

        return ObjectMap(objects)

    @staticmethod
    def _build_object(
        fields: list[FieldCorrelation],
        start: int,
        end: int,
    ) -> CandidateObject:
        """
        Build one candidate object.

        The confidence is based on the average field
        confidence with a small bonus for objects
        containing several correlated fields.
        """

        average = (
            sum(
                field.confidence
                for field in fields
            )
            / len(fields)
        )

        bonus = min(
            len(fields) * 0.05,
            0.20,
        )

        confidence = min(
            average + bonus,
            1.0,
        )

        return CandidateObject(
            offset=start,
            length=end - start,
            confidence=confidence,
            fields=tuple(fields),
            data=b"",
        )