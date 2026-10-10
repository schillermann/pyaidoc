"""Pure OOP protocols for AI agent tools, parameters, and tool collections."""

from typing import Iterator, Protocol
from pyaidoc.default import Default


class Parameter(Protocol):
    """Contract for an individual tool parameter."""

    def name(self) -> str:
        """Name of the parameter."""
        ...

    def type(self) -> str:
        """Rendered type name of the parameter."""
        ...

    def required(self) -> bool:
        """Indicates whether parameter must be provided."""
        ...

    def default(self) -> Default:
        """Default value representation object."""
        ...


class Parameters(Protocol):
    """Contract for a collection of tool parameters."""

    def items(self) -> tuple[Parameter, ...]:
        """Returns immutable tuple of parameters."""
        ...

    def empty(self) -> bool:
        """Indicates whether the parameter collection is empty."""
        ...

    def __iter__(self) -> Iterator[Parameter]:
        """Iterates over parameter objects."""
        ...

    def __len__(self) -> int:
        """Number of parameters in collection."""
        ...


class Tool(Protocol):
    """Contract for an autonomous AI function call or agent tool."""

    def name(self) -> str:
        """Identifier name of the tool."""
        ...

    def description(self) -> str:
        """Human-readable documentation for the tool."""
        ...

    def parameters(self) -> Parameters:
        """Parameter collection for the tool."""
        ...


class Tools(Protocol):
    """Contract for an immutable collection of AI agent tools."""

    def all(self) -> tuple[Tool, ...]:
        """Returns immutable tuple of Tool objects."""
        ...

    def empty(self) -> bool:
        """Indicates whether the collection is empty."""
        ...

    def __iter__(self) -> Iterator[Tool]:
        """Iterates over Tool objects in collection."""
        ...

    def __len__(self) -> int:
        """Number of tools in collection."""
        ...
