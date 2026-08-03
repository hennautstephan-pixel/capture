from capture_recovery.research import (
    CorpusKnowledgeBase,
    CorpusKnowledgeEntry,
)

from capture_recovery.tools import (
    DiffAnalysis,
    DiffRegion,
    IntelligentObjectIdentifier,
)


def test_intelligent_identifier_uses_corpus():

    knowledge = CorpusKnowledgeBase()

    knowledge.add_knowledge(
        CorpusKnowledgeEntry(
            category="fixture",
            description="Large block added",
            confidence=0.9,
        )
    )

    analysis = DiffAnalysis(
        regions=(
            DiffRegion(
                start_offset=100,
                end_offset=1200,
                differences=(),
            ),
        ),
    )

    identifier = IntelligentObjectIdentifier()

    result = identifier.identify(
        analysis,
        knowledge,
    )

    assert result.candidate_count == 1

    candidate = result.candidates[0]

    assert candidate.object_type == "fixture"
    assert candidate.confidence > 0
    assert candidate.offset == 100