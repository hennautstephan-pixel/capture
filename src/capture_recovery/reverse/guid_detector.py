"""
capture_recovery.reverse.guid_detector

Detect GUID values inside binary buffers.
"""

from __future__ import annotations


from collections.abc import Iterable


from .detection_options import DetectionOptions
from .detector_type import DetectorType
from .guid_decoder import GuidDecoder
from .guid_type import (
    GUID_TYPES,
    GuidType,
)
from .guid_value import GuidValue
from .offset_iterator import OffsetIterator



class GuidDetector:
    """
    Detect GUID values in binary data.
    """



    def __init__(
        self,
        guid_types: Iterable[GuidType] = GUID_TYPES,
    ) -> None:

        self._guid_types = tuple(
            guid_types
        )



    @property
    def name(self) -> str:

        return "guid"



    def detect(
        self,
        data: bytes | bytearray | memoryview,
        options: DetectionOptions | None = None,
    ) -> list[GuidValue]:
        """
        Detect GUID values.
        """

        if options is None:

            options = DetectionOptions()



        enabled_types = getattr(
            options,
            "enabled_types",
            None,
        )


        if (
            enabled_types
            and DetectorType.GUID
            not in enabled_types
        ):

            return []



        buffer = bytes(
            data
        )



        if options.max_scan_size is not None:

            buffer = buffer[
                :options.max_scan_size
            ]



        max_results = getattr(
            options,
            "max_results",
            None,
        )



        results: list[GuidValue] = []

        seen: set[
            tuple[int, str]
        ] = set()



        for guid_type in self._guid_types:


            for offset in OffsetIterator.iterate(
                length=len(buffer),
                value_size=guid_type.size,
                options=options,
            ):


                if (
                    max_results is not None
                    and len(results) >= max_results
                ):

                    return results



                raw = buffer[
                    offset:
                    offset + guid_type.size
                ]



                if not self._is_valid_candidate(
                    raw
                ):

                    continue



                value = GuidDecoder.decode(
                    buffer,
                    offset,
                    guid_type,
                )



                if value is None:

                    continue



                key = (
                    value.offset,
                    value.type_name,
                )



                if key in seen:

                    continue



                seen.add(
                    key
                )


                results.append(
                    value
                )



        return results



    @staticmethod
    def _is_valid_candidate(
        raw: bytes,
    ) -> bool:
        """
        Reject obvious text interpreted as GUID.

        Do not reject valid binary GUIDs.
        """

        if len(raw) != 16:

            return False



        #
        # UTF-16 LE detection
        #
        # Example:
        # 53 00 6F 00 66 00 74 00
        #

        utf16_le_pairs = sum(

            1

            for index in range(
                1,
                16,
                2,
            )

            if raw[index] == 0

        )


        if utf16_le_pairs >= 5:

            return False



        #
        # UTF-16 BE detection
        #

        utf16_be_pairs = sum(

            1

            for index in range(
                0,
                15,
                2,
            )

            if raw[index] == 0

        )


        if utf16_be_pairs >= 5:

            return False



        #
        # Empty padding
        #

        if raw.count(
            0
        ) >= 12:

            return False



        #
        # Almost entirely printable ASCII
        #

        printable = sum(

            1

            for byte in raw

            if 32 <= byte < 127

        )


        if printable >= 12:

            return False



        return True



    @property
    def guid_types(
        self,
    ) -> tuple[GuidType, ...]:

        return self._guid_types