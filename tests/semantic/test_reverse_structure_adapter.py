from capture_recovery.indexes import DetectionIndex
from capture_recovery.models import DataType
from capture_recovery.reverse.alignment_value import AlignmentValue
from capture_recovery.reverse.entropy_value import EntropyValue
from capture_recovery.reverse.guid_value import GuidValue
from capture_recovery.reverse.numeric_type import INT32
from capture_recovery.reverse.numeric_value import NumericValue
from capture_recovery.reverse.reverse_engine import ReverseResult
from capture_recovery.reverse.string_type import ASCII
from capture_recovery.reverse.string_value import StringValue
from capture_recovery.semantic.reverse_structure_adapter import (
    ReverseStructureAdapter,
)
from capture_recovery.reverse.guid_type import WINDOWS_GUID


def test_create_adapter():

    adapter = ReverseStructureAdapter()

    assert adapter is not None


def test_empty_result():

    adapter = ReverseStructureAdapter()

    index = adapter.adapt(
        ReverseResult(),
    )

    assert isinstance(index, DetectionIndex)

    assert len(index) == 0


def test_numeric_detection():

    adapter = ReverseStructureAdapter()

    value = NumericValue(
        offset=100,
        numeric_type=INT32,
        value=123,
        endianness="little",
    )

    print(value.type_name)

    result = ReverseResult(
        numeric=(value,),
    )

    index = adapter.adapt(result)

    assert len(index) == 1

    detection = index.all()[0]

    assert detection.offset == 100
    assert detection.value == 123
    assert detection.datatype == DataType.INT32
    assert detection.detector == "NumericDetector"


def test_ascii_detection():

    adapter = ReverseStructureAdapter()

    value = StringValue(
        offset=50,
        string_type=ASCII,
        value="Fixture",
        raw_bytes=b"Fixture",
        terminated=True,
    )

    result = ReverseResult(
        strings=(value,),
    )

    index = adapter.adapt(result)

    detection = index.all()[0]

    assert detection.datatype == DataType.ASCII
    assert detection.value == "Fixture"


def test_guid_detection():

    adapter = ReverseStructureAdapter()

    value = GuidValue(
        offset=200,
        guid_type=WINDOWS_GUID,
        value="12345678-1234-1234-1234-123456789ABC",
        raw_bytes=b"\x00" * 16,
    )

    result = ReverseResult(
        guids=(value,),
    )

    index = adapter.adapt(result)

    detection = index.all()[0]

    assert detection.datatype == DataType.UUID
    assert detection.offset == 200


def test_alignment_detection():

    adapter = ReverseStructureAdapter()

    value = AlignmentValue(
        offset=64,
        alignment=16,
        score=0.9,
        length=16,
    )

    result = ReverseResult(
        alignments=(value,),
    )

    index = adapter.adapt(result)

    detection = index.all()[0]

    assert detection.datatype == DataType.STRUCT
    assert detection.value == 16


def test_entropy_detection():

    adapter = ReverseStructureAdapter()

    value = EntropyValue(
        offset=512,
        entropy=7.8,
        score=0.95,
        length=128,
    )

    result = ReverseResult(
        entropy=(value,),
    )

    index = adapter.adapt(result)

    detection = index.all()[0]

    assert detection.datatype == DataType.BYTES
    assert detection.value == 7.8


def test_sorted_index():

    adapter = ReverseStructureAdapter()

    a = NumericValue(
        offset=100,
        numeric_type=INT32,
        value=1,
        endianness="little",
    )

    b = NumericValue(
        offset=20,
        numeric_type=INT32,
        value=2,
        endianness="little",
    )

    result = ReverseResult(
        numeric=(a, b),
    )

    index = adapter.adapt(result)

    detections = index.all()

    assert detections[0].offset == 20
    assert detections[1].offset == 100


def test_call_operator():

    adapter = ReverseStructureAdapter()

    result = ReverseResult()

    index = adapter(result)

    assert isinstance(index, DetectionIndex)