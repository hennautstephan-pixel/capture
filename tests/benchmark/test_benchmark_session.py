from pathlib import Path

from capture_recovery.benchmark import BenchmarkSession


def test_defaults():

    session = BenchmarkSession(
        samples_directory=Path("samples")
    )

    assert session.samples_directory == Path("samples")
    assert not session.completed
    assert session.duration_seconds == 0.0


def test_finish():

    session = BenchmarkSession(
        samples_directory=Path("samples")
    )

    session.finish()

    assert session.completed
    assert session.finished_at is not None
    assert session.duration_seconds >= 0.0


def test_to_dict():

    session = BenchmarkSession(
        samples_directory=Path("samples")
    )

    session.finish()

    data = session.to_dict()

    assert data["samples_directory"] == "samples"
    assert "statistics" in data
    assert "started_at" in data
    assert "finished_at" in data
    assert data["duration_seconds"] >= 0.0