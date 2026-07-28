from capture_recovery.pipeline import (
    BinaryAnalyzer,
)


def test_binary_analyzer():

    analyzer = (
        BinaryAnalyzer()
    )


    data = (

        b"Fixture"

        + b"\x01\x00"

        + b"Test"

    )


    result = (
        analyzer.summary(
            data,
        )
    )


    assert result["size"] == (
        len(data)
    )


    assert result["index"] is not None