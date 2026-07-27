from capture_recovery.python.python_method import PythonMethod


def test_defaults():
    method = PythonMethod("decode")

    assert method.name == "decode"
    assert method.parameters == ()
    assert method.decorators == ()
    assert method.body == ()
    assert method.return_type == ""

    assert method.parameter_count == 0
    assert method.decorator_count == 0
    assert method.line_count == 0
    assert method.has_return_type is False


def test_add_parameter():
    method = (
        PythonMethod("decode")
        .add_parameter("reader: BinaryReader")
        .add_parameter("version: int")
    )

    assert method.parameters == (
        "reader: BinaryReader",
        "version: int",
    )

    assert method.parameter_count == 2


def test_add_decorator():
    method = (
        PythonMethod("decode")
        .add_decorator("staticmethod")
        .add_decorator("final")
    )

    assert method.decorators == (
        "staticmethod",
        "final",
    )

    assert method.decorator_count == 2


def test_add_line():
    method = (
        PythonMethod("decode")
        .add_line("value = reader.read_uint32()")
        .add_line("return value")
    )

    assert method.body == (
        "value = reader.read_uint32()",
        "return value",
    )

    assert method.line_count == 2


def test_return_type():
    method = PythonMethod(
        name="decode",
        return_type="Fixture",
    )

    assert method.return_type == "Fixture"
    assert method.has_return_type is True


def test_immutable():
    original = PythonMethod("decode")

    updated = original.add_parameter("reader: BinaryReader")

    assert original.parameters == ()
    assert updated.parameters == (
        "reader: BinaryReader",
    )