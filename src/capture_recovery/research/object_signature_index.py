from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.research.reference_object_extractor import (
    ReferenceObject,
)



@dataclass(frozen=True, slots=True)
class SignatureLookupResult:
    """
    Result of signature lookup.
    """

    found: bool

    object: ReferenceObject | None



class ObjectSignatureIndex:
    """
    Fast lookup index for reference objects.

    Maps binary signatures to known objects.
    """



    def __init__(self) -> None:

        self._objects: dict[
            str,
            ReferenceObject,
        ] = {}



    def add(
        self,
        obj: ReferenceObject,
    ) -> None:
        """
        Add object to index.
        """

        self._objects[
            obj.signature
        ] = obj



    def add_many(
        self,
        objects: tuple[ReferenceObject, ...],
    ) -> None:
        """
        Add multiple objects.
        """

        for obj in objects:

            self.add(
                obj
            )



    def find(
        self,
        signature: str,
    ) -> SignatureLookupResult:
        """
        Search object by signature.
        """

        obj = self._objects.get(
            signature
        )


        return SignatureLookupResult(
            found=obj is not None,
            object=obj,
        )



    def contains(
        self,
        signature: str,
    ) -> bool:
        """
        Check if signature exists.
        """

        return (
            signature
            in self._objects
        )



    @property
    def size(self) -> int:
        """
        Number of indexed objects.
        """

        return len(
            self._objects
        )