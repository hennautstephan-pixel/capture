from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.research.reference_project_analyzer import (
    ReferenceProjectModel,
    ReferenceBlock,
)



@dataclass(frozen=True, slots=True)
class ReferenceObject:
    """
    Object extracted from a reference project.
    """

    object_type: str

    offset: int

    size: int

    signature: str

    data: bytes

    confidence: float



class ReferenceObjectExtractor:
    """
    Convert reference binary blocks into
    reference objects.

    Current implementation:
    - one block = one candidate object

    Future:
    - Capture object recognition
    - semantic classification
    - cross-reference analysis
    """



    DEFAULT_OBJECT_TYPE = "unknown"



    def __init__(
        self,
        object_type: str = DEFAULT_OBJECT_TYPE,
    ) -> None:

        self._object_type = object_type



    def extract(
        self,
        project: ReferenceProjectModel,
    ) -> tuple[ReferenceObject, ...]:
        """
        Extract objects from reference model.
        """

        objects = []


        for block in project.blocks:

            objects.append(
                self._from_block(
                    block
                )
            )


        return tuple(
            objects
        )



    def _from_block(
        self,
        block: ReferenceBlock,
    ) -> ReferenceObject:
        """
        Convert one binary block into an object.
        """

        return ReferenceObject(
            object_type=self._object_type,
            offset=block.offset,
            size=block.size,
            signature=block.signature,
            data=block.data,
            confidence=0.5,
        )