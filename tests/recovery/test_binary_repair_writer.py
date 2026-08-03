from capture_recovery.recovery import (
    BinaryRepairWriter,
    BinaryRepairOperation,
)


def test_binary_writer_creates_repaired_file(tmp_path):

    source = tmp_path / "original.c2p"

    output = tmp_path / "repaired.c2p"


    source.write_bytes(
        b"AAAAxxxxBBBB"
    )


    operation = BinaryRepairOperation(
        offset=4,
        original_size=4,
        replacement=b"YYYY",
    )


    writer = BinaryRepairWriter()


    result = writer.write_repaired_file(
        source,
        output,
        (
            operation,
        ),
    )


    assert output.exists()

    assert result.output == output

    assert (
        output.read_bytes()
        ==
        b"AAAAYYYYBBBB"
    )


def test_binary_writer_preserves_original(tmp_path):

    source = tmp_path / "original.c2p"

    output = tmp_path / "repaired.c2p"


    source.write_bytes(
        b"123456"
    )


    writer = BinaryRepairWriter()


    writer.write_repaired_file(
        source,
        output,
        (),
    )


    assert (
        source.read_bytes()
        ==
        b"123456"
    )