from __future__ import annotations

import math
import os

import pytest

from capture_recovery.binary.entropy import shannon_entropy


def test_empty_data() -> None:
    assert shannon_entropy(b"") == 0.0


def test_single_byte() -> None:
    assert shannon_entropy(b"\x00") == 0.0


def test_repeated_byte() -> None:
    assert shannon_entropy(b"\xAA" * 1024) == 0.0


def test_two_equal_values() -> None:
    data = b"\x00\xFF" * 512

    entropy = shannon_entropy(data)

    assert entropy == pytest.approx(1.0, abs=1e-6)


def test_four_equal_values() -> None:
    data = bytes([0, 1, 2, 3]) * 256

    entropy = shannon_entropy(data)

    assert entropy == pytest.approx(2.0, abs=1e-6)


def test_uniform_distribution() -> None:
    data = bytes(range(256))

    entropy = shannon_entropy(data)

    assert entropy == pytest.approx(8.0, abs=1e-6)


def test_uniform_distribution_repeated() -> None:
    data = bytes(range(256)) * 16

    entropy = shannon_entropy(data)

    assert entropy == pytest.approx(8.0, abs=1e-6)


def test_entropy_is_between_zero_and_eight() -> None:
    entropy = shannon_entropy(os.urandom(8192))

    assert 0.0 <= entropy <= 8.0


def test_random_data_has_high_entropy() -> None:
    entropy = shannon_entropy(os.urandom(32768))

    assert entropy > 7.5


def test_ascii_text_has_lower_entropy() -> None:
    data = (b"The quick brown fox jumps over the lazy dog. " * 512)

    entropy = shannon_entropy(data)

    assert entropy < 6.5


def test_binary_pattern() -> None:
    data = (b"\x00\x00\xFF\xFF") * 1024

    entropy = shannon_entropy(data)

    assert entropy == pytest.approx(1.0, abs=1e-6)


def test_all_values_twice() -> None:
    data = bytes(range(256)) * 2

    entropy = shannon_entropy(data)

    assert entropy == pytest.approx(8.0, abs=1e-6)


def test_deterministic_result() -> None:
    data = bytes(range(64)) * 100

    first = shannon_entropy(data)
    second = shannon_entropy(data)

    assert first == second


def test_entropy_returns_float() -> None:
    value = shannon_entropy(b"\x00\x01")

    assert isinstance(value, float)


def test_entropy_is_not_nan() -> None:
    value = shannon_entropy(os.urandom(2048))

    assert not math.isnan(value)


def test_entropy_is_not_infinite() -> None:
    value = shannon_entropy(os.urandom(2048))

    assert math.isfinite(value)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (b"", 0.0),
        (b"\x00", 0.0),
        (b"\x00\x01", 1.0),
        (b"\x00\x01\x02\x03", 2.0),
    ],
)
def test_known_values(data: bytes, expected: float) -> None:
    entropy = shannon_entropy(data)

    assert entropy == pytest.approx(expected, abs=1e-6)