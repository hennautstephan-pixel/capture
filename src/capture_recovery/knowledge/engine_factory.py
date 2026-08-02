"""
Knowledge engine factory.

Creates fully configured KnowledgeEngine instances.
"""

from __future__ import annotations

from capture_recovery.knowledge.knowledge_engine import (
    KnowledgeEngine,
)

from capture_recovery.knowledge.registry_builder import (
    build_default_registry,
)


def create_default_engine() -> KnowledgeEngine:
    """
    Create a KnowledgeEngine using the default decoder registry.
    """

    return KnowledgeEngine(
        build_default_registry(),
    )