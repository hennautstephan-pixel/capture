"""
Capture binary signature detector.

Detects repeated binary patterns
inside Capture project containers.
"""

from __future__ import annotations

from collections import defaultdict
import hashlib



class CaptureSignatureDetector:
    """
    Detect repeated binary signatures.
    """



    def __init__(
        self,
        window_size=32,
        minimum_occurrences=2,
    ):

        self.window_size = window_size
        self.minimum_occurrences = minimum_occurrences



    def detect(
        self,
        data: bytes,
    ) -> dict:


        signatures = defaultdict(list)


        length = len(data)


        if length < self.window_size:

            return {
                "count": 0,
                "signatures": [],
            }



        for offset in range(
            0,
            length - self.window_size + 1,
        ):


            block = data[
                offset:
                offset + self.window_size
            ]


            signatures[block].append(
                offset
            )



        results = []


        for block, offsets in signatures.items():


            if len(offsets) >= self.minimum_occurrences:


                results.append(

                    {
                        "signature": hashlib.sha1(
                            block
                        ).hexdigest(),

                        "occurrences": len(offsets),

                        "offsets": offsets[:100],

                        "size": self.window_size,

                    }

                )


        results.sort(
            key=lambda item: item["occurrences"],
            reverse=True,
        )


        return {

            "count": len(results),

            "signatures": results[:100],

        }