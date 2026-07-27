from __future__ import annotations

from capture_recovery.indexes.detection_index import DetectionIndex

from .memory_map import MemoryMap
from .region import MemoryRegion


class RegionBuilder:
    """
    Build MemoryRegions from Detection objects.
    """

    def build(
        self,
        index: DetectionIndex,
    ) -> MemoryMap:

        memory = MemoryMap()

        for detection in index:

            memory.add(

                MemoryRegion(

                    offset=detection.offset,

                    size=detection.length,

                    kind=detection.datatype,

                    confidence=detection.confidence,

                    source="DetectionPipeline",

                    metadata={
                        "value": detection.value,
                    },
                )
            )

        memory.merge_adjacent()

        return memory