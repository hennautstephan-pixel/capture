from pathlib import Path

from capture_recovery.research import (
    ReferenceProjectAnalyzer,
    ReferenceProjectModel,
)



def test_reference_project_analyzer(tmp_path):

    project = tmp_path / "reference.c2p"


    project.write_bytes(
        b"CAPTURE_REFERENCE_DATA"
    )


    analyzer = ReferenceProjectAnalyzer(
        block_size=8
    )


    result = analyzer.analyze(
        project
    )


    assert isinstance(
        result,
        ReferenceProjectModel,
    )


    assert (
        result.size
        ==
        len(
            b"CAPTURE_REFERENCE_DATA"
        )
    )


    assert len(
        result.blocks
    ) == 3



def test_reference_blocks_have_signature(tmp_path):

    project = tmp_path / "reference.c2p"


    project.write_bytes(
        b"ABCDEFGH"
    )


    result = (
        ReferenceProjectAnalyzer(
            block_size=4
        )
        .analyze(project)
    )


    assert len(
        result.blocks
    ) == 2


    assert (
        result.blocks[0].signature
        !=
        result.blocks[1].signature
    )