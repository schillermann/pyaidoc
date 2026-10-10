"""Type name resolution for annotations in Pure OOP."""

import inspect
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class TypeNameCandidate(Protocol):
    """Candidate strategy for extracting a type representation."""

    def matched(self) -> bool:
        """Returns True if this candidate can resolve the annotation."""
        ...

    def text(self) -> str:
        """Returns the formatted type name."""
        ...


class StrippedPrefix:
    """Removes a prefix string if present in pure OOP."""

    def __init__(self, text: str, prefix: str) -> None:
        self._text = text
        self._prefix = prefix

    def text(self) -> str:
        if self._text.startswith(self._prefix):
            return self._text[len(self._prefix):]
        return self._text

    def __str__(self) -> str:
        return self.text()


class EmptyTypeName:
    """Resolves empty annotations to 'Any'."""

    def __init__(self, annotation: Any) -> None:
        self._annotation = annotation

    def matched(self) -> bool:
        return self._annotation is inspect.Parameter.empty or self._annotation is inspect._empty

    def text(self) -> str:
        return "Any"


class NamedTypeName:
    """Resolves standard named classes and types to their __name__."""

    def __init__(self, annotation: Any) -> None:
        self._annotation = annotation

    def matched(self) -> bool:
        return (
            hasattr(self._annotation, "__name__")
            and not hasattr(self._annotation, "__origin__")
            and getattr(self._annotation, "__name__") != "_empty"
        )

    def text(self) -> str:
        return str(getattr(self._annotation, "__name__"))


class FallbackTypeName:
    """Resolves arbitrary or generic annotations using stripped representation."""

    def __init__(self, annotation: Any) -> None:
        self._annotation = annotation

    def matched(self) -> bool:
        return True

    def text(self) -> str:
        return str(StrippedPrefix(str(self._annotation), "typing."))


class TypeNameCandidates:
    """Provides candidate resolvers for an annotation."""

    def __init__(self, annotation: Any) -> None:
        self._annotation = annotation

    def all(self) -> tuple[TypeNameCandidate, ...]:
        return (
            EmptyTypeName(self._annotation),
            NamedTypeName(self._annotation),
            FallbackTypeName(self._annotation),
        )


class TypeName:
    """Extracts human-readable name from a type annotation in Pure OOP."""

    def __init__(self, annotation: Any) -> None:
        self._annotation = annotation

    def text(self) -> str:
        for candidate in TypeNameCandidates(self._annotation).all():
            if candidate.matched():
                return candidate.text()
        return "Any"

    def __str__(self) -> str:
        return self.text()
