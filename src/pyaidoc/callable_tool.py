"""CallableTool adapter in Pure OOP."""

from typing import Any, Callable
from pyaidoc.docstring import Docstring
from pyaidoc.parameters import CallableParameters
from pyaidoc.tool import Tool, Parameters


class CallableTool:
    """Adapts a Python callable into an autonomous AI tool in Pure OOP."""

    def __init__(self, origin: Callable[..., Any]) -> None:
        self._origin = origin

    def name(self) -> str:
        if hasattr(self._origin, "__name__"):
            return self._origin.__name__
        return self._origin.__class__.__name__

    def description(self) -> str:
        return Docstring(self._origin).text()

    def parameters(self) -> Parameters:
        return CallableParameters(self._origin)

    def __str__(self) -> str:
        return self.name()
