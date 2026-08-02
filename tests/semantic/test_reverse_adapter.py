from capture_recovery.semantic.reverse_adapter import (
    ReverseSemanticAdapter,
    SemanticObject,
)


class EmptyReverseResult:
    strings = ()
    guids = ()
    numeric = ()
    alignments = ()
    entropy = ()


def test_create_adapter():

    adapter = ReverseSemanticAdapter()

    assert adapter is not None


def test_empty_adapt():

    adapter = ReverseSemanticAdapter()

    result = adapter.adapt(
        EmptyReverseResult(),
    )

    assert result == []


def test_empty_analyze():

    adapter = ReverseSemanticAdapter()

    result = adapter.analyze(
        EmptyReverseResult(),
    )

    assert "objects" in result
    assert "evidence" in result

    assert result["objects"] == []


def test_semantic_object_as_dict():

    obj = SemanticObject(
        identifier="fixture_1",
        object_type="fixture",
        confidence=0.75,
        properties={
            "name": "Front 1",
        },
    )

    data = obj.as_dict()

    assert data["identifier"] == "fixture_1"
    assert data["object_type"] == "fixture"
    assert data["confidence"] == 0.75
    assert data["properties"]["name"] == "Front 1"


class FakeString:

    offset = 100
    value = "Project"


def test_project_marker_detection():

    class Reverse:

        strings = [
            FakeString(),
        ]

        guids = ()
        numeric = ()
        alignments = ()
        entropy = ()

    adapter = ReverseSemanticAdapter()

    result = adapter.adapt(
        Reverse(),
    )

    assert len(result) == 1

    assert result[0].object_type == "project"

    assert (
        result[0].properties[
            "has_project_marker"
        ]
        is True
    )


class FakeNumeric:

    offset = 10
    value = 123


def test_numeric_block():

    class Reverse:

        strings = ()
        guids = ()
        numeric = [
            FakeNumeric(),
        ]
        alignments = ()
        entropy = ()

    adapter = ReverseSemanticAdapter()

    result = adapter.adapt(
        Reverse(),
    )

    assert len(result) == 1

    assert result[0].object_type == "numeric_block"