"""
Cue decoder.
"""

from __future__ import annotations

from capture_recovery.decoders.base_decoder import (
    BaseSemanticDecoder,
)


class CueDecoder(BaseSemanticDecoder):
    """
    Decode lighting cues.
    """

    object_type = "Cue"