from pathlib import Path

from capture_recovery.benchmark import (
    BenchmarkResult,
    BenchmarkRunner,
    SampleLoader,
)


def fake_analyser(path: str) -> BenchmarkResult:

    return BenchmarkResult(
        filename=Path(path).name,
        file_size=100,
        object_count=10,
        recovered_objects=9,
        unknown_objects=1,
        property_count=20,
        candidate_count=15,
        average_confidence=0.9,
        minimum_confidence=0.7,
        maximum_confidence=1.0,
        conflict_count=0,
        unknown_signature_count=0,
        duration_seconds=0.01,
    )


def test_empty(tmp_path: Path):

    runner = BenchmarkRunner(
        SampleLoader(tmp_path),
        fake_analyser,
    )

    stats = runner.run()

    assert stats.project_count == 0


def test_run(tmp_path: Path):

    (tmp_path / "a.c2p").write_bytes(b"")
    (tmp_path / "b.c2p").write_bytes(b"")

    runner = BenchmarkRunner(
        SampleLoader(tmp_path),
        fake_analyser,
    )

    stats = runner.run()

    assert stats.project_count == 2
    assert stats.total_objects == 20
    assert stats.recovered_objects == 18
    assert stats.recovery_rate == 0.9