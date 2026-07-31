from capture_recovery.discovery import (
    DiscoveryKnowledgeBase,
    PropertyCandidate,
    ValueType,
)


def make_candidate(
    *,
    property_name="Position.X",
    offset=0x184,
    confidence=1.0,
    observations=4,
):
    return PropertyCandidate(
        object_type="Fixture",
        property_name=property_name,
        offset=offset,
        value_type=ValueType.FLOAT32,
        confidence=confidence,
        observations=observations,
    )


def test_empty():

    knowledge = DiscoveryKnowledgeBase()

    assert len(knowledge) == 0
    assert knowledge.total_entries == 0
    assert knowledge.total_observations == 0
    assert knowledge.average_confidence == 0.0


def test_add():

    knowledge = DiscoveryKnowledgeBase()

    entry = knowledge.add(
        make_candidate()
    )

    assert len(knowledge) == 1
    assert knowledge.total_entries == 1

    assert entry.object_type == "Fixture"
    assert entry.property_name == "Position.X"


def test_add_same_candidate_updates():

    knowledge = DiscoveryKnowledgeBase()

    knowledge.add(make_candidate())
    knowledge.add(make_candidate())

    assert knowledge.total_entries == 1

    entry = next(iter(knowledge))

    assert entry.confirmations == 2
    assert entry.observations == 8


def test_contains():

    knowledge = DiscoveryKnowledgeBase()

    entry = knowledge.add(
        make_candidate()
    )

    assert entry.identifier in knowledge


def test_find():

    knowledge = DiscoveryKnowledgeBase()

    entry = knowledge.add(
        make_candidate()
    )

    found = knowledge.find(
        entry.identifier
    )

    assert found == entry


def test_find_unknown():

    knowledge = DiscoveryKnowledgeBase()

    assert knowledge.find("unknown") is None


def test_by_object():

    knowledge = DiscoveryKnowledgeBase()

    knowledge.add(make_candidate())

    results = knowledge.by_object(
        "Fixture"
    )

    assert len(results) == 1


def test_by_name():

    knowledge = DiscoveryKnowledgeBase()

    knowledge.add(
        make_candidate(
            property_name="Rotation.Z"
        )
    )

    results = knowledge.by_name(
        "Rotation.Z"
    )

    assert len(results) == 1


def test_by_offset():

    knowledge = DiscoveryKnowledgeBase()

    knowledge.add(
        make_candidate(offset=512)
    )

    results = knowledge.by_offset(512)

    assert len(results) == 1


def test_total_observations():

    knowledge = DiscoveryKnowledgeBase()

    knowledge.add(
        make_candidate(observations=10)
    )

    knowledge.add(
        make_candidate(
            property_name="Rotation.Z",
            observations=5,
        )
    )

    assert knowledge.total_observations == 15


def test_average_confidence():

    knowledge = DiscoveryKnowledgeBase()

    knowledge.add(
        make_candidate(confidence=1.0)
    )

    knowledge.add(
        make_candidate(
            property_name="Rotation.Z",
            confidence=0.5,
        )
    )

    assert knowledge.average_confidence == 0.75


def test_iteration():

    knowledge = DiscoveryKnowledgeBase()

    knowledge.add(make_candidate())

    entries = list(knowledge)

    assert len(entries) == 1


def test_merge():

    left = DiscoveryKnowledgeBase()
    right = DiscoveryKnowledgeBase()

    left.add(make_candidate())

    right.add(
        make_candidate(
            property_name="Rotation.Z"
        )
    )

    left.merge(right)

    assert left.total_entries == 2