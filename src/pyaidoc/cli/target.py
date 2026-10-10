"""Tools target resolver for pyaidoc in Pure OOP."""

import importlib
import os
import sys
from typing import Any
from pyaidoc.tool import Tools as ToolsProtocol
from pyaidoc.tools import Tools, AdaptedTools


class TargetCandidates:
    """Candidate specifications for discovering tools."""

    def __init__(self, target: str = "") -> None:
        self._target = target

    def all(self) -> tuple[str, ...]:
        if self._target:
            return (self._target,)
        env = os.getenv("PYAIDOC_TOOLS", "")
        if env:
            return (env,)
        return (
            "chat.capabilities.capability_specs:CapabilitySpecs",
            "capabilities.specs:CapabilitySpecs",
            "capabilities:tools",
            "tools:tools",
        )


class CandidateSpec:
    """Encapsulates a module and attribute target specification."""

    def __init__(self, spec: str) -> None:
        self._spec = spec

    def module_name(self) -> str:
        return self._spec.split(":", 1)[0] if ":" in self._spec else self._spec

    def attribute_name(self) -> str:
        return self._spec.split(":", 1)[1] if ":" in self._spec else "tools"


class CandidateTools:
    """Attempts to resolve tools from a candidate specification in Pure OOP."""

    def __init__(self, spec: CandidateSpec) -> None:
        self._spec = spec

    def tools(self) -> ToolsProtocol:
        try:
            module = importlib.import_module(self._spec.module_name())
            obj: Any = getattr(module, self._spec.attribute_name())
            instance: Any = obj() if callable(obj) and not hasattr(obj, "all") else obj
            list_method: Any = getattr(instance, "list", None)
            items: Any = list_method() if callable(list_method) else instance
            if hasattr(items, "all"):
                return items
            return AdaptedTools(*items)
        except (ModuleNotFoundError, AttributeError):
            pass
        return Tools()


class SearchPaths:
    """Search directories for candidate module resolution."""

    def __init__(self, root: str) -> None:
        self._root = root

    def all(self) -> tuple[str, ...]:
        parent = os.path.dirname(self._root)
        return (
            self._root,
            os.path.join(self._root, "backend"),
            parent,
            os.path.join(parent, "backend"),
        )


class ToolsTarget:
    """Resolves and loads an AI tools collection from target specifications."""

    def __init__(self, target: str = "") -> None:
        self._target = target

    def candidates(self) -> tuple[str, ...]:
        return TargetCandidates(self._target).all()

    def tools(self) -> ToolsProtocol:
        for directory in SearchPaths(os.getcwd()).all():
            if os.path.isdir(directory) and directory not in sys.path:
                sys.path.insert(0, directory)

        for spec_str in self.candidates():
            found = CandidateTools(CandidateSpec(spec_str)).tools()
            if not found.empty():
                return found

        return Tools()
