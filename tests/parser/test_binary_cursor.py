from capture_recovery.parser import BinaryCursor


def test_u8():

    cursor = BinaryCursor(
        b"\x05"
    )

    assert cursor.read_u8() == 5


def test_u16():

    cursor = BinaryCursor(
        b"\x34\x12"
    )

    assert cursor.read_u16() == 0x1234


def test_u32():

    cursor = BinaryCursor(
        b"\x78\x56\x34\x12"
    )

    assert cursor.read_u32() == 0x12345678


def test_float():

    cursor = BinaryCursor(
        b"\x00\x00\x80\x3f"
    )

    assert cursor.read_float() == 1.0


def test_seek():

    cursor = BinaryCursor(
        b"abcdef"
    )

    cursor.seek(3)

    assert cursor.read_bytes(2) == b"de"


def test_string():

    cursor = BinaryCursor(
        b"Capture\x00ABC"
    )

    assert cursor.read_string(11) == "Capture"