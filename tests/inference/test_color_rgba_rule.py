from capture_recovery.inference import ColorRGBARule
from capture_recovery.models import DataType
from capture_recovery.structures import (
    Field,
    Structure,
)


def build():

    s = Structure(
        name="Unknown",
        offset=100,
        length=16,
    )

    values = [1.0, 0.5, 0.25, 1.0]

    for i, value in enumerate(values):

        s.add(
            Field(
                name=f"c{i}",
                offset=100 + i * 4,
                length=4,
                datatype=DataType.FLOAT32,
                value=value,
            )
        )

    return s


def test_match():

    result = ColorRGBARule().match(build())

    assert result.matched
    assert result.structure_name == "ColorRGBA"


def test_outside_range():

    s = build()

    s.fields[2].value = 5.0

    result = ColorRGBARule().match(s)

    assert not result.matched


def test_wrong_datatype():

    s = build()

    s.fields[1].datatype = DataType.INT32

    result = ColorRGBARule().match(s)

    assert not result.matched