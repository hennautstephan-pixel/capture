from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.models import Detection


@dataclass(slots=True, frozen=True)
class Cluster:
    """
    Immutable group of nearby detections.

    A Cluster is an intermediate object between DetectionIndex
    and Structure.

    It represents a candidate binary structure before semantic
    reconstruction.
    """

    detections: tuple[Detection, ...]

    def __post_init__(self) -> None:

        if not self.detections:
            raise ValueError(
                "Cluster cannot be empty."
            )

        ordered = tuple(
            sorted(
                self.detections,
                key=lambda d: d.offset,
            )
        )

        object.__setattr__(
            self,
            "detections",
            ordered,
        )

    # ---------------------------------------------------------
    # Geometry
    # ---------------------------------------------------------

    @property
    def start(self) -> int:
        """
        First byte of the cluster.
        """
        return self.detections[0].offset

    @property
    def end(self) -> int:
        """
        First byte after the cluster.
        """
        return self.detections[-1].end

    @property
    def span(self) -> int:
        """
        Total byte span.
        """
        return self.end - self.start

    @property
    def size(self) -> int:
        """
        Alias for span.
        """
        return self.span

    @property
    def detection_count(self) -> int:
        """
        Number of detections.
        """
        return len(self.detections)

    @property
    def confidence(self) -> float:
        """
        Average confidence.
        """
        return (
            sum(d.confidence for d in self.detections)
            / len(self.detections)
        )

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    def contains(
        self,
        offset: int,
    ) -> bool:

        return self.start <= offset < self.end

    def overlaps(
        self,
        other: "Cluster",
    ) -> bool:

        return (
            self.start < other.end
            and other.start < self.end
        )

    def adjacent(
        self,
        other: "Cluster",
    ) -> bool:

        return (
            self.end == other.start
            or other.end == self.start
        )

    def distance_to(
        self,
        other: "Cluster",
    ) -> int:
        """
        Distance in bytes between clusters.

        Returns 0 if they overlap.
        """

        if self.overlaps(other):
            return 0

        if self.end <= other.start:
            return other.start - self.end

        return self.start - other.end

    # ---------------------------------------------------------
    # Merge
    # ---------------------------------------------------------

    def merge(
        self,
        other: "Cluster",
    ) -> "Cluster":

        return Cluster(
            self.detections
            + other.detections
        )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def first(self) -> Detection:

        return self.detections[0]

    def last(self) -> Detection:

        return self.detections[-1]

    # ---------------------------------------------------------
    # Magic methods
    # ---------------------------------------------------------

    def __len__(self) -> int:

        return self.detection_count

    def __iter__(self):

        return iter(self.detections)

    def __contains__(
        self,
        offset: int,
    ) -> bool:

        return self.contains(offset)

    def __repr__(self) -> str:

        return (
            "Cluster("
            f"start=0x{self.start:X}, "
            f"end=0x{self.end:X}, "
            f"detections={len(self.detections)}, "
            f"confidence={self.confidence:.2f})"
        )