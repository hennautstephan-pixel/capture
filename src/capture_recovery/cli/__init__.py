"""
Command line interfaces for Capture Recovery.

The executable modules are intentionally not imported here
to avoid eager loading when using:

    python -m capture_recovery.cli.recover
"""

from .corpus_loader import (
    CorpusLoader,
    CorpusLoadResult,
)

from .diff_builder import (
    DiffBuilder,
    StreamDiff,
    ByteDifference,
)


__all__ = [
    "CorpusLoader",
    "CorpusLoadResult",
    "DiffBuilder",
    "StreamDiff",
    "ByteDifference",
]