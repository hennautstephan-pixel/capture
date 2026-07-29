from __future__ import annotations

import gzip
import zlib
from dataclasses import dataclass, field
from io import BytesIO
from zipfile import ZipFile, BadZipFile

from .container_detector import Container


@dataclass(slots=True)
class ExtractedContainer:
    kind: str
    data: bytes
    metadata: dict[str, object] = field(default_factory=dict)


class ContainerExtractor:
    """
    Extract the payload of supported containers.
    """

    @classmethod
    def extract(
        cls,
        container: Container,
        data: bytes | bytearray | memoryview,
    ) -> ExtractedContainer:

        raw = memoryview(data)[
            container.offset:container.offset + container.length
        ].tobytes()

        if container.kind == "zlib":
            return ExtractedContainer(
                kind="zlib",
                data=zlib.decompress(raw),
            )

        if container.kind == "gzip":
            return ExtractedContainer(
                kind="gzip",
                data=gzip.decompress(raw),
            )

        if container.kind == "zip":

            with ZipFile(BytesIO(raw)) as archive:

                files = {
                    name: archive.read(name)
                    for name in archive.namelist()
                }

            return ExtractedContainer(
                kind="zip",
                data=raw,
                metadata={
                    "files": files,
                    "names": list(files.keys()),
                },
            )

        return ExtractedContainer(
            kind=container.kind,
            data=raw,
        )