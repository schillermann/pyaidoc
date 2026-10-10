"""CapabilityTool adapting domain capability objects into pure Tools in Pure OOP."""

import re
from typing import Any
from pyaidoc.docstring import Docstring
from pyaidoc.parameters import CallableParameters
from pyaidoc.tool import Parameters


class CapabilityTool:
    """Adapts a domain capability object with an execute() method into a Tool in Pure OOP."""

    def __init__(self, origin: Any, ignored: tuple[str, ...] = ("self", "cls")) -> None:
        self._origin = origin
        self._ignored = ignored

    def name(self) -> str:
        if hasattr(self._origin, "name") and callable(getattr(self._origin, "name")):
            return str(self._origin.name())
        raw = self._origin.__name__ if hasattr(self._origin, "__name__") else self._origin.__class__.__name__
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", raw).lower()

    def description(self) -> str:
        if hasattr(self._origin, "description") and callable(getattr(self._origin, "description")):
            desc = str(self._origin.description())
            if desc:
                return desc
        exec_doc = Docstring(getattr(self._origin, "execute"))
        if exec_doc.present():
            return exec_doc.clean_text()
        return Docstring(self._origin).clean_text()

    def parameters(self) -> Parameters:
        ignored = (
            tuple(self._origin.ignored_parameters())
            if hasattr(self._origin, "ignored_parameters") and callable(getattr(self._origin, "ignored_parameters"))
            else self._ignored
        )
        return CallableParameters(getattr(self._origin, "execute"), ignored=ignored)

    def __str__(self) -> str:
        return self.name()

