from capture_recovery.formats import (
    CaptureJsonLoader,
    CaptureJsonSerializer,
    CaptureProjectBuilder,
    SceneStructure,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_truss():

    return SemanticObject(
        object_type="Structure",

        identifier="Face Truss",

        properties={
            "type": "Truss",

            "position": (
                0.0,
                0.0,
                6.0,
            ),

            "rotation": (
                0.0,
                0.0,
                0.0,
            ),

            "length": 8.0,
        },
    )


def test_project_builder_adds_structure():

    builder = CaptureProjectBuilder()

    project = builder.build(
        [
            create_truss(),
        ],
        name="Structure Test",
    )

    assert len(
        project.structures,
    ) == 1

    structure = project.structures[0]

    assert structure.name == "Face Truss"

    assert structure.structure_type == "Truss"

    assert structure.length == 8.0


def test_structure_position_is_preserved():

    builder = CaptureProjectBuilder()

    project = builder.build(
        [
            create_truss(),
        ],
    )

    structure = project.structures[0]

    assert structure.position == (
        0.0,
        0.0,
        6.0,
    )


def test_structure_json_export():

    builder = CaptureProjectBuilder()

    project = builder.build(
        [
            create_truss(),
        ],
    )

    serializer = CaptureJsonSerializer()

    data = serializer.serialize(
        project,
    )

    assert data["structures"][0] == {
        "name": "Face Truss",

        "type": "Truss",

        "position": [
            0.0,
            0.0,
            6.0,
        ],

        "rotation": [
            0.0,
            0.0,
            0.0,
        ],

        "length": 8.0,

        "properties": {
            "type": "Truss",

            "position": (
                0.0,
                0.0,
                6.0,
            ),

            "rotation": (
                0.0,
                0.0,
                0.0,
            ),

            "length": 8.0,
        },
    }


def test_structure_json_import():

    builder = CaptureProjectBuilder()

    project = builder.build(
        [
            create_truss(),
        ],
    )

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    restored = loader.from_dict(
        serializer.serialize(
            project,
        )
    )

    assert len(
        restored.structures,
    ) == 1

    structure = restored.structures[0]

    assert isinstance(
        structure,
        SceneStructure,
    )

    assert structure.name == "Face Truss"

    assert structure.structure_type == "Truss"

    assert structure.length == 8.0