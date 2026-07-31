from pathlib import Path

from capture_recovery.benchmark import SampleLoader


def test_missing_directory(tmp_path: Path):

    loader = SampleLoader(
        tmp_path / "missing"
    )

    assert loader.exists() is False
    assert loader.load() == []
    assert loader.count() == 0


def test_empty_directory(tmp_path: Path):

    loader = SampleLoader(tmp_path)

    assert loader.exists() is True
    assert loader.load() == []
    assert loader.count() == 0


def test_single_file(tmp_path: Path):

    (tmp_path / "project.c2p").write_bytes(b"")

    loader = SampleLoader(tmp_path)

    files = loader.load()

    assert len(files) == 1
    assert files[0].name == "project.c2p"
    assert loader.count() == 1


def test_recursive(tmp_path: Path):

    sub = tmp_path / "sub"

    sub.mkdir()

    (tmp_path / "a.c2p").write_bytes(b"")
    (sub / "b.c2p").write_bytes(b"")
    (sub / "ignore.txt").write_text("x")

    loader = SampleLoader(tmp_path)

    files = loader.load()

    assert len(files) == 2

    assert {
        file.name
        for file in files
    } == {
        "a.c2p",
        "b.c2p",
    }


def test_sorted(tmp_path: Path):

    (tmp_path / "z.c2p").write_bytes(b"")
    (tmp_path / "a.c2p").write_bytes(b"")
    (tmp_path / "m.c2p").write_bytes(b"")

    loader = SampleLoader(tmp_path)

    names = [
        file.name
        for file in loader.load()
    ]

    assert names == [
        "a.c2p",
        "m.c2p",
        "z.c2p",
    ]


def test_iter(tmp_path: Path):

    (tmp_path / "b.c2p").write_bytes(b"")
    (tmp_path / "a.c2p").write_bytes(b"")

    loader = SampleLoader(tmp_path)

    assert [
        file.name
        for file in loader
    ] == [
        "a.c2p",
        "b.c2p",
    ]


def test_len(tmp_path: Path):

    (tmp_path / "a.c2p").write_bytes(b"")
    (tmp_path / "b.c2p").write_bytes(b"")

    loader = SampleLoader(tmp_path)

    assert len(loader) == 2