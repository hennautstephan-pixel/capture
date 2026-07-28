"""
Relation graph.

Stores and queries semantic object relations.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .object_relation import (
    ObjectRelation,
)


@dataclass
class RelationGraph:
    """
    Directed graph of object relations.
    """

    relations: list[ObjectRelation] = field(
        default_factory=list,
    )

    def add(
        self,
        relation: ObjectRelation,
    ) -> None:
        """
        Add a relation.
        """

        self.relations.append(
            relation,
        )


    def find_from(
        self,
        source: str,
    ) -> list[ObjectRelation]:
        """
        Find relations starting from object.
        """

        return [
            relation
            for relation in self.relations
            if relation.source == source
        ]


    def find_to(
        self,
        target: str,
    ) -> list[ObjectRelation]:
        """
        Find relations pointing to object.
        """

        return [
            relation
            for relation in self.relations
            if relation.target == target
        ]


    def find_type(
        self,
        relation_type: str,
    ) -> list[ObjectRelation]:
        """
        Find relations by type.
        """

        return [
            relation
            for relation in self.relations
            if relation.relation_type == relation_type
        ]