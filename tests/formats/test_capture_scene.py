from capture_recovery.formats import (
    CaptureScene,
    SceneBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_objects():

    return [

        SemanticObject(
            object_type="Structure",

            identifier="Truss",

            properties={
                "position": (
                    0.0,
                    0.0,
                    6.0,
                ),
            },
        ),

        SemanticObject(
            object_type="Fixture",

            identifier="MAC Aura",

            properties={
                "parent": "Truss",

                "position": (
                    1.0,
                    0.0,
                    0.0,
                ),
            },
        ),
    ]


def test_scene_builder_creates_nodes():

    scene = SceneBuilder().build(
        create_objects(),
    )

    assert isinstance(
        scene,
        CaptureScene,
    )

    assert "Truss" in scene.nodes

    assert "MAC Aura" in scene.nodes


def test_scene_parent_relation():

    scene = SceneBuilder().build(
        create_objects(),
    )

    truss = scene.nodes["Truss"]

    assert (
        "MAC Aura"
        in truss.children
    )


def test_scene_root_nodes():

    scene = SceneBuilder().build(
        create_objects(),
    )

    assert scene.root_nodes == [
        "Truss",
    ]