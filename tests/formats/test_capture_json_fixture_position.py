from capture_recovery.formats import (
    CaptureFixture,
    CaptureJsonLoader,
    CaptureJsonSerializer,
    CaptureProject,
    FixturePosition,
)


def create_project():

    project = CaptureProject(
        name="Position JSON Test",
    )

    project.add_fixture(
        CaptureFixture(
            name="MAC Aura",

            universe=1,

            address=10,

            manufacturer="Martin",

            model="MAC Aura",

            mode="Standard",

            position=FixturePosition(
                x=4.0,
                y=2.5,
                z=7.0,
                pan=180.0,
                tilt=45.0,
                roll=0.0,
            ),

            properties={
                "channels": {
                    "dimmer": 1,
                },
            },
        )
    )

    return project


def test_serializer_exports_fixture_position():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    fixture = result["fixtures"][0]

    assert fixture["position"] == {
        "x": 4.0,
        "y": 2.5,
        "z": 7.0,
        "pan": 180.0,
        "tilt": 45.0,
        "roll": 0.0,
    }


def test_serializer_keeps_fixture_properties():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    fixture = result["fixtures"][0]

    assert fixture["properties"]["channels"][
        "dimmer"
    ] == 1


def test_loader_restores_fixture_position():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    data = serializer.serialize(
        create_project(),
    )

    result = loader.from_dict(
        data,
    )

    fixture = result.fixtures[0]

    assert fixture.position.x == 4.0

    assert fixture.position.y == 2.5

    assert fixture.position.z == 7.0

    assert fixture.position.pan == 180.0

    assert fixture.position.tilt == 45.0

    assert fixture.position.roll == 0.0


def test_json_fixture_position_round_trip():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    original = create_project()

    restored = loader.from_dict(
        serializer.serialize(
            original,
        )
    )

    original_fixture = (
        original.fixtures[0]
    )

    restored_fixture = (
        restored.fixtures[0]
    )

    assert (
        restored_fixture.name
        == original_fixture.name
    )

    assert (
        restored_fixture.position
        == original_fixture.position
    )