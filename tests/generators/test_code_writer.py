import pytest

from capture_recovery.generators.code_writer import CodeWriter


def test_empty():
    writer = CodeWriter()

    assert writer.render() == "\n"


def test_one_line():
    writer = CodeWriter()

    writer.line("hello")

    assert writer.render() == "hello\n"


def test_blank():
    writer = CodeWriter()

    writer.line("a")
    writer.blank()
    writer.line("b")

    assert writer.render() == "a\n\nb\n"


def test_indent():
    writer = CodeWriter()

    writer.line("class A:")
    writer.indent()
    writer.line("pass")

    assert writer.render() == (
        "class A:\n"
        "    pass\n"
    )


def test_dedent():
    writer = CodeWriter()

    writer.indent()
    writer.dedent()

    assert writer.indentation == 0


def test_negative_indent():
    writer = CodeWriter()

    with pytest.raises(ValueError):
        writer.dedent()


def test_extend():
    writer = CodeWriter()

    writer.extend(
        [
            "a",
            "b",
            "c",
        ]
    )

    assert writer.render() == (
        "a\n"
        "b\n"
        "c\n"
    )


def test_clear():
    writer = CodeWriter()

    writer.line("abc")
    writer.indent()

    writer.clear()

    assert writer.render() == "\n"
    assert writer.indentation == 0