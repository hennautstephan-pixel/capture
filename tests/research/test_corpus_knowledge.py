from pathlib import Path

from capture_recovery.research import (
    CorpusKnowledgeBase,
    CorpusSample,
    CorpusKnowledgeEntry,
)


def test_add_sample():

    database = CorpusKnowledgeBase()

    sample = CorpusSample(
        name="1 projecteur",
        path=Path("samples/1 projecteur.c2p"),
        category="fixture",
    )

    database.add_sample(
        sample,
    )

    assert len(database.samples()) == 1

    assert database.samples()[0].category == "fixture"


def test_add_knowledge():

    database = CorpusKnowledgeBase()

    entry = CorpusKnowledgeEntry(
        category="fixture",
        description="Large block added",
        confidence=0.8,
    )

    database.add_knowledge(
        entry,
    )

    result = database.find_by_category(
        "fixture",
    )

    assert len(result) == 1

    assert result[0].confidence == 0.8