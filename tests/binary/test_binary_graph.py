from capture_recovery.binary.binary_graph import BinaryGraph
from capture_recovery.binary.binary_reference import BinaryReference


def test_empty_graph():

    graph = BinaryGraph()

    assert len(graph) == 0


def test_add_reference():

    graph = BinaryGraph()

    graph.add(
        BinaryReference(
            source=1,
            target=2,
            offset=128,
        )
    )

    assert len(graph) == 1


def test_children():

    graph = BinaryGraph()

    graph.add(BinaryReference(1, 2, 10))
    graph.add(BinaryReference(1, 3, 20))

    assert graph.children(1) == frozenset({2, 3})


def test_parents():

    graph = BinaryGraph()

    graph.add(BinaryReference(10, 5, 0))
    graph.add(BinaryReference(20, 5, 0))

    assert graph.parents(5) == frozenset({10, 20})


def test_isolated():

    graph = BinaryGraph()

    assert graph.is_isolated(42)

    graph.add(BinaryReference(1, 42, 0))

    assert not graph.is_isolated(42)


def test_clear():

    graph = BinaryGraph()

    graph.add(BinaryReference(1, 2, 0))
    graph.add(BinaryReference(2, 3, 0))

    graph.clear()

    assert len(graph) == 0
    assert graph.children(1) == frozenset()
    assert graph.parents(3) == frozenset()


def test_iterator():

    graph = BinaryGraph()

    ref = BinaryReference(1, 2, 10)

    graph.add(ref)

    assert list(graph) == [ref]