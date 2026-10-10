"""Parameters collection derived from a Python callable in Pure OOP."""

import inspect
from typing import Any, Callable, Iterator
from pyaidoc.parameter import Parameter, CallableParameter
from pyaidoc.tool import Parameters as ParametersProtocol


class CallableParameters:
    """Derives parameters from a callable signature without side effects."""

    def __init__(
        self,
        origin: Callable[..., Any],
        ignored: tuple[str, ...] = ("self", "cls"),
    ) -> None:
        self._origin = origin
        self._ignored = ignored

    def items(self) -> tuple[CallableParameter, ...]:
        signature = inspect.signature(self._origin)
        return tuple(
            CallableParameter(param, self._origin)
            for param in signature.parameters.values()
            if param.name not in self._ignored
            and param.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        )

    def empty(self) -> bool:
        return len(self.items()) == 0

    def __iter__(self) -> Iterator[CallableParameter]:
        return iter(self.items())

    def __len__(self) -> int:
        return len(self.items())


Parameters = CallableParameters
