from __future__ import annotations

from capture_recovery.reverse.base_detector import BaseDetector
from capture_recovery.reverse.detection_options import DetectionOptions
from capture_recovery.reverse.detector_type import DetectorType


class DummyDetector(BaseDetector):
    detector_type = DetectorType.NUMERIC


def test_is_enabled_returns_true_when_enabled_types_is_none():
    options = DetectionOptions()

    assert DummyDetector._is_enabled(
        options,
        DetectorType.NUMERIC,
    )


def test_is_enabled_returns_true_when_detector_enabled():
    options = DetectionOptions(
        enabled_types={DetectorType.NUMERIC},
    )

    assert DummyDetector._is_enabled(
        options,
        DetectorType.NUMERIC,
    )


def test_is_enabled_returns_false_when_detector_disabled():
    options = DetectionOptions(
        enabled_types={DetectorType.STRING},
    )

    assert not DummyDetector._is_enabled(
        options,
        DetectorType.NUMERIC,
    )


def test_buffer_returns_full_memoryview():
    data = b"abcdef"
    options = DetectionOptions()

    buffer = DummyDetector._buffer(data, options)

    assert isinstance(buffer, memoryview)
    assert bytes(buffer) == data


def test_buffer_respects_max_scan_size():
    data = b"abcdef"

    options = DetectionOptions(
        max_scan_size=3,
    )

    buffer = DummyDetector._buffer(data, options)

    assert bytes(buffer) == b"abc"


def test_limit_results_without_limit():
    options = DetectionOptions()

    results = DummyDetector._limit_results(
        [1, 2, 3, 4],
        options,
    )

    assert results == (1, 2, 3, 4)


def test_limit_results_with_limit():
    options = DetectionOptions(
        max_results=2,
    )

    results = DummyDetector._limit_results(
        [1, 2, 3, 4],
        options,
    )

    assert results == (1, 2)


def test_offset_in_range():
    assert DummyDetector._offset_in_range(0, 10)
    assert DummyDetector._offset_in_range(9, 10)

    assert not DummyDetector._offset_in_range(-1, 10)
    assert not DummyDetector._offset_in_range(10, 10)


def test_default_name():
    detector = DummyDetector()

    assert detector.name == "DummyDetector"