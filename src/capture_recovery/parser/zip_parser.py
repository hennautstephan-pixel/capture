from __future__ import annotations

from dataclasses import dataclass
from zipfile import ZipFile
from io import BytesIO

from .container_extractor import ExtractedContainer


@dataclass(slots=True)
class ZipEntry:
    name: str
    compressed_size: int
    size: int
    crc: int
    data: bytes


class ZipParser:
    """
    Parse the content of an extracted ZIP container.
    """

    @staticmethod
    def parse(container: ExtractedContainer) -> list[ZipEntry]:

        if container.kind != "zip":
            raise ValueError("container is not a ZIP archive")

        archive = ZipFile(BytesIO(container.data))

        entries: list[ZipEntry] = []

        for info in archive.infolist():
            entries.append(
                ZipEntry(
                    name=info.filename,
                    compressed_size=info.compress_size,
                    size=info.file_size,
                    crc=info.CRC,
                    data=archive.read(info.filename),
                )
            )

        return entries