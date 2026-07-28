from capture_recovery.formats import (
    CaptureSerializer,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.models.project import (
    Project,
)


def create_universe():

    return SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={
            "universe": 1,
            "protocol": "sACN",
            "priority": 100,
            "ip_address": "2.0.0.1",
            "port": 5568,
        },
    )


def create_project():

    project = Project(
        name="Universe Test",
    )

    project.add(
        create_universe(),
    )

    return project


def test_serializer_builds_universe():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert len(
        result.universes
    ) == 1


def test_serializer_preserves_universe_number():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    universe = result.universes[0]

    assert universe.universe == 1


def test_serializer_preserves_protocol():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    universe = result.universes[0]

    assert universe.protocol == "sACN"


def test_serializer_preserves_network_properties():

    serializer = CaptureSerializer()

    result = serializer.serialize(
        create_project(),
    )

    universe = result.universes[0]

    assert universe.properties[
        "priority"
    ] == 100

    assert universe.properties[
        "ip_address"
    ] == "2.0.0.1"

    assert universe.properties[
        "port"
    ] == 5568