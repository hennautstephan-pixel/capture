from capture_recovery.discovery import (
    ConfidenceAggregator,
    ConstraintMerger,
    EnumConstraint,
    PropertyCandidate,
    RangeConstraint,
)


def candidate(*constraints):

    return PropertyCandidate(
        object_type="Fixture",
        property_name="Intensity",
        offset=12,
        value_type="uint8",
        confidence=0.6,
        observations=5,
        constraints=tuple(constraints),
    )


def test_merge_constraints():

    merger = ConstraintMerger()

    merged = merger.merge(
        [
            candidate(
                RangeConstraint(
                    minimum=0,
                    maximum=255,
                )
            ),
            candidate(
                EnumConstraint(
                    values=(0, 64, 128, 255),
                )
            ),
        ]
    )

    assert len(merged) == 1

    assert len(merged[0].constraints) == 2


def test_remove_duplicate_constraints():

    merger = ConstraintMerger()

    constraint = RangeConstraint(
        minimum=0,
        maximum=255,
    )

    merged = merger.merge(
        [
            candidate(constraint),
            candidate(constraint),
        ]
    )

    assert len(merged) == 1

    assert len(merged[0].constraints) == 1


def test_confidence_is_aggregated():

    merger = ConstraintMerger()
    aggregator = ConfidenceAggregator()

    a = candidate()

    b = PropertyCandidate(
        object_type=a.object_type,
        property_name=a.property_name,
        offset=a.offset,
        value_type=a.value_type,
        confidence=0.95,
        observations=20,
        constraints=(),
    )

    merged = merger.merge([a, b])

    assert merged[0].confidence == aggregator.aggregate(
        [
            0.6,
            0.95,
        ]
    )

    assert merged[0].observations == 20


def test_different_value_types_are_not_merged():

    merger = ConstraintMerger()

    a = candidate()

    b = PropertyCandidate(
        object_type=a.object_type,
        property_name=a.property_name,
        offset=a.offset,
        value_type="float32",
        confidence=a.confidence,
        observations=a.observations,
        constraints=(),
    )

    merged = merger.merge([a, b])

    assert len(merged) == 2