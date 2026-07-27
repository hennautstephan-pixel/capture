from capture_recovery.decoders.universe_decoder import UniverseDecoder
from capture_recovery.knowledge.signature_engine import SignatureEngine
from capture_recovery.knowledge.signature_registry import SignatureRegistry
from capture_recovery.knowledge.signatures.universe_signature import (
    UNIVERSE_SIGNATURE,
)
from capture_recovery.knowledge.semantic_object import SemanticObject
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field
from capture_recovery.structures.structure import Structure


def create_universe_structure():
    structure = Structure(
        name="Universe",
        offset=0,
        length=50,
    )

    structure.add(
        Field(
            name="name",
            offset=0,
            length=10,
            datatype=DataType.STRING,
            value="Universe 1",
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
            name="protocol",
            offset=12,
            length=5,
            datatype=DataType.STRING,
            value="sACN",
        )
    )

    return structure


def create_decoder():
    registry = SignatureRegistry()

    registry.register(
        "Universe",
        UNIVERSE_SIGNATURE,
    )

    engine = SignatureEngine(
        registry,
    )

    return UniverseDecoder(
        engine,
    )


def test_universe_decoder_accepts_universe_structure():

    decoder = create_decoder()

    structure = create_universe_structure()

    assert decoder.can_decode(
        structure,
    ) is True


def test_universe_decoder_decodes_universe_structure():

    decoder = create_decoder()

    structure = create_universe_structure()

    result = decoder.decode(
        structure,
    )

    assert isinstance(
        result,
        SemanticObject,
    )

    assert result.object_type == "Universe"

    assert result.identifier == "Universe 1"

    assert result.get(
        "name",
    ) == "Universe 1"

    assert result.get(
        "universe",
    ) == 1

    assert result.get(
        "protocol",
    ) == "sACN"


def test_universe_decoder_confidence():

    decoder = create_decoder()

    result = decoder.decode(
        create_universe_structure(),
    )

    assert result is not None

    assert result.confidence > 0


def test_universe_decoder_rejects_empty_structure():

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