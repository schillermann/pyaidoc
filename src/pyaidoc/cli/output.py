"""Output stream abstractions in Pure OOP."""

from io import StringIO
import sys
from typing import Protocol, TextIO


class Output(Protocol):
    """Contract for text output destinations."""

    def print(self, text: str) -> "Output":
        """Emits a line of text and returns self."""
        ...


class Stdout:
    """Standard console output wrapping a stream."""

    def __init__(self, stream: TextIO = sys.stdout) -> None:
        self._stream = stream

    def print(self, text: str) -> "Stdout":
        self._stream.write(f"{text}\n")
        self._stream.flush()
        return self


class MemoryOutput:
    """In-memory output stream collector wrapping a StringIO buffer."""

    def __init__(self, stream: StringIO) -> None:
        self._stream = stream

    @classmethod
    def empty(cls) -> "MemoryOutput":
        """Secondary constructor providing an empty in-memory stream."""
        return cls(StringIO())

    def print(self, text: str) -> "MemoryOutput":
        self._stream.write(f"{text}\n")
        return self

    def text(self) -> str:
        """Returns collected text from the stream buffer."""
        return self._stream.getvalue()

    def lines(self) -> tuple[str, ...]:
        """Returns tuple of lines without trailing newline."""
        content = self.text()
        return tuple(content.splitlines()) if content else ()
