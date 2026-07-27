from capture_recovery.python.python_field import PythonField


def test_without_default():
    field = PythonField(
        name="manufacturer",
        annotation="str",
    )

    assert field.render() == "manufacturer: str"


def test_string_default():
    field = PythonField(
        name="manufacturer",
        annotation="str",
        default="ADB",
    )

    assert field.render() == (
        "manufacturer: str = 'ADB'"
    )


def test_integer_default():
    field = PythonField(
        name="universe",
        annotation="int",
        default=1,
    )

    assert field.render() == (
        "universe: int = 1"
    )


def test_boolean_default():
    field = PythonField(
        name="enabled",
        annotation="bool",
        default=True,
    )

    assert field.render() == (
        "enabled: bool = True"
    )


def test_has_default():
    field = PythonField(
        name="value",
        annotation="int",
        default=42,
    )

    assert field.has_default


def test_without_default_flag():
    field = PythonField(
        name="value",
        annotation="int",
    )

    assert not field.has_default


def test_documentation():
    field = PythonField(
        name="manufacturer",
        annotation="str",
        documentation="Fixture manufacturer",
    )

    assert field.documentation == "Fixture manufacturer"


def test_repr():
    field = PythonField(
        name="manufacturer",
        annotation="str",
    )

    assert "manufacturer" in repr(field)