"""
capture_recovery.reverse.string_detector

Optimized string detection engine.

Extracts meaningful strings from
binary Capture project files.
"""

from __future__ import annotations


from collections.abc import Iterable
import string


from .detection_options import DetectionOptions
from .detector_type import DetectorType


from .string_type import (
    ASCII,
    UTF8,
    UTF16_LE,
    UTF16_BE,
    StringType,
)


from .string_value import (
    StringValue,
)



_DEFAULT_STRING_TYPES = (
    ASCII,
    UTF8,
    UTF16_LE,
    UTF16_BE,
)



_PRINTABLE = set(
    string.printable
)



class StringDetector:
    """
    Detect useful text strings inside binary data.
    """



    def __init__(
        self,
        string_types: Iterable[StringType] = _DEFAULT_STRING_TYPES,
    ) -> None:

        self._string_types = tuple(
            string_types
        )



    @property
    def name(
        self,
    ) -> str:

        return "string"



    @property
    def string_types(
        self,
    ) -> tuple[StringType, ...]:

        return self._string_types



    def detect(
        self,
        data: bytes | bytearray | memoryview,
        options: DetectionOptions | None = None,
        *,
        min_length: int = 4,
        max_results: int = 1000,
    ) -> list[StringValue]:
        """
        Detect strings and remove noise.
        """



        if options is not None:

            enabled = getattr(
                options,
                "enabled_types",
                None,
            )


            if (
                enabled
                and DetectorType.STRING
                not in enabled
            ):

                return []



        buffer = bytes(
            data
        )


        results: list[StringValue] = []



        if (
            ASCII in self._string_types
            or UTF8 in self._string_types
        ):

            results.extend(
                self._scan_ascii(
                    buffer,
                    min_length,
                )
            )



        if UTF16_LE in self._string_types:

            results.extend(
                self._scan_utf16(
                    buffer,
                    minimum=min_length,
                    little=True,
                    string_type=UTF16_LE,
                )
            )



        if UTF16_BE in self._string_types:

            results.extend(
                self._scan_utf16(
                    buffer,
                    minimum=min_length,
                    little=False,
                    string_type=UTF16_BE,
                )
            )



        results = self._remove_overlaps(
            results
        )


        return results[
            :max_results
        ]



    def _scan_ascii(
        self,
        buffer: bytes,
        minimum: int,
    ) -> list[StringValue]:

        results = []

        start = None



        for index, byte in enumerate(buffer):

            char = chr(byte)


            valid = (

                char in _PRINTABLE

                and char not in "\x00\r\n\t"

            )



            if valid:


                if start is None:

                    start = index



            elif start is not None:


                raw = buffer[
                    start:index
                ]



                if len(raw) >= minimum:


                    text = raw.decode(
                        "ascii",
                        errors="ignore",
                    )


                    if self._valid_text(
                        text
                    ):


                        results.append(

                            StringValue(

                                offset=start,

                                value=text,

                                string_type=ASCII,

                                raw_bytes=raw,

                            )

                        )



                start = None



        return results



    def _scan_utf16(
        self,
        buffer: bytes,
        *,
        minimum: int,
        little: bool,
        string_type: StringType,
    ) -> list[StringValue]:

        results = []

        start = None



        for offset in range(
            0,
            len(buffer)-1,
            2,
        ):


            pair = buffer[
                offset:
                offset + 2
            ]



            if little:

                valid = (

                    pair[1] == 0

                    and chr(pair[0])
                    in _PRINTABLE

                )

            else:

                valid = (

                    pair[0] == 0

                    and chr(pair[1])
                    in _PRINTABLE

                )



            if valid:


                if start is None:

                    start = offset



            elif start is not None:


                length = (
                    offset - start
                ) // 2



                if length >= minimum:


                    raw = buffer[
                        start:offset
                    ]


                    encoding = (

                        "utf-16le"

                        if little

                        else

                        "utf-16be"

                    )


                    text = raw.decode(
                        encoding,
                        errors="ignore",
                    )


                    if self._valid_text(
                        text
                    ):


                        results.append(

                            StringValue(

                                offset=start,

                                value=text,

                                string_type=string_type,

                                raw_bytes=raw,

                            )

                        )


                start = None



        return results



    @staticmethod
    def _valid_text(
        text: str,
    ) -> bool:
        """
        Reject binary ASCII noise.
        """

        text = text.strip()



        if len(text) < 4:

            return False



        printable = sum(

            1

            for char in text

            if char.isprintable()

        )



        if (
            printable / len(text)
        ) < 0.95:

            return False



        letters = sum(

            1

            for char in text

            if char.isalpha()

        )



        digits = sum(

            1

            for char in text

            if char.isdigit()

        )



        symbols = (
            len(text)
            -
            letters
            -
            digits
        )



        #
        # Too many symbols
        #

        if symbols > letters:

            return False



        #
        # Short random strings
        #

        if len(text) <= 6:

            if letters < 3:

                return False



        #
        # Text density
        #

        if (
            letters / len(text)
        ) < 0.65:

            return False



        return True



    @staticmethod
    def _remove_overlaps(
        values: list[StringValue],
    ) -> list[StringValue]:
        """
        Keep longest meaningful strings.

        Example:

        Project
        roject
        oject

        becomes:

        Project
        """



        if not values:

            return []



        values = sorted(

            values,

            key=lambda item: (

                -len(item.value),

                item.offset,

            )

        )



        result: list[StringValue] = []



        for candidate in values:


            candidate_text = (
                candidate.value
            )


            duplicate = False



            for existing in result:


                existing_text = (
                    existing.value
                )



                if candidate_text in existing_text:

                    duplicate = True

                    break



                if existing_text in candidate_text:


                    result.remove(
                        existing
                    )

                    break



            if not duplicate:

                result.append(
                    candidate
                )



        return sorted(

            result,

            key=lambda item:
                item.offset,

        )