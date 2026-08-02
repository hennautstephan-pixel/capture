from capture_recovery.tools import (
    SampleAnalyzer,
)


def test_empty(tmp_path):

    report = SampleAnalyzer().analyze(tmp_path)

    assert report.statistics.file_count == 0

    assert report.statistics.comparison_count == 0