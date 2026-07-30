"""
capture_recovery.reverse.guid_detector

Detect GUID values inside binary buffers.
"""

from __future__ import annotations

from collections.abc import Iterable

from .base_detector import BaseDetector
from .detection_options import DetectionOptions
from .detector_type import DetectorType
from .guid_decoder import GuidDecoder
from .guid_type import (
    GUID_TYPES,
    GuidType,
)
from .guid_value import GuidValue
from .offset_iterator import OffsetIterator


class GuidDetector(BaseDetector):
    """
    Detect GUID values in binary data.
    """

    detector_type = DetectorType.GUID

    HEADER_SKIP_SIZE = 128

    def __init__(
        self,
        guid_types: Iterable[GuidType] = GUID_TYPES,
    ) -> None:
        self._guid_types = tuple(guid_types)

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

        if not self._is_enabled(options, self.detector_type):
            return []

        buffer = bytes(self._buffer(data, options))
        max_results = options.max_results

        results: list[GuidValue] = []
        seen = set()

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
                    return list(self._limit_results(results, options))

                if (
                    len(buffer) > 1024
                    and offset < self.HEADER_SKIP_SIZE
                ):
                    continue

                raw = bytes(buffer[offset: offset + guid_type.size])

                if not self._is_valid_candidate(raw):
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

                seen.add(key)
                results.append(value)

        return list(self._limit_results(results, options))

    @staticmethod
    def _is_valid_candidate(
        raw: bytes,
    ) -> bool:
        if len(raw) != 16:
            return False

        utf16_le_pairs = sum(
            1
            for index in range(1, 16, 2)
            if raw[index] == 0
        )
        if utf16_le_pairs >= 5:
            return False

        utf16_be_pairs = sum(
            1
            for index in range(0, 15, 2)
            if raw[index] == 0
        )
        if utf16_be_pairs >= 5:
            return False

        if raw.count(0) >= 12:
            return False

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