"""
Reconstruction context.

This module defines the immutable context passed to every reconstruction
heuristic. It contains the damaged binary data together with optional metadata
that heuristics can use to infer missing or corrupted structures.

The context must never be modified by heuristics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ReconstructionContext:
    """
    Context supplied to every reconstruction heuristic.

    Parameters
    ----------
    data:
        Raw binary buffer being analysed.

    offset:
        Offset of the current structure within the original file.

    metadata:
        Optional information supplied by previous recovery stages
        (parser, inspector, inference engine...).

    attributes:
        Arbitrary immutable key/value store allowing future extensions
        without changing the constructor.
    """

    data: bytes
    offset: int = 0
    metadata: Mapping[str, Any] = field(default_factory=dict)
    attributes: Mapping[str, Any] = field(default_factory=dict)

    @property
    def size(self) -> int:
        """Return the size of the binary buffer."""
        return len(self.data)

    def has_metadata(self, key: str) -> bool:
        """Return True if a metadata entry exists."""
        return key in self.metadata

    def metadata_value(self, key: str, default: Any = None) -> Any:
        """Safely retrieve a metadata value."""
        return self.metadata.get(key, default)

    def attribute(self, key: str, default: Any = None) -> Any:
        """Safely retrieve an extension attribute."""
        return self.attributes.get(key, default)

    def slice(
        self,
        start: int,
        length: int,
    ) -> bytes:
        """
        Return a slice of the binary buffer.

        Values outside the buffer are silently clamped.
        """

        if start < 0:
            start = 0

        end = max(start, start + length)

        return self.data[start:end]

    def contains(
        self,
        signature: bytes,
    ) -> bool:
        """
        Return True if the binary buffer contains the given signature.
        """

        return signature in self.data

    def describe(self) -> dict[str, Any]:
        """
        Return a serialisable description of the reconstruction context.

        Useful for logging and debugging.
        """

        return {
            "offset": self.offset,
            "size": self.size,
            "metadata_keys": sorted(self.metadata.keys()),
            "attribute_keys": sorted(self.attributes.keys()),
        }