from capture_recovery.tools import (
    CompareAll,
    ComparisonReport,
)


def test_empty(tmp_path):

    report = CompareAll().compare(tmp_path)

    assert isinstance(
        report,
        ComparisonReport,
    )

    assert report.comparison_count == 0


def test_two_files(tmp_path):

    (tmp_path / "a.bin").write_bytes(
        b"A"
    )

    (tmp_path / "b.bin").write_bytes(
        b"B"
    )

    report = CompareAll().compare(tmp_path)

    assert report.comparison_count == 1

    assert report.different_pairs == 1