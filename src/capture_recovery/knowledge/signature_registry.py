"""
Registry of object signatures.
"""

from __future__ import annotations

from collections.abc import Mapping

from capture_recovery.knowledge.signature import Signature


class SignatureRegistry:
    """
    Registry of known object signatures.
    """

    def __init__(
        self,
        signatures: Mapping[str, Signature] | None = None,
    ) -> None:
        self._signatures: dict[str, Signature] = dict(
            signatures or {}
        )

    def register(
        self,
        name: str,
        signature: Signature,
    ) -> None:
        """
        Register an object signature.
        """

        self._signatures[name] = signature

    def signature_for(
        self,
        name: str,
    ) -> Signature:
        """
        Return the signature associated with an object name.
        """

        try:
            return self._signatures[name]
        except KeyError as exc:
            raise KeyError(
                f"No signature registered for '{name}'."
            ) from exc

    def __contains__(
        self,
        name: object,
    ) -> bool:
        return name in self._signatures

    def __len__(self) -> int:
        return len(self._signatures)

    def __iter__(self):
        return iter(self._signatures)

    @property
    def names(self) -> tuple[str, ...]:
        """
        Return registered signature names.
        """

        return tuple(sorted(self._signatures))