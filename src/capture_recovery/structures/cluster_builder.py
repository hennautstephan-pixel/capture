from __future__ import annotations

from capture_recovery.indexes import DetectionIndex
from capture_recovery.models import Detection

from .cluster import Cluster


class ClusterBuilder:
    """
    Build clusters of nearby detections.

    This class extracts the clustering phase from StructureBuilder.
    It does not perform any semantic reconstruction.
    """

    def __init__(
        self,
        max_gap: int = 8,
    ) -> None:

        self.max_gap = max_gap

    def build(
        self,
        index: DetectionIndex,
    ) -> list[Cluster]:
        """
        Build clusters from a DetectionIndex.
        """

        detections = sorted(
            index.all(),
            key=lambda d: d.offset,
        )

        if not detections:
            return []

        clusters: list[Cluster] = []

        current: list[Detection] = [
            detections[0],
        ]

        for detection in detections[1:]:

            previous = current[-1]

            gap = (
                detection.offset
                - previous.end
            )

            if gap <= self.max_gap:

                current.append(
                    detection,
                )

            else:

                clusters.append(
                    Cluster(
                        tuple(current),
                    )
                )

                current = [
                    detection,
                ]

        clusters.append(
            Cluster(
                tuple(current),
            )
        )

        return clusters

    def __call__(
        self,
        index: DetectionIndex,
    ) -> list[Cluster]:

        return self.build(
            index,
        )