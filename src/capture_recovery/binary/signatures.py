"""
Binary signature detection utilities.

Provides a simple registry of well-known binary signatures (magic bytes)
and helper functions to identify binary formats.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


__all__ = [
    "BinarySignature",
    "SignatureRegistry",
]


@dataclass(slots=True, frozen=True)
class BinarySignature:
    """
    Represents a binary signature.
    """

    name: str
    pattern: bytes
    offset: int = 0
    description: str = ""


class SignatureRegistry:
    """
    Registry of binary signatures.
    """

    def __init__(self) -> None:
        self._signatures: list[BinarySignature] = []

        self._register_defaults()

    def __iter__(self) -> Iterable[BinarySignature]:
        return iter(self._signatures)

    def __len__(self) -> int:
        return len(self._signatures)

    def register(self, signature: BinarySignature) -> None:
        """
        Register a new signature.
        """

        self._signatures.append(signature)

    def clear(self) -> None:
        """
        Remove all signatures.
        """

        self._signatures.clear()

    def match(self, data: bytes) -> BinarySignature | None:
        """
        Return the first matching signature.
        """

        for signature in self._signatures:

            offset = signature.offset
            end = offset + len(signature.pattern)

            if len(data) < end:
                continue

            if data[offset:end] == signature.pattern:
                return signature

        return None

    def matches(self, data: bytes) -> list[BinarySignature]:
        """
        Return every matching signature.
        """

        matches: list[BinarySignature] = []

        for signature in self._signatures:

            offset = signature.offset
            end = offset + len(signature.pattern)

            if len(data) < end:
                continue

            if data[offset:end] == signature.pattern:
                matches.append(signature)

        return matches

    def identify(self, data: bytes) -> str | None:
        """
        Return the signature name.
        """

        signature = self.match(data)

        if signature is None:
            return None

        return signature.name

    def _register_defaults(self) -> None:

        defaults = [

            BinarySignature(
                name="ZIP",
                pattern=b"PK\x03\x04",
                description="ZIP archive",
            ),

            BinarySignature(
                name="PNG",
                pattern=b"\x89PNG\r\n\x1a\n",
                description="Portable Network Graphics",
            ),

            BinarySignature(
                name="JPEG",
                pattern=b"\xff\xd8\xff",
                description="JPEG image",
            ),

            BinarySignature(
                name="GIF87a",
                pattern=b"GIF87a",
                description="GIF image",
            ),

            BinarySignature(
                name="GIF89a",
                pattern=b"GIF89a",
                description="GIF image",
            ),

            BinarySignature(
                name="PDF",
                pattern=b"%PDF-",
                description="Portable Document Format",
            ),

            BinarySignature(
                name="RIFF",
                pattern=b"RIFF",
                description="RIFF container",
            ),

            BinarySignature(
                name="Ogg",
                pattern=b"OggS",
                description="Ogg container",
            ),

            BinarySignature(
                name="SQLite",
                pattern=b"SQLite format 3\x00",
                description="SQLite database",
            ),

            BinarySignature(
                name="ELF",
                pattern=b"\x7fELF",
                description="ELF executable",
            ),

            BinarySignature(
                name="PE",
                pattern=b"MZ",
                description="Portable Executable",
            ),

            BinarySignature(
                name="GZIP",
                pattern=b"\x1f\x8b",
                description="GZip archive",
            ),

            BinarySignature(
                name="BZIP2",
                pattern=b"BZh",
                description="BZip2 archive",
            ),

            BinarySignature(
                name="XZ",
                pattern=b"\xfd7zXZ\x00",
                description="XZ archive",
            ),

            BinarySignature(
                name="7ZIP",
                pattern=b"7z\xbc\xaf\x27\x1c",
                description="7-Zip archive",
            ),

            BinarySignature(
                name="RAR",
                pattern=b"Rar!\x1a\x07",
                description="RAR archive",
            ),

            BinarySignature(
                name="XML",
                pattern=b"<?xml",
                description="XML document",
            ),
        ]

        self._signatures.extend(defaults)