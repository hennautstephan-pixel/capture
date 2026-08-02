from pathlib import Path

from capture_recovery.research import (
    CorpusExporter,
    CorpusLoader,
    CorpusKnowledgeBase,
    CorpusKnowledgeEntry,
    CorpusSample,
)


def test_load_corpus(tmp_path):

    database = CorpusKnowledgeBase()

    database.add_sample(
        CorpusSample(
            name="projecteur",
            path=Path(
                "projecteur.c2p",
            ),
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

    file = tmp_path / "corpus.json"

    CorpusExporter().export(
        database,
        file,
    )

    loaded = CorpusLoader().load(
        file,
    )

    assert len(
        loaded.samples(),
    ) == 1

    assert len(
        loaded.knowledge(),
    ) == 1

    assert (
        loaded.knowledge()[0].category
        == "object"
    )