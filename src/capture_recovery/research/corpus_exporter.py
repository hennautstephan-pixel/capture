from __future__ import annotations

import json

from pathlib import Path

from .corpus_knowledge import (
    CorpusKnowledgeBase,
)


class CorpusExporter:
    """
    Export corpus knowledge to JSON files.
    """

    def export(
        self,
        knowledge_base: CorpusKnowledgeBase,
        output_file: str | Path,
    ) -> Path:
        """
        Export a CorpusKnowledgeBase into JSON.
        """

        destination = Path(
            output_file,
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = {
            "samples": [
                {
                    "name": sample.name,
                    "path": str(sample.path),
                    "category": sample.category,
                }
                for sample in knowledge_base.samples()
            ],
            "knowledge": [
                {
                    "category": entry.category,
                    "description": entry.description,
                    "confidence": entry.confidence,
                }
                for entry in knowledge_base.knowledge()
            ],
        }

        destination.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return destination