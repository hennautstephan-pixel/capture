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


            if (
                max_results is not None
                and len(results) >= max_results
            ):

                return list(self._limit_results(results, options))



            if (
                numeric_type.floating
                and not floats
            ):

                continue



            if (
                not numeric_type.floating
                and not integers
            ):

                continue



            offsets = OffsetIterator.iterate(
                length=len(buffer),
                value_size=numeric_type.size,
                options=options,
            )



            for offset in offsets:


                if (
                    max_results is not None
                    and len(results) >= max_results
                ):

                    return list(self._limit_results(results, options))



                if offset % numeric_type.size != 0:

                    continue



                for current_endianness in endian_list:



                    if (
                        max_results is not None
                        and len(results) >= max_results
                    ):

                        return list(self._limit_results(results, options))



                    value = NumericDecoder.decode(
                        buffer,
                        offset,
                        numeric_type,
                        endianness=current_endianness,
                    )



                    if value is None:

                        continue



                    if (
                        finite_only
                        and isinstance(
                            value.value,
                            float,
                        )
                        and not math.isfinite(
                            value.value
                        )
                    ):

                        continue



                    key = (
                        value.offset,
                        value.type_name,
                        value.endianness,
                    )



                    if key in seen:

                        continue



                    seen.add(key)

                    results.append(
                        value
                    )



        return list(self._limit_results(results, options))