"""
Relation builder.

Detects semantic relationships between
recovered Capture objects.
"""

from __future__ import annotations

from .object_relation import (
    ObjectRelation,
)


class RelationBuilder:
    """
    Builds relationships between semantic objects.
    """

    def build(
        self,
        objects,
    ) -> list[ObjectRelation]:
        """
        Analyze semantic objects and create relations.
        """

        relations: list[ObjectRelation] = []

        for obj in objects:

            properties = obj.properties or {}

            identifier = str(
                obj.identifier,
            )

            # Parent hierarchy relation
            parent = properties.get(
                "parent",
            )

            if parent:

                relations.append(
                    ObjectRelation(
                        source=identifier,

                        target=str(
                            parent,
                        ),

                        relation_type="child_of",
                    )
                )

            # Mounting relation
            structure_id = properties.get(
                "structure_id",
            )

            if structure_id:

                relations.append(
                    ObjectRelation(
                        source=identifier,

                        target=str(
                            structure_id,
                        ),

                        relation_type="mounted_on",
                    )
                )

            # Focus relation
            focus_point = properties.get(
                "focus_point",
            )

            if focus_point:

                relations.append(
                    ObjectRelation(
                        source=identifier,

                        target=str(
                            focus_point,
                        ),

                        relation_type="focuses",
                    )
                )

            # Group relation
            group = properties.get(
                "group",
            )

            if group:

                relations.append(
                    ObjectRelation(
                        source=identifier,

                        target=str(
                            group,
                        ),

                        relation_type="belongs_to",
                    )
                )

        return relations