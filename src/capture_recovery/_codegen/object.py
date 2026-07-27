"""
Fluent object definition builder.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Field:
    """
    Definition of one object field.
    """

    name: str
    type_name: str
    required: bool = False


@dataclass(slots=True, frozen=True)
class Object:
    """
    Fluent object definition.
    """

    name: str
    fields: tuple[Field, ...] = field(default_factory=tuple)

    def add(
        self,
        type_name: str,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        """
        Return a new object with an additional field.
        """
        return Object(
            name=self.name,
            fields=(
                *self.fields,
                Field(
                    name=name,
                    type_name=type_name,
                    required=required,
                ),
            ),
        )

    def string(
        self,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        return self.add(
            "string",
            name,
            required=required,
        )

    def uint8(
        self,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        return self.add(
            "uint8",
            name,
            required=required,
        )

    def uint16(
        self,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        return self.add(
            "uint16",
            name,
            required=required,
        )

    def uint32(
        self,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        return self.add(
            "uint32",
            name,
            required=required,
        )

    def float32(
        self,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        return self.add(
            "float32",
            name,
            required=required,
        )

    def vector2(
        self,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        return self.add(
            "vector2",
            name,
            required=required,
        )

    def vector3(
        self,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        return self.add(
            "vector3",
            name,
            required=required,
        )

    def boolean(
        self,
        name: str,
        *,
        required: bool = False,
    ) -> "Object":
        return self.add(
            "boolean",
            name,
            required=required,
        )

    @property
    def field_count(self) -> int:
        """
        Number of fields.
        """
        return len(self.fields)