"""CapabilityTool adapting domain capability objects into pure Tools in Pure OOP."""

import re
from typing import Any
from pyaidoc.docstring import Docstring
from pyaidoc.parameters import CallableParameters
from pyaidoc.tool import Parameters


class CapabilityTool:
    """Adapts a domain capability object with an execute() method into a Tool in Pure OOP."""

    def __init__(self, origin: Any) -> None:
        self._origin = origin

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
        doc = Docstring(self._origin).clean_text()
        if doc and doc != "Keine Beschreibung verfügbar.":
            return doc
        return Docstring(getattr(self._origin, "execute")).clean_text()

    def parameters(self) -> Parameters:
        return CallableParameters(getattr(self._origin, "execute"))

    def __str__(self) -> str:
        return self.name()
