from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.recovery.intelligent_restore_action import (
    IntelligentRestoreAction,
)

from capture_recovery.recovery.binary_repair_writer import (
    BinaryRepairWriter,
    BinaryRepairOperation,
    BinaryRepairResult,
)


@dataclass(slots=True, frozen=True)
class BinaryExecutionResult:
    """
    Result of binary repair execution.
    """

    actions: tuple[BinaryRepairResult, ...]



class BinaryRepairExecutor:
    """
    Execute intelligent restore actions
    through BinaryRepairWriter.
    """

    def __init__(
        self,
        writer: BinaryRepairWriter | None = None,
    ) -> None:

        self._writer = (
            writer
            if writer is not None
            else BinaryRepairWriter()
        )


    def execute_action(
        self,
        action: IntelligentRestoreAction,
        source: Path,
        output: Path,
        replacement: bytes,
    ) -> BinaryRepairResult:
        """
        Execute one intelligent repair action.
        """

        operation = BinaryRepairOperation(
            offset=action.offset,
            original_size=action.size,
            replacement=replacement,
        )


        return self._writer.write_repaired_file(
            source,
            output,
            (
                operation,
            ),
        )



    def execute_plan(
        self,
        actions: tuple[IntelligentRestoreAction, ...],
        source: Path,
        output: Path,
        replacements: tuple[bytes, ...],
    ) -> BinaryExecutionResult:
        """
        Execute multiple repair actions.
        """

        results = []


        for action, replacement in zip(
            actions,
            replacements,
        ):

            result = self.execute_action(
                action,
                source,
                output,
                replacement,
            )

            results.append(
                result,
            )


        return BinaryExecutionResult(
            actions=tuple(results),
        )