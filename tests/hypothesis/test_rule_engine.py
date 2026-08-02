from capture_recovery.hypothesis import (
    Hypothesis,
    RuleEngine,
)

from capture_recovery.models import (
    DataType,
    Detection,
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
        )
    )

    c = StructureCandidate(cluster)

    c.score = score
    c.confidence = score

    return c


class DummyRule:

    @property
    def name(self):
        return "dummy"

    @property
    def priority(self):
        return 500

    def apply(
        self,
        candidate,
    ):
        return [
            Hypothesis(
                object_type="Dummy",
                confidence=100,
                candidate=candidate,
                source="dummy",
            )
        ]


def test_create():

    engine = RuleEngine()

    assert engine.count >= 1


def test_add():

    engine = RuleEngine()

    engine.add(
        DummyRule(),
    )

    assert engine.count >= 2


def test_clear():

    engine = RuleEngine()

    engine.clear()

    assert engine.count == 0


def test_rules_property():

    engine = RuleEngine()

    assert isinstance(
        engine.rules,
        tuple,
    )


def test_apply():

    engine = RuleEngine(
        (
            DummyRule(),
        )
    )

    result = engine.apply(
        candidate(50),
    )

    assert len(result) == 1


def test_callable():

    engine = RuleEngine(
        (
            DummyRule(),
        )
    )

    result = engine(
        candidate(50),
    )

    assert len(result) == 1


def test_best():

    engine = RuleEngine(
        (
            DummyRule(),
        )
    )

    result = engine.apply(
        candidate(50),
    )

    assert (
        result.best().object_type
        ==
        "Dummy"
    )