from capture_recovery.knowledge import KnowledgeResult


def test_defaults():

    result = KnowledgeResult()

    assert result.known_signature_count == 0
    assert result.unknown_signature_count == 0
    assert result.decoded_object_count == 0
    assert result.signature_count == 0
    assert result.total == 0
    assert result.coverage == 0.0
    assert not result


def test_add_known():

    result = KnowledgeResult()

    result.add_known("fixture")

    assert result.known_signature_count == 1
    assert result.total == 1
    assert result.coverage == 1.0
    assert result


def test_add_unknown():

    result = KnowledgeResult()

    result.add_unknown("blob")

    assert result.unknown_signature_count == 1
    assert result.total == 1
    assert result.coverage == 0.0
    assert not result


def test_add_object():

    result = KnowledgeResult()

    result.add_object(object())

    assert result.decoded_object_count == 1


def test_add_signature():

    result = KnowledgeResult()

    result.add_signature(object())

    assert result.signature_count == 1


def test_mixed_statistics():

    result = KnowledgeResult()

    result.add_known("fixture")
    result.add_known("group")

    result.add_unknown("blob1")
    result.add_unknown("blob2")

    assert result.known_signature_count == 2
    assert result.unknown_signature_count == 2
    assert result.total == 4
    assert result.coverage == 0.5


def test_len():

    result = KnowledgeResult()

    result.add_known(1)
    result.add_unknown(2)
    result.add_unknown(3)

    assert len(result) == 3


def test_bool():

    result = KnowledgeResult()

    assert not result

    result.add_known(1)

    assert result