"""
Capture project writer.

Exports reconstructed Capture projects
with fixtures, structures, bindings
and scene hierarchy.
"""

from __future__ import annotations

import json
from pathlib import Path



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


        path = Path(
            path
        )


        path.parent.mkdir(
            parents=True,
            exist_ok=True,
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

            "name":
                project.name,


            "fixtures":

                [

                    {

                        "name":
                            fixture.name,

                        "universe":
                            fixture.universe,

                        "address":
                            fixture.address,

                        "manufacturer":
                            fixture.manufacturer,

                        "model":
                            fixture.model,

                        "mode":
                            fixture.mode,

                        "properties":
                            fixture.properties,

                    }

                    for fixture
                    in project.fixtures

                ],



            "structures":

                [

                    self._serialize_object(
                        item
                    )

                    for item
                    in project.structures

                ],



            "bindings":

                [

                    self._serialize_object(
                        item
                    )

                    for item
                    in project.bindings

                ],



            "scene":

                self._serialize_scene(
                    project.scene
                ),



            "groups":

                [

                    self._serialize_object(
                        item
                    )

                    for item
                    in project.groups

                ],



            "cues":

                [

                    self._serialize_object(
                        item
                    )

                    for item
                    in project.cues

                ],



            "universes":

                [

                    self._serialize_object(
                        item
                    )

                    for item
                    in project.universes

                ],



            "metadata":
                project.metadata,

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

            "nodes":

                [

                    {

                        "name":
                            node.name,

                        "parent":
                            node.parent,

                        "children":
                            node.children,

                        "properties":
                            node.properties,

                    }

                    for node
                    in scene.nodes.values()

                ]

        }



    def _serialize_object(
        self,
        obj,
    ) -> dict:
        """
        Generic serializer.

        Supports:
        - dataclass
        - dataclass(slots=True)
        - normal objects
        """

        if obj is None:

            return {}



        if hasattr(
            obj,
            "__dataclass_fields__",
        ):

            return {

                field:
                    self._serialize_value(
                        getattr(
                            obj,
                            field,
                        )
                    )

                for field
                in obj.__dataclass_fields__

                if hasattr(
                    obj,
                    field,
                )

            }



        if hasattr(
            obj,
            "__slots__",
        ):

            return {

                key:
                    self._serialize_value(
                        getattr(
                            obj,
                            key,
                        )
                    )

                for key
                in obj.__slots__

                if hasattr(
                    obj,
                    key,
                )

            }



        if hasattr(
            obj,
            "__dict__",
        ):

            return {

                key:
                    self._serialize_value(
                        value
                    )

                for key, value
                in obj.__dict__.items()

            }



        return {

            "value":
                str(obj)

        }



    def _serialize_value(
        self,
        value,
    ):
        """
        Convert nested objects.
        """

        if value is None:

            return None



        if isinstance(
            value,
            (str, int, float, bool),
        ):

            return value



        if isinstance(
            value,
            list,
        ):

            return [

                self._serialize_value(
                    item
                )

                for item
                in value

            ]



        if isinstance(
            value,
            dict,
        ):

            return {

                key:
                    self._serialize_value(
                        item
                    )

                for key, item
                in value.items()

            }



        if hasattr(
            value,
            "__dataclass_fields__",
        ):

            return self._serialize_object(
                value
            )



        if hasattr(
            value,
            "__slots__",
        ):

            return self._serialize_object(
                value
            )



        return str(
            value
        )