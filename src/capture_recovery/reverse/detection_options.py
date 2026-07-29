"""
capture_recovery.reverse.detection_options

Shared configuration object for every detector.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .detection_strategy import DetectionStrategy
from .detector_type import DetectorType


@dataclass(
    slots=True,
    frozen=True,
    kw_only=True,
)
class DetectionOptions:

    strategy: DetectionStrategy = (
        DetectionStrategy.SCAN
    )

    start: int = 0

    stop: int | None = None

    alignment: int = 1

    offsets: tuple[int, ...] = field(
        default_factory=tuple
    )

    finite_only: bool = True

    # Limite uniquement utilisée
    # pour les gros fichiers
    max_results: int | None = None

    # Protection gros fichiers
    max_scan_size: int | None = None

    enabled_types: frozenset[DetectorType] | None = None


    def __post_init__(self):

        self._validate_range()

        self._validate_alignment()

        self._validate_limits()

        self._validate_offsets()

        self._normalize_offsets()

        self._normalize_types()



    def _validate_range(self):

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



    def _validate_alignment(self):

        if self.alignment <= 0:

            raise ValueError(
                "alignment must be > 0"
            )



    def _validate_limits(self):

        if (
            self.max_results is not None
            and self.max_results <= 0
        ):

            raise ValueError(
                "max_results must be > 0"
            )



        if (
            self.max_scan_size is not None
            and self.max_scan_size <= 0
        ):

            raise ValueError(
                "max_scan_size must be > 0"
            )



    def _validate_offsets(self):

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



    def _normalize_offsets(self):

        object.__setattr__(
            self,
            "offsets",
            tuple(
                sorted(
                    set(
                        self.offsets
                    )
                )
            ),
        )



    def _normalize_types(self):

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

        if self.enabled_types is None:

            return True


        return detector_type in self.enabled_types



    def has_custom_offsets(self):

        return bool(
            self.offsets
        )