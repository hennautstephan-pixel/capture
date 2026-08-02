from capture_recovery.tools import (
    DiffAnalyzer,
    DiffRegion,
    StreamDiff,
    StreamDifference,
)


def test_identical_stream():

    diff = StreamDiff(
        left_size=10,
        right_size=10,
        differences=(),
    )

    analyzer = DiffAnalyzer()

    result = analyzer.analyze(
        diff,
    )

    assert result.region_count == 0
    assert result.regions == ()


def test_single_difference():

    diff = StreamDiff(
        left_size=10,
        right_size=10,
        differences=(
            StreamDifference(
                offset=5,
                left=1,
                right=2,
            ),
        ),
    )

    analyzer = DiffAnalyzer()

    result = analyzer.analyze(
        diff,
    )

    assert result.region_count == 1

    region = result.regions[0]

    assert isinstance(
        region,
        DiffRegion,
    )

    assert region.start_offset == 5
    assert region.end_offset == 5
    assert region.size == 1


def test_multiple_separated_regions():

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

    analyzer = DiffAnalyzer()

    result = analyzer.analyze(
        diff,
    )

    assert result.region_count == 3

    assert result.regions[0].start_offset == 1
    assert result.regions[0].end_offset == 1

    assert result.regions[1].start_offset == 5
    assert result.regions[1].end_offset == 5

    assert result.regions[2].start_offset == 12
    assert result.regions[2].end_offset == 12


def test_contiguous_differences_are_grouped():

    diff = StreamDiff(
        left_size=20,
        right_size=20,
        differences=(
            StreamDifference(
                offset=100,
                left=1,
                right=2,
            ),
            StreamDifference(
                offset=101,
                left=3,
                right=4,
            ),
            StreamDifference(
                offset=102,
                left=5,
                right=6,
            ),
        ),
    )

    analyzer = DiffAnalyzer()

    result = analyzer.analyze(
        diff,
    )

    assert result.region_count == 1

    region = result.regions[0]

    assert region.start_offset == 100
    assert region.end_offset == 102
    assert region.size == 3

    assert len(region.differences) == 3


def test_region_size():

    region = DiffRegion(
        start_offset=50,
        end_offset=59,
        differences=(),
    )

    assert region.size == 10