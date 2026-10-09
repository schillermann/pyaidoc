import html
from typing import Any, Protocol


class Default(Protocol):
    """Represents an optional default value of a parameter."""


    def text(self) -> str:
        ...

    def html(self) -> str:
        ...

    def present(self) -> bool:
        ...


class NoDefault:
    """Null object representing the absence of a default value."""

    def text(self) -> str:
        return "—"

    def html(self) -> str:
        return '<span class="pyaidoc-empty">—</span>'

    def present(self) -> bool:
        return False

    def __str__(self) -> str:
        return self.text()


class PresentDefault:
    """Represents a present parameter default value."""

    def __init__(self, value: Any) -> None:
        self._value = value

    def text(self) -> str:
        if isinstance(self._value, str):
            return f'"{self._value}"'
        return str(self._value)

    def html(self) -> str:
        return f"<code>{html.escape(self.text())}</code>"

    def present(self) -> bool:
        return True

    def __str__(self) -> str:
        return self.text()
