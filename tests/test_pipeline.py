from src.capture_recovery.detectors.float_detector import FloatDetector
from src.capture_recovery.detectors.pipeline import DetectorPipeline


def test_pipeline():

    pipeline = DetectorPipeline([
        FloatDetector(),
    ])

    detections = pipeline.detect(
        b"\x00\x00\x80\x3f"
    )

    assert len(detections) == 1

    detection = detections[0]

    assert detection.datatype == "float"
    assert detection.offset == 0
    assert detection.length == 4
    assert detection.value == 1.0
    assert detection.confidence == 0.70


def test_pipeline_empty():

    pipeline = DetectorPipeline([])

    detections = pipeline.detect(b"")

    assert detections == []