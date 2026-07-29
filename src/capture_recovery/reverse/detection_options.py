"""
capture_recovery.reverse.detection_options

Shared configuration object for every detector.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .detection_strategy import DetectionStrategy
from .detector_type import DetectorType


@dataclass(slots=True, frozen=True, kw_only=True)
class DetectionOptions:
    """
    Common configuration used by all detectors.

    The object validates and normalizes its data at creation time.

    After initialization:

    - offsets are sorted
    - duplicate offsets are removed
    - offsets are immutable
    - detector types are immutable
    """

    strategy: DetectionStrategy = DetectionStrategy.SCAN

    start: int = 0

    stop: int | None = None

    alignment: int = 1

    offsets: tuple[int, ...] = field(
        default_factory=tuple,
    )

    finite_only: bool = True

    enabled_types: frozenset[DetectorType] | None = None


    def __post_init__(self) -> None:
        """
        Validate and normalize configuration.
        """

        self._validate_range()

        self._validate_alignment()

        self._validate_offsets()

        self._normalize_offsets()

        self._normalize_types()


    def _validate_range(self) -> None:
        """
        Validate scan boundaries.
        """

        if self.start < 0:
            raise ValueError(
                "start must be >= 0"
            )

        if (
            self.stop is not None
            and self.stop < self.start
        ):
            raise ValueError(
                "stop must be >= start"
            )


    def _validate_alignment(self) -> None:
        """
        Validate alignment.
        """

        if self.alignment <= 0:
            raise ValueError(
                "alignment must be > 0"
            )


    def _validate_offsets(self) -> None:
        """
        Validate custom offsets.
        """

        if any(
            offset < 0
            for offset in self.offsets
        ):
            raise ValueError(
                "offsets must be >= 0"
            )

        if (
            self.strategy
            is DetectionStrategy.CUSTOM
            and not self.offsets
        ):
            raise ValueError(
                "custom strategy requires offsets"
            )


    def _normalize_offsets(self) -> None:
        """
        Normalize offsets.

        Example:

        (50, 10, 50, 20)

        becomes:

        (10, 20, 50)
        """

        normalized = tuple(
            sorted(
                set(self.offsets)
            )
        )

        object.__setattr__(
            self,
            "offsets",
            normalized,
        )


    def _normalize_types(self) -> None:
        """
        Normalize enabled detector types.
        """

        if self.enabled_types is None:
            return

        object.__setattr__(
            self,
            "enabled_types",
            frozenset(
                self.enabled_types
            ),
        )


    def allows_type(
        self,
        detector_type: DetectorType,
    ) -> bool:
        """
        Check whether a detector type is enabled.

        If no filter is defined,
        every type is allowed.
        """

        if self.enabled_types is None:
            return True

        return detector_type in self.enabled_types


    def has_custom_offsets(self) -> bool:
        """
        Return True if explicit offsets exist.
        """

        return bool(self.offsets)