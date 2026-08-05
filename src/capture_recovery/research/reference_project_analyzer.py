from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib



@dataclass(frozen=True, slots=True)
class ReferenceBlock:
    """
    Binary block extracted from a reference project.
    """

    offset: int

    size: int

    signature: str

    data: bytes



@dataclass(frozen=True, slots=True)
class ReferenceProjectModel:
    """
    Indexed representation of a valid Capture project.
    """

    source: Path

    size: int

    blocks: tuple[ReferenceBlock, ...]



class ReferenceProjectAnalyzer:
    """
    Analyze a valid Capture project.

    Current responsibilities:
    - load binary data
    - split into blocks
    - generate stable signatures

    Future:
    - Capture object detection
    - object relations
    - semantic extraction
    """



    DEFAULT_BLOCK_SIZE = 64



    def __init__(
        self,
        block_size: int = DEFAULT_BLOCK_SIZE,
    ) -> None:

        if block_size <= 0:
            raise ValueError(
                "Block size must be positive."
            )

        self._block_size = block_size



    def analyze(
        self,
        project: Path,
    ) -> ReferenceProjectModel:
        """
        Analyze a reference project file.
        """

        if not project.exists():

            raise FileNotFoundError(
                project
            )


        data = project.read_bytes()


        blocks = []


        for offset in range(
            0,
            len(data),
            self._block_size,
        ):

            chunk = data[
                offset:
                offset + self._block_size
            ]


            blocks.append(
                ReferenceBlock(
                    offset=offset,
                    size=len(chunk),
                    signature=self._signature(
                        chunk
                    ),
                    data=chunk,
                )
            )


        return ReferenceProjectModel(
            source=project,
            size=len(data),
            blocks=tuple(blocks),
        )



    def _signature(
        self,
        data: bytes,
    ) -> str:
        """
        Generate binary fingerprint.
        """

        return hashlib.sha256(
            data
        ).hexdigest()