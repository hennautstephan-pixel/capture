from capture_recovery.formats import (
    HierarchyResolver,
    SceneNode,
)


def test_parent_child_position():

    nodes = {

        "Room": SceneNode(
            name="Room",

            position=(
                0.0,
                0.0,
                5.0,
            ),
        ),

        "Truss": SceneNode(
            name="Truss",

            parent="Room",

            position=(
                0.0,
                0.0,
                1.0,
            ),
        ),
    }


    result = HierarchyResolver().resolve(
        "Truss",
        nodes,
    )


    assert result.z == 6.0


def test_nested_hierarchy():

    nodes = {

        "Stage": SceneNode(
            name="Stage",
        ),

        "Bridge": SceneNode(
            name="Bridge",

            parent="Stage",

            position=(
                1.0,
                0.0,
                0.0,
            ),
        ),

        "Lamp": SceneNode(
            name="Lamp",

            parent="Bridge",

            position=(
                0.0,
                2.0,
                0.0,
            ),
        ),
    }


    result = HierarchyResolver().resolve(
        "Lamp",
        nodes,
    )


    assert result.x == 1.0

    assert result.y == 2.0