"""
Registry for code generators.
"""

from __future__ import annotations

from collections.abc import Iterator

from .base import Generator


class GeneratorRegistry:
    """
    Registry of available generators.
    """

    def __init__(self) -> None:
        self._generators: dict[str, Generator] = {}

    def register(self, generator: Generator) -> None:
        """
        Register a generator.

        Raises
        ------
        ValueError
            If another generator with the same name is already registered.
        """
        if generator.name in self._generators:
            raise ValueError(
                f"Generator '{generator.name}' is already registered."
            )

        self._generators[generator.name] = generator

    def unregister(self, name: str) -> None:
        """
        Remove a generator from the registry.
        """
        self._generators.pop(name, None)

    def get(self, name: str) -> Generator:
        """
        Return a generator by name.

        Raises
        ------
        KeyError
            If the generator does not exist.
        """
        return self._generators[name]

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and name in self._generators

    def __len__(self) -> int:
        return len(self._generators)

    def __iter__(self) -> Iterator[Generator]:
        return iter(self._generators.values())

    def names(self) -> tuple[str, ...]:
        """
        Return the registered generator names.
        """
        return tuple(self._generators.keys())

    def generators(self) -> tuple[Generator, ...]:
        """
        Return all registered generators.
        """
        return tuple(self._generators.values())

    def clear(self) -> None:
        """
        Remove every registered generator.
        """
        self._generators.clear()