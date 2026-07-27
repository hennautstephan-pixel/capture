from __future__ import annotations

from capture_recovery.models.project import Project

from .validation_result import ValidationResult


class ProjectValidator:
    """
    Validate reconstructed Capture projects.
    """

    def validate(
        self,
        project: Project,
    ) -> ValidationResult:

        result = ValidationResult()

        self._validate_fixtures(
            project,
            result,
        )

        self._validate_universes(
            project,
            result,
        )

        return result

    def _validate_fixtures(
        self,
        project: Project,
        result: ValidationResult,
    ) -> None:

        used_addresses: set[tuple[int, int]] = set()

        for fixture in project.fixtures:

            universe = fixture.get(
                "universe",
            )

            address = fixture.get(
                "address",
            )

            if universe is None:
                result.add_error(
                    f"Fixture {fixture.identifier}: missing universe"
                )

                continue

            if address is None:
                result.add_error(
                    f"Fixture {fixture.identifier}: missing address"
                )

                continue

            if not 1 <= address <= 512:
                result.add_error(
                    f"Fixture {fixture.identifier}: invalid DMX address"
                )

            key = (
                universe,
                address,
            )

            if key in used_addresses:
                result.add_error(
                    f"Duplicate DMX address universe={universe} address={address}"
                )

            used_addresses.add(
                key,
            )

    def _validate_universes(
        self,
        project: Project,
        result: ValidationResult,
    ) -> None:

        numbers: set[int] = set()

        for universe in project.universes:

            number = universe.get(
                "universe",
            )

            if number is None:
                result.add_error(
                    f"Universe {universe.identifier}: missing number"
                )

                continue

            if number in numbers:
                result.add_error(
                    f"Duplicate universe {number}"
                )

            numbers.add(
                number,
            )