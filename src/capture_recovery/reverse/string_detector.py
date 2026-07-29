"""
capture_recovery.reverse.string_detector

String detection engine.
"""

from __future__ import annotations

from collections.abc import Iterable

from .detection_options import DetectionOptions
from .detector_type import DetectorType
from .string_decoder import StringDecoder
from .string_type import (
    ASCII,
    UTF8,
    UTF16_LE,
    UTF16_BE,
    StringType,
)
from .string_value import StringValue



_DEFAULT_STRING_TYPES = (
    ASCII,
    UTF8,
    UTF16_LE,
    UTF16_BE,
)



class StringDetector:
    """
    Detect strings inside binary buffers.
    """


    def __init__(
        self,
        string_types: Iterable[StringType] = _DEFAULT_STRING_TYPES,
    ) -> None:

        self._string_types = tuple(
            string_types
        )


    @property
    def name(self) -> str:
        """
        Detector name.
        """

        return "string"



    @property
    def string_types(
        self,
    ) -> tuple[StringType, ...]:
        """
        Supported string formats.
        """

        return self._string_types



    def detect(
        self,
        data: bytes | bytearray | memoryview,
        options: DetectionOptions | None = None,
        *,
        min_length: int = 1,
    ) -> list[StringValue]:
        """
        Detect strings.

        Search all possible offsets.
        """


        if options is not None:

            enabled = getattr(
                options,
                "enabled_types",
                None,
            )

            if (
                enabled
                and DetectorType.STRING not in enabled
            ):
                return []



        buffer = bytes(data)

        results: list[StringValue] = []

        seen: set[
            tuple[int, str]
        ] = set()



        for string_type in self._string_types:


            for offset in range(
                len(buffer),
            ):


                value = StringDecoder.decode(
                    buffer,
                    offset,
                    string_type,
                )


                if value is None:
                    continue



                if len(value.value) < min_length:
                    continue



                key = (
                    value.offset,
                    value.value,
                )


                if key in seen:
                    continue


                seen.add(key)


                results.append(
                    value
                )



        return results