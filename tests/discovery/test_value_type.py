from capture_recovery.discovery import ValueType


def test_string_values():

    assert ValueType.FLOAT32 == "float32"
    assert ValueType.UINT16 == "uint16"
    assert ValueType.BOOL == "bool"


def test_integer_types():

    assert ValueType.INT8.is_integer
    assert ValueType.INT16.is_integer
    assert ValueType.INT32.is_integer
    assert ValueType.INT64.is_integer

    assert ValueType.UINT8.is_integer
    assert ValueType.UINT16.is_integer
    assert ValueType.UINT32.is_integer
    assert ValueType.UINT64.is_integer


def test_float_types():

    assert ValueType.FLOAT32.is_float
    assert ValueType.FLOAT64.is_float


def test_numeric_types():

    assert ValueType.FLOAT32.is_numeric
    assert ValueType.INT32.is_numeric
    assert ValueType.UINT64.is_numeric

    assert not ValueType.STRING.is_numeric
    assert not ValueType.BYTES.is_numeric
    assert not ValueType.BOOL.is_numeric
    assert not ValueType.UNKNOWN.is_numeric


def test_signed_types():

    assert ValueType.INT8.is_signed
    assert ValueType.INT16.is_signed
    assert ValueType.INT32.is_signed
    assert ValueType.INT64.is_signed

    assert not ValueType.UINT32.is_signed
    assert not ValueType.FLOAT32.is_signed


def test_unsigned_types():

    assert ValueType.UINT8.is_unsigned
    assert ValueType.UINT16.is_unsigned
    assert ValueType.UINT32.is_unsigned
    assert ValueType.UINT64.is_unsigned

    assert not ValueType.INT32.is_unsigned
    assert not ValueType.FLOAT64.is_unsigned


def test_enum_lookup():

    assert ValueType("float32") is ValueType.FLOAT32
    assert ValueType("uint16") is ValueType.UINT16
    assert ValueType("string") is ValueType.STRING


def test_enum_names():

    assert ValueType.FLOAT32.name == "FLOAT32"
    assert ValueType.FLOAT32.value == "float32"