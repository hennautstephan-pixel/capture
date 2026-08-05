from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.research.reference_object_extractor import (
    ReferenceObject,
)

from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
)



@dataclass(frozen=True, slots=True)
class ReferenceLibraryResult:
    """
    Result of reference library creation.
    """

    objects_added: int

    library: ObjectLibrary



class ReferenceLibraryBuilder:
    """
    Build an ObjectLibrary from reference objects.

    Converts analysed Capture reference data
    into a searchable reconstruction library.
    """



    def build(
        self,
        objects: tuple[ReferenceObject, ...],
    ) -> ReferenceLibraryResult:
        """
        Create an ObjectLibrary.
        """

        library = ObjectLibrary()


        for obj in objects:

            library.add(
                obj,
            )


        return ReferenceLibraryResult(
            objects_added=len(objects),
            library=library,
        )