from capture_recovery.discovery import ConfidenceAggregator


def test_empty():

    aggregator = ConfidenceAggregator()

    assert aggregator.aggregate([]) == 0.0


def test_single_value():

    aggregator = ConfidenceAggregator()

    assert aggregator.aggregate([0.8]) == 0.8


def test_two_values():

    aggregator = ConfidenceAggregator()

    result = aggregator.aggregate(
        [
            0.8,
            0.8,
        ]
    )

    assert abs(result - 0.96) < 1e-9


def test_three_values():

    aggregator = ConfidenceAggregator()

    result = aggregator.aggregate(
        [
            0.7,
            0.8,
            0.9,
        ]
    )

    assert abs(result - 0.994) < 1e-9


def test_order_does_not_matter():

    aggregator = ConfidenceAggregator()

    a = aggregator.aggregate(
        [
            0.3,
            0.8,
            0.5,
        ]
    )

    b = aggregator.aggregate(
        [
            0.5,
            0.3,
            0.8,
        ]
    )

    assert abs(a - b) < 1e-12


def test_clamps_values():

    aggregator = ConfidenceAggregator()

    result = aggregator.aggregate(
        [
            -1.0,
            2.0,
        ]
    )

    assert result == 1.0


def test_result_never_exceeds_one():

    aggregator = ConfidenceAggregator()

    result = aggregator.aggregate(
        [
            1.0,
            1.0,
            1.0,
        ]
    )

    assert result == 1.0