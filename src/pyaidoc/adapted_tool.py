"""AdaptedTool universal envelope adapter in Pure OOP."""

from typing import Any, Protocol, runtime_checkable
from pyaidoc.tool import Tool, Parameters
from pyaidoc.callable_tool import CallableTool
from pyaidoc.schema_tool import SchemaTool
from pyaidoc.capability_tool import CapabilityTool


@runtime_checkable
class AdaptedToolCandidate(Protocol):
    """Candidate strategy for resolving an adapted tool."""

    def matched(self) -> bool:
        """Returns True if origin matches this candidate."""
        ...

    def tool(self) -> Tool:
        """Returns the resolved Tool object."""
        ...


class ExistingToolCandidate:
    """Resolves an origin that already satisfies the Tool protocol."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def matched(self) -> bool:
        return (
            hasattr(self._origin, "parameters")
            and hasattr(self._origin, "name")
            and hasattr(self._origin, "description")
        )

    def tool(self) -> Tool:
        return self._origin


class SchemaToolCandidate:
    """Resolves an origin that behaves as a schema dictionary mapping."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def matched(self) -> bool:
        return hasattr(self._origin, "get") and hasattr(self._origin, "keys")

    def tool(self) -> Tool:
        return SchemaTool(self._origin)


class CapabilityToolCandidate:
    """Resolves an origin that provides an execute() method."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def matched(self) -> bool:
        return hasattr(self._origin, "execute") and callable(getattr(self._origin, "execute"))

    def tool(self) -> Tool:
        return CapabilityTool(self._origin)


class CallableToolCandidate:
    """Resolves an origin that is a callable function or method."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def matched(self) -> bool:
        return callable(self._origin)

    def tool(self) -> Tool:
        return CallableTool(self._origin)


class AdaptedToolCandidates:
    """Collection of candidate resolvers for an adapted origin."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def all(self) -> tuple[AdaptedToolCandidate, ...]:
        return (
            ExistingToolCandidate(self._origin),
            CapabilityToolCandidate(self._origin),
            SchemaToolCandidate(self._origin),
            CallableToolCandidate(self._origin),
        )


class AdaptedTool:
    """Smart envelope adapting callables, dict schemas, or existing tools into a pure Tool."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

    def name(self) -> str:
        return self.delegate().name()

    def description(self) -> str:
        return self.delegate().description()

    def parameters(self) -> Parameters:
        return self.delegate().parameters()

    def delegate(self) -> Tool:
        """Resolves the adapted Tool via candidate polymorphism without isinstance."""
        for candidate in AdaptedToolCandidates(self._origin).all():
            if candidate.matched():
                return candidate.tool()
        return CallableTool(self._origin)

    def __str__(self) -> str:
        return self.name()
