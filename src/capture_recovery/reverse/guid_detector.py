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
        """
        Detector public name.
        """

        return "guid"



    def detect(
        self,
        data: bytes | bytearray | memoryview,
        options: DetectionOptions | None = None,
    ) -> list[GuidValue]:
        """
        Detect GUID values.
        """


        if options is not None:

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



        buffer = bytes(data)

        results: list[GuidValue] = []

        seen: set[tuple[int, str]] = set()



        for guid_type in self._guid_types:


            iterator_options = (
                options
                if options is not None
                else DetectionOptions()
            )


            for offset in OffsetIterator.iterate(
                length=len(buffer),
                value_size=guid_type.size,
                options=iterator_options,
            ):


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


                seen.add(key)

                results.append(
                    value
                )


        return results



    @property
    def guid_types(
        self,
    ) -> tuple[GuidType, ...]:
        """
        Supported GUID formats.
        """

        return self._guid_types