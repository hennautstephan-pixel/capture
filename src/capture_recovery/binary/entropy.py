"""
Entropy calculation utilities.

This module provides a Shannon entropy implementation for binary data.
The entropy is expressed in bits per byte and ranges from 0.0 to 8.0.

Examples
--------
>>> shannon_entropy(b"")
0.0

>>> shannon_entropy(b"\x00" * 100)
0.0

>>> round(shannon_entropy(bytes(range(256))), 2)
8.0
"""

from __future__ import annotations

from collections import Counter
from math import log2

__all__ = [
    "shannon_entropy",
]


def shannon_entropy(data: bytes) -> float:
    """
    Compute the Shannon entropy of a byte sequence.

    Parameters
    ----------
    data
        Binary data.

    Returns
    -------
    float
        Entropy in bits per byte.

    Notes
    -----
    The returned value is between 0.0 and 8.0.

    Empty input returns 0.0.
    """

    if not data:
        return 0.0

    counts = Counter(data)
    length = len(data)

    entropy = 0.0

    for count in counts.values():
        probability = count / length
        entropy -= probability * log2(probability)

    return entropy