"""
Compare reconstructed structures.
"""

from __future__ import annotations

from capture_recovery.diff.field_differ import FieldDiffer
from capture_recovery.diff.models import StructureChange
from capture_recovery.structures.structure import Structure


class StructureDiffer:
    """
    Compare reconstructed structures.
    """

    def __init__(self) -> None:
        self._field_differ = FieldDiffer()

    def compare(
        self,
        before: list[Structure],
        after: list[Structure],
    ) -> tuple[StructureChange, ...]:
        """
        Compare two structure collections.
        """

        before_map = {s.offset: s for s in before}
        after_map = {s.offset: s for s in after}

        offsets = sorted(before_map.keys() | after_map.keys())

        changes: list[StructureChange] = []

        for offset in offsets:

            previous = before_map.get(offset)
            current = after_map.get(offset)

            if previous is None:
                changes.append(
                    StructureChange(
                        offset=offset,
                        structure_after=current,
                        changed_fields=("added",),
                    )
                )
                continue

            if current is None:
                changes.append(
                    StructureChange(
                        offset=offset,
                        structure_before=previous,
                        changed_fields=("removed",),
                    )
                )
                continue

            changed = self._changed_properties(previous, current)

            if changed:
                changes.append(
                    StructureChange(
                        offset=offset,
                        structure_before=previous,
                        structure_after=current,
                        changed_fields=tuple(changed),
                    )
                )

        return tuple(changes)

    def _changed_properties(
        self,
        before: Structure,
        after: Structure,
    ) -> list[str]:
        """
        Return modified structure properties.
        """

        changed: list[str] = []

        if before.name != after.name:
            changed.append("name")

        if before.length != after.length:
            changed.append("length")

        if before.confidence != after.confidence:
            changed.append("confidence")

        if before.metadata != after.metadata:
            changed.append("metadata")

        field_changes = self._field_differ.compare(
            before.fields,
            after.fields,
        )

        if field_changes:
            changed.append("fields")

        return changed