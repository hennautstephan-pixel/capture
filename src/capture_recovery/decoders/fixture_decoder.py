"""
Fixture decoder.
"""

from __future__ import annotations

from capture_recovery.decoders.base_decoder import (
    BaseSemanticDecoder,
)


class FixtureDecoder(BaseSemanticDecoder):
    """
    Decode lighting fixtures.
    """

    object_type = "Fixture"