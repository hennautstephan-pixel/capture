from pathlib import Path

from capture_recovery.generators.generated_file import GeneratedFile


def test_filename():
    file = GeneratedFile(
        path=Path("models/fixture.py"),
        content="pass",
    )

    assert file.name == "fixture.py"


def test_stem():
    file = GeneratedFile(
        path=Path("models/fixture.py"),
        content="pass",
    )

    assert file.stem == "fixture"


def test_suffix():
    file = GeneratedFile(
        path=Path("models/fixture.py"),
        content="pass",
    )

    assert file.suffix == ".py"


def test_with_content():
    file = GeneratedFile(
        path=Path("models/fixture.py"),
        content="old",
    )

    updated = file.with_content("new")

    assert updated.content == "new"
    assert updated.path == file.path
    assert updated.encoding == "utf-8"
    assert updated is not file


def test_str():
    file = GeneratedFile(
        path=Path("models/fixture.py"),
        content="",
    )

    assert str(file) == "models/fixture.py"