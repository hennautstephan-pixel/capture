from capture_recovery.research import (
    ClassificationResult,
    CorpusClassifier,
    CorpusKnowledgeBase,
    CorpusKnowledgeEntry,
)

from capture_recovery.tools import (
    DiffRegion,
)


def test_classifier_uses_corpus():

    database = CorpusKnowledgeBase()

    database.add_knowledge(
        CorpusKnowledgeEntry(
            category="fixture",
            description="Large block added",
            confidence=0.9,
        )
    )

    region = DiffRegion(
        start_offset=100,
        end_offset=1200,
        differences=(),
    )

    classifier = CorpusClassifier()

    result = classifier.classify(
        region,
        database,
    )

    assert isinstance(
        result,
        ClassificationResult,
    )

    assert result.category == "fixture"

    assert result.confidence > 0