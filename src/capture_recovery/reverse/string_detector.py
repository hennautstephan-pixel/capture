"""
capture_recovery.reverse.string_detector

Detect strings inside binary buffers.
"""

from __future__ import annotations


from collections.abc import Callable, Iterable
from typing import TypeAlias


from .base_detector import BaseDetector
from .detection_options import DetectionOptions

from .detector_type import DetectorType

from .string_type import (
    STRING_TYPES,
    StringType,
)

from .string_value import (
    StringValue,
)


_Scanner: TypeAlias = Callable[
    [bytes, StringType, int],
    list[StringValue],
]
_Validator: TypeAlias = Callable[[bytes], bool]


class StringDetector(BaseDetector):
    """
    Detect readable strings.
    """

    detector_type = DetectorType.STRING
    _ASCII_TYPE = "ascii"
    _UTF16_BE_TYPE = "utf16_be"
    _UTF16_ALIASES = (
        "utf16",
        "utf16-le",
        "utf16_le",
    )



    def __init__(
        self,
        string_types: Iterable[StringType] = STRING_TYPES,
        minimum_length: int = 4,
    ) -> None:


        self._string_types = tuple(
            string_types
        )


        self.minimum_length = minimum_length
        self._scanners: dict[str, _Scanner] | None = None



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



    def _build_scanners(self) -> dict[str, _Scanner]:
        scanners = {
            self._ASCII_TYPE: self._scan_ascii,
            self._UTF16_BE_TYPE: self._scan_utf16_be,
        }

        for alias in self._UTF16_ALIASES:
            scanners[alias] = self._scan_utf16

        return scanners



    def _get_scanners(self) -> dict[str, _Scanner]:
        if self._scanners is None:
            self._scanners = self._build_scanners()

        return self._scanners



    def _get_scanner(
        self,
        string_type: StringType,
    ) -> _Scanner | None:
        return self._get_scanners().get(string_type.name)



    def detect(
        self,
        data,
        options: DetectionOptions | None = None,
        min_length: int | None = None,
    ) -> list[StringValue]:


        if options is None:

            options = DetectionOptions()



        if min_length is None:

            min_length = self.minimum_length



        if hasattr(
            options,
            "enabled_types",
        ):

            enabled = options.enabled_types


            if enabled is not None:

                if DetectorType.STRING not in enabled:

                    return []



        buffer = bytes(
            data
        )



        if options.max_scan_size is not None:

            buffer = buffer[
                :options.max_scan_size
            ]



        results: list[StringValue] = []



        for string_type in self._string_types:

            scanner = self._get_scanner(string_type)

            if scanner is None:

                continue


            results.extend(

                scanner(

                    buffer,

                    string_type,

                    min_length,

                )

            )



        return list(self._limit_results(self._remove_duplicates(results), options))





    def _scan_generic(
        self,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
        step: int,
        validator: _Validator,
    ) -> list[StringValue]:


        results: list[StringValue] = []

        start = None

        index = 0


        def finalize(end: int) -> None:
            nonlocal start

            if start is None:

                return

            self._append_string(
                results,
                start,
                end,
                data,
                string_type,
                minimum_length,
            )

            start = None



        while index + step <= len(data):

            element = data[
                index:index + step
            ]


            if validator(element):

                if start is None:

                    start = index

            else:

                finalize(index)


            index += step



        finalize(len(data))



        return results



    def _scan_ascii(
        self,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
    ) -> list[StringValue]:
        return self._scan_generic(
            data,
            string_type,
            minimum_length,
            1,
            self._validate_ascii_element,
        )



    def _scan_utf16(
        self,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
    ) -> list[StringValue]:
        return self._scan_utf16_generic(
            data,
            string_type,
            minimum_length,
            self._validate_utf16_le_element,
        )

    def _scan_utf16_be(
        self,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
    ) -> list[StringValue]:
        return self._scan_utf16_generic(
            data,
            string_type,
            minimum_length,
            self._validate_utf16_be_element,
        )

    def _scan_utf16_generic(
        self,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
        validator: _Validator,
    ) -> list[StringValue]:
        return self._scan_generic(
            data,
            string_type,
            minimum_length,
            2,
            validator,
        )








    def _validate_ascii_element(
        self,
        element: bytes,
    ) -> bool:
        return self._is_ascii_byte(element[0])

    def _validate_utf16_le_element(
        self,
        element: bytes,
    ) -> bool:
        return self._is_utf16_le_pair(element)

    def _validate_utf16_be_element(
        self,
        element: bytes,
    ) -> bool:
        return self._is_utf16_be_pair(element)

    def _is_ascii_byte(
        self,
        byte: int,
    ) -> bool:
        return 32 <= byte <= 126

    def _is_utf16_le_pair(
        self,
        pair: bytes,
    ) -> bool:
        return pair[1] == 0 and 32 <= pair[0] <= 126

    def _is_utf16_be_pair(
        self,
        pair: bytes,
    ) -> bool:
        return pair[0] == 0 and 32 <= pair[1] <= 126

    def _append_string(
        self,
        results: list[StringValue],
        start: int,
        end: int,
        data: bytes,
        string_type: StringType,
        minimum_length: int,
    ) -> None:
        raw = data[start:end]
        value = self._decode_string(raw, string_type.encoding)

        if self._valid(value, minimum_length):
            results.append(
                self._build_string_value(
                    start,
                    string_type,
                    value,
                    raw,
                )
            )

    def _decode_string(
        self,
        raw: bytes,
        encoding: str,
    ) -> str:
        try:
            return raw.decode(
                encoding,
                errors="ignore",
            )
        except Exception:
            return ""

    def _build_string_value(
        self,
        offset: int,
        string_type: StringType,
        value: str,
        raw: bytes,
    ) -> StringValue:
        return StringValue(
            offset=offset,
            string_type=string_type,
            value=value,
            raw_bytes=raw,
            terminated=True,
        )

    def _valid(
        self,
        value: str,
        minimum_length: int,
    ) -> bool:


        value = value.strip()



        if len(value) < minimum_length:

            return False



        printable = sum(

            1

            for char in value

            if char.isprintable()

        )



        if printable / len(value) < 0.8:

            return False



        letters = sum(

            1

            for char in value

            if char.isalpha()

        )



        if letters == 0:

            return False



        return True





    def _remove_duplicates(
        self,
        values: list[StringValue],
    ) -> list[StringValue]:


        result: list[StringValue] = []

        seen: set[tuple[int, str]] = set()



        for item in values:


            key = (

                item.offset,

                item.value,

            )



            if key in seen:

                continue



            seen.add(
                key
            )


            result.append(
                item
            )



        return result