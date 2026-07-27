"""
Convert structure changes into semantic changes.
"""

from __future__ import annotations

from capture_recovery.diff.models import SemanticChange
from capture_recovery.diff.models import StructureChange


class SemanticDiffer:
    """
    Convert structure-level modifications into semantic changes.
    """

    def compare(
        self,
        changes: list[StructureChange] | tuple[StructureChange, ...],
    ) -> tuple[SemanticChange, ...]:

        semantic: list[SemanticChange] = []

        for change in changes:

            before = change.structure_before
            after = change.structure_after

            object_type = (
                after.name
                if after is not None
                else before.name
                if before is not None
                else "Structure"
            )

            object_identifier = change.offset

            if before is None:
                semantic.append(
                    SemanticChange(
                        offset=change.offset,
                        object_type=object_type,
                        object_identifier=object_identifier,
                        property_name="structure",
                        before=None,
                        after="added",
                        confidence=change.confidence,
                    )
                )
                continue

            if after is None:
                semantic.append(
                    SemanticChange(
                        offset=change.offset,
                        object_type=object_type,
                        object_identifier=object_identifier,
                        property_name="structure",
                        before="present",
                        after=None,
                        confidence=change.confidence,
                    )
                )
                continue

            for property_name in change.changed_fields:

                semantic.append(
                    SemanticChange(
                        offset=change.offset,
                        object_type=object_type,
                        object_identifier=object_identifier,
                        property_name=property_name,
                        before=getattr(before, property_name, None),
                        after=getattr(after, property_name, None),
                        confidence=change.confidence,
                    )
                )

        return tuple(semantic)