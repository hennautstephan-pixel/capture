from capture_recovery.analysis import AnalysisResult
from capture_recovery.benchmark import BenchmarkResult


def make_result() -> BenchmarkResult:

    return BenchmarkResult(
        filename="Hospitaliens.c2p",
        file_size=1024,
        object_count=100,
        recovered_objects=95,
        unknown_objects=5,
        property_count=420,
        candidate_count=180,
        average_confidence=0.94,
        minimum_confidence=0.52,
        maximum_confidence=1.0,
        conflict_count=2,
        unknown_signature_count=3,
        duration_seconds=1.5,
    )


def test_properties():

    result = make_result()

    assert result.filename == "Hospitaliens.c2p"
    assert result.file_size == 1024
    assert result.object_count == 100
    assert result.recovered_objects == 95
    assert result.unknown_objects == 5
    assert result.property_count == 420
    assert result.candidate_count == 180
    assert result.average_confidence == 0.94
    assert result.minimum_confidence == 0.52
    assert result.maximum_confidence == 1.0
    assert result.conflict_count == 2
    assert result.unknown_signature_count == 3
    assert result.duration_seconds == 1.5


def test_recovery_rate():

    result = make_result()

    assert result.recovery_rate == 0.95


def test_unknown_rate():

    result = make_result()

    assert result.unknown_rate == 0.05


def test_zero_objects():

    result = BenchmarkResult(
        filename="empty.c2p",
        file_size=0,
        object_count=0,
        recovered_objects=0,
        unknown_objects=0,
        property_count=0,
        candidate_count=0,
        average_confidence=0.0,
        minimum_confidence=0.0,
        maximum_confidence=0.0,
        conflict_count=0,
        unknown_signature_count=0,
        duration_seconds=0.0,
    )

    assert result.recovery_rate == 0.0
    assert result.unknown_rate == 0.0


def test_analysed():

    result = make_result()

    assert result.analysed


def test_not_analysed():

    result = BenchmarkResult(
        filename="failed.c2p",
        file_size=0,
        object_count=0,
        recovered_objects=0,
        unknown_objects=0,
        property_count=0,
        candidate_count=0,
        average_confidence=0.0,
        minimum_confidence=0.0,
        maximum_confidence=0.0,
        conflict_count=0,
        unknown_signature_count=0,
        duration_seconds=-1.0,
    )

    assert not result.analysed


def test_from_analysis():

    analysis = AnalysisResult(
        filename="demo.c2p",
        file_size=2048,
        object_count=100,
        property_count=250,
        candidate_count=180,
        average_confidence=0.91,
        minimum_confidence=0.72,
        maximum_confidence=1.00,
        unknown_objects=8,
        unknown_signatures=3,
        conflict_count=2,
        duration_seconds=0.42,
    )

    result = BenchmarkResult.from_analysis(
        analysis
    )

    assert result.filename == "demo.c2p"
    assert result.file_size == 2048
    assert result.object_count == 100
    assert result.recovered_objects == 92
    assert result.unknown_objects == 8
    assert result.property_count == 250
    assert result.candidate_count == 180
    assert result.average_confidence == 0.91
    assert result.minimum_confidence == 0.72
    assert result.maximum_confidence == 1.00
    assert result.conflict_count == 2
    assert result.unknown_signature_count == 3
    assert result.duration_seconds == 0.42
    assert result.recovery_rate == 0.92