from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .object_mapper import CandidateObject
from .repair_plan import (
    ExecutionPlan,
    RepairOperation,
)


@dataclass(slots=True, frozen=True)
class RebuiltChunk:
    """
    One rebuilt binary region.
    """

    offset: int

    data: bytes

    @property
    def length(self) -> int:
        return len(self.data)


@dataclass(slots=True, frozen=True)
class StreamRebuildResult:
    """
    Result of a stream reconstruction.
    """

    chunks: list[RebuiltChunk]

    stream: bytes

    repaired_objects: int

    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def size(self) -> int:
        return len(self.stream)

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)

    @property
    def is_empty(self) -> bool:
        return self.size == 0


class StreamRebuilder:
    """
    Rebuild a binary stream from repaired objects.
    """

    def rebuild(
        self,
        plan: ExecutionPlan,
        objects: Iterable[CandidateObject],
    ) -> StreamRebuildResult:

        chunks: list[RebuiltChunk] = []

        stream = bytearray()

        repaired = 0

        warnings: list[str] = []

        rebuild_required = any(
            task.operation is RepairOperation.REBUILD_STREAM
            for task in plan.tasks
        )

        if not rebuild_required:
            return StreamRebuildResult(
                chunks=[],
                stream=b"",
                repaired_objects=0,
                warnings=(),
            )

        for obj in objects:

            try:
                data = obj.encode()
            except Exception as exc:
                warnings.append(
                    f"Failed to encode object at offset {obj.offset}: {exc}"
                )
                continue

            if data is None:
                data = b""

            if not isinstance(data, bytes):
                data = bytes(data)

            chunks.append(
                RebuiltChunk(
                    offset=len(stream),
                    data=data,
                )
            )

            stream.extend(data)

            repaired += 1

        return StreamRebuildResult(
            chunks=chunks,
            stream=bytes(stream),
            repaired_objects=repaired,
            warnings=tuple(warnings),
        )