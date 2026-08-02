from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.tools import (
    CompareAll,
    DiffAnalyzer,
)

from .corpus_knowledge import (
    CorpusKnowledgeBase,
    CorpusKnowledgeEntry,
    CorpusSample,
)


@dataclass(slots=True, frozen=True)
class CorpusBuildResult:
    """
    Result of corpus analysis.
    """

    sample_count: int

    comparison_count: int

    knowledge_count: int


class CorpusBuilder:
    """
    Build a knowledge base from Capture samples.
    """

    def __init__(self) -> None:

        self._comparer = CompareAll()

        self._diff_analyzer = DiffAnalyzer()


    def build(
        self,
        samples_directory: str | Path,
    ) -> tuple[
        CorpusKnowledgeBase,
        CorpusBuildResult,
    ]:
        """
        Analyse all samples from a directory.
        """

        directory = Path(
            samples_directory,
        )

        database = CorpusKnowledgeBase()

        samples = self._collect_samples(
            directory,
        )

        for sample in samples:

            database.add_sample(
                sample,
            )

        comparison_count = 0

        knowledge_count = 0

        for left, right in self._pairs(samples):

            comparison_count += 1

            result = self._comparer.compare(
                left.path,
                right.path,
            )

            analysis = self._diff_analyzer.analyze(
                result,
            )

            for region in analysis.regions:

                entry = CorpusKnowledgeEntry(
                    category=self._guess_category(
                        left,
                        right,
                        region.size,
                    ),
                    description=(
                        f"{left.name} -> {right.name} "
                        f"offset={region.start_offset} "
                        f"size={region.size}"
                    ),
                    confidence=self._confidence(
                        region.size,
                    ),
                )

                database.add_knowledge(
                    entry,
                )

                knowledge_count += 1

        return (
            database,
            CorpusBuildResult(
                sample_count=len(samples),
                comparison_count=comparison_count,
                knowledge_count=knowledge_count,
            ),
        )


    def _collect_samples(
        self,
        directory: Path,
    ) -> list[CorpusSample]:

        samples = []

        for file in sorted(
            directory.glob("*.c2p"),
        ):

            samples.append(
                CorpusSample(
                    name=file.stem,
                    path=file,
                    category="unknown",
                )
            )

        return samples


    def _pairs(
        self,
        samples: list[CorpusSample],
    ):

        for index, left in enumerate(samples):

            for right in samples[index + 1:]:

                yield left, right


    def _guess_category(
        self,
        left: CorpusSample,
        right: CorpusSample,
        size: int,
    ) -> str:
        """
        First heuristic classifier.
        """

        names = (
            left.name.lower()
            + " "
            + right.name.lower()
        )

        if "dmx" in names:

            return "dmx"

        if (
            "rotation" in names
            or "deplacement" in names
        ):

            return "transform"

        if "allume" in names:

            return "state"

        if size > 512:

            return "object"

        return "property"


    def _confidence(
        self,
        size: int,
    ) -> float:
        """
        Estimate confidence from region size.
        """

        if size > 2000:

            return 0.90

        if size > 512:

            return 0.75

        if size > 32:

            return 0.55

        return 0.35