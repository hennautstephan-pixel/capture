from capture_recovery.parser.binary_analysis import BinaryAnalysis
from capture_recovery.parser.segment import Segment


def test_empty_analysis():

    analysis = BinaryAnalysis()

    assert analysis.size == 0
    assert analysis.segment_count == 0
    assert analysis.detection_count == 0
    assert analysis.statistics == {}
    assert analysis.metadata == {}


def test_add_segment():

    analysis = BinaryAnalysis()

    segment = Segment(
        offset=0,
        length=10,
        kind="ascii",
    )

    analysis.add_segment(segment)

    assert analysis.segment_count == 1
    assert analysis.segments[0] is segment


def test_add_detection():

    analysis = BinaryAnalysis()

    detection = object()

    analysis.add_detection(detection)

    assert analysis.detection_count == 1


def test_add_string():

    analysis = BinaryAnalysis()

    analysis.add_string("Capture")

    assert analysis.strings == ["Capture"]


def test_add_signature():

    analysis = BinaryAnalysis()

    signature = object()

    analysis.add_signature(signature)

    assert analysis.signatures == [signature]


def test_add_object():

    analysis = BinaryAnalysis()

    obj = object()

    analysis.add_object(obj)

    assert analysis.inferred_objects == [obj]


def test_add_relation():

    analysis = BinaryAnalysis()

    relation = object()

    analysis.add_relation(relation)

    assert analysis.relations == [relation]