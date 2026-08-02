from capture_recovery.io import (
    CaptureFormatDetector,
)


def test_detect_json(tmp_path):

    path = tmp_path / "project.json"

    path.write_bytes(
        b"{\"test\":1}"
    )

    detector = CaptureFormatDetector()

    assert detector.detect(path) == "json"