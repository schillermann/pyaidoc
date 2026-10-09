import inspect
from typing import Any, Callable


class EmptyDocstring:
    """Null object when no docstring is present."""

    def text(self) -> str:
        return "Keine Beschreibung verfügbar."

    def summary(self) -> str:
        return "Keine Beschreibung verfügbar."

    def __str__(self) -> str:
        return self.text()


class Docstring:
    """Extracts docstring from a callable without returning null."""

    def __init__(self, origin: Callable[..., Any]) -> None:
        self._origin = origin

    def text(self) -> str:
        doc = inspect.getdoc(self._origin)
        if not doc or not doc.strip():
            return EmptyDocstring().text()
        return doc.strip()

    def summary(self) -> str:
        full_text = self.text()
        lines = full_text.splitlines()
        return lines[0].strip() if lines else EmptyDocstring().summary()

    def __str__(self) -> str:
        return self.text()
