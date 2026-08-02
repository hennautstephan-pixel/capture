from pathlib import Path

from capture_recovery.research import (
    CorpusExporter,
    CorpusKnowledgeBase,
    CorpusKnowledgeEntry,
    CorpusSample,
)


def test_export_corpus(tmp_path):

    database = CorpusKnowledgeBase()

    database.add_sample(
        CorpusSample(
            name="test",
            path=Path("sample.c2p"),
            category="fixture",
        )
    )

    database.add_knowledge(
        CorpusKnowledgeEntry(
            category="object",
            description="fixture added",
            confidence=0.9,
        )
    )

    output = tmp_path / "corpus.json"

    exporter = CorpusExporter()

    result = exporter.export(
        database,
        output,
    )

    assert result.exists()

    content = result.read_text(
        encoding="utf-8",
    )

    assert "fixture added" in content