"""
capture_recovery.reverse.binary_map

Generic binary mapping utilities.

BinaryMap does not understand the Capture format.
Its only goal is to locate interesting regions inside a binary
stream so they can later be analysed by higher level tools.
"""

from __future__ import annotations

from dataclasses import dataclass
import string


_MIN_ASCII = 4
_MIN_ZERO_BLOCK = 8

_PRINTABLE = set(bytes(string.printable, "ascii"))
_PRINTABLE.discard(0x0b)
_PRINTABLE.discard(0x0c)


@dataclass(slots=True, frozen=True)
class BinaryNode:
    """
    One detected element inside a binary stream.
    """

    offset: int
    length: int
    kind: str
    value: object


class BinaryMap:
    """
    Produces a structural map of a binary buffer.

    This class performs no Capture-specific parsing.
    """

    @classmethod
    def scan(
        cls,
        data: bytes | bytearray | memoryview,
    ) -> list[BinaryNode]:

        if isinstance(data, memoryview):
            buffer = data.tobytes()
        else:
            buffer = bytes(data)

        nodes: list[BinaryNode] = []

        nodes.extend(cls._ascii_strings(buffer))
        nodes.extend(cls._zero_blocks(buffer))

        nodes.sort(key=lambda n: n.offset)

        return nodes

    # ---------------------------------------------------------

    @staticmethod
    def _ascii_strings(data: bytes) -> list[BinaryNode]:

        nodes: list[BinaryNode] = []

        i = 0
        size = len(data)

        while i < size:

            if data[i] not in _PRINTABLE or data[i] == 0:

                i += 1
                continue

            start = i

            while (
                i < size
                and data[i] in _PRINTABLE
                and data[i] != 0
            ):
                i += 1

            length = i - start

            if length >= _MIN_ASCII:

                value = data[start:i].decode(
                    "ascii",
                    errors="ignore",
                )

                nodes.append(
                    BinaryNode(
                        offset=start,
                        length=length,
                        kind="ascii",
                        value=value,
                    )
                )

        return nodes

    # ---------------------------------------------------------

    @staticmethod
    def _zero_blocks(data: bytes) -> list[BinaryNode]:

        nodes: list[BinaryNode] = []

        i = 0
        size = len(data)

        while i < size:

            if data[i] != 0:

                i += 1
                continue

            start = i

            while i < size and data[i] == 0:
                i += 1

            length = i - start

            if length >= _MIN_ZERO_BLOCK:

                nodes.append(
                    BinaryNode(
                        offset=start,
                        length=length,
                        kind="zero_block",
                        value=None,
                    )
                )

        return nodes