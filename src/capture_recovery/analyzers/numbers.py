"""
Capture Recovery

Numbers Analyzer

Fournit des fonctions de lecture des types numériques.
"""

from __future__ import annotations

import math
import struct

from ..binary_reader import BinaryReader


class NumberAnalyzer:

    def __init__(self, reader: BinaryReader):

        self.reader = reader

    # ---------------------------------------------------------

    def read_u16(self, offset: int) -> int:

        self.reader.seek(offset)

        return struct.unpack("<H", self.reader.read(2))[0]

    # ---------------------------------------------------------

    def read_u32(self, offset: int) -> int:

        self.reader.seek(offset)

        return struct.unpack("<I", self.reader.read(4))[0]

    # ---------------------------------------------------------

    def read_u64(self, offset: int) -> int:

        self.reader.seek(offset)

        return struct.unpack("<Q", self.reader.read(8))[0]

    # ---------------------------------------------------------

    def read_i16(self, offset: int) -> int:

        self.reader.seek(offset)

        return struct.unpack("<h", self.reader.read(2))[0]

    # ---------------------------------------------------------

    def read_i32(self, offset: int) -> int:

        self.reader.seek(offset)

        return struct.unpack("<i", self.reader.read(4))[0]

    # ---------------------------------------------------------

    def read_i64(self, offset: int) -> int:

        self.reader.seek(offset)

        return struct.unpack("<q", self.reader.read(8))[0]

    # ---------------------------------------------------------

    def read_float(self, offset: int) -> float:

        self.reader.seek(offset)

        return struct.unpack("<f", self.reader.read(4))[0]

    # ---------------------------------------------------------

    def read_double(self, offset: int) -> float:

        self.reader.seek(offset)

        return struct.unpack("<d", self.reader.read(8))[0]

    # ---------------------------------------------------------

    @staticmethod
    def is_plausible_float(value: float) -> bool:

        if math.isnan(value):
            return False

        if math.isinf(value):
            return False

        return -1e12 < value < 1e12

    # ---------------------------------------------------------

    def is_plausible_pointer(self, value: int) -> bool:

        return 0 <= value < self.reader.size