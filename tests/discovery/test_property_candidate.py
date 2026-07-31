from capture_recovery.discovery import (
    PropertyCandidate,
    PropertyConstraint,
    ValueType,
)


def make_candidate(**kwargs):

    defaults = dict(
        object_type="Fixture",
        property_name="Intensity",
        offset=0x20,
        value_type=ValueType.INT32,
        confidence=0.98,
        observations=10,
    )

    defaults.update(kwargs)

    return PropertyCandidate(**defaults)


def test_default_constraints():

    candidate = make_candidate()

    assert candidate.constraints == ()


def test_constraints_are_stored():

    constraint = PropertyConstraint()

    candidate = make_candidate(
        constraints=(constraint,),
    )

    assert candidate.constraints == (constraint,)


def test_multiple_constraints():

    c1 = PropertyConstraint()
    c2 = PropertyConstraint()

    candidate = make_candidate(
        constraints=(c1, c2),
    )

    assert len(candidate.constraints) == 2


def test_is_immutable():

    candidate = make_candidate()

    try:
        candidate.confidence = 0.5
    except Exception:
        return

    assert False, "PropertyCandidate must be immutable"