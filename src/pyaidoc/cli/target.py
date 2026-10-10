"""Tools target resolver for pyaidoc in Pure OOP."""

import importlib
import os
import sys
from typing import Any
from pyaidoc.tools import Tools


class ToolsTarget:
    """Resolves and loads an AI tools collection from target specifications."""

    def __init__(self, target: str = "") -> None:
        self._target = target

    def candidates(self) -> tuple[str, ...]:
        if self._target:
            return (self._target,)
        env_target = os.getenv("PYAIDOC_TOOLS", "")
        if env_target:
            return (env_target,)
        return (
            "chat.capabilities.capability_specs:CapabilitySpecs",
            "capabilities.specs:CapabilitySpecs",
            "capabilities:tools",
            "tools:tools",
        )

    def tools(self) -> Tools:
        cwd = os.getcwd()
        parent = os.path.dirname(cwd)
        for directory in (cwd, os.path.join(cwd, "backend"), parent, os.path.join(parent, "backend")):
            if os.path.isdir(directory) and directory not in sys.path:
                sys.path.insert(0, directory)

        for candidate in self.candidates():
            try:
                mod_name, attr_name = candidate.split(":", 1) if ":" in candidate else (candidate, "tools")
                module = importlib.import_module(mod_name)
                obj: Any = getattr(module, attr_name)
                instance: Any = obj() if callable(obj) and not isinstance(obj, Tools) else obj
                list_method: Any = getattr(instance, "list", None)
                items = list_method() if callable(list_method) else instance
                if isinstance(items, (list, tuple)):
                    return Tools(*items)
                if isinstance(items, Tools):
                    return items
            except (ImportError, AttributeError):
                continue

        return Tools()
