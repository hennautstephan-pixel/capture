from capture_recovery.tools import (
    StreamDiff,
    StreamDifference,
)


def test_identical():

    diff = StreamDiff(
        left_size=10,
        right_size=10,
        differences=(),
    )

    assert diff.identical

    assert diff.difference_count == 0


def test_difference():

    diff = StreamDiff(
        left_size=10,
        right_size=10,
        differences=(
            StreamDifference(
                offset=0,
                left=1,
                right=2,
            ),
        ),
    )

    assert not diff.identical

    assert diff.difference_count == 1


def test_multiple_differences():

    diff = StreamDiff(
        left_size=20,
        right_size=20,
        differences=(
            StreamDifference(
                offset=1,
                left=10,
                right=11,
            ),
            StreamDifference(
                offset=5,
                left=20,
                right=21,
            ),
            StreamDifference(
                offset=12,
                left=30,
                right=31,
            ),
        ),
    )

    assert diff.difference_count == 3

    assert not diff.identical


def test_different_sizes():

    diff = StreamDiff(
        left_size=100,
        right_size=120,
        differences=(
            StreamDifference(
                offset=100,
                left=-1,
                right=42,
            ),
        ),
    )

    assert diff.left_size == 100

    assert diff.right_size == 120

    assert diff.difference_count == 1