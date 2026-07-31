from __future__ import annotations

from dataclasses import dataclass, field

from capture_recovery.models.project import Project
from capture_recovery.types import (
    BinaryDetection,
    Evidence,
    Metadata,
    ReverseAnalysis,
    SemanticDetection,
    SemanticObject,
)


@dataclass(slots=True)
class BinaryAnalysisResult:
    """
    Result produced by BinaryRecoveryPipeline.
    """

    data: bytes = b""

    size: int = 0

    signature: bytes = b""

    detections: list[BinaryDetection] = field(
        default_factory=list,
    )

    reverse: ReverseAnalysis | None = None

    metadata: Metadata = field(
        default_factory=dict,
    )

    @property
    def count(self) -> int:
        """
        Number of detected binary elements.
        """
        return len(self.detections)

    def add_detection(
        self,
        detection: BinaryDetection,
    ) -> None:
        self.detections.append(detection)

    def clear(self) -> None:
        self.detections.clear()

    def __len__(self) -> int:
        return self.count

    def __bool__(self) -> bool:
        return self.count > 0


@dataclass(slots=True)
class SemanticRecoveryResult:
    """
    Result produced by SemanticRecoveryPipeline.
    """

    detections: list[SemanticDetection] = field(
        default_factory=list,
    )

    objects: list[SemanticObject] = field(
        default_factory=list,
    )

    reverse: ReverseAnalysis | None = None

    evidence: Evidence = field(
        default_factory=dict,
    )

    metadata: Metadata = field(
        default_factory=dict,
    )

    @property
    def count(self) -> int:
        """
        Number of semantic objects.
        """
        return len(self.objects)

    @property
    def property_count(self) -> int:
        """
        Total number of recovered semantic properties.
        """

        total = 0

        for obj in self.objects:
            total += getattr(
                obj,
                "property_count",
                len(getattr(obj, "properties", {})),
            )

        return total

    @property
    def candidate_count(self) -> int:
        """
        Total number of semantic candidates.
        Currently one candidate per semantic object.
        """

        return len(self.objects)

    @property
    def average_confidence(self) -> float:
        """
        Average semantic confidence.
        """

        if not self.objects:
            return 0.0

        values = [
            getattr(obj, "confidence", 0.0)
            for obj in self.objects
        ]

        return sum(values) / len(values)

    @property
    def minimum_confidence(self) -> float:
        """
        Lowest semantic confidence.
        """

        if not self.objects:
            return 0.0

        return min(
            getattr(obj, "confidence", 0.0)
            for obj in self.objects
        )

    @property
    def maximum_confidence(self) -> float:
        """
        Highest semantic confidence.
        """

        if not self.objects:
            return 0.0

        return max(
            getattr(obj, "confidence", 0.0)
            for obj in self.objects
        )

    @property
    def conflict_count(self) -> int:
        """
        Number of semantic conflicts.

        Will later be connected to ConstraintValidator.
        """

        return 0

    def add_object(
        self,
        obj: SemanticObject,
    ) -> None:
        self.objects.append(obj)

    def clear(self) -> None:
        self.objects.clear()

    def __len__(self) -> int:
        return self.count

    def __bool__(self) -> bool:
        return self.count > 0


@dataclass(slots=True)
class ProjectRecoveryResult:
    """
    Result produced by ProjectRecoveryPipeline.
    """

    project: Project | None = None

    valid: bool = False

    errors: list[str] = field(
        default_factory=list,
    )

    metadata: Metadata = field(
        default_factory=dict,
    )

    @property
    def success(self) -> bool:
        """
        Return True if reconstruction succeeded.
        """

        return (
            self.valid
            and self.project is not None
        )

    def add_error(
        self,
        message: str,
    ) -> None:

        self.errors.append(message)
        self.valid = False

    def clear_errors(self) -> None:
        self.errors.clear()

    def __bool__(self) -> bool:
        return self.success


@dataclass(slots=True)
class FullRecoveryResult:
    """
    Result returned by FullRecoveryPipeline.
    """

    binary: BinaryAnalysisResult = field(
        default_factory=BinaryAnalysisResult,
    )

    semantic: SemanticRecoveryResult = field(
        default_factory=SemanticRecoveryResult,
    )

    project: ProjectRecoveryResult = field(
        default_factory=ProjectRecoveryResult,
    )

    metadata: Metadata = field(
        default_factory=dict,
    )

    @property
    def success(self) -> bool:
        """
        Global recovery status.
        """

        return self.project.success

    def __bool__(self) -> bool:
        return self.success