from capture_recovery.formats.capture_project import (
    CaptureProject,
)
from capture_recovery.formats.capture_serializer import (
    CaptureSerializer,
)
from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)
from capture_recovery.models.project import Project


def create_project():

    project = Project(
        name="Recovered Capture",
    )

    project.add(
        SemanticObject(
            object_type="Fixture",
            identifier="Mac Aura",
            properties={
                "universe": 1,
                "address": 10,
                "manufacturer": "Martin",
                "model": "MAC Aura",
                "mode": "Standard",
            },
        )
    )

    project.add(
        SemanticObject(
            object_type="Universe",
            identifier="Universe 1",
            properties={
                "universe": 1,
                "protocol": "sACN",
            },
        )
    )

    project.add(
        SemanticObject(
            object_type="Cue",
            identifier="Intro",
            properties={
                "cue_number": 1,
            },
        )
    )

    return project


def test_serialize_returns_capture_project():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert isinstance(
        result,
        CaptureProject,
    )


def test_serialize_project_name():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert result.name == "Recovered Capture"


def test_serialize_fixture():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert len(result.fixtures) == 1

    fixture = result.fixtures[0]

    assert fixture.name == "Mac Aura"

    assert fixture.universe == 1

    assert fixture.address == 10

    assert fixture.manufacturer == "Martin"


def test_serialize_universe():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert len(result.universes) == 1

    universe = result.universes[0]

    assert universe.name == "Universe 1"

    assert universe.universe == 1

    assert universe.protocol == "sACN"


def test_serialize_cue():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert len(result.cues) == 1

    cue = result.cues[0]

    assert cue.name == "Intro"

    assert cue.number == 1


def test_capture_project_count():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert len(result) == 3