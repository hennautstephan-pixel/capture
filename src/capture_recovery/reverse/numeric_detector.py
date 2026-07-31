"""
capture_recovery.reverse.numeric_detector

Numeric value detection engine.
"""

from __future__ import annotations

import math
from collections.abc import Iterable

from .base_detector import BaseDetector
from .detection_options import DetectionOptions
from .detector_type import DetectorType
from .numeric_decoder import NumericDecoder
from .numeric_type import (
    INT16,
    UINT16,
    INT32,
    UINT32,
    INT64,
    UINT64,
    FLOAT32,
    FLOAT64,
    NumericType,
)
from .numeric_value import NumericValue
from .offset_iterator import OffsetIterator


_DEFAULT_NUMERIC_TYPES = (
    INT16,
    UINT16,
    INT32,
    UINT32,
    INT64,
    UINT64,
    FLOAT32,
    FLOAT64,
)


class _DualMethod:
    """
    Allow:

        NumericDetector.detect(data)

    and:

        detector.detect(data)
    """

    def __init__(self, function):
        self.function = function


    def __get__(self, instance, owner):

        if instance is None:

            return lambda data, *args, **kwargs: (
                owner()._detect(
                    data,
                    *args,
                    scan_all_endianness=True,
                    **kwargs,
                )
            )

        return lambda data, *args, **kwargs: (
            instance._detect(
                data,
                *args,
                scan_all_endianness=False,
                **kwargs,
            )
        )



class NumericDetector(BaseDetector):
    """
    Detect numeric values in binary buffers.
    """

    detector_type = DetectorType.NUMERIC

    def __init__(
        self,
        numeric_types: Iterable[NumericType] =
        _DEFAULT_NUMERIC_TYPES,
    ) -> None:

        self._numeric_types = tuple(
            numeric_types
        )


    @property
    def name(self) -> str:

        return "numeric"


    @property
    def numeric_types(self):

        return self._numeric_types



    @_DualMethod
    def detect(
        self,
        data,
        options=None,
        *,
        integers=True,
        floats=True,
        finite_only=True,
        endianness=None,
    ):

        return self._detect(
            data,
            options,
            integers=integers,
            floats=floats,
            finite_only=finite_only,
            endianness=endianness,
        )



    @staticmethod
    def integers(values):

        return [
            value
            for value in values
            if not value.numeric_type.floating
        ]



    @staticmethod
    def floats(values):

        return [
            value
            for value in values
            if value.numeric_type.floating
        ]



    @staticmethod
    def by_type(values, type_name):

        return [
            value
            for value in values
            if value.type_name == type_name
        ]



    @staticmethod
    def by_offset(values, offset):

        return [
            value
            for value in values
            if value.offset == offset
        ]



    @staticmethod
    def range(
        values,
        minimum=None,
        maximum=None,
    ):

        result = []

        for value in values:

            if (
                minimum is not None
                and value.value < minimum
            ):

                continue


            if (
                maximum is not None
                and value.value > maximum
            ):

                continue


            result.append(value)


        return result




    def _endianness_list(
        self,
        *,
        endianness: str | None,
        scan_all_endianness: bool,
    ) -> tuple[str, ...]:
        """
        Return the list of endianness values to scan.
        """
        if scan_all_endianness:
            return (
                "little",
                "big",
            )

        if endianness is not None:
            return (
                endianness,
            )

        return (
            "little",
        )


    def _offsets(
        self,
        *,
        buffer: bytes,
        numeric_type: NumericType,
        options: DetectionOptions,
    ):
        """
        Return the offsets to scan for a numeric type.
        """
        return OffsetIterator.iterate(
            length=len(buffer),
            value_size=numeric_type.size,
            options=options,
        )


    def _decode_candidate(
        self,
        *,
        buffer: bytes,
        offset: int,
        numeric_type: NumericType,
        endianness: str,
        finite_only: bool,
    ):
        """
        Decode a numeric candidate and apply validity checks.
        """
        value = NumericDecoder.decode(
            buffer,
            offset,
            numeric_type,
            endianness=endianness,
        )

        if value is None:
            return None

        if (
            finite_only
            and isinstance(value.value, float)
            and not math.isfinite(value.value)
        ):
            return None

        return value


    def _scan_numeric_type(
        self,
        *,
        buffer: bytes,
        numeric_type: NumericType,
        options: DetectionOptions,
        endian_list: tuple[str, ...],
        integers: bool,
        floats: bool,
        finite_only: bool,
        results: list,
        seen: set,
    ) -> bool:
        """Scan a single numeric type. Return False if max_results reached."""
        max_results = options.max_results

        if numeric_type.floating and not floats:
            return True
        if not numeric_type.floating and not integers:
            return True

        offsets = self._offsets(
            buffer=buffer,
            numeric_type=numeric_type,
            options=options,
        )

        for offset in offsets:
            if max_results is not None and len(results) >= max_results:
                return False
            if offset % numeric_type.size != 0:
                continue
            for current_endianness in endian_list:
                if max_results is not None and len(results) >= max_results:
                    return False
                value = self._decode_candidate(
                    buffer=buffer,
                    offset=offset,
                    numeric_type=numeric_type,
                    endianness=current_endianness,
                    finite_only=finite_only,
                )
                if value is None:
                    continue
                key=(value.offset,value.type_name,value.endianness)
                if key in seen:
                    continue
                seen.add(key)
                results.append(value)
        return True


    def _detect(
        self,
        data,
        options=None,
        *,
        integers=True,
        floats=True,
        finite_only=True,
        endianness=None,
        scan_all_endianness=False,
    ):


        if options is None:

            options = DetectionOptions()



        if not self._is_enabled(options, self.detector_type):
            return []

        max_results = options.max_results



        endian_list = self._endianness_list(
            endianness=endianness,
            scan_all_endianness=scan_all_endianness,
        )



        buffer = bytes(self._buffer(data, options))



        results = []

        seen = set()



        for numeric_type in self._numeric_types:
            if not self._scan_numeric_type(
                buffer=buffer,
                numeric_type=numeric_type,
                options=options,
                endian_list=endian_list,
                integers=integers,
                floats=floats,
                finite_only=finite_only,
                results=results,
                seen=seen,
            ):
                return list(self._limit_results(results, options))

        return list(self._limit_results(results, options))

