from src.capture_recovery.detectors.pipeline import DetectorPipeline
from src.capture_recovery.detectors.signature_detector import SignatureDetector
from src.capture_recovery.scanners.file_scanner import FileScanner


def test_file_scanner(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(
        b"\x00"
        b"PK\x03\x04"
        b"\x00"
    )

    scanner = FileScanner(
        DetectorPipeline([
            SignatureDetector(),
        ])
    )

    report = scanner.scan(filename)

    assert len(report.detections) == 1

    detection = report.detections[0]

    assert detection.datatype == "zip"
    assert detection.offset == 1
    assert detection.length == 4
    assert detection.value is None
    assert detection.confidence == 1.0