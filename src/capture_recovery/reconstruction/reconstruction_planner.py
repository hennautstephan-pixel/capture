from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.recovery.intelligent_restore_action import (
    IntelligentRestoreAction,
)

from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
    LibraryObject,
)



@dataclass(slots=True, frozen=True)
class ReconstructionPlan:
    """
    Planned reconstruction of a missing object.
    """

    object_type: str

    offset: int

    size: int

    replacement: bytes

    source: str

    confidence: float



class ReconstructionPlanner:
    """
    Create reconstruction plans from intelligent
    repair actions and known corpus objects.
    """


    def __init__(
        self,
        object_library: ObjectLibrary,
    ) -> None:

        self._library = object_library



    def plan(
        self,
        action: IntelligentRestoreAction,
    ) -> ReconstructionPlan | None:
        """
        Find the best object and create a plan.
        """

        candidate = self._find_candidate(
            action,
        )


        if candidate is None:

            return None


        return ReconstructionPlan(
            object_type=action.object_type,
            offset=action.offset,
            size=len(candidate.data),
            replacement=candidate.data,
            source=candidate.source,
            confidence=action.confidence,
        )



    def _find_candidate(
        self,
        action: IntelligentRestoreAction,
    ) -> LibraryObject | None:
        """
        Search the object library.
        """

        candidate = self._library.find(
            object_type=action.object_type,
            size=action.size,
        )


        if candidate is not None:

            return candidate


        return self._library.find(
            object_type=action.object_type,
        )