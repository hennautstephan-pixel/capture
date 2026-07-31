"""
Constraint validation.

Checks whether several PropertyConstraint instances are mutually
compatible.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from .bitmask_constraint import BitmaskConstraint
from .enum_constraint import EnumConstraint
from .property_constraint import PropertyConstraint
from .range_constraint import RangeConstraint
from .step_constraint import StepConstraint


@dataclass(frozen=True, slots=True)
class ConstraintConflict:
    """
    Represents a conflict between two constraints.
    """

    left: PropertyConstraint
    right: PropertyConstraint
    reason: str


@dataclass(frozen=True, slots=True)
class ConstraintValidationResult:
    """
    Result returned by ConstraintValidator.
    """

    valid: bool
    conflicts: tuple[ConstraintConflict, ...]


class ConstraintValidator:
    """
    Validates that several constraints are mutually compatible.
    """

    def validate(
        self,
        constraints: Sequence[PropertyConstraint],
    ) -> ConstraintValidationResult:

        conflicts: list[ConstraintConflict] = []

        constraints = tuple(constraints)

        for i, left in enumerate(constraints):

            for right in constraints[i + 1:]:

                reason = self._check(left, right)

                if reason is not None:

                    conflicts.append(
                        ConstraintConflict(
                            left=left,
                            right=right,
                            reason=reason,
                        )
                    )

        return ConstraintValidationResult(
            valid=not conflicts,
            conflicts=tuple(conflicts),
        )

    def _check(
        self,
        left: PropertyConstraint,
        right: PropertyConstraint,
    ) -> str | None:

        if isinstance(left, RangeConstraint) and isinstance(
            right,
            RangeConstraint,
        ):
            return self._range_vs_range(left, right)

        if isinstance(left, EnumConstraint) and isinstance(
            right,
            EnumConstraint,
        ):
            return self._enum_vs_enum(left, right)

        if isinstance(left, StepConstraint) and isinstance(
            right,
            StepConstraint,
        ):
            return self._step_vs_step(left, right)

        if isinstance(left, BitmaskConstraint) and isinstance(
            right,
            BitmaskConstraint,
        ):
            return self._bitmask_vs_bitmask(left, right)

        if isinstance(left, RangeConstraint) and isinstance(
            right,
            EnumConstraint,
        ):
            return self._range_vs_enum(left, right)

        if isinstance(left, EnumConstraint) and isinstance(
            right,
            RangeConstraint,
        ):
            return self._range_vs_enum(right, left)

        return None

    @staticmethod
    def _range_vs_range(
        left: RangeConstraint,
        right: RangeConstraint,
    ) -> str | None:

        if left.maximum < right.minimum:
            return "disjoint ranges"

        if right.maximum < left.minimum:
            return "disjoint ranges"

        return None

    @staticmethod
    def _enum_vs_enum(
        left: EnumConstraint,
        right: EnumConstraint,
    ) -> str | None:

        if set(left.values).isdisjoint(right.values):
            return "disjoint enums"

        return None

    @staticmethod
    def _step_vs_step(
        left: StepConstraint,
        right: StepConstraint,
    ) -> str | None:

        a = float(left.step)
        b = float(right.step)

        larger = max(a, b)
        smaller = min(a, b)

        quotient = larger / smaller

        if abs(round(quotient) - quotient) > 1e-9:
            return "incompatible steps"

        return None

    @staticmethod
    def _bitmask_vs_bitmask(
        left: BitmaskConstraint,
        right: BitmaskConstraint,
    ) -> str | None:

        union = left.mask | right.mask

        intersection = left.mask & right.mask

        if intersection == 0 and union != 0:
            return "independent bitmasks"

        return None

    @staticmethod
    def _range_vs_enum(
        range_constraint: RangeConstraint,
        enum_constraint: EnumConstraint,
    ) -> str | None:

        for value in enum_constraint.values:

            if (
                value < range_constraint.minimum
                or value > range_constraint.maximum
            ):
                return "enum outside range"

        return None