"""
capture_recovery.reverse.guid_decoder

Decode binary GUID values.
"""

from __future__ import annotations

import uuid

from .guid_type import (
    GuidType,
    WINDOWS_GUID,
    RFC4122_UUID,
)

from .guid_value import GuidValue



class GuidDecoder:
    """
    Decode GUID binary representations.
    """


    @staticmethod
    def can_decode(
        data: bytes,
        offset: int,
        guid_type: GuidType,
    ) -> bool:
        """
        Check if a GUID can be decoded.
        """

        if offset < 0:
            return False


        return (
            offset + guid_type.size
            <= len(data)
        )



    @staticmethod
    def decode(
        data: bytes,
        offset: int,
        guid_type: GuidType = WINDOWS_GUID,
    ) -> GuidValue | None:
        """
        Decode a GUID.

        Returns None if invalid.
        """

        if not GuidDecoder.can_decode(
            data,
            offset,
            guid_type,
        ):
            return None



        raw = data[
            offset:
            offset + guid_type.size
        ]



        if guid_type.microsoft_order:

            value = GuidDecoder._decode_windows(
                raw
            )

        else:

            value = str(
                uuid.UUID(
                    bytes=raw
                )
            )



        return GuidValue(
            offset=offset,
            guid_type=guid_type,
            value=value,
            raw_bytes=raw,
        )



    @staticmethod
    def _decode_windows(
        raw: bytes,
    ) -> str:
        """
        Decode Microsoft GUID layout.
        """

        data1 = int.from_bytes(
            raw[0:4],
            byteorder="little",
        )


        data2 = int.from_bytes(
            raw[4:6],
            byteorder="little",
        )


        data3 = int.from_bytes(
            raw[6:8],
            byteorder="little",
        )


        data4 = raw[8:16]



        return (
            f"{data1:08x}-"
            f"{data2:04x}-"
            f"{data3:04x}-"
            f"{data4[0]:02x}"
            f"{data4[1]:02x}-"
            f"{data4[2:].hex()}"
        )