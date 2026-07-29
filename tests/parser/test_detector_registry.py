from capture_recovery.parser.detector_registry import DetectorRegistry


class DummyDetector:

    def detect(self, data: bytes):
        return []


def test_registry_is_empty():

    registry = DetectorRegistry()

    assert len(registry) == 0


def test_register_detector():

    registry = DetectorRegistry()

    registry.register(DummyDetector())

    assert len(registry) == 1


def test_iter_returns_registered_detector():

    registry = DetectorRegistry()

    detector = DummyDetector()

    registry.register(detector)

    detectors = list(registry)

    assert detectors == [detector]


def test_detectors_returns_tuple():

    registry = DetectorRegistry()

    detector = DummyDetector()

    registry.register(detector)

    detectors = registry.detectors()

    assert isinstance(detectors, tuple)
    assert detectors[0] is detector