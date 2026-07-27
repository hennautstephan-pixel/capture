"""
Capture project JSON loader.

Loads a serialized CaptureProject JSON file
back into a CaptureProject model.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .capture_project import (
    CaptureCue,
    CaptureFixture,
    CaptureProject,
    CaptureUniverse,
)


class CaptureJsonLoader:
    """
    Deserialize CaptureProject JSON data.
    """

    def from_dict(
        self,
        data: dict[str, Any],
    ) -> CaptureProject:
        """
        Create a CaptureProject from a dictionary.
        """

        project_data = data.get(
            "project",
            {},
        )

        project = CaptureProject(
            name=project_data.get(
                "name",
                "Recovered Capture Project",
            ),
            metadata=project_data.get(
                "metadata",
                {},
            ),
        )

        for item in data.get(
            "fixtures",
            [],
        ):
            project.add_fixture(
                CaptureFixture(
                    name=item.get(
                        "name",
                        "",
                    ),
                    universe=item.get(
                        "universe",
                        0,
                    ),
                    address=item.get(
                        "address",
                        0,
                    ),
                    manufacturer=item.get(
                        "manufacturer",
                    ),
                    model=item.get(
                        "model",
                    ),
                    mode=item.get(
                        "mode",
                    ),
                    properties=item.get(
                        "properties",
                        {},
                    ),
                )
            )

        for item in data.get(
            "universes",
            [],
        ):
            project.add_universe(
                CaptureUniverse(
                    name=item.get(
                        "name",
                        "",
                    ),
                    universe=item.get(
                        "universe",
                        0,
                    ),
                    protocol=item.get(
                        "protocol",
                    ),
                    properties=item.get(
                        "properties",
                        {},
                    ),
                )
            )

        for item in data.get(
            "cues",
            [],
        ):
            project.add_cue(
                CaptureCue(
                    name=item.get(
                        "name",
                        "",
                    ),
                    number=item.get(
                        "number",
                        0,
                    ),
                    properties=item.get(
                        "properties",
                        {},
                    ),
                )
            )

        return project

    def load(
        self,
        path: str | Path,
    ) -> CaptureProject:
        """
        Load a CaptureProject from a JSON file.
        """

        path = Path(path)

        data = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )

        return self.from_dict(
            data,
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}()"
        )