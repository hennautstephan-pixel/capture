"""
Analysis package.

Contains semantic analysis,
object relations and relation graphs.
"""

from .object_relation import (
    ObjectRelation,
)

from .relation_builder import (
    RelationBuilder,
)

from .relation_graph import (
    RelationGraph,
)

from .relation_resolver import (
    RelationResolver,
)


__all__ = [

    "ObjectRelation",

    "RelationBuilder",

    "RelationGraph",

    "RelationResolver",
]