from capture_recovery.discovery import (
    ObservationStatistics,
    PropertyObservation,
)


def make_float(value: float) -> PropertyObservation:

    return PropertyObservation(
        object_type="Fixture",
        offset=0x100,
        semantic_property="Position.X",
        binary_before=value,
        binary_after=value,
        semantic_before=value,
        semantic_after=value,
    )


def make_int(value: int) -> PropertyObservation:

    return PropertyObservation(
        object_type="Fixture",
        offset=0x100,
        semantic_property="Mode",
        binary_before=value,
        binary_after=value,
        semantic_before=value,
        semantic_after=value,
    )


def make_bool(value: bool) -> PropertyObservation:

    return PropertyObservation(
        object_type="Fixture",
        offset=0x100,
        semantic_property="Visible",
        binary_before=int(value),
        binary_after=int(value),
        semantic_before=value,
        semantic_after=value,
    )


def make_string(value: str) -> PropertyObservation:

    return PropertyObservation(
        object_type="Fixture",
        offset=0x100,
        semantic_property="Name",
        binary_before=value,
        binary_after=value,
        semantic_before=value,
        semantic_after=value,
    )


def test_empty():

    stats = ObservationStatistics(())

    assert stats.count == 0
    assert stats.semantic_values == ()
    assert stats.binary_values == ()
    assert stats.distinct_semantic_values == frozenset()
    assert stats.distinct_binary_values == frozenset()
    assert stats.minimum is None
    assert stats.maximum is None


def test_float_statistics():

    stats = ObservationStatistics(
        (
            make_float(1.0),
            make_float(2.0),
            make_float(3.0),
        )
    )

    assert stats.count == 3
    assert stats.all_floats
    assert not stats.all_integers
    assert not stats.all_booleans
    assert stats.minimum == 1.0
    assert stats.maximum == 3.0
    assert stats.semantic_value_count == 3


def test_integer_statistics():

    stats = ObservationStatistics(
        (
            make_int(1),
            make_int(2),
            make_int(3),
        )
    )

    assert stats.all_integers
    assert not stats.all_booleans
    assert stats.minimum == 1
    assert stats.maximum == 3


def test_boolean_statistics():

    stats = ObservationStatistics(
        (
            make_bool(True),
            make_bool(False),
        )
    )

    assert stats.all_booleans
    assert not stats.all_integers


def test_string_statistics():

    stats = ObservationStatistics(
        (
            make_string("A"),
            make_string("B"),
        )
    )

    assert stats.all_strings
    assert stats.semantic_value_count == 2


def test_small_integer_domain():

    stats = ObservationStatistics(
        tuple(
            make_int(i)
            for i in range(8)
        )
    )

    assert stats.is_small_integer_domain


def test_large_integer_domain():

    stats = ObservationStatistics(
        tuple(
            make_int(i)
            for i in range(100)
        )
    )

    assert not stats.is_small_integer_domain


def test_distinct_values():

    stats = ObservationStatistics(
        (
            make_int(1),
            make_int(1),
            make_int(2),
            make_int(2),
            make_int(3),
        )
    )

    assert stats.semantic_value_count == 3
    assert stats.binary_value_count == 3