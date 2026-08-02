from __future__ import annotations

import struct

from .header import CaptureHeader


class CaptureHeaderParser:

    PROJECT = b"Project\x00"

    SOFTWARE = b"SoftwareVersion\x00"

    FIRST_ZLIB = b"\x78\x9c"

    def parse(
        self,
        data: bytes,
    ) -> CaptureHeader:

        if len(data) < 64:
            raise ValueError("File too small.")

        file_size = struct.unpack_from("<I", data, 0)[0]

        if data[4:12] != self.PROJECT:
            raise ValueError("Invalid Project signature.")

        format_version = struct.unpack_from("<I", data, 16)[0]

        software_start = 20

        software_end = data.index(
            b"\x00",
            software_start,
        )

        software_tag = data[
            software_start:software_end
        ].decode("ascii")

        software_tag_version = struct.unpack_from(
            "<I",
            data,
            software_end + 1,
        )[0]

        first_stream_offset = data.index(
            self.FIRST_ZLIB
        )

        reserved = data[
            software_end + 5:first_stream_offset
        ]

        raw = data[:first_stream_offset]

        return CaptureHeader(
            file_size=file_size,
            project_tag="Project",
            format_version=format_version,
            software_tag=software_tag,
            software_tag_version=software_tag_version,
            first_stream_offset=first_stream_offset,
            reserved=reserved,
            raw=raw,
        )