from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


@dataclass(slots=True, frozen=True)
class BinaryRepairOperation:
    """
    Describes a binary replacement operation.
    """

    offset: int

    original_size: int

    replacement: bytes



@dataclass(slots=True, frozen=True)
class BinaryRepairResult:
    """
    Result of a binary repair operation.
    """

    source: Path

    output: Path

    backup: Path

    operations: tuple[BinaryRepairOperation, ...]



class BinaryRepairWriter:
    """
    Safe binary repair writer.

    The original file is never modified directly.
    """

    def __init__(
        self,
        *,
        create_backup: bool = True,
    ) -> None:

        self._create_backup = create_backup


    def create_backup(
        self,
        source: Path,
        backup: Path,
    ) -> Path:
        """
        Create a backup copy.
        """

        shutil.copy2(
            source,
            backup,
        )

        return backup



    def write_repaired_file(
        self,
        source: Path,
        output: Path,
        operations: tuple[
            BinaryRepairOperation,
            ...,
        ],
    ) -> BinaryRepairResult:
        """
        Create a repaired binary file.

        Operations are applied on a copy only.
        """

        source = Path(source)

        output = Path(output)


        backup = output.with_suffix(
            output.suffix + ".bak"
        )


        if self._create_backup:

            self.create_backup(
                source,
                backup,
            )


        data = bytearray(
            source.read_bytes()
        )


        for operation in operations:

            self._apply_operation(
                data,
                operation,
            )


        output.write_bytes(
            bytes(data)
        )


        return BinaryRepairResult(
            source=source,
            output=output,
            backup=backup,
            operations=operations,
        )



    def _apply_operation(
        self,
        data: bytearray,
        operation: BinaryRepairOperation,
    ) -> None:
        """
        Apply one controlled binary replacement.
        """

        start = operation.offset

        end = (
            operation.offset
            +
            operation.original_size
        )


        if start < 0:

            raise ValueError(
                "Offset must be positive."
            )


        if end > len(data):

            raise ValueError(
                "Operation exceeds file size."
            )


        data[start:end] = (
            operation.replacement
        )