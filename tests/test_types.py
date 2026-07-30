from capture_recovery.types import *


def test_aliases_exist():
    assert BinaryDetection is object
    assert SemanticDetection is object
    assert SemanticObject is object
    assert ReverseAnalysis is object


def test_dict_aliases():
    assert Metadata == dict[str, object]
    assert Evidence == dict[str, object]
