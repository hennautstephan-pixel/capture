from capture_recovery.reconstruction import (
    BinarySimilarity,
)



def test_binary_similarity_identical():

    analyzer = BinarySimilarity()


    result = analyzer.compare(
        b"ABCDEF",
        b"ABCDEF",
    )


    assert result.score == 1.0

    assert result.matching_bytes == 6



def test_binary_similarity_partial():

    analyzer = BinarySimilarity()


    result = analyzer.compare(
        b"ABCDEF",
        b"ABXYEF",
    )


    assert (
        result.score
        ==
        4 / 6
    )



def test_binary_similarity_empty():

    analyzer = BinarySimilarity()


    assert (
        analyzer.score(
            b"",
            b"",
        )
        ==
        1.0
    )