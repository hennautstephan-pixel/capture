from capture_recovery.python.python_import import PythonImport


def test_plain_import():
    imp = PythonImport("pathlib")

    assert imp.render() == "import pathlib"


def test_plain_import_alias():
    imp = PythonImport(
        module="numpy",
        alias="np",
    )

    assert imp.render() == "import numpy as np"


def test_from_import():
    imp = PythonImport(
        module="dataclasses",
        names=("dataclass",),
    )

    assert imp.render() == (
        "from dataclasses import dataclass"
    )


def test_multiple_names():
    imp = PythonImport(
        module="typing",
        names=("Any", "Iterable"),
    )

    assert imp.render() == (
        "from typing import Any, Iterable"
    )


def test_is_plain_import():
    imp = PythonImport("pathlib")

    assert imp.is_plain_import
    assert not imp.is_from_import


def test_is_from_import():
    imp = PythonImport(
        module="typing",
        names=("Any",),
    )

    assert imp.is_from_import
    assert not imp.is_plain_import


def test_ordering():
    a = PythonImport("abc")
    b = PythonImport("typing")

    assert a < b


def test_equality():
    assert (
        PythonImport("typing")
        == PythonImport("typing")
    )