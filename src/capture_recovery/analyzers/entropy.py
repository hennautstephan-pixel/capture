"""
Capture Recovery

Entropy Analyzer

Calcule l'entropie de Shannon par blocs.
"""

from __future__ import annotations

import math

from ..binary_reader import BinaryReader
from ..models import (
    Block,
    BlockType,
    Report,
)


class EntropyAnalyzer:

    def __init__(self, block_size: int = 4096):

        self.block_size = block_size

    # ---------------------------------------------------------

    @staticmethod
    def shannon(data: bytes) -> float:

        if not data:
            return 0.0

        frequencies = [0] * 256

        for b in data:
            frequencies[b] += 1

        entropy = 0.0
        length = len(data)

        for count in frequencies:

            if count == 0:
                continue

            p = count / length
            entropy -= p * math.log2(p)

        return entropy

    # ---------------------------------------------------------

    @staticmethod
    def classify(entropy: float) -> BlockType:

        if entropy < 2.5:
            return BlockType.METADATA

        if entropy > 7.5:
            return BlockType.COMPRESSED

        return BlockType.UNKNOWN

    # ---------------------------------------------------------

    def run(
        self,
        reader: BinaryReader,
        report: Report,
    ) -> None:

        reader.seek(0)

        offset = 0

        while reader.remaining > 0:

            size = min(
                self.block_size,
                reader.remaining,
            )

            data = reader.read(size)

            entropy = self.shannon(data)

            report.add_block(

                Block(
                    start=offset,
                    end=offset + len(data) - 1,
                    block_type=self.classify(entropy),
                    entropy=entropy,
                    description=f"Entropy {entropy:.2f}",
                )

            )

            offset += len(data)