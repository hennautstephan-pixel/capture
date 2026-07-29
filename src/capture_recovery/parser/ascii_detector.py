from __future__ import annotations

from .segment import Segment


class AsciiDetector:
    """
    Detect printable ASCII strings inside a binary buffer.
    """

    MIN_LENGTH = 4

    @classmethod
    def detect(
        cls,
        data: bytes | bytearray | memoryview,
    ) -> list[Segment]:
        data = memoryview(data)

        segments: list[Segment] = []

        i = 0
        size = len(data)

        while i < size:

            b = data[i]

            if 32 <= b <= 126:

                start = i
                i += 1

                while i < size and 32 <= data[i] <= 126:
                    i += 1

                length = i - start

                if length >= cls.MIN_LENGTH:

                    text = bytes(data[start:i]).decode("ascii")

                    segments.append(
                        Segment(
                            offset=start,
                            length=length,
                            kind="ascii",
                            confidence=1.0,
                            metadata={
                                "text": text,
                            },
                        )
                    )

            else:
                i += 1

        return segments