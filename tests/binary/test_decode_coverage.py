from capture_recovery.binary.decode_coverage import DecodeCoverage


def test_default_values() -> None:
    coverage = DecodeCoverage()

    assert coverage.total_objects == 0
    assert coverage.decoded_objects == 0
    assert coverage.unknown_objects == 0
    assert coverage.decoded_bytes == 0
    assert coverage.total_bytes == 0


def test_object_ratio_empty() -> None:
    coverage = DecodeCoverage()

    assert coverage.object_ratio == 0.0


def test_byte_ratio_empty() -> None:
    coverage = DecodeCoverage()

    assert coverage.byte_ratio == 0.0


def test_object_ratio() -> None:
    coverage = DecodeCoverage(
        total_objects=100,
        decoded_objects=75,
    )

    assert coverage.object_ratio == 0.75


def test_byte_ratio() -> None:
    coverage = DecodeCoverage(
        decoded_bytes=1500,
        total_bytes=2000,
    )

    assert coverage.byte_ratio == 0.75


def test_full_coverage() -> None:
    coverage = DecodeCoverage(
        total_objects=50,
        decoded_objects=50,
        decoded_bytes=4096,
        total_bytes=4096,
    )

    assert coverage.object_ratio == 1.0
    assert coverage.byte_ratio == 1.0


def test_no_decoded_objects() -> None:
    coverage = DecodeCoverage(
        total_objects=100,
        decoded_objects=0,
    )

    assert coverage.object_ratio == 0.0


def test_no_decoded_bytes() -> None:
    coverage = DecodeCoverage(
        decoded_bytes=0,
        total_bytes=1000,
    )

    assert coverage.byte_ratio == 0.0


def test_fractional_ratio() -> None:
    coverage = DecodeCoverage(
        total_objects=3,
        decoded_objects=1,
        total_bytes=3,
        decoded_bytes=1,
    )

    assert coverage.object_ratio == 1 / 3
    assert coverage.byte_ratio == 1 / 3


def test_unknown_objects_counter() -> None:
    coverage = DecodeCoverage(
        total_objects=10,
        decoded_objects=7,
        unknown_objects=3,
    )

    assert coverage.unknown_objects == 3
    assert coverage.decoded_objects + coverage.unknown_objects == coverage.total_objects