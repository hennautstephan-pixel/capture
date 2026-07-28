"""
Relation resolver.

Provides high level queries
on relation graphs.
"""

from __future__ import annotations

from .relation_graph import (
    RelationGraph,
)


class RelationResolver:
    """
    Resolve semantic relations.
    """

    def __init__(
        self,
        graph: RelationGraph,
    ) -> None:

        self.graph = graph


    def find_parent(
        self,
        object_id: str,
    ) -> str | None:
        """
        Find parent object.
        """

        for relation in self.graph.find_from(
            object_id,
        ):

            if relation.relation_type == "child_of":

                return relation.target

        return None


    def find_structure(
        self,
        object_id: str,
    ) -> str | None:
        """
        Find mounting structure.
        """

        for relation in self.graph.find_from(
            object_id,
        ):

            if relation.relation_type == "mounted_on":

                return relation.target

        return None


    def find_children(
        self,
        object_id: str,
    ) -> list[str]:
        """
        Find children objects.
        """

        return [
            relation.source
            for relation in self.graph.find_to(
                object_id,
            )
            if relation.relation_type == "child_of"
        ]