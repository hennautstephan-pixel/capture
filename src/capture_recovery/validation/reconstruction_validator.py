"""
Reconstruction validator.

Checks reconstructed Capture projects.
"""

from __future__ import annotations


class ReconstructionValidator:
    """
    Validate reconstructed projects.
    """

    def validate(
        self,
        project,
    ) -> list[str]:
        """
        Return validation errors.
        """

        errors = []


        for fixture in project.fixtures:

            if not fixture.name:

                errors.append(
                    "Fixture without name"
                )


            if fixture.universe < 0:

                errors.append(
                    "Invalid universe"
                )


            if fixture.address < 0:

                errors.append(
                    "Invalid address"
                )


        return errors