from capture_recovery.reconstruction import (
    FixtureReconstructor,
)

from capture_recovery.formats import (
    CaptureFixture,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def test_fixture_reconstruction():

    obj = SemanticObject(

        object_type="Fixture",

        identifier="MAC Aura",

        properties={

            "manufacturer": "Martin",

            "model": "MAC Aura XB",

            "mode": "Extended",

            "universe": 2,

            "address": 101,

        },
    )


    fixture = (
        FixtureReconstructor()
        .reconstruct(
            obj,
        )
    )


    assert isinstance(
        fixture,
        CaptureFixture,
    )


    assert fixture.name == (
        "MAC Aura"
    )


    assert fixture.universe == 2

    assert fixture.address == 101

    assert fixture.manufacturer == (
        "Martin"
    )