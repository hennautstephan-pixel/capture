from __future__ import annotations

from .cluster import Cluster
from .cluster_builder import ClusterBuilder
from .field import Field
from .structure import Structure
from .structure_candidate import StructureCandidate
from .structure_scorer import StructureScorer


class StructureBuilder:
    """
    Build reconstructed structures.

    Pipeline
    --------

    DetectionIndex
            │
            ▼
    ClusterBuilder
            │
            ▼
    Cluster
            │
            ▼
    StructureCandidate
            │
            ▼
    StructureScorer
            │
            ▼
    Structure
    """

    def __init__(
        self,
        max_gap: int = 8,
        scorer: StructureScorer | None = None,
    ) -> None:

        self._cluster_builder = ClusterBuilder(
            max_gap=max_gap,
        )

        self._scorer = (
            scorer
            if scorer is not None
            else StructureScorer()
        )

    @property
    def max_gap(self) -> int:
        return self._cluster_builder.max_gap

    @property
    def scorer(self) -> StructureScorer:
        return self._scorer

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        index,
    ) -> list[Structure]:

        clusters = self._cluster_builder.build(
            index,
        )

        return [
            self._process_cluster(cluster)
            for cluster in clusters
        ]

    # ---------------------------------------------------------
    # Internal pipeline
    # ---------------------------------------------------------

    def _process_cluster(
        self,
        cluster: Cluster,
    ) -> Structure:

        candidate = self._create_candidate(
            cluster,
        )

        self._score_candidate(
            candidate,
        )

        return self._build_structure(
            candidate,
        )

    def _create_candidate(
        self,
        cluster: Cluster,
    ) -> StructureCandidate:

        return StructureCandidate(
            cluster=cluster,
        )

    def _score_candidate(
        self,
        candidate: StructureCandidate,
    ) -> None:

        self._scorer.score(
            candidate,
        )

    def _build_structure(
        self,
        candidate: StructureCandidate,
    ) -> Structure:

        structure = Structure(
            name=candidate.estimated_type,
            offset=candidate.offset,
            length=candidate.length,
            confidence=candidate.confidence,
        )

        for i, detection in enumerate(candidate):

            structure.add(
                Field(
                    name=f"field_{i}",
                    offset=detection.offset,
                    length=detection.length,
                    datatype=detection.datatype,
                    value=detection.value,
                    confidence=detection.confidence,
                )
            )

        #
        # Additional reconstruction metadata.
        #

        structure.metadata.update(
            {
                "score": candidate.score,
                "estimated_type": candidate.estimated_type,
            }
        )

        return structure

    # ---------------------------------------------------------
    # Callable
    # ---------------------------------------------------------

    def __call__(
        self,
        index,
    ) -> list[Structure]:

        return self.build(
            index,
        )