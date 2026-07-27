from capture_recovery.formats import (
    CaptureFixtureBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.library import (
    FixtureDefinition,
    FixtureLibrary,
    FixtureResolver,
)


def create_builder():

    library = FixtureLibrary()

    library.register(
        FixtureDefinition(
            manufacturer="Martin",
            model="MAC Aura",
            modes=[
                "Standard",
            ],
            channels={
                "dimmer": 1,
                "pan": 2,
                "tilt": 3,
            },
            geometry={
                "beam_angle": 40,
                "zoom": 20,
            },
        )
    )

    resolver = FixtureResolver(
        library,
    )

    return CaptureFixtureBuilder(
        resolver,
    )


def create_fixture():

    return SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={
            "manufacturer": "Martin",
            "model": "MAC Aura",
            "mode": "Standard",
            "universe": 1,
            "address": 10,

            "position": (
                3.5,
                2.0,
                6.0,
            ),

            "rotation": (
                180.0,
                45.0,
                0.0,
            ),

            "scale": (
                1.0,
                1.0,
                1.0,
            ),

            "height": 6.0,

            "focus_point": "Centre plateau",
        },
    )


def test_library_geometry_is_preserved():

    builder = create_builder()

    fixture = builder.build(
        create_fixture(),
    )

    assert fixture.properties["geometry"][
        "beam_angle"
    ] == 40

    assert fixture.properties["geometry"][
        "zoom"
    ] == 20


def test_scene_placement_is_created():

    builder = create_builder()

    fixture = builder.build(
        create_fixture(),
    )

    placement = fixture.properties[
        "placement"
    ]

    assert placement["position"] == (
        3.5,
        2.0,
        6.0,
    )

    assert placement["rotation"] == (
        180.0,
        45.0,
        0.0,
    )


def test_geometry_and_placement_are_separated():

    builder = create_builder()

    fixture = builder.build(
        create_fixture(),
    )

    assert "geometry" in fixture.properties

    assert "placement" in fixture.properties

    assert (
        "position"
        not in fixture.properties["geometry"]
    )

    assert (
        "beam_angle"
        not in fixture.properties["placement"]
    )


def test_placement_height_and_focus():

    builder = create_builder()

    fixture = builder.build(
        create_fixture(),
    )

    placement = fixture.properties[
        "placement"
    ]

    assert placement["height"] == 6.0

    assert placement["focus_point"] == (
        "Centre plateau"
    )