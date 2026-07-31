from capture_recovery.discovery import (
    KnowledgeEntry,
    PropertyCandidate,
    ValueType,
)


def make_candidate() -> PropertyCandidate:

    return PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type=ValueType.FLOAT32,
        confidence=1.0,
        observations=4,
    )


def test_from_candidate():

    candidate = make_candidate()

    entry = KnowledgeEntry.from_candidate(candidate)

    assert entry.object_type == "Fixture"
    assert entry.property_name == "Position.X"
    assert entry.offset == 0x184
    assert entry.value_type is ValueType.FLOAT32
    assert entry.confidence == 1.0
    assert entry.observations == 4
    assert entry.confirmations == 1
    assert entry.contradictions == 0


def test_identifier():

    entry = KnowledgeEntry.from_candidate(
        make_candidate()
    )

    assert (
        entry.identifier
        == "Fixture:388:Position.X"
    )


def test_is_confirmed():

    entry = KnowledgeEntry.from_candidate(
        make_candidate()
    )

    assert entry.is_confirmed is True


def test_confidence_percent():

    candidate = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type=ValueType.FLOAT32,
        confidence=0.95,
        observations=4,
    )

    entry = KnowledgeEntry.from_candidate(candidate)

    assert entry.confidence_percent == 95.0


def test_confirm():

    entry = KnowledgeEntry.from_candidate(
        make_candidate()
    )

    updated = entry.confirm(
        make_candidate()
    )

    assert updated.confirmations == 2
    assert updated.contradictions == 0
    assert updated.observations == 8
    assert updated.confidence == 1.0

    assert entry.confirmations == 1


def test_contradict():

    entry = KnowledgeEntry.from_candidate(
        make_candidate()
    )

    updated = entry.contradict()

    assert updated.confirmations == 1
    assert updated.contradictions == 1
    assert updated.confidence < entry.confidence

    assert updated.is_confirmed is False

    assert entry.contradictions == 0


def test_entry_is_immutable():

    entry = KnowledgeEntry.from_candidate(
        make_candidate()
    )

    try:
        entry.confidence = 0.5
        immutable = False
    except Exception:
        immutable = True

    assert immutable


def test_multiple_confirmations():

    entry = KnowledgeEntry.from_candidate(
        make_candidate()
    )

    entry = entry.confirm(make_candidate())
    entry = entry.confirm(make_candidate())
    entry = entry.confirm(make_candidate())

    assert entry.confirmations == 4
    assert entry.observations == 16
    assert entry.contradictions == 0
    assert entry.confidence == 1.0


def test_multiple_contradictions():

    entry = KnowledgeEntry.from_candidate(
        make_candidate()
    )

    entry = entry.contradict()
    entry = entry.contradict()

    assert entry.confirmations == 1
    assert entry.contradictions == 2
    assert entry.confidence < 1.0