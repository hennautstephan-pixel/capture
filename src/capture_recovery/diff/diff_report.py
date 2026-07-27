@dataclass(frozen=True, slots=True)
class DiffReport:
    """
    Complete immutable diff report.

    This is the main output produced by the diff engine.
    """

    metadata: DiffMetadata

    statistics: DiffStatistics

    binary_changes: tuple[BinaryChange, ...] = ()

    region_changes: tuple[RegionChange, ...] = ()

    structure_changes: tuple[StructureChange, ...] = ()

    semantic_changes: tuple[SemanticChange, ...] = ()

    def is_empty(self) -> bool:
        """
        Returns True if no changes have been detected.
        """
        return (
            not self.binary_changes
            and not self.region_changes
            and not self.structure_changes
            and not self.semantic_changes
        )

    @property
    def total_changes(self) -> int:
        """
        Returns the total number of detected changes.
        """
        return (
            len(self.binary_changes)
            + len(self.region_changes)
            + len(self.structure_changes)
            + len(self.semantic_changes)
        )

    def summary(self) -> str:
        """
        Returns a human-readable summary.
        """
        return (
            f"{len(self.binary_changes)} binary changes, "
            f"{len(self.region_changes)} region changes, "
            f"{len(self.structure_changes)} structure changes, "
            f"{len(self.semantic_changes)} semantic changes"
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the report into a serializable dictionary.
        """
        return {
            "metadata": self.metadata.to_dict(),
            "statistics": {
                "bytes_added": self.statistics.bytes_added,
                "bytes_removed": self.statistics.bytes_removed,
                "bytes_modified": self.statistics.bytes_modified,
                "binary_changes": self.statistics.binary_changes,
                "region_changes": self.statistics.region_changes,
                "structure_changes": self.statistics.structure_changes,
                "semantic_changes": self.statistics.semantic_changes,
                "total_changes": self.statistics.total_changes,
            },
            "binary_changes": [
                {
                    "offset": c.offset,
                    "change_type": c.change_type.value,
                    "before": c.before.hex(),
                    "after": c.after.hex(),
                    "confidence": c.confidence,
                }
                for c in self.binary_changes
            ],
            "region_changes": [
                {
                    "offset": c.offset,
                    "region": str(c.region),
                    "confidence": c.confidence,
                }
                for c in self.region_changes
            ],
            "structure_changes": [
                {
                    "offset": c.offset,
                    "before": str(c.structure_before),
                    "after": str(c.structure_after),
                    "changed_fields": list(c.changed_fields),
                    "confidence": c.confidence,
                }
                for c in self.structure_changes
            ],
            "semantic_changes": [
                {
                    "offset": c.offset,
                    "object_type": c.object_type,
                    "object_identifier": c.object_identifier,
                    "property_name": c.property_name,
                    "before": c.before,
                    "after": c.after,
                    "confidence": c.confidence,
                }
                for c in self.semantic_changes
            ],
        }

    def __len__(self) -> int:
        """
        Number of detected changes.
        """
        return self.total_changes

    def __bool__(self) -> bool:
        """
        False when no changes are present.
        """
        return not self.is_empty()

    def __iter__(self):
        """
        Iterate over every change in the report.
        """
        yield from self.binary_changes
        yield from self.region_changes
        yield from self.structure_changes
        yield from self.semantic_changes

    def binary_at(self, offset: int) -> BinaryChange | None:
        """
        Returns the binary change at the specified offset.
        """
        for change in self.binary_changes:
            if change.offset == offset:
                return change
        return None

    def semantic_of_type(
        self,
        object_type: str,
    ) -> tuple[SemanticChange, ...]:
        """
        Returns all semantic changes of a given object type.
        """
        return tuple(
            change
            for change in self.semantic_changes
            if change.object_type == object_type
        )

    def filter_confidence(
        self,
        minimum: float,
    ) -> "DiffReport":
        """
        Returns a filtered report.
        """
        return DiffReport(
            metadata=self.metadata,
            statistics=self.statistics,
            binary_changes=tuple(
                c
                for c in self.binary_changes
                if c.confidence >= minimum
            ),
            region_changes=tuple(
                c
                for c in self.region_changes
                if c.confidence >= minimum
            ),
            structure_changes=tuple(
                c
                for c in self.structure_changes
                if c.confidence >= minimum
            ),
            semantic_changes=tuple(
                c
                for c in self.semantic_changes
                if c.confidence >= minimum
            ),
        )