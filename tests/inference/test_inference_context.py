from capture_recovery.inference import (
    InferenceContext,
)

from capture_recovery.knowledge import (
    KnowledgeResult,
)

from capture_recovery.structures import (
    Structure,
)


def structure():

    s = Structure(
        name="TestStructure",
        offset=100,
        length=32,
        confidence=91.0,
    )

    #
    # Structure.score is a read-only property that reads
    # metadata["score"].
    #

    s.metadata["score"] = 87.5

    return s


def test_create():

    context = InferenceContext(
        structure(),
    )

    assert context is not None


def test_structure():

    s = structure()

    context = InferenceContext(
        s,
    )

    assert context.structure is s


def test_offset():

    context = InferenceContext(
        structure(),
    )

    assert context.offset == 100


def test_length():

    context = InferenceContext(
        structure(),
    )

    assert context.length == 32


def test_score():

    context = InferenceContext(
        structure(),
    )

    assert context.score == 87.5


def test_confidence():

    context = InferenceContext(
        structure(),
    )

    assert context.confidence == 91.0


def test_without_knowledge():

    context = InferenceContext(
        structure(),
    )

    assert context.has_knowledge is False


def test_with_knowledge():

    context = InferenceContext(
        structure(),
        knowledge_result=KnowledgeResult(),
    )

    assert context.has_knowledge is True


def test_metadata():

    context = InferenceContext(
        structure(),
    )

    context.set(
        "hello",
        "world",
    )

    assert context.get("hello") == "world"


def test_option():

    context = InferenceContext(
        structure(),
        options={
            "strict": True,
        },
    )

    assert context.option("strict") is True


def test_repr():

    context = InferenceContext(
        structure(),
    )

    text = repr(context)

    assert "InferenceContext" in text
    assert "offset=0x64" in text