from capture_recovery.analysis import (
    ObjectRelation,
    RelationGraph,
    RelationResolver,
)


def create_graph():

    graph = RelationGraph()

    graph.add(
        ObjectRelation(
            source="MAC Aura",
            target="Face Truss",
            relation_type="mounted_on",
        )
    )

    graph.add(
        ObjectRelation(
            source="Bar LED",
            target="Face Truss",
            relation_type="child_of",
        )
    )

    return graph



def test_add_relation():

    graph = create_graph()

    assert len(
        graph.relations,
    ) == 2



def test_find_structure():

    resolver = RelationResolver(
        create_graph(),
    )

    assert resolver.find_structure(
        "MAC Aura",
    ) == "Face Truss"



def test_find_children():

    resolver = RelationResolver(
        create_graph(),
    )

    assert resolver.find_children(
        "Face Truss",
    ) == [
        "Bar LED",
    ]