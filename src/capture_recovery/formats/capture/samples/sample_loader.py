from __future__ import annotations

from pathlib import Path


def sample_directory() -> Path:
    """
    Return the directory containing Capture sample files.
    """

    root = Path(__file__).resolve().parents[4]

    candidates = (
        root / "samples",
        root / "tests" / "samples",
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Unable to locate the Capture sample directory."
    )


def iter_c2p_files():
    """
    Iterate over every Capture sample.
    """

    yield from sorted(
        sample_directory().rglob("*.c2p")
    )