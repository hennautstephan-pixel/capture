"""
Capture project writer.

Exports reconstructed Capture projects
with fixtures, structures, bindings
and scene hierarchy.
"""

from __future__ import annotations

import json


class CaptureProjectWriter:
    """
    Write CaptureProject objects.
    """

    def write(
        self,
        project,
        path,
    ) -> None:
        """
        Export project as JSON.
        """

        data = self.to_dict(
            project,
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False,
            )


    def to_dict(
        self,
        project,
    ) -> dict:
        """
        Convert CaptureProject into
        serializable dictionary.
        """

        return {

            "name": project.name,


            "fixtures": [

                {

                    "name": fixture.name,

                    "universe": fixture.universe,

                    "address": fixture.address,

                    "manufacturer": fixture.manufacturer,

                    "model": fixture.model,

                    "mode": fixture.mode,

                    "properties": fixture.properties,

                }

                for fixture in project.fixtures

            ],


            "structures": [

                self._serialize_object(
                    structure,
                )

                for structure in project.structures

            ],


            "bindings": [

                self._serialize_object(
                    binding,
                )

                for binding in project.bindings

            ],


            "scene": self._serialize_scene(
                project.scene,
            ),


            "groups": [

                self._serialize_object(
                    group,
                )

                for group in project.groups

            ],


            "cues": [

                self._serialize_object(
                    cue,
                )

                for cue in project.cues

            ],


            "universes": [

                self._serialize_object(
                    universe,
                )

                for universe in project.universes

            ],


            "metadata": project.metadata,

        }


    def _serialize_scene(
        self,
        scene,
    ) -> dict:
        """
        Serialize CaptureScene.
        """

        if scene is None:

            return {
                "nodes": []
            }


        return {

            "nodes": [

                {

                    "name": node.name,

                    "parent": node.parent,

                    "children": node.children,

                    "properties": node.properties,

                }

                for node in scene.nodes.values()

            ]

        }


    def _serialize_object(
        self,
        obj,
    ) -> dict:
        """
        Generic object serializer.
        """

        if hasattr(
            obj,
            "__dict__",
        ):

            return obj.__dict__


        if hasattr(
            obj,
            "__slots__",
        ):

            return {

                key: getattr(
                    obj,
                    key,
                )

                for key in obj.__slots__

                if hasattr(
                    obj,
                    key,
                )

            }


        return {
            "value": str(obj)
        }