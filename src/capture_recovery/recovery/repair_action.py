"""
Repair actions.

A repair action encapsulates one atomic repair that can be executed by
ProjectRepairEngine or ObjectRepairEngine.

Repair actions never mutate the supplied object directly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping


class RepairStatus(str, Enum):
    """Status returned by a repair action."""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


@dataclass(slots=True, frozen=True)
class RepairResult:
    """
    Result returned by one repair action.
    """

    status: RepairStatus

    action: str

    message: str = ""

    repaired_objects: int = 0

    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )

    @property
    def succeeded(self) -> bool:
        return self.status is RepairStatus.SUCCESS

    @property
    def failed(self) -> bool:
        return self.status is RepairStatus.FAILED

    @property
    def skipped(self) -> bool:
        return self.status is RepairStatus.SKIPPED

    @property
    def blocked(self) -> bool:
        return self.status is RepairStatus.BLOCKED

    @property
    def executed(self) -> bool:
        """
        True if the repair has actually been executed.
        """

        return self.status in (
            RepairStatus.SUCCESS,
            RepairStatus.FAILED,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "action": self.action,
            "message": self.message,
            "repaired_objects": self.repaired_objects,
            "metadata": dict(self.metadata),
        }

    # ------------------------------------------------------------------
    # Factory methods
    # ------------------------------------------------------------------

    @classmethod
    def success_result(
        cls,
        *,
        action: str,
        repaired_objects: int = 0,
        message: str = "",
        **metadata: Any,
    ) -> "RepairResult":
        return cls(
            status=RepairStatus.SUCCESS,
            action=action,
            repaired_objects=repaired_objects,
            message=message,
            metadata=metadata,
        )

    @classmethod
    def failed_result(
        cls,
        *,
        action: str,
        message: str = "",
        **metadata: Any,
    ) -> "RepairResult":
        return cls(
            status=RepairStatus.FAILED,
            action=action,
            message=message,
            metadata=metadata,
        )

    @classmethod
    def skipped_result(
        cls,
        *,
        action: str,
        message: str = "",
        **metadata: Any,
    ) -> "RepairResult":
        return cls(
            status=RepairStatus.SKIPPED,
            action=action,
            message=message,
            metadata=metadata,
        )

    @classmethod
    def blocked_result(
        cls,
        *,
        action: str,
        message: str = "",
        **metadata: Any,
    ) -> "RepairResult":
        return cls(
            status=RepairStatus.BLOCKED,
            action=action,
            message=message,
            metadata=metadata,
        )


class RepairAction(ABC):
    """
    Base class for every repair action.

    Each repair action performs exactly one repair.
    """

    priority: int = 100

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def applicable(
        self,
        project: Any,
        report: Any,
    ) -> bool:
        """
        Return True if this repair can currently be executed.
        """

        return True

    @abstractmethod
    def execute(
        self,
        project: Any,
        report: Any,
    ) -> RepairResult:
        """
        Execute one repair operation.
        """
        raise NotImplementedError

    def __lt__(
        self,
        other: object,
    ) -> bool:
        if not isinstance(other, RepairAction):
            return NotImplemented

        # Highest priority first.
        return self.priority > other.priority

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(priority={self.priority})"
        )