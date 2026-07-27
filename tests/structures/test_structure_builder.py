from capture_recovery.indexes import DetectionIndex
from capture_recovery.models import DataType
from capture_recovery.models import Detection
from capture_recovery.structures import StructureBuilder


def test_empty():

    builder = StructureBuilder()

    result = builder.build(DetectionIndex([]))

    assert result == []


def test_single_structure():

    detections = [

        Detection(
            offset=0,
            length=4,
            datatype=DataType.INT32,
            value=1,
        ),

        Detection(
            offset=4,
            length=4,
            datatype=DataType.FLOAT32,
            value=1.5,
        ),

        Detection(
            offset=8,
            length=4,
            datatype=DataType.FLOAT32,
            value=2.5,
        ),

    ]

    builder = StructureBuilder()

    structures = builder.build(
        DetectionIndex(detections)
    )

    assert len(structures) == 1

    assert len(structures[0].fields) == 3


def test_two_structures():

    detections = [

        Detection(
            offset=0,
            length=4,
            datatype=DataType.INT32,
            value=1,
        ),

        Detection(
            offset=4,
            length=4,
            datatype=DataType.FLOAT32,
            value=2,
        ),

        Detection(
            offset=100,
            length=4,
            datatype=DataType.ASCII,
            value="Hello",
        ),

    ]

    builder = StructureBuilder(max_gap=8)

    result = builder.build(
        DetectionIndex(detections)
    )

    assert len(result) == 2