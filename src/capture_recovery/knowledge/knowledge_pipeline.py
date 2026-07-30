from __future__ import annotations

from collections.abc import Iterable

from capture_recovery.models.project import Project
from capture_recovery.structures.structure import Structure

from .knowledge_registry import KnowledgeRegistry
from .semantic_object import SemanticObject
from .signature_engine import SignatureEngine


class KnowledgePipeline:
    """
    Pipeline responsible for transforming reconstructed binary structures
    into semantic objects.

    Processing steps:

        Structures
            │
            ▼
        SignatureEngine
            │
            ▼
        KnowledgeRegistry
            │
            ▼
        SemanticObjects
            │
            ▼
        Project
    """

    def __init__(
        self,
        signature_engine: SignatureEngine,
        registry: KnowledgeRegistry,
    ) -> None:
        self._signature_engine = signature_engine
        self._registry = registry

    def process(
        self,
        structures: Iterable[Structure],
    ) -> Project:
        """
        Decode every recognized structure into a Project.
        """

        project = Project()

        for structure in structures:

            match = self._signature_engine.match(structure)

            if match is None:
                continue

            decoder = self._registry.get(match.signature.name)

            if decoder is None:
                continue

            semantic_object = decoder.decode(
                structure,
                match,
            )

            if semantic_object is None:
                continue

            project.add(semantic_object)

        return project

    def decode(
        self,
        structures: Iterable[Structure],
    ) -> list[SemanticObject]:
        """
        Decode structures into semantic objects.
        """

        project = self.process(structures)

        return list(project)

    def __call__(
        self,
        structures: Iterable[Structure],
    ) -> Project:
        return self.process(structures)