from capture_recovery.python.python_constant import PythonConstant


def test_defaults():
    constant = PythonConstant(
        "NAME",
        '"Fixture"',
    )

    assert constant.name == "NAME"
    assert constant.value == '"Fixture"'
    assert constant.documentation == ""
    assert constant.has_documentation is False


def test_render():
    constant = PythonConstant(
        "FIELD_COUNT",
        "2",
    )

    assert constant.render() == "FIELD_COUNT = 2"


def test_documentation():
    constant = PythonConstant(
        "NAME",
        '"Fixture"',
        documentation="Object name",
    )

    assert constant.has_documentation is True