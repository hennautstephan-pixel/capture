from capture_recovery.formats import (
    FixtureGeometry,
)


def test_default_geometry():

    geometry = FixtureGeometry()

    assert geometry.position == (
        0.0,
        0.0,
        0.0,
    )

    assert geometry.rotation == (
        0.0,
        0.0,
        0.0,
    )

    assert geometry.scale == (
        1.0,
        1.0,
        1.0,
    )


def test_geometry_coordinates():

    geometry = FixtureGeometry(
        position=(
            3.5,
            2.0,
            6.0,
        ),
        rotation=(
            180.0,
            45.0,
            0.0,
        ),
        height=6.0,
    )

    assert geometry.x == 3.5

    assert geometry.y == 2.0

    assert geometry.z == 6.0

    assert geometry.pan == 180.0

    assert geometry.tilt == 45.0

    assert geometry.height == 6.0


def test_geometry_to_dict():

    geometry = FixtureGeometry(
        position=(
            1.0,
            2.0,
            3.0,
        ),
        rotation=(
            10.0,
            20.0,
            30.0,
        ),
        metadata={
            "source": "Capture",
        },
    )

    data = geometry.to_dict()

    assert data["position"] == (
        1.0,
        2.0,
        3.0,
    )

    assert data["rotation"] == (
        10.0,
        20.0,
        30.0,
    )

    assert data["metadata"]["source"] == "Capture"


def test_translate_geometry():

    geometry = FixtureGeometry(
        position=(
            1.0,
            2.0,
            3.0,
        ),
        rotation=(
            10.0,
            20.0,
            30.0,
        ),
    )

    moved = geometry.translated(
        5.0,
        6.0,
        7.0,
    )

    assert moved.position == (
        5.0,
        6.0,
        7.0,
    )

    assert moved.rotation == (
        10.0,
        20.0,
        30.0,
    )


def test_rotate_geometry():

    geometry = FixtureGeometry(
        position=(
            1.0,
            2.0,
            3.0,
        ),
    )

    rotated = geometry.rotated(
        90.0,
        45.0,
    )

    assert rotated.position == (
        1.0,
        2.0,
        3.0,
    )

    assert rotated.rotation == (
        90.0,
        45.0,
        0.0,
    )


def test_focus_point():

    geometry = FixtureGeometry(
        focus_point="Centre plateau",
    )

    assert geometry.focus_point == (
        "Centre plateau"
    )