from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:

    from capture_recovery.research.object_signature_index import (
        SignatureLookupResult,
    )



@dataclass(frozen=True, slots=True)
class LibraryObject:
    """
    Object stored in reconstruction library.

    This model keeps compatibility with
    existing extractors and reconstruction code.
    """

    object_type: str

    data: bytes

    source: str

    signature: bytes | str = b""

    offset: int = 0



class ObjectLibrary:
    """
    Central reconstruction object library.

    Provides:

    - object storage
    - object counting
    - object search
    - signature indexing
    """



    def __init__(self) -> None:

        self._objects: list[LibraryObject] = []

        self._signature_index = None



    def _ensure_index(self) -> None:
        """
        Lazy creation of signature index.

        Avoids circular imports.
        """

        if self._signature_index is None:

            from capture_recovery.research.object_signature_index import (
                ObjectSignatureIndex,
            )

            self._signature_index = (
                ObjectSignatureIndex()
            )



    def add(
        self,
        obj: LibraryObject,
    ) -> None:
        """
        Add an object to the library.
        """

        self._ensure_index()


        self._objects.append(
            obj
        )


        self._signature_index.add(
            obj
        )



    def add_many(
        self,
        objects: tuple[LibraryObject, ...],
    ) -> None:
        """
        Add multiple objects.
        """

        for obj in objects:

            self.add(
                obj
            )



    def count(
        self,
    ) -> int:
        """
        Return number of stored objects.

        Compatibility API.
        """

        return len(
            self._objects
        )



    def find(
        self,
        *,
        object_type: str,
        size: int | None = None,
    ) -> LibraryObject | None:
        """
        Find object by type.

        Optional size constraint.
        """

        for obj in self._objects:

            if (
                obj.object_type
                !=
                object_type
            ):
                continue


            if size is not None:

                if len(obj.data) != size:

                    continue


            return obj


        return None



    def find_by_signature(
        self,
        signature: str,
    ) -> SignatureLookupResult:
        """
        Find object using signature index.
        """

        self._ensure_index()


        return (
            self._signature_index.find(
                signature
            )
        )



    def contains_signature(
        self,
        signature: str,
    ) -> bool:
        """
        Check if signature exists.
        """

        self._ensure_index()


        return (
            self._signature_index.contains(
                signature
            )
        )



    @property
    def objects(
        self,
    ) -> tuple[LibraryObject, ...]:
        """
        Return all stored objects.
        """

        return tuple(
            self._objects
        )



    @property
    def size(
        self,
    ) -> int:
        """
        Number of stored objects.
        """

        return len(
            self._objects
        )