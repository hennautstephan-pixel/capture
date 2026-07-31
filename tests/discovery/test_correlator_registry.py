from capture_recovery.discovery import (
    CorrelatorRegistry,
    NumericCorrelator,
    PropertyObservation,
)


class HighPriorityCorrelator(NumericCorrelator):
    PRIORITY = 100


class MediumPriorityCorrelator(NumericCorrelator):
    PRIORITY = 50


class LowPriorityCorrelator(NumericCorrelator):
    PRIORITY = 10


def make_registry():

    registry = CorrelatorRegistry()
    registry.register(NumericCorrelator())

    return registry


def make_observation():

    return PropertyObservation(
        object_type="Fixture",
        offset=0x184,
        semantic_property="Position.X",
        binary_before=10,
        binary_after=20,
        semantic_before=1.0,
        semantic_after=2.0,
    )


def test_empty_registry():

    registry = CorrelatorRegistry()

    assert len(registry) == 0
    assert not registry


def test_register():

    registry = CorrelatorRegistry()

    correlator = NumericCorrelator()

    registry.register(correlator)

    assert len(registry) == 1
    assert correlator in registry


def test_duplicate_registration_is_ignored():

    registry = CorrelatorRegistry()

    correlator = NumericCorrelator()

    registry.register(correlator)
    registry.register(correlator)

    assert len(registry) == 1


def test_unregister():

    registry = make_registry()

    correlator = next(iter(registry))

    registry.unregister(correlator)

    assert len(registry) == 0


def test_unregister_unknown_raises():

    registry = CorrelatorRegistry()

    correlator = NumericCorrelator()

    try:
        registry.unregister(correlator)
        assert False
    except ValueError:
        pass


def test_clear():

    registry = make_registry()

    registry.clear()

    assert len(registry) == 0


def test_correlators_property():

    registry = make_registry()

    correlators = registry.correlators

    assert isinstance(correlators, tuple)
    assert len(correlators) == 1


def test_iteration():

    registry = make_registry()

    correlators = list(registry)

    assert len(correlators) == 1
    assert isinstance(
        correlators[0],
        NumericCorrelator,
    )


def test_bool():

    assert not CorrelatorRegistry()
    assert make_registry()


def test_contains():

    registry = make_registry()

    correlator = next(iter(registry))

    assert correlator in registry


def test_find_applicable_returns_registered():

    registry = make_registry()

    observations = (
        make_observation(),
    )

    correlators = registry.find_applicable(
        observations
    )

    assert len(correlators) == 1
    assert isinstance(
        correlators[0],
        NumericCorrelator,
    )


def test_find_applicable_empty_registry():

    registry = CorrelatorRegistry()

    correlators = registry.find_applicable(
        (
            make_observation(),
        )
    )

    assert correlators == ()


def test_constructor_with_correlators():

    correlator = NumericCorrelator()

    registry = CorrelatorRegistry(
        [correlator]
    )

    assert len(registry) == 1
    assert correlator in registry


def test_repr():

    registry = make_registry()

    representation = repr(registry)

    assert "CorrelatorRegistry" in representation
    assert "1" in representation


def test_priority_order():

    registry = CorrelatorRegistry()

    low = LowPriorityCorrelator()
    high = HighPriorityCorrelator()
    medium = MediumPriorityCorrelator()

    registry.register(low)
    registry.register(high)
    registry.register(medium)

    ordered = list(registry)

    assert ordered == [
        high,
        medium,
        low,
    ]


def test_ordered_returns_priority_order():

    registry = CorrelatorRegistry()

    registry.register(LowPriorityCorrelator())
    registry.register(HighPriorityCorrelator())
    registry.register(MediumPriorityCorrelator())

    ordered = registry.ordered()

    assert ordered[0].priority == 100
    assert ordered[1].priority == 50
    assert ordered[2].priority == 10


def test_find_applicable_is_priority_ordered():

    registry = CorrelatorRegistry()

    registry.register(LowPriorityCorrelator())
    registry.register(HighPriorityCorrelator())
    registry.register(MediumPriorityCorrelator())

    correlators = registry.find_applicable(
        (
            make_observation(),
        )
    )

    assert correlators[0].priority == 100
    assert correlators[1].priority == 50
    assert correlators[2].priority == 10