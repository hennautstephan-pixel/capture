from capture_recovery.analysis import (
    ObjectRelation,
    RelationGraph,
)

from capture_recovery.formats import (
    CaptureScene,
    SceneNode,
)

from capture_recovery.reconstruction import (
    RelationApplier,
)


def create_scene():

    scene = CaptureScene()

    scene.add_node(
        SceneNode(
            name="Truss",
        )
    )

    scene.add_node(
        SceneNode(
            name="MAC Aura",
        )
    )

    return scene



def create_graph():

    graph = RelationGraph()

    graph.add(
        ObjectRelation(
            source="MAC Aura",

            target="Truss",

            relation_type="mounted_on",
        )
    )

    return graph



def test_apply_mount_relation():

    scene = create_scene()

    RelationApplier().apply(
        scene,
        create_graph(),
    )


    fixture = scene.nodes[
        "MAC Aura"
    ]

    truss = scene.nodes[
        "Truss"
    ]


    assert fixture.parent == (
        "Truss"
    )

    assert (
        "MAC Aura"
        in truss.children
    )