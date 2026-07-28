from capture_recovery.reconstruction import (
    ProjectReconstructor,
)

from capture_recovery.formats import (
    CaptureProject,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def test_reconstruct_project():

    objects = [

        SemanticObject(
            object_type="Fixture",

            identifier="MAC Aura",

            properties={
                "parent": "Truss",
            },
        )

    ]


    project = (
        ProjectReconstructor()
        .reconstruct(
            objects,
        )
    )


    assert isinstance(
        project,
        CaptureProject,
    )


    assert len(
        project.fixtures,
    ) == 1


    assert (
        "MAC Aura"
        in project.scene.nodes
    )