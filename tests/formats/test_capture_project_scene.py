from capture_recovery.formats import (
    CaptureProjectBuilder,
    CaptureScene,
)


from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_scene_objects():

    return [

        SemanticObject(
            object_type="Structure",

            identifier="Face Truss",

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
                "parent": "Face Truss",
            },
        ),
    ]


def test_project_contains_scene():

    project = CaptureProjectBuilder().build(
        create_scene_objects(),
    )

    assert isinstance(
        project.scene,
        CaptureScene,
    )


def test_project_scene_nodes():

    project = CaptureProjectBuilder().build(
        create_scene_objects(),
    )

    assert (
        "Face Truss"
        in project.scene.nodes
    )

    assert (
        "MAC Aura"
        in project.scene.nodes
    )