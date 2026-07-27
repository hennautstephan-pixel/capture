from capture_recovery.decoders.fixture_decoder import FixtureDecoder
from capture_recovery.knowledge.signature_engine import SignatureEngine
from capture_recovery.knowledge.signature_registry import SignatureRegistry
from capture_recovery.knowledge.signatures.fixture_signature import (
    FIXTURE_SIGNATURE,
)
from capture_recovery.knowledge.semantic_object import SemanticObject
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field
from capture_recovery.structures.structure import Structure


def create_fixture_structure():
    structure = Structure(
        name="Fixture",
        offset=0,
        length=100,
    )

    structure.add(
        Field(
            name="name",
            offset=0,
            length=10,
            datatype=DataType.STRING,
            value="Mac Aura",
        )
    )

    structure.add(
        Field(
            name="universe",
            offset=10,
            length=2,
            datatype=DataType.UINT16,
            value=1,
        )
    )

    structure.add(
        Field(
            name="address",
            offset=12,
            length=2,
            datatype=DataType.UINT16,
            value=10,
        )
    )

    structure.add(
        Field(
            name="manufacturer",
            offset=14,
            length=10,
            datatype=DataType.STRING,
            value="Martin",
        )
    )

    structure.add(
        Field(
            name="model",
            offset=24,
            length=10,
            datatype=DataType.STRING,
            value="MAC Aura",
        )
    )

    return structure


def create_decoder():
    registry = SignatureRegistry()

    registry.register(
        "Fixture",
        FIXTURE_SIGNATURE,
    )

    engine = SignatureEngine(
        registry,
    )

    return FixtureDecoder(
        engine,
    )


def test_fixture_decoder_accepts_fixture_structure():

    decoder = create_decoder()

    structure = create_fixture_structure()

    assert decoder.can_decode(
        structure,
    ) is True


def test_fixture_decoder_decodes_fixture_structure():

    decoder = create_decoder()

    structure = create_fixture_structure()

    result = decoder.decode(
        structure,
    )

    assert isinstance(
        result,
        SemanticObject,
    )

    assert result.object_type == "Fixture"

    assert result.identifier == "Mac Aura"

    assert result.get(
        "name",
    ) == "Mac Aura"

    assert result.get(
        "universe",
    ) == 1

    assert result.get(
        "address",
    ) == 10

    assert result.get(
        "manufacturer",
    ) == "Martin"

    assert result.get(
        "model",
    ) == "MAC Aura"


def test_fixture_decoder_confidence():

    decoder = create_decoder()

    result = decoder.decode(
        create_fixture_structure(),
    )

    assert result is not None

    assert result.confidence > 0

    assert result.confidence < 1.0


def test_fixture_decoder_rejects_empty_structure():

    decoder = create_decoder()

    structure = Structure(
        name="Unknown",
        offset=0,
        length=10,
    )

    assert decoder.can_decode(
        structure,
    ) is False

    assert decoder.decode(
        structure,
    ) is None