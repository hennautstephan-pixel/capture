from __future__ import annotations

from capture_recovery.research import (
    CorpusPatterns,
    PatternMerger,
    PatternRegion,
)


def test_empty():

    merger = PatternMerger()

    merged = merger.merge(
        CorpusPatterns([])
    )

    assert merged.region_count == 0


def test_single_region():

    merger = PatternMerger()

    merged = merger.merge(
        CorpusPatterns(
            [
                PatternRegion(
                    100,
                    10,
                    5,
                )
            ]
        )
    )

    assert merged.region_count == 1

    region = merged.regions[0]

    assert region.offset == 100

    assert region.length == 10

    assert region.occurrence_count == 5

    assert len(region.merged_regions) == 1


def test_overlapping_regions():

    merger = PatternMerger()

    merged = merger.merge(
        CorpusPatterns(
            [
                PatternRegion(
                    100,
                    10,
                    2,
                ),
                PatternRegion(
                    105,
                    8,
                    3,
                ),
            ]
        )
    )

    assert merged.region_count == 1

    region = merged.regions[0]

    assert region.offset == 100

    assert region.length == 13

    assert region.occurrence_count == 5


def test_gap():

    merger = PatternMerger()

    merged = merger.merge(
        CorpusPatterns(
            [
                PatternRegion(
                    100,
                    10,
                    1,
                ),
                PatternRegion(
                    111,
                    5,
                    1,
                ),
            ]
        ),
        max_gap=1,
    )

    assert merged.region_count == 1


def test_no_gap():

    merger = PatternMerger()

    merged = merger.merge(
        CorpusPatterns(
            [
                PatternRegion(
                    100,
                    10,
                    1,
                ),
                PatternRegion(
                    111,
                    5,
                    1,
                ),
            ]
        )
    )

    assert merged.region_count == 2


def test_disjoint():

    merger = PatternMerger()

    merged = merger.merge(
        CorpusPatterns(
            [
                PatternRegion(
                    100,
                    10,
                    2,
                ),
                PatternRegion(
                    300,
                    5,
                    4,
                ),
            ]
        )
    )

    assert merged.region_count == 2


def test_sorted():

    merger = PatternMerger()

    merged = merger.merge(
        CorpusPatterns(
            [
                PatternRegion(
                    300,
                    5,
                    1,
                ),
                PatternRegion(
                    100,
                    5,
                    1,
                ),
            ]
        )
    )

    assert merged.regions[0].offset == 100