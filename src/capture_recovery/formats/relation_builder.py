"""
Relation builder.

Detects relationships between
semantic objects.
"""

from __future__ import annotations

from .object_relation import (
    ObjectRelation,
)


class RelationBuilder:
    """
    Build object relations.
    """

    def build(
        self,
        objects,
    ) -> list[ObjectRelation]:
        """
        Analyze objects and create relations.
        """

        relations = []

        for obj in objects:

            properties = obj.properties

            parent = properties.get(
                "parent",
            )

            if parent:

                relations.append(
                    ObjectRelation(
                        source=str(
                            obj.identifier,
                        ),

                        target=str(
                            parent,
                        ),

                        relation_type="child_of",
                    )
                )


            structure = properties.get(
                "structure_id",
            )

            if structure:

                relations.append(
                    ObjectRelation(
                        source=str(
                            obj.identifier,
                        ),

                        target=str(
                            structure,
                        ),

                        relation_type="mounted_on",
                    )
                )


            focus = properties.get(
                "focus_point",
            )

            if focus:

                relations.append(
                    ObjectRelation(
                        source=str(
                            obj.identifier,
                        ),

                        target=str(
                            focus,
                        ),

                        relation_type="focuses",
                    )
                )

        return relations