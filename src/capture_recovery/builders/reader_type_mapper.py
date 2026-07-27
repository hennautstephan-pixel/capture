"""
Map Python types to BinaryReader methods.
"""

from __future__ import annotations

from typing import Any


class ReaderTypeMapper:
    """
    Map Python types to BinaryReader methods.
    """

    _MAPPING = {
        str: "read_string()",
        int: "read_uint32()",
        float: "read_float()",
        bool: "read_bool()",
    }

    def method_for(
        self,
        python_type: type | Any,
    ) -> str:
        """
        Return the BinaryReader method for a Python type.
        """

        return self._MAPPING.get(
            python_type,
            "read_object()",
        )