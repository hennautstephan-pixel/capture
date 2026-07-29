"""
capture_recovery.reverse.string_decoder

Decode binary buffers into strings.
"""

from __future__ import annotations

from .string_type import StringType
from .string_value import StringValue


class StringDecoder:
    """
    Decode binary strings.
    """

    @staticmethod
    def can_decode(
        data: bytes,
        offset: int,
        string_type: StringType,
    ) -> bool:

        if offset < 0:
            return False

        if offset >= len(data):
            return False

        try:
            data[offset:].decode(
                string_type.encoding,
                errors="strict",
            )
            return True

        except UnicodeDecodeError:
            return False


    @staticmethod
    def decode(
        data: bytes,
        offset: int,
        string_type: StringType,
        max_length: int | None = None,
    ) -> StringValue | None:

        if offset < 0:
            raise ValueError(
                "offset must be >= 0"
            )

        if offset >= len(data):
            return None


        raw = data[offset:]


        if max_length is not None:
            raw = raw[:max_length]


        terminated = False


        if string_type.null_terminated:

            raw, terminated = StringDecoder._remove_terminator(
                raw,
                string_type,
            )


        try:

            value = raw.decode(
                string_type.encoding,
                errors="strict",
            )

        except UnicodeDecodeError:

            return None


        return StringValue(
            offset=offset,
            string_type=string_type,
            value=value,
            raw_bytes=raw,
            terminated=terminated,
        )


    @staticmethod
    def _remove_terminator(
        data: bytes,
        string_type: StringType,
    ) -> tuple[bytes, bool]:
        """
        Remove NULL terminator.

        UTF16 must respect character alignment.
        """


        width = string_type.char_width


        if width == 1:

            index = data.find(
                b"\x00"
            )

            if index >= 0:

                return (
                    data[:index],
                    True,
                )

            return (
                data,
                False,
            )


        # UTF16 / wide strings

        terminator = b"\x00" * width


        for index in range(
            0,
            len(data) - width + 1,
            width,
        ):

            if data[index:index + width] == terminator:

                return (
                    data[:index],
                    True,
                )


        return (
            data,
            False,
        )