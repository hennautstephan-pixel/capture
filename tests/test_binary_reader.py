from pathlib import Path

from src.capture_recovery.binary_reader import BinaryReader


def test_binary_reader_size(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(b"abcdef")

    with BinaryReader(filename) as reader:

        assert reader.size == 6

def test_binary_reader_read(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(b"abcdef")

    with BinaryReader(filename) as reader:

        assert reader.read(3) == b"abc"

import pytest

from src.capture_recovery.binary_reader import BinaryReader


def test_binary_reader_requires_open(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(b"abc")

    reader = BinaryReader(filename)

    with pytest.raises(RuntimeError):
        reader.read(1)


from src.capture_recovery.binary_reader import BinaryReader


def test_binary_reader_open_close(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(b"abcdef")

    reader = BinaryReader(filename)

    reader.open()

    assert reader.read(3) == b"abc"

    reader.close()

    assert reader.file is None

from src.capture_recovery.binary_reader import BinaryReader


def test_binary_reader_read_safe(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(b"abc")

    with BinaryReader(filename) as reader:

        data = reader.read_safe(10)

        assert data == b"abc"

        assert reader.eof

from src.capture_recovery.binary_reader import BinaryReader


def test_binary_reader_peek(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(b"abcdef")

    with BinaryReader(filename) as reader:

        assert reader.tell() == 0

        data = reader.peek(3)

        assert data == b"abc"

        # Le curseur ne doit pas avoir bougé
        assert reader.tell() == 0

        # Une vraie lecture doit retourner les mêmes octets
        assert reader.read(3) == b"abc"

def test_binary_reader_find(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(
        b"\x00ABC\x00ABC\x00"
    )

    with BinaryReader(filename) as reader:

        assert reader.find(b"ABC") == 1

        assert reader.find(b"XYZ") == -1

def test_binary_reader_find_all(tmp_path):

    filename = tmp_path / "sample.bin"

    filename.write_bytes(
        b"ABCxxxABCxxABC"
    )

    with BinaryReader(filename) as reader:

        positions = list(
            reader.find_all(b"ABC")
        )

    assert positions == [0, 6, 11]