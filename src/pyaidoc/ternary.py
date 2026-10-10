"""Ternary conditional object in Pure OOP."""

from typing import Any


class Ternary:
    """Encapsulates a condition-driven value in Pure OOP without imperative branching."""

    def __init__(self, condition: bool, consequent: Any, alternative: Any) -> None:
        self._condition = condition
        self._consequent = consequent
        self._alternative = alternative

    def value(self) -> Any:
        """Resolves the branch according to the condition."""
        return self._consequent if self._condition else self._alternative

    def __str__(self) -> str:
        return str(self.value())
