from capture_recovery.indexes.detection_index import DetectionIndex
from capture_recovery.memory.region_builder import RegionBuilder
from capture_recovery.models import Detection


def test_build():

    detections = [

        Detection(
            datatype="ASCII",
            offset=0,
            length=10,
            value="hello",
            confidence=1.0,
        ),

        Detection(
            datatype="FLOAT",
            offset=100,
            length=4,
            value=3.14,
            confidence=0.95,
        ),

    ]

    index = DetectionIndex(detections)

    builder = RegionBuilder()

    memory = builder.build(index)

    assert len(memory) == 2

    assert memory[0].kind == "ASCII"

    assert memory[1].kind == "FLOAT"