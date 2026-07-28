from capture_recovery.formats import (
    BindingBuilder,
    CaptureFixtureBuilder,
    CaptureJsonLoader,
    CaptureJsonSerializer,
    CaptureProjectBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_mounted_fixture(
    name="MAC Aura",
):

    return SemanticObject(
        object_type="Fixture",

        identifier=name,

        properties={
            "manufacturer": "Martin",

            "model": "MAC Aura",

            "mount": {
                "structure_id": "Face Truss",

                "offset_x": 1.0,

                "offset_y": 0.0,

                "offset_z": -0.2,
            },
        },
    )


def create_structure():

    return SemanticObject(
        object_type="Structure",

        identifier="Face Truss",

        properties={
            "type": "Truss",

            "length": 8.0,
        },
    )


def test_project_builder_creates_binding():

    fixture_builder = CaptureFixtureBuilder()

    project_builder = CaptureProjectBuilder(
        fixture_builder=fixture_builder,
    )

    project = project_builder.build(
        [
            create_mounted_fixture(),
            create_structure(),
        ],
    )

    assert len(
        project.bindings,
    ) == 1

    binding = project.bindings[0]

    assert binding.structure_id == (
        "Face Truss"
    )

    assert (
        "MAC Aura"
        in binding.fixtures
    )


def test_binding_builder_with_multiple_fixtures():

    fixture_builder = CaptureFixtureBuilder()

    project_builder = CaptureProjectBuilder(
        fixture_builder=fixture_builder,
    )

    project = project_builder.build(
        [
            create_mounted_fixture(
                "MAC Aura 1",
            ),

            create_mounted_fixture(
                "MAC Aura 2",
            ),

            create_structure(),
        ],
    )

    binding = project.bindings[0]

    assert len(
        binding.fixtures,
    ) == 2


def test_binding_json_export():

    fixture_builder = CaptureFixtureBuilder()

    project_builder = CaptureProjectBuilder(
        fixture_builder=fixture_builder,
    )

    project = project_builder.build(
        [
            create_mounted_fixture(),
        ],
    )

    serializer = CaptureJsonSerializer()

    data = serializer.serialize(
        project,
    )

    assert data["bindings"][0]["structure_id"] == (
        "Face Truss"
    )

    assert data["bindings"][0]["fixtures"] == [
        "MAC Aura",
    ]


def test_binding_json_import():

    fixture_builder = CaptureFixtureBuilder()

    project_builder = CaptureProjectBuilder(
        fixture_builder=fixture_builder,
    )

    project = project_builder.build(
        [
            create_mounted_fixture(),
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
        restored.bindings,
    ) == 1

    assert restored.bindings[0].structure_id == (
        "Face Truss"
    )

    assert restored.bindings[0].fixtures == [
        "MAC Aura",
    ]


def test_binding_builder_empty_project():

    bindings = BindingBuilder().build(
        CaptureProjectBuilder().build(
            [],
        )
    )

    assert bindings == []