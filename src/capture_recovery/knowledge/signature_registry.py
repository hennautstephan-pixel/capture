from __future__ import annotations

from .signature import Signature


class SignatureRegistry:
    """
    Registry storing every known semantic signature.

    The registry is intentionally lightweight. It only stores signatures
    and provides simple lookup methods. Matching is performed by the
    SignatureEngine.
    """

    def __init__(self) -> None:
        self._signatures: list[Signature] = []

    def register(
        self,
        signature: Signature,
    ) -> None:
        """
        Register a new signature.

        Raises
        ------
        ValueError
            If a signature with the same name already exists.
        """

        if self.get(signature.name) is not None:
            raise ValueError(
                f"Signature '{signature.name}' already registered."
            )

        self._signatures.append(signature)

    def unregister(
        self,
        name: str,
    ) -> bool:
        """
        Remove a signature by name.

        Returns
        -------
        bool
            True if the signature existed.
        """

        name = name.lower()

        for index, signature in enumerate(self._signatures):

            if signature.name.lower() == name:
                del self._signatures[index]
                return True

        return False

    def clear(self) -> None:
        """
        Remove every registered signature.
        """

        self._signatures.clear()

    def get(
        self,
        name: str,
    ) -> Signature | None:
        """
        Return a signature by name.
        """

        name = name.lower()

        for signature in self._signatures:

            if signature.name.lower() == name:
                return signature

        return None

    def contains(
        self,
        name: str,
    ) -> bool:
        """
        Return True if a signature exists.
        """

        return self.get(name) is not None

    @property
    def signatures(self) -> tuple[Signature, ...]:
        """
        Return every registered signature.
        """

        return tuple(self._signatures)

    def __contains__(
        self,
        name: str,
    ) -> bool:
        return self.contains(name)

    def __len__(self) -> int:
        return len(self._signatures)

    def __iter__(self):
        return iter(self._signatures)

    def __getitem__(
        self,
        index: int,
    ) -> Signature:
        return self._signatures[index]

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(count={len(self)})"
        )