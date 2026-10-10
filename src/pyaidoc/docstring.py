"""Docstring extraction and null object in Pure OOP."""

import inspect
import re
from typing import Any, Callable


class EmptyDocstring:
    """Null object when no docstring is present."""

    def __init__(self, fallback: str = "Keine Beschreibung verfügbar.") -> None:
        self._fallback = fallback

    def present(self) -> bool:
        return False

    def empty(self) -> bool:
        return True

    def text(self) -> str:
        return self._fallback

    def summary(self) -> str:
        return self._fallback

    def clean_text(self) -> str:
        return self._fallback

    def __str__(self) -> str:
        return self.text()


class Docstring:
    """Extracts docstring from a callable without returning null."""

    def __init__(
        self,
        origin: Callable[..., Any],
        empty: EmptyDocstring = EmptyDocstring(),
    ) -> None:
        self._origin = origin
        self._empty = empty

    def present(self) -> bool:
        doc = inspect.getdoc(self._origin)
        return bool(doc and doc.strip())

    def empty(self) -> bool:
        return not self.present()

    def text(self) -> str:
        doc = inspect.getdoc(self._origin)
        if not doc or not doc.strip():
            return self._empty.text()
        return doc.strip()

    def clean_text(self) -> str:
        raw = self.text()
        match = re.search(r"\n\s*(?:[:@]param|Args:|Parameters:)", raw)
        if match:
            return raw[:match.start()].strip()
        return raw

    def summary(self) -> str:
        full_text = self.text()
        lines = full_text.splitlines()
        return lines[0].strip() if lines else self._empty.summary()

    def __str__(self) -> str:
        return self.text()

