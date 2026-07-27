from capture_recovery.decoders.cue_decoder import CueDecoder
from capture_recovery.knowledge.signature_engine import SignatureEngine
from capture_recovery.knowledge.signature_registry import SignatureRegistry
from capture_recovery.knowledge.signatures.cue_signature import (
    CUE_SIGNATURE,
)
from capture_recovery.knowledge.semantic_object import SemanticObject
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field
from capture_recovery.structures.structure import Structure


def create_cue_structure():
    structure = Structure(
        name="Cue",
        offset=0,
        length=100,
    )

    structure.add(
        Field(
            name="name",
            offset=0,
            length=20,
            datatype=DataType.STRING,
            value="Intro",
        )
    )

    structure.add(
        Field(
            name="cue_number",
            offset=20,
            length=2,
            datatype=DataType.UINT16,
            value=1,
        )
    )

    return structure


def create_decoder():

    registry = SignatureRegistry()

    registry.register(
        "Cue",
        CUE_SIGNATURE,
    )

    engine = SignatureEngine(
        registry,
    )

    return CueDecoder(
        engine,
    )


def test_cue_decoder_accepts_cue_structure():

    decoder = create_decoder()

    structure = create_cue_structure()

    assert decoder.can_decode(
        structure,
    ) is True


def test_cue_decoder_decodes_cue_structure():

    decoder = create_decoder()

    structure = create_cue_structure()

    result = decoder.decode(
        structure,
    )

    assert isinstance(
        result,
        SemanticObject,
    )

    assert result.object_type == "Cue"

    assert result.identifier == "Intro"

    assert result.get(
        "name",
    ) == "Intro"

    assert result.get(
        "cue_number",
    ) == 1


def test_cue_decoder_confidence():

    decoder = create_decoder()

    result = decoder.decode(
        create_cue_structure(),
    )

    assert result is not None

    assert result.confidence > 0


def test_cue_decoder_rejects_empty_structure():

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