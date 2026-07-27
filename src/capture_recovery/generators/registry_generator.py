"""
Generator producing a registry module.
"""

from __future__ import annotations

from pathlib import Path

from capture_recovery.definitions.object_definition import ObjectDefinition
from capture_recovery.python.python_constant import PythonConstant
from capture_recovery.python.python_import import PythonImport
from capture_recovery.python.python_module import PythonModule

from .context import GenerationContext
from .generated_file import GeneratedFile
from .python_generator import PythonGenerator


class RegistryGenerator(PythonGenerator):
    """
    Generate a registry containing all generated objects.
    """

    @property
    def name(self) -> str:
        return "registry"

    def generate(
        self,
        definitions: tuple[ObjectDefinition, ...],
        context: GenerationContext,
    ) -> tuple[GeneratedFile, ...]:

        module = PythonModule(
            name="registry",
        )

        entries: list[str] = []

        for definition in definitions:

            module = module.add_import(
                PythonImport(
                    module=definition.name.lower(),
                    names=(definition.name,),
                )
            )

            module = module.add_import(
                PythonImport(
                    module=f"{definition.name.lower()}_decoder",
                    names=(f"{definition.name}Decoder",),
                )
            )

            entries.append(
                f'"{definition.name}": '
                "{"
                f'"type": {definition.name}, '
                f'"decoder": {definition.name}Decoder'
                "}"
            )

        registry = "{\n    " + ",\n    ".join(entries) + "\n}"

        module = module.add_constant(
            PythonConstant(
                "REGISTRY",
                registry,
            )
        )

        generated = self.build_file(
            module,
            "registry.py",
            context,
        )

        return (generated,)