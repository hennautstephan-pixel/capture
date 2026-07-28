"""
Capture object detector.

Detects possible Capture objects inside
binary project containers.

This module performs structural detection
only. It does not decode Capture objects.
"""

from __future__ import annotations



class CaptureObjectDetector:
    """
    Detect possible binary objects.
    """



    def __init__(
        self,
        minimum_size=16,
        maximum_size=1024,
    ):

        self.minimum_size = minimum_size

        self.maximum_size = maximum_size



    def detect(
        self,
        data: bytes,
    ) -> list[dict]:
        """
        Detect possible object regions.
        """


        objects = []


        length = len(data)


        offset = 0



        while offset < length:


            size = self._read_size(
                data,
                offset,
            )


            if (
                size is not None
                and self.minimum_size <= size <= self.maximum_size
                and offset + size <= length
            ):


                objects.append(

                    {
                        "offset": offset,

                        "size": size,

                        "type": "unknown",

                        "confidence": self._confidence(
                            data[
                                offset:
                                offset + size
                            ]
                        ),
                    }

                )


                offset += size


            else:

                offset += 1



        return objects



    def _read_size(
        self,
        data,
        offset,
    ):
        """
        Try to interpret a 32-bit little endian
        value as a block size.
        """


        if offset + 4 > len(data):

            return None



        value = int.from_bytes(

            data[
                offset:
                offset + 4
            ],

            byteorder="little",

            signed=False,

        )


        return value



    def _confidence(
        self,
        block,
    ):
        """
        Estimate if a block looks structured.
        """


        if not block:

            return 0.0



        zero_count = block.count(
            0
        )


        ratio = zero_count / len(block)


        if ratio > 0.5:

            return 0.8


        if ratio > 0.2:

            return 0.5


        return 0.2