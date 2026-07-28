from capture_recovery.reconstruction import (
    FixtureTransformReconstructor,
    FocusReconstructor,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def test_fixture_transform():

    obj = SemanticObject(

        object_type="Fixture",

        identifier="Profile",

        properties={

            "position": (
                1.0,
                2.0,
                5.0,
            ),

            "rotation": (
                0.0,
                45.0,
                0.0,
            ),
        },
    )


    result = (
        FixtureTransformReconstructor()
        .reconstruct(
            obj,
        )
    )


    assert result["position"] == (
        1.0,
        2.0,
        5.0,
    )


    assert result["rotation"] == (
        0.0,
        45.0,
        0.0,
    )



def test_focus_reconstruction():

    obj = SemanticObject(

        object_type="Fixture",

        identifier="Wash",

        properties={

            "focus_point": "Centre",

            "pan": 20.0,

            "tilt": -10.0,
        },
    )


    result = (
        FocusReconstructor()
        .reconstruct(
            obj,
        )
    )


    assert result["focus_point"] == (
        "Centre"
    )

    assert result["pan"] == 20.0

    assert result["tilt"] == -10.0