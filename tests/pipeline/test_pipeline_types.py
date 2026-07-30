from capture_recovery.pipeline.types import (
    BinaryAnalysisDict,
    BinaryPipelineDict,
)


def test_binary_analysis_dict() -> None:
    analysis: BinaryAnalysisDict = {
        "size": 123,
        "signature": b"1234567890123456",
        "count": 1,
        "detections": [],
        "detection_index": {},
        "reverse": None,
    }

    assert analysis["size"] == 123
    assert analysis["count"] == 1


def test_binary_pipeline_dict() -> None:
    pipeline: BinaryPipelineDict = {
        "data": b"",
        "analysis": {
            "size": 0,
            "signature": b"",
            "count": 0,
            "detections": [],
            "detection_index": {},
            "reverse": None,
        },
        "result": None,
    }

    assert pipeline["analysis"]["size"] == 0
    assert pipeline["data"] == b""