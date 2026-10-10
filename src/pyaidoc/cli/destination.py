"""File destination abstractions in Pure OOP."""

from io import StringIO
from pathlib import Path
from typing import Protocol


class FileDestination(Protocol):
    """Contract for saving generated document content."""

    def write(self, content: str) -> "FileDestination":
        """Saves content to the destination and returns self."""
        ...

    def path(self) -> Path:
        """Returns the file path or location."""
        ...


class LocalFile:
    """Encapsulates a file on the local filesystem."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def write(self, content: str) -> "LocalFile":
        self._path.write_text(content, encoding="utf-8")
        return self

    def path(self) -> Path:
        return self._path


class MemoryFile:
    """In-memory file destination for zero-I/O testing wrapping a StringIO stream."""

    def __init__(self, virtual_path: Path, stream: StringIO) -> None:
        self._virtual_path = virtual_path
        self._stream = stream

    @classmethod
    def empty(cls, virtual_path: Path = Path("virtual.html")) -> "MemoryFile":
        """Secondary constructor providing an empty in-memory file stream."""
        return cls(virtual_path, StringIO())

    def write(self, content: str) -> "MemoryFile":
        self._stream.write(content)
        return self

    def content(self) -> str:
        """Returns the stored content."""
        return self._stream.getvalue()

    def path(self) -> Path:
        """Returns the virtual path."""
        return self._virtual_path
