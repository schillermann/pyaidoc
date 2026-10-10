"""Parameter default value representation in Pure OOP."""

import html
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Default(Protocol):
    """Represents an optional default value of a parameter."""

    def text(self) -> str:
        """Textual display of the default value."""
        ...

    def html(self) -> str:
        """HTML rendering of the default value."""
        ...

    def present(self) -> bool:
        """Returns True if a default value is present."""
        ...

    def empty(self) -> bool:
        """Returns True if no default value is present."""
        ...

    def value(self) -> Any:
        """Returns the underlying default value."""
        ...


class NoDefault:
    """Null object representing the absence of a default value."""

    def __init__(self, fallback: str = "—") -> None:
        self._fallback = fallback

    def text(self) -> str:
        return self._fallback

    def html(self) -> str:
        return f'<span class="pyaidoc-empty">{html.escape(self._fallback)}</span>'

    def present(self) -> bool:
        return False

    def empty(self) -> bool:
        return True

    def value(self) -> Any:
        return None

    def __str__(self) -> str:
        return self.text()


class StringDefaultValue:
    """Encapsulates quoted string representation for defaults."""

    def __init__(self, value: Any) -> None:
        self._value = value

    def matched(self) -> bool:
        return hasattr(self._value, "startswith") and hasattr(self._value, "capitalize")

    def text(self) -> str:
        return f'"{self._value}"'


class FallbackDefaultValue:
    """Encapsulates string representation for arbitrary default values."""

    def __init__(self, value: Any) -> None:
        self._value = value

    def matched(self) -> bool:
        return True

    def text(self) -> str:
        return str(self._value)


class DefaultValueCandidates:
    """Candidate formatters for parameter default values."""

    def __init__(self, value: Any) -> None:
        self._value = value

    def all(self) -> tuple[Any, ...]:
        return (
            StringDefaultValue(self._value),
            FallbackDefaultValue(self._value),
        )


class PresentDefault:
    """Represents a present parameter default value."""

    def __init__(self, value: Any) -> None:
        self._value = value

    def text(self) -> str:
        for candidate in DefaultValueCandidates(self._value).all():
            if candidate.matched():
                return candidate.text()
        return str(self._value)

    def html(self) -> str:
        return f"<code>{html.escape(self.text())}</code>"

    def present(self) -> bool:
        return True

    def empty(self) -> bool:
        return False

    def value(self) -> Any:
        return self._value

    def __str__(self) -> str:
        return self.text()
