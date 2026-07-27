"""
Compare reconstructed fields.
"""

from __future__ import annotations

from capture_recovery.structures.field import Field

from .models import FieldChange


class FieldDiffer:
    """
    Compare two collections of reconstructed fields.
    """

    def compare(
        self,
        before: list[Field],
        after: list[Field],
    ) -> tuple[FieldChange, ...]:
        """
        Compare two field collections.

        Fields are matched using their offset.

        Returns
        -------
        tuple[FieldChange, ...]
            Sorted tuple of detected changes.
        """

        before_index = {
            field.offset: field
            for field in before
        }

        after_index = {
            field.offset: field
            for field in after
        }

        offsets = sorted(
            set(before_index) | set(after_index)
        )

        changes: list[FieldChange] = []

        for offset in offsets:

            before_field = before_index.get(offset)
            after_field = after_index.get(offset)

            if before_field is None:
                changes.append(
                    FieldChange(
                        offset=offset,
                        field_before=None,
                        field_after=after_field,
                        changed_properties=("added",),
                    )
                )
                continue

            if after_field is None:
                changes.append(
                    FieldChange(
                        offset=offset,
                        field_before=before_field,
                        field_after=None,
                        changed_properties=("removed",),
                    )
                )
                continue

            properties = self._changed_properties(
                before_field,
                after_field,
            )

            if properties:
                changes.append(
                    FieldChange(
                        offset=offset,
                        field_before=before_field,
                        field_after=after_field,
                        changed_properties=properties,
                    )
                )

        return tuple(changes)

    @staticmethod
    def _changed_properties(
        before: Field,
        after: Field,
    ) -> tuple[str, ...]:
        """
        Return modified properties.
        """

        changed: list[str] = []

        if before.name != after.name:
            changed.append("name")

        if before.length != after.length:
            changed.append("length")

        if before.datatype != after.datatype:
            changed.append("datatype")

        if before.value != after.value:
            changed.append("value")

        if before.confidence != after.confidence:
            changed.append("confidence")

        if before.metadata != after.metadata:
            changed.append("metadata")

        return tuple(changed)