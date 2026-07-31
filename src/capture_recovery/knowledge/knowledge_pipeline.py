from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.models.project import Project
from capture_recovery.reverse.semantic_diff import SemanticDiff, SemanticDiffEngine
from capture_recovery.reverse.semantic_pattern_analyzer import PatternReport, SemanticPatternAnalyzer
from capture_recovery.structures.structure import Structure

from .knowledge_base import KnowledgeBase, KnowledgeSnapshot
from .knowledge_registry import KnowledgeRegistry
from .semantic_object import SemanticObject
from .signature_engine import SignatureEngine


class InspectorProtocol(Protocol):
    """Protocol for components that inspect binary data into recovered values."""

    def inspect(self, data: bytes) -> list[RecoveredValue]:
        """Inspect a file payload and return recovered values."""


@dataclass(frozen=True, slots=True)
class KnowledgePipelineResult:
    """Result produced after building a knowledge snapshot from a corpus."""

    snapshot: KnowledgeSnapshot
    files_processed: int
    reports_processed: int
    statistics: Mapping[str, int | float]


class KnowledgePipeline:
    """Coordinate the semantic-learning chain over a corpus of Capture files."""

    def __init__(
        self,
        inspector: InspectorProtocol | None = None,
        diff_engine: SemanticDiffEngine | None = None,
        pattern_analyzer: SemanticPatternAnalyzer | None = None,
        knowledge_base: KnowledgeBase | None = None,
        signature_engine: SignatureEngine | None = None,
        registry: KnowledgeRegistry | None = None,
    ) -> None:
        """Initialize the pipeline with injected dependencies.

        The constructor supports both the existing structure-decoding pipeline and
        the new semantic-learning workflow so that current behavior remains
        available while the new orchestration path can be used in tests.
        """
        self._signature_engine = signature_engine
        self._registry = registry
        self._inspector = inspector
        self._diff_engine = diff_engine
        self._pattern_analyzer = pattern_analyzer
        self._knowledge_base = knowledge_base

    def build(self, corpus: Iterable[bytes]) -> KnowledgePipelineResult:
        """Build a knowledge snapshot from a corpus of file payloads.

        The method is intentionally an orchestrator only: it forwards each file
        through inspection, semantic diffing, pattern analysis, and knowledge
        ingestion without adding any heuristics or Capture-specific logic.
        """
        if self._inspector is None or self._diff_engine is None or self._pattern_analyzer is None or self._knowledge_base is None:
            raise ValueError("KnowledgePipeline build requires inspector, diff_engine, pattern_analyzer, and knowledge_base")

        files = list(corpus)
        reports: list[PatternReport] = []
        diffs: list[SemanticDiff] = []
        knowledge_base = self._knowledge_base

        for file_bytes in files:
            recovered_values = self._inspector.inspect(file_bytes)
            diff = self._diff_engine.compare([], recovered_values)
            diffs.append(diff)
            report = self._pattern_analyzer.analyze([diff])
            reports.append(report)
            knowledge_base.ingest(report)

        snapshot = knowledge_base.snapshot()
        statistics = {
            "files_processed": len(files),
            "semantic_diffs_generated": len(diffs),
            "reports_processed": len(reports),
            "knowledge_entries": len(snapshot.entries),
        }

        return KnowledgePipelineResult(
            snapshot=snapshot,
            files_processed=len(files),
            reports_processed=len(reports),
            statistics=statistics,
        )

    def process(
        self,
        structures: Iterable[Structure],
    ) -> Project:
        """Decode every recognized structure into a Project."""
        if self._signature_engine is None or self._registry is None:
            raise ValueError("KnowledgePipeline process requires signature_engine and registry")

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
        """Decode structures into semantic objects."""
        project = self.process(structures)
        return list(project)

    def __call__(
        self,
        structures: Iterable[Structure],
    ) -> Project:
        return self.process(structures)


__all__ = ["KnowledgePipeline", "KnowledgePipelineResult"]