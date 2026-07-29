from capture_recovery.parser.binary_report import BinaryReport
from capture_recovery.parser.segment import Segment


def test_empty_report():

    assert BinaryReport.generate([]) == "No segments detected."


def test_single_segment():

    report = BinaryReport.generate([
        Segment(
            offset=16,
            length=5,
            kind="ascii",
            metadata={
                "value": "Hello",
            },
        )
    ])

    assert "ascii" in report
    assert "Hello" in report
    assert "00000010" in report


def test_sorted_output():

    report = BinaryReport.generate([
        Segment(offset=100, length=5, kind="b"),
        Segment(offset=10, length=5, kind="a"),
    ])

    lines = report.splitlines()

    assert "0000000A" in lines[2]
    assert "00000064" in lines[3]


def test_multiple_segments():

    report = BinaryReport.generate([
        Segment(offset=0, length=4, kind="ascii"),
        Segment(offset=10, length=8, kind="binary"),
    ])

    assert "ascii" in report
    assert "binary" in report