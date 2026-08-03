from __future__ import annotations

from dataclasses import dataclass


from capture_recovery.recovery.intelligent_restore_action import (
    IntelligentRestoreAction,
)


@dataclass(slots=True, frozen=True)
class ReconstructedObject:
    """
    Result of an object reconstruction.
    """

    object_type: str

    offset: int

    size: int

    data: bytes

    confidence: float

    source: str



class ObjectReconstructor:
    """
    Reconstruct missing Capture objects from
    a known object library.

    This first version only performs lookup.
    Binary insertion is handled later.
    """


    def __init__(
        self,
        object_library,
    ) -> None:

        self._library = object_library



    def reconstruct(
        self,
        action: IntelligentRestoreAction,
    ) -> ReconstructedObject | None:
        """
        Find the best matching object block.
        """

        candidate = self._library.find(
            object_type=action.object_type,
            size=action.size,
        )


        if candidate is None:

            return None


        return ReconstructedObject(
            object_type=action.object_type,
            offset=action.offset,
            size=len(candidate.data),
            data=candidate.data,
            confidence=action.confidence,
            source=candidate.source,
        )