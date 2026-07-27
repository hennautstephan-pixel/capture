from capture_recovery.inference import Vector3Rule
from capture_recovery.models import DataType
from capture_recovery.structures import (
    Field,
    Structure,
)


def build_vector():

    s = Structure(
        name="Unknown",
        offset=100,
        length=12,
    )

    s.add(
        Field(
            "x",
            100,
            4,
            DataType.FLOAT32,
            1.0,
        )
    )

    s.add(
        Field(
            "y",
            104,
            4,
            DataType.FLOAT32,
            2.0,
        )
    )

    s.add(
        Field(
            "z",
            108,
            4,
            DataType.FLOAT32,
            3.0,
        )
    )

    return s


def test_match():

    rule = Vector3Rule()

    result = rule.match(
        build_vector()
    )

    assert result.matched
    assert result.structure_name == "Vector3"
    assert result.confidence > 0.9


def test_wrong_type():

    s = build_vector()

    s.fields[2].datatype = DataType.INT32

    result = Vector3Rule().match(s)

    assert not result.matched


def test_wrong_offset():

    s = build_vector()

    s.fields[2].offset = 120

    result = Vector3Rule().match(s)

    assert not result.matched