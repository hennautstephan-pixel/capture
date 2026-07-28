"""
Project finalization.

Final validation and completion
of reconstructed projects.
"""

from __future__ import annotations


class ProjectFinalize:
    """
    Finalize reconstructed projects.
    """

    def finalize(
        self,
        project,
    ):
        """
        Prepare project for export.
        """

        if project.scene is None:

            return project


        project.metadata[
            "reconstructed"
        ] = True


        project.metadata[
            "fixture_count"
        ] = len(
            project.fixtures
        )


        return project