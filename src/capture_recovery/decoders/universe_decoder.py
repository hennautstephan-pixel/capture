"""
Universe decoder.
"""

from __future__ import annotations

from capture_recovery.decoders.base_decoder import (
    BaseSemanticDecoder,
)


class UniverseDecoder(BaseSemanticDecoder):
    """
    Decode lighting universes.
    """

    object_type = "Universe"