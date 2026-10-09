import inspect
from typing import Any


class TypeName:
    """Extracts human-readable name from a type annotation in Pure OOP."""

    def __init__(self, annotation: Any) -> None:
        self._annotation = annotation

    def text(self) -> str:
        if self._annotation is inspect._empty:
            return "Any"
        if isinstance(self._annotation, type):
            return self._annotation.__name__
        return str(self._annotation).replace("typing.", "")

    def __str__(self) -> str:
        return self.text()
