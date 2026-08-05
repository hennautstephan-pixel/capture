from capture_recovery.reconstruction import (
    CorruptionAnalyzer,
)



def test_detect_corruption_region():

    analyzer = CorruptionAnalyzer()


    result = analyzer.analyze(
        b"AAZZBB",
        b"AAXXBB",
    )


    assert result.corrupted_bytes == 2


    assert len(
        result.regions
    ) == 1


    assert (
        result.regions[0].offset
        ==
        2
    )


    assert (
        result.regions[0].size
        ==
        2
    )



def test_no_corruption():

    analyzer = CorruptionAnalyzer()


    result = analyzer.analyze(
        b"AAAA",
        b"AAAA",
    )


    assert result.corrupted_bytes == 0

    assert result.regions == ()