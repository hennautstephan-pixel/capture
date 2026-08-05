from capture_recovery.cli import (
    DiffBuilder,
    StreamDiff,
)



def test_diff_builder_identical(tmp_path):

    file_a = tmp_path / "a.c2p"

    file_b = tmp_path / "b.c2p"


    file_a.write_bytes(
        b"CAPTURE"
    )

    file_b.write_bytes(
        b"CAPTURE"
    )


    diff = DiffBuilder().compare(
        file_a,
        file_b,
    )


    assert isinstance(
        diff,
        StreamDiff,
    )

    assert diff.identical



def test_diff_builder_detects_difference(tmp_path):

    file_a = tmp_path / "a.c2p"

    file_b = tmp_path / "b.c2p"


    file_a.write_bytes(
        b"AAAA"
    )

    file_b.write_bytes(
        b"AAAB"
    )


    diff = DiffBuilder().compare(
        file_a,
        file_b,
    )


    assert not diff.identical

    assert len(
        diff.differences
    ) == 1

    assert (
        diff.differences[0].offset
        ==
        3
    )