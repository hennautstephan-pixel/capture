from capture_recovery.parser.entropy import EntropyAnalyzer


def test_empty_buffer():
    result = EntropyAnalyzer.analyze(b"")

    assert result.size == 0
    assert result.entropy == 0.0
    assert result.distinct_bytes == 0
    assert result.zero_ratio == 0.0
    assert result.printable_ratio == 0.0
    assert sum(result.histogram) == 0


def test_zero_buffer():
    result = EntropyAnalyzer.analyze(bytes(100))

    assert result.size == 100
    assert result.entropy == 0.0
    assert result.distinct_bytes == 1
    assert result.zero_ratio == 1.0
    assert result.printable_ratio == 0.0
    assert result.histogram[0] == 100


def test_ascii_buffer():
    data = b"Hello World"

    result = EntropyAnalyzer.analyze(data)

    assert result.size == len(data)
    assert result.zero_ratio == 0.0
    assert result.printable_ratio == 1.0
    assert result.entropy > 0.0


def test_distinct_bytes():
    data = bytes(range(256))

    result = EntropyAnalyzer.analyze(data)

    assert result.distinct_bytes == 256
    assert result.histogram[0] == 1
    assert result.histogram[255] == 1


def test_uniform_distribution_entropy():
    data = bytes(range(256))

    result = EntropyAnalyzer.analyze(data)

    assert abs(result.entropy - 8.0) < 1e-9


def test_histogram_counts():
    data = bytes([1, 1, 1, 2, 2, 3])

    result = EntropyAnalyzer.analyze(data)

    assert result.histogram[1] == 3
    assert result.histogram[2] == 2
    assert result.histogram[3] == 1


def test_bytearray_supported():
    data = bytearray(b"Capture")

    result = EntropyAnalyzer.analyze(data)

    assert result.size == len(data)


def test_memoryview_supported():
    data = memoryview(b"Capture")

    result = EntropyAnalyzer.analyze(data)

    assert result.size == len(data)


def test_printable_ratio():
    data = bytes([65, 66, 67, 0])

    result = EntropyAnalyzer.analyze(data)

    assert result.printable_ratio == 0.75
    assert result.zero_ratio == 0.25


def test_entropy_increases():
    low = EntropyAnalyzer.analyze(bytes(256))
    high = EntropyAnalyzer.analyze(bytes(range(256)))

    assert low.entropy < high.entropy