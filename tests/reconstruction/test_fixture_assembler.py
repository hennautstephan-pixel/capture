from capture_recovery.reconstruction import (
    FixtureAssembler,
)

from capture_recovery.formats import (
    CaptureFixture,
)


def test_fixture_assembly():

    fixture = CaptureFixture(
        name="MAC Aura",
    )


    transform = {

        "position": (
            1,
            2,
            3,
        ),

        "rotation": (
            0,
            45,
            0,
        ),
    }


    focus = {

        "focus_point": "Centre",

        "pan": 10,

        "tilt": -5,
    }


    result = (
        FixtureAssembler()
        .assemble(
            fixture,
            transform,
            focus,
        )
    )


    assert result.properties[
        "position"
    ] == (
        1,
        2,
        3,
    )


    assert result.properties[
        "focus_point"
    ] == "Centre"