from capture_recovery.formats import (
    SpatialTransform,
)


def test_no_rotation_translation():

    result = SpatialTransform().transform_position(
        (1.0, 0.0, 0.0),

        (0.0, 0.0, 6.0),

        (0.0, 0.0, 0.0),
    )

    assert result.x == 1.0

    assert result.y == 0.0

    assert result.z == 6.0


def test_rotation_y_90():

    result = SpatialTransform().transform_position(
        (1.0, 0.0, 0.0),

        (0.0, 0.0, 0.0),

        (0.0, 90.0, 0.0),
    )

    assert round(
        result.x,
        5,
    ) == 0.0

    assert round(
        result.z,
        5,
    ) == -1.0


def test_rotation_z_90():

    result = SpatialTransform().transform_position(
        (1.0, 0.0, 0.0),

        (0.0, 0.0, 0.0),

        (0.0, 0.0, 90.0),
    )

    assert round(
        result.x,
        5,
    ) == 0.0

    assert round(
        result.y,
        5,
    ) == 1.0