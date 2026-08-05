"""
Command line interfaces for Capture Recovery.
"""

from .intelligent_analyze import (
    analyze_file,
    main as intelligent_analyze_main,
)

from .recover import (
    recover_file,
    main as recover_main,
)

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
    "analyze_file",
    "intelligent_analyze_main",
    "recover_file",
    "recover_main",
    "CorpusLoader",
    "CorpusLoadResult",
    "DiffBuilder",
    "StreamDiff",
    "ByteDifference",
]