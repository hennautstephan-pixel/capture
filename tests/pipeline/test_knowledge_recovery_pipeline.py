from __future__ import annotations

from collections.abc import Iterable

from capture_recovery.indexes import DetectionIndex
from capture_recovery.knowledge import (
    KnowledgeEngine,
    KnowledgeResult,
)
from capture_recovery.models import Detection
from capture_recovery.structures import (
    Structure,
    StructureBuilder,
)


class KnowledgeRecoveryPipeline:
    """
    Orchestrates the knowledge recovery stage.

    Detection
        ↓
    DetectionIndex
        ↓
    StructureBuilder
        ↓
    KnowledgeEngine
        ↓
    KnowledgeResult
    """

    def __init__(
        self,
        knowledge_engine: KnowledgeEngine,
        structure_builder: StructureBuilder | None = None,
    ) -> None:

        self.knowledge_engine = knowledge_engine
        self.structure_builder = (
            structure_builder
            or StructureBuilder()
        )

    # ---------------------------------------------------------

    def analyze(
        self,
        detections: Iterable[Detection],
    ) -> KnowledgeResult:
        """
        Analyze binary detections.

        Parameters
        ----------
        detections:
            Iterable of Detection objects.

        Returns
        -------
        KnowledgeResult
        """

        detection_list = list(detections)

        if not detection_list:
            return KnowledgeResult()

        index = DetectionIndex(
            detection_list,
        )

        structures = self.structure_builder.build(
            index,
        )

        return self.knowledge_engine.analyze(
            structures,
        )

    # ---------------------------------------------------------

    def analyze_index(
        self,
        index: DetectionIndex,
    ) -> KnowledgeResult:
        """
        Analyze an existing DetectionIndex.
        """

        structures = self.structure_builder.build(
            index,
        )

        return self.knowledge_engine.analyze(
            structures,
        )

    # ---------------------------------------------------------

    def analyze_structures(
        self,
        structures: Iterable[Structure],
    ) -> KnowledgeResult:
        """
        Analyze already reconstructed structures.
        """

        return self.knowledge_engine.analyze(
            structures,
        )