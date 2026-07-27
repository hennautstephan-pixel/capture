"""
Generator producing a Python dataclass from an ObjectDefinition.
"""

from __future__ import annotations

from pathlib import Path

from capture_recovery.definitions.object_definition import ObjectDefinition
from capture_recovery.python.python_class import PythonClass
from capture_recovery.python.python_field import PythonField
from capture_recovery.python.python_import import PythonImport
from capture_recovery.python.python_module import PythonModule
from capture_recovery.writers.python_writer import PythonWriter

from .base import Generator
from .context import GenerationContext
from .generated_file import GeneratedFile


class ObjectGenerator(Generator):
    """
    Generate a Python dataclass from an ObjectDefinition.
    """

    @property
    def name(self) -> str:
        return "object"

    def generate(
        self,
        definition: ObjectDefinition,
        context: GenerationContext,
    ) -> tuple[GeneratedFile, ...]:

        module = PythonModule(
            name=definition.name.lower(),
        )

        module = module.add_import(
            PythonImport(
                module="dataclasses",
                names=("dataclass",),
            )
        )

        cls = PythonClass(
            name=definition.name,
        )

        cls = cls.add_decorator(
            "dataclass(slots=True, frozen=True)"
        )

        for field in definition.fields:

            cls = cls.add_field(
                PythonField(
                    name=field.name,
                    annotation=field.type_name,
                    default=field.default,
                    documentation=field.documentation,
                )
            )

        module = module.add_class(cls)

        source = PythonWriter().write(module)

        generated = GeneratedFile(
            path=context.resolve(
                Path(f"{definition.name.lower()}.py")
            ),
            content=source,
        )

        return (generated,)