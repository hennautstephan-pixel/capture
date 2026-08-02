from capture_recovery.hypothesis import (
    ScoreRule,
)

from capture_recovery.models import (
    Detection,
    DataType,
)

from capture_recovery.structures import (
    Cluster,
    StructureCandidate,
)


def detection(offset):

    return Detection(
        offset=offset,
        length=4,
        datatype=DataType.INT32,
        value=offset,
    )


def candidate(score):

    cluster = Cluster(
        (
            detection(0),
            detection(4),
            detection(8),
        )
    )

    c = StructureCandidate(cluster)

    c.score = score
    c.confidence = score

    return c


def test_name():

    rule = ScoreRule()

    assert rule.name == "score"


def test_priority():

    rule = ScoreRule()

    assert rule.priority == 100


def test_structure():

    result = ScoreRule().apply(
        candidate(95),
    )

    assert len(result) == 1

    assert result[0].object_type == "Structure"


def test_possible_structure():

    result = ScoreRule().apply(
        candidate(80),
    )

    assert len(result) == 1

    assert (
        result[0].object_type
        ==
        "PossibleStructure"
    )


def test_low_score():

    result = ScoreRule().apply(
        candidate(20),
    )

    assert result == []


def test_confidence():

    result = ScoreRule().apply(
        candidate(98),
    )

    assert result[0].confidence == 98


def test_source():

    result = ScoreRule().apply(
        candidate(95),
    )

    assert result[0].source == "score"