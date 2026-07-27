"""
Python source code writer.
"""

from __future__ import annotations

from capture_recovery.python.python_module import PythonModule
from .code_writer import CodeWriter


class PythonWriter:
    """
    Render a PythonModule into Python source code.
    """

    def write(self, module: PythonModule) -> str:
        writer = CodeWriter()

        # Module docstring
        if module.docstring:
            writer.line('"""')
            writer.line(module.docstring)
            writer.line('"""')
            writer.blank()

        # Imports
        for import_ in sorted(module.imports):
            writer.line(import_.render())

        if module.imports:
            writer.blank()

        # Module constants
        for constant in module.constants:
            if constant.documentation:
                writer.line(f"# {constant.documentation}")

            writer.line(constant.render())

        if module.constants:
            writer.blank()

        # Classes
        for class_index, cls in enumerate(module.classes):

            for decorator in cls.decorators:
                writer.line(f"@{decorator}")

            declaration = f"class {cls.name}"

            if cls.bases:
                declaration += f"({', '.join(cls.bases)})"

            declaration += ":"

            writer.line(declaration)
            writer.indent()

            if cls.docstring:
                writer.line('"""')
                writer.line(cls.docstring)
                writer.line('"""')
                writer.blank()

            if cls.fields:
                for field in cls.fields:
                    writer.line(field.render())

                if cls.methods:
                    writer.blank()

            if cls.methods:
                for method_index, method in enumerate(cls.methods):

                    for decorator in method.decorators:
                        writer.line(f"@{decorator}")

                    signature = f"def {method.name}("
                    signature += ", ".join(method.parameters)
                    signature += ")"

                    if method.return_type:
                        signature += f" -> {method.return_type}"

                    signature += ":"

                    writer.line(signature)
                    writer.indent()

                    if method.body:
                        for line in method.body:
                            writer.line(line)
                    else:
                        writer.line("pass")

                    writer.dedent()

                    if method_index < len(cls.methods) - 1:
                        writer.blank()

            elif not cls.fields:
                writer.line("pass")

            writer.dedent()

            if class_index < len(module.classes) - 1:
                writer.blank()

        return writer.render()