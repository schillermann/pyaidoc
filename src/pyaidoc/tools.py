"""Immutable collections of AI agent tools in Pure OOP."""

from typing import Any, Iterator
from pyaidoc.tool import Tool, Tools as ToolsProtocol
from pyaidoc.adapted_tool import AdaptedTool


class ToolsCollection:
    """Concrete immutable collection of typed Tool objects."""

    def __init__(self, *items: Tool) -> None:
        self._items = items

    def all(self) -> tuple[Tool, ...]:
        return self._items

    def plus(self, tool: Tool) -> "ToolsCollection":
        return ToolsCollection(*self._items, tool)

    def empty(self) -> bool:
        return len(self._items) == 0

    def __iter__(self) -> Iterator[Tool]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)


Tools = ToolsCollection


class AdaptedTools:
    """Envelope adapting arbitrary callables, schemas, or tools with 100% code-free constructor."""

    def __init__(self, *items: Any) -> None:
        self._items = items

    def all(self) -> tuple[Tool, ...]:
        return tuple(AdaptedTool(item) for item in self._items)

    def plus(self, tool: Any) -> "AdaptedTools":
        return AdaptedTools(*self._items, tool)

    def empty(self) -> bool:
        return len(self._items) == 0

    def __iter__(self) -> Iterator[Tool]:
        return iter(self.all())

    def __len__(self) -> int:
        return len(self._items)
