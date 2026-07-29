"""
capture_recovery.reverse.offset_iterator

Generate valid offsets for binary detection.
"""

from __future__ import annotations

from collections.abc import Iterator

from .detection_options import DetectionOptions
from .detection_strategy import DetectionStrategy


class OffsetIterator:
    """
    Generate offsets according to DetectionOptions.
    """


    @staticmethod
    def iterate(
        length: int,
        value_size: int,
        options: DetectionOptions,
    ) -> Iterator[int]:
        """
        Generate offsets.

        Parameters
        ----------
        length:
            Buffer size.

        value_size:
            Size of detected value.

        options:
            Detection configuration.
        """

        if length < 0:
            raise ValueError(
                "length must be >= 0"
            )


        if value_size <= 0:
            raise ValueError(
                "value_size must be > 0"
            )


        if options.strategy is DetectionStrategy.CUSTOM:

            yield from OffsetIterator._custom(
                length,
                value_size,
                options,
            )


        elif options.strategy is DetectionStrategy.ALIGNED:

            yield from OffsetIterator._aligned(
                length,
                value_size,
                options,
            )


        else:

            yield from OffsetIterator._scan(
                length,
                value_size,
                options,
            )



    @staticmethod
    def _scan(
        length: int,
        value_size: int,
        options: DetectionOptions,
    ) -> Iterator[int]:
        """
        Scan every possible offset.
        """

        stop = (
            options.stop
            if options.stop is not None
            else length
        )


        maximum = stop - value_size + 1


        for offset in range(
            options.start,
            maximum,
        ):
            yield offset



    @staticmethod
    def _aligned(
        length: int,
        value_size: int,
        options: DetectionOptions,
    ) -> Iterator[int]:
        """
        Generate aligned offsets.
        """

        stop = (
            options.stop
            if options.stop is not None
            else length
        )


        maximum = stop - value_size + 1


        alignment = (
            options.alignment
            if options.alignment
            else value_size
        )


        for offset in range(
            options.start,
            maximum,
            alignment,
        ):
            yield offset



    @staticmethod
    def _custom(
        length: int,
        value_size: int,
        options: DetectionOptions,
    ) -> Iterator[int]:
        """
        Generate custom offsets.
        """

        maximum = length - value_size


        for offset in options.offsets:

            if offset <= maximum:

                yield offset



    @staticmethod
    def list_offsets(
        length: int,
        value_size: int,
        options: DetectionOptions,
    ) -> list[int]:
        """
        Convenience helper.

        Compatibility API used by tests and callers
        needing a materialized list.
        """

        return list(
            OffsetIterator.iterate(
                length,
                value_size,
                options,
            )
        )