from __future__ import annotations

import json

from pathlib import Path

from .corpus_knowledge import (
    CorpusKnowledgeBase,
    CorpusKnowledgeEntry,
    CorpusSample,
)


class CorpusLoader:
    """
    Load a CorpusKnowledgeBase from JSON.
    """

    def load(
        self,
        input_file: str | Path,
    ) -> CorpusKnowledgeBase:
        """
        Restore a knowledge base from JSON.
        """

        source = Path(
            input_file,
        )

        if not source.exists():

            raise FileNotFoundError(
                source,
            )

        data = json.loads(
            source.read_text(
                encoding="utf-8",
            )
        )

        knowledge_base = CorpusKnowledgeBase()

        for sample_data in data.get(
            "samples",
            [],
        ):

            knowledge_base.add_sample(
                CorpusSample(
                    name=sample_data["name"],
                    path=Path(
                        sample_data["path"],
                    ),
                    category=sample_data["category"],
                )
            )


        for entry_data in data.get(
            "knowledge",
            [],
        ):

            knowledge_base.add_knowledge(
                CorpusKnowledgeEntry(
                    category=entry_data["category"],
                    description=entry_data["description"],
                    confidence=entry_data["confidence"],
                )
            )

        return knowledge_base