from capture_recovery.analysis import (
    ObjectRelation,
    RelationBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def test_parent_relation():

    objects = [

        SemanticObject(
            object_type="Fixture",

            identifier="MAC Aura",

            properties={
                "parent": "Face Truss",
            },
        )

    ]


    result = RelationBuilder().build(
        objects,
    )


    assert len(result) == 1

    assert isinstance(
        result[0],
        ObjectRelation,
    )

    assert result[0].source == (
        "MAC Aura"
    )

    assert result[0].target == (
        "Face Truss"
    )

    assert result[0].relation_type == (
        "child_of"
    )


def test_mount_relation():

    objects = [

        SemanticObject(
            object_type="Fixture",

            identifier="Profile",

            properties={
                "structure_id": "Bridge",
            },
        )

    ]


    result = RelationBuilder().build(
        objects,
    )


    assert result[0].relation_type == (
        "mounted_on"
    )


def test_focus_relation():

    objects = [

        SemanticObject(
            object_type="Fixture",

            identifier="Wash",

            properties={
                "focus_point": "Center",
            },
        )

    ]


    result = RelationBuilder().build(
        objects,
    )


    assert result[0].relation_type == (
        "focuses"
    )