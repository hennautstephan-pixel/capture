from __future__ import annotations

from dataclasses import dataclass


from capture_recovery.reconstruction.reconstruction_strategy import (
    ReconstructionDecision,
)



@dataclass(frozen=True, slots=True)
class ReconstructionResult:
    """
    Result after applying a reconstruction.
    """

    data: bytes

    offset: int

    size: int

    success: bool



class ReconstructionExecutor:
    """
    Applies reconstruction decisions
    to binary data.
    """



    def execute(
        self,
        source: bytes,
        decision: ReconstructionDecision,
    ) -> ReconstructionResult:
        """
        Apply a reconstruction decision.
        """

        offset = decision.offset

        size = decision.size


        if offset < 0:

            return ReconstructionResult(
                data=source,

                offset=offset,

                size=size,

                success=False,
            )


        if offset > len(source):

            return ReconstructionResult(
                data=source,

                offset=offset,

                size=size,

                success=False,
            )


        end = offset + size


        if end > len(source):

            return ReconstructionResult(
                data=source,

                offset=offset,

                size=size,

                success=False,
            )


        repaired = (
            source[:offset]
            +
            decision.replacement
            +
            source[end:]
        )


        return ReconstructionResult(
            data=repaired,

            offset=offset,

            size=size,

            success=True,
        )



    def apply(
        self,
        source: bytes,
        decision: ReconstructionDecision,
    ) -> bytes:
        """
        Compatibility shortcut.

        Returns repaired bytes.
        """

        result = self.execute(
            source,

            decision,
        )


        return result.data