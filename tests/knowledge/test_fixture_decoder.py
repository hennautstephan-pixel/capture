from __future__ import annotations

from capture_recovery.knowledge.decoders.fixture_decoder import FixtureDecoder
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field
from capture_recovery.structures.structure import Structure


def make_structure(*fields: Field) -> Structure:
    structure = Structure(
        name="FixtureCandidate",
        offset=100,
        length=64,
    )

    for field in fields:
        structure.add(field)

    return structure


def make_field(
    name: str,
    value,
    datatype: DataType = DataType.STRING,
) -> Field:

    return Field(
        name=name,
        offset=0,
        length=4,
        datatype=datatype,
        value=value,
    )


def test_empty_structure():

    decoder = FixtureDecoder()

    structure = make_structure()

    assert decoder.score(structure) == 0
    assert decoder.can_decode(structure) is False
    assert decoder.decode(structure) is None


def test_name_only():

    decoder = FixtureDecoder()

    structure = make_structure(
        make_field("name", "PAR64"),
    )

    assert decoder.score(structure) == 30
    assert decoder.can_decode(structure) is False


def test_name_universe():

    decoder = FixtureDecoder()

    structure = make_structure(
        make_field("name", "PAR64"),
        make_field("universe", 1, DataType.UINT16),
    )

    assert decoder.score(structure) == 50
    assert decoder.can_decode(structure) is False


def test_fixture_candidate():

    decoder = FixtureDecoder()

    structure = make_structure(
        make_field("name", "PAR64"),
        make_field("universe", 1, DataType.UINT16),
        make_field("address", 25, DataType.UINT16),
        make_field("position", (1.0, 2.0, 3.0)),
    )

    assert decoder.score(structure) == 90
    assert decoder.can_decode(structure)


def test_decode():

    decoder = FixtureDecoder()

    structure = make_structure(
        make_field("name", "PAR64"),
        make_field("universe", 1, DataType.UINT16),
        make_field("address", 25, DataType.UINT16),
        make_field("position", (10.0, 20.0, 30.0)),
        make_field("rotation", (0.0, 90.0, 0.0)),
    )

    fixture = decoder.decode(structure)

    assert fixture is not None

    assert fixture.name == "PAR64"

    assert fixture.universe == 1

    assert fixture.address == 25

    assert fixture.position == (10.0, 20.0, 30.0)

    assert fixture.rotation == (0.0, 90.0, 0.0)


def test_identifier_defaults_to_name():

    decoder = FixtureDecoder()

    structure = make_structure(
        make_field("name", "Spot001"),
        make_field("universe", 1, DataType.UINT16),
        make_field("address", 1, DataType.UINT16),
        make_field("position", (0.0, 0.0, 0.0)),
    )

    fixture = decoder.decode(structure)

    assert fixture.identifier == "Spot001"


def test_identifier_defaults_to_offset():

    decoder = FixtureDecoder()

    structure = Structure(
        name="Unknown",
        offset=512,
        length=64,
    )

    structure.add(make_field("universe", 1, DataType.UINT16))
    structure.add(make_field("address", 1, DataType.UINT16))
    structure.add(make_field("position", (0.0, 0.0, 0.0)))
    structure.add(make_field("rotation", (0.0, 0.0, 0.0)))

    fixture = decoder.decode(structure)

    assert fixture is not None
    assert fixture.identifier == "fixture@512"


def test_invalid_integer():

    decoder = FixtureDecoder()

    structure = make_structure(
        make_field("name", "PAR"),
        make_field("universe", "abc"),
        make_field("address", 1, DataType.UINT16),
        make_field("position", (0.0, 0.0, 0.0)),
    )

    fixture = decoder.decode(structure)

    assert fixture is not None
    assert fixture.universe is None


def test_invalid_position():

    decoder = FixtureDecoder()

    structure = make_structure(
        make_field("name", "PAR"),
        make_field("universe", 1, DataType.UINT16),
        make_field("address", 1, DataType.UINT16),
        make_field("position", (1.0, 2.0)),
    )

    fixture = decoder.decode(structure)

    assert fixture is not None
    assert fixture.position is None


def test_case_insensitive_field_names():

    decoder = FixtureDecoder()

    structure = make_structure(
        make_field("Name", "PAR64"),
        make_field("Universe", 1, DataType.UINT16),
        make_field("Address", 10, DataType.UINT16),
        make_field("Position", (1.0, 2.0, 3.0)),
    )

    assert decoder.can_decode(structure)