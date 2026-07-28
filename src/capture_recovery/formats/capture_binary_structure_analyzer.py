"""
Capture binary structure analyzer.

Provides a non destructive analysis of
Capture project binary containers.

This module does not decode Capture objects.
It detects structures, offsets and
recoverable patterns.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import math



class CaptureBinaryStructureAnalyzer:
    """
    Analyze raw Capture project binary data.
    """


    def analyze(
        self,
        path,
    ) -> dict:
        """
        Analyze a Capture project file.
        """

        path = Path(path)


        if not path.exists():

            raise FileNotFoundError(
                path
            )


        data = path.read_bytes()


        return {

            "file": str(path),

            "size": len(data),

            "sha256": self._hash(
                data
            ),

            "ascii_strings": self._ascii_strings(
                data
            ),

            "utf16_strings": self._utf16_strings(
                data
            ),

            "blocks": self._detect_blocks(
                data
            ),

            "entropy": self._entropy(
                data
            ),

        }



    def _hash(
        self,
        data,
    ):

        return hashlib.sha256(
            data
        ).hexdigest()



    def _ascii_strings(
        self,
        data,
        minimum=4,
    ):

        result = []

        current = bytearray()

        start = 0


        for offset, byte in enumerate(data):

            if 32 <= byte <= 126:


                if not current:

                    start = offset


                current.append(
                    byte
                )


            else:


                if len(current) >= minimum:

                    result.append(

                        {
                            "offset": start,

                            "value": current.decode(
                                "ascii",
                                errors="ignore",
                            ),
                        }

                    )


                current.clear()



        if len(current) >= minimum:

            result.append(

                {
                    "offset": start,

                    "value": current.decode(
                        "ascii",
                        errors="ignore",
                    ),
                }

            )


        return result[:500]



    def _utf16_strings(
        self,
        data,
        minimum=4,
    ):

        """
        Fast UTF-16LE extraction.

        Previous implementation decoded
        the remaining file at every offset,
        causing huge slowdowns.
        """


        result = []


        try:

            text = data.decode(
                "utf-16-le",
                errors="ignore",
            )


        except Exception:

            return result



        current = []

        start = 0


        for index, char in enumerate(text):


            if char != "\x00":

                if not current:

                    start = index


                current.append(
                    char
                )


            else:

                if len(current) >= minimum:


                    result.append(

                        {
                            "offset": start * 2,

                            "value": "".join(
                                current
                            )[:200],

                        }

                    )


                current.clear()



        if len(current) >= minimum:


            result.append(

                {
                    "offset": start * 2,

                    "value": "".join(
                        current
                    )[:200],

                }

            )



        return result[:500]



    def _detect_blocks(
        self,
        data,
        block_size=256,
    ):

        blocks = []


        total = len(data)


        for offset in range(
            0,
            total,
            block_size,
        ):


            chunk = data[
                offset:
                offset + block_size
            ]


            if not chunk:

                continue



            blocks.append(

                {
                    "offset": offset,

                    "size": len(chunk),

                    "entropy": self._entropy(
                        chunk
                    ),
                }

            )


        return blocks[:500]



    def _entropy(
        self,
        data,
    ):

        if not data:

            return 0.0



        counts = {}


        for byte in data:

            counts[byte] = (
                counts.get(
                    byte,
                    0,
                )
                + 1
            )



        entropy = 0.0


        length = len(data)


        for count in counts.values():

            probability = (
                count / length
            )


            entropy -= (
                probability
                *
                math.log2(
                    probability
                )
            )



        return round(
            entropy,
            4,
        )