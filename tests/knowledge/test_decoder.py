from __future__ import annotations

import pytest

from capture_recovery.knowledge.decoder import Decoder


def test_decoder_is_abstract():

    with pytest.raises(TypeError):
        Decoder()