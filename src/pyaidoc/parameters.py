import inspect
from typing import Any, Callable, Iterator
from pyaidoc.parameter import Parameter


class Parameters:
    """Derives parameters from a callable signature without side effects."""

    def __init__(self, origin: Callable[..., Any]) -> None:
        self._origin = origin

    def items(self) -> list[Parameter]:
        signature = inspect.signature(self._origin)
        return [
            Parameter(param)
            for param in signature.parameters.values()
            if param.name not in ("self", "cls")
        ]

    def empty(self) -> bool:
        return len(self.items()) == 0

    def __iter__(self) -> Iterator[Parameter]:
        return iter(self.items())

    def __len__(self) -> int:
        return len(self.items())
