"""ExitCode objects in Pure OOP."""

from typing import Any, Protocol


class ExitCode(Protocol):
    """Represents a process exit code object in Pure OOP."""

    def value(self) -> int:
        """Returns the numeric exit code for OS consumption."""
        ...

    def ok(self) -> bool:
        """Indicates whether execution completed successfully."""
        ...


class Success(int):
    """Represents a successful process outcome (0)."""

    def __new__(cls) -> "Success":
        return super().__new__(cls, 0)

    def value(self) -> int:
        return 0

    def ok(self) -> bool:
        return True

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return int(self) == int(other)
        return hasattr(other, "ok") and other.ok() is True

    def __repr__(self) -> str:
        return "Success(0)"


class Failure(int):
    """Represents a failed process outcome (1) with a required reason."""

    _reason: str

    def __new__(cls, reason: str) -> "Failure":
        obj = super().__new__(cls, 1)
        obj._reason = reason
        return obj

    def value(self) -> int:
        return 1

    def ok(self) -> bool:
        return False

    def reason(self) -> str:
        return self._reason

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return int(self) == int(other)
        return (
            hasattr(other, "ok")
            and other.ok() is False
            and hasattr(other, "reason")
            and other.reason() == self._reason
        )

    def __repr__(self) -> str:
        return f"Failure('{self._reason}')"
