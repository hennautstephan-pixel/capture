"""
Generator producing a Python signature module from an ObjectDefinition.
"""

from __future__ import annotations

from pathlib import Path

from capture_recovery.definitions.object_definition import ObjectDefinition
from capture_recovery.python.python_constant import PythonConstant
from capture_recovery.python.python_module import PythonModule
from capture_recovery.writers.python_writer import PythonWriter

from .base import Generator
from .context import GenerationContext
from .generated_file import GeneratedFile


class SignatureGenerator(Generator):
    """
    Generate a signature module for an ObjectDefinition.
    """

    @property
    def name(self) -> str:
        return "signature"

    def generate(
        self,
        definition: ObjectDefinition,
        context: GenerationContext,
    ) -> tuple[GeneratedFile, ...]:

        module = PythonModule(
            name=f"{definition.name.lower()}_signature",
        )

        module = module.add_constant(
            PythonConstant(
                "NAME",
                f'"{definition.name}"',
            )
        )

        module = module.add_constant(
            PythonConstant(
                "FIELD_COUNT",
                str(definition.field_count),
            )
        )

        field_names = ", ".join(
            f'"{field.name}"'
            for field in definition.fields
        )

        if len(definition.fields) == 1:
            field_names += ","

        module = module.add_constant(
            PythonConstant(
                "FIELD_NAMES",
                f"({field_names})",
            )
        )

        field_types = ", ".join(
            field.type_name
            for field in definition.fields
        )

        if len(definition.fields) == 1:
            field_types += ","

        module = module.add_constant(
            PythonConstant(
                "FIELD_TYPES",
                f"({field_types})",
            )
        )

        source = PythonWriter().write(module)

        generated = GeneratedFile(
            path=context.resolve(
                Path(
                    f"{definition.name.lower()}_signature.py"
                )
            ),
            content=source,
        )

        return (generated,)
    