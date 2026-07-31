import json

from capture_recovery.benchmark import (
    BenchmarkReport,
    BenchmarkResult,
    BenchmarkStatistics,
)


def make_statistics() -> BenchmarkStatistics:

    stats = BenchmarkStatistics()

    stats.add(
        BenchmarkResult(
            filename="project.c2p",
            file_size=100,
            object_count=10,
            recovered_objects=9,
            unknown_objects=1,
            property_count=20,
            candidate_count=15,
            average_confidence=0.90,
            minimum_confidence=0.70,
            maximum_confidence=1.00,
            conflict_count=2,
            unknown_signature_count=1,
            duration_seconds=0.25,
        )
    )

    return stats


def test_text():

    report = BenchmarkReport(
        make_statistics()
    )

    text = report.to_text()

    assert "Capture Recovery Benchmark" in text
    assert "Projects analysed" in text
    assert "Recovery" in text


def test_markdown():

    report = BenchmarkReport(
        make_statistics()
    )

    md = report.to_markdown()

    assert md.startswith("# Capture Recovery Benchmark")
    assert "| Projects |" in md
    assert "| Objects |" in md


def test_json():

    report = BenchmarkReport(
        make_statistics()
    )

    data = json.loads(
        report.to_json()
    )

    assert data["project_count"] == 1
    assert data["total_objects"] == 10


def test_str():

    report = BenchmarkReport(
        make_statistics()
    )

    assert str(report) == report.to_text()