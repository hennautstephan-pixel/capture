from __future__ import annotations


class Registry:

    def __init__(self) -> None:
        self._objects = {}

    def register(self, obj) -> None:
        self._objects[obj.name] = obj

    def get(self, name):
        return self._objects[name]

    def all(self):
        return tuple(self._objects.values())