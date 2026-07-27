from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from capture_recovery.indexes.detection_index import DetectionIndex
from capture_recovery.memory.memory_map import MemoryMap


class RegionPlugin(ABC):

    @abstractmethod
    def build(
        self,
        index: DetectionIndex,
        memory: MemoryMap,
    ) -> None:
        """
        Build regions.
        """