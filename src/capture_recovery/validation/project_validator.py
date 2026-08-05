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
        """
        Validate a reconstructed project.
        """

        result = ValidationResult()

        if project is None:
            result.add_error(
                "Project is missing"
            )

            return result

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
        """
        Validate fixture patch consistency.
        """

        fixtures = getattr(
            project,
            "fixtures",
            [],
        )

        used_addresses: set[tuple[int, int]] = set()

        for fixture in fixtures:

            universe = fixture.get(
                "universe",
            )

            address = fixture.get(
                "address",
            )

            identifier = getattr(
                fixture,
                "identifier",
                "unknown",
            )

            if universe is None:
                result.add_error(
                    f"Fixture {identifier}: missing universe"
                )

                continue

            if address is None:
                result.add_error(
                    f"Fixture {identifier}: missing address"
                )

                continue

            if not 1 <= address <= 512:
                result.add_error(
                    f"Fixture {identifier}: invalid DMX address"
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
        """
        Validate universe declarations.
        """

        universes = getattr(
            project,
            "universes",
            [],
        )

        numbers: set[int] = set()

        for universe in universes:

            number = universe.get(
                "universe",
            )

            identifier = getattr(
                universe,
                "identifier",
                "unknown",
            )

            if number is None:
                result.add_error(
                    f"Universe {identifier}: missing number"
                )

                continue

            if number in numbers:
                result.add_error(
                    f"Duplicate universe {number}"
                )

            numbers.add(
                number,
            )