"""
Project builder.

Transforms semantic objects into a reconstructed project.
"""

from __future__ import annotations

from collections.abc import Iterable

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.models.project import Project


class ProjectBuilder:
    """
    Build a Project from decoded semantic objects.
    """

    def __init__(
        self,
        name: str = "Recovered Project",
    ) -> None:
        self.name = name

    def build(
        self,
        objects: Iterable[SemanticObject],
    ) -> Project:
        """
        Create a project from semantic objects.
        """

        project = Project(
            name=self.name,
        )

        project.extend(
            objects,
        )

        return project

    def add(
        self,
        project: Project,
        obj: SemanticObject,
    ) -> Project:
        """
        Add a semantic object to an existing project.
        """

        project.add(
            obj,
        )

        return project

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name={self.name!r})"
        )