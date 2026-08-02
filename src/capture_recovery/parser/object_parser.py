from __future__ import annotations

from dataclasses import dataclass

from .binary_cursor import BinaryCursor


@dataclass(slots=True, frozen=True)
class ParsedObject:
    """
    Candidate object extracted from a Capture stream.

    At this stage the parser does not attempt to
    interpret the binary data. It only records the
    location and preserves the raw bytes.
    """

    offset: int

    size: int

    raw: bytes

    @property
    def is_empty(self) -> bool:
        return self.size == 0


@dataclass(slots=True, frozen=True)
class ObjectCollection:
    """
    Collection of parsed objects.
    """

    objects: tuple[ParsedObject, ...]

    @property
    def count(self) -> int:
        return len(self.objects)

    @property
    def is_empty(self) -> bool:
        return self.count == 0


class ObjectParser:
    """
    Extract candidate objects from a decompressed stream.

    Until the Capture object format is fully understood,
    the parser returns a single object covering the whole
    stream. Later revisions will split the stream into
    real Capture objects.
    """

    def parse(
        self,
        data: bytes,
    ) -> ObjectCollection:

        if not data:
            return ObjectCollection(objects=())

        cursor = BinaryCursor(data)

        obj = ParsedObject(
            offset=cursor.tell(),
            size=cursor.remaining,
            raw=cursor.read_bytes(cursor.remaining),
        )

        return ObjectCollection(
            objects=(obj,),
        )