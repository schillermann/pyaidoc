from typing import Any, Iterator
from pyaidoc.tool import Tool


class Tools:
    """Immutable collection of AI agent tools."""

    def __init__(self, *items: Any) -> None:
        self._items = items

    def all(self) -> list[Tool]:
        return [item if isinstance(item, Tool) else Tool(item) for item in self._items]

    def plus(self, tool_or_callable: Any) -> "Tools":
        return Tools(*self._items, tool_or_callable)

    def empty(self) -> bool:
        return len(self._items) == 0

    def __iter__(self) -> Iterator[Tool]:
        return iter(self.all())

    def __len__(self) -> int:
        return len(self._items)
