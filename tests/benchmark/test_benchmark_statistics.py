from capture_recovery.benchmark import (
    BenchmarkResult,
    BenchmarkStatistics,
)


def make_result(index: int) -> BenchmarkResult:

    return BenchmarkResult(
        filename=f"project{index}.c2p",
        file_size=1000 * index,
        object_count=100,
        recovered_objects=95,
        unknown_objects=5,
        property_count=500,
        candidate_count=200,
        average_confidence=0.90,
        minimum_confidence=0.60,
        maximum_confidence=1.00,
        conflict_count=2,
        unknown_signature_count=1,
        duration_seconds=float(index),
    )


def test_empty():

    stats = BenchmarkStatistics()

    assert stats.project_count == 0
    assert stats.total_objects == 0
    assert stats.recovery_rate == 0.0
    assert stats.average_confidence == 0.0
    assert stats.average_duration == 0.0


def test_add():

    stats = BenchmarkStatistics()

    stats.add(make_result(1))

    assert stats.project_count == 1


def test_totals():

    stats = BenchmarkStatistics(
        [
            make_result(1),
            make_result(2),
        ]
    )

    assert stats.project_count == 2

    assert stats.total_file_size == 3000

    assert stats.total_objects == 200

    assert stats.recovered_objects == 190

    assert stats.unknown_objects == 10

    assert stats.total_properties == 1000

    assert stats.total_candidates == 400

    assert stats.total_conflicts == 4

    assert stats.total_unknown_signatures == 2

    assert stats.total_duration == 3.0


def test_recovery_rate():

    stats = BenchmarkStatistics(
        [
            make_result(1),
            make_result(2),
        ]
    )

    assert stats.recovery_rate == 0.95


def test_average_confidence():

    stats = BenchmarkStatistics(
        [
            make_result(1),
            make_result(2),
        ]
    )

    assert stats.average_confidence == 0.90


def test_minimum_confidence():

    stats = BenchmarkStatistics(
        [
            make_result(1),
            make_result(2),
        ]
    )

    assert stats.minimum_confidence == 0.60


def test_maximum_confidence():

    stats = BenchmarkStatistics(
        [
            make_result(1),
            make_result(2),
        ]
    )

    assert stats.maximum_confidence == 1.00


def test_average_duration():

    stats = BenchmarkStatistics(
        [
            make_result(1),
            make_result(2),
        ]
    )

    assert stats.average_duration == 1.5