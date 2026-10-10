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


class Success:
    """Represents a successful process outcome (0)."""

    def value(self) -> int:
        return 0

    def ok(self) -> bool:
        return True

    def __int__(self) -> int:
        return self.value()

    def __eq__(self, other: Any) -> bool:
        return hasattr(other, "ok") and other.ok() is True

    def __repr__(self) -> str:
        return "Success(0)"


class Failure:
    """Represents a failed process outcome (1) with a required reason."""

    def __init__(self, reason: str) -> None:
        self._reason = reason

    def value(self) -> int:
        return 1

    def ok(self) -> bool:
        return False

    def reason(self) -> str:
        return self._reason

    def __int__(self) -> int:
        return self.value()

    def __eq__(self, other: Any) -> bool:
        return (
            hasattr(other, "ok")
            and other.ok() is False
            and hasattr(other, "reason")
            and other.reason() == self._reason
        )

    def __repr__(self) -> str:
        return f"Failure('{self._reason}')"
