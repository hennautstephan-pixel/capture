from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class LibraryObject:
    """
    Object stored in the reconstruction library.
    """

    object_type: str

    data: bytes

    source: str

    signature: bytes = b""



@dataclass(slots=True)
class ObjectLibrary:
    """
    Collection of known Capture objects.

    Objects are extracted from validated samples
    and reused during reconstruction.
    """

    _objects: list[LibraryObject] = field(
        default_factory=list
    )


    def add(
        self,
        obj: LibraryObject,
    ) -> None:
        """
        Add an object to the library.
        """

        self._objects.append(
            obj,
        )


    def find(
        self,
        *,
        object_type: str,
        size: int | None = None,
        signature: bytes | None = None,
    ) -> LibraryObject | None:
        """
        Find the best matching object.
        """

        candidates = [
            obj
            for obj in self._objects
            if obj.object_type == object_type
        ]


        if signature is not None:

            signature_matches = [
                obj
                for obj in candidates
                if obj.signature == signature
            ]

            if signature_matches:

                candidates = signature_matches


        if size is not None:

            sized = [
                obj
                for obj in candidates
                if len(obj.data) == size
            ]

            if sized:

                candidates = sized


        if not candidates:

            return None


        return candidates[0]



    def count(self) -> int:
        """
        Return number of stored objects.
        """

        return len(
            self._objects
        )


    def objects(
        self,
    ) -> tuple[LibraryObject, ...]:
        """
        Return immutable object view.
        """

        return tuple(
            self._objects
        )