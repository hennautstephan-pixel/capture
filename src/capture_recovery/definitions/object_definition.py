"""
Definition of an object to generate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .field_definition import FieldDefinition


@dataclass(slots=True, frozen=True)
class ObjectDefinition:
    """
    Immutable description of an object to generate.
    """

    name: str
    description: str = ""
    fields: tuple[FieldDefinition, ...] = field(default_factory=tuple)
    imports: tuple[str, ...] = field(default_factory=tuple)
    base_class: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def add_field(
        self,
        definition: FieldDefinition,
    ) -> "ObjectDefinition":
        """
        Return a copy with an additional field.
        """
        return ObjectDefinition(
            name=self.name,
            description=self.description,
            fields=(*self.fields, definition),
            imports=self.imports,
            base_class=self.base_class,
            metadata=self.metadata.copy(),
        )

    def add_import(
        self,
        module: str,
    ) -> "ObjectDefinition":
        """
        Return a copy with an additional import.
        """
        return ObjectDefinition(
            name=self.name,
            description=self.description,
            fields=self.fields,
            imports=(*self.imports, module),
            base_class=self.base_class,
            metadata=self.metadata.copy(),
        )

    @property
    def field_names(self) -> tuple[str, ...]:
        """
        Return the field names.
        """
        return tuple(field.name for field in self.fields)

    @property
    def field_count(self) -> int:
        """
        Return the number of fields.
        """
        return len(self.fields)